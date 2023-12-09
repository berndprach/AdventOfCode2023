
def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_line(line: str) -> list[int]:
    # "0 3 6 9 12 15"
    return [int(v) for v in line.split(" ")]


def predict_next_number(numbers: list[int]) -> int:
    if all(n == 0 for n in numbers):
        return 0

    differences = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
    new_difference = predict_next_number(differences)
    return numbers[-1] + new_difference


def solve(lines: list[str]) -> int:
    solutions = 0
    for line in lines:
        numbers = parse_line(line)
        solutions += predict_next_number(numbers)
    return solutions


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
