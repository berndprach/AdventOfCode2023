

def first_digit(string):
    for symbol in string:
        if symbol.isdigit():
            return int(symbol)


def last_digit(string):
    for symbol in reversed(string):
        if symbol.isdigit():
            return int(symbol)


def solve(lines):
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
