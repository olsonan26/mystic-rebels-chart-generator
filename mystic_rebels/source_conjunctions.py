"""Source-grounded directional conjunctions ONLY (isolated research API).

PURE ASTROLOGY source pp.236-246 and Phase-9 recovered OOI audit:
Sun 10°, Moon 3°, Mars 4°, Pluto 1.5°, Chiron 1°.
Approximate Saturn 7.5° is PROVISIONAL and excluded by default.
Do not infer aspects, fringe, houses, Spark, or full transit engines from this.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

SOURCE_RADII_DEG = {'Sun': 10.0, 'Moon': 3.0, 'Mars': 4.0, 'Pluto': 1.5, 'Chiron': 1.0}
PROVISIONAL_RADII_DEG = {'Saturn': 7.5}


def angular_distance(a: float, b: float) -> float:
    """Smallest angular displacement on the ecliptic, within [0, 180]."""
    if not (isfinite(a) and isfinite(b)):
        raise ValueError('Longitudes must be finite')
    return abs((a - b + 180) % 360 - 180)


@dataclass(frozen=True)
class DirectedConjunction:
    emitter: str
    receiver: str
    distance_deg: float
    emitter_radius_deg: float
    within_emitter_orb: bool
    status: str = 'source_conjunction_only'


def directed_conjunction(emitter: str, emitter_lon: float, receiver: str,
                         receiver_lon: float, *, allow_provisional: bool = False) -> DirectedConjunction:
    """Never add emitter and receiver orbs. Unverified emitting radii fail closed."""
    radii = dict(SOURCE_RADII_DEG)
    if allow_provisional:
        radii.update(PROVISIONAL_RADII_DEG)
    if emitter not in radii:
        raise KeyError(f'No verified outgoing OOI for {emitter!r}; cannot assert an aspect')
    distance = angular_distance(emitter_lon, receiver_lon)
    return DirectedConjunction(
        emitter, receiver, distance, radii[emitter], distance <= radii[emitter],
        'provisional_saturn' if emitter == 'Saturn' else 'source_conjunction_only'
    )


def transit_conjunctions(natal: dict[str, float], transit: dict[str, float], *,
                         include_provisional: bool = False) -> list[DirectedConjunction]:
    """Only TRANSIT emitter -> NATAL receiver; no reverse ecosystem implication."""
    radii = SOURCE_RADII_DEG | (PROVISIONAL_RADII_DEG if include_provisional else {})
    return [result for emitter in radii if emitter in transit
            for receiver, natal_lon in natal.items()
            if (result := directed_conjunction(emitter, transit[emitter], receiver,
                 natal_lon, allow_provisional=include_provisional)).within_emitter_orb]
