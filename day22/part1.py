from collections import defaultdict
from dataclasses import dataclass
from time import time


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Position = tuple[int, int, int]


@dataclass(eq=False)
class Brick:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @property
    def positions(self) -> list[Position]:
        for x in range(self.x, self.x + self.dx):
            for y in range(self.y, self.y + self.dy):
                for z in range(self.z, self.z + self.dz):
                    yield x, y, z

    @property
    def base_positions(self):
        for x in range(self.x, self.x + self.dx):
            for y in range(self.y, self.y + self.dy):
                yield x, y


def parse_lines(lines: list[str]) -> list[Brick]:
    return [parse_brick(line) for line in lines]


def parse_brick(line: str) -> Brick:
    # E.g. "1,0,1~1,2,1"
    start_str, end_str = line.split("~")
    start = tuple(int(x) for x in start_str.split(","))
    end = tuple(int(x) for x in end_str.split(","))
    size = tuple(end[i] - start[i] + 1 for i in range(3))
    return Brick(*start, *size)


def drop_bricks(bricks: list[Brick]):
    smallest_empty_z: dict[tuple[int, int], int] = defaultdict(lambda: 1)
    position_to_brick: dict[Position, Brick] = {}
    rests_on: dict[Brick, set[Brick]] = {brick: set() for brick in bricks}

    for current_brick in sorted(bricks, key=lambda brick: brick.z):
        new_z = 0
        for (x, y) in current_brick.base_positions:
            new_z = max(new_z, smallest_empty_z[(x, y)])
        current_brick.z = new_z

        for (x, y) in current_brick.base_positions:
            smallest_empty_z[(x, y)] = current_brick.z + current_brick.dz

        for (x, y, z) in current_brick.positions:
            position_to_brick[(x, y, z)] = current_brick

        for (x, y) in current_brick.base_positions:
            brick_below = position_to_brick.get(
                (x, y, current_brick.z-1), None
            )
            if brick_below is not None:
                rests_on[current_brick].add(brick_below)

    return rests_on


def solve(lines: list[str]) -> int:
    bricks = parse_lines(lines)
    rests_on = drop_bricks(bricks)
    supports = {brick: [] for brick in bricks}
    for brick, supporting_bricks in rests_on.items():
        for supporting_brick in supporting_bricks:
            supports[supporting_brick].append(brick)

    count = 0
    for brick in bricks:
        if safe_to_disintegrate(brick, rests_on, supports):
            count += 1
    return count


def safe_to_disintegrate(current_brick: Brick, rests_on, supports) -> bool:
    for supported_brick in supports[current_brick]:
        if len(rests_on[supported_brick]) == 1:
            return False
    return True


def main():
    lines = read_input()
    if len(lines) == 0:
        raise ValueError("Input is empty")

    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
