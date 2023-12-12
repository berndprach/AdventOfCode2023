import functools

from part1 import read_input, parse_line, State, get_number_of_solutions, \
    is_valid

REPETITIONS = 5


def get_number_of_solutions_cached_OLD(is_damaged: list[State],
                                   counts: list[int]
                                   ) -> int:
    # Map from is_damaged index and count index to number of solutions:
    number_of_solutions: dict[tuple[int, int], int] = {}
    return get_number_of_solutions(
        is_damaged, counts, 0, 0, number_of_solutions
    )


def get_number_of_solutions_OLD(states: list[State],
                            counts: list[int],
                            current_state_index: int,
                            current_count_index: int,
                            number_of_solutions: dict[tuple[int, int], int],
                            ) -> int:
    si, ci = current_state_index, current_count_index
    # print(f"Caching {si = }, {ci = }.")
    if (si, ci) in number_of_solutions:
        return number_of_solutions[(si, ci)]

    if si >= len(states):
        if ci == len(counts):
            number_of_solutions[(si, ci)] = 1
        else:
            number_of_solutions[(si, ci)] = 0
        return number_of_solutions[(si, ci)]

    if ci == len(counts):
        if states[si] == State.DAMAGED:
            number_of_solutions[(si, ci)] = 0
            return number_of_solutions[(si, ci)]

        new_si, new_ci = si + 1, ci
        number_of_solutions[(si, ci)] = get_number_of_solutions(
            states, counts, new_si, new_ci, number_of_solutions
        )
        return number_of_solutions[(si, ci)]

    number = 0
    # Try placing count at di:
    count = counts[ci]
    if can_place_count(count, states, si):
        new_di, new_ci = si + count + 1, ci + 1
        number += get_number_of_solutions(
            states, counts, new_di, new_ci, number_of_solutions
        )

    # Try not placing count at di:
    if states[si] != State.DAMAGED:
        new_di, new_ci = si + 1, ci
        number += get_number_of_solutions(
            states, counts, new_di, new_ci, number_of_solutions
        )

    number_of_solutions[(si, ci)] = number
    return number


@functools.cache
def get_number_of_solutions_cached(is_damaged: tuple[State],
                                   counts: tuple[int],
                                   ) -> int:
    # print(".", end="", flush=True)
    if len(counts) == 0:
        if any(s == State.DAMAGED for s in is_damaged):
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
        number_of_solutions += get_number_of_solutions_cached(
            new_is_damaged, counts[1:]
        )
        if is_damaged[first_start] == State.DAMAGED:
            break

    return number_of_solutions


def can_place_count(count: int, states: list[State], start: int) -> bool:
    if start + count > len(states):
        return False

    for i in range(start, start + count):
        if states[i] == State.OPERATIONAL:
            return False

    if start + count < len(states) and states[start + count] == State.DAMAGED:
        return False

    return True


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        # print(line)
        is_damaged_small, counts_small = parse_line(line)
        is_damaged = (is_damaged_small + [State.UNKNOWN]) * (REPETITIONS - 1)
        is_damaged.extend(is_damaged_small)
        line = "".join(s.value for s in is_damaged)
        counts = counts_small * REPETITIONS
        # print(line, counts)
        # print(f"With {len(is_damaged) = }, {len(counts) = }.")
        # solution += get_number_of_solutions_cached(is_damaged, counts)
        solution += get_number_of_solutions_cached(tuple(is_damaged),
                                                   tuple(counts))
        # print(solution)
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
