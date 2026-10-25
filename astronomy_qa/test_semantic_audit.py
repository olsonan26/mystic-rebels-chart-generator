"""Guard source identity, counterevidence and report dependency boundaries."""
import copy
import hashlib
import json
import sqlite3

import pytest

from knowledge_audit.registry import ROOT, load_registry
from knowledge_audit.semantics import (
    load_inventory, validate_inventory, validate_examples, profile_gaps, concept_packet,
    verify_pdf_witnesses,
)


def test_real_inventory_and_examples_reference_existing_source_rules():
    assert validate_inventory(load_inventory())
    assert validate_examples()


@pytest.mark.parametrize('field,value', [
    ('all_important_knowledge_covered', True),
    ('original_batch_scan_mapping_complete', True),
    ('semantic_coverage_percent', 100),
])
def test_no_denominator_or_scan_completeness_inflation(field, value):
    inventory = load_inventory()
    inventory['completeness'][field] = value
    with pytest.raises(ValueError, match='complete source coverage'):
        validate_inventory(inventory)


@pytest.mark.parametrize('field,value', [
    ('answer_use', 'APPROVED'), ('runtime_interpretation', 'IMPLEMENTED'),
])
def test_copied_readiness_flag_cannot_enable_interpretation(field, value):
    inventory = load_inventory()
    inventory['records'][0][field] = value
    with pytest.raises(ValueError, match='cannot authorize'):
        validate_inventory(inventory)


def test_unknown_reference_cycle_and_numbering_confusion_are_rejected():
    inventory = load_inventory()
    inventory['records'][0]['requires_concepts'] = ['not-a-concept']
    with pytest.raises(ValueError, match='Unknown concept'):
        validate_inventory(inventory)
    inventory = load_inventory()
    inventory['records'][0]['requires_concepts'] = [inventory['records'][0]['id']]
    with pytest.raises(ValueError, match='Cyclic'):
        validate_inventory(inventory)
    inventory = load_inventory()
    inventory['records'][0]['witnesses'][0]['reflow_footer'] += 1
    with pytest.raises(ValueError, match='page witness'):
        validate_inventory(inventory)


def test_report_dependencies_include_indirect_spark_and_runtime_gaps():
    # This section's direct concepts omit Spark. Its PHSR-dependent meanings
    # still require a full directional graph, independent of calculated points.
    result = profile_gaps(section_id='retrograde-profile')['sections'][0]
    assert 'directional-context' in result['transitive_concept_ids']
    assert 'N9-033' in result['calculation_rule_ids']
    assert result['status'] == 'NOT_READY_FOR_PERSONAL_REPORT'
    result = profile_gaps(section_id='synastry-profile')['sections'][0]
    assert 'spark-entry' in result['transitive_concept_ids']
    assert {'N9-020', 'N9-021'} <= set(result['calculation_rule_ids'])
    assert next(r for r in result['unresolved_meanings'] if r['id'] == 'spark-entry')['status'] == 'CONFLICT'
    with pytest.raises(ValueError, match='Unknown report section'):
        profile_gaps(section_id='imagined')


def test_numerical_ready_flags_do_not_approve_meaning_sections():
    registry = copy.deepcopy(load_registry())
    # Even a complete calculation register cannot create missing report code.
    for rule in registry['rules']:
        rule.update(implementation_status='RUNTIME_IMPLEMENTED', source_status='PRIMARY_RULE_REVIEWED', conflicts=[])
    result = profile_gaps(registry=registry)
    assert all(section['missing_runtime_interpretations'] for section in result['sections'])
    assert all(section['status'] == 'NOT_READY_FOR_PERSONAL_REPORT' for section in result['sections'])
    assert result['personal_answer_generated'] is False


@pytest.fixture
def synthetic_packet(tmp_path):
    # Unit fixture only: synthetic text, never asserted to be the real PDF.
    inventory = load_inventory()
    record = copy.deepcopy(next(r for r in inventory['records'] if r['id'] == 'spark-entry'))
    inventory['records'] = [record]
    inventory['report_sections'] = [dict(id='test-context', title='Test context',
        concept_ids=['spark-entry'], rule_ids=[], required_chart_facts=[], contexts=['dynamic'])]
    database = tmp_path / 'private.sqlite'
    with sqlite3.connect(database) as db:
        db.executescript('CREATE TABLE sources(id TEXT,sha256 TEXT,pages INTEGER);'
            'CREATE TABLE pages(source_id TEXT,pdf_page INTEGER,text TEXT,text_sha256 TEXT,review_status TEXT);')
        source = inventory['source']
        db.execute('INSERT INTO sources VALUES(?,?,?)', (source['id'],source['sha256'],source['pdf_pages']))
        for witness in record['witnesses']:
            text = 'Synthetic competing witness on page ' + str(witness['pdf_page'])
            digest = hashlib.sha256(text.encode()).hexdigest()
            witness['page_text_sha256'] = digest
            db.execute('INSERT INTO pages VALUES(?,?,?,?,?)',
                (source['id'], witness['pdf_page'], text, digest, 'EXTRACTED_NOT_REVIEWED'))
    return inventory, database


