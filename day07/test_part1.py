
import unittest

from part1 import solve, get_hand_strength, get_sorted_counts

GOAL_SOLUTION = 6440


class TestPart1(unittest.TestCase):
    def test_get_sorted_counts(self):
        self.assertEqual(get_sorted_counts("AAKAK"), [3, 3, 3, 2, 2])
        self.assertEqual(get_sorted_counts("K2244"), [2, 2, 2, 2, 1])
        self.assertEqual(get_sorted_counts("23444"), [3, 3, 3, 1, 1])

    def test_get_hand_order(self):
        hand_order = get_hand_strength("AAKAK")
        self.assertEqual(hand_order, [3, 3, 3, 2, 2, 12, 12, 11, 12, 11])

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
