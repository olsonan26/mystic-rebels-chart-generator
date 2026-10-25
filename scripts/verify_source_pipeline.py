"""Publish metadata-only stage, page-map and retrieval evidence from saved work."""
import hashlib
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.sources import load_manifest,validate_manifest,atomic_assertions
from knowledge_audit.source_pipeline import load_state,manifest_rows,save_json,search_ocr,sha
from knowledge_audit.requirements import load_requirements,validate_requirements


def main():
    manifest=load_manifest();validate_manifest(manifest)
    state=load_state(); rows=manifest_rows(manifest)
    if set(state['files'])!={r['file_id'] for r in rows}:
        raise ValueError('Stage inventory differs from original manifest IDs')
    for row in rows:
        stage=state['files'][row['file_id']]
        if stage['acquisition_status']=='ACQUIRED_HASHED' and (
                row['content_sha256']!=stage['content_sha256'] or row['local_path']!=stage['local_path']):
            raise ValueError('Stage/manifest source mismatch')
    continuation=json.loads((ROOT/'data/knowledge/source_review_continuation.json').read_text())
    by_id={r['file_id']:r for r in continuation['reviews']}
    with sqlite3.connect((ROOT/'reference/knowledge-index.sqlite').as_uri()+'?mode=ro',uri=True) as db:
        page_hashes=dict(db.execute('SELECT pdf_page,text_sha256 FROM pages'))
    mapping=[]; duplicates=defaultdict(list)
    for row in rows:
        if row['acquisition_status']!='ACQUIRED_HASHED':
            continue
        duplicates[row['content_sha256']].append(row['file_id'])
        review=by_id.get(row['file_id'],{})
        mapping.append(dict(file_id=row['file_id'],name=row['name'],image_sha256=row['content_sha256'],
            inspected_printed_headers=row['printed_page_ids'],printed_header_basis=row['printed_page_basis'],
            header_system='UNKNOWN_UNINSPECTED' if not row['printed_page_ids'] else
                'UNCERTAIN_CROPPED' if any('UNKNOWN' in p for p in row['printed_page_ids']) else
                'ROMAN_FRONT_MATTER' if all(p.lower() in {'v','vi','vii','viii'} for p in row['printed_page_ids']) else
                'ARABIC_PRINTED' if all(p.isdigit() for p in row['printed_page_ids']) else 'ALPHABETIC_APPENDIX',
            concepts=review.get('concept_ids',[]),
            pdf_candidates=[dict(pdf_page=p,reflow_footer=p+4,page_text_sha256=page_hashes[p]) for p in row['candidate_pdf_pages']],
            reconciliation_status=row['scan_to_pdf_status'],review_scope='TARGETED_NOT_FULL_PAGE_APPROVAL'
                if row['visual_review_status']=='TARGETED_ORIGINAL_VISUAL_REVIEW' else 'PENDING_TARGETED_REVIEW'))
    save_json(ROOT/'data/knowledge/original_page_map.json',dict(
        scope='INSPECTED_HEADERS_AND_CANDIDATE_PDF_MAP_NOT_CORPUS_COMPLETENESS',
        printed_page_denominator=None,complete_scan_to_pdf_reconciliation=False,files=mapping,
        exact_byte_duplicates=[dict(sha256=d,file_ids=ids) for d,ids in duplicates.items() if len(ids)>1],
        unresolved=['Progression printed492 remains unlocated; no complete printed-page/header accounting or absence claim.',
            'Loose Page156 image has a cropped header; retain filename hint separately.',
            'OCR overlap is a candidate lead, not complete text/diagram alignment or proof of omission.']))
    searches=[]
    for query,expected_name in [('Flora','IMG_5401.JPG'),('Nessus','IMG_5431.JPG'),
            ('Sedna','IMG_5441.JPG'),('Sophia','IMG_5090.JPG')]:
        results=search_ocr(state,query)
        if expected_name not in [r['name'] for r in results]:
            raise ValueError('Expected original OCR candidate missing: '+query)
        searches.append(dict(query=query,results=[{k:r[k] for k in
            ['file_id','name','image_sha256','ocr_sha256','status']} for r in results],
            expected_original_found=expected_name,verified_transcription=False))
    requirements=load_requirements();validate_requirements(requirements)
    baseline=json.loads((ROOT/'evidence/source-pipeline/session-baseline.json').read_text())
    acquired=sum(r['acquisition_status']=='ACQUIRED_HASHED' for r in rows)
    extracted=sum(r['ocr_status']=='OCR_EXTRACTED_CANDIDATE' for r in rows)
    new_acquired_ids={r['file_id'] for r in state['files'].values() if r.get('identity_basis')=='CONNECTOR_RECEIPT_FILE_ID' and r['acquisition_status']=='ACQUIRED_HASHED'}
    reviewed_new_ids=set(by_id)&new_acquired_ids
    counts=dict(file_records=len(rows),newly_acquired=acquired-baseline['acquired'],total_acquired=acquired,
        newly_ocr_extracted=extracted-baseline['ocr_extracted'],total_ocr_extracted=extracted,
        new_targeted_visual_records=len(continuation['reviews']),newly_acquired_images_targeted_reviewed=len(reviewed_new_ids),
        prior_acquired_images_reinspected=len(set(by_id)-new_acquired_ids),total_targeted_visual_records=sum(
            r['visual_review_status']=='TARGETED_ORIGINAL_VISUAL_REVIEW' for r in rows),
        targeted_passage_reconciliations=len(continuation['reviews']),
        new_atomic_assertions=len(continuation['assertions']),total_atomic_assertions=len(atomic_assertions(
            [r['id'] for r in json.loads((ROOT/'data/knowledge/interpretive_inventory.json').read_text())['records']])),
        remaining_acquisition=len(rows)-acquired,remaining_ocr=len(rows)-extracted,
        remaining_visual=sum(r['visual_review_status']!='TARGETED_ORIGINAL_VISUAL_REVIEW' for r in rows),
        exhaustive_semantic_reviews_claimed=0,printed_page_denominator=None)
    for key,status,field in [('remaining_acquisition','ACQUIRED_HASHED','acquisition_status'),
            ('remaining_ocr','OCR_EXTRACTED_CANDIDATE','ocr_status'),
            ('remaining_visual','TARGETED_ORIGINAL_VISUAL_REVIEW','visual_review_status')]:
        if counts[key]!=sum(r[field]!=status for r in rows):
            raise ValueError('Recorded batch count changed: '+key)
    save_json(ROOT/'evidence/source-pipeline/stage-verification.json',dict(
        status='LOCAL_STAGES_AND_CANDIDATE_RETRIEVAL_VERIFIED',baseline='evidence/source-pipeline/session-baseline.json',counts_since_baseline=True,counts=counts,
        requirement_dispositions=dict(Counter(r['disposition'] for r in requirements['requirements'])),
        candidate_searches=searches,personal_answers_generated=False,deployed=False,
        ocr_engine='Windows.Media.Ocr en-US; installed Windows PowerShell5 WinRT; no new package installation',
        ocr_pilot_limit='Initial Spark509 pilot verified extraction; the subsequent bounded batch included diagrams and Roman headings. Broader corpus/rotation/language accuracy is not established.',
        retry_observation='Initial restricted-network acquisition failed with URLError and checkpointed; authorized network retry reused state and succeeded.',
        extraction_failures_current=sum(r['ocr_status']=='OCR_FAILED' for r in state['files'].values()),
        line_reconciliation='data/knowledge/source_line_reconciliation.json',
        source_fidelity_is_astronomical_correctness=False))
    print(json.dumps(counts))


if __name__=='__main__':
    main()
