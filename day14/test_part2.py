
import unittest

from part1 import parse_lines
from part2 import solve, rotate_clockwise
from test_part1 import print_platform

GOAL_SOLUTION = 64


class TestPart2(unittest.TestCase):
    def test_rotate_clockwise(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        platform = parse_lines(lines)
        print("Original platform:")
        print_platform(platform)

        rotated_platform = rotate_clockwise(platform)
        print("Rotated platform:")
        print_platform(rotated_platform)

        rotated4x_platform = rotate_clockwise(
            rotate_clockwise(rotate_clockwise(rotated_platform)))

        self.assertDictEqual(platform, rotated4x_platform)

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
