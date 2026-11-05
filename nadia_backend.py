"""Private core adapter. Never import this module from browser code."""
from __future__ import annotations
import hmac
import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from nadia_runtime import ROOT, VERSION, COMMIT, SHA256, WHEEL, verified_core

router = APIRouter()

def structured_evidence(chart, question, owner_id, *, motion=None):
    """Internal trusted-server component API; never an unrestricted reading route."""
    core = verified_core()
    from nadia_core.synthesis import compose, validate_composition
    evidence = compose(core, chart, question, owner_id, motion=motion)
    validation = validate_composition(core, evidence, chart, question, owner_id, motion=motion)
    if not validation['valid'] or evidence.get('personal_reading_allowed') is not False or evidence.get('complete_question_answer') is not False:
        raise ValueError('Scoped evidence gate mismatch')
    return evidence

def health_payload():
    verified_core()
    return {'status': 'ready', 'knowledge_version': VERSION, 'core_commit': COMMIT,
            'artifact_sha256': SHA256, 'personal_readings_allowed': False,
            'capabilities': {'release_health': True, 'personal_readings': False,
                             'source_verified_interpretation': 'partial_components_only',
                             'structured_evidence': 'internal_server_only',
                             'astronomical_engine': 'existing_engine_not_checked_by_this_endpoint',
                             'public_rule_retrieval': False}}

@router.get('/api/nadia/health')
def health(request: Request):
    token = os.environ.get('NADIA_HEALTH_TOKEN', '')
    supplied = request.headers.get('authorization', '')
    headers = {'Cache-Control': 'private, no-store'}
    if len(token) < 32 or not hmac.compare_digest(supplied.encode(), ('Bearer ' + token).encode()):
        return JSONResponse({'status': 'unauthorized'}, status_code=401, headers=headers)
    try:
        return JSONResponse(health_payload(), headers=headers)
    except Exception:
        return JSONResponse({'status': 'unavailable'}, status_code=503, headers=headers)
