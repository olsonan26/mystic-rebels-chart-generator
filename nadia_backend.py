"""Private core adapter. Never import this module from browser code."""
from __future__ import annotations
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys
import zipfile
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parent
VERSION = '0.7.0'
COMMIT = '5a472f5f8236aa53ae90529a91a6ad20dd9e1382'
SHA256 = '352bb1251ef471e9535ae514ba4ea692411ee91ab0a14d18f269002818b1612b'
WHEEL = 'nadia_knowledge_core-0.7.0-py3-none-any.whl'
router = APIRouter()

def verified_core(runtime=None):
    runtime = Path(runtime) if runtime else ROOT / '.nadia-private'
    wheel = runtime / WHEEL
    if hashlib.sha256(wheel.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Private release integrity failure')
    site = runtime / 'site'
    with zipfile.ZipFile(wheel) as archive:
        names = {n for n in archive.namelist() if n.startswith('nadia_core/') and not n.endswith('/')}
        actual = {p.relative_to(site).as_posix() for p in (site / 'nadia_core').rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts}
        if actual != names:
            raise ValueError('Private installation file set mismatch')
        for name in names:
            if (site / name).read_bytes() != archive.read(name):
                raise ValueError('Private installation integrity failure')
    identity = json.loads((site / 'nadia_core/data/distribution.json').read_text())
    if (identity.get('commit'), identity.get('knowledge_version'), identity.get('personal_readings_allowed')) != (COMMIT, VERSION, False):
        raise ValueError('Private release identity mismatch')
    sys.path.insert(0, str(site))
    from nadia_core import KnowledgeCore
    import nadia_core
    if Path(nadia_core.__file__).resolve() != (site / 'nadia_core/__init__.py').resolve():
        raise ValueError('Unexpected private module origin')
    core = KnowledgeCore(version=VERSION)
    if core.manifest.get('personal_readings_approved') is not False:
        raise ValueError('Personal reading gate mismatch')
    return core

def health_payload():
    verified_core()
    return {'status': 'ready', 'knowledge_version': VERSION, 'core_commit': COMMIT,
            'artifact_sha256': SHA256, 'personal_readings_allowed': False,
            'capabilities': {'release_health': True, 'personal_readings': False,
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
