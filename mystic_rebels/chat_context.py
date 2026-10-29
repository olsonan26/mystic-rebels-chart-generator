"""Trusted natal assessments and dated sky geometry for the chart conversation."""
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from math import floor
import re

from . import astronomy as astro
from .catalog import BY_ID
from .errors import ChartError
from .models import BirthInput
from .placements import derive, dms, RULERS, SIGNS
from .service import calculate
from .chat_knowledge import question_packet
from .relationship_context import condition_graph, conjunction_reach, receiver_packet

CORE = ('Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn',
        'Uranus', 'Neptune', 'Pluto', 'Chiron')
ORDER = ('planet', 'house', 'degree', 'decan', 'aspects', 'sign', 'ruler')
DIAGNOSTIC_ANGLES = (0, 15, 30, 45, 60, 72, 75, 90, 105, 120, 135, 144, 150, 165, 180)


def named_objects(question):
    result = [name for name in BY_ID if re.search(r'\b' + re.escape(name) + r'\b', question, re.I)]
    for term, names in [('node', ('NorthNodeTrue', 'NorthNodeMean', 'SouthNodeTrue', 'SouthNodeMean')),
                        ('lilith', ('LilithMean', 'LilithTrue')), ('sophia', ('SophiaMean', 'SophiaTrue'))]:
        if re.search(r'\b' + term + r's?\b', question, re.I):
            result.extend(names)
    return list(dict.fromkeys(result))


def chart_fingerprint(birth):
    canonical = birth.model_dump(mode='json')
    canonical['objects'] = list(dict.fromkeys(birth.objects))
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


@lru_cache(maxsize=16)
def _natal(canonical):
    # The private request stays in process memory only; no disk/database writes.
    birth = BirthInput.model_validate_json(canonical)
    birth = birth.model_copy(update={'objects': list(dict.fromkeys([*birth.objects, *CORE]))})
    return calculate(birth)


def route(points, start):
    path, current = [], start
    while current in points and current not in path:
        path.append(current)
        current = points[current]['sign_ruler']
    return {'path': path, 'repeat': current if current in path else None,
            'cycle': path[path.index(current):] if current in path else [],
            'missing': current if current and current not in points else None}


def point_fact(point, layer):
    return {k: point.get(k) for k in (
        'id', 'name', 'longitude_deg', 'display_dms', 'degree_in_sign',
        'sign', 'tone', 'pulse', 'decan', 'house', 'field', 'sign_ruler',
        'retrograde', 'speed_longitude_deg_per_day', 'gradity', 'outgoing_emission')} | {'layer': layer}


def assessments(points, ascendant, graph=None):
    result = {}
    for name, point in points.items():
        h = point.get('house')
        delegate = RULERS[(floor(ascendant / 30) + h - 1) % 12] if h and ascendant is not None else None
        g = floor(point['degree_in_sign'])
        ruler = point['sign_ruler']
        ruled = [SIGNS[i] for i, r in enumerate(RULERS) if r == name]
        result[name] = {
            'stages': [
                {'stage': 'planet', 'status': 'calculated', 'body': name,
                 'physical_retrograde': point.get('retrograde'),
                 'parent_convention': {'Sun': 'Father symbolism; no claim about his behavior.',
                                       'Moon': 'Mother symbolism; no claim about her behavior.'}.get(name)},
                {'stage': 'house', 'status': 'calculated' if h else 'unavailable_unknown_time_or_geometry',
                 'house': h, 'field': point.get('field'), 'delegate': delegate,
                 'delegate_retrograde': points.get(delegate, {}).get('retrograde'),
                 'note': 'Delegate condition does not change occupant physical motion.'},
                {'stage': 'degree', 'status': 'exact_coordinate_only_meaning_unresolved',
                 'degree_in_sign': point['degree_in_sign'], 'canonical_spark': None,
                 'house_candidate': SIGNS[(g + (6 if h % 2 == 0 else 0)) % 12] if h else None,
                 'sign_candidate': SIGNS[(g + (6 if (point['sign_index'] + 1) % 2 == 0 else 0)) % 12]},
                {'stage': 'decan', 'status': 'calculated_component', 'decan': point['decan'],
                 'pulse': point['pulse'], 'associated_planet': RULERS[SIGNS.index(point['pulse'])]},
                {'stage': 'aspects', 'status': 'partial_conjunction_reach_complete_directed_rules_missing' if graph else 'incomplete_directed_rules',
                 'qualified_contacts': [], 'reach_refs': ([*graph['nodes']['natal:' + name]['incoming_reach_refs'],
                                                          *graph['nodes']['natal:' + name]['outgoing_reach_refs']] if graph else [])},
                {'stage': 'sign', 'status': 'calculated_component', 'tone': point['tone']},
                {'stage': 'ruler', 'status': 'structural_lookup_condition_incomplete',
                 'ruler': ruler, 'assessment_ref': ruler if ruler in points else None,
                 'condition_ref': 'natal:' + ruler if graph and ruler in points else None}],
            'ruler_route': route(points, name), 'delegate_condition_complete': False,
            'ruled_signs': ruled, 'occupants': [p['id'] for p in points.values() if p['sign'] in ruled],
            'complete_phddasr': False}
    return result


