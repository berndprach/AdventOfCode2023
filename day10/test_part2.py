
import unittest

from part2 import solve

GOAL_SOLUTIONS = {
    "1": 1,
    "2": 1,
    "3": 4,
    "4": 8,
}


class TestPart2(unittest.TestCase):
    def test_solve(self):
        for i, goal_solution in GOAL_SOLUTIONS.items():
            with open(f"test_input{i}.txt") as f:
                lines = f.read().splitlines()
            solution = solve(lines)
            print(f"{i}: {solution = }")
            self.assertEqual(solution, goal_solution)
