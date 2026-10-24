from __future__ import annotations
import hashlib,json,platform
from datetime import datetime,timezone
from importlib.metadata import version
from . import __version__
from . import astronomy as astro
from .catalog import BY_ID,CATALOG,PRESETS
from .chronology import resolve_local
from .errors import ChartError
from .models import BirthInput
from .placements import derive,dms,norm

RULES={
    'whole_sign':{'id':'N9-003','version':'1','status':'READY','evidence':'book:Whole Sign house model'},
    'true_placement':{'id':'N9-004','version':'1','status':'READY','evidence':'book:True Placement'},
    'tone':{'id':'N9-005','version':'1','status':'READY','evidence':'book:astronomical sign'},
    'pulse':{'id':'N9-006','version':'1','status':'READY','evidence':'book:227-230'},
    'ruler':{'id':'N9-007','version':'1','status':'READY','evidence':'book:modern rulers'},
    'parts':{'id':'N9-014','version':'1','status':'READY','evidence':'book:670-678'},
    'nonagesimal':{'id':'N9-011','version':'2','status':'READY','evidence':'book:661-665; viewer:539-542; Leo AC 13°06 -> Taurus Nona 13°06'},
    'spark':{'id':'N9-020/021','version':'1','status':'BLOCKED','reason':'Contradictory parity definitions'},
    'aspects':{'id':'N9-033/034','version':'1','status':'BLOCKED','reason':'Incomplete per-object orbital reach and directional rules'},
    'progressions':{'id':'N9-038','version':'1','status':'BLOCKED','reason':'Unverified calculation procedure'},
}

def object_catalog():
    assets={x['path'] for x in astro.manifest()['assets']}
    rows=[]
    for item in CATALOG:
        row={k:v for k,v in item.items() if k!='body'}
        row['available']=item.get('available',True) and all(x in assets and (astro.EPHE/x).is_file() for x in item.get('assets',[]))
        if not row['available']:row['reason']=item.get('reason','Required ephemeris asset is not installed.')
        rows.append(row)
    return {'objects':rows,'presets':PRESETS,'supported_years':[1800,2399]}

