
import unittest

from part2 import parse_lines, get_galaxy_positions, get_paiwise_distances


class TestPart2(unittest.TestCase):
    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        occupied_positions = parse_lines(lines)

        galaxy_positions = get_galaxy_positions(occupied_positions,
                                                expansion_factor=10)
        pairwise_distances = get_paiwise_distances(galaxy_positions)
        self.assertEqual(sum(pairwise_distances) // 2, 1030)

        galaxy_positions = get_galaxy_positions(occupied_positions,
                                                expansion_factor=100)
        pairwise_distances = get_paiwise_distances(galaxy_positions)
        self.assertEqual(sum(pairwise_distances) // 2, 8410)
