"""Independent JPL/ERFA station and repeated-longitude crossing evidence.

The reference fit never consumes a Swiss position or speed. Swiss is used only
after the independent event has been solved, to measure the model residual.
Raw Horizons responses are immutable cached inputs to the offline QA tests.
"""
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request

import erfa
import numpy as np
import swisseph as swe

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mystic_rebels import astronomy as astro

OUT = ROOT / "evidence" / "astronomy-followup"
WINDOWS = {
    "station_retrograde": ("2024-04-01 16:00", "2024-04-02 04:00"),
    "station_direct": ("2024-04-25 07:00", "2024-04-25 19:00"),
    "pregrade_entry": ("2024-03-18 20:00", "2024-03-19 08:00"),
    "postgrade_exit": ("2024-05-13 00:00", "2024-05-13 12:00"),
}
VENUS_WINDOWS = {
    "station_retrograde": ("2025-03-01 19:00", "2025-03-02 07:00"),
    "station_direct": ("2025-04-12 19:00", "2025-04-13 07:00"),
    "pregrade_entry": ("2025-01-28 07:00", "2025-01-28 19:00"),
    "postgrade_exit": ("2025-05-16 00:00", "2025-05-16 12:00"),
}


def parameters(start, end, target="199"):
    return {
        "format": "json", "COMMAND": repr(target), "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'", "START_TIME": repr(start), "STOP_TIME": repr(end),
        "STEP_SIZE": "'10m'", "TIME_TYPE": "'UT'", "QUANTITIES": "'31,45,46'",
        "ANG_FORMAT": "'DEG'", "EXTRA_PREC": "'YES'", "CSV_FORMAT": "'YES'",
        "REF_SYSTEM": "'ICRF'", "APPARENT": "'AIRLESS'", "CAL_FORMAT": "'JD'",
        "TIME_DIGITS": "'FRACSEC'", "OBJ_DATA": "'YES'",
    }


def fetch(name, start, end, target="199", prefix="mercury-2024"):
    path = OUT / f"{prefix}-{name}.json"
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(parameters(start, end, target))
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        request = urllib.request.Request(url, headers={"User-Agent": "Mystic-Rebels-Independent-Astronomy-QA/0.2"})
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.load(response)
        if "$$SOE" not in payload.get("result", ""):
            raise RuntimeError(payload.get("error", payload))
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload, url, str(path.relative_to(ROOT)).replace("\\", "/")


def rotate_apparent_icrf(jd_utc, ra, dec):
    # ERFA UTC -> TAI -> TT independently supplies the 2024 leap-second offset.
    tai = erfa.utctai(2400000.5, jd_utc - 2400000.5)
    tt = erfa.taitt(*tai)
    vector = erfa.s2c(np.radians(ra), np.radians(dec))
    ecliptic = erfa.ecm06(*tt) @ vector
    mean_lon, latitude = erfa.c2s(ecliptic)
    dpsi, _ = erfa.nut06a(*tt)
    return float(np.degrees(mean_lon + dpsi) % 360), float(np.degrees(latitude))


def parse(payload):
    text = payload["result"]
    records = []
    for row in csv.reader(io.StringIO(text.split("$$SOE")[1].split("$$EOE")[0].strip())):
        values = [cell.strip() for cell in row]
        # UTC JD, blank solar/lunar markers, q31 lon/lat, q45 RA/DEC, q46 rates.
        jd = float(values[0])
        lon, lat, ra, dec, ra_rate, dec_rate = map(float, values[3:9])
        matched_lon, matched_lat = rotate_apparent_icrf(jd, ra, dec)
        records.append({"jd_utc": jd, "horizons_iau7680_lon_deg": lon,
                        "horizons_iau7680_lat_deg": lat, "icrf_apparent_ra_deg": ra,
                        "icrf_apparent_dec_deg": dec, "icrf_ra_cosdec_arcsec_hour": ra_rate,
                        "icrf_dec_arcsec_hour": dec_rate,
                        "matched_longitude_deg": matched_lon, "matched_latitude_deg": matched_lat})
    return records


