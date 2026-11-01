"""Source-anchored regression for the dual wheel's house/Field/Tone/Pulse/ruler rules.

Primary sources: PURE ASTROLOGY, printed pp. 103, 156-157, 188-190, 227-230.
These test the placement layer, NOT complete PHDASR, direction-sensitive
aspects, Energy Flow or prediction. Astrological interpretation is not
scientifically validated by passing numerical tests.
"""
from math import floor
import pytest
from mystic_rebels.placements import SIGNS, RULERS, house, derive
from mystic_rebels.service import RULES, calculate
from mystic_rebels.models import BirthInput


def test_book_scorpio_asc_cancer_planet_is_sagittarius_true_placement():
    # Book's explicit Scorpio Ascendant / Cancer in 9th-house example.
    p = derive(100.0, 220.0)
    assert p['house'] == 9
    assert p['field'] == p['true_placement'] == 'Sagittarius'
    assert p['tone'] == 'Cancer'
    assert p['sign_ruler'] == 'Moon'


def test_sagittarius_rising_gemini_in_seventh_does_not_use_house_ruler():
    p = derive(75.0, 245.0)
    assert p['house'] == 7
    assert p['field'] == 'Libra'
    assert p['tone'] == 'Gemini'
    assert p['pulse'] == 'Libra'
    assert p['sign_ruler'] == 'Mercury'  # NOT Venus.


def test_book_virgo_decan_elemental_sequence():
    assert [derive(v)['pulse'] for v in (150.0, 160.0, 170.0)] == [
        'Virgo', 'Capricorn', 'Taurus'
    ]


@pytest.mark.parametrize('asc_sign', range(12))
@pytest.mark.parametrize('planet_sign', range(12))
@pytest.mark.parametrize('asc_inner', [0.001, 14.999, 29.999])
@pytest.mark.parametrize('planet_inner', [0.0001, 9.999, 10.0, 19.999, 20.0, 29.999])
def test_all_houses_decans_and_rulers_against_independent_counting(
        asc_sign, planet_sign, asc_inner, planet_inner):
    # Independent forward counting, rather than duplicating production floor
    # subtraction; tests all 12 signs and near-boundary positions.
    ac = 30 * asc_sign + asc_inner
    planet = 30 * planet_sign + planet_inner
    expected_house = 1 + next(
        offset for offset in range(12)
        if (asc_sign + offset) % 12 == planet_sign
    )
    p = derive(planet, ac)
    assert house(planet, ac) == expected_house
    assert p['house'] == expected_house
    assert p['true_placement'] == p['field'] == SIGNS[expected_house - 1]
    assert p['tone'] == SIGNS[planet_sign]
    assert p['pulse'] == SIGNS[(planet_sign + 4 * floor(planet_inner / 10)) % 12]
    assert p['sign_ruler'] == RULERS[planet_sign]


def test_no_ascendant_never_invents_true_placement():
    p = derive(100.0)
    assert p['house'] is None
    assert p['true_placement'] is None
    assert p['field'] is None


def test_complete_interpretation_is_not_falsely_claimed_ready():
    for stage in ['spark', 'aspects', 'progressions', 'delegate_traversal',
                  'energy_flow', 'transit_synastry', 'predictive_engine']:
        assert RULES[stage]['status'] == 'BLOCKED'
    assert RULES['whole_sign']['status'] == 'READY'
    assert RULES['true_placement']['status'] == 'READY'
    assert RULES['ruler']['status'] == 'READY'


def test_approximate_birth_time_crossing_ascendant_cusp_does_not_invent_houses():
    # 2024-01-01 00:04 UTC in Los Alamitos: Asc ~29.96° Gemini.
    # The declared ±15-minute range includes Cancer rising. A central-clock
    # 3rd-sign house cannot be asserted for the entire plausible interval.
    chart = calculate(BirthInput(
        local_date='2023-12-31',local_time='16:04:00',
        timezone='America/Los_Angeles',latitude=33.803,longitude=-118.072,
        time_accuracy='approximate',uncertainty_seconds=900,
        objects=['Sun','Mars','Ascendant','Fortune']
    ))
    assert chart['time']['house_time_stable'] is False
    assert any(w['code']=='HOUSE_TIME_UNCERTAIN' for w in chart['warnings'])
    for point in chart['points']:
        if point['available']:
            assert point['house'] is None
            assert point['field'] is None
            assert point['true_placement'] is None
    fortune=next(p for p in chart['points'] if p['id']=='Fortune')
    assert fortune['available'] is False
    assert fortune['error']['code']=='ANGLE_TIME_UNCERTAIN'


def test_known_approximate_time_distant_from_cusp_keeps_house():
    chart=calculate(BirthInput(
        local_date='2023-12-31',local_time='12:00:00',
        timezone='America/Los_Angeles',latitude=33.803,longitude=-118.072,
        time_accuracy='approximate',uncertainty_seconds=900,
        objects=['Sun']
    ))
    assert chart['time']['house_time_stable'] is True
    assert chart['points'][0]['house'] is not None
    assert not any(w['code']=='HOUSE_TIME_UNCERTAIN' for w in chart['warnings'])


def test_uncertainty_at_least_one_hour_fails_closed():
    chart=calculate(BirthInput(
        local_date='2023-12-31',local_time='12:00:00',
        timezone='America/Los_Angeles',latitude=33.803,longitude=-118.072,
        time_accuracy='approximate',uncertainty_seconds=3600,
        objects=['Sun','Spirit']
    ))
    assert chart['time']['house_time_stable'] is False
    assert chart['points'][0]['house'] is None
    assert chart['points'][1]['available'] is False
