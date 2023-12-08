import itertools
import math

from part1 import read_input, parse_lines, Node


# Attempt 1: Brute force
def find_common_end(starting_nodes, instructions, next_node, max_iterations):
    current_nodes = starting_nodes
    iteration_count = 0
    for instruction in itertools.cycle(instructions):
        iteration_count += 1
        current_nodes = [next_node[(node, instruction)]
                         for node in current_nodes]
        if all(node.endswith("Z") for node in current_nodes):
            return iteration_count

        if iteration_count >= max_iterations:
            print(f"Did not find solution in {max_iterations} iterations.")
            raise ValueError("max_iterations exceeded")


def get_starting_nodes(next_node):
    starting_nodes = [node for node, _ in next_node.keys() if node[-1] == "A"]
    return set(starting_nodes)


def solve_brute_force(lines: list[str]) -> int:
    instructions, next_node = parse_lines(lines)
    starting_nodes = get_starting_nodes(next_node)
    max_iterations = 100_000
    solution = find_common_end(
        starting_nodes, instructions, next_node, max_iterations)
    return solution


# Attempt 2a: Find loop and print equations:
def find_loop(starting_node, next_node, instructions):
    current_node = starting_node
    iteration_start_nodes: dict[Node, int] = {}
    end_node_indices = []
    for iteration in range(1_000):
        if current_node in iteration_start_nodes:
            previous_iteration = iteration_start_nodes[current_node]
            loop_start_step = previous_iteration * len(instructions)
            loop_end_step = iteration * len(instructions)
            return loop_start_step, loop_end_step, end_node_indices

        iteration_start_nodes[current_node] = iteration
        for i, instruction in enumerate(instructions):
            current_node = next_node[(current_node, instruction)]
            if current_node.endswith("Z"):
                step = iteration * len(instructions) + i + 1
                end_node_indices.append(step)

    raise ValueError("Did not find loop in 1000 iterations")


def print_end_node_equations(starting_node, next_node, instructions,
                             with_simplification=False):
    print(f"\nConsidering starting node {starting_node}.")
    loop_start_step, loop_end_step, end_node_indices = find_loop(
        starting_node, next_node, instructions
    )
    loop_steps = loop_end_step - loop_start_step
    for end_node_index in end_node_indices:
        if end_node_index < loop_start_step:
            print(f"   Single solution at step {end_node_index}")
        else:
            print(f"   Repeating solution at "
                  f"{end_node_index} + i * {loop_steps}")

    if with_simplification:
        loop_end_node_indices = [i for i in end_node_indices
                                 if i >= loop_start_step]
        end_index, loop_steps = simplify(loop_end_node_indices, loop_steps)
        print(f"   Simplified to: {end_index} + i * {loop_steps}")


def print_all_end_node_equations(lines: list[str], with_simplification=False):
    instructions, next_node = parse_lines(lines)
    starting_nodes = get_starting_nodes(next_node)
    for starting_node in starting_nodes:
        print_end_node_equations(
            starting_node, next_node, instructions, with_simplification
        )


# Attempt 2b: Simplify equations:
def simplify(end_indices, loop_steps):
    if len(end_indices) == 1:
        return end_indices[0], loop_steps

    min_index = min(end_indices)
    new_ends = [min_index]
    for i in end_indices:
        if (i - min_index) % loop_steps == 0:
            continue
        new_ends.append(i)

    if len(new_ends) == 1:
        return new_ends[0], loop_steps

    length = len(new_ends)
    regular_indices = [i * min_index for i in range(1, length + 1)]
    if loop_steps % length == 0 and new_ends == regular_indices:
        return min_index, loop_steps // length

    raise Exception(f"Unclear how to simplify "
                    f"{end_indices} and {loop_steps}")


# Attempt 2c: Final solution:
def solve(lines: list[str]) -> int:
    instructions, next_node = parse_lines(lines)
    starting_nodes = get_starting_nodes(next_node)

    all_loop_steps = []
    for node in starting_nodes:
        loop_start_step, loop_end_step, end_node_indices = find_loop(
            node, next_node, instructions
        )
        loop_steps = loop_end_step - loop_start_step
        end_index, loop_steps = simplify(end_node_indices, loop_steps)
        assert end_index == loop_steps

        all_loop_steps.append(loop_steps)

    return lowest_common_multiple(all_loop_steps)


def lowest_common_multiple(numbers):
    return math.lcm(*numbers)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
