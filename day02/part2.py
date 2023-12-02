
from part1 import Color, parse_line, read_input


def solve(lines: list[str]) -> int:
    solution = 0
    for line in lines:
        game_id, samples = parse_line(line)
        max_seen = {color: 0 for color in Color}
        for sample in samples:
            for color in Color:
                max_seen[color] = max(max_seen[color], sample[color])

        game_power = max_seen[Color.RED] * max_seen[Color.GREEN] * max_seen[Color.BLUE]
        solution += game_power
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
