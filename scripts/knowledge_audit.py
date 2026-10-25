"""Run source inventory checks, index a source PDF locally, or retrieve witnesses."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.registry import load_registry,validate_registry,coverage
from knowledge_audit.corpus import index_pdf,search

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('check')
    build=sub.add_parser('index-pdf');build.add_argument('path');build.add_argument('--source-id',required=True)
    lookup=sub.add_parser('search');lookup.add_argument('query');lookup.add_argument('--limit',type=int,default=8)
    parser.add_argument('--database',default=str(ROOT/'reference/knowledge-index.sqlite'))
    args=parser.parse_args()
    if args.command=='check':
        data=load_registry();validate_registry(data);result=coverage(data)
    elif args.command=='index-pdf':result=index_pdf(args.path,args.database,args.source_id)
    else:result=search(args.database,args.query,args.limit)
    print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
