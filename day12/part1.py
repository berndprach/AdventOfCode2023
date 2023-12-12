from enum import Enu


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
    states = [State(c) for c in part1]
    counts = [int(c) for c in part2.split(",")]
    return states, counts


def get_number_of_solutions(states: list[State], counts: list[int]) -> int:
    if len(counts) == 0:
        if any(s == State.DAMAGED for s in states):
            return 0
        else:
            return 1

    number_of_solutions = 0
    # Consider first position as damaged:
    first_count = counts[0]
    if can_place(first_count, index=0, states=states):
        new_states, new_counts = states[first_count + 1:], counts[1:]
        number_of_solutions += get_number_of_solutions(new_states, new_counts)

    # Consider first position as operational:
    if len(states) != 0 and states[0] in {State.OPERATIONAL, State.UNKNOWN}:
        new_states = states[1:]
        number_of_solutions += get_number_of_solutions(new_states, counts)

    return number_of_solutions


def can_place(count: int, index: int, states: list[State]) -> bool:
    if index + count > len(states):
        return False

    for i in range(index, index + count):
        if states[i] == State.OPERATIONAL:
            return False

    if index + count < len(states) and states[index + count] == State.DAMAGED:
        return False

    return True


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        states, counts = parse_line(line)
        solution += get_number_of_solutions(states, counts)
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
