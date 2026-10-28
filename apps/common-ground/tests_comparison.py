"""Behavioral checks for source fidelity and uncertainty in the bridge composer."""
import copy
import json
import re
import unittest

from compare import compose_comparison
from sources import source_catalog, source_pack


PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

def chart_fixture(house=9, tone='Virgo', pulse='Capricorn'):
    return {'time': {'time_is_reference_only': False}, 'input': {'time_accuracy': 'nearest_minute'},
        'points': [{'id': planet, 'available': True, 'house': house, 'true_placement': 'Sagittarius',
            'tone': tone, 'pulse': pulse, 'longitude_deg': 166.5, 'display_dms': 'Virgo 16°30′00″',
            'sign_ruler': 'Mercury', 'retrograde': False} for planet in PLANETS]}

def number_fixture(value=5):
    return {'metrics': [{'id': role.lower().replace(' ', '-'), 'name': role, 'role': role,
            'value': value, 'compound': str(value), 'raw': value, 'calculation': 'Fixture input'}
        for role in ['Soul Urge', 'Expression', 'Called Name', 'Birth Force', 'Ultimate Goal', 'Balance Number']],
        'pmei': {'planes': {'physical': {'count': 4}, 'mental': {'count': 3}, 'emotional': {'count': 2}, 'intuitive': {'count': 0}}}}

def all_insights(result):
    return [row for domain in result['domains'] for row in domain['insights']]


