from time import time

from part1 import (
    read_input,
    get_new_position,
    Position,
    count_positions_within_path,
)


DIRECTION = {
    0: "R",
    1: "D",
    2: "L",
    3: "U",
}


def parse_input(lines: list[str]) -> list[tuple[str, int]]:
    # R 6 (#70c710)
    instructions = []
    for line in lines:
        _, _, instruction_str = line.split()
        distance = int(instruction_str[2:-2], base=16)
        direction = DIRECTION[int(instruction_str[-2])]
        instructions.append((direction, distance))
    return instructions


def get_corners(instructions: list[tuple[str, int]]) -> list[tuple[int, int]]:
    current_position = (0, 0)
    corners = [current_position]
    for instruction in instructions:
        direction, distance = instruction
        next_position = get_new_position(
            current_position, direction, distance
        )
        corners.append(next_position)
        current_position = next_position
    return corners


def count_in_line(line_y: int, corners: list[Position]) -> int:
    # ..........+--+..
    # ..+---+...|##|..
    # ..|###|...|##|..
    # ..|###+---+##|..
    if line_y in {y for _, y in corners}:
        raise NotImplementedError("Line intersects a corner")

    intersection_xs = []
    for i in range(len(corners) - 1):
        x1, y1 = corners[i]
        x2, y2 = corners[i+1]
        if x1 == x2 and min(y1, y2) <= line_y <= max(y1, y2):
            intersection_xs.append(x1)

    intersection_xs = sorted(intersection_xs)
    count = 0
    for i in range(len(intersection_xs)//2):
        start_x = intersection_xs[2*i]
        end_x = intersection_xs[2*i + 1]
        count += end_x - start_x + 1
    return count


def remove_easy_lines(corners: list[Position]) -> tuple[list[Position], int]:
    ys = {y for _, y in corners}
    sorted_ys = sorted(ys)
    count = 0
    old_y_to_new_y = {sorted_ys[0]: 0}

    for i in range(len(sorted_ys) - 1):
        y, next_y = sorted_ys[i], sorted_ys[i+1]
        if next_y - y == 1:
            old_y_to_new_y[next_y] = old_y_to_new_y[y] + 1
            continue

        count_in_single_line = count_in_line(y+1, corners)
        number_of_lines = next_y - 1 - y
        count += count_in_single_line * (number_of_lines-1)
        old_y_to_new_y[next_y] = old_y_to_new_y[y] + 2

    new_corners = []
    for x, y in corners:
        new_corners.append((x, old_y_to_new_y[y]))

    return new_corners, count


def solve(lines: list[str]) -> int:
    instructions = parse_input(lines)
    corners = get_corners(instructions)
    corners, count1 = remove_easy_lines(corners)
    corners = [(y, x) for x, y in corners]
    corners, count2 = remove_easy_lines(corners)

    path_positions = to_path_positions(corners)
    count3 = count_positions_within_path(path_positions)

    return count1 + count2 + count3


def to_path_positions(corners: list[Position]) -> set[Position]:
    path_positions = set()
    for i in range(len(corners) - 1):
        x1, y1 = corners[i]
        x2, y2 = corners[i+1]
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                path_positions.add((x1, y))
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                path_positions.add((x, y1))
    return path_positions


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
