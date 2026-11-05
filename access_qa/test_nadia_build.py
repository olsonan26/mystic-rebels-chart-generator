"""Credential and artifact boundaries for the protected Vercel build stage."""
import os
import unittest
import urllib.request
from unittest.mock import patch
from scripts import build_nadia as build

class PrivateBuildTests(unittest.TestCase):
    def environment(self, **changes):
        values = {'NADIA_PRIVATE_BUILD_ENABLED': 'true', 'VERCEL_PROJECT_ID': build.PROJECT,
                  'VERCEL_ENV': 'preview', 'NADIA_HEALTH_TOKEN': 'x' * 32,
                  'NADIA_CORE_READ_TOKEN': 'unit-test-only-not-a-credential'}
        values.update(changes)
        return patch.dict(os.environ, values, clear=True)

    def test_unconfigured_build_never_uses_network(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(build, 'acquire') as acquire:
            with self.assertRaisesRegex(ValueError, 'not enabled'):
                build.main()
            acquire.assert_not_called()

    def test_wrong_project_rejected(self):
        with self.environment(VERCEL_PROJECT_ID='library-project'):
            with self.assertRaisesRegex(ValueError, 'project'):
                build.require_configuration()

    def test_frontend_compiler_does_not_receive_private_credentials(self):
        with self.environment(), patch.object(build.shutil, 'which', return_value='npm'), patch.object(build.subprocess, 'run') as run:
            build.build_web()
            environment = run.call_args.kwargs['env']
            self.assertNotIn('NADIA_CORE_READ_TOKEN', environment)
            self.assertNotIn('NADIA_HEALTH_TOKEN', environment)

    def test_production_needs_separate_authorization(self):
        with self.environment(VERCEL_ENV='production'):
            with self.assertRaisesRegex(ValueError, 'Production'):
                build.require_configuration()

    def test_missing_reader_and_health_credentials_rejected(self):
        for changes in ({'NADIA_CORE_READ_TOKEN': ''}, {'NADIA_HEALTH_TOKEN': ''}):
            with self.environment(**changes), self.assertRaises(ValueError):
                build.require_configuration()

    def test_cross_origin_asset_redirect_removes_repository_credential(self):
        request = urllib.request.Request('https://api.github.com/releases/assets/1',
                                        headers={'Authorization': 'Bearer never-forward-this'})
        redirected = build.AssetRedirect().redirect_request(request, None, 302, '', {},
                      'https://release-assets.githubusercontent.com/asset?signature=temporary')
        self.assertFalse(redirected.has_header('Authorization'))

    def test_unknown_or_insecure_asset_redirect_rejected(self):
        request = urllib.request.Request('https://api.github.com/releases/assets/1')
        for target in ('http://release-assets.githubusercontent.com/asset', 'https://evil.example/asset'):
            with self.assertRaises(ValueError):
                build.AssetRedirect().redirect_request(request, None, 302, '', {}, target)

    def test_asset_bytes_rejected_on_digest_mismatch(self):
        class Response:
            def __init__(self, body): self.body = body
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return self.body[:size]
        import json
        repo = json.dumps({'private': True, 'full_name': build.REPOSITORY}).encode()
        release = json.dumps({'draft': False, 'target_commitish': build.COMMIT,
                              'assets': [{'name': build.WHEEL, 'size': build.SIZE, 'id': 1}]}).encode()
        with patch.object(build.urllib.request, 'build_opener') as opener:
            opener.return_value.open.side_effect = [Response(repo), Response(release), Response(b'tampered')]
            with self.assertRaisesRegex(ValueError, 'digest'):
                build.acquire('unit-test-only')
