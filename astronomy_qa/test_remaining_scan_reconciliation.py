"""Review provenance must survive reconciliation without implying approval."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('remaining_reconciliation', ROOT / 'scripts/reconcile_remaining_scans_20261029.py')
reconcile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconcile)


def fixture():
    original = dict(file_id='original-id', name='page.jpg', content_sha256='a' * 64,
        local_path='reference/originals/original-id.jpg', visual_review_status='NOT_REVIEWED',
        _review_group='later')
    review = dict(file_id='original-id', name='page.jpg', content_sha256='a' * 64,
        printed_page_ids=['251'], printed_page_basis='VISUAL_HEADER', visible_page_count=1,
        image_quality='Full original photograph inspected.', concept_ids=['age-activation'],
        summary='The original distinguishes the documented age-degree example from a universal event or timing algorithm.',
        visual_observations=['Diagram labels distinguish the fixed coordinate from a later event.'],
        assertion_candidates=[dict(id='example-scope', concept_id='age-activation',
            proposition='The documented activation is an example with a delayed manifestation.',
            applicability='This worked example only.', exclusions_and_limits=['No universal delay rule established.'])],
        uncertainties=[], source_status='READABLE_TARGETED_REVIEW')
    return original, review


def run(original, review, manifest=None, continuation=None, assertions=None):
    return reconcile.reconcile(manifest or {'batches': [{'files': [original]}], 'loose_root_files': []},
        continuation or {'reviews': [], 'assertions': []}, assertions or {'assertions': []},
        {original['file_id']: review}, {original['file_id']: original}, {'age-activation'},
        {original['file_id']: [{'pdf_page': 71, 'overlap': .5, 'status': 'OCR_TRIGRAM_CANDIDATE_NOT_ALIGNMENT_APPROVAL'}]})


def test_inspected_original_is_idempotent_with_scoped_assertion_and_candidate_pdf():
    original, review = fixture()
    m, c, a, receipt = run(original, review)
    assert m['batches'][0]['files'][0]['visual_review_status'] == 'TARGETED_ORIGINAL_VISUAL_REVIEW'
    assert c['reviews'][0]['reconciliation_status'] == 'CANDIDATE_TEXT_OVERLAP_NOT_COMPLETE_ALIGNMENT'
    assert c['reviews'][0]['visual_observations'] == review['visual_observations']
    assert a['assertions'][0]['witnesses'][0]['content_sha256'] == original['content_sha256']
    assert a['assertions'][0]['answer_use'] == 'NOT_APPROVED'
    assert not receipt['full_method_approved'] and receipt['ocr_locator_signoffs_added'] == 0
    m2, c2, a2, again = run(original, review, m, c, a)
    assert (m2, c2, a2) == (m, c, a)
    assert again['new_assertions'] == again['newly_reviewed_originals'] == 0


def test_unreadable_photograph_is_preserved_without_semantic_or_assertion_approval():
    original, review = fixture()
    review.update(source_status='PARTIAL_UNREADABLE', printed_page_ids=[], printed_page_basis='HEADER_UNCLEAR',
        assertion_candidates=[], uncertainties=['Motion blur prevents reading the header and body.'])
    m, c, a, receipt = run(original, review)
    row = m['batches'][0]['files'][0]
    assert row['visual_review_status'] == 'ORIGINAL_IMAGE_INSPECTED_UNREADABLE'
    assert row['semantic_review_status'] == 'UNREADABLE_REQUIRES_REPLACEMENT'
    assert not c['reviews'] and not a['assertions']
    assert receipt['inspected_unreadable_ids'] == [original['file_id']]
    assert not receipt['unreadable_source_approved']


@pytest.mark.parametrize('mutation, message', [
    ({'content_sha256': 'b' * 64}, 'original identity'),
    ({'source_status': 'OCR_EXTRACTED_CANDIDATE'}, 'OCR/extraction'),
    ({'concept_ids': ['invented']}, 'known-concept'),
    ({'printed_page_ids': []}, 'cannot be empty'),
    ({'visible_page_count': True}, 'page count'),
    ({'source_status': 'PARTIAL_UNREADABLE', 'uncertainties': ['blur']}, 'new assertions'),
])
def test_rejects_fabricated_review_authority(mutation, message):
    original, review = fixture()
    review.update(mutation)
    with pytest.raises(ValueError, match=message):
        reconcile.validate_review(review, original, {'age-activation'}, check_image=False)


def test_exact_image_bytes_are_required_when_source_available(tmp_path):
    import hashlib
    original, review = fixture()
    p = tmp_path / original['local_path']
    p.parent.mkdir(parents=True)
    p.write_bytes(b'original image fixture')
    original['content_sha256'] = review['content_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    assert reconcile.validate_review(review, original, {'age-activation'}, root=tmp_path)
    p.write_bytes(b'changed')
    with pytest.raises(ValueError, match='photograph bytes changed'):
        reconcile.validate_review(review, original, {'age-activation'}, root=tmp_path)


def test_competing_assertion_id_cannot_silently_replace_old_text():
    original, review = fixture()
    m, c, a, _ = run(original, review)
    a['assertions'][0]['proposition'] = 'An incompatible claimed rule.'
    with pytest.raises(ValueError, match='Competing assertions'):
        run(original, review, m, c, a)


def test_incomplete_frozen_queue_cannot_be_marked_reconciled(tmp_path):
    for group, n in [('foundations', 100), ('middle', 95), ('later', 104)]:
        p = tmp_path / reconcile.RESEARCH
        (p / 'assignments').mkdir(parents=True, exist_ok=True)
        rows = [{'file_id': group + str(i)} for i in range(n)]
        (p / 'assignments' / (group + '.json')).write_text(json.dumps({'assigned_count': n, 'files': rows}))
        (p / (group + '-reviews.jsonl')).write_text('')
    with pytest.raises(ValueError, match='Incomplete or duplicated'):
        reconcile.load_reviews(tmp_path)
