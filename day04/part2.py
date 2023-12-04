
from part1 import read_input, parse_line


def solve(lines: list[str]) -> int:
    nrof_copies = [1 for _ in lines]
    for current_index, line in enumerate(lines):
        numbers = parse_line(line)
        score = number_of_intersections(*numbers)
        for i in range(score):
            new_index = current_index + 1 + i
            nrof_copies[new_index] += nrof_copies[current_index]

    return sum(nrof_copies)


def number_of_intersections(winning_numbers: list[int],
                            card_numbers: list[int],
                            ) -> int:
    intersection = set(winning_numbers).intersection(set(card_numbers))
    return len(intersection)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
