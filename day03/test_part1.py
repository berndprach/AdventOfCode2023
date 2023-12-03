
import unittest

from part1 import solve, find_numbers_in_line, Position

GOAL_SOLUTION = 4361


class TestPart1(unittest.TestCase):
    def test_find_numbers_in_line(self):
        line = "467..114.."
        numbers = find_numbers_in_line(line, line_number=0)
        self.assertEqual(len(numbers), 2)

        self.assertEqual(numbers[0].value, 467)
        self.assertEqual(len(numbers[0].positions), 3)
        self.assertIn(Position(0, 0), numbers[0].positions)
        self.assertIn(Position(1, 0), numbers[0].positions)
        self.assertIn(Position(2, 0), numbers[0].positions)

        self.assertEqual(numbers[1].value, 114)
        self.assertEqual(len(numbers[1].positions), 3)
        self.assertIn(Position(5, 0), numbers[1].positions)
        self.assertIn(Position(6, 0), numbers[1].positions)
        self.assertIn(Position(7, 0), numbers[1].positions)

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
