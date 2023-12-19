
import unittest

from part1 import solve, parse_input

GOAL_SOLUTION = 19114


class TestPart1(unittest.TestCase):
    def test_print_parsed_input(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        rules, part_ratings = parse_input(lines)
        print(f"{rules = }")
        print(f"{part_ratings = }")

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
