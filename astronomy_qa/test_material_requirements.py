"""Prevent omitted subrequirements and source corrections from disappearing."""
import copy
import json

import pytest

from knowledge_audit.registry import ROOT
from knowledge_audit.requirements import load_requirements, validate_requirements, requirement_packet
from knowledge_audit.sources import load_manifest, validate_manifest, original_witnesses, atomic_assertions


def test_original_eighteen_rows_and_each_atomic_task_are_accounted_for():
    data = load_requirements()
    assert validate_requirements(data)
    assert len(data['sections']) == 18
    assert sum(len(s['fragments']) for s in data['sections']) == 74
    assert len(data['requirements']) == 207
    # Requirements are a new denominator; they do not establish book coverage.
    assert data['semantic_coverage_percent'] is None
    assert all(not r['personal_answer_approved'] for r in data['requirements'])


@pytest.mark.parametrize('mutation', ['atomic', 'fragment', 'section', 'orphan'])
def test_compound_entries_cannot_be_closed_by_dropping_one_part(mutation):
    data = load_requirements()
    if mutation == 'atomic':
        data['requirements'].pop(1)
    elif mutation == 'fragment':
        data['sections'][0]['fragments'].pop(1)
    elif mutation == 'section':
        data['sections'].pop()
    else:
        data['sections'][0]['fragments'][0]['atomic_requirement_ids'].append(data['requirements'][1]['id'])
    with pytest.raises(ValueError):
        validate_requirements(data, check_files=False)


def test_source_found_calculation_and_answer_use_remain_distinct():
    data = load_requirements()
    sophia = [r for r in data['requirements'] if r['title'].endswith('Sophia construction')]
    assert len(sophia) == 2
    assert all(r['disposition'] == 'source found but implementation missing' for r in sophia)
    assert all({w['original_printed_page'] for w in r['original_scan_witnesses']} >= {'617','618','619'} for r in sophia)
    assert all(r['implementation_evidence']['actual_report_use'] == 'ABSENT_IN_INSPECTED_SOURCE' for r in sophia)
    assert not [r for r in data['requirements'] if r['disposition'] == 'inaccessible']
    missing = next(r for r in data['requirements'] if r['title'].startswith('Flora'))
    assert missing['concept_ids']==['asteroid-flora']
    assert missing['disposition']=='source found but implementation missing'
    assert {w['original_printed_page'] for w in missing['original_scan_witnesses']} >= {'720','721','773'}
    assert missing['implementation_evidence']['source_present']=='TARGETED_ORIGINAL_ONLY'
    assert not missing['personal_answer_approved']


def test_deployed_usage_or_resolution_cannot_be_asserted_by_a_flag_edit():
    data = load_requirements()
    data['requirements'][0]['disposition'] = 'resolved'
    with pytest.raises(ValueError, match='resolved or approved'):
        validate_requirements(data, check_files=False)
    data = load_requirements()
    data['requirements'][0]['implementation_evidence']['actual_report_use'] = 'USED'
    with pytest.raises(ValueError, match='deployed answer use'):
        validate_requirements(data, check_files=False)


def test_original_counterevidence_is_required_in_each_linked_task():
    data = load_requirements()
    row = next(r for r in data['requirements'] if r['title'].startswith('Mean Sophia'))
    row['original_scan_witnesses'].pop()
    with pytest.raises(ValueError, match='original counterevidence'):
        validate_requirements(data, check_files=False)


def test_visible_drive_denominator_keeps_file_and_page_accounting_separate():
    data = load_manifest()
    assert validate_manifest(data)
    assert [b['observed_count'] for b in data['batches']] == [56,66,73,31,253,186,66,297]
    assert data['file_record_denominator'] == 1029
    assert data['printed_page_denominator'] is None
    assert all(b['connector_subset_of_browser'] for b in data['batches'])
    assert data['repeated_filenames'][0]['name'] == 'img_5079.jpg'
    # Two IDs with one name are not proven duplicates of book content.
    assert len(data['repeated_filenames'][0]['file_ids']) == 2


