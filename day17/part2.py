from queue import PriorityQueue
from time import time

from part1 import (
    read_input,
    Grid,
    Position,
    State,
    parse_input,
    possible_new_directions,
    move_in_direction
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
            for number_of_steps in range(4, 11):
                new_state = move_in_direction(
                    direction, number_of_steps, state, heat_loss_grid
                )
                if new_state.position in heat_loss_grid:
                    queue.put(new_state)


def solve(lines: list[str]) -> int:
    heat_loss_grid = parse_input(lines)
    start = Position(0, 0)
    max_x = max(position.x for position in heat_loss_grid)
    max_y = max(position.y for position in heat_loss_grid)
    end = Position(max_x, max_y)
    return find_shortest_path(heat_loss_grid, start, end)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
