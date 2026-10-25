"""Reproduce ID-keyed review records from analyst observations, never from OCR.

Printed headers and summaries are explicitly authored after viewing images.
PDF overlap candidates below are research leads, not a complete page alignment.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.source_pipeline import load_state, save_json


def grams(text):
    words=re.findall('[a-z]+',text.lower())
    return set(zip(words,words[1:],words[2:]))


def main():
    state=load_state()['files']
    names={}
    for row in state.values():
        names.setdefault(row['name'].casefold(),[]).append(row)
    previous=ROOT/'data/knowledge/source_review_continuation.json'
    existing=json.loads(previous.read_text()) if previous.exists() else {}
    retained={r['file_id']:r for r in existing.get('reviews',[])}
    database=ROOT/'reference/knowledge-index.sqlite'
    pages=[]
    if database.exists():
        with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as db:
            pages=[(p,grams(t)) for p,t in db.execute('SELECT pdf_page,text FROM pages')]
    reviews=[]
    for line in (ROOT/'data/knowledge/source_review_batch_notes.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        key,header,concepts,summary=line.split('|')
        rows=[state[key]] if key in state else names.get(key.casefold(),[])
        if len(rows)!=1:
            raise ValueError('Ambiguous review identity: '+key)
        row=rows[0]
        if row['acquisition_status']!='ACQUIRED_HASHED':
            raise ValueError('Review requires acquired exact-byte witness')
        # Keep candidates reproducible in CI without publishing source text.
        candidates=retained.get(row['file_id'],{}).get('candidate_pdf_overlaps',[])
        path=ROOT/row.get('ocr_path','reference/missing')
        if pages and path.is_file():
            words=grams(json.loads(path.read_text(encoding='utf-8-sig'))['text'])
            ranked=sorted([(len(words & g)/max(1,len(words)),p) for p,g in pages],reverse=True)
            candidates=[dict(pdf_page=p,overlap=round(score,4),status='OCR_TRIGRAM_CANDIDATE_NOT_ALIGNMENT_APPROVAL')
                        for score,p in ranked[:3] if score>=0.10]
        ids=[c['pdf_page'] for c in candidates]
        reviews.append(dict(file_id=row['file_id'],name=row['name'],content_sha256=row['content_sha256'],
            printed_page_ids=[header],printed_page_basis='PARTIAL_CROPPED_UNKNOWN' if header.startswith('UNKNOWN') else 'VISUAL_HEADER',
            concept_ids=concepts.replace('asteroid-pallas-athene','asteroid-pallas').split(),summary=summary,
            pdf_pages=sorted(ids),candidate_pdf_overlaps=candidates,
            reconciliation_status='CANDIDATE_TEXT_OVERLAP_NOT_COMPLETE_ALIGNMENT' if ids else 'ORIGINAL_PASSAGE_NOT_LOCATED_BY_CANDIDATE_SEARCH',
            visual_review_scope='HEADER_DIAGRAMS_AND_SELECTED_PASSAGES_NOT_LINE_BY_LINE_TRANSCRIPTION',
            image_quality='PARTIALLY_CROPPED_HEADER_BODY_READABLE' if header.startswith('UNKNOWN') else 'TARGET_PASSAGES_READABLE_PHOTOGRAPH',
            duplicate_content_status='EXACT_BYTE_DUPLICATE_OTHER_DRIVE_ID' if row['name']=='IMG_5079.jpg' else 'NO_DUPLICATE_CLAIM',
            visible_page_count=1,semantic_status='TARGETED_PASSAGE_RECONCILIATION_NOT_EXHAUSTIVE'))
    assertions=[]
    for line in (ROOT/'data/knowledge/source_assertion_additions.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        identity,concept,kind,keys,proposition,limit,dependencies=line.split('|')
        witnesses=[]
        for key in keys.split():
            selected=[state[key]] if key in state else names.get(key.casefold(),[])
            if len(selected)!=1:
                raise ValueError('Ambiguous assertion witness: '+key)
            row=selected[0]
            review=next(r for r in reviews if r['file_id']==row['file_id'])
            if concept not in review['concept_ids']:
                raise ValueError('Assertion is not linked to its inspected concept')
            witnesses.append(dict(file_id=row['file_id'],name=row['name'],content_sha256=row['content_sha256'],
                original_printed_pages=review['printed_page_ids']))
        assertions.append(dict(id=identity,concept_id=concept,kind=kind,proposition=proposition,
            applicability='Only the explicitly stated technique/chart context; full condition and all linked counterevidence required.',
            exclusions_and_limits=[limit],requires_concepts=dependencies.split(),witnesses=witnesses,
            authority='ORIGINAL_BATCH_SCAN_TARGETED_REVIEW',execution_status='NOT_EXECUTABLE_NOT_RUNTIME_APPROVED',
            interpretation_validation='SOURCE_FAITHFULNESS_ONLY_NOT_EMPIRICAL_VALIDATION',answer_use='NOT_APPROVED'))
    meanings={a['concept_id']:a['proposition'] for a in assertions if a['id'] in
        ['flora-dispersed-actions','ixion-repeated-patterns','nessus-transmitted-residue','sedna-delayed-consequence']}
    out=dict(schema_version='1.0',scope='TARGETED_ID_KEYED_SOURCE_CONTINUATION_NOT_EXHAUSTIVE',
        review_date_local='2026-10-25',reviews=reviews,
        assertions=assertions,question_updates=existing.get('question_updates',[]),
        source_only_concepts=[dict(id=concept,meaning_summary=meaning) for concept,meaning in meanings.items()])
    save_json(previous,out)
    print(json.dumps(dict(targeted_visual_records=len(reviews),printed_page_denominator=None)))


if __name__=='__main__':
    main()
