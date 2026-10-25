"""Run source inventory checks, index a source PDF locally, or retrieve witnesses."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from knowledge_audit.registry import load_registry,validate_registry,coverage
from knowledge_audit.corpus import index_pdf,search
from knowledge_audit.semantics import load_inventory,validate_inventory,validate_examples,profile_gaps,concept_packet,verify_pdf_witnesses
from knowledge_audit.sources import load_manifest,validate_manifest
from knowledge_audit.requirements import load_requirements,validate_requirements,requirement_packet

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('check')
    sub.add_parser('check-semantics')
    sub.add_parser('check-sources')
    sub.add_parser('check-requirements')
    requirement=sub.add_parser('requirement');requirement.add_argument('id')
    gaps=sub.add_parser('profile-gaps');gaps.add_argument('--section')
    concept=sub.add_parser('concept');concept.add_argument('id');concept.add_argument('--section',required=True)
    verify=sub.add_parser('verify-pdf-witnesses');verify.add_argument('path')
    build=sub.add_parser('index-pdf');build.add_argument('path');build.add_argument('--source-id',required=True)
    lookup=sub.add_parser('search');lookup.add_argument('query');lookup.add_argument('--limit',type=int,default=8)
    parser.add_argument('--database',default=str(ROOT/'reference/knowledge-index.sqlite'))
    args=parser.parse_args()
    if args.command=='check':
        data=load_registry();validate_registry(data);result=coverage(data)
    elif args.command=='check-semantics':
        data=load_inventory();validate_inventory(data);validate_examples(inventory=data);result=profile_gaps(data)['counts']
        result['status']='VALID_AUDIT_NOT_REPORT_APPROVAL'
    elif args.command=='check-sources':
        data=load_manifest();validate_manifest(data)
        result=dict(status='VALID_VISIBLE_SNAPSHOT_NOT_PAGE_COVERAGE',file_records=data['file_record_denominator'],printed_page_denominator=None)
    elif args.command=='check-requirements':
        data=load_requirements();validate_requirements(data)
        result=dict(status='VALID_RECONCILIATION_NOT_REPORT_APPROVAL',sections=len(data['sections']),requirements=len(data['requirements']))
    elif args.command=='requirement':result=requirement_packet(args.id,args.database)
    elif args.command=='profile-gaps':result=profile_gaps(section_id=args.section)
    elif args.command=='concept':result=concept_packet(args.id,args.database,args.section)
    elif args.command=='verify-pdf-witnesses':result=verify_pdf_witnesses(args.path,args.database)
    elif args.command=='index-pdf':result=index_pdf(args.path,args.database,args.source_id)
    else:result=search(args.database,args.query,args.limit)
    print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
