"""Local-only natal/name comparison server. Does not load source-app secrets."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import functools
import gzip
import json
import re
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator

PROTOTYPE_ROOT = Path(__file__).resolve().parent
MYSTIC_ROOT = PROTOTYPE_ROOT.parent / "Mystic-Rebels"
if not MYSTIC_ROOT.is_dir():
    MYSTIC_ROOT = PROTOTYPE_ROOT.parents[1]
sys.path.insert(0, str(PROTOTYPE_ROOT))
sys.path.insert(0, str(MYSTIC_ROOT))
from mystic_rebels.models import BirthInput
from mystic_rebels.service import calculate
from mystic_rebels.errors import ChartError
from mystic_rebels import astronomy
from numerology import calculate_numerology, METHODS

MYSTIC_COMMIT = "3d83db75c30b26d9b068576d84ec49554822fd8c"
PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
app = FastAPI(title="Mystic natal comparison prototype", docs_url=None, redoc_url=None, openapi_url=None)


class ComparisonInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    full_name: str = Field(min_length=1, max_length=120)
    birth_date: str
    birth_time: str | None = None
    time_accuracy: Literal["nearest_minute", "approximate", "unknown"] = "nearest_minute"
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1, max_length=100)
    location_name: str = Field(min_length=1, max_length=200)
    coordinate_provenance: str = Field(default="User supplied coordinates", max_length=250)
    uncertainty_seconds: float | None = Field(default=None, ge=0, le=86400)
    fold: Literal[0, 1] | None = None

    @field_validator("full_name")
    @classmethod
    def valid_name(cls, value):
        if not re.search("[A-Za-z]", value):
            raise ValueError("Enter the supplied full birth name using A-Z letters.")
        return value.strip()

    @field_validator("birth_date")
    @classmethod
    def valid_birth_date(cls, value):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Use a birth date in YYYY-MM-DD format.")
        date.fromisoformat(value)
        return value

    @field_validator("birth_time")
    @classmethod
    def valid_birth_time(cls, value):
        if value is None or value == "":
            return None
        if not re.fullmatch(r"\d{2}:\d{2}(:\d{2})?", value):
            raise ValueError("Use a local birth time in HH:MM format.")
        datetime.strptime(value, "%H:%M:%S" if len(value) == 8 else "%H:%M")
        return value


@app.middleware("http")
async def local_headers(request: Request, call_next):
    if request.method == "POST":
        try:
            size = int(request.headers.get("content-length", "0"))
        except ValueError:
            return JSONResponse(status_code=400, content={"error": {"code": "INVALID_SIZE", "message": "Invalid request size."}})
        if size > 32768:
            return JSONResponse(status_code=413, content={"error": {"code": "PAYLOAD_TOO_LARGE", "message": "The form is too large."}})
        origin = request.headers.get("origin")
        if origin and origin not in {"http://127.0.0.1:8766", "http://localhost:8766"}:
            return JSONResponse(status_code=403, content={"error": {"code": "LOCAL_ORIGIN_REQUIRED", "message": "Open this form in its local prototype tab."}})
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.exception_handler(ChartError)
async def chart_error(request, exc):
    return JSONResponse(status_code=422, content={"error": exc.record()})


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    # Do not echo submitted personal inputs in errors/logs.
    fields = [{"field": ".".join(str(part) for part in error["loc"] if part != "body"),
               "message": error["msg"]} for error in exc.errors()]
    message = " ".join(f'{row["field"]}: {row["message"]}' for row in fields)
    return JSONResponse(status_code=422, content={"error": {
        "code": "INVALID_FORM", "message": message, "fields": fields}})


@app.get("/api/health")
def health():
    try:
        with astronomy.LOCK:
            astronomy.initialize()
            astronomy.verify_assets(["sepl_18.se1", "semo_18.se1"])
        return {"status": "ready", "engine": "Mystic Rebels Swiss Ephemeris", "local_only": True,
                "source_commit": MYSTIC_COMMIT, "personal_report_approved": False}
    except ChartError as exc:
        return JSONResponse(status_code=503, content={"status": "unavailable", "error": exc.record()})


def normalize(value: str) -> str:
    return "".join(character for character in unicodedata.normalize("NFKD", value)
                   if not unicodedata.combining(character)).casefold()


@functools.lru_cache(maxsize=1)
def city_rows():
    with gzip.open(MYSTIC_ROOT / "data" / "locations.json.gz", "rt", encoding="utf-8") as stream:
        cities = json.load(stream)
    result = []
    for city in cities:
        label = ", ".join(part for part in [city["name"], city.get("region"), city["country"]] if part)
        key = normalize(" ".join([city["name"], city.get("region", ""), city.get("region_code", ""),
                                  city["country"], city["countrycode"]]))
        result.append({**city, "label": label, "search_key": key, "search_words": key.split()})
    # This smaller city is absent from the source GeoNames population-filtered
    # dataset. Keep the additional primary-source centroid separate and explicit.
    fallback_key = normalize("Los Alamitos California CA United States US")
    result.append({"geonameid": "census-0643224", "name": "Los Alamitos",
                   "label": "Los Alamitos, California, United States",
                   "latitude": 33.7971040, "longitude": -118.0591800,
                   "timezone": "America/Los_Angeles", "population": 0,
                   "search_key": fallback_key, "search_words": fallback_key.split(),
                   "provenance": "US Census Bureau BAS26 incorporated-place centroid, GEOID 0643224; city centroid, not a certified birth address",
                   "source_url": "https://tigerweb.geo.census.gov/tigerwebmain/Files/bas26/tigerweb_bas26_incplace_ca.html"})
    return result


@app.get("/api/locations")
def locations(q: str = Query(min_length=2, max_length=100)):
    search = normalize(" ".join(q.replace(",", " ").split()))
    if not search:
        return []
    terms = search.split()
    found = [row for row in city_rows() if search in row["search_key"] or all(
        any(word.startswith(term) for word in row["search_words"]) for term in terms)]
    found.sort(key=lambda row: (not row["search_key"].startswith(search), -row["population"]))
    return [{"id": row["geonameid"], "name": row["label"], "latitude": row["latitude"],
             "longitude": row["longitude"], "timezone": row["timezone"],
             "provenance": row.get("provenance", f"GeoNames city centroid, geonamescache 3.0.2, ID {row['geonameid']}"),
             "source_url": row.get("source_url", "https://www.geonames.org/")}
            for row in found[:12]]


@app.get("/api/methods")
def methods():
    return {**METHODS, "astrology": {
        "engine_commit": MYSTIC_COMMIT, "center": "geocentric", "zodiac": "tropical",
        "houses": "Whole Sign", "birth_time_status": "User supplied; not independently documented",
        "position_model": "Swiss file backend, apparent ecliptic/equinox of date",
        "blocked_rules_preserved": ["Spark", "complete directional aspect network", "progressions"],
        "personal_report_approved": False,
    }}


@app.get("/api/timezone")
def coordinate_timezone(latitude: float = Query(ge=-90, le=90),
                        longitude: float = Query(ge=-180, le=180)):
    import tzfpy
    return {"timezone": tzfpy.get_tz(longitude, latitude),
            "method": "tzfpy coordinate polygon lookup; historical local clock resolved separately by the pinned IANA database"}


@app.get("/api/sources")
def sources():
    from sources import source_catalog
    return source_catalog()


def build_comparison(data: ComparisonInput):
    unknown = data.time_accuracy == "unknown" or data.birth_time is None
    request = BirthInput(
        name=data.full_name, local_date=data.birth_date, local_time=data.birth_time,
        timezone=data.timezone, fold=data.fold, latitude=data.latitude, longitude=data.longitude,
        location_name=data.location_name, coordinate_provenance=data.coordinate_provenance,
        time_accuracy="unknown" if unknown else data.time_accuracy,
        uncertainty_seconds=None if unknown else (data.uncertainty_seconds if data.uncertainty_seconds is not None else 30 if data.time_accuracy == "nearest_minute" else None),
        objects=PLANETS + ["Ascendant", "Midheaven"], chart_type="natal",
    )
    chart = calculate(request)
    numerology = calculate_numerology(data.full_name, data.birth_date)
    from compare import compose_comparison
    comparison = compose_comparison(chart, numerology)
    limitations = [
        "This is a proposed cross-system research comparison, not an approved PURE personal report or a validated accuracy score.",
        "The supplied name and birth time have not been independently verified against records.",
        "Shared name and birth-date inputs are not independent confirmations.",
        "Daily numerology, transits, Spark, progressions and the full directional aspect network are not used.",
    ]
    if unknown:
        limitations.append("Birth time is unknown. Planet positions use local noon only as a reference; houses and angles are unavailable.")
    elif data.time_accuracy == "approximate":
        limitations.append("Birth time is approximate. Houses, angles and near-boundary placements can change with the unknown timing error.")
    profile = {
        "full_name": data.full_name, "name_basis": "Name as supplied; no additional middle names inferred",
        "birth_date": data.birth_date, "birth_time": data.birth_time,
        "time_accuracy": "unknown" if unknown else data.time_accuracy,
        "birth_time_status": "User supplied, not independently record-verified",
        "latitude": data.latitude, "longitude": data.longitude, "timezone": data.timezone,
        "location_name": data.location_name, "coordinate_provenance": data.coordinate_provenance,
        "fold": data.fold,
        "uncertainty_seconds": request.uncertainty_seconds,
    }
    return {
        "schema_version": "1.0", "product": "Natal comparison prototype",
        "profile": profile, "numerology": numerology, "chart": chart,
        "comparison": comparison, "sources": comparison.get("sources", []),
        "limitations": limitations, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "personal_report_approved": False, "stored_server_side": False,
    }


@app.post("/api/compare")
def compare_endpoint(data: ComparisonInput):
    return build_comparison(data)


class ResearchInput(ComparisonInput):
    year: int = Field(ge=1800, le=2653, strict=True)
    topic: Literal['trust', 'voice', 'autonomy', 'year'] = 'trust'
    annual_name_policy: Literal['birth_name'] = 'birth_name'


@app.post('/api/research')
def research_endpoint(data: ResearchInput):
    from annual_adapter import annual_numbers
    from phsr import assess
    from report_builder import build_reading
    unknown = data.time_accuracy == 'unknown' or data.birth_time is None
    chart = calculate(BirthInput(
        name=data.full_name, local_date=data.birth_date, local_time=data.birth_time,
        timezone=data.timezone, fold=data.fold, latitude=data.latitude, longitude=data.longitude,
        location_name=data.location_name, coordinate_provenance=data.coordinate_provenance,
        time_accuracy='unknown' if unknown else data.time_accuracy,
        uncertainty_seconds=None if unknown else data.uncertainty_seconds if data.uncertainty_seconds is not None else 30,
        objects=PLANETS+['Chiron','Ceres','Pallas','Juno','Vesta','NorthNodeTrue','SouthNodeTrue',
                         'LilithMean','Ascendant','Descendant','Midheaven','ImumCoeli','Vertex','Fortune','Spirit','Love']))
    assessment=assess(chart)
    try:
        annual=annual_numbers(data.full_name,data.birth_date,data.year)
    except ValueError as exc:
        return JSONResponse(status_code=422,content={'error':{'code':'ANNUAL_UNAVAILABLE','message':str(exc)}})
    return {'schema_version':'1.0','chart':chart,'assessment':assessment,'annual':annual,
            'reading':build_reading(assessment,data.topic,annual),
            'profile':data.model_dump(mode='json'),'personal_report_approved':False,
            'stored_server_side':False,'reported_history_used':False,
            'name_policy_note':'Birth-name scenario. Current-name transition policy remains unresolved.',
            'timing_status':'No activation dates, transits or forecasts are inferred by this endpoint.'}


static_root = PROTOTYPE_ROOT / "static"
static_root.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_root), html=True), name="prototype")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8766, access_log=False, log_level="warning")

