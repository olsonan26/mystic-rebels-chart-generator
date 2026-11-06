"""Local-only, authenticated individual review. Never a source-rule promotion.

SQLite stores private cases and append-only revisions in ignored tmp. Deployment
is intentionally disabled: this is a single-practitioner local product workflow.
The existing site gate and all Knowledge Core approval flags remain unchanged.
"""
from __future__ import annotations
from contextlib import contextmanager

import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import sqlite3
import time
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from .profile_reports import ROOT, MAJORS, ProfileRequest, generate_report
from nadia_runtime import verified_core
from site_access import password_valid

COOKIE = 'nadia_practitioner'
QUESTIONS = {
    'identity': 'What makes me different from everyone else?',
    'strengths': 'What are my greatest strengths and natural abilities?',
    'challenges': 'What are my biggest weaknesses?',
    'motivation': 'What naturally motivates me?',
    'talents': 'What talents might I not recognize?',
    'relationships': 'What relationship patterns deserve my attention?',
    'family': 'What can I understand about my family relationships?',
    'application': 'How can I apply what I have learned?',
    'love': 'What do I need to feel loved?',
}
PARTS = ('recognition', 'explanation', 'practical_application')


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def config():
    directory = Path(os.environ.get('NADIA_REVIEW_STORE', '')).resolve()
    password = os.environ.get('NADIA_REVIEW_PASSWORD_HASH', '')
    actor = os.environ.get('NADIA_REVIEWER_NAME', '').strip()
    if (os.environ.get('VERCEL') or not os.environ.get('NADIA_REVIEW_STORE')
            or not directory.is_relative_to((ROOT/'tmp').resolve())
            or not password.startswith('pbkdf2_sha256$') or not actor):
        raise HTTPException(503, 'Private review is not configured on this machine.')
    return directory, password, actor


@contextmanager
def database():
    directory, _, _ = config()
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    db = sqlite3.connect(directory/'review.sqlite3', timeout=15)
    db.row_factory = sqlite3.Row
    db.executescript('''
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, csrf TEXT,
            expires REAL, actor TEXT, configuration TEXT);
        CREATE TABLE IF NOT EXISTS attempts(address TEXT PRIMARY KEY, failures INTEGER,
            last_failure REAL);
        CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY, actor TEXT, revision INTEGER,
            document TEXT);
        CREATE TABLE IF NOT EXISTS history(case_id TEXT, revision INTEGER, actor TEXT,
            action TEXT, created REAL, document TEXT, PRIMARY KEY(case_id, revision));
    ''')
    try:
        with db:
            yield db
    finally:
        db.close()


def boundary(request: Request):
    config()
    if (request.url.hostname not in {'localhost', '127.0.0.1', '::1'}
            or not request.client or request.client.host not in {'127.0.0.1', '::1'}):
        raise HTTPException(403, 'Private review is available only on this computer.')
    if request.method not in {'GET', 'HEAD'}:
        expected = str(request.base_url).rstrip('/')
        if request.headers.get('origin') != expected:
            raise HTTPException(403, 'Open private review in this application.')


router = APIRouter(prefix='/api/practitioner', dependencies=[Depends(boundary)])


def authenticated(request: Request):
    _, password, actor = config()
    raw = request.cookies.get(COOKIE, '')
    with database() as db:
        row = db.execute('SELECT * FROM sessions WHERE token=?',
                         (hashlib.sha256(raw.encode()).hexdigest(),)).fetchone()
    if (not row or row['expires'] <= time.time() or row['actor'] != actor
            or row['configuration'] != digest([password, actor])):
        raise HTTPException(401, 'Sign in to the private practitioner workspace.')
    if request.method not in {'GET', 'HEAD'} and not hmac.compare_digest(
            request.headers.get('x-review-csrf', ''), row['csrf']):
        raise HTTPException(403, 'Review session check failed. Sign in again.')
    return dict(row)


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Login(Strict):
    password: str = Field(min_length=1, max_length=256)


