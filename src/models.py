from dataclasses import dataclass
from typing import Literal

Kind = Literal["Mealy", "Moore"]
Edge = tuple[str, str]


@dataclass
class Machine:
    kind: Kind
    states: tuple[str, ...]  # Q
    inputs: tuple[str, ...]  # Σ
    outputs: tuple[str, ...]  # Δ
    initial: str  # q0
    transitions: dict[Edge, str]  # δ
    edge_outputs: dict[Edge, str]  # Mealy λ
    state_outputs: dict[str, str | None]  # Moore λ; None is the display-only start

    @property
    def initial_marker(self):
        return self.kind == "Moore" and self.state_outputs[self.initial] is None


def display_output(output: str | None) -> str:
    return "ε" if output is None else output