@pytest.mark.parametrize('mutation', ['endpoint','hash','semantic','duplicate'])
def test_inventory_cannot_turn_a_capped_listing_into_reviewed_pages(mutation):
    data = load_manifest()
    if mutation == 'endpoint':
        data['batches'][4]['files'].pop()
    elif mutation == 'hash':
        data['batches'][0]['files'][0]['acquisition_status'] = 'ACQUIRED_HASHED'
        data['batches'][0]['files'][0]['content_sha256'] = None
    elif mutation == 'semantic':
        data['printed_page_denominator'] = 1029
    else:
        data['batches'][0]['files'][1]['file_id'] = data['batches'][0]['files'][0]['file_id']
    with pytest.raises(ValueError):
        validate_manifest(data, check_files=False)


def test_original_corrections_keep_residual_conflicts_and_numbering():
    data = json.loads((ROOT / 'data/knowledge/source_review_updates.json').read_text())
    questions = {q['id']: q for q in data['source_questions']}
    assert questions['pluto-arithmetic']['disposition'] == 'resolved'
    assert questions['pluto-original-coordinate']['disposition'] == 'contradictory'
    assert questions['chiron-jackson-degree']['disposition'] == 'resolved'
    assert questions['chiron-saturn-aspect']['disposition'] == 'contradictory'
    assert questions['eunomia-two-meanings']['disposition'] == 'contradictory'
    assert questions['progression-original-492']['disposition'] == 'inaccessible'
    witnesses = original_witnesses(['sophia'])
    assert {w['original_printed_page'] for w in witnesses} >= {'617','618','619','620','623','624'}
    assert all(w['pdf_pages'] == [] and w['reflow_footer'] is None for w in witnesses if w['original_printed_page'] in {'617','618','619'})
    bad = copy.deepcopy(data)
    next(r for r in bad['reviews'] if r[0] == 'IMG_5086.JPG')[4] = 'An invented formula'
    with pytest.raises(ValueError, match='mapping mismatch'):
        original_witnesses(['sophia'], updates=bad)


def test_atomic_meanings_keep_both_competing_eunomia_claims_and_formula_limits():
    meanings = atomic_assertions(['asteroid-eunomia'])
    assert {r['id'] for r in meanings} == {'eunomia-surviving-core','eunomia-functional-order'}
    sophia = atomic_assertions(['sophia'])
    assert len([r for r in sophia if r['kind'] == 'formula_specification']) == 2
    assert all(r['execution_status'] == 'NOT_EXECUTABLE_NOT_RUNTIME_APPROVED' for r in sophia)
    data = json.loads((ROOT / 'data/knowledge/original_assertions.json').read_text())
    data['assertions'] = [r for r in data['assertions'] if r['id'] != 'eunomia-surviving-core']
    with pytest.raises(ValueError, match='Competing source assertion'):
        atomic_assertions(['asteroid-eunomia'], data=data)


def test_corrected_original_examples_preserve_each_residual_error():
    examples = json.loads((ROOT / 'data/knowledge/worked_examples.json').read_text())['examples']
    by_id = {e['id']:e for e in examples}
    pluto = by_id['pluto-ooi-counterexample']['original_scan_correction']
    parse = lambda value: sum(int(n) * factor for n, factor in zip(value.split(':'), (60,1)))
    assert parse(pluto['actual_interval'][0]) + 90 == parse(pluto['actual_interval'][1])
    assert parse(pluto['actual_interval'][1]) < parse('25:57')
    assert parse(pluto['earlier_original_prose']) + 90 > parse('25:57')
    chiron = by_id['chiron-jackson-values']['original_scan_correction']
    assert chiron['original_diagram'] == '19:18 Rx'
    assert 'ASPECT_CONFLICT_REMAINS' in chiron['disposition']