@router.post('/login')
def login(data: Login, request: Request, response: Response):
    _, password, actor = config()
    address = request.client.host
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        previous = db.execute('SELECT * FROM attempts WHERE address=?', (address,)).fetchone()
        if previous and previous['failures'] >= 5 and time.time()-previous['last_failure'] < 60:
            raise HTTPException(429, 'Too many attempts. Wait a minute before trying again.')
        if not password_valid(data.password, password):
            failures = previous['failures']+1 if previous and time.time()-previous['last_failure'] < 60 else 1
            db.execute('INSERT OR REPLACE INTO attempts VALUES(?,?,?)', (address, failures, time.time()))
            db.commit()
            raise HTTPException(401, 'The practitioner password did not match.')
        db.execute('DELETE FROM attempts WHERE address=?', (address,))
        raw, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        db.execute('DELETE FROM sessions WHERE expires < ?', (time.time(),))
        db.execute('INSERT INTO sessions VALUES(?,?,?,?,?)',
                   (hashlib.sha256(raw.encode()).hexdigest(), csrf, time.time()+28800,
                    actor, digest([password, actor])))
    response.set_cookie(COOKIE, raw, httponly=True, secure=request.url.scheme == 'https',
                        samesite='strict', path='/api/practitioner', max_age=28800)
    return {'actor': actor, 'csrf': csrf, 'scope': 'individual_review_only'}


@router.get('/session')
def session(who=Depends(authenticated)):
    return {'actor': who['actor'], 'csrf': who['csrf'], 'scope': 'individual_review_only'}


@router.post('/logout')
def logout(request: Request, response: Response, who=Depends(authenticated)):
    with database() as db:
        db.execute('DELETE FROM sessions WHERE token=?', (who['token'],))
    response.delete_cookie(COOKIE, path='/api/practitioner')
    return {'signed_out': True}


def preparation(packet, owner):
    facts = {}
    for p in packet['chart']['points']:
        if p['available']:
            facts['point:'+p['id']] = {'kind': 'calculated', 'label': p['name'], 'value': p}
    meanings = {}
    for section in packet['sections']:
        if section['status'] == 'unavailable':
            continue
        meanings['section:'+section['id']] = {
            'kind': section['status'], 'label': section['title'], 'value': section,
            'authority': 'component_scope_only_not_personal_entailment'}
    sources = sorted({r for s in packet['sections'] for r in s['source_refs']})
    preparation = {'evidence': {**facts, **meanings}, 'source_refs': sources,
                   'relationships': None, 'bounded_suggestions': [],
                   'missing': packet['readiness']['limitations'],
                   'selection': 'All available context retained. Reviewer selects question-specific relevance; no automatic dominance ranking.'}
    if packet['readiness']['knowledge_status'] == 'verified' and packet['chart']['angles'].get('Ascendant') is not None:
        core = verified_core()
        from nadia_core.methodology import context_graph
        points = {p['id']: p for p in packet['chart']['points'] if p['id'] in MAJORS and p['available']}
        positions = {b:p['longitude_deg'] for b,p in points.items()}
        asc = packet['chart']['angles']['Ascendant']
        if len(positions) == 10:
            preparation['relationships'] = context_graph(positions, asc)
            # Reuse the existing bounded operation; suggestions remain unapproved.
            from nadia_core.interpretation import function_components
            from scripts.personal_review import bounded_need
            components = function_components(core, positions, asc)
            moon = next(c for c in components if c['body']=='Moon')
            suggestion = bounded_need(core, moon, positions, asc, owner_id=owner)
            preparation['bounded_suggestions'].append(suggestion)
            preparation['evidence']['bounded:Moon'] = {
                'kind':'bounded_hypothesis','label':'Moon bounded starting theme',
                'value':suggestion,'authority':'unapproved_partial_theme_not_personal_entailment'}
            preparation['source_refs'] = sorted(set(preparation['source_refs']) | set(suggestion['source_refs']))
            # Reuse the existing typed Base return, retaining its exclusions.
            from nadia_core.synthesis import compose
            from scripts.semantic_return import ReviewSession
            record={'ascendant':asc,'utc':packet['chart']['time']['birth_utc'],
                'positions':{b:{'longitude':p['longitude_deg'],'retrograde':p['retrograde'],
                    'longitude_speed_deg_day':p['speed_longitude_deg_per_day']} for b,p in points.items()}}
            motion={'bodies':{}}
            for b,p in points.items():
                grade=p.get('gradity',{});phase=(grade.get('phase') or '').casefold()
                if grade.get('status')=='NOT_APPLICABLE' and b in {'Sun','Moon'}:
                    motion['bodies'][b]={'body':b,'phase':'NOT APPLICABLE','when':record['utc']}
                elif grade.get('status')=='VERIFIED' and phase in {'pregrade','postgrade','prograde','retrograde'}:
                    motion['bodies'][b]={'body':b,'phase':phase,'when':record['utc']}
            focus='What do I need to feel loved?'
            composition=compose(core,record,focus,owner,motion=motion)
            review={'calculated_record':record,'calculated_record_sha256':digest(record),
                'composition':composition,'question':focus,'owner_id':owner,'motion_input':motion,'components':components}
            returned=ReviewSession(core,review).evidence()
            preparation['evidence']['bounded:Moon:base-return']={
                'kind':'bounded_hypothesis','label':'Moon represented-Field partial return','value':returned,
                'authority':'partial_rule_application_not_complete_occupant_return'}
            preparation['bounded_suggestions'].append({'theme':next(iter(returned['claims'].values()),None),
                'blockers':returned['missing']})
            preparation['evidence']['composition']={'kind':'source_scoped_relationships',
                'label':'Verified contacts, motion and directional composition','value':composition,
                'authority':'structural_and_scoped_source_claims_not_complete_personal_synthesis'}
            for c in components:
                preparation['evidence']['component:'+c['body']] = {
                    'kind': 'source_component', 'label': c['body']+' full source component', 'value': c,
                    'authority': 'conditions_not_fully_interpreted'}
    return preparation