def fit(records, degree=5, maximum_hours=None, center_jd=None):
    center = center_jd if center_jd is not None else records[len(records)//2]["jd_utc"]
    selected = records if maximum_hours is None else [r for r in records if abs(r["jd_utc"]-center)*24 <= maximum_hours]
    x = np.array([(r["jd_utc"]-center)*24 for r in selected])
    longitude = np.degrees(np.unwrap(np.radians([r["matched_longitude_deg"] for r in selected])))
    polynomial = np.polynomial.Polynomial.fit(x, longitude, degree).convert()
    residual_arcsec = float(np.max(np.abs(polynomial(x)-longitude))*3600)
    return center, polynomial, residual_arcsec


def station(records, degree=5, maximum_hours=None, center_jd=None):
    center, poly, residual = fit(records, degree, maximum_hours, center_jd)
    real = [float(r.real) for r in poly.deriv().roots() if abs(r.imag)<1e-8 and abs(r.real)<6]
    if len(real) != 1:
        raise RuntimeError(f"Station root not unique inside bracket: {real}")
    root = real[0]
    return center+root/24, float(poly(root)%360), residual


def crossing(records, longitude, degree=5):
    center, poly, residual = fit(records, degree)
    # Choose the same 360-degree branch as the unwrapped reference samples.
    longitude += 360*round((float(poly(0))-longitude)/360)
    shifted = poly-longitude
    real = [float(r.real) for r in shifted.roots() if abs(r.imag)<1e-8 and abs(r.real)<6]
    if len(real) != 1:
        raise RuntimeError(f"Crossing root not unique inside bracket: {real}")
    return center+real[0]/24, residual


def iso(jd):
    return (datetime(1970,1,1,tzinfo=timezone.utc)+timedelta(days=jd-2440587.5)).isoformat()


def swiss_at(jd, body=swe.MERCURY):
    date = datetime.fromisoformat(iso(jd))
    tt = astro.times(date)["jd_tt"]
    data, flags = swe.calc(tt, body, astro.FLAGS)
    astro.assert_backend(flags)
    return {"longitude_deg":data[0], "speed_deg_day":data[3], "returned_flags":flags}


def main(name="Mercury", year=2024, target="199", windows=WINDOWS):
    OUT.mkdir(parents=True,exist_ok=True)
    astro.initialize()
    datasets = {}
    provenance = {}
    body = getattr(swe,name.upper())
    prefix = f"{name.lower()}-{year}"
    for event_name, (start,end) in windows.items():
        payload, url, raw = fetch(event_name,start,end,target,prefix)
        datasets[event_name] = parse(payload)
        provenance[event_name] = {"url":url,"raw_response":raw,"samples":len(datasets[event_name]),
                                  "sha256":hashlib.sha256((ROOT/raw).read_bytes()).hexdigest()}
        print(name,event_name, len(datasets[event_name]), flush=True)
    events = {}
    for event_name in ("station_retrograde","station_direct"):
        jd, longitude, residual = station(datasets[event_name])
        short = station(datasets[event_name], degree=4, maximum_hours=3, center_jd=jd)
        events[event_name] = {"jd_utc":jd,"utc":iso(jd),"longitude_deg":longitude,
                        "fit_max_residual_arcsec":residual,"independent_refit_delta_seconds":abs(short[0]-jd)*86400}
    for event_name,station_name in (("pregrade_entry","station_direct"),("postgrade_exit","station_retrograde")):
        jd, residual = crossing(datasets[event_name], events[station_name]["longitude_deg"])
        alternate, _ = crossing(datasets[event_name], events[station_name]["longitude_deg"],degree=4)
        events[event_name] = {"jd_utc":jd,"utc":iso(jd),"target_longitude_deg":events[station_name]["longitude_deg"],
                        "fit_max_residual_arcsec":residual,"independent_refit_delta_seconds":abs(alternate-jd)*86400}
    for event in events.values():
        event["swiss_at_reference_event"] = swiss_at(event["jd_utc"],body)
    # Production event comparison is deliberately downstream of the independent
    # fit. It cannot affect any JPL-derived reference epoch or longitude.
    from mystic_rebels.gradity import cycles_for_month
    cycles = cycles_for_month(name,year,4 if name == "Mercury" else 3)
    matching = min(cycles, key=lambda c:abs(datetime.fromisoformat(c[1]["utc"].replace("Z","+00:00")).timestamp()-datetime.fromisoformat(events["station_retrograde"]["utc"]).timestamp()))
    for computed in matching:
        reference = events[computed["kind"]]
        instant = datetime.fromisoformat(computed["utc"].replace("Z","+00:00"))
        residual = (instant-datetime.fromisoformat(reference["utc"])).total_seconds()
        reference["production_event"] = {**computed,"time_residual_seconds":residual}
    longitude_residuals = []
    q31_residuals = []
    for records in datasets.values():
        for row in records:
            swiss = swiss_at(row["jd_utc"],body)["longitude_deg"]
            longitude_residuals.append(abs((swiss-row["matched_longitude_deg"]+180)%360-180)*3600)
            q31_residuals.append(abs((swiss-row["horizons_iau7680_lon_deg"]+180)%360-180)*3600)
    report = {
        "provider":"NASA JPL Horizons + independent ERFA IAU2006/2000A coordinate rotation",
        "retrieved_at_utc":datetime.now(timezone.utc).isoformat(),"object":name,
        "scope":f"One {year} {name} cycle, not a universal error guarantee or predictive validation",
        "reference_conventions":{
            "center":"500@399 Earth geocenter", "target":f"{target} {name} body center",
            "time":"Horizons UT labels are UTC post1962; ERFA UTC->TAI->TT rotation epoch",
            "q45":"ICRF apparent RA/DEC with down-leg light-time, solar deflection, stellar aberration; AIRLESS",
            "rotation":"ERFA ecm06 ICRS->IAU2006 mean ecliptic/equinox of date; nut06a delta psi added for true equinox",
            "production":"Swiss SWIEPH|SPEED=258 tropical geocentric apparent ecliptic/equinox of date; unchanged",
            "residual_models":"Swiss long-term precession versus IAU2006 and provider light-deflection differences retained",
            "q31_diagnostic":"Horizons native IAU76/80 longitude recorded separately, not falsely treated as identical frame",
            "solver":"Fifth-degree polynomial over 73 JPL samples at10-minute spacing within12h windows; root of first derivative for stations, repeated longitude for crossings; fourth-degree refit checks stability",
        },
        "authoritative_references":["https://ssd.jpl.nasa.gov/horizons/manual.html#observer-table","https://ssd-api.jpl.nasa.gov/doc/horizons.html","https://www.astro.com/swisseph/swephprg.htm","https://github.com/liberfa/erfa"],
        "raw_inputs":provenance,"events":events,
        "matched_max_longitude_residual_arcsec":max(longitude_residuals),
        "unmatched_q31_max_longitude_residual_arcsec":max(q31_residuals),
        "max_event_time_residual_seconds":max(abs(e["production_event"]["time_residual_seconds"]) for e in events.values()),
        "tolerances":{"matched_longitude_arcsec":0.02,"event_time_seconds":10,
                      "rationale":"Allows IAU2006/Swiss long-term precession, apparent-model differences and sampled-fit uncertainty; measured residuals and refit stability reported separately"},
    }
    (OUT/f"{prefix}-independent-events.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"events":events,"max_arcsec":max(longitude_residuals)},indent=2))


if __name__ == "__main__":
    main()
    main("Venus",2025,"299",VENUS_WINDOWS)
