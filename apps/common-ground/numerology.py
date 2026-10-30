"""Explicit natal calculation adapter for the inspected LOOKS-LIKE-COSTAR method.

No generated interpretations live here. Each role retains its literal calculation
and method identifier; other legacy reduction/name methods are not substituted.
"""
from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

COSTAR_COMMIT = "023140de4ac9ebad8a804b4c984337135e77b19a"
NATAL_METHOD = "costar-core-natal-master-preserving-v1"
PMEI_METHOD = "costar-pmei-raw-letter-counts-v1"
MASTERS = {11, 22, 33}
VOWELS = set("AEIOU")
PLANE_MAP = {
    1: "mental", 2: "emotional", 3: "emotional", 4: "physical",
    5: "physical", 6: "emotional", 7: "intuitive", 8: "mental",
    9: "intuitive",
}
PLANE_NUMBERS = {
    "physical": {4, 5}, "mental": {1, 8},
    "emotional": {2, 3, 6}, "intuitive": {7, 9},
}
METHODS = {
    "natal": {
        "id": NATAL_METHOD,
        "source_commit": COSTAR_COMMIT,
        "source_url": f"https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_COMMIT}/services/numerology.ts#L238-L391",
        "letter_mapping": "Pythagorean A=1 through I=9, repeating through Z",
        "vowels": ["A", "E", "I", "O", "U"],
        "master_numbers_preserved": [11, 22, 33],
        "ultimate_goal": "reduce(reduce(month + day + year) + reduce(full-name letter-value sum))",
        "birth_force": "reduce(sum of all numeric birth-date digits))",
        "called_name": "reduce(reduce(first-name letter sum) + reduce(last-name letter sum)); middle names excluded by this specific role",
        "name_basis": "The full birth name supplied in the form; no name change or unprovided middle names are inferred.",
    },
    "pmei": {
        "id": PMEI_METHOD,
        "source_url": f"https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/{COSTAR_COMMIT}/services/pmeiEngine.ts#L267-L350",
        "rule": "One count per A-Z letter, categorized by its letter value. Counts are never digit-reduced.",
        "bins": {key: sorted(value) for key, value in PLANE_NUMBERS.items()},
        "margin_rule": "The legacy 'genius factor' label means only a top-minus-next count margin of at least 2, not measured intelligence.",
    },
    "legacy_differences": [
        "The name cue engine additionally classifies Y as a vowel; this adapter follows the natal calculator's A/E/I/O/U definition.",
        "The name cue engine reduces master numbers to a single digit; this adapter preserves 11, 22 and 33 as the natal calculator does.",
        "Ultimate Goal includes name and date. It is not silently renamed to a birth-date-only Life Path.",
        "Called Name here follows the source's first-plus-last calculation, not an inferred nickname calculation.",
        "No daily, monthly, progression or predictive timing rules are used.",
    ],
}


def reduce_with_chain(number: int) -> dict[str, Any]:
    if not isinstance(number, int) or isinstance(number, bool) or number < 0:
        raise ValueError("Reduction needs a non-negative integer.")
    sequence = [number]
    while sequence[-1] > 9 and sequence[-1] not in MASTERS:
        sequence.append(sum(int(digit) for digit in str(sequence[-1])))
    return {"value": sequence[-1], "compound": "/".join(map(str, sequence)),
            "sequence": sequence}


def letter_value(character: str) -> int:
    upper = character.upper()
    if upper < "A" or upper > "Z":
        return 0
    return (ord(upper[0]) - ord("A")) % 9 + 1


def value_from_name(name: str, kind: str = "all") -> dict[str, Any]:
    if kind not in {"all", "vowels", "consonants"}:
        raise ValueError("Unknown letter selection.")
    letters = []
    for character in name.lower():
        value = letter_value(character)
        if value <= 0:
            continue
        is_vowel = character.upper() in VOWELS
        if kind == "all" or (kind == "vowels" and is_vowel) or (kind == "consonants" and not is_vowel):
            letters.append({"letter": character.upper(), "value": value})
    return {"sum": sum(item["value"] for item in letters), "letters": letters,
            "calculation": " + ".join(f'{item["letter"]}({item["value"]})' for item in letters)}


def _metric(identifier: str, role: str, raw: int, calculation: str, **extra: Any) -> dict[str, Any]:
    reduction = reduce_with_chain(raw)
    return {
        "id": identifier, "name": role, "role": role, "raw": raw,
        **reduction, "calculation": calculation,
        "method_id": NATAL_METHOD, "source_ids": ["costar-natal-calculations"],
        **extra,
    }


