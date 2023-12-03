
def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position({self.x}, {self.y})"


Grid = dict[Position, str]


def lines_to_grid(lines: list[str]) -> Grid:
    grid: Grid = {}

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            grid[Position(x, y)] = character

    return grid


"""
. . .
. x .
. . .
"""
NEIGHBOUR_DIRECTIONS: list[Position] = [
    Position(dx, dy)
    for dx in [-1, 0, 1]
    for dy in [-1, 0, 1]
    if not (dx == 0 and dy == 0)
]


def get_neighbours(position: Position, grid: Grid) -> set[Position]:
    return {
        position + direction
        for direction in NEIGHBOUR_DIRECTIONS
        if position + direction in grid.keys()
    }


def get_neighbours_of_set(positions: set[Position],
                          grid: Grid,
                          ) -> set[Position]:
    neighbours = set()
    for position in positions:
        local_neighbours = get_neighbours(position, grid)
        neighbours.update(local_neighbours)
    return neighbours - positions


class NumberWithPosition:
    def __init__(self, value: int, positions: set[Position]):
        self.value = value
        self.positions = positions


def find_numbers_in_lines(lines: list[str]) -> list[NumberWithPosition]:
    numbers: list[NumberWithPosition] = []

    for y, line in enumerate(lines):
        numbers.extend(find_numbers_in_line(line, line_number=y))

    return numbers


def find_numbers_in_line(line: str, line_number: int):
    # "467..114.."
    numbers: list[NumberWithPosition] = []

    x = 0
    while x < len(line):
        if not line[x].isdigit():
            x += 1
            continue

        length = find_length_of_number(line, starting_position=x)
        value = int(line[x:x + length])
        positions = {Position(x + i, line_number) for i in range(length)}
        new_number = NumberWithPosition(value, positions)
        numbers.append(new_number)

        x += length

    return numbers


def find_length_of_number(line, starting_position):
    length = 1
    while starting_position + length < len(line):
        next_character = line[starting_position + length]
        if next_character.isdigit():
            length += 1
        else:
            break

    return length


def solve(lines: list[str]) -> int:
    numbers = find_numbers_in_lines(lines)
    grid = lines_to_grid(lines)

    solution = 0
    for number in numbers:
        if has_adjacent_symbol(grid, number):
            solution += number.value

    return solution


def has_adjacent_symbol(grid: Grid, number: NumberWithPosition) -> bool:
    neighbours = get_neighbours_of_set(number.positions, grid)
    for neighbour in neighbours:
        if is_symbol(grid[neighbour]):
            return True

    return False


def is_symbol(character: str) -> bool:
    if character.isdigit() or character == ".":
        return False

    return True


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
