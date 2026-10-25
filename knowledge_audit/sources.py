"""Validate source accounting without turning file enumeration into page coverage."""
import hashlib
import json
import re
from pathlib import Path

from .registry import ROOT

MANIFEST = ROOT / 'data/knowledge/source_manifest.json'


def load_manifest(path=MANIFEST):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def validate_manifest(data=None, check_files=True):
    data = load_manifest() if data is None else data
    if data['scope'] != 'VISIBLE_DRIVE_DIRECT_CHILDREN_SNAPSHOT':
        raise ValueError('Unknown source inventory scope')
    batches = data['batches']
    if (len(batches) != 8 or len({b['folder_id'] for b in batches}) != 8
            or {b['name'] for b in batches} != {f'BATCH {i}' for i in range(1, 9)}):
        raise ValueError('Eight distinct original batches required')
    all_ids = set()
    for batch in batches:
        rows = batch['files']
        ids = [r['file_id'] for r in rows]
        if len(ids) != len(set(ids)) or set(ids) & all_ids:
            raise ValueError('Duplicate file identity in batch inventory')
        all_ids.update(ids)
        if (batch['observed_count'] != len(rows)
                or batch['observed_indices'] != list(range(1, len(rows) + 1))
                or batch['grid_rowcount'] != len(rows)):
            raise ValueError('Incomplete or inconsistent visible listing endpoint')
        if check_files:
            evidence = ROOT / batch['listing_evidence']['path']
            if hashlib.sha256(evidence.read_text(encoding='utf-8').encode()).hexdigest() != batch['listing_evidence']['sha256']:
                raise ValueError('Listing evidence changed')
        for row in rows:
            if not row['name'] or not row['file_id'] or not row['mime_type']:
                raise ValueError('Missing source file identity')
            digest = row['content_sha256']
            acquired = row['acquisition_status'] == 'ACQUIRED_HASHED'
            if acquired != bool(digest) or (digest and not re.fullmatch('[0-9a-f]{64}', digest)):
                raise ValueError('Acquisition requires actual content hash')
            if row['visual_review_status'] == 'TARGETED_ORIGINAL_VISUAL_REVIEW':
                if not acquired or not row['printed_page_ids'] or not row['review_evidence']:
                    raise ValueError('Visual review lacks an acquired original witness')
            if row['semantic_review_status'] == 'COMPLETE':
                raise ValueError('Targeted review cannot establish exhaustive semantics')
            if check_files and acquired:
                path = ROOT / row['local_path']
                # Original bytes are intentionally private/ignored and may not
                # exist in CI. Verify whenever this checkout has the asset.
                if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise ValueError('Original source bytes changed')
    root = data['loose_root_files']
    # Loose originals have the same integrity obligations as batched originals.
    for row in root:
        acquired = row['acquisition_status'] == 'ACQUIRED_HASHED'
        if acquired != bool(row['content_sha256']):
            raise ValueError('Loose acquisition requires actual content hash')
        if acquired and check_files:
            path = ROOT / row['local_path']
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != row['content_sha256']:
                raise ValueError('Loose original source bytes changed')
    for row in [r for b in batches for r in b['files']] + root:
        if row['ocr_status'] == 'OCR_EXTRACTED_CANDIDATE':
            if not row['content_sha256'] or row.get('ocr_source_sha256') != row['content_sha256']:
                raise ValueError('OCR lost original source identity')
            if not row.get('ocr_output_sha256') or not row.get('ocr_path'):
                raise ValueError('OCR output lacks provenance')
            output = ROOT / row['ocr_path']
            if check_files and output.exists() and hashlib.sha256(output.read_bytes()).hexdigest() != row['ocr_output_sha256']:
                raise ValueError('OCR output bytes changed')
    if any(r['file_id'] in all_ids for r in root):
        raise ValueError('Loose root file counted twice')
    total = len(all_ids) + len(root)
    if data['file_record_denominator'] != total:
        raise ValueError('File record denominator mismatch')
    if (data['printed_page_denominator'] is not None
            or data['all_original_pages_semantically_reviewed'] is not False
            or data['complete_scan_to_pdf_reconciliation'] is not False
            or data['semantic_coverage_percent'] is not None):
        raise ValueError('File enumeration is not complete page or semantic coverage')
    return True


