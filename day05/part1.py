from dataclasses import dataclass
from typing import Iterator


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Seeds = list[int]


@dataclass
class CategoryMap:
    category_name: str
    next_category: str
    map_tuples: list[tuple[int, int, int]]

    def apply(self, value: int) -> int:
        for to_idx, from_idx, length in self.map_tuples:
            if from_idx <= value < from_idx + length:
                return to_idx + (value - from_idx)
        return value


def parse_lines(lines: list[str]
                ) -> tuple[Seeds, dict[str, CategoryMap]]:
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

    category_maps: dict[str, CategoryMap] = {}

    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if "map" in line:
            from_category, to_category = parse_map_line(line)
            map_tuples = parse_map_tuples(line_iterator)

            category_map = CategoryMap(
                from_category,
                to_category,
                map_tuples,
            )

            category_maps[from_category] = category_map

    return seeds, category_maps


def parse_map_line(line: str) -> tuple[str, str]:
    # "seed-to-soil map:"
    from_category, to_category = line.replace(" map:", "").split("-to-")
    return from_category, to_category


def parse_map_tuples(line_iterator: Iterator[str]):
    """
    seed-to-soil map:
    50 98 2
    52 50 48

    """
    category_map_tuples: list[tuple[int, int, int]] = []
    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if line == "":
            break

        to_idx, from_idx, length = line.split(" ")
        category_map_tuples.append((int(to_idx), int(from_idx), int(length)))
    return category_map_tuples


def solve(lines: list[str]) -> int:
    seeds, category_maps = parse_lines(lines)

    seed_to_location = {}
    for seed in seeds:
        location = get_location_from_seed(seed, category_maps)
        seed_to_location[seed] = location

    closest_location = min(seed_to_location.values())
    return closest_location


def get_location_from_seed(seed_number: int,
                           category_maps: dict[str, CategoryMap],
                           ) -> int:
    category = "seed"
    value = seed_number
    while category != "location":
        category_map = category_maps[category]
        value = category_map.apply(value)
        category = category_map.next_category
    return value


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
