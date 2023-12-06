from typing import Callable

from part1 import read_input, parse_lines


def beats_record(charging_time: int,
                 race_time: int,
                 race_record: int) -> bool:
    distance = (race_time - charging_time) * charging_time
    return distance > race_record


def solve(lines: list[str]) -> int:
    race_times, race_records = parse_lines(lines)
    race_time = int("".join(str(n) for n in race_times))
    race_record = int("".join(str(n) for n in race_records))

    best_charging_time = race_time // 2
    if not beats_record(best_charging_time, race_time, race_record):
        return 0

    lowest_charging_with_record = find_lowest_above(
        lower=0,
        upper=best_charging_time,
        is_above=lambda t: beats_record(t, race_time, race_record)
    )
    highest_charging_with_record = race_time - lowest_charging_with_record
    return highest_charging_with_record - (lowest_charging_with_record - 1)


def find_lowest_above(lower: int,
                      upper: int,
                      is_above: Callable[[int], bool],
                      ) -> int:
    if upper == lower + 1:
        return upper

    middle = (upper + lower) // 2
    if is_above(middle):
        return find_lowest_above(lower, middle, is_above)
    else:
        return find_lowest_above(middle, upper, is_above)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
