"""A dirty local fix must not become the published audit's code fingerprint."""
import hashlib

import pytest

from knowledge_audit import requirements as module


def trace(text,basis=None):
    value={'code_trace':[{'path':'app.py','sha256':hashlib.sha256(text.encode()).hexdigest()}]}
    if basis:value['code_trace_basis']=basis
    return value


def test_committed_trace_excludes_dirty_file_but_detects_new_commit(tmp_path,monkeypatch):
    (tmp_path/'.git').write_text('managed checkout marker')
    (tmp_path/'app.py').write_text('uncommitted fix\n')
    def read_committed(args,cwd):
        assert args==['git','show','HEAD:app.py'] and cwd==tmp_path
        return b'published code\r\n'
    monkeypatch.setattr(module.subprocess,'check_output',read_committed)
    data=trace('published code\n','COMMITTED_HEAD')
    module.validate_code_trace(data,tmp_path)
    monkeypatch.setattr(module.subprocess,'check_output',lambda *a,**k:b'new committed code\n')
    with pytest.raises(ValueError,match='product path changed'):
        module.validate_code_trace(data,tmp_path)


def test_source_archive_validates_included_code_without_git(tmp_path):
    (tmp_path/'app.py').write_bytes(b'published code\r\n')
    data=trace('published code\n','COMMITTED_HEAD')
    module.validate_code_trace(data,tmp_path)
    (tmp_path/'app.py').write_text('different code\n')
    with pytest.raises(ValueError,match='product path changed'):
        module.validate_code_trace(data,tmp_path)


def test_legacy_worktree_trace_stays_strict_and_unknown_basis_fails(tmp_path):
    (tmp_path/'app.py').write_text('local code\n')
    module.validate_code_trace(trace('local code\n'),tmp_path)
    with pytest.raises(ValueError,match='product path changed'):
        module.validate_code_trace(trace('old code\n'),tmp_path)
    with pytest.raises(ValueError,match='Unknown code trace basis'):
        module.validate_code_trace(trace('local code\n','IGNORE_CHANGES'),tmp_path)
