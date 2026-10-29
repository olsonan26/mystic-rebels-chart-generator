"""Source-bound reach and receiving structure, separate from full interpretation."""
from math import isclose, isfinite

from .placements import RULERS, SIGNS

MISSING = ('degree_meaning', 'complete_directed_aspects', 'ordered_receiver_synthesis')


def validate_profile(profile, assertions):
    if (profile.get('schema_version') != 'relationship-components-v1'
            or profile.get('full_method_approved') is not False
            or profile.get('personal_report_approved') is not False):
        raise ValueError('Relationship component cannot approve the full method')
    ids = {row['id'] for row in assertions['assertions']}
    for section in [*profile['numeric_reach'].values(), profile['conjunction'], profile['receiver_context']]:
        if not section.get('assertion_ids') or set(section['assertion_ids']) - ids:
            raise ValueError('Relationship rule lost source assertion references')
    for rule in profile['numeric_reach'].values():
        radius = rule.get('radius_deg')
        if radius is not None and (not isinstance(radius, (int, float)) or not isfinite(radius) or not 0 < radius < 180):
            raise ValueError('Invalid source reach parameter')
        if rule['status'].startswith('APPROXIMATE') and radius is not None:
            raise ValueError('Approximate source reach cannot become an exact threshold')
    return True


def physical(point):
    return point.get('group') in ('Planets', 'Asteroids', 'Minor bodies')


def separation(a, b):
    values = [a['longitude_deg'], b['longitude_deg']]
    if not all(isinstance(v, (int, float)) and isfinite(v) for v in values):
        raise ValueError('A relationship needs finite coordinates')
    return abs((values[1] - values[0] + 180) % 360 - 180)


def conjunction_reach(sender, receiver, profile, sender_layer='natal', receiver_layer='natal'):
    """Test sender -> receiver exact coordinate, never summed-radius overlap."""
    if sender_layer not in ('natal', 'sky') or receiver_layer not in ('natal', 'sky'):
        raise ValueError('Unknown relationship layer')
    distance = separation(sender, receiver)
    rule = profile['numeric_reach'].get(sender['id'], {})
    result = dict(sender=f"{sender_layer}:{sender['id']}", receiver=f"{receiver_layer}:{receiver['id']}",
        kind='direct_conjunction_reach', separation_deg=distance, angle_deg=0,
        radius_deg=rule.get('radius_deg'), physical_reach_supported=None,
        source_assertion_ids=profile['conjunction']['assertion_ids'] + rule.get('assertion_ids', []),
        complete_aspect_interpretation=False, interpretive_roles_assigned=False)
    if sender_layer == 'natal' and receiver_layer == 'sky':
        return result | {'status': 'NATAL_OUTWARD_TRANSIT_EMISSION_NOT_ALLOWED', 'physical_reach_supported': False}
    if not physical(sender):
        return result | {'status': 'NO_PHYSICAL_POINT_EMISSION', 'physical_reach_supported': False}
    if not physical(receiver):
        return result | {'status': 'POINT_RECEIVING_SCOPE_UNRESOLVED'}
    radius = result['radius_deg']
    if radius is None:
        return result | {'status': rule.get('status', 'SOURCE_RADIUS_UNAVAILABLE')}
    # Numerical equality tolerance only, not a physical orb extension.
    if isclose(distance, radius, abs_tol=1e-10, rel_tol=0):
        return result | {'status': 'EXACT_RADIUS_BOUNDARY_UNRESOLVED'}
    return result | {'status': 'WITHIN_EXPLICIT_CONJUNCTION_REACH' if distance < radius else 'OUTSIDE_THIS_CONJUNCTION_REACH',
                     'physical_reach_supported': distance < radius}


def ruler_route(points, start):
    path, current = [], start
    while current in points and current not in path:
        path.append(current)
        current = points[current]['sign_ruler']
    return dict(path=path, repeat=current if current in path else None,
                missing=current if current not in points else None,
                cycle=path[path.index(current):] if current in path else [],
                final_ruler=None, strength_multiplier=None)


