"""Offline, review-only interpretation evidence; never a customer API or approval.

Uses the existing report calculator and pinned private core. The new operation
binds an eligible function to one of two inspected occupied-Field meanings.
It proposes a bounded theme, not a full-condition personal conclusion.
Private input/output MUST stay outside Git. No network or generative API is used.
"""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import html
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mystic_rebels.models import BirthInput
from mystic_rebels.profile_reports import ProfileRequest, generate_report, MAJORS
from nadia_runtime import verified_core

QUESTION = 'What is the ONE thing you need to feel loved that other people keep missing?'
# Finite source roles already examined by the existing thematic experiment.
FIELDS = {3: ('communication and thought', ['original-page-284']),
          7: ('connection and design', ['original-page-286', 'original-page-287'])}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def bounded_need(core, component, positions, ascendant, *, owner_id):
    """Small missing operation: ordered safety-function/Field proposal, not rank.

    The function is read from the verified core, the placement from its existing
    function_components output. This operation has no arbitrary text argument,
    house relabelling, inherited physical motion or personal approval path.
    """
    from nadia_core.interpretation import resolve
    from nadia_core.interpretation import function_components
    expected = next(c for c in function_components(core, positions, ascendant) if c['body'] == 'Moon')
    if digest(component) != digest(expected):
        raise ValueError('Participant differs from immutable calculated configuration')
    gate = resolve(core, ['phase4:function-moon', 'phase6:composition-links', 'phase6:claim-articulation'])
    placement = component['placement']
    target = FIELDS.get(placement['house'])
    if not owner_id or component['body'] != 'Moon':
        raise ValueError('Explicit chart owner and Moon component required')
    if component.get('personal_inference_allowed') is not False:
        raise ValueError('Unexpected function approval')
    eligible = gate['status'] == 'AVAILABLE' and target is not None
    return {'owner_id': owner_id, 'function': core.cross_chapter['planetary_functions']['Moon'],
            'placement': placement, 'gate': gate, 'field_component': target,
            'operation': 'function_operates_in_occupied_field',
            'theme': f"Emotional safety in the area of {target[0]}." if eligible else None,
            'source_refs': ['original-page-112', 'original-page-113', 'original-page-284', 'original-page-285'] + (target[1] if target else []),
            'eligible_for_bounded_proposal': eligible,
            'blockers': [] if eligible else gate.get('blockers', []) + ['occupied_field_meaning_not_inspected_by_this_finite_operation'],
            'required_for_personal_conclusion': ['complete_related_condition_return', 'question_specific_relevance_adjudication', 'reported_experience', 'claim_level_semantic_review'],
            'ranking': None, 'personal_reading_allowed': False}


