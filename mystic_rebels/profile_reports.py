"""Ephemeral, source-governed profile documents; never complete personal readings.

The public consumer contains presentation and gates, not the private rule library.
Chart calculations reuse the existing engine. Source vocabulary is obtained only
from the integrity-verified, immutable private release on the server.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from .errors import ChartError
from .models import BirthInput
from .service import calculate
from nadia_runtime import verified_core, VERSION, COMMIT

router = APIRouter()
MAJORS = ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto')
ROOT = Path(__file__).resolve().parents[1]
LEAD_QUESTION = 'What is the ONE thing you need to feel loved that other people keep missing?'
METHOD_GAPS = [
    'Spark and degree/FCA authority remains unresolved.',
    'Complete body-angle limits and exact contact boundaries are not established.',
    'Complete related-configuration meaning and personal synthesis are not approved.',
    'Motion shadow overlap, exact boundaries and progressed-context applicability remain unresolved.',
    'All essential natal report requirements must be source-verified, implemented and tested before a complete personal reading is available.',
]


class ProfileRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    birth: BirthInput
    tier: Literal['essential', 'premium'] = 'essential'
    synthetic: bool = False


def booking_url():
    """Owner-supplied configuration only; never guess a live booking destination."""
    value = os.environ.get('NADIA_BOOKING_URL', '').strip()
    parts = urlsplit(value)
    if parts.scheme == 'https' and parts.hostname and not parts.username and not parts.password and not any(c.isspace() for c in value):
        return value
    return None


def report_section(identity, title, status, summary, *, facts=(), refs=(), rules=(), blockers=(), required_facts=(), evidence=None):
    return {'id': identity, 'title': title, 'status': status, 'summary': summary,
            'facts': list(facts), 'source_refs': sorted(set(refs)), 'rule_ids': sorted(set(rules)),
            'blockers': list(blockers), 'required_facts': list(required_facts),
            'calculation_evidence': evidence or {}, 'personal_interpretation_approved': False}


def generate_report(request: ProfileRequest):
    if request.birth.chart_type != 'natal':
        raise ChartError('NATAL_PROFILE_REQUIRED', 'Choose a natal chart for a profile report.')
    # The user-selected chart object list must not omit required natal context.
    birth = request.birth.model_copy(update={'objects': list(MAJORS) + ['Ascendant', 'Midheaven']})
    chart = calculate(birth)
    # A document has stable identity for identical input, independent of wall clock.
    chart.pop('created_at_utc', None)
    chart = deepcopy(chart)
    uncertain = (birth.time_accuracy in {'unknown', 'approximate'} or birth.local_time is None
                 or birth.uncertainty_seconds is None or birth.uncertainty_seconds > 30)
    if uncertain:
        chart['angles'] = {}
        chart['whole_sign_cusps'] = []
        for point in chart['points']:
            for key in ('house', 'field', 'true_placement'):
                point[key] = None
            if point['id'] in {'Ascendant', 'Midheaven'}:
                point.update(available=False, longitude_deg=None,
                             error={'code': 'UNCERTAIN_BIRTH_TIME', 'message': 'A sufficiently precise birth time is required.'})
    points = {p['id']: p for p in chart['points'] if p.get('available') and p.get('longitude_deg') is not None}
    positions = {b: points[b]['longitude_deg'] for b in MAJORS if b in points}
    missing = sorted(set(MAJORS) - positions.keys())
    limitations = list(METHOD_GAPS)
    if uncertain:
        limitations.insert(0, 'Birth time is missing or uncertain. Houses, angles, Delegates and related house context are unavailable; positions describe the labelled reference epoch only.')
    else:
        limitations.insert(0, 'Positions and house assignments describe the entered birth instant; rounding for display does not establish certainty throughout a birth-time interval.')
    sections = [report_section('calculated-chart', 'Your calculated chart', 'calculated',
                'Tropical, geocentric positions calculated by the existing astronomical engine. Whole Sign houses are shown only with sufficiently precise birth time.',
                facts=[{'label': b, 'value': points[b]['display_dms'] + (' (reference epoch)' if uncertain else '')} for b in MAJORS if b in points],
                blockers=['Unavailable body: ' + b for b in missing], required_facts=['birth_date', 'timezone', 'coordinates'],
                evidence={'chart_id': chart['chart_id'], 'time': chart['time'], 'configuration': chart['configuration']})]
    core_identity = None
    knowledge_status = 'unavailable'
    components = []
    source_refs = set()
    try:
        core = verified_core()
        if core.manifest.get('personal_readings_approved') is not False:
            raise ValueError('Unexpected personal interpretation approval')
        knowledge_status = 'verified'
        core_identity = {'version': VERSION, 'commit': COMMIT}
        ascendant = chart['angles'].get('Ascendant')
        if not missing and ascendant is not None:
            from nadia_core.interpretation import function_components
            components = function_components(core, positions, ascendant)
        else:
            # Do not invent an Ascendant to make the source component API work.
            for body in MAJORS:
                definition = core.cross_chapter['planetary_functions'][body]
                rule = core.rules[definition['rule_id']]
                closure = core.dependencies([rule['id']])
                if closure['missing'] or closure['cycles'] or any(not core.eligible(core.rules[r]) for r in closure['rule_ids']):
                    raise ValueError('Unverified source vocabulary')
                components.append({'body': body, 'function': definition['label'],
                                   'source_keywords': definition['keywords'], 'rule_ids': closure['rule_ids'],
                                   'source_refs': rule['source_refs'], 'personal_inference_allowed': False})
        for component in components:
            body = component['body']
            if component.get('personal_inference_allowed') is not False:
                raise ValueError('Unsupported inference')
            facts = [{'label': 'Source function', 'value': component['function']},
                     {'label': 'Source vocabulary', 'value': ', '.join(component['source_keywords'])}]
            if 'placement' in component:
                p = component['placement']
                facts += [{'label': 'Field / house', 'value': f"{p['field']} / {p['house']}"},
                          {'label': 'Tone', 'value': p['tone']}, {'label': 'Pulse', 'value': p['pulse']},
                          {'label': 'Forward ruler', 'value': p['sign_ruler']}]
                for delegate in component['ruler_context']['delegates']:
                    facts.append({'label': 'Ruled house and occupants', 'value': f"{delegate['sign']}, house {delegate['house']}: " + (', '.join(delegate['occupant_ids']) or 'no major-body occupants')})
            source_refs.update(component['source_refs'])
            sections.append(report_section('placement-' + body.lower(), body + ': source context', 'source_vocabulary',
                'The source associates this planetary function with the vocabulary below. The chart links are calculated context; they do not establish a psychological conclusion about you.',
                facts=facts, refs=component['source_refs'], rules=component['rule_ids'],
                blockers=['Complete planetary conditions and related personal meaning are not approved.'] + (['House context unavailable.'] if uncertain else []),
                required_facts=['verified_major_body_positions', 'source_approved_vocabulary'],
                evidence={'body': body, 'longitude_deg': positions.get(body), 'house_context_available': 'placement' in component}))
    except (OSError, ValueError, KeyError, ImportError):
        # Never fall back to legacy source dictionaries or fabricated interpretations.
        knowledge_status = 'unavailable'
        core_identity = None
        components = []
        source_refs.clear()
        sections = sections[:1]
        limitations.insert(0, 'Verified source components are temporarily unavailable. Calculated chart facts remain available.')
    # Reuse the established eighteen-section product architecture. Preserve the
    # distinction between universal natal context and optional specialized contexts.
    catalog = json.loads((ROOT / 'data/knowledge/interpretive_inventory.json').read_text(encoding='utf-8'))
    for section in catalog['report_sections']:
        natal = 'natal' in section['contexts']
        sections.append(report_section(section['id'], section['title'], 'unavailable',
            'Complete personal interpretation is awaiting verified source requirements, implementation and tests.' if natal else 'This specialized context needs a separately verified method and additional inputs.',
            rules=section['rule_ids'], required_facts=section['required_chart_facts'],
            blockers=METHOD_GAPS if natal else ['Specialized method and context not approved for this natal profile.']))
    identity = {'birth': birth.model_dump(mode='json'), 'tier': request.tier, 'synthetic': request.synthetic,
                'schema_version': 'nadia-profile/1', 'core_identity': core_identity}
    report_id = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    return {'schema_version': 'nadia-profile/1', 'report_id': report_id, 'tier': request.tier, 'synthetic': request.synthetic,
            'profile': {'name': birth.name, 'birth_date': birth.local_date, 'birth_time': birth.local_time,
                        'location': birth.location_name, 'timezone': birth.timezone, 'time_accuracy': birth.time_accuracy},
            'chart': chart, 'core_identity': core_identity,
            'readiness': {'technical_report_ready': not missing, 'complete_personal_reading': False,
                          'interpretation_status': 'blocked', 'knowledge_status': knowledge_status, 'limitations': limitations},
            'sections': sections,
            'lead': {'question': LEAD_QUESTION,
                     'reflection_question': 'When have you felt understood and cared for, and what did the other person do?',
                     'personalized_answer': None, 'booking_url': booking_url(),
                     'readiness': 'reflection_only_personalized_answer_blocked',
                     'required_context': ['whole_natal_chart', 'planetary_functions', 'Field_Tone_Pulse', 'bidirectional_rulership_and_occupants', 'planetary_conditions_and_contacts', 'reported_personal_context', 'verified_contextual_synthesis'],
                     'source_refs': sorted(source_refs), 'blockers': METHOD_GAPS},
            'privacy': {'server_persistence': False, 'browser_persistence': False,
                        'exports': 'Birth details are included in downloads and printouts. Share them deliberately.'}}


@router.post('/api/profile-reports')
def profile_report(data: ProfileRequest, request: Request):
    origin = request.headers.get('origin')
    origin_parts = urlsplit(origin or '')
    # Vite proxies5173 ->8000 during local development. This exception is limited
    # to loopback on both sides and is disabled for every Vercel deployment.
    local_dev = (not os.environ.get('VERCEL') and origin_parts.scheme == 'http'
                 and origin_parts.hostname in {'127.0.0.1', 'localhost'}
                 and request.url.hostname in {'127.0.0.1', 'localhost'})
    if origin and origin_parts.netloc != request.headers.get('host', '') and not local_dev:
        return JSONResponse({'error': {'code': 'INVALID_ORIGIN', 'message': 'Open the report in this application.'}}, status_code=403)
    return JSONResponse(generate_report(data), headers={'Cache-Control': 'private, no-store', 'X-Robots-Tag': 'noindex, nofollow'})
