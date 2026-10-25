"""Separate source completeness, implementation, retrieval and rule approval."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTER=ROOT/'data/knowledge/capabilities.json'

def load_registry():
    return json.loads(REGISTER.read_text(encoding='utf-8'))

def approval_errors(rule, by_id):
    errors=[]
    if rule.get('source_status') not in ('PRIMARY_RULE_REVIEWED','ENGINEERING_SPECIFIED'):
        errors.append('source_not_reviewed_or_unresolved')
    if rule.get('conflicts'): errors.append('unresolved_source_conflict')
    if rule.get('implementation_status')!='RUNTIME_IMPLEMENTED': errors.append('not_implemented_at_runtime')
    if not rule.get('verification_tests'): errors.append('missing_regression_evidence')
    if not rule.get('witnesses') and rule.get('source_status')!='ENGINEERING_SPECIFIED': errors.append('missing_primary_witness')
    for dependency in rule.get('dependencies',[]):
        if dependency not in by_id: errors.append('unknown_dependency:'+dependency)
        elif by_id[dependency].get('answer_use')!='APPROVED': errors.append('unapproved_dependency:'+dependency)
    return errors

def validate_registry(registry, check_files=True):
    rules=registry['rules']; ids=[r['id'] for r in rules]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate rule ID')
    by_id={r['id']:r for r in rules}
    for rule in rules:
        if check_files:
            for name in rule.get('implementation_files',[])+rule.get('verification_tests',[]):
                if not (ROOT/name.split('::')[0]).is_file(): raise ValueError('Missing evidence file: '+name)
        if rule.get('answer_use')=='APPROVED':
            errors=approval_errors(rule,by_id)
            if errors: raise ValueError(rule['id']+': '+','.join(errors))
    return True

def coverage(registry):
    batches=registry['source_inventory']['batches']
    complete=all(b.get('enumeration_complete') is True for b in batches) and len(batches)==8
    return {'batch_count':len(batches),'enumeration_complete':complete,
            'known_file_lower_bound':sum(b['known_files'] for b in batches),
            'source_semantic_coverage_percent':None,
            'coverage_percent_reason':'No complete eight-batch page/concept denominator or verified scan-to-rule mapping yet.',
            'runtime_rules':sum(r['implementation_status']=='RUNTIME_IMPLEMENTED' for r in registry['rules']),
            'registered_rules':len(registry['rules']),
            'complete_intelligence_claim_allowed':False}
