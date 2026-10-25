"""Build a complete per-OCR-line candidate map plus exact human-review queue."""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.source_pipeline import load_state,save_json,sha,private_path
from knowledge_audit.line_reconciliation import reconcile,page_index,header_candidates,validate_annotation


def main():
    state=load_state()['files']
    with sqlite3.connect((ROOT/'reference/knowledge-index.sqlite').as_uri()+'?mode=ro',uri=True) as db:
        records=list(db.execute('SELECT pdf_page,text,text_sha256 FROM pages'))
    pages={p:t for p,t,h in records}; hashes={p:h for p,t,h in records}
    index=page_index(pages)
    annotation_path=ROOT/'data/knowledge/source_line_annotations.json'
    notes=json.loads(annotation_path.read_text())['annotations'] if annotation_path.exists() else []
    files=[]; totals=Counter(); pending=[]; numeric=[]
    for identity,row in state.items():
        if row['ocr_status']!='OCR_EXTRACTED_CANDIDATE': continue
        source=private_path(row['local_path']); output=private_path(row['ocr_path'])
        if sha(source)!=row['content_sha256'] or sha(output)!=row['ocr_output_sha256']:
            raise ValueError('Source/OCR changed before line reconciliation: '+identity)
        ocr=json.loads(output.read_text(encoding='utf-8-sig'))
        lines,details,ranked=reconcile(ocr,pages,index,hashes)
        for note in [n for n in notes if n['file_id']==identity]:
            validate_annotation(note,row,ocr)
            for first,last in note['line_ranges']:
                for n in range(first,last+1):
                    lines[n-1]['visual_transcription_status']='TARGETED_IMAGE_CHECK_NOT_FULL_PAGE_APPROVAL'
                    lines[n-1].setdefault('annotation_ids',[]).append(note['id'])
        for public,private in zip(lines,details):
            private.update(public)
        path=ROOT/'reference/line-reconciliation'/f'{identity}.json'
        save_json(path,dict(file_id=identity,image_sha256=row['content_sha256'],ocr_output_sha256=row['ocr_output_sha256'],lines=details))
        counts=Counter(l['comparison_status'] for l in lines)
        checked=[l['line_number'] for l in lines if l['visual_transcription_status']!='PENDING']
        files.append(dict(file_id=identity,name=row['name'],image_sha256=row['content_sha256'],
            ocr_output_sha256=row['ocr_output_sha256'],image_dimensions=[ocr['width'],ocr['height']],
            printed_header_candidates=header_candidates(ocr),candidate_pages=[dict(pdf_page=p,trigram_hits=h) for p,h in ranked],
            private_details_path=path.relative_to(ROOT).as_posix(),private_details_sha256=sha(path),
            lines=lines,counts=dict(counts),targeted_checked_lines=checked))
        totals.update(counts); totals['lines']+=len(lines); totals['targeted_checked_lines']+=len(checked)
        pending.append(dict(file_id=identity,pending_line_numbers=[l['line_number'] for l in lines if l['visual_transcription_status']=='PENDING']))
        numeric.append(dict(file_id=identity,line_numbers=[l['line_number'] for l in lines if l['review_flags'] and 'NUMERIC_OR_GLYPH_PRESENT' in l['review_flags']]))
    result=dict(schema_version='1.0',scope='EVERY_OCR_LINE_COMPARED_LEXICALLY_NOT_EXHAUSTIVE_VISUAL_OR_SEMANTIC_APPROVAL',
        matching_algorithm='Exact normalized-token runs >=3; highest trigram anchor and adjacent reflow pages; punctuation/numerical glyph errors remain candidates.',
        pdf_pages=len(pages),files_processed=len(files),counts=dict(totals),
        corpus_semantically_complete=False,all_lines_visually_verified=False,files=files)
    save_json(ROOT/'data/knowledge/source_line_reconciliation.json',result)
    save_json(ROOT/'evidence/source-pipeline/line-review-queue.json',dict(scope='EXACT_UNCHECKED_OCR_LINES_NOT_SOURCE_ABSENCE',
        missing_ocr_file_ids=[i for i,r in state.items() if r['ocr_status']!='OCR_EXTRACTED_CANDIDATE'],files=pending,numeric_or_glyph_priority=numeric))
    print(json.dumps(dict(files=len(files),counts=dict(totals))))


if __name__=='__main__': main()
