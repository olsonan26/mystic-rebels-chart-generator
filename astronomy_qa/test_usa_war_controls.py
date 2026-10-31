"""Versioned research assertions for declared U.S. war dates (not a model validation)."""
from research.usa_war_2026.war_case_controls import DECLARED_US_WARS, scores, NATAL
from mystic_rebels.source_conjunctions import angular_distance


def test_natal_uranus_proxy():
    assert abs(NATAL['Uranus'] - 68.89989037416827) < 0.01


def test_five_formal_war_date_feature_totals():
    rows = [scores(day) for _, day in DECLARED_US_WARS]
    assert len(rows) == 5
    assert sum(r['directed_conjunction_contacts'] for r in rows) == 7
    assert sum(r['directed_mars_contacts'] for r in rows) == 2
    assert sum(r['directed_pluto_contacts'] for r in rows) == 1
    assert sum(r['uranus_return_1deg'] for r in rows) == 0


def test_historical_example_is_proximity_only():
    assert angular_distance(NATAL['Uranus'], scores_and_sky('1861-04-12')) < 1


def scores_and_sky(day):
    from research.usa_war_2026.war_case_controls import sky
    return sky(day)['Uranus']
