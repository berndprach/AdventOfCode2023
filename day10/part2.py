
from part1 import (
    read_input,
    parse_lines,
    label_starting_position,
    Position,
    Grid,
    Directions,
    valid_neighbours,
)


def get_loop_positions(starting_position: Position,
                       grid: Grid,
                       ) -> list[Position]:
    previous_position = starting_position
    first_direction = grid[starting_position].directions[0]
    current_position = starting_position + first_direction.value
    loop_positions = [starting_position]

    while current_position != starting_position:
        loop_positions.append(current_position)
        current_pipe = grid[current_position]
        next_position = current_pipe.next_position(previous_position)

        previous_position = current_position
        current_position = next_position

    return loop_positions


def count_right_turns(loop_positions: list[Position]):
    number_of_right_turns = 0
    for i in range(len(loop_positions)):
        previous_position = loop_positions[i - 1]
        current_position = loop_positions[i]
        next_position = loop_positions[(i + 1) % len(loop_positions)]

        if is_right_turn(previous_position, current_position, next_position):
            number_of_right_turns += 1

    return number_of_right_turns


def is_right_turn(previous_position, current_position, next_position):
    direction_in = Directions(current_position + (-previous_position))
    right_turn_in = RIGHT_TURN[direction_in]
    direction_out = Directions(next_position + (-current_position))
    return direction_out == right_turn_in


RIGHT_TURN = {
    Directions.UP: Directions.RIGHT,
    Directions.RIGHT: Directions.DOWN,
    Directions.DOWN: Directions.LEFT,
    Directions.LEFT: Directions.UP,
}
LEFT_TURN = {value: key for key, value in RIGHT_TURN.items()}


def find_positions_just_inside(loop_positions: list[Position], inside_turn):
    positions_just_inside = []
    for i in range(len(loop_positions)):
        previous_position = loop_positions[i - 1]
        current_position = loop_positions[i]
        direction = Directions(current_position + (-previous_position))
        inside_direction = inside_turn[direction]
        inside_position = current_position + inside_direction.value
        positions_just_inside.append(inside_position)
        positions_just_inside.append(
            previous_position + inside_direction.value
        )

    return positions_just_inside


def solve(lines: list[str]) -> int:
    starting_position, grid = parse_lines(lines)
    label_starting_position(starting_position, grid)

    loop_positions = get_loop_positions(starting_position, grid)

    number_of_right_turns = count_right_turns(loop_positions)
    number_of_left_turns = count_right_turns(list(reversed(loop_positions)))
    loop_is_clockwise = number_of_right_turns > number_of_left_turns
    inside_turn = RIGHT_TURN if loop_is_clockwise else LEFT_TURN

    positions_just_inside = find_positions_just_inside(loop_positions,
                                                       inside_turn)

    queue = positions_just_inside
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
