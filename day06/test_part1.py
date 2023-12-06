
import unittest

from part1 import solve, parse_lines

GOAL_SOLUTION = 288


class TestPart1(unittest.TestCase):
    def test_parse_input(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        times, furthest_distances = parse_lines(lines)
        self.assertEqual(times, [7, 15, 30])
        self.assertEqual(furthest_distances, [9, 40, 200])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
