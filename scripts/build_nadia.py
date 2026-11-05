"""Fail-closed Vercel build acquisition; credentials stay in process memory."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nadia_runtime import VERSION, COMMIT, SHA256, WHEEL
from scripts.install_nadia import install

PROJECT = 'prj_MBgBhgCUjxUwJ8OZO9OrqDqK4Vwl'
REPOSITORY = 'olsonan26/NADIA-KNOWLEDGE-CORE'
API = 'https://api.github.com/repos/' + REPOSITORY
SIZE = 1477941

class AssetRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlsplit(newurl)
        if target.scheme != 'https' or target.hostname not in {
            'api.github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'
        } or target.username or target.password:
            raise ValueError('Untrusted private asset redirect')
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        # A release asset URL carries its own short-lived access signature.
        # Repository credentials must never reach a different origin.
        if (target.scheme, target.netloc) != (urllib.parse.urlsplit(req.full_url).scheme,
                                             urllib.parse.urlsplit(req.full_url).netloc):
            redirected.remove_header('Authorization')
        return redirected

def require_configuration():
    if os.environ.get('NADIA_PRIVATE_BUILD_ENABLED') != 'true':
        raise ValueError('Protected private build is not enabled')
    if os.environ.get('VERCEL_PROJECT_ID') != PROJECT:
        raise ValueError('Unapproved consumer project')
    environment = os.environ.get('VERCEL_ENV')
    if environment not in {'preview', 'production'}:
        raise ValueError('Explicit deployment environment required')
    if environment == 'production' and os.environ.get('NADIA_PRODUCTION_ENABLED') != 'true':
        raise ValueError('Production authorization is not configured')
    if len(os.environ.get('NADIA_HEALTH_TOKEN', '')) < 32:
        raise ValueError('Dedicated health credential is missing')
    token = os.environ.get('NADIA_CORE_READ_TOKEN', '')
    if not token:
        raise ValueError('Scoped private release reader is missing')
    return token

def acquire(token):
    opener = urllib.request.build_opener(AssetRedirect())
    def fetch(url, accept, limit):
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token,
              'Accept': accept, 'User-Agent': 'NADIA-private-build', 'X-GitHub-Api-Version': '2022-11-28'})
        with opener.open(req, timeout=60) as response:
            body = response.read(limit + 1)
        if len(body) > limit:
            raise ValueError('Oversized private release response')
        return body
    repo = json.loads(fetch(API, 'application/vnd.github+json', 200000))
    if repo.get('private') is not True or repo.get('full_name') != REPOSITORY:
        raise ValueError('Private release repository mismatch')
    release = json.loads(fetch(API + '/releases/tags/v' + VERSION, 'application/vnd.github+json', 200000))
    if release.get('draft') is not False or release.get('target_commitish') != COMMIT:
        raise ValueError('Private release identity mismatch')
    assets = [a for a in release.get('assets', []) if a.get('name') == WHEEL]
    if len(assets) != 1 or assets[0].get('size') != SIZE or type(assets[0].get('id')) is not int:
        raise ValueError('Private release asset mismatch')
    body = fetch(API + '/releases/assets/' + str(assets[0]['id']), 'application/octet-stream', SIZE)
    if len(body) != SIZE or hashlib.sha256(body).hexdigest() != SHA256:
        raise ValueError('Private wheel digest mismatch')
    return body

def main():
    token = require_configuration()
    body = acquire(token)
    with tempfile.TemporaryDirectory(prefix='nadia-build-') as temporary:
        wheel = Path(temporary) / WHEEL
        wheel.write_bytes(body)
        install(wheel)
    print('Pinned private runtime installed; browser build may proceed')

def build_web():
    # The browser compiler needs no private repository or health credential.
    secret_names = {'NADIA_CORE_READ_TOKEN', 'NADIA_HEALTH_TOKEN'}
    web_env = {key: value for key, value in os.environ.items() if key not in secret_names}
    npm = shutil.which('npm')
    if not npm:
        raise ValueError('Frontend build runtime unavailable')
    subprocess.run([npm, 'run', 'build'], cwd=ROOT, env=web_env, check=True)
    secrets = [os.environ[name].encode() for name in secret_names if os.environ.get(name)]
    for path in (ROOT / 'dist').rglob('*'):
        if path.is_file() and any(secret in path.read_bytes() for secret in secrets):
            raise ValueError('Credential found in browser artifact')

if __name__ == '__main__':
    try:
        main()
        build_web()
    except Exception as exc:
        # Do not log HTTP bodies, signed download URLs, tokens or private paths.
        raise SystemExit('Private NADIA build stopped (' + type(exc).__name__ + '); check protected configuration and release identity.') from None
