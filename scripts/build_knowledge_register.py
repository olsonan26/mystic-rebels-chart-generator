"""Reproducible migration of historical readiness labels into audited capability states.

Historical READY is evidence of a prior proposal, never runtime completion.
Source excerpts and photographs stay in the excluded reference directory.
"""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    historical=json.loads((ROOT/'reference/fixtures/rule_register.json').read_text(encoding='utf-8'))
    inventory=json.loads((ROOT/'evidence/methodology-review/drive-inventory-partial.json').read_text(encoding='utf-8'))
    runtime={1:('mystic_rebels/chronology.py','astronomy_qa/test_core.py'),
             2:('mystic_rebels/astronomy.py','astronomy_qa/test_horizons.py'),
             **{i:('mystic_rebels/placements.py','astronomy_qa/test_core.py') for i in range(3,8)},
             **{i:('mystic_rebels/astronomy.py','astronomy_qa/test_core.py') for i in range(9,14)},
             14:('mystic_rebels/service.py','astronomy_qa/test_core.py'),
             16:('mystic_rebels/astronomy.py','astronomy_qa/test_core.py'),
             17:('web/src/Wheel.tsx','web/src/wheelLayout.test.tsx')}
    research={19,20,21,22}
    rules=[]
    for old in historical['rules']:
        n=int(old['id'].split('-')[-1])
        files,tests=runtime.get(n,(None,None))
        rules.append({'id':old['id'],'name':old['name'],
          'historical_tier':old['tier'],'historical_source_status':old['status'],
          'source_status':'ENGINEERING_SPECIFIED' if old['status'] in ('ENGINEERING','MATHEMATICAL') and files else 'SECONDARY_REGISTER_NEEDS_PRIMARY_MAPPING',
          'implementation_status':'RUNTIME_IMPLEMENTED' if files else 'RESEARCH_HELPER_ONLY' if n in research else 'NOT_IMPLEMENTED_AS_PRODUCT_WORKFLOW',
          'implementation_files':[files] if files else ['web/src/phase10Research.ts'] if n in research else [],
          'verification_tests':[tests] if tests else ['web/src/phase10Research.test.ts'] if n in research else [],
          'witnesses':[],'conflicts':[],'dependencies':[],
          'answer_use':'NOT_APPROVED_FOR_PERSONAL_ANSWERS',
          'limitation':old['limitation'],
          'retrieval_status':'NOT_RETRIEVED_BY_PRODUCT'})
    by_id={r['id']:r for r in rules}
    for n in (20,21):
        r=by_id[f'N9-{n:03d}'];r['source_status']='CONTRADICTED'
        r['witnesses']=[{'drive_file_id':'1cY5Ih6NDZDJOMBTwx0pHcB3EoJMakSfR','original_printed_page':235,'pdf_page':293,'reflow_footer':297,'verified_visually':True},
                         {'pdf_page':433,'original_printed_page':509}, {'pdf_page':434,'original_printed_page':510}, {'pdf_page':458,'original_printed_page':546}]
        r['conflicts']=['SPARK_HOUSE_VS_SIGN_PARITY','COMPOSITE_SATURN_MATCHES_NEITHER']
        r['explicit_written_procedure']='house parity: (floor(degree_within_sign)+(6 if house even else 0)) modulo 12; Aries index 0'
        r['witnesses'].append({'drive_file_id':'1m6MFoG8NsmpSZP0X-7VJbcrQYQ1PffVETGfRPSIny_w',
                              'title':'You Are Not Your Sign - Technical Specification v2',
                              'section':'compute_spark','procedure':'astronomical-sign parity',
                              'authority_status':'SUPPLEMENTAL_APP_SPEC_NOT_CONFIRMED_AS_BOOK_ERRATUM'})
        r['conflicts'].append('BOOK_HOUSE_PROCEDURE_VS_SUPPLEMENTAL_APP_SIGN_PROCEDURE')
    by_id['N9-038']['source_status']='DEFINITION_MISSING_FROM_SUPPLIED_PDF'
    by_id['N9-038']['witnesses']=[{'pdf_page':421,'missing_original_printed_pages':[491,492]}]
    by_id['N9-025']['source_status']='CONTRADICTED'
    by_id['N9-025']['conflicts']=['PLUTO_1_5_DEGREES_VS_WORKED_1_DEGREE']
    by_id['N9-025']['witnesses']=[{'pdf_page':343,'original_printed_page':378}]
    rules.append({'id':'N10-GRADITY','name':'Event-based four-phase Gradity',
      'source_status':'PRIMARY_RULE_REVIEWED','implementation_status':'RUNTIME_IMPLEMENTED',
      'implementation_files':['mystic_rebels/gradity.py','mystic_rebels/service.py'],
      'verification_tests':['astronomy_qa/test_gradity.py','astronomy_qa/test_horizons_gradity.py'],
      'witnesses':[{'pdf_page':203,'reflow_footer':207,'original_printed_page':143},{'pdf_page':477,'reflow_footer':481,'original_printed_pages':[569,570]}],
      'conflicts':['EXACT_BOUNDARY_EQUALITY_UNSPECIFIED','OVERLAPPING_SHADOW_PRECEDENCE_UNSPECIFIED'],
      'dependencies':['N9-001','N9-002'],'answer_use':'NOT_APPROVED_FOR_PERSONAL_ANSWERS',
      'astronomy_test_scope':'Mercury 2024 and Venus 2025; 584 JPL/ERFA samples, 8 events; not all epochs or planets',
      'retrieval_status':'NOT_RETRIEVED_BY_PRODUCT',
      'limitation':'Event metadata supported for Mercury through Pluto; boundaries/overlaps remain unassigned. No interpretation validation.'})
    result={'schema_version':'1.0','product':'Mystic Rebels / Alchemystic Astrology',
      'baseline_commit':'9059304b31d241fee2cb08fb4e46aad32f9bf228',
      'audit_status':'IN_PROGRESS_NOT_FULL_SOURCE_COVERAGE',
      'source_inventory':{'batches':[{'name':b['batch'],'id':b['id'],'known_files':len(b['files']),
                                     'enumeration_complete':False,'semantic_review_complete':False,
                                     'listing_limit_warning':len(b['files'])==100} for b in inventory['batches']],
                          'compiled_pdf_sha256':'9d5fb55cf6d4f2134ed780c2694503d2dde42bdad68add60ff35acef0237161d',
                          'compiled_pdf_pages':692,'compiled_pdf_review_complete':True,
                          'compiled_pdf_is_complete_scan_set':False},
      'intelligence_layers':{'runtime_source_retrieval':'ABSENT','local_page_retrieval':'IMPLEMENTED_RESEARCH_ONLY',
         'personal_question_answering':'ABSENT','life_context_memory':'ABSENT','source_cited_narrative':'ABSENT',
         'chart_calculation':'IMPLEMENTED','source_to_rule_coverage':'INCOMPLETE'},
      'rules':rules}
    out=ROOT/'data/knowledge/capabilities.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Migrated {len(rules)} rule capability records; no source completeness or personal-answer approval asserted.')
if __name__=='__main__':main()
