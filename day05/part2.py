
from part1 import (
    read_input,
    parse_lines,
    CategoryMap,
)

ValueRange = tuple[int, int]  # start, end+1


def apply_category_map_to_range(category_map: CategoryMap,
                                value_range: ValueRange,
                                ) -> list[ValueRange]:
    # Split:
    # ..........s=================t..........
    # ................s====t.................
    all_starts = [from_idx
                  for _, from_idx, _ in category_map.map_tuples]
    all_ends = [from_idx + length
                for _, from_idx, length in category_map.map_tuples]
    all_s_and_t = sorted(set(all_starts + all_ends))

    split_ranges = []
    next_start = value_range[0]
    for v in all_s_and_t:
        if v <= value_range[0] or v >= value_range[1]:
            continue

        split_ranges.append((next_start, v))
        next_start = v
    split_ranges.append((next_start, value_range[1]))

    new_ranges = []
    for s, t in split_ranges:
        new_start = category_map.apply(s)
        new_end = new_start + (t - s)
        new_ranges.append((new_start, new_end))

    return new_ranges


def solve(lines: list[str]) -> int:
    seed_data, category_maps = parse_lines(lines)

    seed_intervals = []
    for i in range(len(seed_data) // 2):
        s = seed_data[2 * i]
        length = seed_data[2 * i + 1]
        seed_intervals.append((s, s+length))

    location_intervals = get_location_from_seed_intervals(
        seed_intervals,
        category_maps
    )
    closest_location = min([i[0] for i in location_intervals])
    return closest_location


def get_location_from_seed_intervals(seed_intervals: list[ValueRange],
                                     category_maps: dict[str, CategoryMap],
                                     ) -> list[ValueRange]:
    category = "seed"
    intervals = seed_intervals
    while category != "location":
        category_map = category_maps[category]
        all_new_intervals = []
        for interval in intervals:
            new_intervals = apply_category_map_to_range(category_map, interval)
            all_new_intervals.extend(new_intervals)

        intervals = all_new_intervals
        category = category_map.next_category

    return intervals


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
