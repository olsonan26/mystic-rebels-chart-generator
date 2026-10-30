"""Ordered, source-bounded assessments. Geometry never becomes an approved aspect."""
import json
from pathlib import Path
from math import floor

SIGNS = ('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
RULERS = ('Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Pluto','Jupiter','Saturn','Uranus','Neptune')
ORDER = ['planet','house','degree','decan','aspects','sign','ruler']

def pack():
    return json.loads((Path(__file__).parent/'data/phsr-rules-v1.json').read_text(encoding='utf-8'))

def ruler_route(points, start):
    path=[]
    current=start
    while current in points and current not in path:
        path.append(current)
        current=points[current].get('sign_ruler')
    return {'path':path,'repeat':current if current in path else None,
            'cycle':path[path.index(current):] if current in path else [],
            'missing_node':current if current and current not in points else None}

def assess(chart, start='Chiron'):
    source=pack()
    points={p['id']:p for p in chart['points'] if p.get('available')}
    records=source['records']
    ac=chart.get('angles',{}).get('Ascendant')
    assessments={}
    for name,p in points.items():
        if name not in set(RULERS)|{'Chiron'}:
            continue
        record_id='meaning-'+name.lower()
        meaning=records.get(record_id,{})
        function=meaning.get('meaning_summary')
        if name=='Chiron':
            function=source['profiles']['chiron-reviewed-vocabulary']['source_meaning']
        parent={'Sun':'Father symbolism is a documented convention, not a claim about behavior.',
                'Moon':'Mother symbolism is a documented convention, not a claim about behavior.'}.get(name)
        h=p.get('house')
        delegate=RULERS[(floor(ac/30)+h-1)%12] if h and ac is not None else None
        dp=points.get(delegate,{})
        g=p['degree_in_sign']
        degree=floor(g)
        geometry=[]
        for target,q in points.items():
            if target==name or target not in set(RULERS)|{'Chiron','Ascendant','Midheaven'}:
                continue
            separation=abs((q['longitude_deg']-p['longitude_deg']+180)%360-180)
            angle=min(range(0,181,15),key=lambda a:abs(a-separation))
            geometry.append({'target':target,'separation_deg':separation,
                             'nearest_diagnostic_angle_deg':angle,'residual_deg':abs(separation-angle),
                             'status':'GEOMETRY_ONLY_NOT_DIRECTED_ASPECT'})
        stages=[
            {'stage':'planet','status':'supported_component','meaning':function,'record_id':record_id if name!='Chiron' else 'chiron-reviewed-vocabulary',
             'motion':'retrograde' if p.get('retrograde') else 'direct',
             'gradity':p.get('gradity',{}),'parent_convention':parent},
            {'stage':'house','status':'supported_component' if h else 'unavailable_unknown_time',
             'house':h,'field':p.get('field'),'meaning':records.get(f'field-{h:02d}',{}).get('meaning_summary') if h else None,
             'delegate':delegate,'delegate_retrograde':dp.get('retrograde'),
             'condition_note':'Delegate motion describes carriage elsewhere; it does not change occupant physical motion.',
             'record_id':'house-field','field_record_id':f'field-{h:02d}' if h else None},
            {'stage':'degree','status':'conflict','degree_in_sign':g,'canonical_spark':None,
             'house_parity_candidate':SIGNS[(degree+(6 if h%2==0 else 0))%12] if h else None,
             'sign_parity_candidate':SIGNS[(degree+(6 if (p['sign_index']+1)%2==0 else 0))%12],
             'meaning':None,'record_id':'spark-entry','missing_rule_ids':['D1']},
            {'stage':'decan','status':'supported_component','decan':p['decan'],'pulse':p['pulse'],
             'associated_planet':RULERS[SIGNS.index(p['pulse'])],
             'meaning':source['profiles']['sign-'+p['pulse'].lower()]['source_meaning'],
             'record_id':'tone-pulse','meaning_profile_id':'sign-'+p['pulse'].lower(),
             'relationship_type':'decan_refinement'},
            {'stage':'aspects','status':'incomplete','geometry':geometry,
             'directed_aspects':[],'record_id':'directional-context','missing_rule_ids':['D2'],
             'meaning':None},
            {'stage':'sign','status':'supported_component','tone':p['tone'],
             'meaning':source['profiles']['sign-'+p['tone'].lower()]['source_meaning'],
             'record_id':'sign-'+p['tone'].lower()},
            {'stage':'ruler','status':'structural_lookup','ruler':p['sign_ruler'],
             'assessment_ref':p['sign_ruler'] if p['sign_ruler'] in points else None,
             'record_id':'delegate-condition'}]
        ruled_signs=[SIGNS[i] for i,r in enumerate(RULERS) if r==name]
        occupants=[{'id':q['id'],'house':q.get('house'),'sign':q['sign'],
                    'retrograde':q.get('retrograde'),'group':q.get('group'),
                    'outgoing_emission':q.get('outgoing_emission'),
                    'assessment_ref':q['id'] if q['id'] in set(RULERS)|{'Chiron'} else None}
                   for q in points.values() if q['sign'] in ruled_signs]
        assessments[name]={'id':name,'position':p['display_dms'],'house':h,'stages':stages,
                           'complete_phsr':False,'composition_status':'CONDITIONAL_RESEARCH',
                           'delegate_payload':{'ruled_signs':ruled_signs,'occupants':occupants,
                                               'condition_complete':False},
                           'ruler_route':ruler_route(points,name)}
    route=ruler_route(points,start)
    return {'method_id':source['method_id'],'stage_order':ORDER,'root':start,
            'root_route':route,'assessments':assessments,
            'coverage':{'requested_objects':[p['id'] for p in chart['points']],
                        'unavailable_objects':[p['id'] for p in chart['points'] if not p.get('available')],
                        'delegate_condition_complete':False},
            'decisions':source['decisions'],'personal_report_approved':False,
            'sources':{'records':records,'profiles':source['profiles'],'source_commit':source['source_commit']}}