def geometry(a, b):
    separation = abs((b['longitude_deg'] - a['longitude_deg'] + 180) % 360 - 180)
    angle = min(DIAGNOSTIC_ANGLES, key=lambda value: abs(value - separation))
    return [a['id'], b['id'], separation, angle, abs(separation - angle)]


def sky_snapshot(epoch, natal, question):
    if not 1800 <= epoch.year <= 2399:
        raise ValueError('The selected sky date must be within 1800-2399 UTC.')
    names = list(CORE)
    for name, row in BY_ID.items():
        if row['body'] is not None and re.search(r'\b' + re.escape(name) + r'\b', question, re.I) and name not in names:
            names.append(name)
    sky, unavailable = [], []
    with astro.LOCK:
        astro.initialize()
        time_data = astro.times(epoch)
        for name in names:
            row = BY_ID[name]
            try:
                if not row.get('available', True) or (row.get('max_year') and epoch.year > row['max_year']):
                    raise ChartError('OBJECT_UNAVAILABLE', 'This body is unavailable at the selected epoch.')
                p = astro.position(time_data['jd_ut1'], row['body'],
                                   list(dict.fromkeys(['sepl_18.se1', 'semo_18.se1', *row.get('assets', [])])))
                d = derive(p['longitude_deg'])
                overlay = derive(p['longitude_deg'], natal['angles'].get('Ascendant'))
                sky.append({'id': name, 'available': True, 'group': row['group'], **p, **d, 'display_dms': dms(p['longitude_deg']),
                            'house': None, 'field': None,
                            'natal_overlay_house': overlay['house'], 'natal_overlay_field': overlay['field']})
            except ChartError as exc:
                unavailable.append({'id': name, 'error': exc.record()})
    targets = [p for p in natal['points'] if p.get('available')]
    return {'as_of_utc': epoch.isoformat(), 'time': time_data, 'points': sky,
            'unavailable': unavailable, 'current_location': None,
            'sky_houses': 'NOT_CALCULATED_NO_CURRENT_LOCATION_SELECTED',
            'overlay_method': 'Fixed natal Whole Sign sectors; no moving/relocated Ascendant substituted.',
            'geometry_columns': ['from', 'to', 'separation_deg', 'nearest_diagnostic_angle_deg', 'residual_deg'],
            'sky_to_natal_geometry': [geometry(a, b) for a in sky for b in targets],
            'sky_to_sky_geometry': [geometry(a, b) for i, a in enumerate(sky) for b in sky[i + 1:]],
            'geometry_status': 'ANGLES_ONLY_NOT_OOI_QUALIFICATION_OR_DIRECTED_INTERPRETATION',
            'qualified_aspects': [], 'exact_event_dates': [],
            'timing_limit': 'Single dated snapshot; no interval roots, peak dates, influence windows or repeat-pass forecast inferred.'}


