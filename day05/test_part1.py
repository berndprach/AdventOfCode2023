
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

        seeds, category_to_next, category_maps = parse_lines(lines)
        self.assertEqual(seeds, [79, 14, 55, 13])
        self.assertEqual(category_to_next, {
            "seed": "soil",
            "soil": "fertilizer",
        })
        self.assertEqual(category_maps, {
            "seed": [(50, 98, 2), (52, 50, 48)],
            "soil": [(0, 15, 37)],
        })

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
