from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from time import sleep, time


# Position = tuple[int, int]


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

    def __neg__(self):
        return Position(-self.x, -self.y)


Grid = dict[Position, int]


class Direction(Enum):
    Up = Position(0, -1)
    Down = Position(0, 1)
    Left = Position(-1, 0)
    Right = Position(1, 0)


def get_neighbours(position: Position):
    return [position + direction.value for direction in Direction]


State = tuple[Position, Direction, int]  # position, previous direction, steps


@dataclass(order=True)
class State:
    position: Position = field(compare=False)
    previous_direction: Direction = field(compare=False)
    steps_in_direction: int = field(compare=False)
    heat_loss: int

    def visited(self):
        return (
            self.position,
            self.previous_direction,
            self.steps_in_direction,
        )


def find_shortest_path(heat_loss_grid: Grid,
                       start: Position,
                       end: Position
                       ) -> int:
    # starting_state = State(start, Direction.Up, 0, 0)
    starting_state = State(start, None, 0, 0)
    queue = PriorityQueue()
    visited: set[State] = set()
    queue.put(starting_state)
    while not queue.empty():
        # print(queue.queue)
        state = queue.get()

        if state.visited() in visited:
            # print(f"   Already visited {state.visited()}.")
            continue

        # print(state)
        # sleep(0.1)

        visited.add(state.visited())
        if state.position == end:
            return state.heat_loss

        for direction in Direction:
            if state.previous_direction is not None and direction.value == -state.previous_direction.value:
                continue

            if direction == state.previous_direction:
                new_steps = state.steps_in_direction + 1
            else:
                new_steps = 1

            if new_steps > 3:
                continue

            new_position = state.position + direction.value
            if new_position not in heat_loss_grid:
                continue

            new_state = State(
                position=new_position,
                previous_direction=direction,
                steps_in_direction=new_steps,
                heat_loss=state.heat_loss + heat_loss_grid[new_position],
            )
            queue.put(new_state)
            # print(f"  Enqueued {new_state}")


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_input(lines: list[str]) -> Grid:
    heat_loss_grid: Grid = {}
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            heat_loss_grid[Position(x, y)] = int(character)
    return heat_loss_grid


def solve(lines: list[str]) -> int:
    heat_loss_grid = parse_input(lines)
    start = Position(0, 0)
    max_x = max(position.x for position in heat_loss_grid)
    max_y = max(position.y for position in heat_loss_grid)
    end = Position(max_x, max_y)
    return find_shortest_path(heat_loss_grid, start, end)


def main():
    lines = read_input()
    if len(lines) == 0:
        raise ValueError("Input is empty")

    solution = solve(lines)
    # 857 is too low.
    # 872 too high.
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in {time() - start_time:.4f} seconds")
