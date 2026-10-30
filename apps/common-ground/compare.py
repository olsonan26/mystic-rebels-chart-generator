"""Deterministic contextual comparison, with transparent proposed bridges.

This never enables a blocked PURE calculation or claims empirical associations.
Planet presence alone is not a match: every ordinary natal chart includes them.
"""
from sources import number_vocabulary, role_vocabulary, source_pack, source_record

# All cross-system links below are new analyst proposals. Ingredient vocabulary
# is separately attributed in the frozen source pack, not falsely cited as a bridge.
BRIDGES = {
    1: {'theme': 'initiative and independent direction', 'planet': 'Mars', 'other': 'Sun', 'tags': ['initiative', 'purpose'], 'question': 'What changes when beginning something is separated from deciding what it is for?'},
    2: {'theme': 'cooperation, detail and fair exchange', 'planet': 'Venus', 'other': 'Mercury', 'tags': ['connection', 'fairness', 'precision'], 'question': 'When do careful standards support cooperation, and when does each need its own attention?'},
    3: {'theme': 'creative expression and communication', 'planet': 'Sun', 'other': 'Mercury', 'tags': ['expression', 'communication'], 'question': 'Is the useful distinction creative self-expression, sharing information, or making space for both?'},
    4: {'theme': 'durable structure and careful method', 'planet': 'Saturn', 'other': 'Mercury', 'tags': ['structure', 'precision', 'tangible'], 'question': 'Where is a dependable method useful, and where would room for revision help it work better?'},
    5: {'theme': 'exploration, adaptability and learning through experience', 'planet': 'Jupiter', 'other': 'Mercury', 'tags': ['exploration', 'options', 'communication', 'innovation'], 'question': 'Does variety become useful experience through exploration, communication, or a practical method?'},
    6: {'theme': 'care, responsibility and stewardship', 'planet': 'Moon', 'other': 'Venus', 'tags': ['nurture', 'connection', 'responsibility'], 'question': 'Which part of care matters in this context: emotional safety, reciprocal connection, practical organization or responsibility?'},
    7: {'theme': 'analysis, depth and inquiry', 'planet': 'Mercury', 'other': 'Pluto', 'tags': ['analysis', 'precision', 'depth', 'unknown'], 'question': 'When is careful analysis enough, and when does the question call for deeper investigation or tolerance of uncertainty?'},
    8: {'theme': 'executive strategy, authority and outcomes', 'planet': 'Saturn', 'other': 'Venus', 'tags': ['authority', 'structure', 'resources', 'power'], 'question': 'How would a useful outcome balance responsibility, resources and the way authority is exercised?'},
    9: {'theme': 'service, wider perspective and release', 'planet': 'Neptune', 'other': 'Jupiter', 'tags': ['service', 'collective', 'release', 'worldview'], 'question': 'What would distinguish practical help, a wider contribution and a necessary completion in this context?'},
}

SIGN_TAGS = {
    'Aries': ['initiative'], 'Taurus': ['tangible', 'resources'], 'Gemini': ['communication', 'options'],
    'Cancer': ['nurture', 'needs'], 'Leo': ['expression', 'purpose'], 'Virgo': ['analysis', 'precision', 'service'],
    'Libra': ['connection', 'fairness'], 'Scorpio': ['depth', 'power'], 'Sagittarius': ['exploration', 'worldview'],
    'Capricorn': ['structure', 'authority', 'responsibility'], 'Aquarius': ['innovation', 'collective', 'communication'],
    'Pisces': ['unknown', 'release'],
}
HOUSE_TAGS = {
    1: ['initiative'], 2: ['resources'], 3: ['communication', 'options'], 4: ['nurture', 'needs'],
    5: ['expression', 'purpose'], 6: ['precision', 'service'], 7: ['connection', 'fairness'],
    8: ['depth', 'power'], 9: ['exploration', 'worldview'], 10: ['structure', 'authority', 'responsibility'],
    11: ['innovation', 'collective'], 12: ['unknown', 'release'],
}
TAG_LABELS = {'initiative': 'initiative', 'purpose': 'purpose', 'connection': 'connection', 'fairness': 'fair exchange',
    'precision': 'careful refinement', 'expression': 'creative expression', 'communication': 'communication',
    'structure': 'structure', 'tangible': 'making things tangible', 'exploration': 'exploration and experience',
    'options': 'alternative options', 'innovation': 'innovation', 'nurture': 'nurture', 'responsibility': 'responsibility',
    'analysis': 'analysis', 'depth': 'hidden depth', 'unknown': 'the unknown', 'authority': 'authority',
    'resources': 'resources and worth', 'power': 'power', 'service': 'practical service', 'collective': 'collective participation',
    'release': 'release', 'worldview': 'wider perspective', 'needs': 'personal needs'}

