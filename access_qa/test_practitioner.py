"""Real authenticated local workflow, review isolation and privacy boundaries.

Synthetic chart only. Public CI needs no proprietary core; source interpretation
quality is not asserted by these lifecycle/security checks.
"""
import hashlib
from pathlib import Path
import tempfile
import pytest
from fastapi.testclient import TestClient
from mystic_rebels.api import app
from mystic_rebels.practitioner import ROOT, COOKIE

PASSWORD='synthetic-local-test-only'
ORIGIN='http://127.0.0.1'
BIRTH={'name':'Synthetic workflow','local_date':'2000-01-01','local_time':'12:00:00',
       'timezone':'Etc/UTC','latitude':51.4779,'longitude':0,
       'location_name':'Synthetic Greenwich fixture','time_accuracy':'nearest_minute','uncertainty_seconds':30}


@pytest.fixture
def client(monkeypatch):
    (ROOT/'tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review-test-',dir=ROOT/'tmp') as directory:
        salt=b'public-synthetic-salt'
        password='pbkdf2_sha256$100000$'+salt.hex()+'$'+hashlib.pbkdf2_hmac('sha256',PASSWORD.encode(),salt,100000).hex()
        monkeypatch.setenv('NADIA_REVIEW_STORE',directory)
        monkeypatch.setenv('NADIA_REVIEW_PASSWORD_HASH',password)
        monkeypatch.setenv('NADIA_REVIEWER_NAME','Synthetic test reviewer')
        monkeypatch.delenv('VERCEL',raising=False)
        with TestClient(app,base_url=ORIGIN,client=('127.0.0.1',54321)) as c:
            yield c


def signin(c):
    response=c.post('/api/practitioner/login',json={'password':PASSWORD},headers={'Origin':ORIGIN})
    assert response.status_code==200,response.text
    return {'Origin':ORIGIN,'X-Review-CSRF':response.json()['csrf']}


def create(c,headers,demo=True):
    response=c.post('/api/practitioner/cases',json={'birth':BIRTH,'synthetic':True,'demonstration':demo},headers=headers)
    assert response.status_code==200,response.text
    return response.json()


def draft(case):
    return [{'question_id':'love','part':part,'text':'Synthetic review content; not a personal assertion.',
        'basis':'example_content' if case['demonstration'] else 'expert_judgment',
        'evidence_ids':['point:Moon'],'source_refs':[],
        'rationale':'This is a synthetic protocol test of individual review, not semantic validation.',
        'limitations':'No real person or source-derived personal conclusion is established.',
        'practice_kind':'adaptation' if part=='practical_application' else 'not_applicable'}
        for part in ['recognition','explanation','practical_application']]


def save(c,h,case,claims):
    return c.put('/api/practitioner/cases/'+case['id']+'/claims',headers=h,
                 json={'expected_revision':case['revision'],'claims':claims})


def decision(c,h,case,claim,kind='approved',**extra):
    return c.post('/api/practitioner/cases/'+case['id']+'/decision',headers=h,json={
        'expected_revision':case['revision'],'claim_id':claim['id'],'decision':kind,
        'note':'Synthetic individual review only; no semantic certification.',
        'assertions_checked':True,'conditions_reviewed':True,**extra})


def test_authentication_origin_csrf_and_local_only(client,monkeypatch):
    assert client.get('/api/practitioner/cases').status_code==401
    assert client.post('/api/practitioner/login',json={'password':PASSWORD}).status_code==403
    assert client.post('/api/practitioner/login',json={'password':PASSWORD},headers={'Origin':'https://evil.example'}).status_code==403
    h=signin(client)
    assert client.post('/api/practitioner/cases',json={'birth':BIRTH},headers={'Origin':ORIGIN}).status_code==403
    assert client.get('/api/practitioner/cases',headers={'Host':'evil.example'}).status_code==403
    response=client.get('/api/practitioner/session')
    assert response.headers['cache-control']=='private, no-store'
    assert response.headers['x-robots-tag']=='noindex, nofollow'
    monkeypatch.setenv('VERCEL','1')
    assert client.get('/api/practitioner/cases').status_code==503


def test_wrong_password_rate_limit_cookie_and_logout(client):
    for _ in range(5):
        assert client.post('/api/practitioner/login',json={'password':'wrong'},headers={'Origin':ORIGIN}).status_code==401
    assert client.post('/api/practitioner/login',json={'password':PASSWORD},headers={'Origin':ORIGIN}).status_code==429


def test_session_cookie_rotation_and_revocation(client,monkeypatch):
    response=client.post('/api/practitioner/login',json={'password':PASSWORD},headers={'Origin':ORIGIN})
    cookie=response.headers['set-cookie']
    assert 'HttpOnly' in cookie and 'SameSite=strict' in cookie and 'Path=/api/practitioner' in cookie
    h={'Origin':ORIGIN,'X-Review-CSRF':response.json()['csrf']}
    assert client.post('/api/practitioner/logout',headers=h).status_code==200
    assert client.get('/api/practitioner/session').status_code==401
    signin(client)
    monkeypatch.setenv('NADIA_REVIEWER_NAME','Rotated actor')
    assert client.get('/api/practitioner/session').status_code==401


