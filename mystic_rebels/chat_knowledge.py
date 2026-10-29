"""Question-focused source packets; source reference never becomes rule approval."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re

from knowledge_audit.report_components import usage_catalog
from .relationship_context import validate_profile

ROOT = Path(__file__).resolve().parents[1]
AUTHORITIES = ('concepts', 'assertions', 'findings', 'requirements', 'meaning_profiles', 'relationship_profiles')
FOUNDATION = ('objective-context', 'agency', 'phsr', 'planet-lexicon', 'house-field',
              'tone-pulse', 'spark-entry', 'delegate-condition', 'directional-context')
TOPICS = {
    'relationships': ('relationship partner marriage dating love intimacy trust boundaries',
                      ('field-07', 'field-08', 'meaning-venus', 'chiron')),
    'family': ('family father dad mother mom parent childhood home',
               ('field-04', 'meaning-sun', 'meaning-moon')),
    'work': ('work job career vocation business purpose',
             ('field-06', 'field-10', 'meaning-saturn', 'meaning-sun')),
    'resources': ('money finance income resources worth value',
                  ('field-02', 'field-08', 'meaning-venus')),
    'voice': ('voice communication speak writing thoughts learning',
              ('field-03', 'meaning-mercury', 'meaning-moon')),
    'current': ('now current today yesterday tomorrow transit week month year future timing when',
                ('natal-transit-order', 'with-while', 'pass-through', 'vantage-resolution')),
}


def tokens(value):
    words = set(re.findall(r'[a-z]{3,}', value.lower()))
    words.update(word[:-1] for word in list(words) if word.endswith('s') and len(word) > 4)
    return words - {
        'the', 'and', 'with', 'what', 'does', 'this', 'that', 'have', 'about',
        'chart', 'want', 'know', 'tell', 'please', 'from', 'your', 'there', 'would', 'could'}


@lru_cache(maxsize=2)
def _load(root_name, stamps):
    root = Path(root_name)
    manifest_path = root / 'data/knowledge/report_knowledge_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    data, hashes = {}, {}
    for key in AUTHORITIES:
        ref = manifest['authorities'][key]
        path = (root / ref['path']).resolve()
        if not path.is_relative_to((root / 'data/knowledge').resolve()):
            raise ValueError('Knowledge authority path is invalid')
        text = path.read_text(encoding='utf-8')  # universal newline normalization
        sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if ref['hash_normalization'] != 'UTF8_UNIVERSAL_NEWLINES' or sha != ref['sha256']:
            raise ValueError('Knowledge authority changed; rebuild the portable export')
        data[key], hashes[key] = json.loads(text), sha
    validate_profile(data['relationship_profiles'], data['assertions'])
    catalog = usage_catalog(data['concepts'], data['assertions'], data['findings'], data['meaning_profiles'])
    return data, {r['concept_id']: r for r in catalog['components']}, {
        'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'authority_hashes': hashes, 'normalization': 'UTF8_UNIVERSAL_NEWLINES'}


def authorities():
    paths = [ROOT / 'data/knowledge/report_knowledge_manifest.json']
    manifest = json.loads(paths[0].read_text(encoding='utf-8'))
    paths += [ROOT / manifest['authorities'][k]['path'] for k in AUTHORITIES]
    return _load(str(ROOT.resolve()), tuple((p.stat().st_size, p.stat().st_mtime_ns) for p in paths))


def question_packet(question, chart, history=()):
    data, catalog, fingerprint = authorities()
    records = {r['id']: r for r in data['concepts']['records']}
    profiles = {r['concept_id']: r for r in data['meaning_profiles']['profiles']}
    # A short follow-up retains the user's preceding topic; assistant wording is
    # never used to promote a hypothesis into source or chart evidence.
    query = tokens(question + ' ' + ' '.join(t['content'] for t in history[-4:] if t['role'] == 'user'))
    selected, roots = [], set(FOUNDATION)
    # Every numeric/structural rule sent to the writer retains its original
    # assertion and concept dependencies, even in a short follow-up.
    profile = data['relationship_profiles']
    profile_assertions = {a for row in [*profile['numeric_reach'].values(), profile['conjunction'], profile['receiver_context']]
                          for a in row['assertion_ids']}
    roots.update(a['concept_id'] for a in data['assertions']['assertions'] if a['id'] in profile_assertions)
    for match in re.finditer(r'\b(?:house\s*(1[0-2]|[1-9])|(1[0-2]|[1-9])(?:st|nd|rd|th)\s+house)\b', question, re.I):
        roots.add(f'field-{int(match.group(1) or match.group(2)):02d}')
    for name, (words, ids) in TOPICS.items():
        if query & tokens(words):
            selected.append(name)
            roots.update(ids)
    points = [p for p in chart['points'] if p.get('available')]
    for p in points:
        identity = next((k for k in ('meaning-' + p['id'].lower(), 'asteroid-' + p['id'].lower(), p['id'].lower()) if k in records), None)
        if identity:
            roots.add(identity)
        if p.get('house'):
            roots.add(f'field-{p["house"]:02d}')
        roots.update('sign-' + p[k].lower() for k in ('tone', 'pulse'))
    scored = sorted(((len(query & tokens(r['title'] + ' ' + r['meaning_summary'])), r['id'])
                     for r in records.values()), reverse=True)
    roots.update(identity for score, identity in scored[:5] if score)
    # Include only relevant section contracts, rather than every section that
    # happens to share a foundational dependency such as planet-lexicon.
    sections = data['requirements']['sections']
    section_ids = {s.get('section_id', s.get('id')) for s in sections
                   if query & tokens(str(s.get('title', '')) + ' ' + str(s.get('section_id', s.get('id', ''))))}
    section_ids.add('profile-foundation')
    requirements = [r for r in data['requirements']['requirements'] if r['section_id'] in section_ids
                    and (not r['id'].startswith('M01-02-') or set(r['concept_ids']) & roots)]
    for row in requirements:
        roots.update(row['concept_ids'] + row.get('dependency_concept_ids', []))
    chosen, visiting = set(), set()

    def visit(identity):
        if identity in chosen:
            return
        if identity in visiting:
            raise ValueError('Cyclic source dependencies')
        visiting.add(identity)
        if identity in profiles:
            profile = profiles[identity]
            dependencies = (profile['dependencies'] + [profile['source_concept_id']]
                            + records.get(identity, {}).get('requires_concepts', []))
        elif identity in records:
            dependencies = records[identity]['requires_concepts']
        else:
            raise ValueError('Missing source dependency: ' + identity)
        for dependency in dependencies:
            if dependency != identity:
                visit(dependency)
        chosen.add(identity)
        visiting.remove(identity)

    for identity in sorted(roots):
        visit(identity)
    # Original assertions have their own prerequisites, beyond inventory closure.
    while True:
        previous = len(chosen)
        claims = [a for a in data['assertions']['assertions'] if a['concept_id'] in chosen]
        for claim in claims:
            for dependency in claim.get('requires_concepts', []):
                visit(dependency)
        if len(chosen) == previous:
            break
    ledger = {}

    def citation(witness):
        metadata = {k: v for k, v in witness.items() if k not in ('proposition', 'assertion_id')}
        identity = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode()).hexdigest()[:24]
        ledger[identity] = metadata
        result = {'witness_ref': identity}
        if witness.get('assertion_id'):
            result['assertion_id'] = witness['assertion_id']
        return result

    components = []
    for identity in sorted(chosen):
        c = catalog[identity]
        components.append({k: c.get(k) for k in (
            'concept_id', 'title', 'source_meaning', 'source_status', 'use_status',
            'chart_vocabulary_annotation_allowed', 'chart_alternatives_annotation_allowed',
            'personal_trait_claim_allowed', 'completed_personal_report_approved',
            'exceptions', 'dependencies', 'report_gap', 'citations', 'alternatives')})
        components[-1]['citations'] = [citation(w) for w in c.get('citations', [])]
    assertions = [{k: a.get(k) for k in (
        'id', 'concept_id', 'proposition', 'applicability', 'exclusions_and_limits',
        'requires_concepts', 'witnesses', 'execution_status', 'answer_use')} for a in claims]
    for assertion in assertions:
        assertion['witnesses'] = [citation(w) for w in assertion['witnesses']]
    findings = [f for f in data['findings']['findings'] if set(f['concept_ids']) & chosen]
    requirements = [{k: r.get(k) for k in (
        'id', 'section_id', 'title', 'concept_ids', 'dependency_concept_ids',
        'required_chart_facts', 'disposition', 'remaining_work', 'personal_answer_approved')} for r in requirements]
    return {'selection': {'topics': selected, 'roots': sorted(roots),
                          'purpose': 'QUESTION_RELEVANCE_NOT_PLANETARY_STRENGTH'},
            'components': components, 'assertions': assertions, 'findings': findings,
            'witness_ledger': ledger,
            'requirements': requirements, 'fingerprint': fingerprint,
            'relationship_profiles': data['relationship_profiles'],
            'external_library_fallback_allowed': False,
            'complete_personal_report_approved': False,
            'selected_sequence': 'Planet -> House -> Degree -> Decan -> Aspects -> Sign -> Ruler',
            'sequence_variation': 'Original chapter216 puts Aspects before Sign; lexicon u puts Sign before Aspect. Chapter sequence selected; both witnesses retained.',
            'additional_audit_limits': ['Original503 scenarioB lists SunH5 but retains an H4 parenthesis; source conflict remains unresolved.',
                'Lexicon ae Velocity Focus is source-only: no executable peak/acceleration method is approved.']}
