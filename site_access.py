"""Shared-password access boundary; astronomy and chart data are unchanged."""
from __future__ import annotations

import hashlib
import hmac
import os
import time
from urllib.parse import parse_qs, urlsplit

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

COOKIE = '__Host-mr_access'
LOGIN = '/api/site-access'
SESSION_SECONDS = 86400


def session_valid(token: str, secret: str) -> bool:
    try:
        expiry, signature = token.split('.')
        remaining = int(expiry) - int(time.time())
        expected = hmac.new(secret.encode(), expiry.encode(), hashlib.sha256).hexdigest()
        return 0 < remaining <= SESSION_SECONDS and hmac.compare_digest(signature, expected)
    except (ValueError, TypeError):
        return False


def password_valid(password: str, record: str) -> bool:
    try:
        algorithm, rounds, salt, expected = record.split('$')
        if algorithm != 'pbkdf2_sha256' or not 100000 <= int(rounds) <= 1000000:
            return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), int(rounds)).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def login_page(error: bool = False):
    message = '<p class="error" role="alert">That password didn’t match. Try again.</p>' if error else ''
    return HTMLResponse('''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Mystic Rebels | Enter password</title><style>
*{box-sizing:border-box}body{margin:0;min-height:100svh;display:grid;place-items:center;padding:24px;background:radial-gradient(ellipse at 50% 10%,#301145,transparent 65%),#100c14;color:#faf4ff;font:16px/1.5 system-ui,sans-serif}
main{width:min(100%,420px);padding:36px 28px;border:1px solid #73458c66;border-radius:20px;background:#19121ed9;box-shadow:0 24px 90px #0006}
.brand{letter-spacing:.16em;font-size:13px;text-transform:uppercase;color:#dab7ec}h1{font-size:29px;line-height:1.2;margin:16px 0 12px}p{color:#c7b8cf;margin:0 0 24px}label{display:block;font-size:14px;margin:0 0 8px}input,button{width:100%;font:inherit;border-radius:9px;padding:13px 15px}input{color:#fff;background:#100c14;border:1px solid #735480;outline-offset:4px}button{margin-top:18px;border:0;background:#b47bd5;color:#160b1d;font-weight:700;cursor:pointer}button:hover{background:#c998e5}.error{color:#ffb8c9;margin:16px 0 0;font-size:14px}input:focus-visible,button:focus-visible{outline:2px solid #d8a9f3;outline-offset:4px}
</style></head><body><main><div class="brand">Mystic Rebels</div><h1>Your chart awaits.</h1>
<p>Enter the password to open Alchemystic Astrology.</p><form method="post" action="/api/site-access">
<label for="password">Password</label><input id="password" name="password" type="password" autocomplete="current-password" maxlength="256" required autofocus>
''' + message + '''<button type="submit">Open chart generator</button></form></main></body></html>''',
        status_code=401 if error else 200,
        headers={'Cache-Control': 'private, no-store', 'X-Robots-Tag': 'noindex, nofollow',
                 'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
                 'X-Content-Type-Options': 'nosniff'})


class SitePasswordGate(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        secret = os.environ.get('SITE_ACCESS_SECRET', '')
        record = os.environ.get('SITE_ACCESS_HASH', '')
        if not secret and not record and not os.environ.get('VERCEL'):
            return await call_next(request)
        if len(secret) < 32 or not record:
            return JSONResponse({'error': 'Site access is not configured.'}, status_code=503,
                                headers={'Cache-Control': 'no-store'})
        if request.url.path == LOGIN:
            if request.method in ('GET', 'HEAD'):
                return login_page()
            if request.method != 'POST':
                return JSONResponse({'error': 'Method not allowed.'}, status_code=405)
            origin = request.headers.get('origin', '')
            host = request.headers.get('x-forwarded-host', request.headers.get('host', ''))
            if urlsplit(origin).netloc != host:
                return JSONResponse({'error': 'Invalid request origin.'}, status_code=403)
            if request.headers.get('content-type', '').split(';')[0] != 'application/x-www-form-urlencoded':
                return JSONResponse({'error': 'Invalid form.'}, status_code=400)
            if int(request.headers.get('content-length', '0') or 0) > 2048:
                return JSONResponse({'error': 'Form is too large.'}, status_code=413)
            body = await request.body()
            if len(body) > 2048:
                return JSONResponse({'error': 'Form is too large.'}, status_code=413)
            password = parse_qs(body.decode('utf-8', errors='replace')).get('password', [''])[0]
            if len(password) > 256 or not password_valid(password, record):
                return login_page(error=True)
            expiry = str(int(time.time()) + SESSION_SECONDS)
            signature = hmac.new(secret.encode(), expiry.encode(), hashlib.sha256).hexdigest()
            response = RedirectResponse('/', status_code=303, headers={'Cache-Control': 'private, no-store'})
            response.set_cookie(COOKIE, expiry + '.' + signature, max_age=SESSION_SECONDS,
                                httponly=True, secure=True, samesite='lax', path='/')
            return response
        if not session_valid(request.cookies.get(COOKIE, ''), secret):
            if request.url.path.startswith('/api/'):
                return JSONResponse({'error': {'code': 'SITE_PASSWORD_REQUIRED', 'message': 'Enter the site password.'}},
                                    status_code=401, headers={'Cache-Control': 'private, no-store'})
            return RedirectResponse(LOGIN, status_code=303, headers={'Cache-Control': 'private, no-store'})
        return await call_next(request)
