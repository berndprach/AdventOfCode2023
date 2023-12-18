
import unittest

from part2 import solve, parse_input

GOAL_SOLUTION = 952408144115


class TestPart2(unittest.TestCase):
    def test_parse_input(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        instructions = parse_input(lines[:2])
        print(f"{instructions = }")
        self.assertEqual(instructions, [
            ("R", 461937),
            ("D", 56407),
        ])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
