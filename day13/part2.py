from typing import Optional

from part1 import read_input, Pattern, parse_lines


def find_smugded_horizontal_reflection(pattern: Pattern) -> Optional[int]:
    max_y = max(y for x, y in pattern)
    for reflection_y in range(1, max_y):
        if is_smugded_horizontal_reflection(reflection_y, pattern):
            return reflection_y

    return None


def is_smugded_horizontal_reflection(reflection_y, pattern: Pattern) -> bool:
    nrof_differences = 0
    for x, y in pattern:
        other_y = 2 * reflection_y - y + 1
        if (x, other_y) not in pattern:
            continue
        if pattern[(x, y)] != pattern[(x, other_y)]:
            nrof_differences += 1

        if nrof_differences > 2:
            return False

    return nrof_differences == 2


def find_smudged_vertical_reflection(pattern: Pattern) -> Optional[int]:
    transposed_pattern = {(y, x): is_rock
                          for (x, y), is_rock in pattern.items()}
    return find_smugded_horizontal_reflection(transposed_pattern)


def solve(lines: list[str]) -> int:
    patterns = parse_lines(lines)
    solution = 0
    for pattern in patterns:
        horizonal_reflection = find_smugded_horizontal_reflection(pattern)
        if horizonal_reflection is not None:
            solution += 100*horizonal_reflection
        else:
            vertical_reflection = find_smudged_vertical_reflection(pattern)
            if vertical_reflection is None:
                raise ValueError("No reflection found")
            solution += vertical_reflection

    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