ROLE_CONTEXT = {
    'Soul Urge': 'the vowel-based inner-motivation lens',
    'Expression': 'the full-name expression lens',
    'Called Name': 'the first-and-last-name social-presentation lens',
    'Birth Force': 'the birth-date digit-sum lens',
    'Ultimate Goal': 'the combined name-and-birthday direction lens',
    'Balance Number': 'the initials-based coping-response lens',
}

ROLE_DISTINCTIONS = {
    'Soul Urge': 'This source bank frames its theme as an inner motive: what is wanted or found meaningful.',
    'Expression': 'This source bank frames its theme as a way of expressing and applying ability.',
    'Called Name': 'This source bank concerns possible social reception, separate from what is privately wanted.',
    'Birth Force': 'This date-based source bank describes possible approaches and capacities, separate from a name-derived motive.',
    'Ultimate Goal': 'The selected source bank treats its theme as an organizing direction or journey.',
    'Balance Number': 'This source bank concerns a possible response to a challenge, rather than a general identity.',
}

FIVE_ROLE_DISTINCTIONS = {
    'Soul Urge': 'Its role-specific bank describes freedom and exploration as motives, with intentional variety and clear constraints as balancing themes.',
    'Expression': 'Its role-specific bank describes outward adaptability, connecting with people and expressing a catalyst-for-change theme.',
    'Called Name': 'Its role-specific bank emphasizes how versatility, public-facing communication and quick responses may be received by others.',
    'Birth Force': 'Its role-specific bank emphasizes practical experience and knowledge gained by contact with different people and situations.',
    'Ultimate Goal': 'Its selected direction bank connects adventure and adaptability with opening possibilities and encouraging freedom for others.',
    'Balance Number': 'Its role-specific bank asks for attention to the problem and a creative response rather than avoidance.',
}

def _role_distinction(role, digit):
    return FIVE_ROLE_DISTINCTIONS.get(role, ROLE_DISTINCTIONS[role]) if digit == 5 else ROLE_DISTINCTIONS[role]

def _role_question(role, bridge, context):
    arena = context['field_meaning'].lower() if context['house'] else 'the available planetary context'
    theme = bridge['theme']
    return {
        'Soul Urge': f'What would make {theme} feel internally worthwhile in matters of {arena}?',
        'Expression': f'How could {theme} be expressed usefully in matters of {arena}?',
        'Called Name': f'How might {theme} be received by others in matters of {arena}, and what would make the intended message clear?',
        'Birth Force': f'Which part of {theme} could offer a useful approach to matters of {arena}?',
        'Ultimate Goal': f'What organizing direction could connect {theme} with matters of {arena} over the longer term?',
        'Balance Number': f'When a challenge involves {arena}, how might {theme} inform a considered response?',
    }[role]

def _root(value):
    value = int(value)
    while value > 9:
        value = sum(int(ch) for ch in str(value))
    return value

def _metric(numerology, role):
    rows = numerology.get('core_numbers', numerology.get('metrics', []))
    return next((row for row in rows if row.get('role', row.get('name')) == role or row.get('name') == role), None)

def _point(chart, planet):
    return next((row for row in chart.get('points', []) if row.get('id') == planet and row.get('available')), None)

def _reference_only(chart):
    return bool(chart.get('time', {}).get('time_is_reference_only') or chart.get('input', {}).get('time_accuracy') == 'unknown')

def _statement(source_id):
    return source_record(source_id)['statement']

def _field_text(house):
    return _statement(f'mr:field-{house:02d}').removeprefix('The source life-area sequence includes: ').rstrip('.')

