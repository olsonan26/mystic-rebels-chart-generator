"""Reconcile authored visual observations, never infer review from OCR or a queue.

The complete frozen assignment must have one hash-bound analyst review per ID.
Source summaries and assertions remain separate from runtime/report approval.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path('docs/research-20261029/remaining-scans')
GROUPS = ('foundations', 'middle', 'later')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')


def load_reviews(root=ROOT):
    assignments, reviews = {}, {}
    for group in GROUPS:
        assignment = read(root / RESEARCH / 'assignments' / (group + '.json'))
        if assignment['assigned_count'] != len(assignment['files']):
            raise ValueError('Assignment count changed: ' + group)
        local = {r['file_id']: {**r, '_review_group': group} for r in assignment['files']}
        if len(local) != len(assignment['files']) or set(local) & assignments.keys():
            raise ValueError('Duplicate assignment identity')
        assignments.update(local)
        observations = root / RESEARCH / (group + '-reviews.jsonl')
        records = [json.loads(line) for line in observations.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
        if len(records) != len(local) or {r['file_id'] for r in records} != set(local):
            raise ValueError('Incomplete or duplicated visual review: ' + group)
        reviews.update({r['file_id']: r for r in records})
    if len(assignments) != 299 or len(reviews) != 299:
        raise ValueError('Frozen remaining assignment must retain all 299 IDs')
    return assignments, reviews


def validate_review(review, original, concepts, root=ROOT, check_image=True):
    for field in ('file_id', 'name', 'content_sha256'):
        if review.get(field) != original[field]:
            raise ValueError('Visual observation lost original identity: ' + field)
    if check_image:
        path = (root / original['local_path']).resolve()
        if not path.is_relative_to((root / 'reference/originals').resolve()):
            raise ValueError('Original image outside private source directory')
        if hashlib.sha256(path.read_bytes()).hexdigest() != original['content_sha256']:
            raise ValueError('Original photograph bytes changed')
    if review.get('source_status') not in ('READABLE_TARGETED_REVIEW', 'PARTIAL_UNREADABLE'):
        raise ValueError('An OCR/extraction status cannot establish visual review')
    if (not isinstance(review.get('summary'), str) or len(review['summary']) < 60
            or not isinstance(review.get('concept_ids'), list)
            or not review['concept_ids'] or set(review['concept_ids']) - concepts):
        raise ValueError('Visual review needs substantive known-concept context')
    pages = review.get('printed_page_ids')
    if not isinstance(pages, list) or not all(isinstance(p, str) and p.strip() for p in pages):
        raise ValueError('Invalid observed printed headers')
    if review.get('printed_page_basis') not in ('VISUAL_HEADER', 'UNPAGINATED', 'HEADER_UNCLEAR'):
        raise ValueError('Printed header needs an explicit visual basis')
    if review['printed_page_basis'] == 'VISUAL_HEADER' and not pages:
        raise ValueError('A visually read printed header cannot be empty')
    if type(review.get('visible_page_count')) is not int or not 1 <= review['visible_page_count'] <= 4:
        raise ValueError('Visible page count must be inspected')
    for field in ('visual_observations', 'assertion_candidates', 'uncertainties'):
        if not isinstance(review.get(field), list):
            raise ValueError('Visual review lost evidence/uncertainty fields')
    if review['source_status'] == 'PARTIAL_UNREADABLE':
        if not review['uncertainties']:
            raise ValueError('An unreadable observation needs its actual limitation')
        if review['assertion_candidates']:
            raise ValueError('Unreadable source cannot establish new assertions')
    for assertion in review['assertion_candidates']:
        if (assertion.get('concept_id') not in concepts or not assertion.get('proposition')
                or not assertion.get('applicability') or not assertion.get('exclusions_and_limits')):
            raise ValueError('Assertion candidate lacks scoped source context')
        if not isinstance(assertion['exclusions_and_limits'], list):
            raise ValueError('Assertion limits must remain an explicit list')
        if not re.fullmatch('[a-zA-Z0-9_-]+', assertion.get('id', '')):
            raise ValueError('Assertion candidate needs a stable ID')
        if any(assertion.get(k) for k in ('personal_answer_approved', 'runtime_approved', 'full_method_approved')):
            raise ValueError('Source extraction cannot grant personal/runtime approval')
    return True


def reconcile(manifest, continuation, assertions, reviews, assignments, concepts, pdf_candidates):
    """Pure reconciliation; original bytes and authored records validated first."""
    manifest, continuation, assertions = map(deepcopy, (manifest, continuation, assertions))
    rows = {r['file_id']: r for b in manifest['batches'] for r in b['files']}
    rows.update({r['file_id']: r for r in manifest['loose_root_files']})
    continued = {r['file_id']: r for r in continuation['reviews']}
    known_assertions = {a['id']: a for a in assertions['assertions']}
    baseline_ids = set(known_assertions)
    newly_reviewed, unreadable = [], []
    for file_id, review in reviews.items():
        row = rows[file_id]
        validate_review(review, assignments[file_id], concepts, check_image=False)
        if row['content_sha256'] != review['content_sha256']:
            raise ValueError('Canonical manifest differs from inspected bytes')
        analyst_record = (RESEARCH / (assignments[file_id]['_review_group'] + '-reviews.jsonl')).as_posix()
        if review['source_status'] == 'PARTIAL_UNREADABLE':
            # Preserve the real inspection and replacement need without turning
            # unreadable material into a reviewed semantic witness.
            row.update(visual_review_status='ORIGINAL_IMAGE_INSPECTED_UNREADABLE',
                semantic_review_status='UNREADABLE_REQUIRES_REPLACEMENT',
                printed_page_ids=review['printed_page_ids'], printed_page_basis=review['printed_page_basis'],
                visible_page_count=review['visible_page_count'], multi_page_image_status='VISUALLY_INSPECTED',
                disposition=review['summary'], review_evidence=analyst_record + '#' + file_id)
            unreadable.append(file_id)
            continue
        pages = review['printed_page_ids'] or ['UNKNOWN_' + review['printed_page_basis']]
        candidates = pdf_candidates.get(file_id, [])
        pdf_pages = sorted({c['pdf_page'] for c in candidates})
        status = ('CANDIDATE_TEXT_OVERLAP_NOT_COMPLETE_ALIGNMENT' if pdf_pages
                  else 'ORIGINAL_PASSAGE_NOT_LOCATED_BY_CANDIDATE_SEARCH')
        record = dict(file_id=file_id, name=row['name'], content_sha256=row['content_sha256'],
            printed_page_ids=pages, printed_page_basis=review['printed_page_basis'],
            concept_ids=review['concept_ids'], summary=review['summary'],
            pdf_pages=pdf_pages, candidate_pdf_overlaps=candidates, reconciliation_status=status,
            visual_review_scope='COMPLETE_ORIGINAL_IMAGE_VISUAL_INSPECTION_TARGETED_SEMANTICS_NOT_LINE_TRANSCRIPTION',
            image_quality=review['image_quality'], duplicate_content_status='NO_DUPLICATE_CONTENT_CLAIM',
            visible_page_count=review['visible_page_count'],
            semantic_status='TARGETED_PASSAGE_RECONCILIATION_NOT_EXHAUSTIVE',
            visual_observations=review['visual_observations'], unresolved_observations=review['uncertainties'],
            source_status=review['source_status'],
            analyst_record=analyst_record)
        if file_id in continued:
            if continued[file_id] != record:
                raise ValueError('Existing review differs; reconcile explicitly: ' + file_id)
        else:
            if row['visual_review_status'] != 'NOT_REVIEWED':
                raise ValueError('Assignment unexpectedly replaces prior review')
            continuation['reviews'].append(record)
            newly_reviewed.append(file_id)
        row.update(printed_page_ids=pages, printed_page_basis=review['printed_page_basis'],
            visible_page_count=review['visible_page_count'], multi_page_image_status='VISUALLY_INSPECTED',
            visual_review_status='TARGETED_ORIGINAL_VISUAL_REVIEW',
            semantic_review_status='TARGETED_PASSAGE_REVIEW_NOT_EXHAUSTIVE',
            candidate_pdf_pages=pdf_pages, scan_to_pdf_status=status,
            disposition=review['summary'], review_evidence='data/knowledge/source_review_continuation.json#' + file_id)
        for candidate in review['assertion_candidates']:
            identity = 'remaining-20261029-' + candidate['id']
            witness = dict(file_id=file_id, name=row['name'], content_sha256=row['content_sha256'], original_printed_pages=pages)
            assertion = dict(id=identity, concept_id=candidate['concept_id'], kind='SOURCE_BOUND_VISUAL_REVIEW_PARAPHRASE',
                proposition=candidate['proposition'], applicability=candidate['applicability'],
                exclusions_and_limits=candidate['exclusions_and_limits'], witnesses=[witness], requires_concepts=[],
                authority='ORIGINAL_BATCH_SCAN_TARGETED_REVIEW', execution_status='NOT_EXECUTABLE_NOT_RUNTIME_APPROVED',
                interpretation_validation='SOURCE_FAITHFULNESS_ONLY_NOT_EMPIRICAL_VALIDATION', answer_use='NOT_APPROVED')
            if identity in known_assertions:
                prior = known_assertions[identity]
                if {k: v for k, v in prior.items() if k != 'witnesses'} != {k: v for k, v in assertion.items() if k != 'witnesses'}:
                    raise ValueError('Competing assertions share an ID: ' + identity)
                if witness not in prior['witnesses']:
                    prior['witnesses'].append(witness)
            else:
                assertions['assertions'].append(assertion)
                known_assertions[identity] = assertion
    old_continued = {a['id']: a for a in continuation['assertions']}
    for identity, assertion in known_assertions.items():
        if identity.startswith('remaining-20261029-'):
            if identity in old_continued:
                continuation['assertions'][continuation['assertions'].index(old_continued[identity])] = deepcopy(assertion)
            else:
                continuation['assertions'].append(deepcopy(assertion))
    receipt = dict(schema_version='remaining-scans-reconciliation-v1', assigned=299,
        reviewed_records=len(reviews), newly_reviewed_originals=len(newly_reviewed),
        inspected_unreadable_ids=unreadable, unreadable_source_approved=False,
        source_statuses=dict(Counter(r['source_status'] for r in reviews.values())),
        new_assertions=len(set(known_assertions) - baseline_ids), total_assertions=len(known_assertions),
        full_method_approved=False, personal_report_approved=False, all_important_knowledge_covered=False,
        ocr_locator_signoffs_added=0, pdf_alignment_approved=False)
    return manifest, continuation, assertions, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate all observations without canonical writes')
    args = parser.parse_args()
    assignments, reviews = load_reviews()
    concepts = {r['id'] for r in read(ROOT / 'data/knowledge/interpretive_inventory.json')['records']}
    for identity, review in reviews.items():
        validate_review(review, assignments[identity], concepts)
    manifest, continuation, assertions, receipt = reconcile(
        read(ROOT / 'data/knowledge/source_manifest.json'),
        read(ROOT / 'data/knowledge/source_review_continuation.json'),
        read(ROOT / 'data/knowledge/original_assertions.json'), reviews, assignments, concepts,
        read(ROOT / RESEARCH / 'pdf-candidates.json')['files'])
    if not args.check:
        for name, data in [('source_manifest.json', manifest), ('source_review_continuation.json', continuation), ('original_assertions.json', assertions)]:
            save(ROOT / 'data/knowledge' / name, data)
        save(ROOT / RESEARCH / 'reconciliation.json', receipt)
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
