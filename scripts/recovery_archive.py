"""Create, verify and safely restore a private, content-addressed recovery archive.

Only standard-library modules are required. Credentials and runtime caches are
excluded; originals belong in a private release, never the public source repo.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MAX_ARCHIVE = 512 * 1024 * 1024
SEGMENT = 64 * 1024 * 1024
DEFAULT_INPUTS = ('reference', 'evidence/private', 'CODEX_START_HERE.md',
                  'README_FIRST.md', 'docs/PRECISION_REQUIREMENTS.md')
CACHES = {'.git', '.venv', '.runtime', 'node_modules', '__pycache__',
          '.pytest_cache', '.vercel', '.aws', '.ssh', '.cache', '.temp'}
STORED = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.gz', '.zip', '.pdf',
          '.7z', '.mp4', '.woff', '.woff2'}
TEXT = {'.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.json', '.jsonl',
        '.md', '.txt', '.csv', '.tsv', '.log', '.xml', '.yaml', '.yml',
        '.toml', '.ini', '.cfg', '.ps1', '.sh', '.html', '.css', '.sql'}
SECRET_PATTERNS = (
    ('private_key', re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('github_token', re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b')),
    ('openai_token', re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{30,}\b')),
    ('aws_access_key', re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('bearer_token', re.compile(rb'(?i)authorization["\s:]+bearer\s+[A-Za-z0-9_.-]{30,}')),
    ('supabase_secret', re.compile(rb'\bsb_secret_[A-Za-z0-9_-]{20,}\b')),
    ('slack_token', re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b')),
    ('opaque_credential_assignment', re.compile(rb'''(?i)["']?(?:access_?token|refresh_?token|api_?key|client_?secret|private_?key|token)["']?\s*[:=]\s*["'][A-Za-z0-9_./+=-]{24,}["']''')),
)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def relative(value):
    """Manifest paths have one portable interpretation, including on Windows."""
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Unsafe relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or p.as_posix() != value or any(x in ('.', '..') for x in p.parts):
        raise ValueError('Unsafe relative path')
    if any(x.endswith(('.', ' ')) or any(ord(c) < 32 for c in x)
           or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?', x) for x in p.parts):
        raise ValueError('Unsafe Windows path')
    return p


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True).stdout.decode('utf-8', errors='replace')


def exclusion(path):
    parts = path.parts
    name = path.name.lower()
    if any(p.lower() in CACHES for p in parts):
        return 'cache_or_repository_metadata'
    if ((name.startswith('.env') and name != '.env.example') or name in {'.npmrc', '.pypirc', '.netrc', 'auth.json', 'passwords.json', 'cookies.json', 'storage-state.json'} or name.startswith(('id_rsa', 'id_ed25519'))
            or path.suffix.lower() in {'.pem', '.p12', '.pfx', '.key'}
            or re.search(r'(^|[._-])(credentials?|tokens?|service[-_]account)([._-]|$)', name)):
        return 'credential_filename'
    return None


def json_secret(value):
    """Find opaque credentials by structured field, without printing the value."""
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = re.sub(r'([a-z])([A-Z])', r'\1_\2', key).lower().replace('-', '_')
            # Passwords and private key material can be short or contain spaces.
            # Length/opaque-token heuristics are only appropriate to other keys.
            if (re.fullmatch(r'(?:[a-z][a-z0-9]*_)*(password|passwd|password_?hash|private_?key|client_?secret)', normalized)
                    and isinstance(item, str) and item.strip()):
                return 'structured_credential'
            token_like = (isinstance(item, str) and len(item.strip()) >= 16
                          and (not any(c.isspace() for c in item.strip())
                               or normalized in {'password', 'private_key'} or item.lower().startswith('bearer ')))
            if (re.fullmatch(r'(?:[a-z][a-z0-9]*_)*(access_?token|refresh_?token|api_?key|access_?key|secret_?access_?key|service_?role_?key|secret_?key|private_?key|client_?secret|password_?hash|password|token|secret|authorization)', normalized)
                    and token_like):
                return 'structured_credential'
            found = json_secret(item)
            if found:
                return found
    elif isinstance(value, list):
        return next((found for item in value if (found := json_secret(item))), None)
    return None


def content_exclusion(stream, name, depth=0):
    """Inspect compressed containers, rejecting the container on any secret."""
    suffix = PurePosixPath(name).suffix.lower()
    signature = stream.read(4)
    stream.seek(0)
    if signature in {b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'}:
        suffix = '.zip'
    elif signature.startswith(b'\x1f\x8b'):
        suffix = '.gz'
    if depth > 4:
        return 'container_nesting_limit'
    if PurePosixPath(name).name.lower() == '.env.example':
        data = stream.read(1024 * 1024 + 1)
        if len(data) > 1024 * 1024 or any(pattern.search(data) for _, pattern in SECRET_PATTERNS):
            return 'unsafe_configuration_template'
        try:
            for line in data.decode('utf-8-sig').splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, separator, value = line.removeprefix('export ').partition('=')
                value = value.split(' #', 1)[0].strip().strip('\"\'')
                placeholder = re.fullmatch(r'(?i)(your[_-].*|replace[_-]?me|change[_-]?me|placeholder|<[^>]+>)', value)
                local_url = re.fullmatch(r'https?://(?:localhost|127\.0\.0\.1)(?::[0-9]+)?/?', value)
                if not separator or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*', key.strip()) or (value and not placeholder and not local_url):
                    return 'unverified_configuration_template_value'
        except UnicodeError:
            return 'invalid_configuration_template'
    elif suffix == '.zip':
        try:
            with zipfile.ZipFile(stream) as container:
                for member in container.infolist():
                    if member.is_dir():
                        continue
                    try:
                        nested = relative(member.filename)
                    except ValueError:
                        return 'unsafe_container_member'
                    reason = exclusion(nested)
                    if reason:
                        return 'container:' + reason
                    if member.flag_bits & 1:
                        return 'encrypted_container_not_inspectable'
                    with container.open(member) as child:
                        reason = content_exclusion(child, nested.as_posix(), depth + 1)
                    if reason:
                        return 'container:' + reason
        except (zipfile.BadZipFile, NotImplementedError):
            return 'invalid_or_unsupported_container'
    elif suffix == '.gz':
        try:
            with gzip.GzipFile(fileobj=stream) as child:
                return content_exclusion(child, name[:-3], depth + 1)
        except (OSError, EOFError):
            return 'invalid_compressed_container'
    elif suffix in {'.7z', '.rar', '.tar', '.tgz'}:
        return 'container_format_not_inspectable'
    elif suffix in TEXT:
        if suffix == '.json':
            try:
                reason = json_secret(json.load(stream))
                if reason:
                    return reason
            except (ValueError, UnicodeError):
                pass
            stream.seek(0)
        elif suffix == '.jsonl':
            for line in stream:
                try:
                    reason = json_secret(json.loads(line))
                except (ValueError, UnicodeError):
                    continue
                if reason:
                    return reason
            stream.seek(0)
        tail = b''
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            match = next((label for label, pattern in SECRET_PATTERNS if pattern.search(tail + data)), None)
            if match:
                return 'secret_pattern:' + match
            tail = data[-512:]
    return None


def inventory(root, extra_paths=(), tracked_paths=None):
    tracked = tracked_paths if tracked_paths is not None else git(root, 'ls-files', '-z').split('\0')
    candidates = {str(x) for x in tracked if x}
    for item in (*DEFAULT_INPUTS, *extra_paths):
        p = root / Path(item)
        if not p.resolve().is_relative_to(root.resolve()):
            raise ValueError('Input must remain inside the project')
        if p.is_symlink():
            candidates.add(p.relative_to(root).as_posix())
        elif p.is_dir():
            candidates.update(x.relative_to(root).as_posix() for x in p.rglob('*') if x.is_file() or x.is_symlink())
        elif p.is_file():
            candidates.add(p.relative_to(root).as_posix())
    return sorted(candidates)


def create_archive(root, output, extra_paths=(), tracked_paths=None, chunk_bytes=MAX_ARCHIVE):
    root, output = Path(root).resolve(), Path(output).resolve()
    if not output.is_relative_to(root / 'tmp') or output == root / 'tmp':
        raise ValueError('Archive output must be a new directory below project tmp/')
    if not 1024 * 1024 <= chunk_bytes <= MAX_ARCHIVE:
        raise ValueError('Chunk size must be between 1 MiB and 512 MiB')
    candidates = inventory(root, extra_paths, tracked_paths)
    if any((root / p).resolve().is_relative_to(output) for p in candidates):
        raise ValueError('Archive output cannot also be an input')
    output.mkdir(parents=True, exist_ok=False)
    manifest = {'schema_version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
                'files': [], 'blobs': {}, 'archives': [], 'excluded': []}
    if tracked_paths is None:
        manifest['git'] = {'head': git(root, 'rev-parse', 'HEAD').strip(),
                           'branch': git(root, 'branch', '--show-current').strip(),
                           'status': git(root, 'status', '--porcelain=v1')}
    archive = None
    archive_name = None

    def close_chunk():
        if archive is not None:
            archive.close()
            p = output / archive_name
            if p.stat().st_size > chunk_bytes:
                raise ValueError('Archive exceeded configured chunk size')
            manifest['archives'].append({'filename': archive_name, 'bytes': p.stat().st_size,
                                         'sha256': digest(p)})

    try:
        for name in candidates:
            rel = relative(name)
            path = root / str(rel)
            reason = exclusion(rel)
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                reason = 'symlink_or_outside_project'
            elif not path.is_file():
                reason = 'missing_worktree_file'
            before = path.stat() if not reason else None
            if not reason:
                with path.open('rb') as stream:
                    reason = content_exclusion(stream, name)
            if reason:
                manifest['excluded'].append({'path': name, 'reason': reason})
                continue
            file_hash, pieces, size = hashlib.sha256(), [], 0
            with path.open('rb') as stream:
                while data := stream.read(min(SEGMENT, chunk_bytes // 2)):
                    file_hash.update(data)
                    size += len(data)
                    sha = hashlib.sha256(data).hexdigest()
                    pieces.append(sha)
                    if sha in manifest['blobs']:
                        continue
                    # Deflate can expand incompressible data slightly. Also reserve
                    # central-directory space for every member already written.
                    reserve = 65536 + (len(archive.filelist) + 1) * 256 if archive else 65536
                    if archive and archive.fp.tell() + len(data) * 1.002 + reserve > chunk_bytes:
                        close_chunk()
                        archive = None
                    if archive is None:
                        archive_name = f'assets-{len(manifest["archives"]) + 1:04d}.zip'
                        archive = zipfile.ZipFile(output / archive_name, 'x', allowZip64=True, compresslevel=1)
                    member = 'blobs/' + sha
                    method = zipfile.ZIP_STORED if path.suffix.lower() in STORED else zipfile.ZIP_DEFLATED
                    archive.writestr(member, data, compress_type=method, compresslevel=1)
                    manifest['blobs'][sha] = {'bytes': len(data), 'archive': archive_name, 'member': member}
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or size != before.st_size:
                raise ValueError('Input changed during snapshot: ' + name)
            manifest['files'].append({'path': name, 'bytes': size, 'sha256': file_hash.hexdigest(), 'blobs': pieces})
        close_chunk()
        archive = None
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        verify_archive(output)
        return manifest
    finally:
        if archive is not None:
            archive.close()


def verify_archive(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1:
        raise ValueError('Unsupported recovery manifest')
    archive_names = set()
    for item in manifest['archives']:
        name = item['filename']
        if relative(name).name != name or name in archive_names:
            raise ValueError('Invalid or duplicate archive filename')
        archive_names.add(name)
        p = directory / name
        if p.is_symlink() or p.stat().st_size != item['bytes'] or digest(p) != item['sha256']:
            raise ValueError('Archive integrity failure: ' + name)
        if item['bytes'] > MAX_ARCHIVE:
            raise ValueError('Archive exceeds 512 MiB')
        expected = {v['member']: (sha, v) for sha, v in manifest['blobs'].items() if v['archive'] == name}
        with zipfile.ZipFile(p) as z:
            if len(z.namelist()) != len(expected) or set(z.namelist()) != set(expected):
                raise ValueError('Unexpected or duplicate ZIP members')
            for member, (sha, blob) in expected.items():
                if not re.fullmatch('[0-9a-f]{64}', sha) or member != 'blobs/' + sha:
                    raise ValueError('Invalid content address')
                h, size = hashlib.sha256(), 0
                with z.open(member) as stream:
                    for data in iter(lambda: stream.read(1024 * 1024), b''):
                        h.update(data)
                        size += len(data)
                if size != blob['bytes'] or h.hexdigest() != sha:
                    raise ValueError('Blob integrity failure')
    paths = [relative(item['path']).as_posix().casefold() for item in manifest['files']]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate restore paths')
    paths = set(paths)
    referenced = set()
    for item in manifest['files']:
        p = relative(item['path'])
        if any(a.as_posix().casefold() in paths for a in p.parents if a.as_posix() != '.'):
            raise ValueError('Conflicting restore paths')
        if len(item['blobs']) == 1:
            sha = item['blobs'][0]
            referenced.add(sha)
            blob = manifest['blobs'][sha]
            if blob['archive'] not in archive_names or item['sha256'] != sha or item['bytes'] != blob['bytes']:
                raise ValueError('File integrity failure: ' + item['path'])
            continue
        h, size = hashlib.sha256(), 0
        for sha in item['blobs']:
            referenced.add(sha)
            blob = manifest['blobs'][sha]
            if blob['archive'] not in archive_names:
                raise ValueError('Missing blob archive')
            with zipfile.ZipFile(directory / blob['archive']) as z, z.open(blob['member']) as stream:
                for data in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(data)
                    size += len(data)
        if size != item['bytes'] or h.hexdigest() != item['sha256']:
            raise ValueError('File integrity failure: ' + item['path'])
    if referenced != set(manifest['blobs']):
        raise ValueError('Unreferenced or unknown blob')
    return manifest


def restore_archive(directory, destination):
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Restore destination must not exist')
    manifest = verify_archive(directory)
    destination.mkdir()
    for item in manifest['files']:
        target = destination / str(relative(item['path']))
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            for sha in item['blobs']:
                blob = manifest['blobs'][sha]
                with zipfile.ZipFile(Path(directory) / blob['archive']) as z, z.open(blob['member']) as stream:
                    for data in iter(lambda: stream.read(1024 * 1024), b''):
                        output.write(data)
        if digest(target) != item['sha256']:
            raise ValueError('Restored file failed integrity check')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('create')
    create.add_argument('--output', type=Path, required=True)
    create.add_argument('--input', action='append', default=[], help='Additional project-relative input directory/file')
    for action in ('verify', 'restore'):
        sub = commands.add_parser(action)
        sub.add_argument('--archive', type=Path, required=True)
        if action == 'restore':
            sub.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'create':
        result = create_archive(ROOT, args.output, args.input)
    elif args.command == 'verify':
        result = verify_archive(args.archive)
    else:
        result = restore_archive(args.archive, args.destination)
    print(json.dumps({'status': 'VERIFIED', 'files': len(result['files']),
                      'unique_blobs': len(result['blobs']), 'archives': len(result['archives']),
                      'excluded': result['excluded']}, indent=2))


if __name__ == '__main__':
    main()
