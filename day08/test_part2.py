
import unittest

from part2 import solve, solve_brute_force, print_all_end_node_equations

GOAL_SOLUTION = 6


class TestPart2(unittest.TestCase):
    def test_brute_force(self):
        with open("test_input3.txt") as f:
            lines = f.read().splitlines()
        solution = solve_brute_force(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)

    def test_brute_force_on_full_input(self):
        with open("input.txt") as f:
            lines = f.read().splitlines()
        with self.assertRaises(ValueError):
            solve_brute_force(lines)

    def test_print_all_end_node_equations(self):
        with open("test_input3.txt") as f:
            lines = f.read().splitlines()
        print_all_end_node_equations(lines)

    def test_print_all_simplified_equations(self):
        with open("test_input3.txt") as f:
            lines = f.read().splitlines()
        print_all_end_node_equations(lines, with_simplification=True)

    def test_print_all_simplified_equations_on_full_input(self):
        with open("input.txt") as f:
            lines = f.read().splitlines()
        print_all_end_node_equations(lines, with_simplification=True)

    def test_solve(self):
        with open("test_input3.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
