
import unittest

from part2 import solve

GOAL_SOLUTIONS = {
    6: 16,
    10: 50,
    50: 1594,
    100: 6536,
    500: 167004,
    1000: 668697,
    5000: 16733044,
}


class TestPart2(unittest.TestCase):
    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        for number_of_steps, goal_solution in GOAL_SOLUTIONS.items():
            solution = solve(
                lines,
                number_of_steps=number_of_steps,
                starting_i=5,
            )
            print(f"{number_of_steps = }: {solution = }")
            self.assertEqual(solution, goal_solution)
