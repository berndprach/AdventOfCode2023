from typing import Optional

from part1 import (
    read_input,
    parse_lines,
    place_pipe_at_starting_position,
    Position,
    Directions,
    valid_neighbours,
    Pipe,
    update_positions,
)


def solve(lines: list[str]) -> int:
    starting_position, grid = parse_lines(lines)
    place_pipe_at_starting_position(starting_position, grid)

    loop_positions = get_loop_positions(starting_position, grid)

    number_of_right_turns = count_right_turns(loop_positions)
    number_of_left_turns = count_right_turns(list(reversed(loop_positions)))
    loop_is_clockwise = number_of_right_turns > number_of_left_turns
    inside_turn = RIGHT_TURN if loop_is_clockwise else LEFT_TURN

    positions_one_step_inside = get_positions_one_step_inside(
        loop_positions, inside_turn
    )

    return count_positions_inside(
        positions_one_step_inside, grid, loop_positions
    )


def get_loop_positions(starting_position: Position,
                       pipe_at_position: dict[Position, Optional[Pipe]],
                       ) -> list[Position]:
    current_position = pipe_at_position[starting_position].next_positions[0]
    previous_position = starting_position
    loop_positions = [starting_position]

    while current_position != starting_position:
        loop_positions.append(current_position)
        previous_position, current_position = update_positions(
            previous_position, current_position, pipe_at_position
        )

    return loop_positions


RIGHT_TURN = {
    Directions.UP: Directions.RIGHT,
    Directions.RIGHT: Directions.DOWN,
    Directions.DOWN: Directions.LEFT,
    Directions.LEFT: Directions.UP,
}
LEFT_TURN = {value: key for key, value in RIGHT_TURN.items()}


def is_right_turn(previous_position, current_position, next_position):
    direction_in = Directions(current_position - previous_position)
    direction_out = Directions(next_position - current_position)
    return direction_out == RIGHT_TURN[direction_in]


def count_right_turns(loop_positions: list[Position]):
    number_of_right_turns = 0
    for i in range(len(loop_positions)):
        previous_position = loop_positions[i - 1]
        current_position = loop_positions[i]
        next_position = loop_positions[(i + 1) % len(loop_positions)]

        if is_right_turn(previous_position, current_position, next_position):
            number_of_right_turns += 1

    return number_of_right_turns


def get_positions_one_step_inside(loop_positions: list[Position], inside_turn):
    # Returns position one step inside and (some) on the loop itself.
    positions_just_inside = []
    for i in range(len(loop_positions)):
        previous_position = loop_positions[i - 1]
        current_position = loop_positions[i]
        direction = Directions(current_position - previous_position)
        inside_direction = inside_turn[direction]
        positions_just_inside.append(
            current_position + inside_direction.value
        )
        positions_just_inside.append(
            previous_position + inside_direction.value
        )

    return positions_just_inside


def count_positions_inside(positions_one_step_inside, grid, loop_positions):
    queue = positions_one_step_inside
    visited_positions = set(loop_positions)

    inside_count = 0
    while len(queue) > 0:
        current_position = queue.pop(0)
        if current_position in visited_positions:
            continue

        visited_positions.add(current_position)
        inside_count += 1

        for neighbour in valid_neighbours(current_position, grid):
            queue.append(neighbour)

    return inside_count


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
