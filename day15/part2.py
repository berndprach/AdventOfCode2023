
from collections import OrderedDict

from part1 import read_input, hash_string


BoxContends = list[OrderedDict]


def remove_lense(box_contends: BoxContends, label: str) -> None:
    box_number = hash_string(label)
    box_contend = box_contends[box_number]
    box_contend.pop(label, None)


def add_lense(box_contends: BoxContends, label: str, focal_length: int):
    box_number = hash_string(label)
    box_contend = box_contends[box_number]
    box_contend[label] = focal_length


def solve(lines: list[str]) -> int:
    box_contends = [OrderedDict() for _ in range(256)]
    steps = lines[0].split(",")
    for step in steps:
        if "-" in step:  # E.g. "cm-"
            label, _ = step.split("-")
            remove_lense(box_contends, label)
        else:  # E.g. "rn=1"
            label, focal_length_str = step.split("=")
            focal_length = int(focal_length_str)
            add_lense(box_contends, label, focal_length)

    solution = 0
    for i, box_contend in enumerate(box_contends):
        solution += (i+1) * get_focusing_power(box_contend)
    return solution


def get_focusing_power(box_contend: OrderedDict) -> int:
    focusing_power = 0
    for i, focal_length in enumerate(box_contend.values()):
        focusing_power += (i+1) * focal_length
    return focusing_power


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    main()
