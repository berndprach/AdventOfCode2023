from time import time
from typing import Optional

COMPARISONS = {
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
}

Part = dict[str, int]
Condition = tuple[Optional[str], str, int]  # attribute, comparison, value
Rule = tuple[Condition, str]  # e.g. "x>10:one"
Workflow = list[Rule]


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_input(lines: list[str]) -> tuple[dict[str, Workflow], list[Part]]:
    workflows = {}
    line_number = 0
    while lines[line_number] != "":
        line = lines[line_number]
        workflow_name, workflow_rules = parse_workflow(line)
        workflows[workflow_name] = workflow_rules
        line_number += 1

    line_number += 1
    part_ratings = []
    while line_number < len(lines):
        line = lines[line_number]
        part_rating = parse_part_rating(line)
        part_ratings.append(part_rating)
        line_number += 1

    return workflows, part_ratings


def parse_workflow(line: str) -> tuple[str, list[Rule]]:
    # px{a<2006:qkq,m>2090:A,rfg}
    workflow_name, workflow_body = line.split("{")
    rule_strings = workflow_body.split(",")
    rules = [parse_rule(rule_string) for rule_string in rule_strings]
    return workflow_name, rules


def parse_rule(rule_string: str) -> Rule:
    # "a<2006:qkq" OR "rfg}"
    if rule_string.endswith("}"):
        condition = (None, "<", 0)
        next_workflow_name = rule_string[:-1]
        return condition, next_workflow_name

    condition_string, next_workflow_name = rule_string.split(":")
    for comparison_symbol in COMPARISONS:
        if comparison_symbol in condition_string:
            attribute, value_string = condition_string.split(comparison_symbol)
            value = int(value_string)
            condition = (attribute, comparison_symbol, value)
            return condition, next_workflow_name


def parse_part_rating(part_rating_str: str) -> dict[str, int]:
    # {x=787,m=2655,a=1222,s=2876}
    prs = part_rating_str.replace("=", ": ")
    for attribute in "xmas":
        prs = prs.replace(attribute, f"'{attribute}'")
    return eval(prs)


def apply_workflows(part: Part,
                    workflows: dict[str, Workflow],
                    current_rule_name,
                    ) -> str:

    if current_rule_name in {"R", "A"}:
        return current_rule_name

    workflow_rules = workflows[current_rule_name]
    for condition, next_workflow_name in workflow_rules:
        attribute, comparison, value = condition
        if attribute is None:
            return apply_workflows(part, workflows, next_workflow_name)

        comparison_function = COMPARISONS[comparison]
        if comparison_function(part[attribute], value):
            return apply_workflows(part, workflows, next_workflow_name)


def solve(lines: list[str]) -> int:
    workflows, part_ratings = parse_input(lines)
    solution = 0
    for part_rating in part_ratings:
        final_destination = apply_workflows(part_rating, workflows, "in")
        if final_destination == "A":
            solution += sum(part_rating.values())
    return solution


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
