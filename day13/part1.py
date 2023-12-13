from typing import Optional


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Position = tuple[int, int]
Pattern = dict[Position, bool]


def parse_lines(lines: list[str]) -> list[Pattern]:
    all_patterns = []
    current_pattern = {}
    current_y = 1

    for line in lines:
        if line == "":
            all_patterns.append(current_pattern)
            current_pattern = {}
            current_y = 1
            continue

        for x, character in enumerate(line):
            is_rock = character == "#"
            current_pattern[(x+1, current_y)] = is_rock

        current_y += 1

    all_patterns.append(current_pattern)
    return all_patterns


def find_horizontal_reflection(pattern: Pattern) -> Optional[int]:
    max_y = max(y for x, y in pattern)
    for reflection_y in range(1, max_y):
        if is_horizontal_reflection(reflection_y, pattern):
            return reflection_y

    return None


def is_horizontal_reflection(reflection_y, pattern: Pattern) -> bool:
    for x, y in pattern:
        other_y = 2 * reflection_y - y + 1
        if (x, other_y) not in pattern:
            continue
        if pattern[(x, y)] != pattern[(x, other_y)]:
            return False
    return True


def find_vertical_reflection(pattern: Pattern) -> Optional[int]:
    transposed_pattern = {(y, x): is_rock
                          for (x, y), is_rock in pattern.items()}
    return find_horizontal_reflection(transposed_pattern)


def solve(lines: list[str]) -> int:
    patterns = parse_lines(lines)
    solution = 0
    for pattern in patterns:
        horizonal_reflection = find_horizontal_reflection(pattern)
        if horizonal_reflection is not None:
            solution += 100*horizonal_reflection
        else:
            vertical_reflection = find_vertical_reflection(pattern)
            solution += vertical_reflection

    return solution


def main():
    lines = read_input()
    if len(lines) == 0:
        raise ValueError("Forgot to add input!")
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
