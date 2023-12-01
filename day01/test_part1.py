
import unittest

from part1 import solve, first_digit, last_digit

GOAL_SOLUTION = 142


class TestPart1(unittest.TestCase):
    def test_first_digit(self):
        self.assertEqual(first_digit("1abc2"), 1)
        self.assertEqual(first_digit("pqr3stu8vwx"), 3)

    def test_last_digit(self):
        self.assertEqual(last_digit("1abc2"), 2)
        self.assertEqual(last_digit("pqr3stu8vwx"), 8)

    def test_solve(self):
        with open("test_input1.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
