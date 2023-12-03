
from part1 import (
    read_input,
    find_numbers_in_lines,
    lines_to_grid,
    get_neighbours,
)


def solve(lines: list[str]) -> int:
    numbers = find_numbers_in_lines(lines)
    grid = lines_to_grid(lines)

    position_to_number_id = {
        position: number_id
        for number_id, number in enumerate(numbers)
        for position in number.positions
    }

    solution = 0
    for position in grid.keys():
        if grid[position] != "*":
            continue

        neighbour_number_ids = set()
        for neighbor in get_neighbours(position, grid):
            if neighbor in position_to_number_id.keys():
                neighbour_number_ids.add(position_to_number_id[neighbor])

        if len(neighbour_number_ids) == 2:
            print(f"{position = }")
            nn1_id, nn2_id = neighbour_number_ids
            value1 = numbers[nn1_id].value
            value2 = numbers[nn2_id].value
            solution += value1 * value2

    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
