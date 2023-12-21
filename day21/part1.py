from time import time


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Position = tuple[int, int]
Grid = dict[Position, bool]


def get_neighbours(position: Position) -> list[Position]:
    x, y = position
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]


def parse_input(lines: list[str]) -> tuple[Grid, Position]:
    is_rock: Grid = {}
    starting_position = None
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            is_rock[(x, y)] = character == "#"  # Also true for start
            if character == "S":
                starting_position = (x, y)

    return is_rock, starting_position


def get_reachable_positions(is_rock: Grid,
                            starting_position: Position,
                            number_of_steps: int,
                            ) -> set[Position]:
    reachable = {starting_position}
    for _ in range(number_of_steps):
        new_reachable = set()
        for position in reachable:
            new_reachable.update(
                get_garder_neighbours(position, is_rock)
            )
        reachable = new_reachable
    return reachable


def get_garder_neighbours(position: Position, is_rock: Grid) -> list[Position]:
    garden_neighbours = []
    for neighbour in get_neighbours(position):
        if neighbour in is_rock.keys() and not is_rock[neighbour]:
            garden_neighbours.append(neighbour)
    return garden_neighbours


def solve(lines: list[str], number_of_steps=64) -> int:
    is_rock, starting_position = parse_input(lines)
    reachable = get_reachable_positions(
        is_rock,
        starting_position,
        number_of_steps
    )
    return len(reachable)


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
