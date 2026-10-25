"""Local ID-keyed acquisition, OCR and exact remaining-queue commands."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_audit.source_pipeline import (STATE, load_state, initialize, save_json,
    acquire, ocr, index_ocr, private_path, manifest_rows, search_ocr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['init', 'acquire', 'ocr', 'index', 'search', 'status'])
    parser.add_argument('--query')
    parser.add_argument('--receipts', help='Private connector receipts JSON under reference/')
    parser.add_argument('--ids', nargs='*')
    parser.add_argument('--limit', type=int, default=100)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'data/knowledge/source_manifest.json').read_text())
    state = initialize(manifest, load_state())
    checkpoint = lambda: save_json(STATE, state)
    checkpoint()
    selected = [row for row in state['files'].values() if not args.ids or row['file_id'] in args.ids]
    if args.command == 'acquire':
        receipts = json.loads(private_path(args.receipts).read_text())
        for row in [r for r in selected if r['file_id'] in receipts][:args.limit]:
            acquire(row, receipts[row['file_id']], checkpoint)
            print(json.dumps({k: row.get(k) for k in ['file_id','acquisition_status','last_error']}), flush=True)
    elif args.command == 'ocr':
        pending = [r for r in selected if r['acquisition_status'] == 'ACQUIRED_HASHED'
                   and r['ocr_status'] != 'OCR_EXTRACTED_CANDIDATE']
        for row in pending[:args.limit]:
            ocr(row, checkpoint)
            print(json.dumps({k: row.get(k) for k in ['file_id','ocr_status','ocr_error']}), flush=True)
    elif args.command == 'index':
        index_ocr(state, 'reference/original-candidates.sqlite')
    elif args.command == 'search':
        print(json.dumps(search_ocr(state,args.query or ''),indent=2))
    elif args.command == 'status':
        rows = list(state['files'].values())
        queue = dict(acquisition=[r['file_id'] for r in rows if r['acquisition_status'] != 'ACQUIRED_HASHED'],
            ocr=[r['file_id'] for r in rows if r['ocr_status'] != 'OCR_EXTRACTED_CANDIDATE'],
            visual=[r['file_id'] for r in manifest_rows(manifest) if r['visual_review_status'] != 'TARGETED_ORIGINAL_VISUAL_REVIEW'],
            semantic=[r['file_id'] for r in manifest_rows(manifest) if r['semantic_review_status'] == 'PENDING'])
        save_json(ROOT / 'evidence/source-pipeline/remaining-queue.json', queue)
        print(json.dumps(dict(acquisition=Counter(r['acquisition_status'] for r in rows),
            ocr=Counter(r['ocr_status'] for r in rows), remaining={k:len(v) for k,v in queue.items()})))


if __name__ == '__main__':
    main()