def _context(chart, planet):
    point = _point(chart, planet)
    if point is None:
        return None
    reference = _reference_only(chart)
    house = None if reference else point.get('house')
    tone = point.get('tone', point.get('sign'))
    pulse = point.get('pulse')
    ids = [f'mr:meaning-{planet.lower()}', 'mr:placements']
    if house:
        ids.append(f'mr:field-{int(house):02d}')
    if tone in SIGN_TAGS:
        ids.append('mr:sign-' + tone.lower())
    if pulse in SIGN_TAGS:
        ids.append('mr:sign-' + pulse.lower())
    tags = [] if reference else list(dict.fromkeys(HOUSE_TAGS.get(house, []) + SIGN_TAGS.get(tone, []) + SIGN_TAGS.get(pulse, [])))
    return {'planet': planet, 'point': point, 'house': house, 'tone': tone, 'pulse': pulse,
        'true_placement': None if reference else point.get('true_placement'),
        'field_meaning': _field_text(int(house)) if house else None,
        'planet_meaning': _statement(f'mr:meaning-{planet.lower()}'),
        'tone_meaning': _statement('mr:sign-' + tone.lower()) if tone in SIGN_TAGS else None,
        'pulse_meaning': _statement('mr:sign-' + pulse.lower()) if pulse in SIGN_TAGS else None,
        'source_ids': list(dict.fromkeys(ids)), 'tags': tags, 'reference_only': reference}

def _placement_line(context):
    place = f"House {context['house']} ({context['true_placement']} Field)" if context['house'] else 'no available house/Field'
    return f"{context['planet']} in {place}, with {context['tone']} Tone and {context['pulse']} Pulse"

def _context_text(context):
    if context['reference_only']:
        return 'The birth time is unknown. The chart uses local noon only as a reference; houses and precise birth-context comparisons are withheld.'
    arena = f"Its House {context['house']} field concerns {context['field_meaning'].lower()}. " if context['house'] else 'A house-based life area is unavailable. '
    tone = f"The sourced {context['tone']} Tone vocabulary is {context['tone_meaning'][0].lower() + context['tone_meaning'][1:]} " if context['tone_meaning'] else ''
    if context['pulse'] == context['tone']:
        pulse = 'Pulse repeats that same sign vocabulary; this is a derived refinement, not another independent confirmation.'
    else:
        pulse = f"The {context['pulse']} Pulse adds {context['pulse_meaning'][0].lower() + context['pulse_meaning'][1:]}" if context['pulse_meaning'] else ''
    return arena + tone + pulse

def _display_text(role, value, digit, bridge, context, shared):
    """Keep the main reading legible; complete ingredient text remains inspectable."""
    if context['reference_only']:
        return (f"{role} {value} brings {bridge['theme']} into the number comparison. "
            'The birth time is unknown, so local-noon positions remain reference data. A precise life-area comparison needs a resolved time.'), 'What birth-time range can be documented for a later contextual comparison?'
    opening = f"{role} {value} brings {bridge['theme']} into focus. " + _role_distinction(role, digit) + ' '
    if value in (11, 22, 33):
        opening += f"The calculation keeps {value}; the wording here uses root {digit}. "
    field = (f"The proposed counterpart is {context['planet']} in House {context['house']}: {context['field_meaning'].lower()}. "
        if context['house'] else f"The proposed counterpart is {context['planet']}; a house-based life area is unavailable. ")
    tone = f"Its {context['tone']} Tone contributes {context['tone_meaning'][0].lower() + context['tone_meaning'][1:]} " if context['tone_meaning'] else ''
    pulse = (f"The {context['pulse']} Pulse refines that expression with {context['pulse_meaning'][0].lower() + context['pulse_meaning'][1:]} "
        if context['pulse_meaning'] and context['pulse'] != context['tone'] else 'Tone and Pulse use the same sign vocabulary here. ')
    ending = ('The contextual link to explore is ' + ', '.join(shared) + '.' if shared
        else 'These ingredients introduce different emphases; the useful question is how they might work together.')
    parts = [opening, field, tone, pulse, ending]
    # Omit the longest optional refinement rather than cut a sentence mid-thought.
    if len(''.join(parts).split()) > 120:
        parts[3] = ''
    text = ''.join(parts).strip()
    field_question = _role_question(role, bridge, context)
    return text, field_question

