"""Required private deployment preflight; missing assets FAIL rather than skip.

Run after install_nadia.py. Output contains metadata only, never rule content.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fastapi import FastAPI
from fastapi.testclient import TestClient
import nadia_backend as backend
from site_access import SitePasswordGate

app = FastAPI()
app.include_router(backend.router)
client = TestClient(SitePasswordGate(app))
with patch.dict(os.environ, {'VERCEL': '1', 'NADIA_HEALTH_TOKEN': 'local-test-only-token-0000000000000000'}):
    assert client.get('/api/nadia/health').status_code == 401
    response = client.get('/api/nadia/health', headers={'Authorization': 'Bearer local-test-only-token-0000000000000000'})
    assert response.status_code == 200, response.json()
    payload = response.json()
    assert payload['artifact_sha256'] == backend.SHA256
    assert payload['core_commit'] == backend.COMMIT
    assert payload['knowledge_version'] == backend.VERSION
    assert payload['personal_readings_allowed'] is False
    assert payload['capabilities']['personal_readings'] is False
    assert set(payload) == {'status', 'artifact_sha256', 'core_commit', 'knowledge_version', 'personal_readings_allowed', 'capabilities'}
# Restart compatibility with the same immutable runtime is the rollback target.
subprocess.run([sys.executable, '-c', 'from nadia_backend import verified_core; verified_core()'], cwd=ROOT, check=True)
print(json.dumps({'private_preflight': 'passed', 'restart_pin_verified': True, **payload}))
