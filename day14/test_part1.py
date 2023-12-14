
import unittest

from part1 import solve, tilt_north, parse_lines

GOAL_SOLUTION = 136


class TestPart1(unittest.TestCase):
    def test_tilt_north(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        platform = parse_lines(lines)
        tilt_north(platform)
        print_platform(platform)

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)


def print_platform(platform):
    max_x = max(x for x, y in platform)
    max_y = max(y for x, y in platform)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(platform[(x, y)].value, end="")
        print()
    print()
