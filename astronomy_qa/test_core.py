import json,math,hashlib
from datetime import datetime,timezone
from pathlib import Path
import erfa,pytest,swisseph as swe
from fastapi.testclient import TestClient
from mystic_rebels import astronomy as astro
from mystic_rebels.api import app
from mystic_rebels.models import BirthInput
from mystic_rebels.chronology import resolve_local
from mystic_rebels.errors import ChartError
from mystic_rebels.placements import house,derive,norm
from mystic_rebels.service import calculate
from mystic_rebels.catalog import CATALOG

SAMPLE=dict(local_date='1992-07-17',local_time='20:01:00',timezone='America/Los_Angeles',latitude=33.803,longitude=-118.072)

def independent_angles(ut1,tt,lat,lon):
    theta=erfa.gst06a(2400000.5,ut1-2400000.5,2400000.5,tt-2400000.5)+math.radians(lon)
    _,deps=erfa.nut06a(2400000.5,tt-2400000.5)
    eps=erfa.obl06(2400000.5,tt-2400000.5)+deps
    phi=math.radians(lat)
    # Intersection of horizon plane and ecliptic. Choose the rising root using d(alt)/dt.
    a=math.cos(phi)*math.cos(theta)
    b=math.cos(phi)*math.sin(theta)*math.cos(eps)+math.sin(phi)*math.sin(eps)
    root=math.atan2(-a,b)
    derivative=math.cos(phi)*(-math.cos(root)*math.sin(theta)+math.sin(root)*math.cos(eps)*math.cos(theta))
    if derivative<0:root+=math.pi
    ac=math.degrees(root)%360
    mc=math.degrees(math.atan2(math.sin(theta),math.cos(theta)*math.cos(eps)))%360
    return ac,mc,eps,theta

@pytest.mark.parametrize('date,clock,zone,expected',[
 ('1992-07-17','20:01:00','America/Los_Angeles','1992-07-18T03:01:00+00:00'),
 ('1945-08-14','19:00:00','America/New_York','1945-08-14T23:00:00+00:00'),
 ('1985-12-31','23:59:00','Asia/Kathmandu','1985-12-31T18:29:00+00:00'),
 ('1992-09-02','17:46:00','Europe/Sofia','1992-09-02T14:46:00+00:00'),
 ('2024-01-01','00:00:00','Pacific/Chatham','2023-12-31T10:15:00+00:00')])
def test_historical_iana(date,clock,zone,expected):assert resolve_local(date,clock,zone).isoformat()==expected

@pytest.mark.parametrize('date,clock,zone,code',[
 ('2024-03-10','02:30:00','America/New_York','NONEXISTENT_DST_TIME'),
 ('2024-11-03','01:30:00','America/New_York','AMBIGUOUS_DST_FOLD'),
 ('2011-12-30','12:00:00','Pacific/Apia','NONEXISTENT_DST_TIME'),
 ('1986-01-01','00:05:00','Asia/Kathmandu','NONEXISTENT_DST_TIME')])
def test_dst_typed_errors(date,clock,zone,code):
    with pytest.raises(ChartError) as e:resolve_local(date,clock,zone)
    assert e.value.code==code

def test_dst_fold_choice():
    a=resolve_local('2024-11-03','01:30:00','America/New_York',0)
    b=resolve_local('2024-11-03','01:30:00','America/New_York',1)
    assert (b-a).total_seconds()==3600

@pytest.mark.parametrize('lat,lon',[(33.803,-118.072),(42.6977,23.3219),(-33.8688,151.2093),(0,0),(64.1466,-21.9426),(78.2232,15.6469),(-77.85,166.67)])
@pytest.mark.parametrize('epoch',['1992-07-18T03:01:00+00:00','2000-01-01T12:00:00+00:00','2024-04-08T18:00:00+00:00'])
def test_independent_erfa_horizon_geometry(lat,lon,epoch):
    astro.initialize();time=astro.times(datetime.fromisoformat(epoch));a=astro.angles(time['jd_ut1'],lat,lon)[0]
    ac,mc,eps,theta=independent_angles(time['jd_ut1'],time['jd_tt'],lat,lon)
    delta=lambda x,y:abs((x-y+180)%360-180)*3600
    assert delta(a['Ascendant'],ac)<.1
    assert delta(a['Midheaven'],mc)<.1
    assert delta(a['Ascendant']+180,a['Descendant'])<1e-8
    assert delta(a['Midheaven']+180,a['ImumCoeli'])<1e-8