class ComparisonBehaviorTests(unittest.TestCase):
    def test_actual_context_changes_the_comparison_without_inventing_a_new_number(self):
        first = compose_comparison(chart_fixture(), number_fixture())
        second = compose_comparison(chart_fixture(3, 'Gemini', 'Libra'), number_fixture())
        left = all_insights(first)[0]
        right = all_insights(second)[0]
        self.assertEqual(left['number'], right['number'])
        self.assertNotEqual(left['paragraph'], right['paragraph'])
        self.assertIn('House 9', left['paragraph'])
        self.assertIn('House 3', right['paragraph'])
        self.assertIn('exploration and experience', left['shared_contextual_themes'])
        self.assertIn('communication', right['shared_contextual_themes'])

    def test_same_number_is_not_promoted_into_independent_confirmations(self):
        result = compose_comparison(chart_fixture(), number_fixture())
        self.assertEqual(len(all_insights(result)), 9)
        self.assertFalse(result['has_scoring'])
        self.assertFalse(result['source_status']['empirical_association_established'])
        self.assertTrue(all(not row.get('independent_confirmation', False) for row in all_insights(result)))
        self.assertTrue(any('Planet presence does not confirm' in note for note in result['method_notes']))
        self.assertTrue(any('share name inputs' in note for note in result['method_notes']))

    def test_unknown_time_withholds_house_context_even_if_a_caller_supplies_it(self):
        chart = chart_fixture()
        chart['time']['time_is_reference_only'] = True
        result = compose_comparison(chart, number_fixture())
        self.assertTrue(result['reference_epoch_only'])
        for row in all_insights(result):
            self.assertEqual(row['availability'], 'reference_epoch_only')
            self.assertEqual(row['shared_contextual_themes'], [])
            self.assertNotIn('House 9', row['paragraph'])
            for ingredient in row['ingredients']:
                if ingredient['system'] == 'Astrology':
                    self.assertIsNone(ingredient['house'])
                    self.assertIsNone(ingredient['true_placement'])

    def test_master_calculation_is_preserved_and_root_fallback_is_explicit(self):
        result = compose_comparison(chart_fixture(), number_fixture(11))
        row = all_insights(result)[0]
        self.assertEqual(row['number'], 11)
        self.assertEqual(row['root_used_for_vocabulary'], 2)
        self.assertIn('calculation retains 11', row['paragraph'])
        self.assertTrue(row['ingredients'][0]['master_fallback_explicit'])

    def test_roles_remain_distinct_even_with_same_root(self):
        result = compose_comparison(chart_fixture(), number_fixture())
        roles = {row['numerology_role'] for row in all_insights(result)}
        self.assertTrue({'Soul Urge', 'Expression', 'Called Name', 'Birth Force', 'Ultimate Goal', 'Balance Number'}.issubset(roles))
        soul = next(row for row in all_insights(result) if row['id'] == 'motivation-soul-urge')
        expression = next(row for row in all_insights(result) if row['id'] == 'communication-expression')
        self.assertNotEqual(soul['paragraph'], expression['paragraph'])

    def test_every_citation_resolves_and_ingredients_are_not_falsely_bridge_citations(self):
        result = compose_comparison(chart_fixture(), number_fixture())
        catalog = {row['id']: row for row in source_catalog()}
        for row in all_insights(result):
            for source_id in row['source_ids']:
                self.assertIn(source_id, catalog)
        self.assertEqual(catalog['bridge-method-v1']['source_status'], 'ANALYST_PROPOSED_NOT_SOURCE_RULE')
        self.assertIsNone(catalog['bridge-method-v1']['url'])
        self.assertTrue(catalog['mr:sign-virgo']['witnesses'])
        self.assertFalse(source_pack()['generic_library_fallback_allowed'])
        self.assertFalse(result['source_status']['personal_report_approved'])

    def test_no_biography_or_personality_is_fabricated_from_the_components(self):
        result = compose_comparison(chart_fixture(), number_fixture())
        prose = ' '.join(row['paragraph'] for row in all_insights(result))
        self.assertIsNone(re.search(r'\byou are\b|\byou have always\b|your childhood|destined|will become|past life', prose, re.I))
        self.assertTrue(all(row['relationship'] == 'proposed_contextual_comparison' for row in all_insights(result)))

    def test_missing_object_is_not_replaced_with_an_available_planet(self):
        chart = chart_fixture()
        chart['points'] = [row for row in chart['points'] if row['id'] != 'Jupiter']
        result = compose_comparison(chart, number_fixture())
        row = all_insights(result)[0]
        self.assertEqual(row['planet'], 'Jupiter')
        self.assertEqual(row['availability'], 'chart_context_unavailable')
        self.assertEqual(len(row['ingredients']), 1)

    def test_zero_plane_and_large_counts_stay_literal(self):
        numbers = number_fixture()
        numbers['pmei']['planes']['physical']['count'] = 14
        result = compose_comparison(chart_fixture(), numbers)
        pmei = next(row for row in all_insights(result) if row['id'] == 'work-pmei')
        self.assertEqual(pmei['ingredients'][0]['counts']['physical'], 14)
        self.assertEqual(pmei['ingredients'][0]['counts']['intuitive'], 0)
        self.assertIn('Physical 14', pmei['paragraph'])
        self.assertIn('Intuitive 0', pmei['paragraph'])
        self.assertIsNone(pmei['number'])

    def test_missing_house_geometry_does_not_fabricate_a_life_arena(self):
        chart = chart_fixture()
        for point in chart['points']:
            point['house'] = None
            point['true_placement'] = None
        result = compose_comparison(chart, number_fixture())
        visible = ' '.join(domain['summary'] + ' ' + ' '.join(row['display_paragraph'] for row in domain['insights']) for domain in result['domains'])
        self.assertNotIn('House None', visible)
        self.assertIn('no house-based arena was resolved', visible)

    def test_pmei_missing_one_or_both_required_planets_is_unavailable(self):
        for missing in ({'Mars'}, {'Mercury'}, {'Mars', 'Mercury'}):
            with self.subTest(missing=missing):
                chart = chart_fixture()
                chart['points'] = [row for row in chart['points'] if row['id'] not in missing]
                result = compose_comparison(chart, number_fixture())
                pmei = next(row for row in all_insights(result) if row['id'] == 'work-pmei')
                self.assertEqual(pmei['availability'], 'chart_context_unavailable')
                self.assertIn('not both available', pmei['paragraph'])
                self.assertIn('missing Mars or Mercury', pmei['display_question'])
                self.assertNotIn('House None', pmei['display_paragraph'])

    def test_same_five_roles_use_different_source_banks_and_substantive_questions(self):
        result = compose_comparison(chart_fixture(), number_fixture(5))
        selected = [next(row for row in all_insights(result) if row['id'] == key) for key in
            ['motivation-soul-urge', 'motivation-ultimate-goal', 'communication-expression', 'communication-called-name']]
        role_sources = [row['ingredients'][0]['role_meaning_source_id'] for row in selected]
        self.assertEqual(len(set(role_sources)), 4)
        normalized_prose = []
        for row in selected:
            normalized_prose.append(row['display_paragraph'].replace(row['numerology_role'], 'ROLE'))
            self.assertIn(row['ingredients'][0]['role_meaning_source_id'], row['source_ids'])
            self.assertTrue(row['ingredients'][0]['role_meaning'])
            self.assertLessEqual(len(row['display_paragraph'].split()), 120)
        self.assertEqual(len(set(normalized_prose)), 4)
        self.assertEqual(len({row['display_question'] for row in selected}), 4)
        self.assertIn('motives', selected[0]['display_paragraph'])
        self.assertIn('direction bank', selected[1]['display_paragraph'])
        self.assertIn('outward adaptability', selected[2]['display_paragraph'])
        self.assertIn('received by others', selected[3]['display_paragraph'])

    def test_all_six_role_banks_have_nine_distinct_attributed_entries(self):
        pack = source_pack()
        self.assertEqual(len(pack['role_vocabularies']), 6)
        for role, entries in pack['role_vocabularies'].items():
            self.assertEqual(set(entries), {str(n) for n in range(1, 10)})
            for digit, source_id in entries.items():
                record = pack['sources'][source_id]
                self.assertEqual(record['role'], role)
                self.assertEqual(record['number'], int(digit))
                self.assertTrue(record['statement'])
                self.assertIn('023140de4ac9ebad8a804b4c984337135e77b19a', record['url'])


if __name__ == '__main__':
    unittest.main()
