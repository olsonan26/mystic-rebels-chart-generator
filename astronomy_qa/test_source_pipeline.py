"""Source-processing failures must never erase completed work or imply review."""
import json
import subprocess
from pathlib import Path

import pytest

from knowledge_audit.source_pipeline import acquire, ocr, sha, save_json, load_state, private_path, index_ocr, search_ocr


def pending(identity):
    return dict(file_id=identity, name='IMG_5079.jpg', acquisition_status='METADATA_ONLY', ocr_status='NOT_RUN', attempts=0)


def receipt(identity, data):
    return dict(id=identity, file_size_bytes=len(data), file_uri={'download_url':'https://private.invalid/signed'})


def transfer(data):
    def fetch(url, path):
        path.write_bytes(data)
    return fetch


def test_duplicate_filenames_are_independent_ids_and_exact_hashes(tmp_path):
    a,b = pending('id-a'),pending('id-b')
    left,right = b'\xff\xd8\xffleft',b'\xff\xd8\xffright'
    acquire(a,receipt('id-a',left),lambda:None,tmp_path,transfer(left))
    acquire(b,receipt('id-b',right),lambda:None,tmp_path,transfer(right))
    assert a['local_path'] != b['local_path']
    assert a['content_sha256'] != b['content_sha256']
    assert (tmp_path/a['local_path']).read_bytes() == left
    assert (tmp_path/b['local_path']).read_bytes() == right


def test_interruption_checkpoints_and_resumes_without_restarting_completed_file(tmp_path):
    state = {'files':{'a':pending('a'),'b':pending('b')}}
    state_path = tmp_path/'state.json'
    checkpoint = lambda:save_json(state_path,state)
    data = b'\xff\xd8\xffcomplete'
    acquire(state['files']['a'],receipt('a',data),checkpoint,tmp_path,transfer(data))
    def interrupted(url,path):
        path.write_bytes(b'\xff\xd8\xffpartial')
        raise KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        acquire(state['files']['b'],receipt('b',data),checkpoint,tmp_path,interrupted)
    saved = load_state(state_path)
    assert saved['files']['a']['acquisition_status'] == 'ACQUIRED_HASHED'
    assert saved['files']['b']['acquisition_status'] == 'INTERRUPTED'
    def never_fetch(url,path):
        pytest.fail('A completed original was fetched again')
    acquire(saved['files']['a'],receipt('a',data),checkpoint,tmp_path,never_fetch)
    acquire(saved['files']['b'],receipt('b',data),lambda:None,tmp_path,transfer(data))
    assert (tmp_path/saved['files']['b']['local_path']).read_bytes() == data


def test_bounded_retry_rejects_partial_html_and_does_not_publish_signed_exception(tmp_path):
    row=pending('id')
    calls=[]
    def fail(url,path):
        calls.append(url)
        path.write_text('<html>denied</html>')
        raise OSError(url)
    acquire(row,receipt('id',b'123'),lambda:None,tmp_path,fail,backoff=lambda n:None)
    assert len(calls)==3 and row['acquisition_status']=='ACQUISITION_FAILED'
    assert row['last_error']=='OSError'
    assert 'private.invalid' not in json.dumps(row)
    assert not (tmp_path/'reference/originals/id.jpg').exists()


def test_failed_ocr_keeps_acquisition_and_can_retry(tmp_path):
    row=pending('id'); data=b'\xff\xd8\xffcomplete'
    acquire(row,receipt('id',data),lambda:None,tmp_path,transfer(data))
    digest=row['content_sha256']
    def fail(*args,**kwargs):
        raise subprocess.TimeoutExpired('ocr',90)
    ocr(row,lambda:None,tmp_path,fail)
    assert row['ocr_status']=='OCR_FAILED' and row['content_sha256']==digest
    def success(command,**kwargs):
        Path(command[-1]).write_text(json.dumps({'text':'candidate 19:18','engine':'test','language':'en-US'}))
    ocr(row,lambda:None,tmp_path,success)
    assert row['ocr_status']=='OCR_EXTRACTED_CANDIDATE'
    assert row['ocr_source_sha256']==digest
    assert 'visual_review_status' not in row and 'semantic_review_status' not in row


def test_recovered_final_file_and_changed_completed_bytes(tmp_path):
    path=tmp_path/'reference/originals/id.jpg';path.parent.mkdir(parents=True)
    data=b'\xff\xd8\xffcomplete';path.write_bytes(data)
    row=pending('id')
    acquire(row,receipt('id',data),lambda:None,tmp_path,lambda *args:pytest.fail('recovery redownload'))
    assert row['content_sha256']==sha(path)
    path.write_bytes(b'changed')
    with pytest.raises(ValueError,match='bytes changed'):
        acquire(row,receipt('id',data),lambda:None,tmp_path)


def test_receipt_mismatch_and_reference_escape_are_rejected(tmp_path):
    with pytest.raises(ValueError,match='identity mismatch'):
        acquire(pending('a'),receipt('b',b'123'),lambda:None,tmp_path)
    with pytest.raises(ValueError,match='private reference'):
        private_path('../public.jpg',tmp_path)


def test_candidate_search_rejects_poisoned_index_and_changed_ocr(tmp_path):
    import sqlite3
    row=pending('id');data=b'\xff\xd8\xffcomplete'
    acquire(row,receipt('id',data),lambda:None,tmp_path,transfer(data))
    def success(command,**kwargs):
        Path(command[-1]).write_text(json.dumps({'text':'Flora candidate','engine':'test','language':'en-US'}))
    ocr(row,lambda:None,tmp_path,success)
    state={'files':{'id':row}}
    database=index_ocr(state,'reference/candidates.sqlite',tmp_path)
    results=search_ocr(state,'Flora','reference/candidates.sqlite',tmp_path)
    assert results[0]['file_id']=='id' and results[0]['status']=='OCR_CANDIDATE_NOT_VERIFIED_TRANSCRIPTION'
    with sqlite3.connect(database) as db:
        db.execute("UPDATE candidates SET text='fabricated positive match'")
    with pytest.raises(ValueError,match='integrity'):
        search_ocr(state,'fabricated','reference/candidates.sqlite',tmp_path)
    index_ocr(state,'reference/candidates.sqlite',tmp_path)
    (tmp_path/row['ocr_path']).write_text('changed')
    with pytest.raises(ValueError,match='integrity'):
        search_ocr(state,'Flora','reference/candidates.sqlite',tmp_path)
