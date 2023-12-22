from time import time

from part1 import read_input, parse_lines, drop_bricks, Brick


def count_falling_bricks(removed_brick: Brick, rests_on: dict) -> int:
    gone_bricks = {removed_brick}
    for brick in sorted(rests_on.keys(), key=lambda b: b.z):
        if brick.z == 1:
            continue

        if rests_on[brick].issubset(gone_bricks):
            gone_bricks.add(brick)

    return len(gone_bricks) - 1


def solve(lines: list[str]) -> int:
    bricks = parse_lines(lines)
    rests_on = drop_bricks(bricks)

    solution = 0
    for brick in bricks:
        solution += count_falling_bricks(brick, rests_on)
    return solution


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
