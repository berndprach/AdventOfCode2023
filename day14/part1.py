from enum import Enum


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


class Entity(Enum):
    EMPTY = "."
    ROUND_ROCK = "O"
    SQUARE_ROCK = "#"


Position = tuple[int, int]
Platform = dict[Position, Entity]


def parse_lines(lines: list[str]) -> Platform:
    platform = {}
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            object_at_position = Entity(character)
            platform[(x, y)] = object_at_position
    return platform


def tilt_north(platform: Platform) -> Platform:
    max_x = max(x for x, y in platform)
    for x in range(max_x + 1):
        tilt_column_north(x, platform)
    return platform


def tilt_column_north(x: int, platform: Platform) -> None:
    max_y = max(y for x, y in platform)
    next_empty_y = 0
    for current_y in range(max_y + 1):
        object_at_position = platform[(x, current_y)]

        if object_at_position == Entity.SQUARE_ROCK:
            next_empty_y = current_y + 1
            continue

        if object_at_position == Entity.ROUND_ROCK:
            platform[(x, current_y)] = Entity.EMPTY  # First remove
            platform[(x, next_empty_y)] = object_at_position  # Then place
            next_empty_y += 1
            continue


def get_total_load(platform: Platform) -> int:
    total_load = 0
    max_y = max(y for x, y in platform)
    for position, object_at_position in platform.items():
        if object_at_position == Entity.ROUND_ROCK:
            rock_load = max_y - position[1] + 1
            total_load += rock_load
    return total_load


def solve(lines: list[str]) -> int:
    platform = parse_lines(lines)
    tilt_north(platform)
    return get_total_load(platform)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
