"""Resumable private originals/OCR with public, ID-keyed stage provenance.

Candidate OCR is never a visual review or an approved source assertion.
Download receipts containing bearer URLs must remain under reference/.
"""
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import time
import urllib.request
from pathlib import Path

from .registry import ROOT

STATE = ROOT / 'data/knowledge/source_pipeline.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    # OneDrive/indexers can briefly hold the destination on Windows. Keep the
    # completed temporary checkpoint and retry only this transient lock.
    for attempt in range(6):
        try:
            os.replace(temporary, path)
            break
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(0.05 * 2 ** attempt)


def load_state(path=STATE):
    path = Path(path)
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(
        schema_version='1.0', scope='ID_KEYED_ORIGINAL_SOURCE_STAGES_NOT_REVIEW_APPROVAL', files={})


def manifest_rows(manifest):
    return [r for b in manifest['batches'] for r in b['files']] + manifest['loose_root_files']


def safe_id(file_id):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', file_id):
        raise ValueError('Invalid provider file ID')
    return file_id


def private_path(relative, root=ROOT):
    target = (root / relative).resolve()
    if not target.is_relative_to((root / 'reference').resolve()):
        raise ValueError('Originals and OCR must remain under private reference/')
    return target


def initialize(manifest, state, root=ROOT):
    for source in manifest_rows(manifest):
        identity = safe_id(source['file_id'])
        row = state['files'].setdefault(identity, dict(file_id=identity, name=source['name'],
            acquisition_status='METADATA_ONLY', ocr_status='NOT_RUN', attempts=0))
        if row['name'] != source['name']:
            raise ValueError('Provider identity/name drift requires explicit reconciliation')
        if source['acquisition_status'] == 'ACQUIRED_HASHED' and row['acquisition_status'] != 'ACQUIRED_HASHED':
            path = private_path(source['local_path'], root)
            if path.exists():
                if sha(path) != source['content_sha256']:
                    raise ValueError('Legacy original bytes changed')
                row.update(acquisition_status='ACQUIRED_HASHED', local_path=source['local_path'],
                    content_sha256=source['content_sha256'], size_bytes=path.stat().st_size,
                    identity_basis='EXISTING_VERIFIED_MANIFEST_FILE_ID')
    return state


def download(url, target):
    with urllib.request.urlopen(url, timeout=45) as response, target.open('wb') as output:
        while block := response.read(1024 * 256):
            output.write(block)


def validate_image(path, expected_size=None):
    if expected_size is not None and path.stat().st_size != int(expected_size):
        raise ValueError('DOWNLOAD_SIZE_MISMATCH')
    with path.open('rb') as source:
        magic = source.read(8)
    if not (magic.startswith(b'\xff\xd8\xff') or magic == b'\x89PNG\r\n\x1a\n'):
        raise ValueError('DOWNLOAD_NOT_IMAGE_BYTES')


def acquire(row, receipt, checkpoint, root=ROOT, fetch=download, retries=3, backoff=time.sleep):
    """Checkpoint each attempt; never overwrite a previously hashed original."""
    identity = safe_id(row['file_id'])
    if receipt['id'] != identity:
        raise ValueError('Receipt provider identity mismatch')
    if row['acquisition_status'] == 'ACQUIRED_HASHED':
        if sha(private_path(row['local_path'], root)) != row['content_sha256']:
            raise ValueError('Previously acquired original bytes changed')
        return
    target = private_path('reference/originals/' + identity + '.jpg', root)
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = receipt.get('file_size_bytes')
    if target.exists():
        validate_image(target, expected)
        row.update(acquisition_status='ACQUIRED_HASHED', local_path=target.relative_to(root).as_posix(),
            content_sha256=sha(target), size_bytes=target.stat().st_size, identity_basis='CONNECTOR_RECEIPT_FILE_ID')
        checkpoint()
        return
    partial = target.with_suffix('.jpg.part')
    for attempt in range(retries):
        row.update(acquisition_status='ACQUISITION_IN_PROGRESS', attempts=row.get('attempts', 0) + 1)
        checkpoint()
        try:
            fetch(receipt['file_uri']['download_url'], partial)
            validate_image(partial, expected)
            os.replace(partial, target)
            row.update(acquisition_status='ACQUIRED_HASHED', local_path=target.relative_to(root).as_posix(),
                content_sha256=sha(target), size_bytes=target.stat().st_size,
                identity_basis='CONNECTOR_RECEIPT_FILE_ID', last_error=None)
            checkpoint()
            return
        except KeyboardInterrupt:
            row.update(acquisition_status='INTERRUPTED', last_error='KeyboardInterrupt')
            checkpoint()
            raise
        except Exception as error:
            # Exception strings can contain signed URLs: publish class only.
            row.update(acquisition_status='ACQUISITION_FAILED', last_error=type(error).__name__)
            checkpoint()
            if attempt + 1 < retries:
                backoff(min(2 ** attempt, 8))


