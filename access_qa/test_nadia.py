"""Public tests need no private assets. Actual-wheel checks run separately."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
import nadia_backend as backend
from site_access import SitePasswordGate

class NadiaBoundaryTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        app.include_router(backend.router)
        self.client = TestClient(SitePasswordGate(app))
        self.env = patch.dict(os.environ, {'VERCEL': '1', 'NADIA_HEALTH_TOKEN': 'x' * 32})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_anonymous_and_wrong_token_are_rejected_before_loading(self):
        with patch.object(backend, 'health_payload') as load:
            for headers in ({}, {'Authorization': 'Bearer wrong'}):
                self.assertEqual(self.client.get('/api/nadia/health', headers=headers).status_code, 401)
            load.assert_not_called()

    def test_unconfigured_token_never_accepts_empty_bearer(self):
        with patch.dict(os.environ, {'NADIA_HEALTH_TOKEN': ''}):
            self.assertEqual(self.client.get('/api/nadia/health', headers={'Authorization': 'Bearer '}).status_code, 401)

    def test_authorized_failure_hides_private_exception(self):
        with patch.object(backend, 'health_payload', side_effect=ValueError('PRIVATE RULE CONTENT')):
            response = self.client.get('/api/nadia/health', headers={'Authorization': 'Bearer ' + 'x' * 32})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})
        self.assertIn('no-store', response.headers['cache-control'])

    def test_modified_wheel_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / backend.WHEEL).write_bytes(b'modified')
            with self.assertRaisesRegex(ValueError, 'integrity'):
                backend.verified_core(directory)
