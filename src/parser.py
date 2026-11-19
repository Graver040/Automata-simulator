import csv
import io

from src.models import Kind, Machine
from src.validator import validate


def rows(text: str, width: int, section: str):
    reader = csv.reader(io.StringIO(text), skipinitialspace=True, strict=True)
    try:
        for fields in reader:
            if not fields or (len(fields) == 1 and not fields[0].strip()):
                continue
            cells = tuple(field.strip() for field in fields)
            if len(cells) != width or not all(cells) or any(
                not cell.isprintable() for cell in cells
            ):
                raise ValueError(f"{section}, line {reader.line_num}: expected {width} printable fields.")
            yield cells
    except csv.Error as error:
        raise ValueError(f"{section}, line {reader.line_num}: {error}.") from error


def parse(kind: Kind, states: str, inputs: str, outputs: str, initial: str,
          transition_text: str, output_text: str = "") -> Machine:
    transitions, edge_outputs, state_outputs = {}, {}, {}
    for state, symbol, target, *output in rows(
        transition_text, 4 if kind == "Mealy" else 3, "Transitions"
    ):
        edge = state, symbol
        if edge in transitions:
            raise ValueError(f"Duplicate transition for {edge}.")
        transitions[edge] = target
        if output:
            edge_outputs[edge] = output[0]
    if kind == "Moore":
        for state, output in rows(output_text, 2, "State outputs"):
            if state in state_outputs:
                raise ValueError(f"Duplicate output for state {state!r}.")
            state_outputs[state] = output

    declarations = [
        tuple(part.strip() for part in field.split(",")) for field in (states, inputs, outputs)
    ]
    if any(not value.isprintable() for field in declarations for value in field if value):
        raise ValueError("Declarations must contain printable labels.")
    if any(any(character.isspace() for character in symbol) for symbol in declarations[1]):
        raise ValueError("Input symbols must contain no whitespace.")
    machine = Machine(kind, *declarations, initial.strip(), transitions, edge_outputs, state_outputs)
    validate(machine)
    return machine
