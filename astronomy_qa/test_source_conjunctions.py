import unittest
from mystic_rebels.source_conjunctions import angular_distance, directed_conjunction, transit_conjunctions


class SourceConjunctionTests(unittest.TestCase):
    def test_wrap(self):
        self.assertAlmostEqual(angular_distance(359, 1), 2)

    def test_source_forced_example(self):
        self.assertTrue(directed_conjunction('Saturn', 10, 'Moon', 5, allow_provisional=True).within_emitter_orb)
        self.assertFalse(directed_conjunction('Moon', 5, 'Saturn', 10).within_emitter_orb)

    def test_no_combined_orbs(self):
        self.assertFalse(directed_conjunction('Moon', 5, 'Moon', 10).within_emitter_orb)
        self.assertFalse(directed_conjunction('Moon', 10, 'Moon', 5).within_emitter_orb)

    def test_boundary(self):
        self.assertTrue(directed_conjunction('Mars', 5, 'Mercury', 9).within_emitter_orb)
        self.assertFalse(directed_conjunction('Mars', 5, 'Mercury', 9.001).within_emitter_orb)

    def test_unknown_orb_rejected(self):
        with self.assertRaises(KeyError):
            directed_conjunction('Uranus', 0, 'Moon', 0)

    def test_transit_not_bidirectional(self):
        contacts = transit_conjunctions({'Moon': 5}, {'Saturn': 10, 'Moon': 10}, include_provisional=True)
        self.assertEqual([c.emitter for c in contacts], ['Saturn'])

    def test_finite(self):
        with self.assertRaises(ValueError):
            angular_distance(float('nan'), 0)


if __name__ == '__main__':
    unittest.main()
