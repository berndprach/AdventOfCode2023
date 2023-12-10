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

    def __neg__(self):
        return Position(-self.x, -self.y)

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
                 directions: Optional[tuple[Directions, Directions]]):
        self.position = position
        self.directions = directions

        self.next_position = (
            self.position + self.directions[0].value,
            self.position + self.directions[1].value,
        ) if self.directions is not None else None

    def next_position(self, previous_position: Position) -> Position:
        if self.directions is None:
            raise ValueError("Pipe has no directions")
        if previous_position == self.position + self.directions[0].value:
            return self.position + self.directions[1].value
        elif previous_position == self.position + self.directions[1].value:
            return self.position + self.directions[0].value
        else:
            raise ValueError("Pipe does not connect to previous position")


Grid = dict[Position, Pipe]


SYMBOL_TO_DIRECTION = {
    "|": {Directions.UP, Directions.DOWN},
    "-": {Directions.LEFT, Directions.RIGHT},
    "L": {Directions.UP, Directions.RIGHT},
    "J": {Directions.UP, Directions.LEFT},
    "7": {Directions.DOWN, Directions.LEFT},
    "F": {Directions.DOWN, Directions.RIGHT},
}


def parse_lines(lines: list[str]) -> tuple[Position, Grid]:
    grid = {}
    starting_position = None

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                pipe = Pipe(Position(x, y), None)
            elif char == "S":
                pipe = Pipe(Position(x, y), None)
                starting_position = Position(x, y)
            elif char in SYMBOL_TO_DIRECTION:
                pipe = Pipe(Position(x, y), tuple(SYMBOL_TO_DIRECTION[char]))
            else:
                raise ValueError(f"Unknown symbol {char}")
            grid[Position(x, y)] = pipe

    if starting_position is None:
        raise ValueError("No starting position found")

    return starting_position, grid


def valid_neighbours(position: Position, grid: Grid) -> list[Position]:
    return [
        position + direction.value
        for direction in Directions
        if position + direction.value in grid
    ]


def label_starting_position(starting_position: Position, grid: Grid) -> None:
    pipe_directions = set()
    for direction in Directions:
        neighbour_position = starting_position + direction.value
        if neighbour_position not in grid:
            continue
        neighbour_pipe = grid[neighbour_position]
        if neighbour_pipe.directions is None:
            continue
        opposite_direction = Directions(-direction.value)
        if opposite_direction in neighbour_pipe.directions:
            pipe_directions.add(direction)

    assert len(pipe_directions) == 2
    grid[starting_position].directions = tuple(pipe_directions)


def solve(lines: list[str]) -> int:
    starting_position, grid = parse_lines(lines)
    print(f"{starting_position = }")

    label_starting_position(starting_position, grid)
    starting_directions = grid[starting_position].directions
    current_position_1 = starting_position + starting_directions[0].value
    current_position_2 = starting_position + starting_directions[1].value

    previous_position_1 = starting_position
    previous_position_2 = starting_position
    print(f"{current_position_1 = }")
    print(f"{current_position_2 = }")
    solution = 1

    while current_position_1 != current_position_2:
        pipe1 = grid[current_position_1]
        next_position_1 = pipe1.next_position(previous_position_1)
        previous_position_1 = current_position_1
        current_position_1 = next_position_1
        print(f"{current_position_1 = }")

        pipe2 = grid[current_position_2]
        next_position_2 = pipe2.next_position(previous_position_2)
        previous_position_2 = current_position_2
        current_position_2 = next_position_2
        print(f"{current_position_2 = }")

        solution += 1

    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
