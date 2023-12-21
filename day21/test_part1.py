
import unittest

from part1 import solve

GOAL_SOLUTION = 16


class TestPart1(unittest.TestCase):
    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines, number_of_steps=6)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
