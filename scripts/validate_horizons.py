"""Independent live NASA JPL Horizons comparisons. Raw responses retained."""
from __future__ import annotations
import csv,io,json,sys,urllib.parse,urllib.request,math
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mystic_rebels import astronomy as astro
from mystic_rebels.catalog import BY_ID,CATALOG
import swisseph as swe

DATES=['1992-07-18T03:01:00+00:00','2000-01-01T12:00:00+00:00','2024-04-08T18:00:00+00:00']
TARGETS={'Sun':'10','Moon':'301','Mercury':'199','Venus':'299','Mars':'4','Jupiter':'5','Saturn':'6','Uranus':'7','Neptune':'8','Pluto':'9','Chiron':'2060;','Ceres':'1;','Pallas':'2;','Juno':'3;','Vesta':'4;','Eris':'136199;','Sedna':'90377;','Hygiea':'10;','Psyche':'16;','Eros':'433;','Pholus':'5145;','Nessus':'7066;'}
TARGETS.update({row['id']:f"{row['number']};" for row in CATALOG if 'number' in row})

def run():
    out=ROOT/'evidence'/'horizons';out.mkdir(parents=True,exist_ok=True)
    dates=[datetime.fromisoformat(t) for t in DATES]
    utc_jds=[swe.julday(t.year,t.month,t.day,t.hour+t.minute/60+t.second/3600) for t in dates]
    report={'provider':'NASA JPL Horizons','retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'reference_conventions':{'center':'500@399 Earth geocenter','table':'OBSERVER quantities 1 and 31','coordinates':'1: astrometric ICRF RA/DEC; 31: apparent Earth ecliptic of date IAU76/80','time':'UTC supplied to Horizons as UT post-1962; Swiss UTC-to-TT conversion','corrections':'ICRF astrometric: light-time only, no aberration or solar deflection; apparent ecliptic: light-time, aberration, solar deflection, no atmosphere','outer_planets':'planetary-system barycenters matching Swiss default','models_notice':'ICRF comparison matches reference frame and correction conventions. Apparent of-date comparison retains documented IAU precession/nutation model differences. Swiss file and current JPL minor-body orbit solutions need not be identical.'},'comparisons':[],'failures':[]}
    with astro.LOCK:
        astro.initialize()
        for name,target in TARGETS.items():
            params={'format':'json','COMMAND':f"'{target}'",'EPHEM_TYPE':"'OBSERVER'",'CENTER':"'500@399'",'TLIST':"'"+'\n'.join(str(j) for j in utc_jds)+"'",'TIME_TYPE':"'UT'",'QUANTITIES':"'1,31'",'ANG_FORMAT':"'DEG'",'EXTRA_PREC':"'YES'",'CSV_FORMAT':"'YES'",'OBJ_DATA':"'YES'",'REF_SYSTEM':"'ICRF'",'APPARENT':"'AIRLESS'"}
            url='https://ssd.jpl.nasa.gov/api/horizons.api?'+urllib.parse.urlencode(params)
            rawpath=out/f'{name}-icrf-and-ecliptic.json'
            try:
                if rawpath.exists():payload=json.loads(rawpath.read_text())
                else:
                    req=urllib.request.Request(url,headers={'User-Agent':'Mystic-Rebels-Independent-Astronomy-QA/0.1'})
                    with urllib.request.urlopen(req,timeout=90) as response:payload=json.load(response)
                    rawpath.write_text(json.dumps(payload,indent=2),encoding='utf-8')
                text=payload.get('result','')
                if '$$SOE' not in text:raise RuntimeError(payload.get('error',text[:600]))
                rows=list(csv.reader(io.StringIO(text.split('$$SOE')[1].split('$$EOE')[0].strip())))
                if len(rows)!=len(dates):raise RuntimeError(f'Expected {len(dates)} reference epochs, got {len(rows)}')
                for date,row in zip(dates,rows):
                    lon,lat=float(row[-3]),float(row[-2])
                    tt=astro.times(date)['jd_tt']
                    data,flags=swe.calc(tt,BY_ID[name]['body'],astro.FLAGS)
                    astro.assert_backend(flags)
                    diagnostic_flags=astro.FLAGS|swe.FLG_EQUATORIAL|swe.FLG_J2000|swe.FLG_NONUT|swe.FLG_NOABERR|swe.FLG_NOGDEFL|swe.FLG_ICRS
                    aligned,af=swe.calc(tt,BY_ID[name]['body'],diagnostic_flags)
                    astro.assert_backend(af)
                    delta=lambda a,b:((a-b+180)%360-180)*3600
                    ref_ra,ref_dec=float(row[-5]),float(row[-4])
                    dra=delta(aligned[0],ref_ra)*math.cos(math.radians(ref_dec));ddec=(aligned[1]-ref_dec)*3600
                    report['comparisons'].append({'object':name,'utc':date.isoformat(),'reference_longitude_deg':lon,'reference_latitude_deg':lat,'swiss_longitude_deg':data[0],'longitude_residual_arcsec':delta(data[0],lon),'latitude_residual_arcsec':(data[1]-lat)*3600,'icrf_reference_ra_deg':ref_ra,'icrf_reference_dec_deg':ref_dec,'icrf_ra_cosdec_residual_arcsec':dra,'icrf_dec_residual_arcsec':ddec,'icrf_separation_arcsec':math.hypot(dra,ddec),'returned_flags':flags,'icrf_requested_flags':diagnostic_flags,'icrf_returned_flags':af,'reference_url':url,'raw_response':f'evidence/horizons/{name}-icrf-and-ecliptic.json'})
                print(f'{name}: compared {len(rows)} epochs',flush=True)
            except Exception as exc:
                report['failures'].append({'object':name,'reason':str(exc),'reference_url':url})
                print(f'{name}: UNAVAILABLE {exc}',flush=True)
            (ROOT/'evidence'/'independent-astronomy.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if report['failures']:raise SystemExit(1)

if __name__=='__main__':run()
