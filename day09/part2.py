
from part1 import read_input, parse_line, predict_next_number


def solve(lines: list[str]) -> int:
    solutions = 0
    for line in lines:
        numbers = parse_line(line)
        reverse_numbers = numbers[::-1]
        previous_number = predict_next_number(reverse_numbers)
        solutions += previous_number
    return solutions


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
