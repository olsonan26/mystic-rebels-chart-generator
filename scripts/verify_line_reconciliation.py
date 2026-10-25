"""Check every saved line locator and private OCR/PDF provenance."""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.source_pipeline import load_state,sha,private_path,save_json
from knowledge_audit.line_reconciliation import text_hash,validate_annotation


def main():
    ledger=json.loads((ROOT/'data/knowledge/source_line_reconciliation.json').read_text())
    state=load_state()['files']
    expected={i for i,r in state.items() if r['ocr_status']=='OCR_EXTRACTED_CANDIDATE'}
    if {r['file_id'] for r in ledger['files']}!=expected:
        raise ValueError('Line ledger does not cover every successful OCR ID')
    with sqlite3.connect((ROOT/'reference/knowledge-index.sqlite').as_uri()+'?mode=ro',uri=True) as db:
        pages={p:(t,h) for p,t,h in db.execute('SELECT pdf_page,text,text_sha256 FROM pages')}
    if any(text_hash(t)!=h for t,h in pages.values()): raise ValueError('PDF index text drift')
    notes=json.loads((ROOT/'data/knowledge/source_line_annotations.json').read_text())['annotations']
    totals=Counter(); seen_notes=set()
    for file in ledger['files']:
        row=state[file['file_id']]
        if (sha(private_path(row['local_path']))!=file['image_sha256'] or
                sha(private_path(row['ocr_path']))!=file['ocr_output_sha256']):
            raise ValueError('Line witness bytes changed')
        ocr=json.loads(private_path(row['ocr_path']).read_text(encoding='utf-8-sig'))
        details=private_path(file['private_details_path'])
        if sha(details)!=file['private_details_sha256']: raise ValueError('Private line ledger drift')
        raw=json.loads(details.read_text())['lines']
        if len(file['lines'])!=len(ocr['lines']) or len(raw)!=len(file['lines']):
            raise ValueError('Line count changed')
        checked=set()
        for note in [n for n in notes if n['file_id']==row['file_id']]:
            validate_annotation(note,row,ocr);seen_notes.add(note['id'])
            for first,last in note['line_ranges']: checked.update(range(first,last+1))
        for n,(line,source,private) in enumerate(zip(file['lines'],ocr['lines'],raw),1):
            if (line['line_number']!=n or line['line_sha256']!=text_hash(source['text']) or
                    private['source_text']!=source['text'] or line['matched_tokens']>line['tokens']):
                raise ValueError('Line locator/text drift')
            if (line['visual_transcription_status']!='PENDING')!=(n in checked):
                raise ValueError('Automatic match was promoted into image review')
            for span in line['pdf_spans']:
                text,digest=pages[span['pdf_page']]
                if span['page_text_sha256']!=digest or not 0<=span['char_start']<span['char_end']<=len(text):
                    raise ValueError('PDF line span drift')
            totals[line['comparison_status']]+=1;totals['lines']+=1
        totals['targeted_checked_lines']+=len(checked)
    if dict(totals)!=ledger['counts'] or seen_notes!={n['id'] for n in notes}:
        raise ValueError('Line counts or annotation identities differ')
    findings=json.loads((ROOT/'data/knowledge/source_blocker_findings.json').read_text())['findings']
    assertions={a['id'] for a in json.loads((ROOT/'data/knowledge/original_assertions.json').read_text())['assertions']}
    for finding in findings:
        if set(finding['annotation_ids'])-seen_notes or set(finding['assertion_ids'])-assertions:
            raise ValueError('Blocker finding lost a witness')
    quality=json.loads((ROOT/'data/knowledge/source_quality_issues.json').read_text())['issues']
    for issue in quality:
        if state[issue['file_id']]['content_sha256']!=issue['image_sha256']:
            raise ValueError('Quality witness drift')
    result=dict(status='ALL_SAVED_OCR_LINE_LOCATORS_AND_HASHES_VERIFIED',files=len(expected),counts=dict(totals),
        annotations=len(notes),named_blocker_findings=len(findings),
        unreconciled_ocr_files=[i for i in state if i not in expected],
        full_visual_or_semantic_signoff=False,source_blockers_all_resolved=False,
        source_line_ledger_sha256=sha(ROOT/'data/knowledge/source_line_reconciliation.json'))
    save_json(ROOT/'evidence/source-pipeline/line-verification.json',result)
    print(json.dumps(result))


if __name__=='__main__': main()