def original_witnesses(concept_ids, manifest=None, updates=None):
    """Return every explicitly linked original, never replace competing PDF text."""
    manifest = load_manifest() if manifest is None else manifest
    validate_manifest(manifest)
    updates = (json.loads((ROOT / 'data/knowledge/source_review_updates.json').read_text())
               if updates is None else updates)
    rows = {r['name'].casefold(): r for b in manifest['batches'] for r in b['files']
            if r['visual_review_status'] == 'TARGETED_ORIGINAL_VISUAL_REVIEW'}
    reviews = {r[0]: r for r in updates['reviews']}
    continuation_path = ROOT / 'data/knowledge/source_review_continuation.json'
    continuation = json.loads(continuation_path.read_text()) if continuation_path.exists() else {'reviews': []}
    continued = {r['file_id']:r for r in continuation['reviews']}
    result = []
    for name, linked in updates['concept_links'].items():
        if not set(linked) & set(concept_ids):
            continue
        row = rows.get(name.casefold())
        review = reviews.get(name)
        followup=continued.get(row['file_id'],{}) if row else {}
        current_matches_followup=bool(row and followup and
            followup.get('content_sha256')==row['content_sha256'] and
            followup.get('printed_page_ids')==row['printed_page_ids'] and
            followup.get('summary')==row['disposition'] and followup.get('pdf_pages')==row['candidate_pdf_pages'])
        if (not row or not review or row['printed_page_ids'] != [review[1]] or
                (not current_matches_followup and
                 (row['disposition'] != review[4] or row['candidate_pdf_pages'] != review[2]))):
            raise ValueError('Original review/manifest mapping mismatch: ' + name)
        result.append(dict(file_id=row['file_id'], name=row['name'],
            source_authority='ORIGINAL_BATCH_PHOTOGRAPH', content_sha256=row['content_sha256'],
            local_path=row['local_path'], original_printed_page=review[1],
            pdf_pages=review[2], reflow_footer=None,
            reconciliation_status=review[3], review_summary=review[4],
            linked_concept_ids=linked, use='AUDIT_WITNESS_NOT_REPORT_APPROVAL'))
    files = {r['file_id']: r for b in manifest['batches'] for r in b['files']}
    files.update({r['file_id']: r for r in manifest['loose_root_files']})
    for review in continuation['reviews']:
        linked = review['concept_ids']
        if not set(linked) & set(concept_ids):
            continue
        row = files[review['file_id']]
        if (row['content_sha256'] != review['content_sha256'] or row['printed_page_ids'] != review['printed_page_ids']
                or row['visual_review_status'] != 'TARGETED_ORIGINAL_VISUAL_REVIEW'):
            raise ValueError('Continuation review/manifest mapping mismatch')
        result.append(dict(file_id=row['file_id'], name=row['name'],
            source_authority='ORIGINAL_BATCH_PHOTOGRAPH', content_sha256=row['content_sha256'],
            local_path=row['local_path'], original_printed_page=', '.join(review['printed_page_ids']),
            pdf_pages=review['pdf_pages'], reflow_footer=None,
            reconciliation_status=review['reconciliation_status'], review_summary=review['summary'],
            linked_concept_ids=linked, use='AUDIT_WITNESS_NOT_REPORT_APPROVAL'))
    return result


def atomic_assertions(concept_ids, data=None, manifest=None):
    """Retrieve source assertions; formula descriptions are never executed."""
    data = (json.loads((ROOT / 'data/knowledge/original_assertions.json').read_text())
            if data is None else data)
    manifest = load_manifest() if manifest is None else manifest
    if (data['scope'] != 'SELECTED_ATOMIC_ORIGINAL_SOURCE_ASSERTIONS_NOT_EXHAUSTIVE'
            or data['all_important_knowledge_covered'] is not False):
        raise ValueError('Atomic assertions are not exhaustive knowledge coverage')
    ids = [r['id'] for r in data['assertions']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate atomic source assertion')
    by_id = {r['id']:r for r in data['assertions']}
    for pair in data['required_competing_pairs']:
        if any(id not in by_id for id in pair):
            raise ValueError('Competing source assertion was omitted')
    files = {r['file_id']:r for b in manifest['batches'] for r in b['files']}
    files.update({r['file_id']: r for r in manifest['loose_root_files']})
    for row in data['assertions']:
        if (row['answer_use'] != 'NOT_APPROVED'
                or row['execution_status'] != 'NOT_EXECUTABLE_NOT_RUNTIME_APPROVED'
                or not row['exclusions_and_limits'] or not row['witnesses']):
            raise ValueError('Source assertion cannot authorize execution or answers')
        for witness in row['witnesses']:
            original = files.get(witness['file_id'])
            if (not original or witness['content_sha256'] != original['content_sha256']
                    or witness['original_printed_pages'] != original['printed_page_ids']
                    or original['visual_review_status'] != 'TARGETED_ORIGINAL_VISUAL_REVIEW'):
                raise ValueError('Atomic assertion lost original witness identity')
    return [r for r in data['assertions'] if r['concept_id'] in concept_ids]
