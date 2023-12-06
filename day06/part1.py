import re


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_lines(lines: list[str]) -> tuple[list[int], list[int]]:
    race_times = [int(n) for n in re.findall(r"\d+", lines[0])]
    race_records = [int(n) for n in re.findall(r"\d+", lines[1])]
    return race_times, race_records


def solve(lines: list[str]) -> int:
    race_times, race_records = parse_lines(lines)

    solution = 1
    for race_time, race_record in zip(race_times, race_records):
        solution *= get_number_of_possibilities(race_time, race_record)
    return solution


def get_number_of_possibilities(race_time: int, race_record: int) -> int:
    number_of_possible_positions = 0
    for charging_time in range(1, race_record):
        moving_time = race_time - charging_time
        distance = moving_time * charging_time
        if distance > race_record:
            number_of_possible_positions += 1
    return number_of_possible_positions


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
