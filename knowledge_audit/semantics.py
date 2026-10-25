"""Audit-only interpretation inventory, dependency tracing and source retrieval.

This module never calculates charts, approves rules or generates personal prose.
The existing calculation register remains the authority for runtime method status.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

from .registry import ROOT, load_registry, validate_registry
from .sources import original_witnesses, atomic_assertions

INVENTORY = ROOT / 'data/knowledge/interpretive_inventory.json'
EXAMPLES = ROOT / 'data/knowledge/worked_examples.json'
SOURCE_STATES = {
    'PASSAGE_REVIEWED', 'CONFLICT', 'SEMANTIC_TENSION', 'INCOMPLETE',
    'FRAGMENT', 'PRIOR_REVIEW_ONLY',
}
SHA256 = re.compile(r'[0-9a-f]{64}\Z')


def load_inventory(path=INVENTORY):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def validate_examples(examples=None, inventory=None):
    inventory = load_inventory() if inventory is None else inventory
    validate_inventory(inventory)
    examples = json.loads(EXAMPLES.read_text(encoding='utf-8')) if examples is None else examples
    if (examples['source_id'] != inventory['source']['id']
            or examples['source_sha256'] != inventory['source']['sha256']
            or examples['scope'] != 'SELECTED_WORKED_EXAMPLES_NOT_EXHAUSTIVE'):
        raise ValueError('Worked example source/scope mismatch')
    records = {r['id']: r for r in inventory['records']}
    _unique(examples['examples'], 'worked example ID')
    for example in examples['examples']:
        record = records.get(example['concept_id'])
        if record is None:
            raise ValueError('Unknown worked example concept')
        witness_pages = {w['pdf_page'] for w in record['witnesses']}
        if not example['pdf_pages'] or not set(example['pdf_pages']) <= witness_pages:
            raise ValueError('Worked example page outside its concept witnesses')
        if (not example['source_assertion'] or not example['audit_expectation']
                or example['use'] != 'SOURCE_EXAMPLE_NOT_INDEPENDENT_PERSONAL_VALIDATION'):
            raise ValueError('Worked example lacks its applicability limit')
    return True


def _unique(rows, label):
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate ' + label)
    return {row['id']: row for row in rows}


def validate_inventory(inventory, registry=None):
    """Reject incomplete citations, dangling dependencies and readiness inflation."""
    registry = load_registry() if registry is None else registry
    validate_registry(registry, check_files=False)
    rules = {row['id']: row for row in registry['rules']}
    if inventory.get('schema_version') != '1.0':
        raise ValueError('Unknown interpretive inventory schema')
    if inventory.get('scope') != 'TARGETED_PDF_MEANING_CONTEXT_EXCEPTION_AUDIT':
        raise ValueError('Unknown audit scope')
    completeness = inventory['completeness']
    if (completeness['all_important_knowledge_covered'] is not False
            or completeness['original_batch_scan_mapping_complete'] is not False
            or completeness['semantic_coverage_percent'] is not None):
        raise ValueError('Unestablished complete source coverage')
    source = inventory['source']
    if (not SHA256.fullmatch(source['sha256'])
            or source['sha256'] != registry['source_inventory']['compiled_pdf_sha256']
            or source['pdf_pages'] != registry['source_inventory']['compiled_pdf_pages']):
        raise ValueError('Source identity differs from the preserved audit baseline')
    records = _unique(inventory['records'], 'concept ID')
    sections = _unique(inventory['report_sections'], 'report section ID')
    if not records or not sections:
        raise ValueError('Empty interpretive inventory')
    page_hashes = {}
    original_only = [r['id'] for r in records.values() if not r.get('witnesses')]
    original_verified = {c for w in original_witnesses(original_only) for c in w['linked_concept_ids']} if original_only else set()
    for row in records.values():
        if row['source_status'] not in SOURCE_STATES:
            raise ValueError('Unknown source status: ' + row['id'])
        # These records document gaps. A flag edit cannot approve personal use.
        if row['answer_use'] != 'NOT_APPROVED' or row['runtime_interpretation'] != 'ABSENT':
            raise ValueError('Audit records cannot authorize runtime interpretation: ' + row['id'])
        for field in ('title', 'kind', 'meaning_summary', 'report_gap', 'contexts'):
            if not row.get(field):
                raise ValueError('Missing ' + field + ': ' + row['id'])
        if not row['witnesses']:
            if row.get('witness_scope') != 'ORIGINAL_ONLY_NO_DEDICATED_COMPILED_MEANING' or row['id'] not in original_verified:
                raise ValueError('Missing verified original or compiled witnesses: ' + row['id'])
        for witness in row['witnesses']:
            p = witness['pdf_page']
            if (type(p) is not int or not 1 <= p <= source['pdf_pages']
                    or witness['reflow_footer'] != p + 4
                    or witness['source_id'] != source['id']
                    or not SHA256.fullmatch(witness['page_text_sha256'])):
                raise ValueError('Invalid page witness: ' + row['id'])
            previous = page_hashes.setdefault(p, witness['page_text_sha256'])
            if previous != witness['page_text_sha256']:
                raise ValueError('Conflicting page hashes')
        for dependency in row['requires_concepts']:
            if dependency not in records:
                raise ValueError('Unknown concept dependency: ' + dependency)
        for rule_id in row['calculation_rule_ids']:
            if rule_id not in rules:
                raise ValueError('Unknown calculation rule: ' + rule_id)
    for section in sections.values():
        if not section['contexts'] or not section['concept_ids']:
            raise ValueError('Missing section context or concepts')
        for concept_id in section['concept_ids']:
            if concept_id not in records:
                raise ValueError('Unknown section concept: ' + concept_id)
        for rule_id in section['rule_ids']:
            if rule_id not in rules:
                raise ValueError('Unknown section rule: ' + rule_id)
    # Check cycles even in concepts not currently requested by a report section.
    _closure(records, list(records))
    return True


def _closure(records, ids):
    ordered, done, visiting = [], set(), set()

    def visit(id):
        if id not in records:
            raise ValueError('Unknown concept: ' + id)
        if id in visiting:
            raise ValueError('Cyclic concept prerequisite: ' + id)
        if id in done:
            return
        visiting.add(id)
        for dependency in records[id]['requires_concepts']:
            visit(dependency)
        visiting.remove(id)
        done.add(id)
        ordered.append(id)

    for id in ids:
        visit(id)
    return ordered


def profile_gaps(inventory=None, registry=None, section_id=None):
    """List actual transitive blockers; this is not a personalized report planner."""
    inventory = load_inventory() if inventory is None else inventory
    registry = load_registry() if registry is None else registry
    validate_inventory(inventory, registry)
    records = {row['id']: row for row in inventory['records']}
    rules = {row['id']: row for row in registry['rules']}
    sections = inventory['report_sections']
    if section_id is not None:
        sections = [row for row in sections if row['id'] == section_id]
        if not sections:
            raise ValueError('Unknown report section: ' + section_id)
    output = []
    for section in sections:
        ids = _closure(records, section['concept_ids'])
        rule_ids = sorted(set(section['rule_ids']).union(
            *(records[id]['calculation_rule_ids'] for id in ids)))
        rule_blockers = [dict(id=id, implementation=rules[id]['implementation_status'],
            source=rules[id]['source_status'], conflicts=rules[id]['conflicts'])
            for id in rule_ids if rules[id]['implementation_status'] != 'RUNTIME_IMPLEMENTED'
            or rules[id]['conflicts']
            or rules[id]['source_status'] not in ('PRIMARY_RULE_REVIEWED', 'ENGINEERING_SPECIFIED')]
        output.append(dict(
            **section, transitive_concept_ids=ids,
            status='NOT_READY_FOR_PERSONAL_REPORT',
            calculation_rule_ids=rule_ids,
            calculation_or_source_blockers=rule_blockers,
            unresolved_meanings=[dict(id=id, status=records[id]['source_status'])
                for id in ids if records[id]['source_status'] != 'PASSAGE_REVIEWED'],
            missing_runtime_interpretations=ids,
            missing_runtime_layers=['applicable_source_retrieval', 'chart_context_graph',
                'evidence_bound_synthesis', 'claim_citations_and_evaluation'],
            required_chart_facts_status='REQUIREMENTS_ONLY_NOT_CHECKED_AGAINST_A_PERSON',
        ))
    return dict(scope='OFFLINE_REPORT_REQUIREMENTS_AUDIT',
        personal_answer_generated=False, source_semantic_coverage_percent=None,
        counts=dict(concepts=len(records), report_sections=len(inventory['report_sections']),
            source_states=dict(Counter(r['source_status'] for r in records.values()))),
        sections=output)


def concept_packet(concept_id, database_path, section_id, inventory=None, registry=None):
    """Exact concept retrieval returns every cited witness, including counterevidence.

    A report section supplies an explicit context contract. No FTS ranking can
    suppress contradictory witnesses. Retrieved text remains unapproved data.
    """
    inventory = load_inventory() if inventory is None else inventory
    registry = load_registry() if registry is None else registry
    report = profile_gaps(inventory, registry, section_id)['sections'][0]
    if concept_id not in report['transitive_concept_ids']:
        raise ValueError('Concept is outside this report section context')
    records = {row['id']: row for row in inventory['records']}
    ids = _closure(records, [concept_id])
    source = inventory['source']
    # Read-only SQLite prevents an accidental empty or altered private source DB.
    uri = Path(database_path).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        actual = db.execute('SELECT sha256,pages FROM sources WHERE id=?', (source['id'],)).fetchone()
        if actual != (source['sha256'], source['pdf_pages']):
            raise ValueError('Indexed source identity mismatch')
        witnesses = {}
        for id in ids:
            for witness in records[id]['witnesses']:
                p = witness['pdf_page']
                page = db.execute('SELECT text,text_sha256,review_status FROM pages WHERE source_id=? AND pdf_page=?',
                    (source['id'], p)).fetchone()
                if (page is None or page[1] != witness['page_text_sha256']
                        or hashlib.sha256(page[0].encode()).hexdigest() != page[1]):
                    raise ValueError('Page witness integrity mismatch: ' + str(p))
                witnesses[p] = dict(**witness, text=page[0], extraction_status=page[2],
                    original_printed_page=None, original_page_mapping='NOT_ESTABLISHED_BY_THIS_PACKET')
    blocker_path=ROOT/'data/knowledge/source_blocker_findings.json'
    blockers=json.loads(blocker_path.read_text())['findings'] if blocker_path.exists() else []
    return dict(scope='LOCAL_RESEARCH_WITNESS_PACKET', use='AUDIT_ONLY_NOT_PERSONAL_ADVICE',
        report_section_id=section_id, contexts=report['contexts'],
        concept_ids=ids, concepts=[records[id] for id in ids],
        source_sha256=source['sha256'], witnesses=[witnesses[p] for p in sorted(witnesses)],
        original_scan_witnesses=original_witnesses(ids),
        original_atomic_assertions=atomic_assertions(ids),
        original_line_reconciliation_findings=[r for r in blockers if set(r['concept_ids']) & set(ids)],
        witness_policy='RETAIN_COMPILATION_AND_ORIGINAL_COUNTEREVIDENCE_SEPARATELY',
        report_readiness=report['status'], personal_answer_generated=False)


def verify_pdf_witnesses(pdf_path, database_path, inventory=None):
    """Verify all normalized page bytes against the supplied PDF, not DB labels."""
    from pypdf import PdfReader
    inventory = load_inventory() if inventory is None else inventory
    validate_inventory(inventory)
    source = inventory['source']
    pdf_path = Path(pdf_path)
    if hashlib.sha256(pdf_path.read_bytes()).hexdigest() != source['sha256']:
        raise ValueError('PDF source hash mismatch')
    reader = PdfReader(pdf_path)
    if len(reader.pages) != source['pdf_pages']:
        raise ValueError('PDF page count mismatch')
    expected = {w['pdf_page']: w['page_text_sha256'] for r in inventory['records'] for w in r['witnesses']}
    uri = Path(database_path).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        if db.execute('SELECT sha256,pages FROM sources WHERE id=?', (source['id'],)).fetchone() != (source['sha256'], source['pdf_pages']):
            raise ValueError('Indexed source identity mismatch')
        for p, page in enumerate(reader.pages, 1):
            normalized = re.sub(r'\s+', ' ', page.extract_text() or '').strip()
            digest = hashlib.sha256(normalized.encode()).hexdigest()
            indexed = db.execute('SELECT text,text_sha256 FROM pages WHERE source_id=? AND pdf_page=?',
                (source['id'], p)).fetchone()
            if indexed != (normalized, digest) or (p in expected and expected[p] != digest):
                raise ValueError('PDF/index/page witness mismatch: ' + str(p))
    return dict(status='PDF_AND_INDEX_WITNESSES_MATCH', pdf_pages=len(reader.pages),
        concept_witness_pages=len(expected), source_sha256=source['sha256'],
        complete_semantic_coverage_claimed=False)
