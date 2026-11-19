# Feasibility study

**Technical.** Python dictionaries represent total transition functions and enable keyed lookup. Conversion and simulation run locally. Streamlit provides forms and tables. Its Graphviz view renders DOT, with DOT text and tables available as a fallback. State splitting can increase graph size, so tables remain the primary inspection surface for dense machines.

**Operational.** An instructor can open a supplied exercise, inspect the transition table, convert it and explain the output alignment using input 01. A student can edit transition rows and correct validation errors in place. The prototype uses CSV-style text fields for custom machines. An editable grid and better handling of dense graphs are candidates for M2.

**Economic.** The local prototype requires Python, the listed packages and a browser. The design assumes access to a student computer and requires no paid hosting, database or external API. Setup, testing and preparation time are the main expected costs. No cost or usability measurements were collected.
