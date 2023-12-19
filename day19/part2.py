from time import time

from part1 import read_input, Workflow, parse_input


class Range:
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def __contains__(self, value: int) -> bool:
        return self.lower <= value <= self.upper

    def __len__(self):
        return self.upper - self.lower + 1

    def split_by(self, value, comparison):
        if comparison == "<":
            true_range = Range(self.lower, value - 1)
            false_range = Range(value, self.upper)
        elif comparison == ">":
            true_range = Range(value + 1, self.upper)
            false_range = Range(self.lower, value)
        else:
            raise ValueError(f"Invalid comparison: {comparison}")

        return true_range, false_range


Box = dict[str, Range]


def find_accepted_boxes(box: Box,
                        workflows: dict[str, Workflow],
                        current_rule_name,
                        ) -> list[Box]:
    if current_rule_name == "A":
        return [box]
    if current_rule_name == "R":
        return []

    workflow_rules = workflows[current_rule_name]
    accepted_boxes = []
    for condition, next_workflow_name in workflow_rules:
        attribute, comparison, value = condition
        if attribute is None:
            new_accepted_boxes = find_accepted_boxes(
                box, workflows, next_workflow_name
            )
            accepted_boxes.extend(new_accepted_boxes)
            continue

        attribute_range = box[attribute]
        true_range, false_range = attribute_range.split_by(value, comparison)
        if len(true_range) > 0:
            true_box = box.copy()
            true_box[attribute] = true_range
            new_accepted_boxes = find_accepted_boxes(
                true_box, workflows, next_workflow_name
            )
            accepted_boxes.extend(new_accepted_boxes)

        box[attribute] = false_range
        if len(false_range) <= 0:
            break

    return accepted_boxes


def solve(lines: list[str]) -> int:
    workflows, _ = parse_input(lines)
    starting_box = {
        attribute: Range(1, 4_000)
        for attribute in "xmas"
    }
    accepted_boxes = find_accepted_boxes(
        starting_box, workflows, "in"
    )
    return sum(
        get_size(box)
        for box in accepted_boxes
    )


def get_size(box: Box) -> int:
    size = 1
    for attribute in "xmas":
        size *= len(box[attribute])
    return size


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
