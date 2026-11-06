"""Offline bounded semantic return; no model, customer endpoint or approval.

Authority vocabulary comes from the pinned private core through personal_review.
Candidates can select claim IDs only; calculated/source values are not inputs
to the candidate API. A digest binds identity but is NOT proof of source truth.
"""
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from personal_review import digest, FIELDS


@dataclass(frozen=True)
class Theme:
    function: str
    expressed_in: str
    qualified_by: tuple = ()


def return_base(before, meaning):
    """Noncommutative theme construction, not a sum or a biography rule."""
    return Theme(before.function, before.expressed_in,
                 before.qualified_by + (meaning,))


class ReviewSession:
    def __init__(self, core, review):
        from nadia_core.interpretation import function_components
        from nadia_core.synthesis import validate_composition
        record = review['calculated_record']
        valid = validate_composition(core, review['composition'], record,
                                     review['question'], review['owner_id'],
                                     motion=review['motion_input'])
        positions = {b: p['longitude'] for b, p in record['positions'].items()}
        expected = function_components(core, positions, record['ascendant'])
        if (not valid['valid'] or digest(expected) != digest(review['components'])
                or digest(record) != review['calculated_record_sha256']):
            raise ValueError('Recomputed chart/source composition mismatch')
        # Serialize, do not retain a mutable caller-owned object.
        self.__snapshot = json.dumps(review, sort_keys=True, allow_nan=False)
        self.snapshot_id = digest(json.loads(self.__snapshot))

    def evidence(self):
        review = json.loads(self.__snapshot)
        moon = next(n for n in review['composition']['nodes'] if n['body'] == 'Moon')
        component = next(n for n in review['components'] if n['body'] == 'Moon')
        occupied = component['placement']['house']
        claims, missing = {}, []
        initial = None
        if occupied in FIELDS:
            initial = Theme('emotional safety', FIELDS[occupied][0])
        else:
            missing.append('occupied_Field_not_in_existing_inspected_finite_scope')
        after = initial
        returns = []
        for delegate in moon['delegated_houses']:
            # Different core versions may carry more metadata; the calculated
            # representation itself is never inferred from natural rulership.
            house = delegate['house']
            meaning = FIELDS.get(house)
            if house == 9:
                meaning = ('expansion', ['original-page-284', 'original-page-285'])
            entry = {'represented_configuration': delegate,
                     'operation': 'represented_Field_qualifies_function',
                     'source_refs': ['original-page-187', 'original-page-284', 'original-page-285'],
                     'occupant_return': 'unresolved_full_assessed_condition_not_substituted'}
            if initial is not None and meaning:
                after = return_base(after, meaning[0])
                entry.update(status='partial_theme_return', contribution=meaning[0],
                             meaning_source_refs=meaning[1])
            else:
                entry.update(status='withheld', contribution=None)
                missing.append('represented_or_occupied_Field_meaning_unavailable_for_return')
            returns.append(entry)
        if after and after != initial:
            text = (f"Emotional safety concerned with {' and '.join(after.qualified_by)}, "
                    f"expressed in the area of {after.expressed_in}.")
            claims['theme:Moon:base-return'] = text
        return {'snapshot_id': self.snapshot_id, 'owner_id': review['owner_id'],
                'initial': initial.__dict__ if initial else None,
                'contributions': returns, 'after': after.__dict__ if after else None,
                'claims': claims, 'missing': missing + [
                    'complete_represented_occupant_return', 'complete_ruler_Bridge_return',
                    'Tone_Pulse_Spark_contextual_integration',
                    'question_specific_priority', 'personal_confirmation'],
                'personal_readings_approved': False,
                'scope': 'bounded_rule_application_requires_semantic_review'}

    def render_selection(self, candidate):
        """Strict selection protocol. No free prose parsing or repair."""
        if not isinstance(candidate, dict) or set(candidate) != {'snapshot_id', 'claim_ids'}:
            raise ValueError('Only snapshot_id and claim_ids permitted')
        ids = candidate['claim_ids']
        evidence = self.evidence()
        if (candidate['snapshot_id'] != self.snapshot_id or not isinstance(ids, list)
                or any(not isinstance(i, str) for i in ids)
                or len(ids) != len(set(ids))
                or any(i not in evidence['claims'] for i in ids)):
            raise ValueError('Unknown, repeated or cross-snapshot claim')
        return '\n'.join(evidence['claims'][i] for i in ids)
