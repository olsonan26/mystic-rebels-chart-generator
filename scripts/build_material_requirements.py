"""Expand every original missing-context cell into separately accountable tasks.

Declarations below are analyst-authored requirements, not inferred domain rules.
The original 18-row table is preserved verbatim and hashed. Generated stage
evidence never upgrades source statements into implemented interpretations.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_audit.registry import load_registry
from knowledge_audit.semantics import load_inventory, _closure
from knowledge_audit.sources import original_witnesses, atomic_assertions
from knowledge_audit.requirements import code_trace_hash

# Entries are grouped in exactly the same order as comma-separated fragments
# in the original table. A slash/compound can require several independent tasks.
# Each atomic item is title :: directly relevant concept IDs :: disposition.
SPECS = [
    ['PHSR+ ordered assembler::phsr',
     '@VOCABULARY',
     'Rising templates::templates', 'Canonical Spark parity::spark-entry::contradictory',
     'Personal dialogue and known-fact separation::objective-context agency'],
    ['Incoming directed relationships::directional-context; Outgoing directed relationships::directional-context',
     'Receiving placement and ruler condition::directional-context delegate-condition',
     'Delegate payload preservation::delegate-condition; Delegate cycles and multiple responsibilities::delegate-condition'],
    ['Empty-house meaning::empty-house',
     'House ruler condition::delegate-condition; Each occupant condition::phsr retrograde-meaning',
     'Multiple concurrent house themes::intra-house', 'Delegate retrograde house context::retrograded-house'],
    ['Body-specific natal retrograde meaning::retrograde-meaning; Body-specific transit retrograde meaning::retrograde-meaning natal-transit-order',
     'Sequential double retrograde reading::double-retrograde', 'Modern-ruler template exceptions::retrograded-house templates'],
    ['Complete approved per-body OOI catalog::directional-context::source incomplete; Directed contact graph::directional-context::source incomplete',
     'Forced response versus initiation::forced-contact', 'Conjunction hand-off::handoff; Opposition 180 hand-off::handoff',
     'Aspect-specific spectrum bands::spectrum-meanings::source incomplete; Aspect spectrum meanings::spectrum-meanings',
     'Fringe overlap meaning and transit activation::fringe-fca::source incomplete; FCA before-boundary thresholds::fringe-fca::contradictory; FCA after-boundary exceptions::fringe-fca::source incomplete; FCA retrograde handling::fringe-fca::source incomplete',
     'Rolling clusters and forced members::clusters::source incomplete'],
    ['Ascendant anchor meaning::anchors; Descendant anchor meaning::anchors; Midheaven anchor meaning::anchors; IC anchor meaning::anchors; Nonagesimal potential::nonagesimals; Subnonagesimal potential::nonagesimals',
     'Invertex reset and re-entry::invertex; Vertex overextension and visibility::vertex', 'Axial Flow loop::axial-flow',
     'Full participating rulers::delegate-condition; Full participating contacts::directional-context'],
    ['Fortune ordered formula meaning::fortune parts-mechanics; Spirit ordered formula meaning::spirit parts-mechanics; Love ordered formula meaning::love parts-mechanics',
     'Ordered operand conditions::parts-mechanics delegate-condition', 'Exact Part activation convention::parts-mechanics::source incomplete',
     'Trigger process::parts-mechanics; Point expression::parts-mechanics'],
    ['Mean and true node integration::nodes; Node interpretive ordering::nodes',
     'Mean Lilith meaning::lilith; Osculating Lilith meaning::lilith',
     'Lilith arc filter::lunar-arcs::source incomplete; Sophia arc filter::lunar-arcs::source incomplete',
     'Mean Sophia construction::sophia::source found but implementation missing; Osculating Sophia construction::sophia::source found but implementation missing'],
    ['North declination meaning::declination::source found but implementation missing; South declination meaning::declination::source found but implementation missing',
     'Approved parallel tolerance::declination::source incomplete', 'Out-of-bounds interpretation::declination::source found but implementation missing'],
    ['FREE Theory house relationships::free-theory', 'Vantage and reverse perspective::vantage-resolution',
     'Threading relationships::free-theory directional-context; Trigger selection::free-theory directional-context',
     'STQ entry and resolution order::stq', 'Intra-house balancing::intra-house'],
    ['@ALL_BODIES', '@FRAGMENTS', 'Body-specific full conditions::phsr delegate-condition; Additional-body outgoing OOIs::directional-context::source incomplete'],
    ['Sky-to-sky condition before overlay::cosmic-first', 'Personal sky overlay::natal-transit-order',
     'Transit sender and natal receiver::natal-transit-order forced-contact; Natal response without physical reverse emission::natal-transit-order forced-contact',
     'Pass-through without direct contact::pass-through', 'Connected WITH context::with-while; Concurrent WHILE context::with-while'],
    ['Vernal first lived equinox::profections::source incomplete', 'Twelve-year cycle overlay::profections::source incomplete',
     'Timing equality and ingress boundary ownership::profections age-degree::source incomplete; Timing longitude wrap::age-degree::source incomplete',
     'Fractional age-degree dates::age-degree::source incomplete', 'Retrograde activation delays::age-degree::source incomplete'],
    ['Progression planetary epoch mapping::core-trinity::source incomplete; Progression angular advancement::core-trinity::source incomplete; Progression time-scale and year-day units::core-trinity::source incomplete',
     'Explicit natal-versus-relocated comparison::relocation core-trinity', 'Three-layer simultaneous context::core-trinity::source incomplete'],
    ['Return phase selection::returns::source incomplete; Retrograde re-entry precedence::returns::source incomplete; Exact return phase boundary ownership::returns::source incomplete',
     'Retain natal linkage in each phase::returns', 'Concurrent luminary resonance::returns cosmic-first::source incomplete'],
    ['Person A full condition::synastry phsr; Person B full condition::synastry phsr; Person A chart layers::synastry core-trinity::source incomplete; Person B chart layers::synastry core-trinity::source incomplete',
     'A-to-B asymmetric reach::synastry directional-context; B-to-A asymmetric reach::synastry directional-context',
     'A into B house overlay::synastry; B into A house overlay::synastry',
     'Composite midpoint construction and wrap::composite::source incomplete; Composite antipodal ambiguity::composite::source incomplete; Composite joint entity meaning::composite'],
    ['Relocation comparison workflow::relocation', 'Parans horizon frame and simultaneous events::parans::source incomplete',
     'Location distance attenuation::parans::source incomplete; Location intensity interpretation::parans::source incomplete',
     'Local Space journey origin::local-space; Local Space origin history::local-space'],
    ['Electional context and verified event choice::election-horary::source incomplete; Horary question origin and scope::election-horary::source incomplete',
     'Source-specific eclipse taxonomy::eclipse::source incomplete', 'Derivative chart retains natural chart::derivatives',
     'Epoch anchoring and versioned hierarchy::epoch-imprint::source incomplete', 'Rectification objective and uncertainty::rectification::source incomplete',
     'Explicit rejected techniques::exclusions; Explicit unfinished theories::exclusions']
]


def table_rows():
    text = (ROOT / 'docs/INTERPRETIVE_COVERAGE_AUDIT.md').read_text(encoding='utf-8')
    rows = []
    for line in text.splitlines():
        if not line.startswith('| ') or line.startswith('| Report section'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 3:
            rows.append(cells)
        if len(rows) == 18:
            break
    if len(rows) != 18:
        raise ValueError('Original 18-section table changed or unavailable')
    return rows


def main():
    inventory = load_inventory()
    records = {r['id']: r for r in inventory['records']}
    all_originals = original_witnesses(list(records))
    all_assertions = atomic_assertions(list(records))
    registry = load_registry()
    rules = {r['id']: r for r in registry['rules']}
    source_rows = table_rows()
    trace_paths = ['mystic_rebels/api.py', 'mystic_rebels/service.py', 'mystic_rebels/models.py',
                   'mystic_rebels/catalog.py', 'mystic_rebels/placements.py', 'web/src/App.tsx',
                   'web/src/MethodVerification.tsx', '.vercelignore']
    code_trace = [dict(path=p, sha256=code_trace_hash(p, 'COMMITTED_HEAD'),
                       hash_normalization='UTF8_UNIVERSAL_NEWLINES') for p in trace_paths]
    sections, requirements = [], []
    component_path = ROOT / 'data/knowledge/relationship_rule_profiles.json'
    component_progress = json.loads(component_path.read_text(encoding='utf-8'))['requirement_progress'] if component_path.exists() else {}
    examples = json.loads((ROOT / 'data/knowledge/worked_examples.json').read_text())['examples']
    for index, (cells, spec, section) in enumerate(zip(source_rows, SPECS, inventory['report_sections']), 1):
        fragments = cells[2].split(', ')
        if len(fragments) != len(spec):
            raise ValueError(f'Unreconciled fragments in {cells[0]}: {fragments}')
        original_fragments = []
        for fi, (fragment, declarations) in enumerate(zip(fragments, spec), 1):
            if declarations == '@VOCABULARY':
                declarations = '; '.join(r['title'] + '::' + r['id']
                    for r in inventory['records'] if r['id'].startswith(('meaning-', 'field-')))
                profile_path=ROOT/'data/knowledge/source_meaning_profiles.json'
                covered={p.get('sign') for p in json.loads(profile_path.read_text())['profiles'] if p['kind']=='sign'} if profile_path.exists() else set()
                declarations += '; ' + '; '.join(sign + ' sign vocabulary::tone-pulse::'+('source found but implementation missing' if sign in covered else 'source incomplete')
                    for sign in ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'])
                declarations += '; Degree entry meaning::spark-entry::contradictory; Decan layer meaning::tone-pulse'
            if declarations == '@ALL_BODIES':
                declarations = '; '.join(r['title'] + '::' + r['id']
                    for r in inventory['records'] if (r['id'] == 'chiron' or r['id'].startswith('asteroid-'))
                    and r['id'] not in {'asteroid-flora','asteroid-nessus','asteroid-ixion','asteroid-sedna'})
                # Preserve the original requirement IDs and order as source gaps close.
                declarations += '; ' + '; '.join(name + ' dedicated meaning::asteroid-' + name.lower()
                    for name in ['Flora', 'Nessus', 'Ixion', 'Sedna'])
            if declarations == '@FRAGMENTS':
                declarations = '; '.join('Recover ' + name + ' chapter and figures::asteroid-' + name.lower() + '::source incomplete'
                    for name in ['Elektra', 'Eros', 'Gonggong', 'Iris', 'Salacia', 'Sylvia', 'Hygiea', 'Metis', 'Orcus', 'Pallas'])
            ids = []
            for ai, declaration in enumerate(declarations.split('; '), 1):
                parts = declaration.split('::')
                title, concept_text = parts[:2]
                concepts = concept_text.split()
                if any(c not in records for c in concepts):
                    raise ValueError('Unknown direct concept in ' + declaration)
                status = parts[2] if len(parts) > 2 else None
                if not status:
                    states = {records[c]['source_status'] for c in concepts}
                    status = ('inaccessible' if not concepts else 'contradictory' if states & {'CONFLICT', 'SEMANTIC_TENSION'}
                              else 'source incomplete' if states - {'PASSAGE_REVIEWED'}
                              else 'source found but implementation missing')
                rid = f'M{index:02d}-{fi:02d}-{ai:02d}'
                ids.append(rid)
                transitive = _closure(records, concepts)
                rule_ids = sorted({r for c in transitive for r in records[c]['calculation_rule_ids']})
                witnesses = {w['pdf_page']: w for c in concepts for w in records[c]['witnesses']}
                originals = [w for w in all_originals if set(w['linked_concept_ids']) & set(concepts)]
                related_examples = [e['id'] for e in examples if e['concept_id'] in concepts]
                relevant_tests = sorted({t for r in rule_ids for t in rules[r]['verification_tests']})
                requirements.append(dict(id=rid, section_id=section['id'], original_fragment=fragment,
                    title=title, record_kind='ATOMIC_REQUIREMENT_NOT_AN_APPROVED_INTERPRETATION',
                    concept_ids=concepts, dependency_concept_ids=[c for c in transitive if c not in concepts],
                    contexts=section['contexts'], required_chart_facts=section['required_chart_facts'],
                    source_witnesses=[witnesses[p] for p in sorted(witnesses)], original_scan_witnesses=originals,
                    original_atomic_assertion_ids=[a['id'] for a in all_assertions if a['concept_id'] in concepts],
                    applicability='Only in the listed chart context; dependencies and exclusions must be evaluated before personal use.',
                    exclusions=[e for c in concepts for e in records[c]['exceptions']],
                    structured_meaning_status='CITED_THEMATIC_SUMMARY_AND_ATOMIC_REQUIREMENT' if concepts else 'ABSENT',
                    calculation_evidence=[dict(rule_id=r, status=rules[r]['implementation_status'],
                        files=rules[r]['implementation_files'], tests=rules[r]['verification_tests'],
                        limitation='Calculation or diagnostic tests do not validate this interpretation.') for r in rule_ids],
                    code_trace_ids=trace_paths,
                    implementation_evidence=dict(
                        source_present='COMPILED_AND_TARGETED_ORIGINAL' if originals and witnesses else 'TARGETED_ORIGINAL_ONLY' if originals else 'COMPILED_ONLY' if concepts else 'NO_VERIFIED_DEDICATED_WITNESS',
                        original_visually_reviewed='TARGETED_NOT_ALL_WITNESSES' if originals else 'NOT_ESTABLISHED_FOR_REQUIREMENT',
                        deterministic_calculation='SEE_SEPARATE_CALCULATION_EVIDENCE_NOT_INTERPRETATION',
                        context_dependencies='NOT_IMPLEMENTED_AS_COMPLETE_INTERPRETER',
                        locally_retrievable='REQUIREMENT_AND_ALL_LINKED_WITNESSES' if concepts else 'REQUIREMENT_GAP_ONLY',
                        deployed_retrieval='NO_ANSWER_RETRIEVAL_PATH_IN_INSPECTED_SOURCE',
                        actual_report_use='ABSENT_IN_INSPECTED_SOURCE',
                        live_behavior='NOT_AUTHENTICATED_OR_VERIFIED_IN_THIS_CONTINUATION'),
                    tests=dict(source_examples=related_examples, calculation_regressions=relevant_tests,
                        interpretation_regressions=[], audit_integrity_tests=['astronomy_qa/test_material_requirements.py'],
                        required_behavior=f'For {title}, retain every cited exclusion and competing witness; require all context dependencies; abstain when source or facts are unavailable.'),
                    disposition=status,
                    remaining_work=('Identify a dedicated original source witness and represent its meaning before implementation.' if not concepts else
                        'Implement and test the complete contextual meaning after resolving the recorded source questions; numerical support alone does not close this requirement.'),
                    personal_answer_approved=False))
                if rid in component_progress:
                    requirements[-1]['partial_component_evidence'] = dict(
                        source_profile='data/knowledge/relationship_rule_profiles.json',
                        progress=component_progress[rid],
                        implementation_files=['mystic_rebels/relationship_context.py', 'mystic_rebels/chat_context.py'],
                        component_tests=['astronomy_qa/test_relationship_context.py'],
                        complete_requirement_resolved=False,
                        actual_report_use_scope='The existing ABSENT field refers to complete section synthesis, not these bounded chat components.')
            original_fragments.append(dict(text=fragment, atomic_requirement_ids=ids))
        sections.append(dict(index=index, section_id=section['id'], original_title=cells[0],
            original_existing_support=cells[1], original_missing_context=cells[2], fragments=original_fragments,
            disposition='NOT_READY_FOR_PERSONAL_REPORT'))
    data = dict(schema_version='1.0', scope='ROW_BY_ROW_ORIGINAL_18_SECTION_RECONCILIATION',
        audit_date_local='2026-10-25', source_table_sha256=hashlib.sha256(json.dumps(source_rows, separators=(',', ':')).encode()).hexdigest(),
        source_table_path='docs/INTERPRETIVE_COVERAGE_AUDIT.md',
        semantic_coverage_percent=None, all_important_knowledge_covered=False,
        code_trace_basis='COMMITTED_HEAD', code_trace=code_trace, sections=sections, requirements=requirements)
    output = ROOT / 'data/knowledge/material_requirements.json'
    output.write_text(json.dumps(data, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    lines = ['# Original 18-section material-context reconciliation', '',
        'This reconciles every comma-separated fragment and its compound requirements against the original table. '
        'It is a requirements denominator, not the denominator of all knowledge in the book. '
        'No section is ready for a personal report. Original scans and compiled witnesses remain separately identified.', '',
        '| Original section | Original fragments | Atomic tasks | Dispositions |', '|---|---:|---:|---|']
    for section in sections:
        rs = [r for r in requirements if r['section_id'] == section['section_id']]
        counts = Counter(r['disposition'] for r in rs)
        lines.append(f"| {section['original_title']} | {len(section['fragments'])} | {len(rs)} | " + '; '.join(f'{k}: {v}' for k, v in sorted(counts.items())) + ' |')
    lines += ['', 'The machine-readable ledger includes source/page hashes, original scan IDs/hashes, dependencies, '
        'calculation files/tests, inspected product paths, separate retrieval/report-use stages, selected examples and missing interpretation tests for each task.', '',
        '| Task | Original fragment | Atomic requirement | Witnesses | Disposition |', '|---|---|---|---|---|']
    for r in requirements:
        pdfs = ','.join(str(w['pdf_page']) for w in r['source_witnesses'])
        scans = ','.join(w['original_printed_page'] for w in r['original_scan_witnesses'])
        lines.append(f"| {r['id']} | {r['original_fragment']} | {r['title']} | PDF {pdfs or 'none'}; original {scans or 'not reviewed'} | {r['disposition']} |")
    (ROOT / 'docs/MATERIAL_CONTEXT_RECONCILIATION.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(sections=len(sections), original_fragments=sum(len(s['fragments']) for s in sections),
        atomic_requirements=len(requirements), dispositions=Counter(r['disposition'] for r in requirements))))


if __name__ == '__main__':
    main()