def calculate(request:BirthInput):
    unknown_time=request.time_accuracy=='unknown' or request.local_time is None
    # Unknown time is an explicit labelled reference epoch. Houses and angles are suppressed.
    clock='12:00:00' if unknown_time else request.local_time
    utc=resolve_local(request.local_date,clock,request.timezone,request.fold)
    if not 1800<=utc.year<=2399:
        raise ChartError('COMPUTATION_OUTSIDE_SUPPORTED_RANGE','The installed core ephemeris supports 1800–2399 UTC.')
    canonical=request.model_dump(mode='json')
    canonical['objects']=list(dict.fromkeys(request.objects))
    fingerprint=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    points=[];warnings=[]
    with astro.LOCK:
        astro.initialize()
        astro.verify_assets(['sepl_18.se1','semo_18.se1'])
        time_data=astro.times(utc)
        jd=time_data['jd_ut1'];geometry={};cusps=[]
        if not unknown_time:
            try:geometry,cusps=astro.angles(jd,request.latitude,request.longitude)
            except ChartError as exc:warnings.append(exc.record())
        ac=geometry.get('Ascendant')
        cache={}
        def get_body(id):
            if id in cache:return cache[id]
            row=BY_ID[id]
            if row.get('max_year') and utc.year>row['max_year']:
                raise ChartError('COMPUTATION_OUTSIDE_SUPPORTED_RANGE',f"{row['name']} is supported through {row['max_year']} by its installed file.")
            paths=['sepl_18.se1','semo_18.se1']+row.get('assets',[])
            cache[id]=astro.position(jd,row['body'],list(dict.fromkeys(paths)))
            return cache[id]
        for id in canonical['objects']:
            row=BY_ID.get(id)
            base={'id':id,'name':row['name'] if row else id,'glyph':row['glyph'] if row else '?','group':row['group'] if row else 'Unknown'}
            try:
                if not row:raise ChartError('OBJECT_NOT_SUPPORTED','This object is not registered in the current catalog.')
                if not row.get('available',True):raise ChartError('RULE_NOT_VERIFIED',row['reason'])
                if row['body'] is not None:
                    value=get_body(id)
                elif id.startswith('SouthNode'):
                    parent=get_body(id.replace('South','North'))
                    value={**parent,'longitude_deg':norm(parent['longitude_deg']+180),'latitude_deg':-parent['latitude_deg'],'declination_deg':-parent['declination_deg'],'provenance':{**parent['provenance'],'algorithm':'opposite-lunar-node-v1','parent':id.replace('South','North')}}
                elif row['group']=='Angles':
                    if id not in geometry:raise ChartError('ANGLE_GEOMETRY_UNDEFINED','A resolved birth time and valid horizon geometry are required.')
                    value={'longitude_deg':geometry[id],'retrograde':None,'provenance':{'algorithm':'swiss-independent-horizon-angles-v1' if id not in ('Nonagesimal','Subnonagesimal') else 'asc-minus90-plus90-source-verified-v2','backend':'GEOMETRY','julian_ut1':jd,'rule':RULES['nonagesimal'] if id in ('Nonagesimal','Subnonagesimal') else None}}
                elif row['group']=='Parts':
                    if ac is None:raise ChartError('ANGLE_GEOMETRY_UNDEFINED','A resolved Ascendant is required for this Part.')
                    sun=get_body('Sun')['longitude_deg'];moon=get_body('Moon')['longitude_deg'];venus=get_body('Venus')['longitude_deg']
                    longitude={'Fortune':ac+moon-sun,'Spirit':ac+sun-moon,'Love':ac+venus-sun}[id]
                    value={'longitude_deg':norm(longitude),'retrograde':None,'provenance':{'algorithm':'fixed-parts-no-sect-reversal-v1','backend':'DERIVED','parent_points':['Ascendant','Sun','Moon','Venus'],'rule':RULES['parts']}}
                else:raise ChartError('OBJECT_NOT_SUPPORTED','Calculation method is not available.')
                value={**value,'available':True,**derive(value['longitude_deg'],ac),'display_dms':dms(value['longitude_deg']),'input_fingerprint':fingerprint,'placement_provenance':{key:RULES[key] for key in ('whole_sign','true_placement','tone','pulse','ruler')},'outgoing_emission':False if row['group'] in ('Angles','Parts','Lunar points') else None}
                points.append({**base,**value})
            except ChartError as exc:points.append({**base,'available':False,'longitude_deg':None,'error':exc.record()})
    if unknown_time:warnings.append({'code':'TIME_UNKNOWN','message':'Positions use explicitly labelled local noon as a reference epoch. Birth positions vary during the day; houses, angles and house-derived placements are unavailable.'})
    if utc.year<1970:warnings.append({'code':'HISTORICAL_TIMEZONE','message':'Historical civil-time rules can have incomplete local records. Verify the documented birth offset for this date and location.'})
    return {'schema_version':'1.0','product':'Mystic Rebels','engine_version':__version__,'chart_id':fingerprint,'input':canonical,'input_fingerprint':fingerprint,'time':{**time_data,'birth_utc':utc.isoformat(),'iana_zone':request.timezone,'utc_offset_seconds':int(utc.astimezone(__import__('zoneinfo').ZoneInfo(request.timezone)).utcoffset().total_seconds()),'tzdata_version':version('tzdata'),'time_is_reference_only':unknown_time,'uncertainty_seconds':None if unknown_time else request.uncertainty_seconds},'configuration':{'center':'geocentric','zodiac':'tropical','houses':'whole_sign','position_type':'apparent ecliptic/equinox of date','backend_requested':'SWIEPH','requested_flags':astro.FLAGS,'swiss_version':astro.swe.version,'binding_version':version('pyswisseph'),'python_version':platform.python_version(),'asset_manifest_sha256':hashlib.sha256((astro.ROOT/'data'/'ephemeris-manifest.json').read_bytes()).hexdigest()},'angles':geometry,'whole_sign_cusps':cusps,'points':points,'warnings':warnings,'rules':RULES,'created_at_utc':datetime.now(timezone.utc).isoformat()}
