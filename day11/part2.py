
from part1 import read_input, parse_lines, get_counts, distance, Position, \
    get_paiwise_distances

EXPANSION_FACTOR = 1_000_000


def get_galaxy_positions(occupied_positions: set[Position],
                         expansion_factor: int,
                         ) -> set[Position]:
    x_coordinates = set(x for x, _ in occupied_positions)
    max_x = max(x_coordinates)
    empty_columns = [x for x in range(max_x + 1) if x not in x_coordinates]
    empty_columns_before: list[int] = get_counts(empty_columns, max_x + 1)

    y_coordinates = set(y for _, y in occupied_positions)
    max_y = max(y_coordinates)
    empty_rows = [i for i in range(max_y + 1) if i not in y_coordinates]
    empty_rows_before: list[int] = get_counts(empty_rows, max_y + 1)

    galaxy_positions = set()
    for x, y in occupied_positions:
        galaxy_x = x + (expansion_factor - 1) * empty_columns_before[x]
        galaxy_y = y + (expansion_factor - 1) * empty_rows_before[y]
        galaxy_positions.add((galaxy_x, galaxy_y))
    return galaxy_positions


def solve(lines: list[str]) -> int:
    occupied_positions = parse_lines(lines)
    galaxy_positions = get_galaxy_positions(
        occupied_positions, EXPANSION_FACTOR
    )
    pairwise_distances = get_paiwise_distances(galaxy_positions)
    return sum(pairwise_distances) // 2


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