class CreateCase(ProfileRequest):
    demonstration: bool = False
    purpose: str = Field(default='Individual profile review only', min_length=10, max_length=500)


def write(db, case, actor, action):
    case['revision'] += 1
    db.execute('INSERT OR REPLACE INTO cases VALUES(?,?,?,?)',
               (case['id'], actor, case['revision'], canonical(case)))
    db.execute('INSERT INTO history VALUES(?,?,?,?,?,?)',
               (case['id'], case['revision'], actor, action, time.time(), canonical(case)))


def load(db, identity, actor):
    row = db.execute('SELECT * FROM cases WHERE id=? AND actor=?', (identity, actor)).fetchone()
    if not row:
        raise HTTPException(404, 'Review case not found.')
    case = json.loads(row['document'])
    if digest(case['packet']) != case['packet_hash'] or digest(case['preparation']) != case['preparation_hash']:
        raise HTTPException(409, 'The protected evidence snapshot changed. Create a new case.')
    return case


def revision(case, expected):
    if case['revision'] != expected:
        raise HTTPException(409, 'This case changed in another view. Reload before editing.')


@router.post('/cases')
def create_case(data: CreateCase, who=Depends(authenticated)):
    packet = generate_report(ProfileRequest(birth=data.birth, tier=data.tier, synthetic=data.synthetic))
    packet['privacy'].update(server_persistence=True, local_only=True,
                             purpose='Authenticated individual practitioner case')
    prepared = preparation(packet, packet['report_id'])
    case = {'id': uuid4().hex, 'revision': 0, 'packet': packet, 'packet_hash': digest(packet),
            'preparation': prepared, 'preparation_hash': digest(prepared),
            'demonstration': data.demonstration, 'purpose': data.purpose,
            'questions': QUESTIONS, 'claims': [], 'benchmark_consent': None, 'reader_feedback': [],
            'automated_interpretation_authorized': False, 'source_rule_promotion': False}
    with database() as db:
        write(db, case, who['actor'], 'create_case')
    return case


@router.get('/cases')
def cases(who=Depends(authenticated)):
    with database() as db:
        rows = db.execute('SELECT document FROM cases WHERE actor=? ORDER BY rowid DESC', (who['actor'],)).fetchall()
    return [{'id':c['id'], 'name':c['packet']['profile']['name'], 'revision':c['revision'],
             'demonstration':c['demonstration']} for row in rows for c in [json.loads(row['document'])]]


@router.get('/cases/{identity}')
def get_case(identity: str, who=Depends(authenticated)):
    with database() as db:
        return load(db, identity, who['actor'])


class Claim(Strict):
    id: str | None = None
    question_id: Literal['identity','strengths','challenges','motivation','talents','relationships','family','application','love']
    part: Literal['recognition','explanation','practical_application']
    text: str = Field(max_length=4000)
    basis: Literal['source_supported','expert_judgment','example_content']
    evidence_ids: list[str] = Field(max_length=40)
    source_refs: list[str] = Field(max_length=80)
    rationale: str = Field(max_length=4000)
    limitations: str = Field(max_length=2000)
    rejected_alternative: str = Field(default='', max_length=2000)
    practice_kind: Literal['not_applicable','source_practice','adaptation'] = 'not_applicable'


