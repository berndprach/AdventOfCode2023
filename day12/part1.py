from enum import Enum, auto


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


class State(Enum):
    DAMAGED = "#"
    OPERATIONAL = "."
    UNKNOWN = "?"


def parse_line(line: str) -> tuple[list[State], list[int]]:
    # "???.### 1,1,3"
    part1, part2 = line.split(" ")
    decoded = {s.value: s for s in State}
    states = [decoded[c] for c in part1]
    counts = [int(c) for c in part2.split(",")]
    return states, counts


def get_number_of_solutions(states: list[State], counts: list[int]) -> int:
    if len(counts) == 0:
        if any(s == State.DAMAGED for s in states):
            return 0
        else:
            return 1

    number_of_solutions = 0
    first_count = counts[0]
    for first_start in range(len(is_damaged) - first_count + 1):
        if not is_valid(first_start, first_count, is_damaged):
            if is_damaged[first_start] == State.DAMAGED:
                break
            continue

        new_is_damaged_start = first_start + first_count + 1
        new_is_damaged = is_damaged[new_is_damaged_start:]
        number_of_solutions += get_number_of_solutions(new_is_damaged,
                                                       counts[1:])
        if is_damaged[first_start] == State.DAMAGED:
            break

    return number_of_solutions


def is_valid(start: int, count: int, line: list[State]) -> bool:
    # Check if exactly count damaged ones in [start, start + count) is valid:
    for i in range(start, start + count):
        if line[i] == State.OPERATIONAL:
            return False

    if start+count < len(line) and line[start + count] == State.DAMAGED:
        return False

    return True


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        # print(f"Evaluating {line = }.")
        is_damaged, counts = parse_line(line)
        solution += get_number_of_solutions(is_damaged, counts)
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
