import hashlib
import hmac
import time

import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from site_access import COOKIE, LOGIN, SitePasswordGate, session_valid

SECRET = 'test-session-secret-' * 3
PASSWORD = 'test-only-password'
SALT = bytes.fromhex('1234567890abcdef1234567890abcdef')
RECORD = 'pbkdf2_sha256$240000$' + SALT.hex() + '$' + hashlib.pbkdf2_hmac('sha256', PASSWORD.encode(), SALT, 240000).hex()


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv('SITE_ACCESS_SECRET', SECRET)
    monkeypatch.setenv('SITE_ACCESS_HASH', RECORD)
    app = Starlette(routes=[Route('/{path:path}', lambda request: JSONResponse({'protected': True}), methods=['GET', 'POST'])])
    return TestClient(SitePasswordGate(app), base_url='https://testserver', follow_redirects=False)


def login(client, password=PASSWORD, origin='https://testserver'):
    return client.post(LOGIN, data={'password': password}, headers={'Origin': origin})


def test_no_password_blocks_page_and_direct_api(client):
    assert client.get('/').status_code == 303
    assert client.get('/api/charts').status_code == 401
    assert client.get('/api/index.py').status_code == 401
    assert client.get('/api/methodology').status_code == 401
    assert client.get('/assets/app.js').status_code == 303


def test_form_contains_no_password_or_secret(client):
    page = client.get(LOGIN)
    assert page.status_code == 200
    assert 'type="password"' in page.text
    assert PASSWORD not in page.text and SECRET not in page.text and RECORD not in page.text
    assert 'no-store' in page.headers['cache-control']


def test_wrong_password_stays_locked(client):
    assert login(client, 'wrong-password').status_code == 401
    assert client.get('/api/charts').status_code == 401


def test_correct_password_unlocks_with_secure_cookie(client):
    response = login(client)
    assert response.status_code == 303
    cookie = response.headers['set-cookie']
    for attribute in ('HttpOnly', 'Secure', 'SameSite=lax', 'Path=/', 'Max-Age=86400'):
        assert attribute in cookie
    assert client.get('/').json() == {'protected': True}
    assert client.post('/api/charts', json={}).status_code == 200


def test_forged_and_expired_cookies_are_rejected(client):
    for token in ('1.' + '0' * 64, str(int(time.time()) + 3600) + '.' + '0' * 64):
        client.cookies.set(COOKIE, token)
        assert client.get('/api/charts').status_code == 401
    expiry = str(int(time.time()) - 1)
    signature = hmac.new(SECRET.encode(), expiry.encode(), hashlib.sha256).hexdigest()
    assert not session_valid(expiry + '.' + signature, SECRET)


def test_cross_site_and_oversized_forms_are_rejected(client):
    assert login(client, origin='https://other.example').status_code == 403
    assert login(client, password='x' * 3000).status_code == 413


def test_missing_production_configuration_fails_closed(client, monkeypatch):
    monkeypatch.delenv('SITE_ACCESS_HASH')
    assert client.get('/api/charts').status_code == 503


def test_password_rotation_invalidates_existing_session(client, monkeypatch):
    login(client)
    monkeypatch.setenv('SITE_ACCESS_SECRET', SECRET + '-rotated')
    assert client.get('/api/charts').status_code == 401
