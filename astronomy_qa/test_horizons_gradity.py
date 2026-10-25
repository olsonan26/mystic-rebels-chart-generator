"""Offline independent NASA JPL/ERFA event references; no network in CI."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
import swisseph as swe

from mystic_rebels import astronomy as astro
from mystic_rebels.gradity import cycles_for_month, classify
from scripts.astronomy_followup_horizons import parse, station, crossing

ROOT = Path(__file__).resolve().parents[1]
REPORTS = [json.loads((ROOT/"evidence"/"astronomy-followup"/f"{name}-independent-events.json").read_text())
           for name in ("mercury-2024","venus-2025")]


@pytest.fixture(scope="module",params=REPORTS,ids=lambda r:r["object"])
def reference(request):
    report=request.param
    astro.initialize()
    year=2024 if report["object"]=="Mercury" else 2025
    cycles=cycles_for_month(report["object"],year,4 if year==2024 else 3)
    target=datetime.fromisoformat(report["events"]["station_retrograde"]["utc"])
    cycle=min(cycles,key=lambda c:abs((datetime.fromisoformat(c[1]["utc"].replace("Z","+00:00"))-target).total_seconds()))
    return report,cycle


@pytest.mark.parametrize("kind",["pregrade_entry","station_retrograde","station_direct","postgrade_exit"])
def test_actual_station_and_shadow_events_match_independent_horizons(reference,kind):
    report,cycle=reference
    expected=report["events"][kind]
    actual=next(e for e in cycle if e["kind"]==kind)
    difference=(datetime.fromisoformat(actual["utc"].replace("Z","+00:00"))-datetime.fromisoformat(expected["utc"])).total_seconds()
    # These sample/model tolerances are separate from a numerical root bracket.
    assert abs(difference)<report["tolerances"]["event_time_seconds"]
    longitude=expected.get("longitude_deg",expected.get("target_longitude_deg"))
    assert abs((actual["longitude_deg"]-longitude+180)%360-180)*3600<report["tolerances"]["matched_longitude_arcsec"]


@pytest.mark.parametrize("kind",["pregrade_entry","station_retrograde","station_direct","postgrade_exit"])
def test_cached_reference_coordinates_match_production_with_frames_aligned(reference,kind):
    report,_=reference
    raw=report["raw_inputs"][kind]
    path=ROOT/raw["raw_response"]
    assert hashlib.sha256(path.read_bytes()).hexdigest()==raw["sha256"]
    payload=json.loads(path.read_text())
    assert payload["signature"]["source"]=="NASA/JPL Horizons API"
    records=parse(payload)
    assert len(records)==73
    body=getattr(swe,report["object"].upper())
    for record in records:
        # UTC is converted independently by ERFA in parse(); this conversion is
        # the production UTC->TT path being compared against that reference.
        utc=datetime.fromtimestamp((record["jd_utc"]-2440587.5)*86400,timezone.utc)
        tt=astro.times(utc)["jd_tt"]
        data,returned=swe.calc(tt,body,astro.FLAGS)
        astro.assert_backend(returned)
        delta=abs((data[0]-record["matched_longitude_deg"]+180)%360-180)*3600
        assert delta<report["tolerances"]["matched_longitude_arcsec"]


def test_independent_fits_reproduce_frozen_reference_epochs(reference):
    report,_=reference
    references={}
    for kind in ("station_retrograde","station_direct"):
        records=parse(json.loads((ROOT/report["raw_inputs"][kind]["raw_response"]).read_text()))
        jd,longitude,residual=station(records)
        expected=report["events"][kind]
        assert abs(jd-expected["jd_utc"])*86400<0.001
        assert abs(longitude-expected["longitude_deg"])*3600<0.00001
        assert residual<0.00001
        references[kind]=longitude
    for kind,target in (("pregrade_entry","station_direct"),("postgrade_exit","station_retrograde")):
        records=parse(json.loads((ROOT/report["raw_inputs"][kind]["raw_response"]).read_text()))
        jd,residual=crossing(records,references[target])
        assert abs(jd-report["events"][kind]["jd_utc"])*86400<0.001
        assert residual<0.00001


def test_venus_cycle_across_zero_aries_preserves_event_order_and_phases():
    astro.initialize()
    cycles=cycles_for_month("Venus",2025,3)
    cycle=next(c for c in cycles if "2025-03" in c[1]["utc"])
    pre,retro,direct,post=cycle
    assert retro["longitude_deg"]<30
    assert direct["longitude_deg"]>330
    assert pre["jd_ut1"]<retro["jd_ut1"]<direct["jd_ut1"]<post["jd_ut1"]
    for left,right,phase in ((pre,retro,"Pregrade"),(retro,direct,"Retrograde"),(direct,post,"Postgrade")):
        actual,status,_=classify((left["jd_ut1"]+right["jd_ut1"])/2,cycles)
        assert (actual,status)==(phase,"VERIFIED")
