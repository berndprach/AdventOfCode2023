
def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def find_hash(string: str) -> int:
    current_value = 0
    for character in string:
        ascii_value = ord(character)
        current_value += ascii_value
        current_value *= 17
        current_value %= 256
    return current_value


def solve(lines: list[str]) -> int:
    line = lines[0]
    parts = line.split(",")
    solution = sum(find_hash(part) for part in parts)
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
