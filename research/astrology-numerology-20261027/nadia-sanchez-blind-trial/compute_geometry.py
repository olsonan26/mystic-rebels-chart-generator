"""Read-only retrospective trial. Writes research artifacts only; imports no app secrets."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, math
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from functools import lru_cache
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MYSTIC = ROOT / "work" / "Mystic-Rebels"
sys.path.insert(0, str(MYSTIC))
from mystic_rebels import astronomy as astro
from mystic_rebels.models import BirthInput
from mystic_rebels.service import calculate
swe=astro.swe
PACIFIC=ZoneInfo("America/Los_Angeles")
TARGETS=["Sun","Moon","Mercury","Venus","Mars","Ascendant","Midheaven"]
TRANSITS={"Saturn":swe.SATURN,"Uranus":swe.URANUS,"Neptune":swe.NEPTUNE,"Pluto":swe.PLUTO}
OFFSETS=[0,60,90,120,180,240,270,300]
WINDOWS=[("2003-07-17","2005-07-17"),("2008-07-17","2014-07-17")]
ASPECTS={0:"conjunction",60:"sextile",90:"square",120:"trine",180:"opposition"}
def jd_for_local(day):
    utc=datetime.fromisoformat(day).replace(tzinfo=PACIFIC).astimezone(timezone.utc)
    return astro.times(utc)["jd_ut1"]
def utc_dt(jd):
    y,m,d,h,minute,sec=swe.jdut1_to_utc(jd,swe.GREG_CAL)
    return datetime(y,m,d,h,minute,min(59,int(sec)),tzinfo=timezone.utc)
def local_dt(jd):return utc_dt(jd).astimezone(PACIFIC)
def age_on(day):
    return day.year-1992-((day.month,day.day)<(7,17))
def wrap(x):return (x+180)%360-180
@lru_cache(maxsize=250000)
def position(jd,body):
    vals,flags=swe.calc_ut(jd,body,astro.FLAGS)
    astro.assert_backend(flags)
    return vals[0]%360,vals[3]
def refine(body,target,a,b):
    fa=wrap(position(a,body)[0]-target)
    for _ in range(45):
        middle=(a+b)/2
        fm=wrap(position(middle,body)[0]-target)
        if abs(fm)<1e-10 or b-a<1e-8:return middle
        if fa*fm<=0:b=middle
        else:a=middle;fa=fm
    return (a+b)/2
def scan(step):
    found=[]
    for lo,hi in WINDOWS:
        start,end=jd_for_local(lo),jd_for_local(hi)
        grid=[start+i*step for i in range(math.ceil((end-start)/step))]
        grid.append(end)
        for transit,body in TRANSITS.items():
            values=[position(t,body)[0] for t in grid]
            for point in natal["points"]:
                if point["id"] not in TARGETS or not point["available"]:continue
                natal_lon=point["longitude_deg"]
                for offset in OFFSETS:
                    target=(natal_lon+offset)%360
                    for index in range(len(grid)-1):
                        fa,fb=wrap(values[index]-target),wrap(values[index+1]-target)
                        if abs(fb-fa)>180 or fa*fb>0:continue
                        exact=refine(body,target,grid[index],grid[index+1])
                        if not start<=exact<end:continue
                        lon,speed=position(exact,body)
                        date=local_dt(exact)
                        if found and any(r["transit"]==transit and r["target"]==point["id"] and abs(r["jd_ut1"]-exact)<0.001 for r in found[-50:]):continue
                        angle=min(offset,360-offset)
                        found.append({"transit":transit,"target":point["id"],"aspect_angle_deg":angle,
                            "geometry":ASPECTS[angle],"oriented_offset_deg":offset,"jd_ut1":exact,
                            "exact_utc":utc_dt(exact).isoformat(),"exact_local":date.isoformat(),
                            "local_date":date.date().isoformat(),"age":age_on(date),
                            "transit_longitude_deg":lon,"target_longitude_deg":natal_lon,
                            "residual_deg":abs(wrap(lon-target)),"retrograde":speed<0,
                            "transit_natal_house":int(((lon//30)-(natal["angles"]["Ascendant"]//30))%12+1),
                            "target_house":point.get("house"),"target_tone":point.get("tone"),
                            "target_pulse":point.get("pulse"),"target_field":point.get("field")})
    return sorted(found,key=lambda r:r["jd_ut1"])
astro.initialize()
astro.verify_assets(["sepl_18.se1","semo_18.se1"])
request=BirthInput(name="Nadia Sanchez",local_date="1992-07-17",local_time="20:01:00",
    timezone="America/Los_Angeles",latitude=33.8044,longitude=-118.0673,
    coordinate_provenance="User-supplied coordinates",location_name="Los Alamitos, California",
    time_accuracy="nearest_minute",uncertainty_seconds=30,
    objects=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","Ascendant","Midheaven"])
natal=calculate(request)
(HERE/"natal.json").write_text(json.dumps(natal,indent=2),encoding="utf-8")
daily=scan(1.0)
sixhour=scan(0.25)
fingerprint=lambda rows:[(r["transit"],r["target"],r["geometry"],r["local_date"]) for r in rows]
verification={"daily_contact_count":len(daily),"six_hour_contact_count":len(sixhour),
    "independent_grid_agreement":fingerprint(daily)==fingerprint(sixhour),
    "max_root_residual_degrees":max((r["residual_deg"] for r in sixhour),default=0)}
config={"status":"EXPLORATORY_RAW_GEOMETRY_NOT_APPROVED_PURE_DIRECTIONAL_ASPECT_ENGINE",
    "transiting_bodies":list(TRANSITS),"natal_targets":TARGETS,"unsigned_angles_deg":[0,60,90,120,180],
    "selection":"Fixed before outcomes: all exact contacts for these bodies, targets, angles, and civil-date age windows. Supportive geometries retained alongside squares/oppositions. No orb or danger ranking.",
    "date_windows_local_start_inclusive_end_exclusive":WINDOWS,"timezone":"America/Los_Angeles",
    "natal_input":request.model_dump(mode="json"),"backend_requested":"SWIEPH","flags":astro.FLAGS,
    "note":"Dates are computed angular equalities, not event forecasts, influence windows, or exact birth-record validation.",
    "source_gates_unchanged":True,"life_events_supplied":False}
output={"configuration":config,"verification":verification,"contacts":sixhour}
(HERE/"transit-geometry.json").write_text(json.dumps(output,indent=2),encoding="utf-8")
print(json.dumps(verification))
print("NATAL",json.dumps([{"id":p["id"],"position":p.get("display_dms"),"house":p.get("house"),"field":p.get("field")} for p in natal["points"]]))
for age in [11,12,16,17,18,19,20,21]:
    rows=[r for r in sixhour if r["age"]==age]
    print("AGE",age,json.dumps([{"date":r["local_date"],"transit":r["transit"],"geometry":r["geometry"],"target":r["target"]} for r in rows]))