def condition_graph(chart, profile, layer='natal', evaluated_ids=None):
    """Finite graph; carrying a condition reference never means it is complete."""
    points = {p['id']: p for p in chart['points'] if p.get('available')}
    prefix = layer + ':'
    cusps = chart.get('whole_sign_cusps', []) if layer == 'natal' else []
    houses = {SIGNS[int(longitude // 30) % 12]: h for h, longitude in enumerate(cusps, 1)}
    unknown_time = chart.get('time', {}).get('time_is_reference_only', False)
    contacts, boundaries = [], []
    names = list(points)
    if not unknown_time:
        for sender in names:
            if sender not in profile['numeric_reach']:
                continue
            for receiver in names:
                if sender == receiver:
                    continue
                result = conjunction_reach(points[sender], points[receiver], profile, layer, layer)
                if result['physical_reach_supported'] is True:
                    contacts.append({'id': f'{prefix}{sender}->{prefix}{receiver}:conjunction', **result})
                elif result['status'] == 'EXACT_RADIUS_BOUNDARY_UNRESOLVED':
                    boundaries.append(result)
    nodes = {}
    for name, p in points.items():
        ref = prefix + name
        h = p.get('house') if layer == 'natal' else None
        house_sign = next((sign for sign, number in houses.items() if number == h), None)
        delegate = RULERS[SIGNS.index(house_sign)] if house_sign else None
        ruled = [sign for sign, ruler in zip(SIGNS, RULERS) if ruler == name]
        areas = []
        for sign in ruled:
            areas.append(dict(sign=sign, house=houses.get(sign),
                occupant_condition_refs=[prefix + q['id'] for q in points.values() if q['sign'] == sign],
                full_condition_complete=False))
        nodes[ref] = dict(fact_ref=ref, condition_ref=ref,
            point_kind='physical_body' if physical(p) else 'mathematical_or_derived_point',
            physical_retrograde=p.get('retrograde') if physical(p) else None,
            calculated_motion_retrograde=p.get('retrograde'),
            sign_ruler_ref=prefix + p['sign_ruler'] if p['sign_ruler'] in points else None,
            house_delegate_ref=prefix + delegate if delegate in points else None,
            house_delegate_retrograde=points.get(delegate, {}).get('retrograde'),
            ruled_areas=areas, ruler_route=ruler_route(points, name),
            incoming_reach_refs=[c['id'] for c in contacts if c['receiver'] == ref],
            outgoing_reach_refs=[c['id'] for c in contacts if c['sender'] == ref],
            missing_dependencies=list(MISSING) + (['actual_house'] if not h else []),
            full_condition_complete=False)
    return dict(schema_version='condition-graph-v1', layer=layer,
        epoch=chart.get('time', {}).get('birth_utc') or chart.get('as_of_utc'),
        evaluated_catalog_ids=list(evaluated_ids or chart.get('input', {}).get('objects', names)),
        available_ids=names,
        unavailable=[{'id': p['id'], 'error': p.get('error')} for p in chart['points'] if not p.get('available')],
        nodes=nodes, direct_conjunction_reach=contacts, unresolved_boundaries=boundaries,
        unknown_birth_time=unknown_time,
        aspect_coverage='CONJUNCTION_REACH_COMPONENT_ONLY_NOT_COMPLETE_ASPECT_GRAPH',
        absence_is_not_no_aspects=True, full_delegate_condition_complete=False,
        source_assertion_ids=profile['receiver_context']['assertion_ids'])


def receiver_packet(graph, relation):
    """Resolve the receiving side of an identified relation without role inference."""
    ref = relation['receiver']
    if ref not in graph['nodes']:
        raise ValueError('Receiving condition is outside this graph')
    return dict(relation_ref=relation['id'], receiver=ref,
        condition=graph['nodes'][ref], complete=False,
        physical_reach_status=relation['status'], interpretive_roles_assigned=False)
