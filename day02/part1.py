from enum import Enum


class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"


Sample = dict[Color, int]


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_line(line: str) -> tuple[int, list[Sample]]:
    # "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    game_name, all_samples_str = line.split(": ")
    game_id = int(game_name.replace("Game ", ""))
    sample_strs = all_samples_str.split("; ")
    samples = [parse_sample_string(sample_str) for sample_str in sample_strs]
    return game_id, samples


def parse_sample_string(sample_str: str) -> dict[Color, int]:
    # "3 blue, 4 red"
    color_strings = sample_str.split(", ")
    color_dict = {}
    for color_str in color_strings:
        amount_str, color_str = color_str.split(" ")
        color_dict[color_str] = int(amount_str)

    return {
        color: color_dict.get(color.value, 0)
        for color in Color
    }


def sample_is_possible(sample: Sample):
    if sample[Color.RED] > 12:
        return False
    if sample[Color.GREEN] > 13:
        return False
    if sample[Color.BLUE] > 14:
        return False

    return True


def samples_are_possible(samples: list[Sample]):
    for sample in samples:
        if not sample_is_possible(sample):
            return False
    return True


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        game_id, samples = parse_line(line)
        if samples_are_possible(samples):
            solution += game_id

    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