class Save(Strict):
    expected_revision: int
    claims: list[Claim] = Field(max_length=27)


@router.put('/cases/{identity}/claims')
def save_claims(identity: str, data: Save, who=Depends(authenticated)):
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        case = load(db, identity, who['actor']); revision(case, data.expected_revision)
        old = {c['id']:c for c in case['claims']}
        seen, parts, updated = set(), set(), []
        for item in data.claims:
            value = item.model_dump(); key = value['id'] or uuid4().hex
            if (key in seen or (value['question_id'], value['part']) in parts
                    or (value['id'] and key not in old)):
                raise HTTPException(422, 'Duplicate or unknown claim identity.')
            if (set(value['evidence_ids']) - case['preparation']['evidence'].keys()
                    or set(value['source_refs']) - set(case['preparation']['source_refs'])):
                raise HTTPException(422, 'Evidence must reference this protected chart/source snapshot.')
            if value['basis']=='example_content' and not case['demonstration']:
                raise HTTPException(422, 'Example content belongs only in a labeled demonstration case.')
            value['id']=key
            unchanged = key in old and all(old[key].get(k)==v for k,v in value.items())
            value.update(status=old[key]['status'] if unchanged else 'draft',
                         review=old[key]['review'] if unchanged else None)
            updated.append(value); seen.add(key); parts.add((value['question_id'], value['part']))
        case['claims'] = updated
        # Any edit also withdraws any previous authorization for secondary use.
        case['benchmark_consent'] = None
        write(db, case, who['actor'], 'save_claims')
    return case


class Decision(Strict):
    expected_revision: int
    claim_id: str
    decision: Literal['approved','revise','rejected']
    note: str = Field(min_length=10, max_length=2000)
    assertions_checked: bool = False
    conditions_reviewed: bool = False


@router.post('/cases/{identity}/decision')
def decide(identity: str, data: Decision, who=Depends(authenticated)):
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        case=load(db,identity,who['actor']); revision(case,data.expected_revision)
        claim=next((c for c in case['claims'] if c['id']==data.claim_id),None)
        if not claim:
            raise HTTPException(404,'Claim not found.')
        if data.decision=='approved':
            if (not data.assertions_checked or not data.conditions_reviewed or not claim['text'].strip()
                    or not claim['evidence_ids'] or len(claim['rationale'].strip())<20
                    or len(claim['limitations'].strip())<10):
                raise HTTPException(422,'Review every assertion, evidence link, rationale and unresolved condition before approval.')
            if claim['basis']=='source_supported' and (not claim['source_refs'] or case['packet']['readiness']['knowledge_status']!='verified'):
                raise HTTPException(422,'Source-supported individual claims require available verified source components and references.')
            if claim['part']=='practical_application' and (claim['practice_kind']=='not_applicable'
                    or claim['practice_kind']=='source_practice' and not claim['source_refs']):
                raise HTTPException(422,'Identify an applicable sourced practice or a new adaptation.')
        claim['status']=data.decision
        claim['review']={'actor':who['actor'],'note':data.note,'at':time.time(),
                         'assertions_checked':data.assertions_checked,'conditions_reviewed':data.conditions_reviewed,
                         'scope':'individual_case_only','source_verified_automatically':False,
                         'content_hash':digest({k:v for k,v in claim.items() if k not in {'review','status'}})}
        case['benchmark_consent']=None
        write(db,case,who['actor'],'claim_'+data.decision)
    return case


def assembled(case):
    sections=[]
    for identity, question in QUESTIONS.items():
        claims=[c for c in case['claims'] if c['question_id']==identity]
        if {c['part'] for c in claims if c['status']=='approved'}==set(PARTS):
            sections.append({'id':identity,'question':question,
                             'claims':[next(c for c in claims if c['part']==part) for part in PARTS]})
    if not sections:
        raise HTTPException(409,'Approve Recognition, Explanation and Practical Application for at least one question before assembling a report.')
    return {'schema_version':'nadia-individual-review/1','case_id':case['id'],'revision':case['revision'],
            'packet':case['packet'],'reviewed_sections':sections,
            'incomplete_questions':[q for key,q in QUESTIONS.items() if key not in {s['id'] for s in sections}],
            'demonstration':case['demonstration'],
            'review_scope':'demonstration_only_not_expert_reading' if case['demonstration'] else 'practitioner_reviewed_individual_sections',
            'complete_personal_profile':False,'automated_interpretation_authorized':False,
            'source_rule_promotion':False}


