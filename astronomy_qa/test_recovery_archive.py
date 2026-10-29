"""Private recovery must preserve bytes and reject tampering or unsafe writes."""
import importlib.util
import io
import json
import os
import zipfile
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('recovery_archive', Path(__file__).resolve().parents[1] / 'scripts/recovery_archive.py')
recovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)


def snapshot(tmp_path, files):
    root = tmp_path / 'project'
    root.mkdir()
    for name, data in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    output = root / 'tmp' / 'backup'
    manifest = recovery.create_archive(root, output, tracked_paths=list(files))
    return root, output, manifest


def rewrite_manifest(output, manifest):
    (output / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')


def test_duplicates_dirty_bytes_empty_files_and_restore(tmp_path):
    files = {'src/app.py': b'current dirty worktree bytes\r\n',
             'reference/originals/a.jpg': b'original scan bytes',
             'reference/duplicate.jpg': b'original scan bytes', 'empty': b''}
    root, output, manifest = snapshot(tmp_path, files)
    assert len(manifest['files']) == 4
    assert len(manifest['blobs']) == 2
    destination = tmp_path / 'restored'
    recovery.restore_archive(output, destination)
    assert {name: (destination / name).read_bytes() for name in files} == files
    assert (root / 'src/app.py').read_bytes() == files['src/app.py']


def test_secret_patterns_and_runtime_caches_are_excluded_without_values(tmp_path):
    token = ('ghp_' + 'x' * 36).encode()
    files = {'.env': b'API_SECRET=value', '.npmrc': b'auth', 'client.pem': b'key',
             '.vercel/project.json': b'project', 'supabase/.temp/config': b'temp',
             'evidence/private/receipt.json': b'{"token":"' + token + b'"}',
             'evidence/private/astro-cli/auth.json': b'{"token":"opaque-session-value-1234567890"}',
             'evidence/private/nested.json': b'{"state":[{"refreshToken":"opaque-session-value-1234567890"}]}',
             'src/config.py': b'API_TOKEN = get_environment_variable()\n',
             'src/service-account.json': b'credential file'}
    _, output, manifest = snapshot(tmp_path, files)
    assert [f['path'] for f in manifest['files']] == ['src/config.py']
    assert len(manifest['excluded']) == 9
    assert token not in (output / 'manifest.json').read_bytes()
    assert any(x['reason'] == 'structured_credential' for x in manifest['excluded'])


def test_archive_tamper_is_rejected_before_destination_is_created(tmp_path):
    _, output, manifest = snapshot(tmp_path, {'a': b'important'})
    archive = output / manifest['archives'][0]['filename']
    archive.write_bytes(archive.read_bytes() + b'tamper')
    destination = tmp_path / 'restored'
    with pytest.raises(ValueError, match='Archive integrity'):
        recovery.restore_archive(output, destination)
    assert not destination.exists()


@pytest.mark.parametrize('path', ['../escape', '/escape', 'C:/escape', 'x\\escape', '//server/share', 'CON', 'x/../escape', 'x.'])
def test_manifest_traversal_and_windows_aliases_rejected(tmp_path, path):
    _, output, manifest = snapshot(tmp_path, {'a': b'important'})
    manifest['files'][0]['path'] = path
    rewrite_manifest(output, manifest)
    destination = tmp_path / 'restored'
    with pytest.raises(ValueError, match='Unsafe'):
        recovery.restore_archive(output, destination)
    assert not destination.exists()


def test_restore_never_overwrites_existing_destination(tmp_path):
    _, output, _ = snapshot(tmp_path, {'a': b'important'})
    destination = tmp_path / 'restored'
    destination.mkdir()
    (destination / 'a').write_bytes(b'keep me')
    with pytest.raises(FileExistsError):
        recovery.restore_archive(output, destination)
    assert (destination / 'a').read_bytes() == b'keep me'


def test_large_files_segment_and_roll_into_bounded_archives(tmp_path):
    data = os.urandom(1800000)
    _, output, manifest = snapshot(tmp_path, {'large.bin': data})
    # Rebuild with a tiny supported chunk cap to exercise segmentation/rollover.
    root = output.parents[1]
    output2 = root / 'tmp' / 'small-chunks'
    manifest = recovery.create_archive(root, output2, tracked_paths=['large.bin'], chunk_bytes=1024 * 1024)
    assert len(manifest['archives']) >= 2
    assert all(x['bytes'] <= 1024 * 1024 for x in manifest['archives'])
    restored = tmp_path / 'restored-large'
    recovery.restore_archive(output2, restored)
    assert (restored / 'large.bin').read_bytes() == data


def test_file_hash_mismatch_and_path_prefix_collision_are_rejected(tmp_path):
    _, output, manifest = snapshot(tmp_path, {'a': b'important'})
    manifest['files'][0]['sha256'] = '0' * 64
    rewrite_manifest(output, manifest)
    with pytest.raises(ValueError, match='File integrity'):
        recovery.verify_archive(output)
    manifest['files'][0]['sha256'] = manifest['files'][0]['blobs'][0]
    manifest['files'].append(dict(manifest['files'][0], path='a/child'))
    rewrite_manifest(output, manifest)
    with pytest.raises(ValueError, match='Conflicting restore'):
        recovery.verify_archive(output)


def test_missing_tracked_files_recorded_and_output_cannot_overlap_inputs(tmp_path):
    root = tmp_path / 'project'
    root.mkdir()
    output = root / 'tmp' / 'backup'
    manifest = recovery.create_archive(root, output, tracked_paths=['deleted.py'])
    assert manifest['excluded'] == [{'path': 'deleted.py', 'reason': 'missing_worktree_file'}]
    with pytest.raises(ValueError, match='new directory below'):
        recovery.create_archive(root, tmp_path / 'outside', tracked_paths=[])


def test_nested_zip_credentials_reject_whole_container_without_scrubbing(tmp_path):
    nested = io.BytesIO()
    with zipfile.ZipFile(nested, 'w') as z:
        z.writestr('receipt.json', '{"state":{"refreshToken":"opaque-secret-value-1234567890"}}')
    outer = io.BytesIO()
    with zipfile.ZipFile(outer, 'w') as z:
        z.writestr('source.py', 'substantive source')
        z.writestr('nested.zip', nested.getvalue())
    _, output, manifest = snapshot(tmp_path, {'reference/old-release.zip': outer.getvalue(), 'source.py': b'keep'})
    assert [x['path'] for x in manifest['files']] == ['source.py']
    assert manifest['excluded'][0]['reason'] == 'container:container:structured_credential'
    assert b'opaque-secret' not in (output / 'manifest.json').read_bytes()


def test_safe_zip_preserved_and_credential_filename_zip_excluded(tmp_path):
    good, bad = io.BytesIO(), io.BytesIO()
    with zipfile.ZipFile(good, 'w') as z:
        z.writestr('source.py', 'source')
    with zipfile.ZipFile(bad, 'w') as z:
        z.writestr('credentials/auth.json', '{}')
    _, _, manifest = snapshot(tmp_path, {'reference/good.zip': good.getvalue(), 'reference/bad.zip': bad.getvalue()})
    assert [x['path'] for x in manifest['files']] == ['reference/good.zip']
    assert manifest['excluded'][0]['reason'] == 'container:credential_filename'


def test_empty_or_placeholder_templates_preserved_but_actual_values_excluded(tmp_path):
    good, bad = io.BytesIO(), io.BytesIO()
    with zipfile.ZipFile(good, 'w') as z:
        z.writestr('.env.example', '# Configuration\nAPI_SECRET=\nAPI_URL=http://localhost:8000\nPASSWORD=your_password\n')
    with zipfile.ZipFile(bad, 'w') as z:
        z.writestr('.env.example', 'API_SECRET=opaque-real-looking-value-1234567890')
    _, _, manifest = snapshot(tmp_path, {'.env.example': b'API_SECRET=\n', 'reference/good.zip': good.getvalue(), 'reference/bad.zip': bad.getvalue()})
    assert [x['path'] for x in manifest['files']] == ['.env.example', 'reference/good.zip']
    assert manifest['excluded'][0]['reason'] == 'container:unverified_configuration_template_value'


def test_jsonl_tokens_and_log_assignments_excluded_but_authorization_prose_retained(tmp_path):
    files = {'events.jsonl': b'{"nested":{"refreshToken":"opaque-secret-value-1234567890"}}\n',
             'trace.log': b'event token="opaque-secret-value-1234567890"',
             'receipt.json': b'{"publication":{"authorization":"The user explicitly authorized publication of this completed audit work."}}'}
    _, _, manifest = snapshot(tmp_path, files)
    assert [x['path'] for x in manifest['files']] == ['receipt.json']
    assert len(manifest['excluded']) == 2


@pytest.mark.parametrize('key', ['password', 'db_password', 'passwd', 'clientSecret', 'private_key'])
def test_short_structured_credentials_are_excluded(tmp_path, key):
    payload = json.dumps({'nested': {key: 'tiny'}}).encode()
    _, _, manifest = snapshot(tmp_path, {'reference/receipt.json': payload})
    assert manifest['files'] == []
    assert manifest['excluded'] == [{'path': 'reference/receipt.json', 'reason': 'structured_credential'}]
