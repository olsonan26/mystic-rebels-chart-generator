"""Conditional research prose, separate from calculated facts and reported events."""
TOPICS = {
    'trust': {'title':'Trust and boundaries','root':'Chiron',
              'question':'What would make a close or shared arrangement workable for your own needs?'},
    'voice': {'title':'Voice and emotional needs','root':'Moon',
              'question':'Which words or forms of expression help you recognize what you need?'},
    'autonomy': {'title':'Autonomy and worth','root':'Saturn',
                 'question':'Which structure supports your own actions, and which standard needs revision?'},
    'year': {'title':'Yearly direction','root':'Sun',
             'question':'How can the year’s practical approach leave room for your own direction and support?'}
}

FIELD_CONTEXT = {
    1:'your own actions and autonomy',2:'worth, resources and what you value',
    3:'words, perception and your immediate surroundings',4:'home, care and personal safety',
    5:'play, purpose and personal expression',6:'habits, details and daily responsibilities',
    7:'relationships, exchange and the value you express outwardly',
    8:'shared trust, intimate involvement and what remains private',
    9:'experience, learning and beliefs',10:'structure, accomplishment and public responsibilities',
    11:'groups, networks and making existing systems work better',
    12:'the unknown, imagination and what can be released'
}
FUNCTIONS = {
    'Chiron':'whether an established expectation actually accommodates you',
    'Sun':'room to exist, create and express your own purpose',
    'Moon':'what feels familiar and what meets your emotional needs',
    'Mercury':'how you perceive information and give it words',
    'Venus':'what you value and how exchange can be fair',
    'Mars':'how you can act and assert yourself',
    'Jupiter':'what experience teaches you and which beliefs you develop',
    'Saturn':'which boundaries and responsibilities are workable',
    'Uranus':'what needs revision and how a better system could work',
    'Neptune':'how to approach uncertainty, imagination and meaning',
    'Pluto':'how to understand hidden material, power and deep involvement'
}

def build_reading(packet,topic,annual):
    meta=TOPICS[topic]
    assessments=packet['assessments']
    root=assessments.get(meta['root'])
    paragraphs=[]
    evidence=[]
    if root is None:
        paragraphs.append('The starting factor is unavailable, so this topic cannot yet be assembled.')
    elif root['house'] is None:
        paragraphs.append('A birth time is needed to place this question in its personal life context. The calculated sky positions remain available, while a house-based reading is withheld.')
    else:
        route=root['ruler_route']
        for i,name in enumerate(route['path']):
            a=assessments.get(name)
            if not a:continue
            field=FIELD_CONTEXT.get(a['house'],'an unresolved life context')
            ruler=a['stages'][-1]['ruler']
            s=a['stages']
            motion=' This factor is retrograde, so inward review is part of the documented interpretation; it does not establish an event.' if s[0]['motion']=='retrograde' else ''
            lead='Begin by considering ' if i==0 else 'Following that connection brings attention to '
            paragraph=lead+FUNCTIONS[name]+' in '+field+'.'+motion
            if name=='Chiron':paragraph+=' The question is how the arrangement could fit you better, rather than whether you should force yourself to satisfy it.'
            if name=='Sun':paragraph+=' The father-related convention can be explored here without assuming anything about a particular parent’s conduct.'
            if name=='Moon':paragraph+=' Familiarity and safety are separate questions; the mother-related convention does not tell us what actually happened.'
            paragraph+=' Its decan adds this refinement: '+s[3]['meaning']+' Its sign colors the expression this way: '+s[5]['meaning']
            if ruler in assessments:
                paragraph+=' The next connection concerns '+FUNCTIONS[ruler]+' in '+FIELD_CONTEXT.get(assessments[ruler]['house'],'an unresolved life context')+'.'
            paragraphs.append(paragraph)
            evidence.append({'assessment_id':name,'stage_refs':list(range(7)),
                             'claim_kind':'COMPOSED_HYPOTHESIS','not_observed_biography':True})
        if route['cycle']:
            paragraphs.append('The route returns to a factor already assessed. Keep those questions connected without counting their repetition as extra confirmation or a stronger prediction.')
    if annual:
        f=annual['fields']
        values=', '.join(k.upper()+' '+ '/'.join(map(str,f[k]['trail'])) for k in ['ess','py','com'])
        paragraphs.append(str(annual['year'])+' adds three distinct yearly roles: '+values+'. Essence is the experiential frame, Personal Year is the annual cycle, and the Combiner supplies an approach. The source’s category-specific text is available separately; it is not evidence of what happened.')
    return {'topic':topic,'title':meta['title'],'paragraphs':paragraphs,'question':meta['question'],
            'claim_kind':'COMPOSED_HYPOTHESIS','claim_evidence':evidence,
            'reported_history_used':False,'complete_phsr':False,
            'scope':'Conditional research reflection. Degree-entry meaning and the full directed aspect stage remain unresolved.'}