def build_review(birth, owner_id, *, synthetic=False):
    core = verified_core()
    report = generate_report(ProfileRequest(birth=birth, synthetic=synthetic))
    if report['readiness']['knowledge_status'] != 'verified':
        raise ValueError('Verified source components required; no fallback')
    from nadia_core.interpretation import function_components
    from nadia_core.synthesis import compose, validate_composition
    from nadia_core.methodology import context_graph
    points = {p['id']: p for p in report['chart']['points'] if p['id'] in MAJORS and p['available']}
    asc = report['chart']['angles'].get('Ascendant')
    if asc is None or len(points) != 10:
        raise ValueError('This review requires the complete major-body map and sufficiently precise time')
    positions = {b: points[b]['longitude_deg'] for b in MAJORS}
    record = {'ascendant': asc, 'utc': report['chart']['time']['birth_utc'],
              'positions': {b: {'longitude': positions[b], 'retrograde': points[b]['retrograde'],
                    'longitude_speed_deg_day': points[b]['speed_longitude_deg_per_day']} for b in MAJORS}}
    motion = {'bodies': {}}
    unresolved_motion = {}
    for body, point in points.items():
        grade = point.get('gradity', {})
        phase = (grade.get('phase') or '').casefold()
        if grade.get('status') == 'NOT_APPLICABLE' and body in {'Sun', 'Moon'}:
            motion['bodies'][body] = {'body':body,'phase':'NOT APPLICABLE','when':record['utc']}
        elif grade.get('status') == 'VERIFIED' and phase in {'pregrade','postgrade','prograde','retrograde'}:
            motion['bodies'][body] = {'body':body,'phase':phase,'when':record['utc']}
        else:
            unresolved_motion[body] = deepcopy(grade)
    composition = compose(core, record, QUESTION, owner_id, motion=motion)
    validation = validate_composition(core, composition, record, QUESTION, owner_id, motion=motion)
    if not validation['valid']:
        raise ValueError('Existing composition failed independent recomputation')
    components = function_components(core, positions, asc)
    moon = next(c for c in components if c['body'] == 'Moon')
    proposal = bounded_need(core, moon, positions, asc, owner_id=owner_id)
    profiles = json.loads((ROOT/'data/knowledge/source_meaning_profiles.json').read_text(encoding='utf-8'))
    tone = next(p for p in profiles['profiles'] if p['id'] == 'sign-' + moon['placement']['tone'].lower())
    tone_refs = ['original-page-'+str(page) for c in tone['citations'] for page in c['original_printed_pages']]
    graph = context_graph(positions, asc)
    extended = None
    if not synthetic:
        from mystic_rebels.service import calculate, object_catalog
        extended = calculate(birth.model_copy(update={'objects':[p['id'] for p in object_catalog()['objects']]}))
    claims = []
    def claim(identity, kind, text, facts, refs, operation, missing=()):
        claims.append({'id':identity,'kind':kind,'text':text,'fact_refs':facts,
                       'source_refs':refs,'operation':operation,'missing_conditions':list(missing),
                       'customer_publication_allowed':False})
    for b in MAJORS:
        p=points[b]; component=next(c for c in components if c['body']==b)
        claim('fact:'+b,'calculated_fact',f"{b}: {p['display_dms']}; occupied house {p['house']}; own motion {'retrograde' if p['retrograde'] else 'direct'}.",
              ['chart.points.'+b],[], 'existing_calculation_service')
        claim('meaning:'+b,'explicit_source_meaning',f"{b} function: {component['function']}; vocabulary: {', '.join(component['source_keywords'])}.",
              ['components.'+b],component['source_refs'],'existing_eligible_function_component')
    for c in composition['claims']:
        claim(c['claim_id'],'source_scoped_context_component',c['sentence'],
              ['composition.claims.'+c['claim_id']],list(c['source_passages']),'existing_synthesis_compose',c['missing_dependencies'])
    if proposal['theme']:
        claim('theme:Moon-field','bounded_thematic_proposal',proposal['theme'],
              ['fact:Moon','meaning:Moon'],proposal['source_refs'],'function_operates_in_occupied_field',proposal['required_for_personal_conclusion'])
    claim('tone:Moon','explicit_source_vocabulary',tone['source_meaning'],['fact:Moon'],
          tone_refs,
          'source_vocabulary_not_personal_manifestation', ['full_tone_pulse_and_related_condition_integration'])
    field = moon['placement']['house']
    if proposal['theme'] and field == 3:
        recognition = ('A need worth testing is space to put your feelings into words and feel that another person has understood what you mean.')
        if moon['placement']['tone'] == 'Pisces':
            recognition += ' A reflective conversation, with room for an image, a memory or an unfinished thought, is one specific possibility to explore.'
        explanation = ('The source associates emotional safety with the Moon. Here its occupied area concerns communication and thought. '
            'That supports exploring whether being understood helps you feel secure. It does not establish that you are highly talkative, '
            'that your partner dismisses you, or that this outranks every other need. '
            f"The source vocabulary for the expression layer is: {tone['source_meaning']} "
            'Choosing a particular lived expression from those themes remains interpretive judgment.')
        exercise = [
            'Only if this hypothesis fits your experience, choose one recent, ordinary conversation when you wanted to feel close.',
            'Separate what was actually said from what you felt it meant. Leave room for the other person to explain their intention.',
            'Try a specific request: “Let me find the words first, then tell me what you understood before we move to solutions.”',
            'Compare whether the exchange helped you feel understood, or whether quiet company, practical help or another response mattered more. Record a counterexample; discard or revise the hypothesis if it fits poorly.'
        ]
    elif proposal['theme'] and field == 7:
        recognition = 'A need worth testing is participation in shaping how closeness works between you, rather than accepting an arrangement without discussing it.'
        explanation = ('The safety function is operating in the inspected area of connection and design. This changes the proposed theme from communication itself to how a connection is formed. '
                       f"Its expression vocabulary is {tone['source_meaning']} No rule here makes this your single dominant need.")
        exercise = ['If this fits, choose one small shared expectation and ask to design it together.',
                    'Record whether participation itself helped, and a counterexample where a different response mattered more. This is not a guaranteed outcome.']
    else:
        recognition = 'This finite operation cannot responsibly select a personalized need for this configuration.'
        explanation = f"The occupied house is {field}, outside the two inspected Field meanings used by this operation. The full evidence remains available; a generic interpretation is not substituted."
        exercise = []
    claim('hypothesis:need','contextual_hypothesis',recognition,
          (['theme:Moon-field','tone:Moon'] if proposal['theme'] else ['fact:Moon','tone:Moon']),proposal['source_refs']+tone_refs+['original-page-211','original-page-102'],
          'question_lens_and_proposed_articulation', proposal['required_for_personal_conclusion'])
    for cid, text, why in [
        ('exclusive','This is your ONE greatest need.','No verified topic-specific selection or dominance rule establishes exclusivity.'),
        ('history','Other people repeatedly miss this need.','No personal interaction history was supplied; the question is not evidence that this happened.'),
        ('rx','The Moon is physically retrograde because its ruler is retrograde.','Own motion and Delegate motion are distinct; fact:Moon records direct motion.'),
        ('contact','The Moon and its ruler have a verified trine because they are linked by rulership.','A ruler link is not a verified planetary contact; use the actual contact inventory.'),
    ]:
        claim('reject:'+cid,'rejected_personal_assertion',text,['fact:Moon'],['original-page-102','original-page-187','original-page-211'], 'reject_unsupported_transition',[why])
    claim('exercise','adaptation', ' / '.join(exercise) if exercise else 'No configuration-specific exercise proposed.',
          ['hypothesis:need'], ['original-page-102','original-page-445','original-page-942','original-page-969','original-page-970'],
          'newly_designed_conditional_exercise_not_a_Logan_protocol', ['usefulness_not_tested_with_person','no_claim_of_manifested_outcome'])
    links_by_body = {b:[l['id'] for l in composition['links'] if b in l['participants']] for b in MAJORS}
    relevance = [{'body':b,'function':core.cross_chapter['planetary_functions'][b]['label'],
        'decision':'provisional_security_focus_not_exclusive' if b=='Moon' else 'connected_context_candidate_not_assigned_a_weight',
        'why':'Safety directly matches the security part of the question; source112–113. Lens choice is judgment, not a ranking theorem.' if b=='Moon' else
              'Evaluate the actual linked configuration under the relationship Lens; function or graph connectivity alone does not establish its contribution or priority.',
        'actual_link_ids':links_by_body[b],'weight':None} for b in MAJORS]
    moon_node = next(n for n in composition['nodes'] if n['body']=='Moon')
    trace = {
        'before': {'meaning':'Emotional safety; no individual love preference yet established.', 'claim_ids':['meaning:Moon']},
        'contributions': [
            {'kind':'occupied_Field','facts':moon['placement'],'status':'bounded_function_field_combination_only', 'source_refs':proposal['source_refs']},
            {'kind':'Tone','facts':tone['source_meaning'],'status':'vocabulary_supported_personal_expression_requires_judgment','source_refs':tone_refs},
            {'kind':'Pulse_and_degree','facts':{k:moon['placement'][k] for k in ['degree_in_sign','decan','pulse','spark','spark_status']},
             'status':'calculated_Pulse_not_an_independent_duplicate_vote; Spark_unknown; contextual_effect_not_assessed'},
            {'kind':'represented_occupants','facts':moon_node['delegated_houses'],'status':'actual_links_assessed_structurally; returned_meaning_not_established'},
            {'kind':'own_and_Delegate_motion','facts':moon_node['own_condition'],'status':'separate_source_operations; no_personality_inferred'},
            {'kind':'rulers_and_contacts','facts':composition['links'],'status':'all_major_links_recorded; complete_participant_return_not_established'}],
        'after':{'bounded_theme':proposal['theme'],'proposed_personal_articulation':recognition,'complete_answer':False},
        'why': 'Source112–113 supplies safety; occupied Field3 or7 supplies its inspected area; source284–287 permits an ordered thematic combination. Source211 permits a question Lens but not a unique ranking. Source285 and102 prevent treating this partial combination as a completed life assessment.',
        'weighting':'No equal-factor sum or invented dominance score. Provisional focus is analyst judgment. Other connected factors are unresolved contributions, not zero-weight factors.'}
    return {'scope':'INTERNAL_REVIEW_ONLY_NOT_CUSTOMER_READING','question':QUESTION,'owner_id':owner_id,
            'report':report,'calculated_record':record,'calculated_record_sha256':digest(record),
            'components':components,'context_graph':graph,'composition':composition,
            'motion_input':motion,'unresolved_motion':unresolved_motion,
            'extended_calculated_chart':extended,
            'extended_scope':'Existing catalogue geometry only; the major-only source contact consumer does not certify contacts or contextual meaning for additional bodies.',
            'composition_recomputation':validation,'relevance_decisions':relevance,'bounded_proposal':proposal,
            'reasoning_trace':trace,
            'claims':claims,'draft':{'recognition':recognition,'explanation':explanation,'practical_application':exercise,
                'practical_source_rationale': [
                    'Alchemizing, p445: usefulness depends on context; the adaptation changes how a conversation is used rather than labelling a reflective style good or bad.',
                    'Manifestation, p942: the author discusses intentional focus and action. The adaptation makes a concrete request; it does not adopt a cosmic guarantee, blame a person for unmet needs, or promise affection.',
                    'Free Will, pp969–970: preserve personal agency. The person can reject this hypothesis or prefer a different way of connecting; the chart is not a command.'],
                'exercise_status':'new_adaptation_conditional_on_hypothesis_not_source_prescription'},
            'missing_operations':['source_constrained_return_of_assessed_related_meanings',
                'question_specific_relevance_and_priority_adjudication','personal_context_confirmation'],
            'complete_personal_interpretation':False,'personal_readings_approved':False,
            'review_status':'unreviewed_no_qualified_practitioner_approval','generator':'controlled_offline_composition_no_generative_model',
            'limits':['Theme change is not proof of a correct personalized interpretation.',
                      'All ten major configurations are assessed structurally; additional bodies and unknown contact reach are not thereby excluded.',
                      'Practical chapter references are informational teachings, not activated personal-outcome rules.']}


