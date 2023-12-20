import math
from time import time

from part1 import read_input, parse_input, PulseModule


def solve_brute_force(lines: list[str]) -> int:
    pulse_modules = parse_input(lines)

    for i in range(100_000):
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
                        ) -> dict[str, set[int]]:
    times_button_pressed = 0
    pulse_queue = []

    module_of_interest = pulse_modules[module_name]
    incoming_high_events = {
        sender: [] for sender in module_of_interest.senders
    }

    while True:
        if len(pulse_queue) == 0:
            pulse_queue = pulse_modules["button"].send_pulse(is_high=False)
            times_button_pressed += 1

            if times_button_pressed > number_of_button_presses:
                return incoming_high_events

        pulse = pulse_queue.pop(0)
        pulse_module = pulse_modules.get(pulse.receiver, None)
        if pulse_module is None:  # E.g. "output" module
            continue
        new_pulses = pulse_module.process_pulse(pulse)
        pulse_queue.extend(new_pulses)

        for sender in module_of_interest.senders:
            if module_of_interest.last_incoming_was_high[sender]:
                if times_button_pressed in incoming_high_events[sender]:
                    continue
                incoming_high_events[sender].append(times_button_pressed)


def solve(lines: list[str]) -> int:
    pulse_modules = parse_input(lines)

    incoming_high_events = find_incoming_highs(pulse_modules, "rg")
    factors = []
    for sender, times in incoming_high_events.items():
        factors.append(min(times))
    print(f"{factors = }")
    return lowest_common_multiple(factors)


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
