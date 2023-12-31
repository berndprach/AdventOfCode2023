
import unittest

from part2 import solve

GOAL_SOLUTION = 154


class TestPart2(unittest.TestCase):
    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
