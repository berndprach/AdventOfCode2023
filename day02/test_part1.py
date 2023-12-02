
import unittest

import part1
from part1 import solve, Color

GOAL_SOLUTION = 8


class TestPart1(unittest.TestCase):
    def test_parse_reveal_string(self):
        sample_string = "3 blue, 4 red"
        sample_dict = part1.parse_sample_string(sample_string)
        self.assertEqual(3, sample_dict[Color.BLUE])
        self.assertEqual(4, sample_dict[Color.RED])
        self.assertEqual(0, sample_dict[Color.GREEN])

    def test_parse_line(self):
        line = "Game 1: 3 blue, 4 red; 5 green, 2 red"
        game_id, samples = part1.parse_line(line)
        self.assertEqual(game_id, 1)
        self.assertEqual(len(samples), 2)

        self.assertEqual(3, samples[0][part1.Color.BLUE])
        self.assertEqual(4, samples[0][part1.Color.RED])
        self.assertEqual(0, samples[0][part1.Color.GREEN])

        self.assertEqual(5, samples[1][part1.Color.GREEN])
        self.assertEqual(2, samples[1][part1.Color.RED])
        self.assertEqual(0, samples[1][part1.Color.BLUE])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