def _insight(chart, metric, domain, suffix='', use_other=False, fixed_planet=None, purpose=None):
    if metric is None:
        return None
    value = int(metric['value'])
    digit = _root(value)
    if digit not in BRIDGES:
        return None
    bridge = BRIDGES[digit]
    planet = fixed_planet or bridge['other' if use_other else 'planet']
    context = _context(chart, planet)
    role = metric.get('role', metric.get('name', 'Number'))
    role_source = role_vocabulary(role, digit)
    source_ids = ['costar-natal-calculations', f'costar-number-{digit}', role_source['id'], 'bridge-method-v1']
    if digit == 5:
        source_ids.append('costar-first_name_total_flavor-5')
    if role == 'Called Name':
        source_ids.append(f'costar-called_name_vibe-{digit}')
    master_note = f"The calculation retains {value}; this comparison explicitly uses its {digit} root vocabulary because the selected natal bank has no distinct master interpretation. " if value in (11, 22, 33) else ''
    ingredient = {'system': 'Numerology', 'role': role, 'value': value, 'root_used_for_vocabulary': digit,
        'compound': metric.get('compound'), 'raw': metric.get('raw'), 'calculation': metric.get('calculation'),
        'meaning': f"The {role} {digit} bank's attributed wording (not an observed fact about this person): " + role_source['statement'],
        'number_theme': number_vocabulary(digit)['essence'], 'role_meaning': role_source['statement'],
        'role_meaning_source_id': role_source['id'], 'role_distinction': _role_distinction(role, digit),
        'source_ids': source_ids[:3],
        'master_fallback_explicit': value in (11, 22, 33)}
    if context is None:
        return {'id': f'{domain}-{role.lower().replace(" ", "-")}{suffix}', 'title': f'{role} {value}: chart context unavailable',
            'relationship': 'proposed_contextual_comparison', 'numerology_role': role, 'number': value, 'planet': planet,
            'paragraph': f'{role} {value} is available, but {planet} was unavailable in this chart. No replacement chart context is invented.',
            'question': 'Would a corrected or more complete birth input make this comparison available?',
            'display_paragraph': f'{role} {value} is calculated, but its proposed {planet} context is unavailable. The number ingredients remain visible for review.',
            'display_question': 'Would more complete birth input make this contextual comparison available?',
            'source_ids': source_ids, 'ingredients': [ingredient], 'availability': 'chart_context_unavailable', 'shared_contextual_themes': []}
    source_ids += context['source_ids']
    function = context['planet_meaning'][0].lower() + context['planet_meaning'][1:]
    base = (f"{role} {value} is {ROLE_CONTEXT.get(role, 'a separate numerology lens')}; the selected number vocabulary concerns {bridge['theme']}. "
        + _role_distinction(role, digit) + ' '
        + master_note + f"This proposed comparison places it beside {_placement_line(context)}. The planetary function concerns {function} ")
    shared = [TAG_LABELS[tag] for tag in bridge['tags'] if tag in context['tags']]
    if context['reference_only']:
        paragraph = (f"{role} {value} retains its number calculation and selected vocabulary: {bridge['theme']}. " + master_note + _context_text(context))
        availability = 'reference_epoch_only'
        pattern = 'withheld_due_to_unknown_time'
        question = 'What is the documented birth time, or what time uncertainty should be retained for a later contextual comparison?'
    else:
        qualifier = (f"The proposed contextual overlap is {', '.join(shared)}. " if shared
            else 'The selected chart context introduces different emphases rather than an obvious repeated contextual theme. ')
        paragraph = base + _context_text(context) + ' ' + qualifier
        if purpose:
            paragraph += purpose + ' '
        paragraph += 'This combines attributed ingredients into a question to investigate; it does not establish a personal trait or validate a number–planet equivalence.'
        availability = 'contextual_comparison_available'
        pattern = 'candidate_shared_context' if shared else 'different_contexts'
        question = _role_question(role, bridge, context)
    astrology_ingredient = {'system': 'Astrology', 'planet': planet, 'house': context['house'],
        'true_placement': context['true_placement'], 'tone': context['tone'], 'pulse': context['pulse'],
        'longitude_deg': context['point'].get('longitude_deg'), 'display_dms': context['point'].get('display_dms'),
        'retrograde': context['point'].get('retrograde'), 'sign_ruler': context['point'].get('sign_ruler'),
        'planet_meaning': context['planet_meaning'], 'field_meaning': context['field_meaning'],
        'tone_meaning': context['tone_meaning'], 'pulse_meaning': context['pulse_meaning'],
        'reference_only': context['reference_only'], 'source_ids': context['source_ids']}
    display_paragraph, display_question = _display_text(role, value, digit, bridge, context, shared)
    return {'id': f'{domain}-{role.lower().replace(" ", "-")}{suffix}',
        'title': f"{role} {value}: {bridge['theme']}", 'relationship': 'proposed_contextual_comparison',
        'pattern': pattern, 'numerology_role': role, 'number': value, 'root_used_for_vocabulary': digit, 'planet': planet,
        'paragraph': paragraph, 'question': question, 'display_paragraph': display_paragraph, 'display_question': display_question,
        'source_ids': list(dict.fromkeys(source_ids)),
        'ingredients': [ingredient, astrology_ingredient], 'availability': availability,
        'shared_contextual_themes': shared, 'independent_confirmation': False}

