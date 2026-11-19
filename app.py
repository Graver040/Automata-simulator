import streamlit as st

from src import mealy_to_moore, moore_to_mealy
from src.examples import MEALY, MOORE
from src.models import display_output
from src.parser import parse
from src.simulator import aligned, simulate, tokenize
from src.visualization import dot, table

st.set_page_config(page_title="Mealy–Moore Simulator", layout="wide")
st.title("Mealy–Moore Machine Conversion Simulator")

direction = st.radio("Conversion direction", ("Mealy → Moore", "Moore → Mealy"), horizontal=True)
kind = direction.split()[0]
source = st.radio("Machine", ("Specification example", "Custom machine"), horizontal=True)
sample = (MEALY if kind == "Mealy" else MOORE) if source == "Specification example" else ("",) * 6
configuration = (direction, source)
if st.session_state.get("configuration") != configuration:
    st.session_state.pop("conversion", None)
    st.session_state.pop("word", None)
    st.session_state.configuration = configuration

key = f"{kind}-{source}"
with st.form(key):
    st.subheader("Machine definition")
    st.caption("Use comma-separated declarations and one CSV row per transition. Edit a sample to explore variations.")
    left, right = st.columns(2)
    states = left.text_input("States (Q)", sample[0], key=f"{key}-states")
    inputs = left.text_input("Input alphabet (Σ)", sample[1], key=f"{key}-inputs")
    outputs = right.text_input("Output alphabet (Δ)", sample[2], key=f"{key}-outputs")
    initial = right.text_input("Initial state (q0)", sample[3], key=f"{key}-initial")
    shape = "from, input, to, output" if kind == "Mealy" else "from, input, to"
    transitions = st.text_area(f"Transitions ({shape})", sample[4], key=f"{key}-transitions")
    state_outputs = ""
    if kind == "Moore":
        state_outputs = st.text_area("State outputs (state, output)", sample[5], key=f"{key}-state-outputs")
    submitted = st.form_submit_button("Validate and convert", type="primary")

if submitted:
    st.session_state.pop("conversion", None)
    try:
        original = parse(kind, states, inputs, outputs, initial, transitions, state_outputs)
        if kind == "Mealy":
            target, pairs = mealy_to_moore.convert(original)
        else:
            target, pairs = moore_to_mealy.convert(original), {}
        st.session_state.conversion = original, target, pairs
    except ValueError as error:
        st.error(str(error))

if "conversion" not in st.session_state:
    st.stop()

original, target, pairs = st.session_state.conversion
st.subheader("Conversion results")
for column, machine, title in zip(st.columns(2), (original, target), ("Original", "Converted")):
    with column:
        st.markdown(f"**{title} · {machine.kind}**")
        st.dataframe(table(machine), hide_index=True)
        graph = dot(machine)
        st.graphviz_chart(graph)
        with st.expander("Diagram source (DOT)"):
            st.code(graph, language="dot")

if pairs:
    st.markdown("**Reachable state copies**")
    st.write("Each reachable destination/output pair becomes one state. Multiple rows for an original state indicate a split.")
    st.write(f"Fresh start: {target.initial} / ε. Its outgoing transitions reproduce the original initial state's first step.")
    st.dataframe([{"Moore state": name, "Original state": state, "Incoming output": output}
                  for name, (state, output) in pairs.items()], hide_index=True)
else:
    st.write("Each Mealy edge uses the output of its destination Moore state.")

st.subheader("Test an input")
st.caption("Use adjacent characters for single-character alphabets or spaces between tokens for other alphabets. Blank input runs zero steps.")
word = st.text_input("Input string", "01" if source == "Specification example" else "", key="word")
try:
    tokens = tokenize(word, original.inputs)
    sequences = []
    for column, machine in zip(st.columns(2), (original, target)):
        trace = simulate(machine, tokens)
        sequence = aligned(machine, trace)
        sequences.append(sequence)
        with column:
            st.markdown(f"**{machine.kind} trace**")
            st.text(f"Initial state: {trace.initial}")
            st.dataframe([dict(zip(("From", "Input", "To", "Output"), step)) for step in trace.steps],
                         hide_index=True)
            st.text(f"Raw: {[display_output(token) for token in trace.raw]}")
            st.text(f"Aligned: {sequence}")
    st.caption("Alignment excludes exactly the first Moore output entry.")
    if sequences[0] == sequences[1]:
        st.success("Aligned outputs match for this input.")
    else:
        st.error("Aligned outputs differ for this input.")
except ValueError as error:
    st.error(str(error))