def build_context(birth, expected_chart_id, question, history, as_of, include_current):
    if chart_fingerprint(birth) != expected_chart_id:
        raise ValueError('The chart changed. Generate or reopen it before asking again.')
    # Source-defined Delegate payloads require evaluating hidden catalog occupants
    # too. Retrieval remains question-focused; geometry and coverage do not depend
    # on the wheel's display toggles. Unavailable objects stay explicit.
    focus = set(birth.objects) | set(CORE) | set(named_objects(question))
    enriched = birth.model_copy(update={'objects': list(BY_ID)})
    natal = _natal(enriched.model_dump_json())
    source = question_packet(question, {**natal, 'points': [p for p in natal['points'] if p['id'] in focus]}, history)
    profile = source['relationship_profiles']
    points = {p['id']: p for p in natal['points'] if p.get('available')}
    graph = condition_graph(natal, profile)
    graph['catalog_inventory_complete'] = set(graph['evaluated_catalog_ids']) == set(BY_ID)
    graph['omitted_catalog_ids'] = sorted(set(BY_ID) - set(graph['evaluated_catalog_ids']))
    loaded = {c['concept_id'] for c in source['components']}
    for ref, node in graph['nodes'].items():
        name = ref.split(':', 1)[1].lower()
        node['source_vocabulary_loaded'] = any(c in loaded for c in ('meaning-' + name, 'asteroid-' + name, name))
        if not node['source_vocabulary_loaded']:
            node['missing_dependencies'].append('body_vocabulary_not_selected_for_this_question')
    facts = {'natal:' + name: point_fact(p, 'natal') for name, p in points.items()}
    for h, longitude in enumerate(natal['whole_sign_cusps'], 1):
        derived = derive(longitude)
        facts[f'natal:House{h}'] = {'id': f'House{h}', 'kind': 'whole_sign_house', 'layer': 'natal',
            'name': f'Whole Sign house {h}', 'longitude_deg': longitude,
            'display_dms': dms(longitude), 'house': h, 'field': SIGNS[h - 1],
            'tone': derived['tone'], 'sign_ruler': derived['sign_ruler'], 'retrograde': None,
            'occupants': [p['id'] for p in points.values() if p.get('house') == h]}
    epoch = as_of.astimezone(timezone.utc) if as_of else datetime.now(timezone.utc)
    sky = sky_snapshot(epoch, natal, question) if include_current else None
    if sky:
        facts.update({'sky:' + p['id']: {**point_fact(p, 'sky'),
                                       'natal_overlay_house': p['natal_overlay_house'],
                                       'as_of_utc': sky['as_of_utc']} for p in sky['points']})
        sky['condition_graph'] = condition_graph(sky, profile, layer='sky', evaluated_ids=[p['id'] for p in sky['points']] + [p['id'] for p in sky['unavailable']])
        sky['condition_graph']['catalog_inventory_complete'] = False
        sky['condition_graph']['omitted_catalog_ids'] = sorted(set(BY_ID) - set(sky['condition_graph']['evaluated_catalog_ids']))
        sky['condition_graph']['scope_limit'] = 'Core and explicitly named current bodies only; sky occupant inventory is not complete.'
        overlay = []
        if not natal['time']['time_is_reference_only']:
            for sender in sky['points']:
                for receiver in points.values():
                    reach = conjunction_reach(sender, receiver, profile, 'sky', 'natal')
                    if reach['physical_reach_supported'] is True:
                        relation = {'id': f"sky:{sender['id']}->natal:{receiver['id']}:conjunction", **reach}
                        overlay.append({**relation, 'receiving_context': receiver_packet(graph, relation)})
        sky['direct_conjunction_reach'] = overlay
        sky['full_transit_interpretation_complete'] = False
    context = {'schema_version': 'chart-chat-context-v1', 'chart_id': expected_chart_id,
               'assessment_chart_id': natal['chart_id'], 'facts': facts,
               'natal_time': natal['time'], 'configuration': natal['configuration'],
               'birth_uncertainty': natal['warnings'],
               'unavailable_natal_objects': [p for p in natal['points'] if not p.get('available')],
               'phddasr_order': list(ORDER), 'assessments': assessments(points, natal['angles'].get('Ascendant'), graph),
               'condition_graph': graph,
               'answer_capabilities': {
                   'available': ['Reviewed natal component vocabulary', 'All 74 catalog entries evaluated; unavailable entries retained',
                                 'Actual ruler/Delegate sectors and occupant condition references', 'Source-numeric direct conjunction reach for five emitters'],
                   'partial': ['Full PHDDASR synthesis', 'Complete directed aspects and receiving interpretation'],
                   'timing': 'No progressions or forecast windows; this limits timing claims, not every natal explanation.'},
               'current_sky': sky, 'knowledge': source,
               'personal_report_approved': False,
               'scope': 'Reviewed component reflections, source explanations, chart facts and dated sky geometry; incomplete full-method interpretation.'}
    raw = json.dumps(context, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    if len(raw) > 1200000:
        raise ValueError('Please focus this question on one topic so all its evidence can be retained.')
    context['context_sha256'] = hashlib.sha256(raw).hexdigest()
    return context