def test_real_chart_draft_review_report_revision_and_no_promotion(client):
    h=signin(client); case=create(client,h)
    assert case['packet']['chart']['points'] and case['packet']['privacy']['server_persistence']
    assert client.get('/api/practitioner/cases/'+case['id']+'/report').status_code==409
    case=save(client,h,case,draft(case)).json()
    for index in range(3):
        r=decision(client,h,case,case['claims'][index]); assert r.status_code==200,r.text
        case=r.json()
    report=client.get('/api/practitioner/cases/'+case['id']+'/report').json()
    assert len(report['reviewed_sections'])==1 and len(report['incomplete_questions'])==8
    assert report['demonstration'] and not report['automated_interpretation_authorized']
    assert not report['source_rule_promotion'] and report['packet']['readiness']['complete_personal_reading'] is False
    assert all(c['review']['source_verified_automatically'] is False for c in report['reviewed_sections'][0]['claims'])
    changed=draft(case)
    for new,old in zip(changed,case['claims']):new['id']=old['id']
    changed[0]['text']='Changed assertion must receive a new review.'
    updated=save(client,h,case,changed).json()
    assert updated['claims'][0]['status']=='draft' and updated['claims'][0]['review'] is None
    assert updated['claims'][1]['status']=='approved'
    assert client.get('/api/practitioner/cases/'+case['id']+'/report').status_code==409
    assert save(client,h,case,changed).status_code==409
    history=client.get('/api/practitioner/cases/'+case['id']+'/history').json()
    assert len(history)==6 and history[-1]['action']=='save_claims'
    assert client.get('/api/practitioner/benchmarks').json()==[]


def test_cross_chart_evidence_and_injected_facts_rejected(client):
    h=signin(client); case=create(client,h); claims=draft(case)
    claims[0]['house']=7
    assert save(client,h,case,claims).status_code==422
    claims=draft(case); claims[0]['evidence_ids']=['point:Invented']
    assert save(client,h,case,claims).status_code==422
    claims=draft(case); claims[0]['source_refs']=['original-page-999999']
    assert save(client,h,case,claims).status_code==422
    claims=draft(case); claims[0]['id']='another-chart-claim'
    assert save(client,h,case,claims).status_code==422
    assert client.get('/api/practitioner/cases/unknown').status_code==404


def test_review_is_not_inferred_from_fluency_or_json(client):
    h=signin(client);case=create(client,h)
    claims=draft(case);claims[0]['rationale']=''
    case=save(client,h,case,claims).json()
    assert decision(client,h,case,case['claims'][0]).status_code==422
    assert decision(client,h,case,case['claims'][1],assertions_checked=False).status_code==422
    assert decision(client,h,case,case['claims'][1],kind='rejected').status_code==200
    assert client.get('/api/practitioner/cases/'+case['id']+'/report').status_code==409


def test_source_classification_needs_source_and_demonstration_cannot_become_benchmark(client):
    h=signin(client);case=create(client,h);claims=draft(case)
    claims[0]['basis']='source_supported'
    case=save(client,h,case,claims).json()
    assert decision(client,h,case,case['claims'][0]).status_code==422
    r=client.post('/api/practitioner/cases/'+case['id']+'/benchmark-consent',headers=h,json={
        'expected_revision':case['revision'],'authorization_record':'Synthetic explicit authorization record for protocol testing only.',
        'purpose':'private_benchmark_candidate_only'})
    assert r.status_code==422
    assert client.get('/api/practitioner/source/unknown').status_code==404


def test_secondary_use_requires_separate_record_and_never_becomes_gold(client):
    h=signin(client);case=create(client,h,demo=False)
    claims=draft(case);claims[0]['basis']='example_content'
    assert save(client,h,case,claims).status_code==422
    case=save(client,h,case,draft(case)).json()
    for index in range(3):case=decision(client,h,case,case['claims'][index]).json()
    assert client.get('/api/practitioner/benchmarks').json()==[]
    r=client.post('/api/practitioner/cases/'+case['id']+'/benchmark-consent',headers=h,json={
        'expected_revision':case['revision'],'authorization_record':'Synthetic subject authorization record; no actual private reader data.',
        'purpose':'private_benchmark_candidate_only'})
    assert r.status_code==200,r.text
    library=client.get('/api/practitioner/benchmarks').json()
    assert len(library)==1 and not library[0]['gold_standard']
    assert library[0]['consent']['status']=='candidate_requires_independent_reference_review'


def test_voluntary_feedback_stays_reported_experience(client):
    h=signin(client);case=create(client,h)
    value={'expected_revision':case['revision'],'text':'A third party reported that the demonstration was understandable.',
           'reported_by':'third_party','voluntarily_supplied':False}
    url='/api/practitioner/cases/'+case['id']+'/feedback'
    assert client.post(url,headers=h,json=value).status_code==422
    value['voluntarily_supplied']=True
    response=client.post(url,headers=h,json=value)
    assert response.status_code==200,response.text
    recorded=response.json()['reader_feedback'][0]
    assert recorded['reported_by']=='third_party'
    assert recorded['status']=='reported_experience_not_source_or_predictive_validation'
    assert client.get('/api/practitioner/benchmarks').json()==[]