def test_exact_concept_lookup_retains_all_competing_witnesses(synthetic_packet):
    inventory, database = synthetic_packet
    packet = concept_packet('spark-entry', database, 'test-context', inventory)
    assert {w['pdf_page'] for w in packet['witnesses']} == {292,293,433,434,458}
    assert packet['concepts'][0]['source_status'] == 'CONFLICT'
    assert packet['contexts'] == ['dynamic']
    assert packet['use'] == 'AUDIT_ONLY_NOT_PERSONAL_ADVICE'
    assert not packet['personal_answer_generated']
    assert all(w['extraction_status'] == 'EXTRACTED_NOT_REVIEWED' for w in packet['witnesses'])


def test_integrity_and_context_fail_closed(synthetic_packet, tmp_path):
    inventory, database = synthetic_packet
    with pytest.raises(ValueError, match='outside this report section'):
        concept_packet('fortune', database, 'test-context', inventory)
    with sqlite3.connect(database) as db:
        db.execute("UPDATE pages SET text='wrong' WHERE pdf_page=458")
    with pytest.raises(ValueError, match='integrity mismatch: 458'):
        concept_packet('spark-entry', database, 'test-context', inventory)
    with sqlite3.connect(database) as db:
        db.execute("UPDATE sources SET sha256='wrong'")
    with pytest.raises(ValueError, match='source identity mismatch'):
        concept_packet('spark-entry', database, 'test-context', inventory)
    missing = tmp_path / 'missing.sqlite'
    with pytest.raises(sqlite3.OperationalError):
        concept_packet('spark-entry', missing, 'test-context', inventory)
    assert not missing.exists()


def test_an_altered_pdf_cannot_claim_the_recorded_source_identity(tmp_path):
    wrong = tmp_path / 'wrong.pdf'
    wrong.write_bytes(b'not the source')
    with pytest.raises(ValueError, match='PDF source hash mismatch'):
        verify_pdf_witnesses(wrong, tmp_path / 'unused.sqlite')


def test_all_pdf_pages_accounted_for_without_semantic_completion_claim():
    inventory = load_inventory()
    ledger = json.loads((ROOT / 'evidence/semantic-audit/page-ledger.json').read_text())
    assert ledger['source_sha256'] == inventory['source']['sha256']
    assert [p['pdf_page'] for p in ledger['pages']] == list(range(1,693))
    expected = {}
    for record in inventory['records']:
        for witness in record['witnesses']:
            expected.setdefault(witness['pdf_page'], set()).add(record['id'])
    for page in ledger['pages']:
        assert set(page['interpretive_record_ids']) == expected.get(page['pdf_page'], set())
        assert page['original_scan_mapping'] == 'UNRESOLVED'
        assert 'text' not in page


def test_examples_keep_the_nonmatching_and_nonnumeric_cases():
    examples = json.loads((ROOT / 'data/knowledge/worked_examples.json').read_text())
    by_id = {e['id']:e for e in examples['examples']}
    assert by_id['spark-composite-saturn']['kind'] == 'CONTRADICTION'
    assert by_id['with-while-non-aspect']['kind'] == 'CONTEXT_SEPARATION'
    # These arithmetic checks expose the source conflicts, not a new rule.
    pluto = by_id['pluto-ooi-counterexample']['source_facts']
    assert 24*60+42+pluto['stated_radius_deg']*60 == 26*60+12
    assert (133+325-81)%360 == by_id['fortune-arithmetic']['source_facts']['rounded_result']
    assert (133+81-325)%360 == by_id['spirit-arithmetic']['source_facts']['rounded_result']
    broken = copy.deepcopy(examples)
    broken['examples'][0]['pdf_pages'] = [1]
    with pytest.raises(ValueError, match='outside its concept witnesses'):
        validate_examples(broken)
