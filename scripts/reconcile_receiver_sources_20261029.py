"""Record the targeted original-page review; no complete method approval."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/knowledge'


def read(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))


def save(name, data):
    (BASE / name).write_text(json.dumps(data, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')


def main():
    manifest = read('source_manifest.json')
    files = {r['name'].lower(): r for b in manifest['batches'] for r in b['files']}
    continuation = read('source_review_continuation.json')
    reviewed = {r['file_id'] for r in continuation['reviews']}
    summaries = {
        208: ('delegate-condition directional-context', 'The worked Aquarius Moon/H7 carries Cancer/H12 and its North Node before forward reference to Uranus. Interpretive point notation is not physical emission.'),
        209: ('delegate-condition', 'Delegate condition includes all ruled-area contents, not merely a forward sign-ruler chain. A terminal or self-ruled planet is not a dominating final ruler.'),
        210: ('delegate-condition', 'Assess each layer before carrying its context through the ruler. Gemini Rising puts Cancer in H2; Moon carries that actual sector while retaining its own function.'),
        211: ('objective-context delegate-condition', 'A question-specific Lens considers the whole chart. H7 alone is partner/relating context, not a complete love reading; H10 alone is not a complete career reading.'),
        212: ('objective-context delegate-condition', 'The Lens continuation requires the whole chart and distinguishes relationship subtopics across different houses. Topic relevance is not a fixed single-house classification.'),
    }
    new_ids = []
    for page, (concepts, summary) in summaries.items():
        row = files[f'img_{page + 4421}.jpg']
        assert hashlib.sha256((ROOT / row['local_path']).read_bytes()).hexdigest() == row['content_sha256']
        if row['file_id'] in reviewed:
            continue
        assert row['visual_review_status'] == 'NOT_REVIEWED'
        row.update(printed_page_ids=[str(page)], printed_page_basis='VISUAL_HEADER',
            visible_page_count=1, visual_review_status='TARGETED_ORIGINAL_VISUAL_REVIEW',
            semantic_review_status='TARGETED_PASSAGE_REVIEW_NOT_EXHAUSTIVE',
            scan_to_pdf_status='ORIGINAL_PASSAGE_NOT_LOCATED_BY_CANDIDATE_SEARCH',
            candidate_pdf_pages=[], disposition=summary,
            review_evidence='data/knowledge/source_review_continuation.json#' + row['file_id'])
        continuation['reviews'].append(dict(file_id=row['file_id'], name=row['name'],
            content_sha256=row['content_sha256'], printed_page_ids=[str(page)],
            printed_page_basis='VISUAL_HEADER', concept_ids=concepts.split(), summary=summary,
            pdf_pages=[], candidate_pdf_overlaps=[],
            reconciliation_status='ORIGINAL_PASSAGE_NOT_LOCATED_BY_CANDIDATE_SEARCH',
            visual_review_scope='COMPLETE_PAGE_VISUAL_READING_TARGETED_SEMANTICS_NOT_FULL_TRANSCRIPTION',
            image_quality='TARGET_PASSAGES_READABLE_PHOTOGRAPH',
            duplicate_content_status='NO_DUPLICATE_CLAIM', visible_page_count=1,
            semantic_status='TARGETED_PASSAGE_RECONCILIATION_NOT_EXHAUSTIVE'))
        new_ids.append(row['file_id'])
    save('source_manifest.json', manifest)
    save('source_review_continuation.json', continuation)
    assertions = read('original_assertions.json')
    known = {r['id'] for r in assertions['assertions']}
    before_assertions = len(known)
    declarations = [
        ('delegate208-reverse-sector-occupants', 'delegate-condition', [208], 'The worked Moon condition includes its ruled Cancer sector and that sector North Node before following the Moon Aquarius ruler.', 'Worked topology only; no autobiography transfer or mathematical-point emission rule.'),
        ('delegate209-no-final-ruler', 'delegate-condition', [209], 'A Delegate carries ruled-area contents; a terminal, self-ruled or repeated planet is not a controlling final ruler.', 'Complete condition is still required; graph repetition does not multiply strength.'),
        ('delegate210-layer-before-carriage', 'delegate-condition', [210], 'Assess each layer energies and variables before carrying its precise context through its ruler.', 'Structural prerequisite, not a complete synthesis algorithm or a personal outcome.'),
        ('delegate210-gemini-cancer-house-example', 'delegate-condition', [210], 'Gemini Rising places Cancer in H2, so Moon carries that actual sector alongside its own function.', 'Whole Sign topology fixture; not a universal Moon/money or Venus/H2 assignment.'),
        ('lens211-whole-chart-context', 'objective-context', [211, 212], 'A question Lens adjusts relevance across the whole chart; H7 alone is partner/relating context rather than a complete relationship reading.', 'No rigid one-house reading, strength ranking or empirical accuracy claim.'),
        ('conjunction240241-core-reach', 'directional-context', [240, 241], 'The within-ecosystem conjunction examples test each planet reach to the other exact coordinate. A wider reach can connect the pair when the narrower one cannot; overlap of radii alone does not make direct conjunction.', 'Saturn7.5 is approximate; exact OOI boundary ownership, interpretive order, other aspect caps and Fringe synthesis are not supplied by these examples.'),
        ('transit245-no-natal-outgoing', 'directional-context', [245], 'When reading transits, natal OOI is not added or emitted outward into the current sky; receiving response is distinct from physical initiation.', 'Between-ecosystem physical direction; does not equate interpretive notation with emission or complete a transit model.'),
        ('conjunction373-mutual-endpoints', 'directional-context', [373], 'The True Stellium example requires mutual reach between the first and last planets and separately notes a smaller-radius middle Moon may not reach an endpoint.', 'A connected chain is not proof that every pair is mutually connected; this example does not complete general cluster interpretation.'),
    ]
    for identity, concept, pages, proposition, limit in declarations:
        if identity in known:
            continue
        witnesses = []
        for page in pages:
            filename = {373: 'img_4809.jpg'}.get(page, f'img_{page + 4421}.jpg')
            row = files[filename]
            assert row['visual_review_status'] == 'TARGETED_ORIGINAL_VISUAL_REVIEW'
            assert hashlib.sha256((ROOT / row['local_path']).read_bytes()).hexdigest() == row['content_sha256']
            witnesses.append(dict(file_id=row['file_id'], name=row['name'],
                content_sha256=row['content_sha256'], original_printed_pages=row['printed_page_ids']))
        assertions['assertions'].append(dict(id=identity, concept_id=concept,
            kind='SOURCE_CONTEXT_AND_NUMERIC_EXAMPLE', proposition=proposition,
            applicability='Only the stated source context; preserve incomplete calculation/interpretive prerequisites.',
            exclusions_and_limits=[limit], witnesses=witnesses,
            requires_concepts=['delegate-condition', 'directional-context'] if concept == 'objective-context' else [],
            authority='ORIGINAL_BATCH_SCAN_TARGETED_REVIEW', execution_status='NOT_EXECUTABLE_NOT_RUNTIME_APPROVED',
            interpretation_validation='SOURCE_FAITHFULNESS_ONLY_NOT_EMPIRICAL_VALIDATION', answer_use='NOT_APPROVED'))
    save('original_assertions.json', assertions)
    continued_assertions = {r['id'] for r in continuation['assertions']}
    declared_ids = {r[0] for r in declarations}
    continuation['assertions'].extend(r for r in assertions['assertions']
        if r['id'] in declared_ids and r['id'] not in continued_assertions)
    save('source_review_continuation.json', continuation)
    print(json.dumps({'new_targeted_original_ids': new_ids, 'new_assertions': len(assertions['assertions']) - before_assertions,
        'total_assertions': len(assertions['assertions']), 'full_report_approved': False}))


if __name__ == '__main__':
    main()
