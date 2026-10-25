"""Apply explicitly reviewed scan corrections without changing PDF witnesses."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'data/knowledge/source_review_updates.json'
    data = json.loads(path.read_text())
    links = {}
    def link(names, concepts):
        for name in names.split():
            links[name] = concepts.split()
    link('IMG_4658.jpg IMG_4659.jpg IMG_4660.jpg IMG_4661.jpg IMG_4662.jpg', 'directional-context spectrum-meanings forced-contact')
    link('IMG_4663.jpg IMG_4664.jpg', 'fringe-fca directional-context')
    link('IMG_4665.jpg IMG_4666.jpg IMG_4667.jpg', 'directional-context forced-contact natal-transit-order')
    link('IMG_4799.jpg IMG_4800.jpg', 'vantage-resolution directional-context')
    link('IMG_4814.jpg', 'forced-contact clusters directional-context')
    link('IMG_4913.jpg', 'quadrants free-theory house-field')
    link('IMG_4942.jpg', 'agency')
    link('IMG_4952.jpg IMG_4954.jpg IMG_4968.jpg', 'core-trinity')
    link('IMG_4958.jpg IMG_4959.jpg IMG_4960.jpg', 'cosmic-first natal-transit-order pass-through')
    link('IMG_4969.jpg IMG_4971.jpg', 'fringe-fca spark-entry core-trinity')
    link('IMG_5007.jpg IMG_5009.JPG', 'composite synastry')
    link('IMG_5084.JPG IMG_5085.JPG IMG_5086.JPG', 'sophia lunar-arcs lilith')
    link('IMG_5111.jpg IMG_5237.jpg', 'anchors')
    link('IMG_5282.jpg IMG_5283.jpg IMG_5284.JPG', 'chiron')
    link('IMG_5388.JPG IMG_5454.JPG', 'asteroid-elektra')
    link('IMG_5392.JPG IMG_5393.JPG IMG_5394.jpg IMG_5455.JPG', 'asteroid-eunomia')
    link('IMG_5394.jpg IMG_5395.JPG IMG_5455.JPG', 'asteroid-euphrosyne')
    # Mixed pages retain all relevant concept associations.
    links['IMG_5394.jpg'] = ['asteroid-eunomia', 'asteroid-euphrosyne']
    links['IMG_5455.JPG'] = ['asteroid-eunomia', 'asteroid-euphrosyne', 'asteroid-europa']
    link('IMG_5451.JPG', 'asteroid-vesta')
    data['concept_links'] = links
    data['source_questions'] = [
        dict(id='spark-parity', disposition='contradictory', concepts=['spark-entry'],
            finding='House parity is the explicit book procedure; conflicting sign-parity examples remain. Original510 preserves the mixed examples. No author erratum establishes precedence.',
            needed='Author-issued correction for original235,509-510,546 and authority of supplemental sign-parity specification.'),
        dict(id='fca-width-and-boundaries', disposition='contradictory', concepts=['fringe-fca'],
            finding='Original508 confirms 3 arcminutes at degree scale; original510 still includes Mars5:56, four arcminutes before6. After-boundary and retrograde weighting remain unspecified.',
            needed='Author correction for Mars example and explicit equality, first/last spill, after-boundary and retrograde conventions.'),
        dict(id='directional-ooi-catalog', disposition='source incomplete', concepts=['directional-context', 'spectrum-meanings'],
            finding='Original238-246 recover Sun10, Moon3, Mars4, approximately Saturn7.5 and Chiron1, diagrams and ecosystem distinctions. This is not a complete body/aspect catalog.',
            needed='Complete versioned outgoing catalog, aspect-specific limits and all receiving-point/exact-boundary exceptions.'),
        dict(id='pluto-arithmetic', disposition='resolved', concepts=['forced-contact'],
            finding='Original378 adds24:15+1:30=25:45 correctly. PDF343 substitutes24:42->25:42; the reported1-degree arithmetic is a compilation error.',
            needed='No further arithmetic clarification; do not conflate with remaining original coordinate conflict.'),
        dict(id='pluto-original-coordinate', disposition='contradictory', concepts=['forced-contact'],
            finding='Original378 earlier prose gives24:42, but figure and final arithmetic use24:15; opposite Moon25:57 changes reach depending on the starting coordinate.',
            needed='Author-confirmed Pluto starting coordinate and applicable chart/version.'),
        dict(id='sophia-original-617-619', disposition='resolved', concepts=['sophia'],
            finding='All three original pages recovered and visually reviewed. Original619 directly places corresponding mean/osculating points opposite Lilith. Selene substitution is expressly rejected.',
            needed='Source acquisition gap closed; independent numerical fixture/frame/speed comparison still needed before runtime implementation.'),
        dict(id='progression-original-491', disposition='resolved', concepts=['core-trinity'],
            finding='Original491 recovered; day-for-year relationship is explicitly described. Prior statement that no such mapping survived applies only to the compilation.',
            needed='Source acquisition gap for491 closed; exact units, angles and location coupling remain unresolved.'),
        dict(id='progression-original-492', disposition='inaccessible', concepts=['core-trinity'],
            finding='Original492 has not been located or acquired. Missing camera filename4953 does not prove printed492 is absent from every other image.',
            needed='Identify or supply a readable original492, then specify year/day/time-scale and angular advancement conventions.'),
        dict(id='chiron-jackson-degree', disposition='resolved', concepts=['chiron'],
            finding='Original687 figure shows19:18Rx, consistent with rounded original688 prose19. PDF568 description14:22Rx is a transcription error.',
            needed='No further degree-text correction; an independently timed chart fixture is still absent.'),
        dict(id='chiron-saturn-aspect', disposition='contradictory', concepts=['chiron'],
            finding='Original687 says sextile and original688 says trine. This disagreement is in the printed source.',
            needed='Author correction of the Saturn aspect and confirmed example chart epoch.'),
        dict(id='eunomia-two-meanings', disposition='contradictory', concepts=['asteroid-eunomia'],
            finding='Original712 explicitly rejects order while original772 assigns functional order. Both witnesses are printed originals; broader scope or precedence is not established.',
            needed='Author clarification or versioned erratum; preserve both meanings in retrieval.'),
        dict(id='asteroid-fragments-and-figures', disposition='source incomplete', concepts=['asteroid-elektra', 'asteroid-gonggong', 'asteroid-iris', 'asteroid-salacia', 'asteroid-sylvia'],
            finding='Elektra707 opening and771 comparison recovered. Other truncated chapters and the entire diagram inventory are not reconciled.',
            needed='Acquire and visually reconcile each fragmented chapter, tables and figures; hash and disposition every remaining scan.'),
        dict(id='activation-equality-wrap-retrograde', disposition='source incomplete', concepts=['age-degree', 'parts-mechanics', 'returns', 'profections', 'gradity-context'],
            finding='Formula arithmetic and actual ephemeris events do not settle interpretive equality, exact activation windows, return re-entry priorities or retrograde delay rules.',
            needed='Technique-specific, source-issued boundary rules and dated worked fixtures; do not reuse a universal orb or conventional astrology default.')
    ]
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    inventory_path = ROOT / 'data/knowledge/interpretive_inventory.json'
    inventory = json.loads(inventory_path.read_text())
    inventory['source_status_scope'] = 'COMPILED_PDF_PASSAGES_WITH_SEPARATE_ORIGINAL_SCAN_UPDATES'
    records = {r['id']:r for r in inventory['records']}
    continuation_path=ROOT/'data/knowledge/source_review_continuation.json'
    continuation=json.loads(continuation_path.read_text()) if continuation_path.exists() else {'source_only_concepts':[]}
    for item in continuation['source_only_concepts']:
        concept=item['id']
        row=dict(id=concept,title=concept.removeprefix('asteroid-').title()+' dedicated meaning',kind='meaning',
            contexts=['general'],source_status='PASSAGE_REVIEWED',meaning_summary=item['meaning_summary'],
            exceptions=['Source interpretation only; no literal personal history, diagnosis, deterministic forecast or empirical validation.',
                'Full house, ruler, motion and contact context remains required.'],
            report_gap='Dedicated original meaning recovered; contextual implementation and interpretation tests remain absent.',
            calculation_rule_ids=[],requires_concepts=['phsr'],runtime_interpretation='ABSENT',answer_use='NOT_APPROVED',
            witnesses=[],witness_scope='ORIGINAL_ONLY_NO_DEDICATED_COMPILED_MEANING')
        if concept in records:
            records[concept].update(row)
        else:
            inventory['records'].append(row)
            records[concept]=row
        section=next(s for s in inventory['report_sections'] if s['id']=='asteroid-detail')
        if concept not in section['concept_ids']:
            section['concept_ids'].append(concept)
    data['continuation_review_log']='data/knowledge/source_review_continuation.json'
    data['source_questions'].extend([
        dict(id='dedicated-four-meanings-originals',disposition='resolved',concepts=[r['id'] for r in continuation['source_only_concepts']],
            finding='Dedicated Flora720-721, Ixion734-735, Nessus749 and Sedna758-760 recovered and visually inspected. Source-location gaps closed; runtime interpretation remains absent.',
            needed='Contextual implementation and meaningful interpretation tests, preserving glossary variants and limitations.'),
        dict(id='anchor-receiver-and-activation',disposition='source incomplete',concepts=['anchors','directional-context'],
            finding='Original625 distinguishes natal association using the emitter OOI from exact transit activation, and says anchors do not emit.',
            needed='Exact-contact numerical tolerance, time scale, complete receiver catalog and independently verified events.'),
        dict(id='lunar-arc-order-and-wrap',disposition='source incomplete',concepts=['lunar-arcs','sophia','lilith'],
            finding='Original623-624 recovers first-endpoint trajectory and within-arc gradient regardless of OOI. Original620 links osculating Sophia retrograde to matching Lilith.',
            needed='Explicit directed/short-arc selection, wrap and endpoint equality, numerical frame/speed fixtures; no inferred convention.')])
    questions={q['id']:q for q in data['source_questions']}
    for identity,finding in {
        'spark-parity':'Original234 explicitly develops sign parity, while original235 explicitly instructs house parity. Original509 and511 preserve examples inconsistent with the house candidate. Original510 and composite546 counterexamples remain linked; no source-issued precedence is established.',
        'fca-width-and-boundaries':'Original508 three-arcminute rule and510 Mars5:56 conflict remain. Original732 now visually confirms Interamnia0:12 Virgo H2 blending H1/H2 from H2. This recovers post-boundary evidence without settling weighting, equality or retrograde rules.',
        'asteroid-fragments-and-figures':'Targeted original review now recovers Elektra708 closing, Gonggong725-726, Iris732-733, Salacia756-758 and Sylvia760-762, alongside additional chapters and comparative entries. Original-to-PDF mapping and all-diagram/line-level reconciliation remain incomplete.'
    }.items():
        questions[identity]['historical_finding_before_pipeline']=questions[identity]['finding']
        questions[identity]['finding']=finding
        questions[identity]['continuation_evidence']='data/knowledge/source_review_continuation.json'
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    notes = {
        'sophia': 'Original617-619 recovered in targeted scan review: matching mean/osculating Sophia is directly opposite matching Lilith. Full numerical fixture and arc selection remain unverified. Retain PDF fragments as historical compilation witnesses.',
        'core-trinity': 'Original491 explicitly describes day-for-year progression and simultaneous natal/progressed/relocated reference. Original492 is still unlocated; exact units, angle method and relocation coupling are not settled.',
        'chiron': 'Original687 diagram shows19:18Rx, resolving the PDF14:22 transcription discrepancy. Original687 sextile versus688 trine remains contradictory.',
        'forced-contact': 'Original378 uses24:15->25:45 for1.5-degree reach; PDF343 changes these values. Original prose24:42 versus figure24:15 remains a starting-coordinate conflict.',
        'asteroid-eunomia': 'Original712 rejects order and original772 assigns functional order. Original scan review confirms competing claims; do not silently merge or select by majority.',
        'asteroid-elektra': 'Original707 chapter opening and771 comparison recovered: coordination of hidden complexity and invisible labor. Full chapter/context review is still incomplete.'}
    for id, note in notes.items():
        records[id]['original_scan_update'] = note
    records['asteroid-eunomia']['source_status'] = 'CONFLICT'
    blocker_path=ROOT/'data/knowledge/source_blocker_findings.json'
    if blocker_path.exists():
        for finding in json.loads(blocker_path.read_text())['findings']:
            if finding['id'] in questions:
                question=questions[finding['id']]
                question['historical_finding_before_full_queue']=question['finding']
                question['finding']=finding['finding']
                question['needed']=finding['remaining']
                question['line_reconciliation_status']=finding['status']
                question['line_reconciliation_evidence']='data/knowledge/source_blocker_findings.json#'+finding['id']
            for concept in finding['concept_ids']:
                records[concept].setdefault('line_reconciliation_finding_ids',[])
                if finding['id'] not in records[concept]['line_reconciliation_finding_ids']:
                    records[concept]['line_reconciliation_finding_ids'].append(finding['id'])
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    # Do not erase historical source assertions or promote runtime/readiness.
    inventory_path.write_text(json.dumps(inventory, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    examples_path = ROOT / 'data/knowledge/worked_examples.json'
    examples = json.loads(examples_path.read_text())
    for example in examples['examples']:
        if example['id'] == 'pluto-ooi-counterexample':
            example['original_scan_correction'] = dict(original_page='378', scan='IMG_4814.jpg',
                actual_interval=['24:15', '25:45'], earlier_original_prose='24:42',
                disposition='PDF_ARITHMETIC_TRANSCRIPTION_ERROR_ORIGINAL_COORDINATE_CONFLICT_REMAINS')
        if example['id'] == 'chiron-jackson-values':
            example['original_scan_correction'] = dict(original_pages=['687','688'], scans=['IMG_5282.jpg','IMG_5283.jpg'],
                original_diagram='19:18 Rx', disposition='PDF_DEGREE_ERROR_RESOLVED_ORIGINAL_ASPECT_CONFLICT_REMAINS')
    examples_path.write_text(json.dumps(examples, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    manifest_path = ROOT / 'data/knowledge/source_manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        register_path = ROOT / 'data/knowledge/capabilities.json'
        register = json.loads(register_path.read_text())
        snapshot = {b['folder_id']: b for b in manifest['batches']}
        for batch in register['source_inventory']['batches']:
            batch['known_files'] = snapshot[batch['id']]['observed_count']
            batch['visible_listing_snapshot_complete'] = True
            batch['enumeration_complete'] = False
            batch['enumeration_scope_note'] = 'Visible browser direct-child endpoint reached; provider revision freeze and full page accounting remain unestablished.'
        register['source_inventory']['visible_snapshot_manifest'] = 'data/knowledge/source_manifest.json'
        register['source_inventory']['visible_file_records_including_loose_root'] = manifest['file_record_denominator']
        register['source_inventory']['printed_page_denominator'] = None
        register['source_inventory']['original_scan_corrections'] = 'data/knowledge/source_review_updates.json'
        for rule in register['rules']:
            if rule['id'] in ('N9-025','N9-033','N9-038'):
                rule['original_scan_followup'] = 'data/knowledge/source_review_updates.json#source_questions'
        register_path.write_text(json.dumps(register, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
