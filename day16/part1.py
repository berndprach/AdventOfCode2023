from enum import Enum


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Direction(Enum):
    North = Position(0, -1)
    East = Position(1, 0)
    South = Position(0, 1)
    West = Position(-1, 0)


def get_new_directions(current_direction: Direction,
                       symbol: str,
                       ) -> list[Direction]:
    if symbol == ".":
        return [current_direction]

    if symbol == "/":
        new_direction_dict = {
            Direction.North: Direction.East,
            Direction.East: Direction.North,
            Direction.South: Direction.West,
            Direction.West: Direction.South,
        }
        new_direction = new_direction_dict[current_direction]
        return [new_direction]

    if symbol == "\\":  # \
        new_direction_dict = {
            Direction.North: Direction.West,
            Direction.East: Direction.South,
            Direction.South: Direction.East,
            Direction.West: Direction.North,
        }
        new_direction = new_direction_dict[current_direction]
        return [new_direction]

    if symbol == "|":
        if current_direction in (Direction.East, Direction.West):
            return [Direction.North, Direction.South]
        else:
            return [current_direction]

    if symbol == "-":
        if current_direction in (Direction.North, Direction.South):
            return [Direction.East, Direction.West]
        else:
            return [current_direction]


def find_number_of_enegized_positions(grid: dict[Position, str],
                                      starting_position: Position,
                                      starting_direction: Direction,
                                      ) -> int:
    is_energized = {position: False for position in grid}

    active_light_beams = [(starting_position, starting_direction)]
    previous_light_beams = set()

    while len(active_light_beams) > 0:
        position, direction = active_light_beams.pop()

        if (position, direction) in previous_light_beams:
            continue
        previous_light_beams.add((position, direction))

        is_energized[position] = True
        new_directions = get_new_directions(direction, grid[position])
        for new_direction in new_directions:
            new_position = position + new_direction.value
            if new_position in grid:
                active_light_beams.append((new_position, new_direction))

    return sum(is_energized.values())


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_input(lines: list[str]) -> dict[Position, str]:
    grid = {}
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            grid[Position(x, y)] = symbol
    return grid


def solve(lines: list[str]) -> int:
    grid = parse_input(lines)
    initial_position = Position(0, 0)
    initial_direction = Direction.East
    return find_number_of_enegized_positions(grid, initial_position, initial_direction)


def main():
    lines = read_input()

    if len(lines) == 0:
        raise ValueError("Input is empty")

    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