def _pmei_insight(chart, numerology):
    planes = numerology.get('planes', numerology.get('pmei', {}).get('planes', {}))
    counts = {key: int(planes.get(key, {}).get('count', 0)) for key in ('physical', 'mental', 'emotional', 'intuitive')}
    mars = _context(chart, 'Mars')
    mercury = _context(chart, 'Mercury')
    ids = ['costar-pmei', 'bridge-method-v1']
    if mars:
        ids += mars['source_ids']
    if mercury:
        ids += mercury['source_ids']
    opening = ', '.join(f'{key.title()} {value}' for key, value in counts.items())
    paragraph = f"PMEI records {opening}. These are literal letter counts; they are not digit-reduced, a capability score, or a planetary-element distribution. "
    if _reference_only(chart):
        paragraph += 'With an unknown birth time, no house-based output-versus-planning comparison is made.'
    elif mars and mercury and mars['house'] and mercury['house']:
        paragraph += (f"For a contextual comparison of practical output and planning, Mars is in House {mars['house']} with {mars['tone']} Tone/{mars['pulse']} Pulse, "
            f"while Mercury is in House {mercury['house']} with {mercury['tone']} Tone/{mercury['pulse']} Pulse. "
            'Their separate source functions concern action and information respectively. The comparison asks where acting and organizing information might serve different tasks; it does not equate Physical with Earth or Mental with Air.')
    elif mars and mercury:
        paragraph += 'Mars and Mercury positions are available, but a house-based life area was not resolved. No practical-life arena is invented.'
    else:
        paragraph += 'The required Mars/Mercury contexts were not both available, so no substitute placement is used.'
    if not (mars and mercury):
        availability = 'chart_context_unavailable'
        display_question = 'Can the missing Mars or Mercury position be calculated from valid chart input?'
    elif _reference_only(chart):
        availability = 'reference_epoch_only'
        display_question = 'What time information would make the practical-context comparison available?'
    else:
        availability = 'contextual_comparison_available'
        display_question = (f"How would action in House {mars['house']} and information in House {mercury['house']} serve different practical needs?"
            if mars['house'] and mercury['house'] else 'What additional birth input would resolve the missing house geometry?')
    return {'id': 'work-pmei', 'title': 'PMEI: output and planning stay distinct', 'relationship': 'proposed_contextual_comparison',
        'numerology_role': 'PMEI raw counts', 'number': None, 'planet': 'Mars / Mercury', 'paragraph': paragraph,
        'question': 'Which tasks call for hands-on action, careful planning, emotional connection or reflective space, without assuming that a low count means inability?',
        'display_paragraph': paragraph,
        'display_question': display_question,
        'source_ids': list(dict.fromkeys(ids)), 'ingredients': [{'system': 'Numerology', 'role': 'PMEI raw counts', 'counts': counts, 'source_ids': ['costar-pmei']}],
        'availability': availability,
        'shared_contextual_themes': [], 'independent_confirmation': False}

def _domain_summary(domain_id, insights):
    available = [row for row in insights if row['availability'] == 'contextual_comparison_available']
    if not available:
        return 'The number calculations remain visible. Birth-time or missing-object limits prevent a precise contextual comparison in this section.'
    roles = {row['numerology_role']: row for row in available}
    astrology = [ingredient for row in available for ingredient in row['ingredients'] if ingredient['system'] == 'Astrology']
    fields = list(dict.fromkeys(ingredient['field_meaning'].lower() for ingredient in astrology if ingredient.get('field_meaning')))
    field_words = '; '.join(fields[:2]) or 'the available planetary functions and sign styles; no house-based arena was resolved'
    if domain_id == 'motivation':
        soul = roles.get('Soul Urge')
        birth = roles.get('Birth Force')
        if soul and birth:
            a = BRIDGES[soul['root_used_for_vocabulary']]['theme']
            b = BRIDGES[birth['root_used_for_vocabulary']]['theme']
            relation = f"The motivation and date-based lenses both introduce {a}" if a == b else f"The motivation lens introduces {a}, while the date-based lens adds {b}"
            return (relation + f". The selected natal fields concern {field_words}. "
                'The useful inquiry is how a broad motive could take a particular form in those life areas. Ultimate Goal adds a direction lens while retaining its shared name/date inputs.')
    if domain_id == 'communication':
        expression = roles.get('Expression')
        called = roles.get('Called Name')
        if expression and called:
            same = expression['root_used_for_vocabulary'] == called['root_used_for_vocabulary']
            contrast = 'The Expression and Called Name roots repeat the same broad number vocabulary, but retain separate expression and presentation roles' if same else 'Expression and Called Name bring different number vocabularies into expression and social presentation'
            mercury = next((row for row in astrology if row['planet'] == 'Mercury'), None)
            detail = (f"Mercury's {mercury['tone']} Tone adds an information-and-discernment context" +
                (f" in House {mercury['house']}. " if mercury['house'] else '; a house-based area is unavailable. ') if mercury else '')
            return contrast + '. ' + detail + 'Consider what is being expressed, how it is communicated and how it may be received as separate questions.'
    if domain_id == 'work':
        balance = roles.get('Balance Number')
        coping = BRIDGES[balance['root_used_for_vocabulary']]['theme'] if balance else 'the available initials-based vocabulary'
        return (f"This section compares {coping} as a Balance lens with the separate work questions of method, responsibility and sustained accomplishment. "
            f"The selected natal fields concern {field_words}. PMEI then keeps practical output, planning, feeling and reflection visible as literal name-derived channels, without converting them into astrological elements.")
    return 'The available number roles and chart contexts remain separate ingredients for the detailed questions below.'

