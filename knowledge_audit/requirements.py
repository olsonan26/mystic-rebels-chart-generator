"""Account for every original material-context fragment and its atomic tasks."""
import hashlib
import json
import subprocess
from pathlib import Path

from .registry import ROOT
from .semantics import load_inventory, validate_inventory, concept_packet
from .sources import original_witnesses, atomic_assertions

REQUIREMENTS = ROOT / 'data/knowledge/material_requirements.json'
DISPOSITIONS = {'resolved', 'source found but implementation missing',
                'source incomplete', 'contradictory', 'inaccessible'}


def load_requirements(path=REQUIREMENTS):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def code_trace_hash(path, basis='WORKING_TREE', root=ROOT):
    """Keep published-code evidence separate from unrelated uncommitted work.

    A source archive has no Git metadata, so its included files are the trace.
    In a checkout, COMMITTED_HEAD inspects HEAD:path and detects committed code
    changes while deliberately excluding uncommitted local fixes.
    """
    if basis not in ('WORKING_TREE', 'COMMITTED_HEAD'):
        raise ValueError('Unknown code trace basis: ' + basis)
    if basis == 'COMMITTED_HEAD' and (root / '.git').exists():
        raw = subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=root)
        text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    else:
        text = (root / path).read_text(encoding='utf-8')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate_code_trace(data, root=ROOT):
    basis = data.get('code_trace_basis', 'WORKING_TREE')
    for ref in data['code_trace']:
        if code_trace_hash(ref['path'], basis, root) != ref['sha256']:
            raise ValueError('Inspected product path changed; refresh code trace: ' + ref['path'])


def _source_table():
    rows = []
    text = (ROOT / 'docs/INTERPRETIVE_COVERAGE_AUDIT.md').read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.startswith('| ') and not line.startswith('| Report section'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == 3:
                rows.append(cells)
            if len(rows) == 18:
                break
    return rows


def validate_requirements(data=None, check_files=True):
    data = load_requirements() if data is None else data
    inventory = load_inventory()
    validate_inventory(inventory)
    records = {r['id']: r for r in inventory['records']}
    sections = data['sections']
    table = _source_table()
    if (len(sections) != 18 or [s['section_id'] for s in sections]
            != [s['id'] for s in inventory['report_sections']]):
        raise ValueError('Original eighteen sections must reconcile in order')
    digest = hashlib.sha256(json.dumps(table, separators=(',', ':')).encode()).hexdigest()
    if data['source_table_sha256'] != digest:
        raise ValueError('Original source table changed; reconcile every row again')
    ids = [r['id'] for r in data['requirements']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate atomic requirement')
    by_id = {r['id']: r for r in data['requirements']}
    assigned = []
    for section, cells in zip(sections, table):
        if [section['original_title'], section['original_existing_support'], section['original_missing_context']] != cells:
            raise ValueError('Original table row mismatch')
        if [f['text'] for f in section['fragments']] != cells[2].split(', '):
            raise ValueError('An original material-context fragment was omitted')
        for fragment in section['fragments']:
            if not fragment['atomic_requirement_ids']:
                raise ValueError('Compound fragment has no atomic requirements')
            for id in fragment['atomic_requirement_ids']:
                row = by_id.get(id)
                if not row or row['section_id'] != section['section_id'] or row['original_fragment'] != fragment['text']:
                    raise ValueError('Atomic requirement missing or assigned to wrong original fragment')
                assigned.append(id)
    if sorted(assigned) != sorted(ids):
        raise ValueError('Atomic requirements omitted, duplicated or orphaned')
    # A later targeted inspection may add evidence for the same photograph.
    # Retain both historical and continuation observations by review identity;
    # deduplicating only by file ID silently discards earlier counterevidence.
    originals = original_witnesses(records)
    assertions = atomic_assertions(list(records))
    for row in by_id.values():
        if row['disposition'] not in DISPOSITIONS:
            raise ValueError('Unknown final disposition')
        if row['personal_answer_approved'] is not False or row['disposition'] == 'resolved':
            raise ValueError('No runtime interpretation has been resolved or approved in this ledger')
        for id in row['concept_ids'] + row['dependency_concept_ids']:
            if id not in records:
                raise ValueError('Unknown requirement concept')
        expected_pdf = {w['pdf_page']: w for c in row['concept_ids'] for w in records[c]['witnesses']}
        if row['source_witnesses'] != [expected_pdf[p] for p in sorted(expected_pdf)]:
            raise ValueError('Requirement lost or changed compiled source witnesses')
        expected_scans = [w for w in originals if set(w['linked_concept_ids']) & set(row['concept_ids'])]
        if row['original_scan_witnesses'] != expected_scans:
            raise ValueError('Requirement lost or changed original counterevidence')
        if row['original_atomic_assertion_ids'] != [a['id'] for a in assertions if a['concept_id'] in row['concept_ids']]:
            raise ValueError('Requirement lost an atomic original source assertion')
        if not row['tests']['required_behavior'] or row['tests']['interpretation_regressions']:
            raise ValueError('Interpretation test coverage cannot be invented')
        if (row['implementation_evidence']['actual_report_use'] != 'ABSENT_IN_INSPECTED_SOURCE'
                or row['implementation_evidence']['live_behavior'] != 'NOT_AUTHENTICATED_OR_VERIFIED_IN_THIS_CONTINUATION'):
            raise ValueError('Local requirements cannot prove deployed answer use')
    if (data['semantic_coverage_percent'] is not None
            or data['all_important_knowledge_covered'] is not False):
        raise ValueError('Requirements denominator is not book semantic coverage')
    if check_files:
        validate_code_trace(data)
        for row in by_id.values():
            for name in row['tests']['calculation_regressions'] + row['tests']['audit_integrity_tests']:
                if not (ROOT / name.split('::')[0]).is_file():
                    raise ValueError('Missing requirement test evidence')
    return True


def requirement_packet(requirement_id, database_path, data=None):
    data = load_requirements() if data is None else data
    validate_requirements(data)
    row = next((r for r in data['requirements'] if r['id'] == requirement_id), None)
    if not row:
        raise ValueError('Unknown atomic requirement: ' + requirement_id)
    # Source retrieval is independent of report membership: concepts can expose
    # an omitted dependency of the original section itself. Use an audit-only
    # section containing the requirement and its context, never approve it.
    inventory = load_inventory()
    inventory['report_sections'] = [dict(id='atomic-audit', title=row['title'],
        concept_ids=row['concept_ids'], rule_ids=[], required_chart_facts=row['required_chart_facts'], contexts=row['contexts'])] if row['concept_ids'] else inventory['report_sections']
    packets = [concept_packet(c, database_path, 'atomic-audit', inventory) for c in row['concept_ids']]
    return dict(scope='LOCAL_ATOMIC_REQUIREMENT_AUDIT', requirement=row,
        evidence_packets=packets, personal_answer_generated=False,
        missing_source_explicit=not bool(row['concept_ids']))
