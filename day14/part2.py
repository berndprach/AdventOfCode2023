from part1 import read_input, Platform, tilt_north, get_total_load, parse_lines

NUMBER_OF_CYCLES = 1_000_000_000


def rotate_clockwise(platform: Platform) -> Platform:
    # (0, 0) -> (max_y, 0),
    # (0, 1) -> (max_y-1, 0),
    # (1, 0) -> (max_y, 1),
    # (1, 1) -> (max_y-1, 1),
    max_y = max(y for x, y in platform)
    rotated_platform = {
        (max_y-y, x): platform[(x, y)]
        for x, y in platform
    }
    return rotated_platform


def apply_cycle(platform: Platform) -> Platform:
    for _ in range(4):
        platform = tilt_north(platform)
        platform = rotate_clockwise(platform)
    return platform


def solve(lines: list[str]) -> int:
    platform = parse_lines(lines)
    previous_appearances: dict[platform, int] = {}

    iteration = 0
    while iteration < NUMBER_OF_CYCLES:
        platform = apply_cycle(platform)
        platform_key = frozenset(platform.items())

        if platform_key in previous_appearances:
            previous_iteration = previous_appearances[platform_key]
            iteration_difference = iteration - previous_iteration
            print(f"Platforms are equal after iterations {previous_iteration} "
                  f"and {iteration} (difference: {iteration_difference})")

            iterations_left = NUMBER_OF_CYCLES - iteration
            new_iteration_left = iterations_left % iteration_difference
            iteration = NUMBER_OF_CYCLES - new_iteration_left
            print(f"Set iteration to {iteration:,}.\n")
            previous_appearances = {}

        previous_appearances[platform_key] = iteration

        iteration += 1

    return get_total_load(platform)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
