
import unittest

from part1 import solve

GOAL_SOLUTION = 142


class TestPart1(unittest.TestCase):
    def test_first_digit(self):
        self.assertEqual(first_digit("1abc2"), 1)
        self.assertEqual(first_digit("pqr3stu8vwx"), 3)

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
