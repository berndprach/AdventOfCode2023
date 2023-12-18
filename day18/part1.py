from time import time


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Position = tuple[int, int]


def parse_input(lines: list[str]) -> list[tuple[str, int]]:
    # R 6 (#70c710)
    instructions = []
    for line in lines:
        direction, distance_str, _ = line.split()
        instructions.append(
            (direction, int(distance_str))
        )
    return instructions


DIRECTION: dict[str, Position] = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def get_new_position(current_position: Position,
                     direction: str,
                     distance: int = 1,
                     ) -> Position:
    x, y = current_position
    dx, dy = DIRECTION[direction]
    return x + dx * distance, y + dy * distance


def find_path_positions(instructions) -> set[Position]:
    path_positions = set()
    current_position = (0, 0)
    for instruction in instructions:
        direction, distance = instruction
        for _ in range(distance):
            current_position = get_new_position(current_position, direction)
            path_positions.add(current_position)

    assert current_position == (0, 0)
    return path_positions


def count_positions_within_path(path_positions: set[Position]) -> int:
    min_x = min(x for x, _ in path_positions) - 1
    max_x = max(x for x, _ in path_positions) + 1
    min_y = min(y for _, y in path_positions) - 1
    max_y = max(y for _, y in path_positions) + 1

    outside_positions = set()
    queue = [(min_x, min_y)]
    while len(queue) > 0:
        x, y = queue.pop()
        if (x, y) in path_positions:
            continue

        if (x, y) in outside_positions:
            continue

        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue

        outside_positions.add((x, y))
        for dx, dy in DIRECTION.values():
            queue.append((x + dx, y + dy))

    total_size = (max_x - min_x + 1) * (max_y - min_y + 1)
    count_within = total_size - len(outside_positions)
    return count_within


def solve(lines: list[str]) -> int:
    instructions = parse_input(lines)
    path_positions = find_path_positions(instructions)
    return count_positions_within_path(path_positions)


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