def render(review):
    e=html.escape; d=review['draft']
    styles=(ROOT/'web/src/profileReport.css').read_text(encoding='utf-8')
    body=f'<header class="nadia-report-cover"><div><p>NADIA · Internal review only</p><h1>{e(review["report"]["profile"]["name"])}</h1><p>Unapproved interpretation hypothesis. Do not publish or deliver as a completed reading.</p></div></header>'
    for title,text in [('Recognition',d['recognition']),('Explanation',d['explanation'])]:
        body+=f'<section class="nadia-report-introduction"><h2>{title}</h2><p>{e(text)}</p></section>'
    body+='<section class="nadia-report-introduction"><h2>Practical application</h2><p>New adaptation, conditional on the hypothesis. Not a source-prescribed protocol or an outcome guarantee.</p><ol>'
    body+=''.join('<li>'+e(s)+'</li>' for s in d['practical_application'])+'</ol></section>'
    if d.get('practical_source_rationale'):
        body+='<section class="nadia-report-introduction"><h3>Why this application</h3>'+''.join('<p>'+e(s)+'</p>' for s in d['practical_source_rationale'])+'<p>These are author-teaching references, not activated natal-outcome rules. The exercise itself is a new adaptation.</p></section>'
    body+='<section class="nadia-report-introduction"><h2>What this does not establish</h2><p>Neither the single most important need nor a history of other people missing it is established. Connected ruler/occupant/contact meanings have not been returned as a complete contextual assessment. No qualified practitioner or personal feedback has validated this proposal.</p></section>'
    body+='<section class="nadia-report-introduction"><h2>Claim-by-claim reasoning record</h2>'
    for c in review['claims']:
        body+=f'<section class="nadia-report-section"><h3>{e(c["id"])} · {e(c["kind"])}</h3><p>{e(c["text"])}</p><p>Operation: {e(c["operation"])}. Facts: {e(", ".join(c["fact_refs"]))}.</p><p>Sources: {e(", ".join(c["source_refs"])) or "Existing calculation service; full numerical record in JSON"}.</p><p>Missing: {e("; ".join(c["missing_conditions"])) or "None for this bounded statement; no personal inference approved"}.</p></section>'
    body+='</section>'
    return '<!doctype html><html><head><meta charset="utf-8"><title>NADIA internal review</title><style>'+styles+'body{margin:0}.nadia-report-introduction li{margin:12px 0;line-height:1.6}@media print{.nadia-report-cover{display:block}.nadia-report-introduction{padding:5mm 7mm}.nadia-report-section{break-inside:avoid}}</style></head><body class="nadia-report-app"><article class="nadia-report-document">'+body+'</article></body></html>'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,help='Private report JSON or BirthInput; never commit this data')
    parser.add_argument('--output',default='tmp/first-personal')
    args=parser.parse_args()
    out=Path(args.output).resolve()
    if not out.is_relative_to((ROOT/'tmp').resolve()):
        raise ValueError('Private output must stay in ignored consumer tmp')
    out.mkdir(parents=True,exist_ok=True)
    raw=json.loads(Path(args.input).read_text(encoding='utf-8'))
    birth=BirthInput.model_validate(raw['chart']['input'] if 'chart' in raw else raw)
    synthetic=[BirthInput(name='Synthetic A',local_date='2000-01-01',local_time='12:00:00',timezone='Etc/UTC',latitude=51.4779,longitude=0,location_name='Constructed Greenwich fixture'),
       BirthInput(name='Synthetic B',local_date='1984-05-15',local_time='06:30:00',timezone='Australia/Sydney',latitude=-33.8688,longitude=151.2093,location_name='Constructed Sydney fixture'),
       BirthInput(name='Synthetic C',local_date='2005-10-09',local_time='18:45:00',timezone='Atlantic/Reykjavik',latitude=64.1466,longitude=-21.9426,location_name='Constructed Reykjavik fixture')]
    results=[]
    for identity,b in [('target',birth)]+[(f'synthetic-{i+1}',b) for i,b in enumerate(synthetic)]:
        result=build_review(b,identity,synthetic=identity!='target')
        (out/(identity+'.json')).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (out/(identity+'.html')).write_text(render(result),encoding='utf-8')
        results.append({'id':identity,'record_sha256':result['calculated_record_sha256'],
            'moon':result['bounded_proposal']['placement'],'theme':result['bounded_proposal']['theme'],
            'recognition':result['draft']['recognition'],'complete_personal_interpretation':False})
    (out/'comparison.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(results))


if __name__=='__main__':main()
