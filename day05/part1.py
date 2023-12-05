from typing import Iterator


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Seeds = list[int]
CategoryToNext = dict[str, str]
CategoryMap = list[tuple[int, int, int]]
CategoryMaps = dict[str, CategoryMap]


class CategoryMap:
    def __init__(self, from_idx: int, to_idx: int, length: int):
        self.from_idx = from_idx
        self.to_idx = to_idx
        self.length = length


def parse_lines(lines: list[str]
                ) -> tuple[Seeds, CategoryToNext, CategoryMaps]:
    """
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48
    ...
    """
    line_iterator = iter(lines)
    seed_line = next(line_iterator)
    seeds = [int(n) for n in seed_line.replace("seeds: ", "").split(" ")]

    category_to_next: CategoryToNext = {}
    category_maps: CategoryMaps = {}

    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if "map:" in line:
            from_category, to_category = parse_map_line(line)
            category_map = parse_category_map_lines(line_iterator)

            category_to_next[from_category] = to_category
            category_maps[from_category] = category_map

    return seeds, category_to_next, category_maps


def parse_map_line(line: str) -> tuple[str, str]:
    # "seed-to-soil map:"
    from_category, to_category = line.replace(" map:", "").split("-to-")
    return from_category, to_category


def parse_category_map_lines(line_iterator: Iterator[str]):
    # "50 98 2"
    category_map: list[tuple[int, int, int]] = []
    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if line == "":
            break

        to_idx, from_idx, length = line.split(" ")
        category_map.append((int(to_idx), int(from_idx), int(length)))
    return category_map


def apply_category_map(category_map: CategoryMap, value: int) -> int:
    for to_idx, from_idx, length in category_map:
        if from_idx <= value < from_idx + length:
            return to_idx + (value - from_idx)
    return value


def solve(lines: list[str]) -> int:
    seeds, category_to_next, category_maps = parse_lines(lines)

    seed_to_soil = {}
    for seed in seeds:
        soil = get_location_from_seed(seed, category_to_next, category_maps)
        seed_to_soil[seed] = soil

    # closest_seed = min(seed_to_soil, key=seed_to_soil.get)
    closest_location = min(seed_to_soil.values())
    return closest_location


def get_location_from_seed(seed_number: int,
                           category_to_next: CategoryToNext,
                           category_maps: CategoryMaps,
                           ) -> int:
    category = "seed"
    value = seed_number
    while category != "location":
        category_map = category_maps[category]
        value = apply_category_map(category_map, value)
        category = category_to_next[category]
        # print(f"{category = }, {value = }")
    return value


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
