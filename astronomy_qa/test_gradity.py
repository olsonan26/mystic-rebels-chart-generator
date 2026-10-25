"""Real loop ordering, derivative transitions, phase boundaries and API gates."""
from datetime import datetime, timezone
import json
import pytest
from fastapi.testclient import TestClient
from mystic_rebels import astronomy as astro
from mystic_rebels import gradity as g
from mystic_rebels.models import BirthInput
from mystic_rebels.service import calculate
from mystic_rebels.api import app

@pytest.mark.parametrize('name',list(g.WINDOW_DAYS))
def test_real_station_transitions_and_each_phase(name):
    with astro.LOCK:
        astro.initialize()
        cycles=g.cycles_for_month(name,2024,4)
        for events in cycles:
            a,b,c,d=[e['jd_ut1'] for e in events]
            body=getattr(g.swe,name.upper())
            assert a < b < c < d
            # Independent finite differences of actual longitude, not native
            # speed: signs reverse on opposite sides of both solved stations.
            def derivative(t):
                return g.delta(g.sample(t+1/1440,body)[0],g.sample(t-1/1440,body)[0])/(2/1440)
            assert derivative(b-1/24)>0 and derivative(b+1/24)<0
            assert derivative(c-1/24)<0 and derivative(c+1/24)>0
            assert abs(g.delta(events[0]['longitude_deg'],events[2]['longitude_deg']))<1e-5
            assert abs(g.delta(events[3]['longitude_deg'],events[1]['longitude_deg']))<1e-5
            for t in (a,b,c,d):
                assert g.classify(t,cycles)[0:2]==(None,'BOUNDARY')
            pre=g.classify((a+b)/2,cycles)
            assert pre[0]=='Pregrade' or (pre[1]=='UNAVAILABLE' and len(pre[2])>4)
            assert g.classify((b+c)/2,cycles)[0]=='Retrograde'
            post=g.classify((c+d)/2,cycles)
            assert post[0]=='Postgrade' or (post[1]=='UNAVAILABLE' and len(post[2])>4)
        for first,second in zip(cycles,cycles[1:]):
            left,right=first[-1]['jd_ut1'],second[0]['jd_ut1']
            if left<right:
                assert g.classify((left+right)/2,cycles)[0]=='Prograde'

@pytest.mark.parametrize('name',['Neptune','Pluto'])
def test_overlapping_real_shadows_do_not_invent_phase_precedence(name):
    with astro.LOCK:
        astro.initialize()
        cycles=g.cycles_for_month(name,2024,4)
        overlaps=[]
        for first,second in zip(cycles,cycles[1:]):
            start,end=second[0]['jd_ut1'],first[-1]['jd_ut1']
            if start<end:
                overlaps.append((start,end))
                phase,status,events=g.classify((start+end)/2,cycles)
                assert phase is None and status=='UNAVAILABLE' and len(events)==8
                # A second loop's exact boundary must beat the first loop's
                # otherwise-valid Postgrade interval.
                assert g.classify(start,cycles)[1]=='BOUNDARY'
        assert overlaps

@pytest.mark.parametrize('year',[1800,2399])
def test_search_range_failure_does_not_remove_planet(year):
    chart=calculate(BirthInput(local_date=f'{year}-01-02' if year==1800 else f'{year}-12-30',local_time='12:00:00',timezone='UTC',latitude=0,longitude=0,objects=['Mars']))
    point=chart['points'][0]
    assert point['available'] and point['longitude_deg'] is not None
    assert point['gradity']['status']=='UNAVAILABLE'
    assert point['gradity']['error_code']=='GRADITY_SEARCH_OUTSIDE_RANGE'

def test_real_api_pregrade_and_full_precision_export():
    with TestClient(app) as client:
        response=client.post('/api/charts',json={'local_date':'2024-03-25','local_time':'12:00:00','timezone':'UTC','latitude':0,'longitude':0,'objects':['Mercury','Sun','Ascendant','Fortune','NorthNodeTrue','Ceres']})
    assert response.status_code==200
    chart=response.json()
    mercury,*rest=chart['points']
    assert mercury['gradity']['phase']=='Pregrade'
    assert len(mercury['gradity']['events'])==4
    assert all(p['gradity']['status']=='NOT_APPLICABLE' for p in rest[:-1])
    assert rest[-1]['gradity']['status']=='UNAVAILABLE'
    assert json.loads(json.dumps(chart))==chart
    assert mercury['longitude_deg']!=round(mercury['longitude_deg'],6)

def test_exact_event_utc_roundtrip_remains_unassigned():
    with astro.LOCK:
        astro.initialize()
        event=g.cycles_for_month('Mercury',2024,4)[1][1]
        utc=datetime.fromisoformat(event['utc'].replace('Z','+00:00'))
        jd=astro.times(utc)['jd_ut1']
        assert abs(jd-event['jd_ut1'])*86400<0.002
        assert g.calculate_gradity('Mercury',jd,utc)['status']=='BOUNDARY'

def test_fallback_rejected_and_event_metadata_fails_closed(monkeypatch):
    g.cycles_for_month.cache_clear()
    monkeypatch.setattr(g.swe,'calc_ut',lambda *args: ((0,0,0,1,0,0),g.swe.FLG_MOSEPH))
    result=g.calculate_gradity('Mercury',2460409.25,datetime(2024,4,8,tzinfo=timezone.utc))
    assert result['phase'] is None and result['status']=='UNAVAILABLE'
    assert result['error_code']=='EPHEMERIS_BACKEND_MISMATCH'

def test_cached_events_do_not_bypass_asset_integrity(monkeypatch):
    with astro.LOCK:
        astro.initialize()
        g.cycles_for_month('Mercury',2024,4)
        def corrupt(_):
            raise g.ChartError('EPHEMERIS_ASSET_INTEGRITY','Test corrupted file')
        monkeypatch.setattr(astro,'verify_assets',corrupt)
        result=g.calculate_gradity('Mercury',2460409.25,datetime(2024,4,8,tzinfo=timezone.utc))
    assert result['status']=='UNAVAILABLE' and result['error_code']=='EPHEMERIS_ASSET_INTEGRITY'

def test_incomplete_loop_cannot_become_false_prograde(monkeypatch):
    g.cycles_for_month.cache_clear()
    original=g.shadow
    calls=0
    def missing_crossing(*args):
        nonlocal calls
        calls+=1
        if calls==3:
            raise g.ChartError('GRADITY_SHADOW_UNAVAILABLE','Fault-injected missing middle loop')
        return original(*args)
    monkeypatch.setattr(g,'shadow',missing_crossing)
    with astro.LOCK:
        astro.initialize()
        result=g.calculate_gradity('Mercury',2460409.25,datetime(2024,4,8,tzinfo=timezone.utc))
    assert result['status']=='UNAVAILABLE' and result['phase'] is None
    assert result['error_code']=='GRADITY_SHADOW_UNAVAILABLE'
