from dataclasses import dataclass
from time import time


@dataclass
class Pulse:
    is_high: bool
    sender: str
    receiver: str

    def __repr__(self):
        pulse_type = "high" if self.is_high else "low"
        return f"{self.sender} -{pulse_type}-> {self.receiver}"


class PulseModule:
    high_pulses_sent = 0
    low_pulses_sent = 0

    def __init__(self, name: str):
        self.name = name
        self.receivers = []
        self.senders = []

    def add_receiver(self, receiver: str):
        self.receivers.append(receiver)

    def add_sender(self, sender: str):
        self.senders.append(sender)

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError

    def send_pulse(self, is_high: bool):
        if is_high:
            PulseModule.high_pulses_sent += len(self.receivers)
        else:
            PulseModule.low_pulses_sent += len(self.receivers)

        return [
            Pulse(is_high, self.name, receiver)
            for receiver in self.receivers
        ]


class FlipFlopModule(PulseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.is_high:
            return []

        self.state = not self.state
        return self.send_pulse(is_high=self.state)


class ConjunctionModule(PulseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.last_incoming_was_high = {}

    def add_sender(self, sender: str):
        super().add_sender(sender)
        self.last_incoming_was_high[sender] = False

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.last_incoming_was_high[pulse.sender] = pulse.is_high
        if all(self.last_incoming_was_high.values()):
            return self.send_pulse(is_high=False)
        else:
            return self.send_pulse(is_high=True)


class BroadcastModule(PulseModule):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return self.send_pulse(is_high=pulse.is_high)


class ButtonModule(PulseModule):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise ValueError("Button module should not receive any pulses")


def read_input() -> list[str]:
    with open("input.txt") as f:
        lines = f.read().splitlines()
    return lines


def parse_input(lines: list[str]) -> dict[str, PulseModule]:
    pulse_modules = {}
    for line in lines:
        # E.g. "%qx -> gz", "broadcaster -> sr, cg, dt, zs"
        name_str, receiver_str = line.split(" -> ")
        if name_str.startswith("%"):
            name = name_str[1:]
            pulse_module = FlipFlopModule(name)
        elif name_str.startswith("&"):
            name = name_str[1:]
            pulse_module = ConjunctionModule(name)
        elif name_str == "broadcaster":
            pulse_module = BroadcastModule(name_str)
        else:
            raise ValueError(f"Unknown pulse module: {line}")

        pulse_modules[pulse_module.name] = pulse_module
        for receiver_name in receiver_str.split(", "):
            pulse_module.add_receiver(receiver_name)

    for pulse_module in pulse_modules.values():
        for receiver_name in pulse_module.receivers:
            reciever_module = pulse_modules.get(receiver_name, None)
            if reciever_module is not None:  # Excluding e.g. "output" module
                reciever_module.add_sender(pulse_module.name)

    button_module = ButtonModule("button")
    button_module.add_receiver("broadcaster")
    pulse_modules["button"] = button_module
    return pulse_modules


def solve(lines: list[str]) -> int:
    pulse_modules = parse_input(lines)

    for _ in range(1_000):
        process_button_press(pulse_modules)

    return PulseModule.high_pulses_sent * PulseModule.low_pulses_sent


def process_button_press(pulse_modules: dict[str, PulseModule]) -> None:
    pulse_queue = pulse_modules["button"].send_pulse(is_high=False)
    while len(pulse_queue) > 0:
        pulse = pulse_queue.pop(0)
        reciever_module = pulse_modules.get(pulse.receiver, None)
        if reciever_module is None:  # E.g. "output" module
            continue
        new_pulses = reciever_module.process_pulse(pulse)
        pulse_queue.extend(new_pulses)


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
