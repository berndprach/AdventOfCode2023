
DIGIT_SPELLINGS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def first_digit(string) -> int:
    for position, symbol in enumerate(string):
        if symbol.isdigit():
            return int(symbol)

        remaining_string = string[position:]
        for digit, spelling in DIGIT_SPELLINGS.items():
            if remaining_string.startswith(spelling):
                return digit


def last_digit(string) -> int:
    for position_from_end, symbol in enumerate(reversed(string)):
        if symbol.isdigit():
            return int(symbol)

        remaining_string = string[:len(string)-position_from_end]
        for digit, spelling in DIGIT_SPELLINGS.items():
            if remaining_string.endswith(spelling):
                return digit


def solve(lines: list[str]) -> int:
    sum_of_calibrations = 0
    for line in lines:
        calibration_value = 10 * first_digit(line) + last_digit(line)
        sum_of_calibrations += calibration_value
    return sum_of_calibrations


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    solution = solve(lines)

    print(f"{solution = }")


if __name__ == "__main__":
    main()
