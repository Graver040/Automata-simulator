from collections import deque
from itertools import count

from src.models import Machine


def convert(machine: Machine) -> tuple[Machine, dict[str, tuple[str, str]]]:
    """Build only reachable (original state, previous output) pairs."""
    used = set(machine.states)
    suffixes = count(1)

    def fresh(preferred: str) -> str:
        name = preferred
        while name in used:
            name = f"{preferred}_{next(suffixes)}"
        used.add(name)
        return name

    start = fresh("S")
    queue = deque([(start, machine.initial)])
    pairs = {}
    metadata = {}
    transitions = {}
    state_outputs = {start: None}

    while queue:
        source, original = queue.popleft()
        for symbol in machine.inputs:
            edge = original, symbol
            target = machine.transitions[edge]
            output = machine.edge_outputs[edge]
            pair = target, output
            if pair not in pairs:
                name = fresh(f"{target}_{output}")
                pairs[pair] = name
                metadata[name] = pair
                state_outputs[name] = output
                queue.append((name, target))
            transitions[source, symbol] = pairs[pair]

    result = Machine("Moore", tuple(state_outputs), machine.inputs, machine.outputs,
                     start, transitions, {}, state_outputs)
    return result, metadata
