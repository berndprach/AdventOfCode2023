
import unittest

from part1 import solve, Ray, intersect_rays

GOAL_SOLUTION = 2


class TestPart1(unittest.TestCase):
    def test_intersect_rays(self):
        ray1 = Ray((-1, 0), (1, 0))
        ray2 = Ray((0, -1), (0, 1))
        intersection = intersect_rays(ray1, ray2)
        print(f"{intersection = }")
        goal_intersection = (0., 0.)
        self.assertAlmostEqual(intersection[0], goal_intersection[0])
        self.assertAlmostEqual(intersection[1], goal_intersection[1])

        ray1 = Ray((19, 13), (-2, 1))
        ray2 = Ray((18, 19), (-1, -1))
        intersection = intersect_rays(ray1, ray2)
        print(f"{intersection = }")
        goal_intersection = (14.333, 15.333)
        self.assertAlmostEqual(intersection[0], goal_intersection[0], places=3)
        self.assertAlmostEqual(intersection[1], goal_intersection[1], places=3)

    def test_solve(self):
        with open("test_input.txt") as f:
            lines = f.read().splitlines()
        solution = solve(lines, s=7, t=27)
        print(f"{solution = }")
        self.assertEqual(solution, GOAL_SOLUTION)