@router.get('/cases/{identity}/report')
def report(identity: str, who=Depends(authenticated)):
    with database() as db:
        return assembled(load(db,identity,who['actor']))


@router.get('/cases/{identity}/history')
def history(identity: str, who=Depends(authenticated)):
    with database() as db:
        load(db,identity,who['actor'])
        return [dict(r) for r in db.execute('SELECT revision,actor,action,created FROM history WHERE case_id=? ORDER BY revision',(identity,)).fetchall()]


class Consent(Strict):
    expected_revision: int
    authorization_record: str = Field(min_length=30,max_length=2000)
    purpose: Literal['private_benchmark_candidate_only']


class Feedback(Strict):
    expected_revision: int
    text: str = Field(min_length=10,max_length=2000)
    reported_by: Literal['reader','third_party']
    voluntarily_supplied: bool


@router.post('/cases/{identity}/feedback')
def feedback(identity: str, data: Feedback, who=Depends(authenticated)):
    if not data.voluntarily_supplied:
        raise HTTPException(422,'Record only voluntarily supplied feedback for this review.')
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        case=load(db,identity,who['actor']); revision(case,data.expected_revision)
        case.setdefault('reader_feedback',[]).append({'text':data.text,'reported_by':data.reported_by,
            'voluntarily_supplied':True,'recorded_by':who['actor'],'at':time.time(),
            'status':'reported_experience_not_source_or_predictive_validation'})
        case['benchmark_consent']=None
        write(db,case,who['actor'],'record_voluntary_feedback')
    return case


@router.post('/cases/{identity}/benchmark-consent')
def consent(identity: str, data: Consent, who=Depends(authenticated)):
    with database() as db:
        db.execute('BEGIN IMMEDIATE')
        case=load(db,identity,who['actor']); revision(case,data.expected_revision)
        if case['demonstration']:
            raise HTTPException(422,'Demonstration content cannot enter the expert benchmark library.')
        assembled(case)
        case['benchmark_consent']={'authorization_record':data.authorization_record,'purpose':data.purpose,
                                  'recorded_by':who['actor'],'at':time.time(),'reviewed_revision':case['revision'],
                                  'status':'candidate_requires_independent_reference_review','gold_standard':False}
        write(db,case,who['actor'],'record_secondary_use_authorization')
    return case


@router.get('/benchmarks')
def benchmarks(who=Depends(authenticated)):
    with database() as db:
        rows=db.execute('SELECT document FROM cases WHERE actor=?',(who['actor'],)).fetchall()
    return [{'case_id':c['id'],'consent':c['benchmark_consent'],'questions':assembled(c)['reviewed_sections'],
             'chart_configuration':c['packet']['chart'],'source_identity':c['packet']['core_identity'],
             'gold_standard':False,'reader_feedback':c.get('reader_feedback',[]),'metrics':{
                 k:'requires_independent_evaluation' for k in ['factual_correctness','source_fidelity','contextual_correctness','specificity','expert_agreement','reader_usefulness']}}
            for r in rows for c in [json.loads(r['document'])] if c.get('benchmark_consent') and not c['demonstration']]


def local_references():
    path=ROOT/'tmp/practitioner-reference/benchmarks.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {'examples':[],'gold_standard':None}


@router.get('/references')
def references(who=Depends(authenticated)):
    return local_references()


@router.get('/source/{ref}')
def source(ref: str, who=Depends(authenticated)):
    try:
        core=verified_core()
        record=core.sources.get(ref)
        if not record:
            record=next((s for s in local_references().get('source_media',[]) if s['id']==ref),None)
        identity=record['file_id']
        if not identity or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in identity):
            raise ValueError()
        path=ROOT.parent/'Mystic-Rebels/reference/originals'/(identity+'.jpg')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:
            raise ValueError()
    except (ValueError,KeyError,TypeError,OSError):
        raise HTTPException(404,'Verified original source image is not available locally.')
    return FileResponse(path,media_type='image/jpeg',headers={'Cache-Control':'private, no-store'})