def test_source_nonagesimal_and_altitude_maximum():
    # Author's Leo 13°06 AC -> Taurus 13°06 Nona, Scorpio 13°06 Subnona.
    assert norm(133.1-90)==pytest.approx(43.1)
    astro.initialize();t=astro.times(datetime(1992,7,18,3,1,tzinfo=timezone.utc));a=astro.angles(t['jd_ut1'],33.803,-118.072)[0]
    ac,mc,eps,theta=independent_angles(t['jd_ut1'],t['jd_tt'],33.803,-118.072)
    phi=math.radians(33.803)
    # Independent spherical maximum of zenith projection on the ecliptic plane.
    maximum=math.degrees(math.atan2(math.cos(phi)*math.sin(theta)*math.cos(eps)+math.sin(phi)*math.sin(eps),math.cos(phi)*math.cos(theta)))%360
    assert abs(((a['Nonagesimal']-maximum+180)%360-180)*3600)<.1
    assert a['Nonagesimal']!=a['Midheaven']

@pytest.mark.parametrize('lat,lon',[(33.803,-118.072),(42.6977,23.3219),(-33.8688,151.2093),(0,0),(78.2232,15.6469)])
def test_independent_prime_vertical_vertex(lat,lon):
    astro.initialize();t=astro.times(datetime(1992,7,18,3,1,tzinfo=timezone.utc));result=astro.angles(t['jd_ut1'],lat,lon)[0]
    _,_,eps,theta=independent_angles(t['jd_ut1'],t['jd_tt'],lat,lon)
    phi=math.radians(lat)
    a=-math.sin(phi)*math.cos(theta);b=-math.sin(phi)*math.sin(theta)*math.cos(eps)+math.cos(phi)*math.sin(eps)
    root=math.atan2(-a,b)
    east=-math.sin(theta)*math.cos(root)+math.cos(theta)*math.sin(root)*math.cos(eps)
    if east>0:root+=math.pi
    vertex=math.degrees(root)%360
    assert abs((result['Vertex']-vertex+180)%360-180)*3600<.1

@pytest.mark.parametrize('lat',[90,-90])
def test_poles_fail_precisely(lat):
    with pytest.raises(ChartError) as e:astro.angles(2451545,lat,0)
    assert e.value.code=='ANGLE_GEOMETRY_UNDEFINED'

def test_ecliptic_horizon_coincidence_has_no_fake_ascendant():
    astro.initialize();jd=2451545.0
    eps=swe.calc_ut(jd,swe.ECL_NUT,0)[0][0]
    lat=90-eps;lon=((270-swe.sidtime(jd)*15+180)%360)-180
    with pytest.raises(ChartError) as e:astro.angles(jd,lat,lon)
    assert e.value.code=='ANGLE_GEOMETRY_UNDEFINED'

@pytest.mark.parametrize('body',[swe.SUN,swe.MOON,swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN,swe.URANUS,swe.NEPTUNE,swe.PLUTO])
def test_velocity_and_retrograde_by_independent_finite_difference(body):
    astro.initialize();jd=2448821.6257;step=1/1440
    value,_=swe.calc_ut(jd,body,astro.FLAGS)
    before,_=swe.calc_ut(jd-step,body,astro.FLAGS)
    after,_=swe.calc_ut(jd+step,body,astro.FLAGS)
    difference=((after[0]-before[0]+180)%360-180)/(2*step)
    assert difference==pytest.approx(value[3],abs=2e-5)
    assert (difference<0)==(value[3]<0)

@pytest.mark.parametrize('raw,sign',[(0,0),(29+59/60+59.999/3600,0),(30,1),(359.999999999,11),(360,0),(-.0000001,11)])
def test_unrounded_sign_boundary(raw,sign):assert derive(raw)['sign_index']==sign

@pytest.mark.parametrize('raw,decan',[(9.999999999,1),(10,2),(19.999999999,2),(20,3)])
def test_unrounded_decan_boundary(raw,decan):assert derive(raw)['decan']==decan

def test_backend_fallback_rejected():
    with pytest.raises(ChartError) as e:astro.assert_backend(swe.FLG_MOSEPH|swe.FLG_SPEED)
    assert e.value.code=='EPHEMERIS_BACKEND_MISMATCH'

