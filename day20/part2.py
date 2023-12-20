import math
from time import time

from part1 import read_input, parse_input, PulseModule


def solve_brute_force(lines: list[str], number_of_button_presses: int) -> int:
    pulse_modules = parse_input(lines)

    for i in range(number_of_button_presses):
        pulse_queue = pulse_modules["button"].send_pulse(is_high=False)
        while len(pulse_queue) > 0:
            pulse = pulse_queue.pop(0)

            if pulse.receiver == "rx" and not pulse.is_high:
                return i+1

            pulse_module = pulse_modules.get(pulse.receiver, None)
            if pulse_module is None:  # E.g. "output" module
                continue
            new_pulses = pulse_module.process_pulse(pulse)
            pulse_queue.extend(new_pulses)

    raise ValueError("No solution found")


def find_incoming_highs(pulse_modules: dict[str, PulseModule],
                        module_name: str,
                        number_of_button_presses=10_000,
                        ) -> dict[str, list[int]]:
    times_button_pressed = 0
    pulse_queue = []

    module_of_interest = pulse_modules[module_name]
    last_incoming_was_high: dict[str, list[int]] = {
        sender: [] for sender in module_of_interest.senders
    }

    while True:
        if len(pulse_queue) == 0:
            pulse_queue = pulse_modules["button"].send_pulse(is_high=False)
            times_button_pressed += 1

            if times_button_pressed > number_of_button_presses:
                return last_incoming_was_high

        pulse = pulse_queue.pop(0)
        reciever_module = pulse_modules.get(pulse.receiver, None)
        if reciever_module is None:  # E.g. "output" module
            continue
        new_pulses = reciever_module.process_pulse(pulse)
        pulse_queue.extend(new_pulses)

        for sender in module_of_interest.senders:
            if module_of_interest.last_incoming_was_high[sender]:
                if times_button_pressed in last_incoming_was_high[sender]:
                    continue
                last_incoming_was_high[sender].append(times_button_pressed)


def solve(lines: list[str]) -> int:
    pulse_modules = parse_input(lines)

    last_incoming_was_high = find_incoming_highs(pulse_modules, "rg")
    periods = [min(times) for times in last_incoming_was_high.values()]
    return lowest_common_multiple(periods)


def lowest_common_multiple(numbers: list[int]) -> int:
    return math.lcm(*numbers)


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
