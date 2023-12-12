import functools

from part1 import read_input, parse_line, State, can_place

REPETITIONS = 5


@functools.cache
def get_number_of_solutions(states: tuple[State], counts: tuple[int]) -> int:
    if len(counts) == 0:
        if any(s == State.DAMAGED for s in states):
            return 0
        else:
            return 1

    number_of_solutions = 0
    # Consider first position as damaged:
    first_count = counts[0]
    if can_place(first_count, index=0, states=list(states)):
        new_states, new_counts = states[first_count + 1:], counts[1:]
        number_of_solutions += get_number_of_solutions(new_states, new_counts)

    # Consider first position as operational:
    if len(states) != 0 and states[0] in {State.OPERATIONAL, State.UNKNOWN}:
        new_states = states[1:]
        number_of_solutions += get_number_of_solutions(new_states, counts)

    return number_of_solutions


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        states_small, counts_small = parse_line(line)
        states = (states_small + [State.UNKNOWN]) * (REPETITIONS - 1)
        states.extend(states_small)
        counts = counts_small * REPETITIONS
        solution += get_number_of_solutions(tuple(states), tuple(counts))
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
