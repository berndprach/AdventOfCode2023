
from time import time
from typing import Callable

from part1 import read_input, Position, parse_input, get_neighbours


def count_reachable_positions(is_rock: Callable[[Position], bool],
                              starting_position: Position,
                              number_of_steps: int,
                              ) -> int:
    if number_of_steps % 2 == 0:
        starting_positions = {starting_position}
    else:
        starting_positions = {
            neighbour
            for neighbour in get_neighbours(starting_position)
            if not is_rock(neighbour)
        }

    previouse_new_gardens = set()
    current_new_gardens = starting_positions
    reached_count = len(starting_positions)

    for _ in range(number_of_steps // 2):
        one_step = do_step(current_new_gardens, is_rock)
        two_step = do_step(one_step, is_rock)

        next_new_gardens = (
                two_step - current_new_gardens - previouse_new_gardens
        )

        reached_count += len(next_new_gardens)
        previouse_new_gardens = current_new_gardens
        current_new_gardens = next_new_gardens

    return reached_count


def do_step(positions: set[Position], is_rock: Callable) -> set[Position]:
    new_positions = set()
    for position in positions:
        for neighbour in get_neighbours(position):
            if not is_rock(neighbour):
                new_positions.add(neighbour)
    return new_positions


def solve(lines: list[str],
          number_of_steps=26501365,
          starting_i=0) -> int:
    """
    . . . . . . . . . . .
    . . . . . # . . . . .
    . . . . # # # . . . .
    . . . # # # # # . . .
    . . # # # # # # # . .
    . # # # # S # # # # .
    . . # # # # # # # . .
    . . . # # # # # . . .
    . . . . # # # . . . .
    . . . . . # . . . . .
    . . . . . . . . . . .
    """

    is_rock_small, starting_position = parse_input(lines)
    width = len(lines[0])
    height = len(lines)

    assert width == height

    def is_rock(position: Position) -> bool:
        x, y = position
        small_x = x % width
        small_y = y % height
        return is_rock_small[(small_x, small_y)]

    if number_of_steps < (2+starting_i)*width:
        return count_reachable_positions(
            is_rock,
            starting_position,
            number_of_steps
        )

    remainder = number_of_steps % width
    xs, ys = [], []
    for i in range(starting_i, starting_i + 3):
        n_steps = width * i + remainder
        reached_count = count_reachable_positions(
            is_rock,
            starting_position,
            n_steps
        )
        xs.append(n_steps)
        ys.append(reached_count)

    a, b, c = fit_quadratic(xs, ys)

    n = number_of_steps
    solution_estimate = a * n ** 2 + b * n + c
    print(f"{solution_estimate = }")
    return round(solution_estimate)


def fit_quadratic(xs: list[int], ys: list[int]) -> tuple[float, float, float]:
    # - Fits a quadratic function: y = a * x^2 + b * x + c.
    # - Assumes xs are equally spaced.
    # - Uses the last three points.
    # - Relies on the facts that
    #   1) y1 - 2*y2 + y3 = a * (x1^2 - 2*x2^2 + x3^2)   (to find a)
    #   2) y1 - y2 = a * (x1 - x2)^2 + b * (x1 - x2)     (to find b)
    #   3) y1 = a * x1^2 + b * x1 + c                    (to find c)

    if xs[-1] - xs[-2] != xs[-2] - xs[-3]:
        raise NotImplementedError("xs must be equally spaced")

    a = (ys[-1] - 2*ys[-2] + ys[-3]) / (xs[-1]**2 - 2*xs[-2]**2 + xs[-3]**2)
    b = (ys[-1] - ys[-2] - a * xs[-1] ** 2 + a * xs[-2]**2) / (xs[-1] - xs[-2])
    c = ys[-1] - a * xs[-1] ** 2 - b * xs[-1]
    return a, b, c


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
