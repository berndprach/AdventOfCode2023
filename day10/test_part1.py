
import unittest

from part1 import solve

GOAL_SOLUTION1 = 4
GOAL_SOLUTION2 = 8


class TestPart1(unittest.TestCase):
    def test_solve(self):
        with open("test_input1.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION1)

        with open("test_input2.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION2)
