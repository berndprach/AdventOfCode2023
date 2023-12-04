
import unittest

from part1 import solve, parse_line

GOAL_SOLUTION = 13


class TestPart1(unittest.TestCase):
    def test_first_digit(self):
        line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        winning_numbers, my_numbers = parse_line(line)
        self.assertListEqual(winning_numbers, [41, 48, 83, 86, 17])
        self.assertListEqual(my_numbers, [83, 86, 6, 31, 17, 9, 48, 53])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
