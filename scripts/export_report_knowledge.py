"""Export saved audit knowledge losslessly for branch-aware external readers.

This packages existing source records. It never approves a personal report,
adds interpretations, or includes private source images, PDF, OCR or indexes.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.report_components import usage_catalog
BRANCH = 'codex/phsr-numerology-integration-20261028'
REPOSITORY = 'https://github.com/olsonan26/mystic-rebels-chart-generator'
SOURCES = {
    'concepts': 'interpretive_inventory.json',
    'assertions': 'original_assertions.json',
    'requirements': 'material_requirements.json',
    'findings': 'source_blocker_findings.json',
    'capabilities': 'capabilities.json',
    'worked_examples': 'worked_examples.json',
    'annotations': 'source_line_annotations.json',
    'initial_original_reviews': 'source_review_updates.json',
    'continuation_original_reviews': 'source_review_continuation.json',
    'meaning_profiles': 'source_meaning_profiles.json',
    'relationship_profiles': 'relationship_rule_profiles.json',
}


def encode(value):
    return (json.dumps(value, ensure_ascii=True, indent=2) + '\n').encode('utf-8')


def build():
    documents, authorities = {}, {}
    for key, name in SOURCES.items():
        path = 'data/knowledge/' + name
        raw = (ROOT / path).read_bytes()
        documents[key] = json.loads(raw)
        normalized=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n').encode('utf-8')
        authorities[key] = dict(path=path, sha256=hashlib.sha256(normalized).hexdigest(),
            hash_normalization='UTF8_UNIVERSAL_NEWLINES')
    records = documents['concepts']['records']
    ids = {r['id'] for r in records}
    assertions = documents['assertions']['assertions']
    findings = documents['findings']['findings']
    requirements = documents['requirements']['requirements']
    assert all(a['concept_id'] in ids and a.get('witnesses') for a in assertions)
    assert all(a['answer_use'] == 'NOT_APPROVED' for a in assertions)
    assert not any(r.get('personal_answer_approved') for r in requirements)
    assert all(set(f['concept_ids']) <= ids for f in findings)
    counts = dict(concepts=len(records), assertions=len(assertions),
        requirements=len(requirements), findings=len(findings),
        capabilities=len(documents['capabilities']['rules']),
        worked_examples=len(documents['worked_examples']['examples']),
        annotations=len(documents['annotations']['annotations']),
        initial_review_records=len(documents['initial_original_reviews']['reviews']),
        continuation_review_records=len(documents['continuation_original_reviews']['reviews']),
        report_sections=len(documents['concepts']['report_sections']), ready_report_sections=0)
    contract = dict(scope='SAVED_SOURCE_AUDIT_KNOWLEDGE_NOT_APPROVED_PERSONAL_REPORT_RULES',
        required_repository=REPOSITORY, required_ref=BRANCH,
        default_branch_main_contains_this_knowledge=False,
        all_important_knowledge_covered=False,
        personal_answer_approved=False, empirical_accuracy_validated=False,
        private_originals_pdf_ocr_indexes_included=False,
        canonical_json_is_authority=True,
        source_reference_use_allowed=True,
        eligible_chart_vocabulary_annotations_allowed=True,
        personal_interpretation_approval_is_separate=True,
        external_library_fallback_allowed=False,
        rules=[
            'Read meaning_summary together with exceptions, dependencies, witnesses and linked findings.',
            'Preserve every applicable original assertion and contradictory witness; never rank conflicts away.',
            'Resolve report-section transitive dependencies and required chart facts before synthesis.',
            'Source vocabulary and exact calculations do not establish empirical outcome accuracy.',
            'NOT_APPROVED blocks unvalidated personal interpretation, not attributed source reading or eligible vocabulary annotations. Use the component-use catalog; never override execution or complete-report gates.',
            'An author anecdote is not a fact about a report user; do not invent personal history or health conclusions.',
            'Replace existing-library meanings for source-covered signs,Chiron and Eunomia; never fill missing or conflicting material from generic astrology or a model prior.',
            'A GitHub-only export retains reviewed text and citation metadata, not independently inspectable source media.',
        ])
    routes = {
        'planets': [r['id'] for r in records if r['id'].startswith('meaning-') or r['id'] in ('planet-lexicon','planet-categories')],
        'houses': ['house-field'] + [r['id'] for r in records if r['id'].startswith('field-')],
        'sign_degree_decan_context': ['tone-pulse','spark-entry','phsr','house-field'],
        'cusps': ['fringe-fca','anchors'],
        'aspects': ['spectrum-meanings','directional-context','vantage-resolution','handoff','forced-contact','block-color','free-theory','clusters'],
        'asteroids': ['chiron'] + [r['id'] for r in records if r['id'].startswith('asteroid-')],
        'report_context': ['objective-context','agency','core-trinity','delegate-condition'],
    }
    assert all(set(v) <= ids for v in routes.values())
    bundle = dict(schema_version='1.0', contract=contract, counts=counts,
        topic_routes=routes,
        coverage_limits=dict(
            signs='All twelve original sign core entries are recovered in source_meaning_profiles.json; full sign/ruler/aspect synthesis is not approved by core vocabulary coverage.',
            keywords='Reviewed meaning_summary/proposition/review text contains vocabulary. These are contextual source summaries, not unrestricted keyword-to-personality rules.',
            outstanding='Unreviewed images, failed OCR and unresolved semantic/numerical conflicts remain; consult the current audit checkpoint and exact queues for counts.',
            implementation='Bounded chat and partial source-bound condition/reach components exist; complete report synthesis and all 18 full report sections remain unready.'),
        authorities=authorities, documents=documents)
    catalog=usage_catalog(documents['concepts'],documents['assertions'],documents['findings'],documents['meaning_profiles'])
    catalog_path='data/knowledge/report_component_use.json'
    catalog_bytes=encode(catalog)
    bundle_path='data/knowledge/report_knowledge_bundle.json'
    manifest=dict(schema_version='1.0',contract=contract,counts=counts,topic_routes=routes,
        bundle=dict(path=bundle_path,sha256=hashlib.sha256(encode(bundle)).hexdigest()),
        authorities=authorities,
        start_here='REPORT_KNOWLEDGE_START_HERE.md',
        full_history='docs/PROFILE_REPORT_KNOWLEDGE_PATH.md',
        source_checkpoint='evidence/source-pipeline/closing-next-verification.json',
        rebuild_command='python scripts/export_report_knowledge.py',
        check_command='python scripts/export_report_knowledge.py --check')
    manifest['component_use']=dict(path=catalog_path,sha256=hashlib.sha256(catalog_bytes).hexdigest(),
        counts=catalog['counts'],source_reference_use_allowed=True,
        core_sign_entries_present=catalog['core_sign_entries_present'],external_library_fallback_allowed=False,
        annotation_command='python scripts/annotate_chart_sources.py examples/report-source-input.json --format markdown',
        personal_report_approved=False)
    manifest['reviewed_meaning_profiles']=authorities['meaning_profiles']
    outputs={bundle_path:encode(bundle),catalog_path:catalog_bytes}
    by_id={r['id']:r for r in records}
    manifest['topic_packets']={}
    for topic, initial in routes.items():
        selected=set(initial)
        while True:
            expanded=selected.union(*(set(by_id[i]['requires_concepts']) for i in selected))
            expanded.update(d for a in assertions if a['concept_id'] in selected for d in a.get('requires_concepts',[]))
            if expanded==selected:break
            selected=expanded
        chosen_assertions=[a for a in assertions if a['concept_id'] in selected]
        chosen_findings=[f for f in findings if selected.intersection(f['concept_ids'])]
        packet=dict(schema_version='1.0',contract=contract,topic=topic,
            initial_concept_ids=initial,transitive_concept_ids=sorted(selected),
            concepts=[r for r in records if r['id'] in selected],
            assertions=chosen_assertions,findings=chosen_findings,
            reviewed_meaning_profiles=[p for p in documents['meaning_profiles']['profiles'] if p['source_concept_id'] in selected],
            requirement_references=[dict(id=r['id'],section_id=r['section_id'],
                disposition=r['disposition'],personal_answer_approved=r['personal_answer_approved'])
                for r in requirements if selected.intersection(r.get('concept_ids',[]))],
            requirement_authority=authorities['requirements'],
            relationship_component_authority=authorities['relationship_profiles'],
            relationship_components=documents['relationship_profiles'] if topic in ('aspects', 'report_context') else None,
            annotation_authority=authorities['annotations'],
            media_limit='Only reviewed text and witness metadata; private source media/indexes are not included.')
        path='data/knowledge/report_topics/'+topic+'.json'
        outputs[path]=encode(packet)
        manifest['topic_packets'][topic]=dict(path=path,bytes=len(outputs[path]),
            sha256=hashlib.sha256(outputs[path]).hexdigest(),concepts=len(selected),
            assertions=len(chosen_assertions),findings=len(chosen_findings))
        assert len(outputs[path])<1000000, 'Topic exceeds ordinary small-file ingestion limit: '+topic
    manifest['bulk_bundle_note']='Bulk download; smaller topic_packets are provided for bounded connector ingestion.'
    outputs['data/knowledge/report_knowledge_manifest.json']=encode(manifest)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    outputs=build()
    for path, raw in outputs.items():
        if args.check:
            if not (ROOT/path).is_file() or (ROOT/path).read_bytes()!=raw:
                raise SystemExit('Stale/missing knowledge export: '+path+'; regenerate before ingestion.')
        else:
            (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
            (ROOT/path).write_bytes(raw)
    print(json.dumps(dict(status='VERIFIED_LOSSLESS_CURRENT_EXPORT' if args.check else 'EXPORTED_EXISTING_AUDIT_RECORDS',
        files={p:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for p,raw in outputs.items()},
        personal_answer_approved=False)))


if __name__=='__main__':
    main()
