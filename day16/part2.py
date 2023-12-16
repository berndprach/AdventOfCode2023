
from part1 import read_input, find_number_of_enegized, parse_input, Position, \
    Direction


def solve(lines: list[str]) -> int:
    grid = parse_input(lines)

    max_x = max(position.x for position in grid.keys())
    max_y = max(position.y for position in grid.keys())

    starting_configurations = []
    for x in range(max_x + 1):
        starting_configurations.append((Position(x, 0), Direction.South))
        starting_configurations.append((Position(x, max_y), Direction.North))
    for y in range(max_y + 1):
        starting_configurations.append((Position(0, y), Direction.East))
        starting_configurations.append((Position(max_x, y), Direction.West))

    max_enegized = 0
    for starting_position, starting_direction in starting_configurations:
        enegized = find_number_of_enegized(
            grid,  starting_position, starting_direction
        )
        max_enegized = max(max_enegized, enegized)
    return max_enegized


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
