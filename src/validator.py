from itertools import product

from src.models import Machine


def validate(machine: Machine) -> None:
    for name, values in (("States", machine.states), ("Input alphabet", machine.inputs),
                         ("Output alphabet", machine.outputs)):
        if not values or any(not value for value in values):
            raise ValueError(f"{name} must contain nonempty entries.")
        if len(values) != len(set(values)):
            raise ValueError(f"{name} contains duplicate entries.")

    states, inputs, outputs = map(set, (machine.states, machine.inputs, machine.outputs))
    if machine.initial not in states:
        raise ValueError(f"Unknown initial state {machine.initial!r}.")
    if "ε" in outputs:
        raise ValueError("ε is reserved for the generated Moore initial marker.")

    for (state, symbol), target in machine.transitions.items():
        if state not in states or symbol not in inputs:
            raise ValueError(f"Undeclared state or input in transition ({state!r}, {symbol!r}).")
        if target not in states:
            raise ValueError(f"Unknown destination {target!r} in ({state!r}, {symbol!r}).")
    for edge in product(machine.states, machine.inputs):
        if edge not in machine.transitions:
            raise ValueError(f"Missing transition for {edge}.")

    if machine.kind == "Mealy":
        if machine.state_outputs or machine.edge_outputs.keys() != machine.transitions.keys():
            raise ValueError("Mealy requires one output per transition.")
        for edge, output in machine.edge_outputs.items():
            if output not in outputs:
                raise ValueError(f"Unknown output {output!r} on {edge}.")
        return

    if machine.edge_outputs or machine.state_outputs.keys() != states:
        raise ValueError("Moore requires one output per declared state.")
    for state, output in machine.state_outputs.items():
        if output is None and state == machine.initial and state not in machine.transitions.values():
            continue
        if output not in outputs:
            raise ValueError(f"Unknown output {output!r} at state {state!r}.")
