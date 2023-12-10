from enum import Enum
from typing import Optional


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Directions(Enum):
    RIGHT = Position(1, 0)
    LEFT = Position(-1, 0)
    UP = Position(0, -1)
    DOWN = Position(0, 1)


class Pipe:
    def __init__(self,
                 position: Position,
                 directions: tuple[Directions, Directions]):
        self.position = position
        self.directions = directions

        self.next_positions = (
            self.position + self.directions[0].value,
            self.position + self.directions[1].value,
        )

    def next_position(self, previous_position: Position) -> Position:
        if previous_position == self.next_positions[0]:
            return self.next_positions[1]
        elif previous_position == self.next_positions[1]:
            return self.next_positions[0]
        else:
            raise ValueError("Pipe does not connect to previous position")


Grid = dict[Position, Optional[Pipe]]


def valid_neighbours(position: Position, grid: Grid) -> list[Position]:
    return [
        position + direction.value
        for direction in Directions
        if position + direction.value in grid
    ]


SYMBOL_TO_DIRECTIONS = {
    "|": {Directions.UP, Directions.DOWN},
    "-": {Directions.LEFT, Directions.RIGHT},
    "L": {Directions.UP, Directions.RIGHT},
    "J": {Directions.UP, Directions.LEFT},
    "7": {Directions.DOWN, Directions.LEFT},
    "F": {Directions.DOWN, Directions.RIGHT},
}


def parse_lines(lines: list[str]) -> tuple[Position, Grid]:
    pipe_at_position = {}
    starting_position = None

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == ".":
                pipe = None
            elif character == "S":
                pipe = None
                starting_position = Position(x, y)
            elif character in SYMBOL_TO_DIRECTIONS:
                pipe_directions = SYMBOL_TO_DIRECTIONS[character]
                pipe = Pipe(Position(x, y), tuple(pipe_directions))
            else:
                raise ValueError(f"Unknown symbol {character}")
            pipe_at_position[Position(x, y)] = pipe

    if starting_position is None:
        raise ValueError("No starting position found")

    return starting_position, pipe_at_position


def place_pipe_at_starting_position(starting_position: Position,
                                    pipe_at_position: Grid):
    pipe_directions = set()
    for neighbour_position in valid_neighbours(starting_position,
                                               pipe_at_position):
        neighbour_pipe = pipe_at_position[neighbour_position]
        if neighbour_pipe is None:
            continue

        if starting_position in neighbour_pipe.next_positions:
            pipe_direction = Directions(neighbour_position - starting_position)
            pipe_directions.add(pipe_direction)

    assert len(pipe_directions) == 2
    d1, d2 = pipe_directions
    pipe_at_position[starting_position] = Pipe(starting_position, (d1, d2))


def solve(lines: list[str]) -> int:
    starting_position, pipe_at_position = parse_lines(lines)
    place_pipe_at_starting_position(starting_position, pipe_at_position)

    starting_pipe = pipe_at_position[starting_position]
    current_position_1, current_position_2 = starting_pipe.next_positions

    previous_position_1 = starting_position
    previous_position_2 = starting_position
    solution = 1

    while current_position_1 != current_position_2:
        previous_position_1, current_position_1 = update_positions(
            previous_position_1, current_position_1, pipe_at_position
        )

        previous_position_2, current_position_2 = update_positions(
            previous_position_2, current_position_2, pipe_at_position
        )

        solution += 1

    return solution


def update_positions(previous: Position,
                     current: Position,
                     pipe_at_position: Grid):
    current_pipe = pipe_at_position[current]
    next_position = current_pipe.next_position(previous)
    return current, next_position


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
