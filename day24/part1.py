from dataclasses import dataclass
from time import time
from typing import Optional


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


@dataclass
class Ray:
    point: tuple[int, int]
    direction: tuple[int, int]


def intersect_rays(ray1: Ray, ray2: Ray) -> Optional[tuple[float, float]]:
    x1, y1 = ray1.point
    dx1, dy1 = ray1.direction
    x2, y2 = ray2.point
    dx2, dy2 = ray2.direction

    nominator_t = (x2 - x1) * dy2 - (y2 - y1) * dx2
    nominator_u = (x2 - x1) * dy1 - (y2 - y1) * dx1
    denominator = dx1 * dy2 - dy1 * dx2

    if denominator == 0:
        return None  # Lines are parallel

    t = nominator_t / denominator
    u = nominator_u / denominator

    if t < 0 or u < 0:
        return None

    return x1 + t * dx1, y1 + t * dy1


def parse_line_2d(line: str) -> Ray:
    # "19, 13, 30 @ -2, 1, -2"
    point_str, direction_str = line.split(" @ ")
    x, y, z = [int(i) for i in point_str.split(",")]
    dx, dy, dz = [int(i) for i in direction_str.split(",")]
    return Ray((x, y), (dx, dy))


def solve(lines: list[str], s=200000000000000, t=400000000000000) -> int:
    rays = [parse_line_2d(line) for line in lines]
    solution = 0
    for i, ray1 in enumerate(rays):
        for ray2 in rays[i+1:]:
            intersection = intersect_rays(ray1, ray2)
            if (
                    intersection is not None
                    and s <= intersection[0] <= t
                    and s <= intersection[1] <= t
            ):
                solution += 1
    return solution


def main():
    lines = read_input()
    if len(lines) == 0:
        raise ValueError("Input is empty")

    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