def ocr(row, checkpoint, root=ROOT, runner=subprocess.run):
    if row['acquisition_status'] != 'ACQUIRED_HASHED':
        return
    path = private_path(row['local_path'], root)
    if sha(path) != row['content_sha256']:
        raise ValueError('Original changed before OCR')
    output = private_path('reference/ocr/' + safe_id(row['file_id']) + '.json', root)
    if row['ocr_status'] == 'OCR_EXTRACTED_CANDIDATE':
        if sha(output) != row['ocr_output_sha256']:
            raise ValueError('OCR output changed')
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    row['ocr_status'] = 'OCR_IN_PROGRESS'
    checkpoint()
    try:
        runner(['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe', '-NoProfile',
            '-File', str(root / 'scripts/windows_source_ocr.ps1'), '-ImagePath', str(path),
            '-OutputPath', str(output)], check=True, capture_output=True, timeout=90)
        data = json.loads(output.read_text(encoding='utf-8-sig'))
        if not data.get('text', '').strip():
            raise ValueError('EMPTY_OCR')
        row.update(ocr_status='OCR_EXTRACTED_CANDIDATE', ocr_path=output.relative_to(root).as_posix(),
            ocr_output_sha256=sha(output), ocr_text_sha256=hashlib.sha256(data['text'].encode()).hexdigest(),
            ocr_engine=data['engine'], ocr_language=data['language'],
            ocr_source_sha256=row['content_sha256'], ocr_error=None)
    except (Exception, KeyboardInterrupt) as error:
        row.update(ocr_status='OCR_FAILED', ocr_error=type(error).__name__)
        checkpoint()
        if isinstance(error, KeyboardInterrupt):
            raise
        return
    checkpoint()


def index_ocr(state, database, root=ROOT):
    """Separate private candidate index; never alter compiled PDF witnesses."""
    database = private_path(str(database), root)
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as db:
        db.executescript('CREATE TABLE IF NOT EXISTS originals(file_id TEXT PRIMARY KEY, '
            'image_sha256 TEXT,ocr_sha256 TEXT,text TEXT,status TEXT);'
            'CREATE VIRTUAL TABLE IF NOT EXISTS candidates USING fts5(file_id UNINDEXED,text);')
        for row in state['files'].values():
            if row['ocr_status'] != 'OCR_EXTRACTED_CANDIDATE':
                continue
            path = private_path(row['ocr_path'], root)
            if sha(path) != row['ocr_output_sha256']:
                raise ValueError('OCR provenance changed before indexing')
            text = json.loads(path.read_text(encoding='utf-8-sig'))['text']
            db.execute('INSERT OR REPLACE INTO originals VALUES(?,?,?,?,?)',
                (row['file_id'], row['content_sha256'], row['ocr_output_sha256'], text, 'OCR_CANDIDATE_NOT_REVIEWED'))
            db.execute('DELETE FROM candidates WHERE file_id=?', (row['file_id'],))
            db.execute('INSERT INTO candidates VALUES(?,?)', (row['file_id'], text))
    return database


def search_ocr(state, query, database='reference/original-candidates.sqlite', root=ROOT):
    """Bounded candidate lookup checks the public provenance and private text."""
    tokens=re.findall(r'\w+',query)
    if not tokens:
        return []
    match=' AND '.join('"'+token+'"' for token in tokens)
    uri=private_path(str(database),root).as_uri()+'?mode=ro'
    with sqlite3.connect(uri,uri=True) as db:
        found=db.execute('SELECT o.file_id,o.image_sha256,o.ocr_sha256,o.text,c.text FROM candidates c '
            'JOIN originals o ON o.file_id=c.file_id WHERE candidates MATCH ? LIMIT 20',(match,)).fetchall()
    results=[]
    for identity,image_hash,ocr_hash,text,indexed_text in found:
        row=state['files'][identity]
        output=private_path(row['ocr_path'],root)
        if (row['ocr_status']!='OCR_EXTRACTED_CANDIDATE' or row['content_sha256']!=image_hash
                or row['ocr_output_sha256']!=ocr_hash or sha(output)!=ocr_hash
                or sha(private_path(row['local_path'],root))!=image_hash or text!=indexed_text
                or json.loads(output.read_text(encoding='utf-8-sig'))['text']!=text):
            raise ValueError('Candidate OCR retrieval integrity failed')
        results.append(dict(file_id=identity,name=row['name'],image_sha256=image_hash,ocr_sha256=ocr_hash,
            status='OCR_CANDIDATE_NOT_VERIFIED_TRANSCRIPTION',snippet=text[:240]))
    return results
