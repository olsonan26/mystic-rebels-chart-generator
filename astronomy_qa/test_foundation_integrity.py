"""Fault-test research retrieval and transitive approval boundaries."""
import hashlib
import sqlite3

import pytest
from pypdf import PdfWriter

from knowledge_audit.corpus import index_pdf, search
from knowledge_audit.registry import approval_errors


def test_readonly_search_never_creates_a_missing_source_database(tmp_path):
    missing = tmp_path / 'missing.sqlite'
    with pytest.raises(sqlite3.OperationalError):
        search(missing, 'Sophia')
    assert not missing.exists()


def test_fts_poisoning_cannot_return_a_nonmatching_witness(tmp_path):
    dbpath = tmp_path / 'source.sqlite'
    with sqlite3.connect(dbpath) as db:
        db.executescript('CREATE TABLE sources(id TEXT,sha256 TEXT,pages INTEGER);'
            'CREATE TABLE pages(source_id TEXT,pdf_page INTEGER,text TEXT,text_sha256 TEXT,review_status TEXT);'
            'CREATE VIRTUAL TABLE passages USING fts5(source_id UNINDEXED,pdf_page UNINDEXED,text);')
        text = 'Moon source passage'
        db.execute('INSERT INTO sources VALUES(?,?,?)', ('source','a'*64,1))
        db.execute('INSERT INTO pages VALUES(?,?,?,?,?)', ('source',1,text,hashlib.sha256(text.encode()).hexdigest(),'EXTRACTED'))
        db.execute('INSERT INTO passages VALUES(?,?,?)', ('source',1,'Sophia fabricated search match'))
    with pytest.raises(ValueError, match='integrity'):
        search(dbpath, 'Sophia')


def test_reindex_does_not_cover_up_tampered_page_content(tmp_path):
    path, database = tmp_path / 'source.pdf', tmp_path / 'source.sqlite'
    writer = PdfWriter()
    writer.add_blank_page(width=100,height=100)
    with path.open('wb') as f:
        writer.write(f)
    index_pdf(path,database,'v1')
    with sqlite3.connect(database) as db:
        wrong = 'tampered but self-consistent hash'
        db.execute('UPDATE pages SET text=?,text_sha256=?', (wrong,hashlib.sha256(wrong.encode()).hexdigest()))
    with pytest.raises(ValueError, match='integrity failed'):
        index_pdf(path,database,'v1')
    with sqlite3.connect(database) as db:
        assert db.execute('SELECT text FROM pages').fetchone()[0] == wrong


def approved(id, dependencies=()):
    return dict(id=id,source_status='ENGINEERING_SPECIFIED', conflicts=[],
        implementation_status='RUNTIME_IMPLEMENTED', verification_tests=['test.py'],
        answer_use='APPROVED', dependencies=list(dependencies))


def test_approval_cycle_cannot_approve_itself_or_two_dependent_rules():
    a, b = approved('a',['b']), approved('b',['a'])
    assert any('cyclic' in e for e in approval_errors(a,{'a':a,'b':b}))
    a = approved('a',['a'])
    assert any('cyclic' in e for e in approval_errors(a,{'a':a}))


def test_dependency_approved_flag_cannot_hide_an_invalid_grandparent():
    a, b, c = approved('a',['b']), approved('b',['c']), approved('c')
    c['conflicts'] = ['source disagrees']
    errors = approval_errors(a,{'a':a,'b':b,'c':c})
    assert any('invalid_dependency:b:invalid_dependency:c:unresolved_source_conflict' == e for e in errors)
    assert approval_errors(approved('valid'),{}) == []