def test_corrupt_asset_rejected(monkeypatch,tmp_path):
    monkeypatch.setattr(astro,'EPHE',tmp_path)
    (tmp_path/'sepl_18.se1').write_bytes(b'corrupt')
    with pytest.raises(ChartError) as e:astro.verify_assets(['sepl_18.se1'])
    assert e.value.code=='EPHEMERIS_ASSET_INTEGRITY'

def test_all_registered_objects_are_accounted_for():
    r=calculate(BirthInput(**SAMPLE,objects=[x['id'] for x in CATALOG]))
    assert len(r['points'])==len(CATALOG)
    assert [p['id'] for p in r['points'] if not p['available']]==['SophiaMean','SophiaTrue']
    for point in r['points']:
        if point['available'] and point['provenance']['backend']=='SWIEPH':assert point['provenance']['returned_flags']&7==2

def test_geocentric_coordinates_invariant_to_geography():
    a=calculate(BirthInput(**SAMPLE,objects=['Sun','Moon','Midheaven']))
    b=calculate(BirthInput(**{**SAMPLE,'latitude':42.6977,'longitude':23.3219},objects=['Sun','Moon','Midheaven']))
    assert a['points'][0]['longitude_deg']==b['points'][0]['longitude_deg']
    assert a['points'][1]['longitude_deg']==b['points'][1]['longitude_deg']
    assert a['points'][2]['longitude_deg']!=b['points'][2]['longitude_deg']

def test_mc_not_forced_to_house_ten():
    r=calculate(BirthInput(**SAMPLE,objects=['Sun','Midheaven']))
    assert r['points'][0]['house']==7 and r['points'][0]['field']=='Libra'
    assert r['points'][0]['tone']=='Cancer' and r['points'][0]['pulse']=='Pisces'
    assert r['points'][1]['house']==11

def test_unknown_time_does_not_invent_houses():
    r=calculate(BirthInput(**{**SAMPLE,'time_accuracy':'unknown','local_time':None},objects=['Sun','Ascendant','Fortune']))
    assert r['points'][0]['available'] and r['points'][0]['house'] is None
    assert not r['points'][1]['available'] and not r['points'][2]['available']
    assert r['time']['time_is_reference_only']

def test_unsupported_dates():
    with pytest.raises(ChartError) as e:calculate(BirthInput(**{**SAMPLE,'local_date':'1700-01-01'}))
    assert e.value.code=='COMPUTATION_OUTSIDE_SUPPORTED_RANGE'

def test_minor_body_date_range():
    r=calculate(BirthInput(**{**SAMPLE,'local_date':'2200-01-01'},objects=['Sun','Eris']))
    assert r['points'][0]['available'] and not r['points'][1]['available']

def test_unknown_body_never_silently_omitted():
    r=calculate(BirthInput(**SAMPLE,objects=['Unknown123','Sun']))
    assert len(r['points'])==2 and r['points'][0]['error']['code']=='OBJECT_NOT_SUPPORTED'

def test_api_raw_json_roundtrip_and_consistent_reproducibility():
    client=TestClient(app);payload={**SAMPLE,'objects':['Sun','Moon','Ascendant','Midheaven','Eris']}
    response=client.post('/api/charts',json=payload);assert response.status_code==200
    r=response.json();again=client.post('/api/charts',json=payload).json()
    assert r['chart_id']==again['chart_id']
    for a,b in zip(r['points'],again['points']):assert a['longitude_deg']==b['longitude_deg']
    text=json.dumps(r);restored=json.loads(text)
    assert restored['points'][0]['longitude_deg']==r['points'][0]['longitude_deg']
    assert restored['points'][0]['longitude_deg']!=round(r['points'][0]['longitude_deg'],6)
    assert response.headers['cache-control']=='no-store'

def test_city_coordinate_and_timezone_resolution():
    client=TestClient(app)
    rows=client.get('/api/locations?q=Sofia').json()
    sofia=next(x for x in rows if x['name']=='Sofia, Bulgaria')
    assert abs(sofia['latitude']-42.6977)<.02 and abs(sofia['longitude']-23.3219)<.02
    assert sofia['timezone']=='Europe/Sofia'
    assert client.get('/api/timezone?latitude=33.803&longitude=-118.072').json()['timezone']=='America/Los_Angeles'

def test_no_false_aspects_or_spark():
    r=calculate(BirthInput(**SAMPLE))
    assert all(p.get('spark') is None for p in r['points'])
    assert 'aspects' not in r and r['rules']['aspects']['status']=='BLOCKED'
