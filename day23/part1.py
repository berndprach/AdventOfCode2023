from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


DIRECTIONS = {
    ">": Position(1, 0),
    "<": Position(-1, 0),
    "^": Position(0, -1),
    "v": Position(0, 1),
}


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Grid = dict[Position, str]


def parse_input(lines: list[str]) -> Grid:
    characters: dict[Position, str] = {}
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            characters[Position(x, y)] = character
    return characters


Graph = dict[Position, list[Position]]


def get_neighbour_graph(characters: Grid) -> Graph:
    next_positions: Graph = {}
    for position, character in characters.items():
        if character == ".":
            next_positions[position] = [
                position + direction
                for direction in DIRECTIONS.values()
                if characters.get(position + direction, "#") != "#"
            ]
        elif character == "#":
            continue
        else:  # ^, >, v or <
            direction = DIRECTIONS[character]
            next_positions[position] = [position + direction]

    return next_positions


def find_longest_path(start: Position, goal: Position, next_positions) -> int:
    longest_path_to: dict[Position, int] = {start: 0}
    queue = [(start, start)]  # (current, previous)

    while len(queue) > 0:
        current, previous = queue.pop(0)  # first = the shortest current path

        if longest_path_to[current] > 10_000:
            raise ValueError("Seems there is a cycle!")

        for next_position in next_positions[current]:
            if next_position == previous:
                continue

            longest_path_to[next_position] = longest_path_to[current] + 1
            queue.append((next_position, current))

    return longest_path_to[goal]


def solve(lines: list[str]) -> int:
    start_x = lines[0].index(".")
    start = Position(start_x, 0)
    goal_x = lines[-1].index(".")
    goal = Position(goal_x, len(lines) - 1)

    characters = parse_input(lines)
    next_positions = get_neighbour_graph(characters)

    return find_longest_path(start, goal, next_positions)


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
