
def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Position = tuple[int, int]


def parse_lines(lines: list[str]) -> set[Position]:
    occupied_positions = set()
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == "#":
                occupied_positions.add((x, y))
    return occupied_positions


def get_galaxy_positions(occupied_positions: set[Position]) -> set[Position]:
    x_coordinates = set(x for x, _ in occupied_positions)
    max_x = max(x_coordinates)
    empty_columns = [x for x in range(max_x+1) if x not in x_coordinates]
    empty_columns_before: list[int] = get_counts(empty_columns, max_x+1)

    y_coordinates = set(y for _, y in occupied_positions)
    max_y = max(y_coordinates)
    empty_rows = [i for i in range(max_y+1) if i not in y_coordinates]
    empty_rows_before: list[int] = get_counts(empty_rows, max_y+1)

    galaxy_positions = set()
    for x, y in occupied_positions:
        galaxy_x = x + empty_columns_before[x]
        galaxy_y = y + empty_rows_before[y]
        galaxy_positions.add((galaxy_x, galaxy_y))
    return galaxy_positions


def get_counts(indices: list[int], length: int) -> list[int]:
    indices = set(indices)
    counts = []
    current_count = 0
    for i in range(length):
        if i in indices:
            current_count += 1
        counts.append(current_count)
    return counts


def solve(lines: list[str]) -> int:
    occupied_positions = parse_lines(lines)
    galaxy_positions = get_galaxy_positions(occupied_positions)
    pairwise_distances = get_paiwise_distances(galaxy_positions)
    return sum(pairwise_distances) // 2


def get_paiwise_distances(positions: set[Position]) -> list[int]:
    distances = []
    for position_1 in positions:
        for position_2 in positions:
            distances.append(distance(position_1, position_2))
    return distances


def distance(position_1: Position, position_2: Position) -> int:
    x1, y1 = position_1
    x2, y2 = position_2
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
