from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from time import time
from typing import Optional


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


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

    def __neg__(self):
        return Position(-self.x, -self.y)


Grid = dict[Position, int]


def parse_input(lines: list[str]) -> Grid:
    heat_loss_grid: Grid = {}
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            heat_loss_grid[Position(x, y)] = int(character)
    return heat_loss_grid


class Direction(Enum):
    North = Position(0, -1)
    South = Position(0, 1)
    East = Position(1, 0)
    West = Position(-1, 0)


@dataclass(order=True)
class State:
    position: Position = field(compare=False)
    previous_direction: Optional[Direction] = field(compare=False)
    heat_loss: int

    @property
    def visited_attributes(self):
        return (
            self.position,
            self.previous_direction,
        )


def find_shortest_path(heat_loss_grid: Grid,
                       starting_position: Position,
                       goal_position: Position
                       ) -> int:
    starting_state = State(
        starting_position, previous_direction=None, heat_loss=0,
    )
    queue = PriorityQueue()
    queue.put(starting_state)
    visited = set()
    while not queue.empty():
        state = queue.get()

        if state.visited_attributes in visited:
            continue
        visited.add(state.visited_attributes)

        if state.position == goal_position:
            return state.heat_loss

        for direction in possible_new_directions(state.previous_direction):
            for number_of_steps in range(1, 4):
                new_state = move_in_direction(
                    direction, number_of_steps, state, heat_loss_grid
                )
                if new_state.position in heat_loss_grid:
                    queue.put(new_state)


def possible_new_directions(previous_direction: Optional[Direction]):
    if previous_direction is None:
        return Direction

    if previous_direction in {Direction.North, Direction.South}:
        return Direction.West, Direction.East
    else:
        return Direction.North, Direction.South


def move_in_direction(direction: Direction,
                      number_of_steps: int,
                      state: State,
                      heat_loss_grid: Grid,
                      ) -> Optional[State]:
    new_position = state.position
    move_heat_loss = 0
    for step in range(number_of_steps):
        new_position += direction.value
        move_heat_loss += heat_loss_grid.get(new_position, 0)

    new_state = State(
        position=new_position,
        previous_direction=direction,
        heat_loss=state.heat_loss + move_heat_loss,
    )
    return new_state


def solve(lines: list[str]) -> int:
    heat_loss_grid = parse_input(lines)
    starting_position = Position(0, 0)
    max_x = max(position.x for position in heat_loss_grid)
    max_y = max(position.y for position in heat_loss_grid)
    goal_position = Position(max_x, max_y)
    return find_shortest_path(heat_loss_grid, starting_position, goal_position)


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
