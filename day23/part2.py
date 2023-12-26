from time import time
from typing import Optional

from part1 import read_input, Position, DIRECTIONS, parse_input, Graph


def get_neighbour_graph(characters: dict[Position, str]) -> Graph:
    next_positions: dict[Position, list[Position]] = {}
    for position, character in characters.items():
        if character == "#":
            continue

        next_positions[position] = [
            position + direction
            for direction in DIRECTIONS.values()
            if characters.get(position + direction, "#") != "#"
        ]

    return next_positions


# Graph = dict[Position, list[Position]]
GraphWithDistance = dict[Position, list[tuple[Position, int]]]


def simplify_graph(next_positions: Graph) -> GraphWithDistance:
    simplified = {}
    for position, neighbour_positions in next_positions.items():
        if len(neighbour_positions) == 2:
            continue

        simplified[position] = []
        for neighbour in neighbour_positions:
            next_intersection, distance = get_next_intersection(
                position, neighbour, next_positions
            )

            simplified[position].append((next_intersection, distance))

    return simplified


def get_next_intersection(previous: Position,
                          current: Position,
                          next_positions: Graph,
                          ) -> tuple[Position, int]:
    # Gets the next intersection or the next dead end.
    distance = 1
    while len(next_positions[current]) == 2:
        for potential_next in next_positions[current]:
            if potential_next == previous:
                continue

            previous = current
            current = potential_next
            distance += 1
            break

    return current, distance


class NoPathToGoalPossible(Exception):
    pass


def find_longest_path(current: Position,
                      goal: Position,
                      visited: set[Position],
                      next_positions) -> Optional[int]:
    visited.add(current)

    if current == goal:
        visited.remove(current)
        return 0

    next_options = [
        (p, d) for (p, d) in next_positions[current]
        if p not in visited
    ]

    path_lengths = []
    for next_position, distance in next_options:
        try:
            path_length = find_longest_path(
                next_position,
                goal,
                visited,
                next_positions
            )
        except NoPathToGoalPossible:
            continue
        path_lengths.append(path_length + distance)

    visited.remove(current)  # Restore visited to function call state

    if len(path_lengths) == 0:
        raise NoPathToGoalPossible

    longest_path_length = max(path_lengths)
    return longest_path_length


def solve(lines: list[str]) -> int:
    start_x = lines[0].index(".")
    start = Position(start_x, 0)
    goal_x = lines[-1].index(".")
    goal = Position(goal_x, len(lines) - 1)

    characters = parse_input(lines)
    next_positions = get_neighbour_graph(characters)
    next_positions = simplify_graph(next_positions)

    return find_longest_path(start, goal, set(), next_positions)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
