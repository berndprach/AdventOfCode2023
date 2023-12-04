
def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_line(line: str) -> tuple[list[int], list[int]]:
    # "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    card_name, numbers = line.split(": ")
    winning_number_str, my_number_str = numbers.split(" | ")
    winning_numbers = [int(n) for n in winning_number_str.split()]
    my_numbers = [int(n) for n in my_number_str.split()]
    return winning_numbers, my_numbers


def score(winning_numbers: list[int], my_numbers: list[int]) -> int:
    intersection = set(winning_numbers).intersection(set(my_numbers))
    if len(intersection) == 0:
        return 0
    else:
        return 2 ** (len(intersection) - 1)


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        winning_numbers, my_numbers = parse_line(line)
        card_score = score(winning_numbers, my_numbers)
        solution += card_score
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