def compose_comparison(chart, numerology):
    """Create nine inspectable research comparisons with no predictive claims."""
    definitions = [
        ('motivation', 'Motivation and direction', [('Soul Urge', False, None, ''), ('Birth Force', True, None, ''), ('Ultimate Goal', False, None, '')]),
        ('communication', 'Expression and connection', [('Expression', False, None, ''), ('Called Name', True, None, ''), ('Soul Urge', True, 'Mercury', '-information')]),
        ('work', 'Work style and practical balance', [('Balance Number', False, None, ''), ('Expression', False, 'Saturn', '-process')]),
    ]
    domains = []
    for domain_id, title, selections in definitions:
        insights = []
        for role, alternate, fixed, suffix in selections:
            insight = _insight(chart, _metric(numerology, role), domain_id, suffix, alternate, fixed,
                purpose='This deliberate work lens compares the number theme with structure and sustained accomplishment, rather than treating their similarity as evidence.' if fixed == 'Saturn' else
                'This deliberate communication lens asks how inner-motivation vocabulary relates to information and discernment; the two functions are not equated.' if fixed == 'Mercury' else None)
            if insight:
                insights.append(insight)
        if domain_id == 'work':
            insights.append(_pmei_insight(chart, numerology))
        domains.append({'id': domain_id, 'title': title, 'summary': _domain_summary(domain_id, insights), 'insights': insights})
    ids = list(dict.fromkeys(source_id for domain in domains for insight in domain['insights'] for source_id in insight['source_ids']))
    notes = [
        'Every cross-system link here is an analyst-proposed contextual comparison, not a rule printed in either original methodology.',
        'Every ordinary natal chart contains the planets. Planet presence does not confirm a number; only its actual context differentiates the comparison.',
        'Expression, Soul Urge, Called Name, Balance and PMEI share name inputs. Ultimate Goal also reuses Expression. Repetition is not independent evidence.',
        'House/True Placement, Tone and Pulse are derived views of the same placement; their labels are not counted as separate confirmations.',
        'Planet, field and sign ingredients remain separate. No aspects, complete Delegate graph, Spark, forecast timing or full PURE personal-report synthesis is inferred.',
        'Number and sign themes describe attributed symbolic vocabularies. The prototype does not infer biography, behavior, maturity, events or outcomes.',
        'The source ingredient pack forbids generic-library fallback. Its personal-report approval status remains false; these are reviewable research comparisons.',
    ]
    if _reference_only(chart):
        notes.insert(0, 'Unknown birth time: local-noon positions are a reference epoch only; house/angle-based and precise natal-context interpretations are withheld.')
    return {'schema_version': '1.0', 'method_id': 'natal-contextual-bridge-v1',
        'summary': 'A contextual comparison of independently preserved natal calculations and name/date number roles. Sources and proposed connections are shown separately.',
        'domains': domains, 'sources': [source_record(source_id) for source_id in ids], 'method_notes': notes,
        'source_status': {'generic_library_fallback_allowed': False, 'personal_report_approved': False,
            'cross_system_links': 'ANALYST_PROPOSED', 'empirical_association_established': False,
            'ready_personal_report_sections': 0, 'total_personal_report_sections': 18,
            'source_commits': source_pack()['source_commits']},
        'has_scoring': False, 'reference_epoch_only': _reference_only(chart)}
