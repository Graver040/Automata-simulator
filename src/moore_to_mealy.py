from src.models import Machine


def convert(machine: Machine) -> Machine:
    edge_outputs = {}
    for edge, target in machine.transitions.items():
        output = machine.state_outputs[target]
        if output is None:
            raise ValueError("A transition cannot enter the display-only initial state.")
        edge_outputs[edge] = output
    return Machine("Mealy", machine.states, machine.inputs, machine.outputs, machine.initial,
                   machine.transitions.copy(), edge_outputs, {})
