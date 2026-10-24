"""Native Swiss file backend, serialized because the C library has global state."""
from __future__ import annotations
import hashlib,json,os,threading
from math import radians,cos,sin,hypot
from datetime import datetime
from pathlib import Path
import swisseph as swe
from .errors import ChartError
from .placements import norm

ROOT=Path(__file__).resolve().parents[1]
EPHE=ROOT/'data'/'ephe'
LOCK=threading.RLock()
FLAGS=swe.FLG_SWIEPH|swe.FLG_SPEED
EPH_MASK=swe.FLG_JPLEPH|swe.FLG_SWIEPH|swe.FLG_MOSEPH

def manifest():
    path=ROOT/'data'/'ephemeris-manifest.json'
    if not path.exists():raise ChartError('EPHEMERIS_BACKEND_UNAVAILABLE','The astronomical data has not been installed.')
    return json.loads(path.read_text(encoding='utf-8'))

def verify_assets(paths):
    records={x['path']:x for x in manifest()['assets']}
    result=[]
    for name in paths:
        record=records.get(name);path=EPHE/name
        if not record or not path.is_file():raise ChartError('EPHEMERIS_ASSET_UNAVAILABLE',f'Missing astronomical data file: {name}',asset=name)
        if path.stat().st_size!=record['byte_size'] or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:
            raise ChartError('EPHEMERIS_ASSET_INTEGRITY',f'Astronomical data checksum failed: {name}',asset=name)
        result.append({'path':name,'sha256':record['sha256']})
    return result

def assert_backend(returned:int):
    if returned&EPH_MASK != swe.FLG_SWIEPH:
        raise ChartError('EPHEMERIS_BACKEND_MISMATCH','The calculation did not use the requested Swiss file backend.',requested_flags=FLAGS,returned_flags=returned)

def initialize():
    # SE_EPHE_PATH overrides set_ephe_path inside Swiss; make any override explicit.
    override=os.environ.get('SE_EPHE_PATH')
    if override and Path(override).resolve()!=EPHE.resolve():
        raise ChartError('EPHEMERIS_CONFIGURATION_CONFLICT','SE_EPHE_PATH overrides the validated astronomical data directory.')
    swe.set_ephe_path(str(EPHE))

def times(utc:datetime):
    sec=utc.second+utc.microsecond/1e6
    et,ut1=swe.utc_to_jd(utc.year,utc.month,utc.day,utc.hour,utc.minute,sec,swe.GREG_CAL)
    return {'jd_ut1':ut1,'jd_tt':et,'delta_t_seconds':(et-ut1)*86400,'time_conversion':'swe.utc_to_jd Gregorian UTC; Swiss built-in Delta T model'}

def position(jd:float,body:int,assets:list[str]):
    refs=verify_assets(assets)
    try:
        data,returned=swe.calc_ut(jd,body,FLAGS)
        assert_backend(returned)
        eq,eqflags=swe.calc_ut(jd,body,FLAGS|swe.FLG_EQUATORIAL)
        assert_backend(eqflags)
    except swe.Error as exc:raise ChartError('EPHEMERIS_OBJECT_UNAVAILABLE',str(exc))
    return {'longitude_deg':norm(data[0]),'latitude_deg':data[1],'distance_au':data[2],'speed_longitude_deg_per_day':data[3],'speed_latitude_deg_per_day':data[4],'declination_deg':eq[1],'retrograde':data[3]<0,'out_of_bounds':abs(eq[1])>23.44,'provenance':{'algorithm':'swiss-geocentric-apparent-ecliptic-of-date-v1','backend':'SWIEPH','requested_flags':FLAGS,'returned_flags':returned,'equatorial_returned_flags':eqflags,'assets':refs}}

def angles(jd,lat,lon):
    if abs(lat)>=89.999999:raise ChartError('ANGLE_GEOMETRY_UNDEFINED','Horizon angles are undefined at the geographic poles.')
    # At the ecliptic pole the ecliptic can coincide with the entire horizon:
    # there is no unique rising intersection, even though the geographic latitude is valid.
    eps=radians(swe.calc_ut(jd,swe.ECL_NUT,0)[0][0])
    theta=radians(swe.sidtime(jd)*15+lon);phi=radians(lat)
    a=cos(phi)*cos(theta);b=cos(phi)*sin(theta)*cos(eps)+sin(phi)*sin(eps)
    if hypot(a,b)<1e-10:raise ChartError('ANGLE_GEOMETRY_UNDEFINED','The ecliptic coincides with the horizon at this location and time; a unique Ascendant cannot be calculated.')
    try:cusps,points=swe.houses_ex(jd,lat,lon,b'W',0)
    except swe.Error as exc:raise ChartError('ANGLE_GEOMETRY_UNDEFINED',str(exc))
    ac,mc,vertex=map(norm,(points[0],points[1],points[3]))
    return {'Ascendant':ac,'Descendant':norm(ac+180),'Midheaven':mc,'ImumCoeli':norm(mc+180),'Vertex':vertex,'Invertex':norm(vertex+180),'Nonagesimal':norm(ac-90),'Subnonagesimal':norm(ac+90)},list(cusps)
