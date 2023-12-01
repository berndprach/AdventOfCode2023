
import unittest

from part2 import solve, first_digit, last_digit

GOAL_SOLUTION = 281


class TestPart2(unittest.TestCase):
    def test_first_number(self):
        self.assertEqual(first_digit("two1nine"), 2)
        self.assertEqual(first_digit("zoneight234"), 1)

    def test_last_number(self):
        self.assertEqual(last_digit("two1nine"), 9)
        self.assertEqual(last_digit("zoneight234"), 4)

    def test_solve(self):
        with open("test_input2.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