def calculate_numerology(full_name: str, birth_date: str) -> dict[str, Any]:
    civil_date = date.fromisoformat(birth_date)
    clean_name = re.sub("[^A-Z]", "", full_name.upper())
    if not clean_name:
        raise ValueError("Enter a name with at least one A-Z letter.")
    parts = full_name.strip().split()
    expression = value_from_name(full_name)
    vowels = value_from_name(full_name, "vowels")
    initials = "".join(part[0] for part in parts)
    balance = value_from_name(initials)
    birthday_raw = civil_date.month + civil_date.day + civil_date.year
    birthday_component = reduce_with_chain(birthday_raw)
    expression_reduced = reduce_with_chain(expression["sum"])
    goal_raw = birthday_component["value"] + expression_reduced["value"]
    date_digits = [int(character) for character in birth_date if character.isdigit()]
    birth_force_raw = sum(date_digits)
    first = value_from_name(parts[0])
    last = value_from_name(parts[-1]) if len(parts) > 1 else {"sum": 0}
    first_reduced = reduce_with_chain(first["sum"])
    last_reduced = reduce_with_chain(last["sum"])
    called_raw = first_reduced["value"] + last_reduced["value"]
    metrics = [
        _metric("expression", "Expression", expression["sum"],
                f'{expression["calculation"]} = {expression["sum"]}',
                letters=expression["letters"]),
        _metric("soul_urge", "Soul Urge", vowels["sum"],
                f'{vowels["calculation"] or "No A/E/I/O/U vowels"} = {vowels["sum"]}',
                letters=vowels["letters"]),
        _metric("birth_force", "Birth Force", birth_force_raw,
                f'{" + ".join(map(str, date_digits))} = {birth_force_raw}'),
        _metric("ultimate_goal", "Ultimate Goal", goal_raw,
                f'Reduced birthday component {birthday_component["compound"]} + reduced full-name sum {expression_reduced["compound"]}; {birthday_component["value"]} + {expression_reduced["value"]} = {goal_raw}',
                birthday_component={"raw": birthday_raw, **birthday_component}),
        _metric("balance", "Balance Number", balance["sum"],
                f'Initials {initials}: {balance["calculation"]} = {balance["sum"]}'),
        _metric("called_name", "Called Name", called_raw,
                f'First name {first_reduced["compound"]} + last name {last_reduced["compound"]}; {first_reduced["value"]} + {last_reduced["value"]} = {called_raw}',
                name_basis="First and last supplied name parts, each reduced before addition"),
    ]
    planes = {key: {"count": 0, "percent": 0.0, "vowels": 0, "consonants": 0}
              for key in ("physical", "mental", "emotional", "intuitive")}
    letter_map = []
    for letter in clean_name:
        value = letter_value(letter)
        plane = PLANE_MAP[value]
        planes[plane]["count"] += 1
        planes[plane]["vowels" if letter in VOWELS else "consonants"] += 1
        letter_map.append({"letter": letter, "value": value, "plane": plane})
    total = len(clean_name)
    for row in planes.values():
        # JS parseFloat((count / total).toFixed(2)): ties choose the larger
        # positive value, unlike Python's built-in ties-to-even round().
        ratio = row["count"] / total
        row["percent"] = float(Decimal.from_float(ratio).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        row["ratio"] = ratio
    ranked = sorted(planes, key=lambda key: -planes[key]["count"])
    margin = planes[ranked[0]]["count"] - planes[ranked[1]]["count"]
    pmei = {
        "method_id": PMEI_METHOD,
        "source_ids": ["costar-pmei"],
        "planes": planes, "total_letters": total, "name_clean": clean_name,
        "qa_checksum_passed": sum(row["count"] for row in planes.values()) == total,
        "zero_planes": [key for key, row in planes.items() if row["count"] == 0],
        "genius_factor": {"plane": ranked[0] if margin >= 2 else None,
                         "margin": margin, "is_genius": margin >= 2,
                         "definition": "Legacy count-margin rule; not a measured intelligence score"},
        "harmony": [key for key, row in planes.items() if row["count"] in PLANE_NUMBERS[key]],
        "cross_matches": [
            {"plane": key, "total_equals": planes[key]["count"], "influence": "emotional"}
            for key in ("physical", "mental", "intuitive") if planes[key]["count"] in {2, 3, 6}
        ],
        "letter_map": letter_map,
        "tone": {"vowels": sum(row["vowels"] for row in planes.values()),
                 "consonants": sum(row["consonants"] for row in planes.values())},
    }
    warnings = []
    ignored = sorted({character for character in full_name if character.isalpha() and not re.fullmatch("[A-Za-z]", character)})
    if ignored:
        warnings.append("The inspected calculation uses A-Z letters; some non-ASCII letters are omitted or handled differently by the legacy modules. Verify spelling and method before using this comparison.")
    if vowels["sum"] == 0:
        warnings.append("No A/E/I/O/U vowels occur in the supplied name; Soul Urge is zero and has no supported number-meaning mapping.")
    return {
        "name_basis": full_name, "birth_date_basis": birth_date,
        "core_numbers": metrics, "metrics": metrics, "pmei": pmei,
        **{key: pmei[key] for key in ("planes", "total_letters", "zero_planes", "genius_factor", "harmony", "cross_matches")},
        "methods": METHODS, "warnings": warnings,
        "shared_input_note": "These name-derived measures share letters and arithmetic; they are different lenses, not independent confirmations.",
    }

