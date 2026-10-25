"""Prevent source readiness, extraction, or search from masquerading as coverage."""
import copy
import json
import sqlite3
import hashlib
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from knowledge_audit.registry import load_registry,validate_registry,coverage,approval_errors
from knowledge_audit.corpus import search,index_pdf
from mystic_rebels.api import app

def test_runtime_inventory_has_real_files_and_never_claims_complete_batches():
    registry=load_registry()
    assert validate_registry(registry)
    report=coverage(registry)
    assert report['batch_count']==8
    assert not report['enumeration_complete']
    assert report['source_semantic_coverage_percent'] is None
    assert not report['complete_intelligence_claim_allowed']
    assert len(registry['rules'])==44

def test_contradiction_and_unimplemented_rule_cannot_be_approved():
    registry=load_registry()
    spark=next(r for r in registry['rules'] if r['id']=='N9-020')
    spark['answer_use']='APPROVED'
    with pytest.raises(ValueError,match='unresolved_source_conflict'):
        validate_registry(registry)
    assert spark['explicit_written_procedure'].startswith('house parity:')

def test_no_dependency_shortcuts_or_unknown_rule_ids():
    rule={'source_status':'PRIMARY_RULE_REVIEWED','implementation_status':'RUNTIME_IMPLEMENTED',
          'witnesses':[{'pdf_page':203}],'verification_tests':['astronomy_qa/test_gradity.py'],
          'dependencies':['missing']}
    assert 'unknown_dependency:missing' in approval_errors(rule,{})
    assert 'unapproved_dependency:missing' in approval_errors(rule,{'missing':{'answer_use':'BLOCKED'}})

def test_methodology_api_returns_metadata_and_honest_layer_status_only():
    with TestClient(app) as client:
        response=client.get('/api/methodology')
    assert response.status_code==200
    data=response.json()
    assert data['intelligence_layers']['runtime_source_retrieval']=='ABSENT'
    assert data['intelligence_layers']['personal_question_answering']=='ABSENT'
    assert data['coverage']['source_semantic_coverage_percent'] is None
    assert 'b64_string' not in response.text and 'detailed_explanation' not in response.text

def test_private_page_index_retrieves_citation_without_rule_approval(tmp_path):
    # Use a tiny page created with pypdf's built-in blank-page facility to verify
    # source hashing/identity even when extraction returns no readable text.
    from pypdf import PdfWriter
    writer=PdfWriter();writer.add_blank_page(width=100,height=100)
    pdf=tmp_path/'source.pdf'
    with pdf.open('wb') as f:writer.write(f)
    database=tmp_path/'index.sqlite'
    report=index_pdf(pdf,database,'version1')
    assert report['pdf_pages']==1 and report['status']=='INDEXED_NOT_RULE_APPROVAL'
    with sqlite3.connect(database) as db:
        text='Spark odd numbered houses'
        db.execute("UPDATE pages SET text=?,text_sha256=? WHERE source_id='version1'",(text,hashlib.sha256(text.encode()).hexdigest()))
        db.execute("UPDATE passages SET text='Spark odd numbered houses' WHERE source_id='version1'")
    rows=search(database,'odd numbered houses')
    assert rows[0]['pdf_page']==1 and rows[0]['source_sha256']==report['sha256']
    assert rows[0]['review_status']=='EXTRACTED_NOT_REVIEWED'
    assert rows[0]['use']=='SOURCE_WITNESS_ONLY_NOT_APPROVED_INTERPRETATION'
    assert search(database,'" OR 1=1 --')==[]
    assert search(database,'')==[]
    with pytest.raises(ValueError):search(database,'Spark',51)
    with sqlite3.connect(database) as db:
        db.execute("UPDATE pages SET text_sha256='corrupt' WHERE source_id='version1'")
    with pytest.raises(ValueError,match='integrity'):search(database,'Spark')
    pdf.write_bytes(pdf.read_bytes()+b'\n%changed')
    with pytest.raises(ValueError,match='Source changed'):index_pdf(pdf,database,'version1')

def test_duplicate_rule_and_missing_evidence_rejected():
    registry=load_registry();registry['rules'].append(copy.deepcopy(registry['rules'][0]))
    with pytest.raises(ValueError,match='Duplicate'):validate_registry(registry)
    registry=load_registry();registry['rules'][0]['verification_tests']=['does-not-exist.py']
    with pytest.raises(ValueError,match='Missing evidence'):validate_registry(registry)
