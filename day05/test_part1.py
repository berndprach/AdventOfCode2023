
import unittest

from part1 import solve, parse_lines

GOAL_SOLUTION = 35


class TestPart1(unittest.TestCase):
    def test_parse_lines(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        lines = lines[:8]
        print("="*40)
        print("\n".join(lines))
        print("="*40)

        seeds, category_maps = parse_lines(lines)
        self.assertEqual(seeds, [79, 14, 55, 13])

        seed_map = category_maps["seed"]
        self.assertEqual(seed_map.category_name, "seed")
        self.assertEqual(seed_map.next_category, "soil")
        self.assertEqual(seed_map.map_tuples, [(50, 98, 2), (52, 50, 48)])

        soil_map = category_maps["soil"]
        self.assertEqual(soil_map.category_name, "soil")
        self.assertEqual(soil_map.next_category, "fertilizer")
        self.assertEqual(soil_map.map_tuples, [(0, 15, 37)])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
