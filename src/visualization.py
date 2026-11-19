import json

from src.models import Machine, display_output


def table(machine: Machine):
    # Explicit headers prevent a declared symbol from colliding with metadata columns.
    records = []
    for state in machine.states:
        record = {"State": state, "Initial": state == machine.initial}
        if machine.kind == "Moore":
            record["State output"] = display_output(machine.state_outputs[state])
        for symbol in machine.inputs:
            edge = state, symbol
            label = machine.transitions[edge]
            if machine.kind == "Mealy":
                label += f" / {machine.edge_outputs[edge]}"
            record[f"Input {symbol}"] = label
        records.append(record)
    return records


def dot(machine: Machine) -> str:
    ids = {state: f"n{index}" for index, state in enumerate(machine.states)}
    lines = ["digraph machine {", "rankdir=LR;", 'start [shape=point, label=""];',
             f"start -> {ids[machine.initial]};"]
    for state in machine.states:
        label = state
        if machine.kind == "Moore":
            label += f" / {display_output(machine.state_outputs[state])}"
        lines.append(f"{ids[state]} [shape=ellipse,label={json.dumps(label, ensure_ascii=False)}];")
    for (state, symbol), target in machine.transitions.items():
        label = symbol
        if machine.kind == "Mealy":
            label += f" / {machine.edge_outputs[state, symbol]}"
        lines.append(f"{ids[state]} -> {ids[target]} [label={json.dumps(label, ensure_ascii=False)}];")
    return "\n".join([*lines, "}"])
