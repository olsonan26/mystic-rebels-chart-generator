"""Original worked geometries and receiver dependencies, not trait validation."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

import pytest

from mystic_rebels.placements import derive, dms
from mystic_rebels.relationship_context import conjunction_reach, condition_graph, receiver_packet, validate_profile
from mystic_rebels.chat_context import build_context, chart_fingerprint
from mystic_rebels.chat_knowledge import authorities
from mystic_rebels.models import BirthInput

PROFILE = json.loads((Path(__file__).resolve().parents[1] / 'data/knowledge/relationship_rule_profiles.json').read_text())


def point(name, longitude, asc=60, group='Planets', rx=False):
    return dict(id=name, available=True, longitude_deg=longitude, group=group,
                retrograde=rx, display_dms=dms(longitude), **derive(longitude, asc))


def chart(points, asc=60, unknown=False):
    return dict(points=points, whole_sign_cusps=[] if unknown else [(asc // 30 * 30 + h * 30) % 360 for h in range(12)],
                time={'birth_utc': '2000-01-01T12:00:00+00:00', 'time_is_reference_only': unknown},
                input={'objects': [p['id'] for p in points]})


def test_source241_no_direct_conjunction_from_overlapping_radii():
    # Printed241: Mars5 cannot reach Saturn10 at radius4. Adding Saturn's
    # approximate7.5 radius would manufacture the wrong direct result.
    r = conjunction_reach(point('Mars', 5), point('Saturn', 10), PROFILE)
    assert r['physical_reach_supported'] is False
    assert r['separation_deg'] == 5
    assert 'conjunction240241-core-reach' in r['source_assertion_ids']


def test_source240_interior_mars_reach_is_preserved_without_ordered_roles():
    r = conjunction_reach(point('Mars', 5), point('Saturn', 8), PROFILE)
    assert r['physical_reach_supported'] is True
    assert not r['interpretive_roles_assigned']
    assert not r['complete_aspect_interpretation']


def test_directed_reach_is_not_symmetric_or_same_house_occupancy():
    a, b = point('Sun', 1), point('Moon', 5)
    assert conjunction_reach(a, b, PROFILE)['physical_reach_supported'] is True
    assert conjunction_reach(b, a, PROFILE)['physical_reach_supported'] is False
    assert conjunction_reach(point('Moon', 1), point('Venus', 20), PROFILE)['physical_reach_supported'] is False


@pytest.mark.parametrize('sender', ['Mercury', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'])
def test_missing_or_approximate_radius_is_not_a_negative_or_generic_default(sender):
    r = conjunction_reach(point(sender, 1), point('Moon', 1.1), PROFILE)
    assert r['physical_reach_supported'] is None
    assert r['radius_deg'] is None


def test_wrap_and_exact_threshold_are_distinct_from_role_or_timing():
    assert conjunction_reach(point('Moon', 358.1), point('Venus', 1), PROFILE)['physical_reach_supported'] is True
    assert conjunction_reach(point('Moon', 358), point('Venus', 1), PROFILE)['status'] == 'EXACT_RADIUS_BOUNDARY_UNRESOLVED'
    r = conjunction_reach(point('Sun', 1), point('Moon', 1), PROFILE)
    assert r['physical_reach_supported'] is True and not r['interpretive_roles_assigned']


def test_transit245_has_no_natal_outgoing_reciprocal_emission():
    a, b = point('Venus', 1), point('Sun', 5)
    assert conjunction_reach(a, b, PROFILE, 'sky', 'natal')['physical_reach_supported'] is True
    assert conjunction_reach(b, a, PROFILE, 'natal', 'sky')['status'] == 'NATAL_OUTWARD_TRANSIT_EMISSION_NOT_ALLOWED'
    assert conjunction_reach(point('Moon', 1), point('Saturn', 6), PROFILE, 'sky', 'natal')['physical_reach_supported'] is False


def test_point_notation_never_grants_emission_or_universal_receiving_orb():
    node = point('NorthNodeTrue', 1, group='Lunar points')
    assert conjunction_reach(node, point('Moon', 1), PROFILE)['physical_reach_supported'] is False
    assert conjunction_reach(point('Sun', 1), node, PROFILE)['status'] == 'POINT_RECEIVING_SCOPE_UNRESOLVED'


def test_original208_moon_carries_actual_cancer_h12_and_its_node_before_uranus():
    points = [point('Moon', 305, asc=120), point('NorthNodeTrue', 100, asc=120, group='Lunar points'), point('Uranus', 200, asc=120)]
    g = condition_graph(chart(points, asc=120), PROFILE)
    moon = g['nodes']['natal:Moon']
    assert moon['ruled_areas'][0]['sign'] == 'Cancer'
    assert moon['ruled_areas'][0]['house'] == 12
    assert moon['ruled_areas'][0]['occupant_condition_refs'] == ['natal:NorthNodeTrue']
    assert moon['sign_ruler_ref'] == 'natal:Uranus'
    assert g['nodes']['natal:NorthNodeTrue']['point_kind'] == 'mathematical_or_derived_point'


def test_original210_gemini_rising_keeps_actual_h2_moon_context_and_dual_rules():
    points = [point('Moon', 1), point('Venus', 80), point('Mercury', 170), point('Juno', 100, group='Asteroids')]
    g = condition_graph(chart(points), PROFILE)
    moon = g['nodes']['natal:Moon']
    assert moon['ruled_areas'] == [{'sign': 'Cancer', 'house': 2, 'occupant_condition_refs': ['natal:Juno'], 'full_condition_complete': False}]
    assert {a['sign']: a['house'] for a in g['nodes']['natal:Venus']['ruled_areas']} == {'Taurus': 12, 'Libra': 5}
    assert {a['sign'] for a in g['nodes']['natal:Mercury']['ruled_areas']} == {'Gemini', 'Virgo'}


def test_cycle_is_finite_without_final_ruler_or_strength_and_motion_is_separate():
    points = [point('Sun', 100), point('Moon', 130, rx=True), point('Juno', 105, group='Asteroids')]
    g = condition_graph(chart(points), PROFILE)
    route = g['nodes']['natal:Sun']['ruler_route']
    assert route['path'] == ['Sun', 'Moon'] and route['repeat'] == 'Sun'
    assert route['final_ruler'] is None and route['strength_multiplier'] is None
    juno = g['nodes']['natal:Juno']
    assert juno['physical_retrograde'] is False
    assert juno['house_delegate_ref'] == 'natal:Moon' and juno['house_delegate_retrograde'] is True


def test_receiver_packet_follows_the_specific_direction_not_a_generic_partner():
    g = condition_graph(chart([point('Sun', 1), point('Moon', 2)]), PROFILE)
    relation = next(c for c in g['direct_conjunction_reach'] if c['sender'] == 'natal:Sun')
    assert receiver_packet(g, relation)['receiver'] == 'natal:Moon'
    with pytest.raises(ValueError, match='outside'):
        receiver_packet(g, {**relation, 'receiver': 'sky:Moon'})


def test_unknown_time_withholds_house_graph_and_natal_reach_claims():
    points = [point('Moon', 1, asc=None), point('Sun', 2, asc=None)]
    g = condition_graph(chart(points, unknown=True), PROFILE)
    assert not g['direct_conjunction_reach']
    assert g['nodes']['natal:Moon']['ruled_areas'][0]['house'] is None
    assert 'actual_house' in g['nodes']['natal:Moon']['missing_dependencies']


def test_profile_sources_remain_manifest_checked_and_cannot_promote_approximation():
    data, _, _ = authorities()
    assert validate_profile(PROFILE, data['assertions'])
    changed = deepcopy(PROFILE); changed['numeric_reach']['Saturn']['radius_deg'] = 7.5
    with pytest.raises(ValueError, match='Approximate'):
        validate_profile(changed, data['assertions'])
    changed = deepcopy(PROFILE); changed['receiver_context']['assertion_ids'] = ['invented']
    with pytest.raises(ValueError, match='source assertion'):
        validate_profile(changed, data['assertions'])


def test_full_requirement_ledger_retains_scoped_component_progress_without_false_resolution():
    from knowledge_audit.requirements import load_requirements, validate_requirements
    data = load_requirements()
    for row in data['requirements']:
        if row['id'] in PROFILE['requirement_progress']:
            evidence = row['partial_component_evidence']
            assert evidence['progress'] == PROFILE['requirement_progress'][row['id']]
            assert not evidence['complete_requirement_resolved'] and not row['personal_answer_approved']
    assert validate_requirements(data)
    row = next(r for r in data['requirements'] if r.get('partial_component_evidence'))
    row['partial_component_evidence']['complete_requirement_resolved'] = True
    with pytest.raises(ValueError, match='Partial component'):
        validate_requirements(data)


def test_real_chart_includes_hidden_catalog_occupants_and_separate_dated_sky():
    birth = BirthInput(name='Fictional graph QA', local_date='2000-01-01', local_time='12:00:00', timezone='UTC', latitude=0, longitude=0, objects=['Sun'])
    c = build_context(birth, chart_fingerprint(birth), 'What can I explore about relationships?', [], datetime(2026, 10, 29, tzinfo=timezone.utc), True)
    natal, sky = c['condition_graph'], c['current_sky']['condition_graph']
    assert natal['catalog_inventory_complete'] and len(natal['evaluated_catalog_ids']) == 74
    assert not natal['omitted_catalog_ids']
    assert {p['id'] for p in natal['unavailable']} == {'SophiaMean', 'SophiaTrue'}
    assert 'natal:Juno' in natal['nodes'] and 'natal:NorthNodeTrue' in natal['nodes']
    assert 'sky:Sun' in sky['nodes'] and 'natal:Sun' not in sky['nodes']
    assert not sky['catalog_inventory_complete'] and sky['omitted_catalog_ids']
    for relation in c['current_sky']['direct_conjunction_reach']:
        assert relation['sender'].startswith('sky:') and relation['receiver'].startswith('natal:')
        assert relation['receiving_context']['receiver'] == relation['receiver']
    assert c['personal_report_approved'] is False
    assertion_ids = {a['id'] for a in c['knowledge']['assertions']}
    for section in [*PROFILE['numeric_reach'].values(), PROFILE['conjunction'], PROFILE['receiver_context']]:
        assert set(section['assertion_ids']) <= assertion_ids
