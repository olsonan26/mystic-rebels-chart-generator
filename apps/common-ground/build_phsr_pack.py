"""Create a separate evidence pack without changing either source application."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MYSTIC = HERE.parent / 'Mystic-Rebels'
if not MYSTIC.is_dir():
    MYSTIC = HERE.parents[1]

def build():
    knowledge = MYSTIC / 'data/knowledge'
    inventory = json.loads((knowledge/'interpretive_inventory.json').read_text(encoding='utf-8-sig'))
    profiles = json.loads((knowledge/'source_meaning_profiles.json').read_text(encoding='utf-8-sig'))
    selected = {'phsr','delegate-condition','directional-context','tone-pulse','spark-entry',
                'retrograde-meaning','retrograded-house','age-degree','natal-transit-order'}
    records = {r['id']: r for r in inventory['records']
               if r['id'] in selected or r['id'].startswith(('meaning-', 'field-'))}
    meanings = {r['id']: r for r in profiles['profiles'] if r['kind']=='sign' or r['id']=='chiron-reviewed-vocabulary'}
    return {'schema_version':'1.0','method_id':'phsr-supported-research-v1',
            'stage_order':['planet','house','degree','decan','aspects','sign','ruler'],
            'generic_library_fallback_allowed':False,'personal_report_approved':False,
            'source_commit':'3d83db75c30b26d9b068576d84ec49554822fd8c',
            'input_sha256':{n:hashlib.sha256((knowledge/n).read_bytes()).hexdigest()
                            for n in ['interpretive_inventory.json','source_meaning_profiles.json']},
            'records':records,'profiles':meanings,
            'decisions':{'D1':'Canonical degree/Spark rule conflicts',
                         'D2':'Complete directed aspect rules and outgoing reach',
                         'D3':'Full Delegate condition composition across cycles',
                         'D4':'Exact activation calendar convention',
                         'D5':'Manifestation delay procedure',
                         'D6':'Progression and relocation coupling',
                         'D7':'Current-name adoption and letter-cycle policy',
                         'D8':'Review of age-specific composed prose'}}

if __name__=='__main__':
    (HERE/'data/phsr-rules-v1.json').write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
