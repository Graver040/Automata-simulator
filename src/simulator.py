from dataclasses import dataclass

from src.models import Machine


@dataclass
class Trace:
    initial: str
    steps: list[tuple[str, str, str, str]]
    raw: list[str | None]


def tokenize(text: str, alphabet: tuple[str, ...]) -> list[str]:
    return list("".join(text.split())) if all(len(symbol) == 1 for symbol in alphabet) else text.split()


def simulate(machine: Machine, tokens: list[str]) -> Trace:
    state = machine.initial
    steps = []
    raw = [machine.state_outputs[state]] if machine.kind == "Moore" else []
    alphabet = set(machine.inputs)
    for index, symbol in enumerate(tokens, start=1):
        if symbol not in alphabet:
            raise ValueError(f"Unknown input symbol {symbol!r} at position {index}.")
        edge = state, symbol
        target = machine.transitions[edge]
        output = machine.edge_outputs[edge] if machine.kind == "Mealy" else machine.state_outputs[target]
        if output is None:
            raise ValueError("Unexpected transition into the display-only initial state.")
        steps.append((state, symbol, target, output))
        raw.append(output)
        state = target
    return Trace(machine.initial, steps, raw)


def aligned(machine: Machine, trace: Trace) -> list[str | None]:
    return trace.raw[1:] if machine.kind == "Moore" else trace.raw
