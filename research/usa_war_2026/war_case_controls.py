"""Exploratory U.S. war-onset case/control study. Not a forecasting engine.

SOURCE RULES: only verified outgoing conjunction OOIs, transit -> natal.
CAVEATS: 1776 outside repo-certified SWIEPH range; MOSEPH proxy, 12:00 UTC,
no birth time, no houses/true placements; outer same-body 1° returns are
astronomical proximities, NOT source-authorized aspects.
CONTROL: non-onset dates in the same year outside ±30 days of first
formal declaration. These dates are not necessarily peaceful.
"""
from __future__ import annotations
import json
import random
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path
import swisseph as swe
from mystic_rebels.source_conjunctions import angular_distance, transit_conjunctions

BODIES = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO
}
OUTERS = ('Uranus', 'Neptune', 'Pluto')
# One onset per conflict; not eleven separate declarations of war.
DECLARED_US_WARS = [
    ('War of 1812', '1812-06-18'),
    ('Mexican-American War', '1846-05-13'),
    ('Spanish-American War', '1898-04-25'),
    ('US enters WWI', '1917-04-06'),
    ('US enters WWII', '1941-12-08')
]
# Heterogeneous events: sensitivity table ONLY, not used in inference.
SECONDARY = [
    ('Fort Sumter', '1861-04-12'),
    ('WWII begins (Europe, not US onset)', '1939-09-01'),
    ('D-Day (not war onset)', '1944-06-06'),
    ('Korean War action', '1950-06-27'),
    ('Gulf of Tonkin Resolution', '1964-08-07'),
    ('Desert Storm', '1991-01-17'),
    ('Afghanistan', '2001-10-07'),
    ('Iraq', '2003-03-20'),
    ('Russia invades Ukraine (not US onset)', '2022-02-24')
]


@lru_cache(maxsize=2500)
def sky(day: str) -> dict[str, float]:
    y, m, d = map(int, day.split('-'))
    jd = swe.julday(y, m, d, 12.0)
    output = {}
    for body, code in BODIES.items():
        pos, flags = swe.calc_ut(jd, code, swe.FLG_MOSEPH | swe.FLG_SPEED)
        if not flags & swe.FLG_MOSEPH:
            raise RuntimeError(f'Unexpected ephemeris backend: {day} {body} {flags}')
        output[body] = pos[0]
    return output


# Moon excluded because US founding clock is unverified.
NATAL = {body: lon for body, lon in sky('1776-07-04').items() if body != 'Moon'}


def scores(day: str) -> dict:
    transit = sky(day)
    directed = transit_conjunctions(NATAL, transit)
    outer_distance = {b: angular_distance(NATAL[b], transit[b]) for b in OUTERS}
    return {
        'directed_conjunction_contacts': len(directed),
        'directed_mars_contacts': sum(c.emitter == 'Mars' for c in directed),
        'directed_pluto_contacts': sum(c.emitter == 'Pluto' for c in directed),
        'uranus_return_1deg': int(outer_distance['Uranus'] <= 1.0),
        'any_outer_return_1deg': int(min(outer_distance.values()) <= 1.0),
        'closest_outer_return_deg': round(min(outer_distance.values()), 5)
    }


def controls(onset: str):
    onset_date = date.fromisoformat(onset)
    day = date(onset_date.year, 1, 1)
    while day.year == onset_date.year:
        if abs((day - onset_date).days) > 30:
            yield day.isoformat()
        day += timedelta(days=1)


def average(values):
    return sum(values) / len(values)


def run(outfile: Path | None = None) -> dict:
    cases = [{'label': name, 'date': day, 'scores': scores(day)}
             for name, day in DECLARED_US_WARS]
    control_data = {row['date']: [scores(d) for d in controls(row['date'])] for row in cases}
    keys = ('directed_conjunction_contacts', 'directed_mars_contacts',
            'directed_pluto_contacts', 'uranus_return_1deg', 'any_outer_return_1deg')
    summaries = {}
    rng = random.Random(20261031)
    N = 100_000
    for key in keys:
        event_values = [r['scores'][key] for r in cases]
        control_values = [[c[key] for c in control_data[r['date']]] for r in cases]
        observed = sum(event_values)
        ge, le = 0, 0
        for _ in range(N):
            result = sum(sample[rng.randrange(len(sample))] for sample in control_values)
            ge += (result >= observed)
            le += (result <= observed)
        summaries[key] = {
            'event_values': event_values,
            'event_mean': average(event_values),
            'control_mean': average([v for yr in control_values for v in yr]),
            'null_expected_total': sum(average(yr) for yr in control_values),
            'observed_total': observed,
            'null_p_ge_event': (ge + 1) / (N + 1),
            'null_p_le_event': (le + 1) / (N + 1),
            'within_year_control_mean': [average(yr) for yr in control_values]
        }
    result = {
        'research_only': True,
        'historical_time_basis': '12:00 UTC each date, including 1776 founding proxy',
        'ephemeris': 'pyswisseph MOSEPH, not repository SWIEPH file backend',
        'natal_body_moon_excluded': True,
        'natal_longitudes': NATAL,
        'case_definition': 'five distinct U.S. formally declared wars',
        'control_definition': 'same-year non-onset days outside ±30d, not peaceful-day verification',
        'source_outgoing_emitters': ['Sun', 'Moon', 'Mars', 'Pluto'],
        'not_implemented': ['houses', 'true placements', 'nonconjunction aspects', 'fringe',
                            'Spark', 'progressions', 'national founding time', 'uranus/neptune OOI'],
        'permutation_draws': N,
        'random_seed': 20261031,
        'case_rows': cases,
        'secondary_rows': [{'label': name, 'date': day, 'scores': scores(day)}
                           for name, day in SECONDARY],
        'matched_control_days': {key: len(value) for key, value in control_data.items()},
        'null_comparison': summaries
    }
    if outfile is None:
        outfile = Path(__file__).with_name('historical_test_results.json')
    outfile.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    for key, stat in summaries.items():
        print(key, 'events', stat['event_values'], 'control_expected', round(stat['null_expected_total'], 3),
              'p_ge', round(stat['null_p_ge_event'], 4))
    print('Saved', outfile)
    return result


if __name__ == '__main__':
    run()
