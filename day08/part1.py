import itertools


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


Node = str
Inst = str


def parse_lines(lines: list[str]) -> tuple[str, dict[tuple[Node, Inst], Node]]:
    instructions = lines[0]

    next_node = {}
    for line in lines[2:]:
        # "AAA = (BBB, CCC)"
        from_node, to_nodes = line.split(" = ")
        left_node, right_node = to_nodes[1:-1].split(", ")
        next_node[(from_node, "L")] = left_node
        next_node[(from_node, "R")] = right_node

    return instructions, next_node


def solve(lines: list[str]) -> int:
    instructions, next_node = parse_lines(lines)
    current_node = "AAA"
    steps_count = 0
    for instruction in itertools.cycle(instructions):
        current_node = next_node[(current_node, instruction)]
        steps_count += 1
        if current_node == "ZZZ":
            break

    return steps_count


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
