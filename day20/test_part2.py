
import unittest

from part1 import read_input, parse_input
from part2 import solve, solve_brute_force, find_incoming_highs

GOAL_SOLUTION = 281


class TestPart2(unittest.TestCase):
    def test_solve_brute_force(self):
        with open("input.txt") as f:
            lines = f.read().splitlines()
        solution = solve_brute_force(lines, number_of_button_presses=10_000)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)

    def test_find_incoming_highs(self):
        with open("input.txt") as f:
            lines = f.read().splitlines()
        pulse_modules = parse_input(lines)

        last_incoming_was_high_rg = find_incoming_highs(pulse_modules, "rg")
        print(f"\n{last_incoming_was_high_rg = }\n")

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
