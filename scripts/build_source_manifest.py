"""Reproduce the manifest from saved connector/visible-browser observations.

No browser access, network, OCR, rule approval or source-text publication.
Original bytes are read only to calculate their SHA256. Review claims come from
the separately authored targeted review log, never from filename order.
"""
import hashlib
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_audit.sources import validate_manifest
from knowledge_audit.source_pipeline import load_state, manifest_rows, sha, private_path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    evidence = ROOT / 'evidence/source-continuation'
    reviews_path = ROOT / 'data/knowledge/source_review_updates.json'
    reviews = {r[0].casefold(): r for r in json.loads(reviews_path.read_text())['reviews']}
    root = json.loads(json.loads((evidence / 'drive-root.json').read_text())['content'])['files']
    local = {p.name.casefold(): p for p in (ROOT / 'reference/source_photos').glob('*') if p.suffix.lower() in ('.jpg', '.jpeg', '.png')}
    extra_metadata = {r['id']: r for r in json.loads((evidence / 'acquired-metadata-final.json').read_text())}
    filename_counts = Counter(
        re.search(r'IMG_\d+\.jpe?g', r['text'], re.I).group().casefold()
        for n in range(1, 9)
        for r in json.loads((evidence / f'browser-batch-{n}.json').read_text())['records'])
    batches = []
    names = defaultdict(list)
    for number in range(1, 9):
        name = f'BATCH {number}'
        folder = next(r for r in root if r['title'] == name)
        path = evidence / f'browser-batch-{number}.json'
        observed = json.loads(path.read_text())
        connector = json.loads(json.loads((evidence / f'drive-batch-{number}.json').read_text())['content'])['files']
        metadata = {r['id']: r for r in connector}
        for id, extra in extra_metadata.items():
            metadata[id] = {**metadata.get(id, {}), **extra}
        files = []
        for item in sorted(observed['records'], key=lambda r: r['index']):
            match = re.search(r'IMG_\d+\.jpe?g', item['text'], re.I)
            if not match:
                raise ValueError('Unclassified visible file; do not silently omit it: ' + item['id'])
            filename = match.group()
            m = metadata.get(item['id'], {})
            review = reviews.get(filename.casefold())
            asset = local.get(filename.casefold())
            if asset and filename_counts[filename.casefold()] > 1:
                raise ValueError('Ambiguous acquired filename: preserve bytes by provider file ID before assigning a hash: ' + filename)
            row = dict(file_id=item['id'], name=filename, batch=name,
                mime_type=m.get('mime_type', 'image/jpeg'),
                mime_type_basis='PROVIDER_METADATA' if m.get('mime_type') else 'JPEG_FILENAME_AND_IMAGE_ROW',
                size_bytes=int(m['size']) if m.get('size') else None,
                displayed_size=re.search(r'(\d+(?:\.\d+)? [KMG]B)', item['text']).group(1),
                created_time=m.get('created_time'), modified_time=m.get('modified_time'),
                provider_revision=None, provider_checksum=None,
                content_sha256=digest(asset) if asset else None,
                local_path=asset.relative_to(ROOT).as_posix() if asset else None,
                acquisition_status='ACQUIRED_HASHED' if asset else 'METADATA_ONLY',
                ocr_status='NOT_RUN',
                visual_review_status='TARGETED_ORIGINAL_VISUAL_REVIEW' if review else ('PRIOR_REVIEW_RECORDED' if asset else 'NOT_REVIEWED'),
                semantic_review_status='TARGETED_PASSAGE_REVIEW_NOT_EXHAUSTIVE' if review else 'PENDING',
                printed_page_ids=[review[1]] if review else [],
                printed_page_basis='VISUAL_HEADER' if review else 'UNKNOWN',
                visible_page_count=1 if review else None,
                multi_page_image_status='ONE_PRINTED_PAGE_VISIBLE' if review else 'NOT_CHECKED',
                candidate_pdf_pages=review[2] if review else [],
                scan_to_pdf_status=review[3] if review else 'UNRECONCILED',
                review_evidence='data/knowledge/source_review_updates.json#' + filename if review else None,
                disposition=review[4] if review else 'Pending original acquisition, OCR, visual and semantic review; metadata is not knowledge coverage.',
                duplicate_content_status='NOT_CHECKED_AGAINST_UNACQUIRED_FILES',
                alternate_version_status='NOT_ESTABLISHED')
            files.append(row)
            names[filename.casefold()].append(item['id'])
        batches.append(dict(name=name, folder_id=folder['id'], observed_count=len(files),
            observed_indices=[r['index'] for r in observed['records']],
            grid_rowcount=int(observed.get('grid', {}).get('rowcount', observed.get('stable_observed_rows', -1))),
            listing_status='VISIBLE_LISTING_ENDPOINT_REACHED',
            listing_evidence=dict(path=path.relative_to(ROOT).as_posix(),
                sha256=hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest(),
                hash_normalization='UTF8_UNIVERSAL_NEWLINES'),
            connector_returned_count=len(connector), connector_subset_of_browser=all(r['id'] in {f['file_id'] for f in files} for r in connector),
            files=files))
    loose = [dict(file_id=r['id'], name=r['title'], mime_type=r['mime_type'],
        size_bytes=int(r['size']) if r.get('size') else None, modified_time=r.get('modified_time'),
        content_sha256=None, provider_revision=None, acquisition_status='METADATA_ONLY',
        ocr_status='NOT_RUN', visual_review_status='NOT_REVIEWED', semantic_review_status='PENDING',
        printed_page_ids=[], filename_page_hint='156', printed_page_basis='NOT_VISUALLY_VERIFIED',
        scan_to_pdf_status='UNRECONCILED', disposition='Loose root image remains an individual pending source task.')
        for r in root if r['file_or_folder'] == 'file']
    data = dict(schema_version='1.0', scope='VISIBLE_DRIVE_DIRECT_CHILDREN_SNAPSHOT',
        audit_date_local='2026-10-25', root_id='1V7G3fU03ZNoAM8NbzLyu9Y9Ne2hXjomj',
        file_record_denominator=sum(len(b['files']) for b in batches) + len(loose),
        printed_page_denominator=None, semantic_coverage_percent=None,
        all_original_pages_semantically_reviewed=False, complete_scan_to_pdf_reconciliation=False,
        limitations=['Browser enumeration is a visible direct-child snapshot, not a provider revision freeze.',
            'No printed-page sequence or chapter completeness is inferred from image filenames.',
            'Unacquired files have no claimed content hash, exact version or duplicate-page disposition.',
            'Candidate PDF pages identify targeted overlap, not a complete scan-to-PDF bijection.'],
        repeated_filenames=[dict(name=n, file_ids=ids) for n, ids in names.items() if len(ids) > 1],
        batches=batches, loose_root_files=loose)
    # The ID-keyed ledger supersedes filename lookup for new acquisition/OCR.
    # Legacy filename mapping above remains only for the existing unique assets.
    stages = load_state()['files']
    continuation_path = ROOT / 'data/knowledge/source_review_continuation.json'
    continuation = json.loads(continuation_path.read_text()) if continuation_path.exists() else {'reviews': []}
    reviewed = {r['file_id']: r for r in continuation['reviews']}
    for row in manifest_rows(data):
        stage = stages.get(row['file_id'])
        if stage and stage['acquisition_status'] == 'ACQUIRED_HASHED':
            path = private_path(stage['local_path'])
            if path.exists() and sha(path) != stage['content_sha256']:
                raise ValueError('ID-keyed acquired bytes changed')
            for key in ('acquisition_status', 'content_sha256', 'local_path', 'size_bytes', 'ocr_status'):
                row[key] = stage[key]
            for key in ('ocr_path','ocr_output_sha256','ocr_text_sha256','ocr_source_sha256','ocr_engine','ocr_language','ocr_error'):
                if key in stage:
                    row[key] = stage[key]
        review = reviewed.get(row['file_id'])
        if review:
            if row['content_sha256'] != review['content_sha256']:
                raise ValueError('Continuation review source hash changed')
            row.update(visual_review_status='TARGETED_ORIGINAL_VISUAL_REVIEW',
                semantic_review_status='TARGETED_PASSAGE_REVIEW_NOT_EXHAUSTIVE',
                printed_page_ids=review['printed_page_ids'], printed_page_basis=review.get('printed_page_basis','VISUAL_HEADER'),
                visible_page_count=review.get('visible_page_count', 1),
                multi_page_image_status=review.get('multi_page_image_status', 'ONE_PRINTED_PAGE_VISIBLE'),
                candidate_pdf_pages=review['pdf_pages'], scan_to_pdf_status=review['reconciliation_status'],
                review_evidence='data/knowledge/source_review_continuation.json#' + row['file_id'],
                disposition=review['summary'], duplicate_content_status=review.get('duplicate_content_status', 'NOT_CHECKED_AGAINST_UNACQUIRED_FILES'))
        elif row['acquisition_status']=='ACQUIRED_HASHED' and row['semantic_review_status']=='PENDING':
            row['disposition']='Acquired and hashed; '+('candidate OCR extracted' if row['ocr_status']=='OCR_EXTRACTED_CANDIDATE' else 'OCR requires attention')+'; visual and semantic review remain pending.'
    validate_manifest(data)
    output = ROOT / 'data/knowledge/source_manifest.json'
    output.write_text(json.dumps(data, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(file_records=data['file_record_denominator'], batches={b['name']:b['observed_count'] for b in batches},
        acquired=sum(r['content_sha256'] is not None for r in manifest_rows(data)),
        targeted_reviews=sum(r['visual_review_status']=='TARGETED_ORIGINAL_VISUAL_REVIEW' for r in manifest_rows(data)), repeated_filenames=len(data['repeated_filenames']))))


if __name__ == '__main__':
    main()
