# Problem Specification: Mealy–Moore Machine Conversion Simulator (M1)

> **Course:** CSET302 – Automata Theory and Computability  
> **Topic:** 14 – Mealy ↔ Moore Machine Conversion  
> **Milestone:** M1 – Problem Analysis and Simulator Design  
> **Purpose of this file:** Give Codex a precise specification for preparing the M1 project materials and a small demonstrable design prototype.  
>
> **Important:** This is an M1 design deliverable, not the full M2 implementation. Prioritize correct theory, design artifacts, algorithms, manually worked examples, and a small prototype only if time permits.

---

## 1. Your role

Act as a careful software engineer and technical-documentation assistant. Help prepare an academically presentable M1 submission for a university Automata Theory project.

Do not invent student names, faculty names, batch numbers, experimental results, or claims about features that have not been implemented. Use clearly marked placeholders where personal or institutional details are missing.

Before changing files, inspect the existing repository and preserve any useful work. If this repository is empty, create a clean project structure.

## 2. Project title

**Mealy–Moore Machine Conversion Simulator**

The proposed simulator converts deterministic finite-state transducers in both directions:

1. Mealy machine → Moore machine
2. Moore machine → Mealy machine

It should help students understand the conversion, inspect the resulting transition tables and state diagrams, and test output behaviour on input strings.

## 3. Problem definition

A Mealy machine associates outputs with transitions. A Moore machine associates outputs with states. Although these models can represent equivalent finite-state input/output behaviour, converting between them requires careful handling of transition outputs, state outputs, and the initial output convention.

The key difficulty in Mealy-to-Moore conversion occurs when transitions entering the same state carry different output symbols. A Moore state has one fixed output, so the destination state may need to be represented by multiple state/output copies.

The project will provide a guided, visual way to perform both conversions and validate their output behaviour.

## 4. Objectives

- Accept a deterministic, complete Mealy or Moore machine as input.
- Support both conversion directions.
- Validate machine definitions and report useful input errors.
- Display original and converted transition tables.
- Display original and converted state diagrams.
- Explain the conversion steps, including any state splitting.
- Simulate an input string on the original and converted machines.
- Compare outputs using an explicitly documented initial-output convention.
- Provide example machines that can be loaded for demonstration.

## 5. Formal machine definitions

Use the following notation consistently throughout the report, UI, source code, and diagrams.

### 5.1 Mealy machine

A Mealy machine is a tuple:

`M = (Q, Σ, Δ, δ, λ, q0)`

where:

- `Q` is a finite set of states.
- `Σ` is the input alphabet.
- `Δ` is the output alphabet.
- `δ: Q × Σ → Q` is the transition function.
- `λ: Q × Σ → Δ` is the output function.
- `q0 ∈ Q` is the initial state.

A transition is displayed as `q -- a / z --> p`, meaning input `a` moves the machine from `q` to `p` and emits output `z`.

### 5.2 Moore machine

A Moore machine is a tuple:

`M = (Q, Σ, Δ, δ, λ, q0)`

where the sets and transition function have the same meanings, but:

- `λ: Q → Δ` assigns one output symbol to each state.

A state is displayed as `q / z`, meaning the machine emits output `z` while it is in state `q`.

### 5.3 Output alignment convention

A Moore machine emits the output of its initial state before consuming any input. A Mealy machine emits one output for each consumed input symbol.

For fair comparison, document this convention clearly:

- For an input of length `n`, the Mealy output has length `n`.
- The Moore output has length `n + 1`, including its initial-state output.
- When comparing a converted pair, exclude the Moore machine's initial output. The remaining `n` Moore outputs must equal the `n` Mealy outputs.

For Mealy-to-Moore conversion, use a fresh initial Moore state with a special display-only output `ε` (or `⊥`) that is not part of the ordinary output alphabet. Its outgoing transitions reproduce the first transition of the original Mealy machine. Explain that this is an alignment convention, not an ordinary output symbol.

For Moore-to-Mealy conversion, the Mealy output on each transition is the output of the destination Moore state. The Moore machine's initial output is omitted from the Mealy output sequence.

## 6. Conversion algorithms

### 6.1 Mealy → Moore

For a Mealy machine `M = (Q, Σ, Δ, δ, λ, q0)`:

1. For each state `p`, identify the distinct output symbols on all transitions entering `p`.
2. For every such output `z`, create a Moore state `(p, z)` whose state output is `z`.
3. Add a fresh initial Moore state `S` with special initial output `ε` (or `⊥`).
4. For each input symbol `a`, add a transition from `S` to `(δ(q0, a), λ(q0, a))`.
5. For every created state `(p, z)` and every input symbol `a`, add a transition:
   `(p, z) -- a --> (δ(p, a), λ(p, a))`.
6. Ensure all target pair states exist. Use a stable, readable naming scheme such as `p_0`, `p_1`, etc., while retaining the original state and output in the displayed metadata.
7. Display which original states were split and why.

Only create pair states that are reachable/needed for the converted machine, or clearly explain if the implementation retains unreachable pairs. Do not silently merge states with different outputs.

**Pseudocode**

```text
MEALY_TO_MOORE(M):
    create fresh initial state S with output ε

    for each original state p:
        for each distinct output z on a transition entering p:
            create Moore state (p, z)
            assign output((p, z)) = z

    for each input a:
        p = δ(q0, a)
        z = λ(q0, a)
        add transition S --a--> (p, z)

    for each created Moore state (p, previous_output):
        for each input a:
            next_state = δ(p, a)
            next_output = λ(p, a)
            add transition (p, previous_output) --a--> 
                (next_state, next_output)

    return Moore machine with initial state S
```

The `previous_output` component identifies the Moore state and its output; outgoing transitions depend on the underlying original Mealy state `p`.

### 6.2 Moore → Mealy

For a Moore machine `M = (Q, Σ, Δ, δ, λ, q0)`:

1. Preserve the states, input alphabet, initial state, and transition destinations.
2. For every state `q` and input `a`, let `p = δ(q, a)`.
3. Label the corresponding Mealy transition with output `λ(p)`, the output of the destination state.
4. Display the converted transition as `q -- a / λ(p) --> p`.

**Pseudocode**

```text
MOORE_TO_MEALY(M):
    create Mealy machine with same states and input alphabet
    preserve initial state

    for each state q:
        for each input a:
            p = δ(q, a)
            z = λ(p)
            add Mealy transition q --a/z--> p

    return Mealy machine
```

## 7. Required manually worked examples

Include both examples below in the M1 documentation. Show the input machine, intermediate reasoning, converted table, and an input-string validation.

### 7.1 Mealy → Moore example

Input Mealy machine:

| State | Input `0` | Input `1` |
|---|---|---|
| `A` (initial) | `B/0` | `A/1` |
| `B` | `A/0` | `B/1` |

Incoming transition outputs:

- `A` receives outputs `0` and `1`, so create `A_0/0` and `A_1/1`.
- `B` receives outputs `0` and `1`, so create `B_0/0` and `B_1/1`.

Add fresh initial state `S/ε`.

Converted Moore table:

| State | State output | Input `0` | Input `1` |
|---|---:|---|---|
| `S` | `ε` | `B_0` | `A_1` |
| `A_0` | `0` | `B_0` | `A_1` |
| `A_1` | `1` | `B_0` | `A_1` |
| `B_0` | `0` | `A_0` | `B_1` |
| `B_1` | `1` | `A_0` | `B_1` |

Validation for input `01`:

- Original Mealy: `A --0/0--> B --1/1--> B`, output `01`.
- Converted Moore: `S --0--> B_0 --1--> B_1`, output sequence `ε01`.
- Excluding the initial `ε`, both outputs are `01`.

### 7.2 Moore → Mealy example

Input Moore machine:

| State | State output | Input `0` | Input `1` |
|---|---:|---|---|
| `A` (initial) | `0` | `B` | `A` |
| `B` | `1` | `A` | `B` |

Converted Mealy table:

| State | Input `0` | Input `1` |
|---|---|---|
| `A` | `B/1` | `A/0` |
| `B` | `A/0` | `B/1` |

Validation for input `01`:

- Moore path: `A → B → A`; state-output sequence is `010`.
- Converted Mealy path: `A --0/1--> B --1/0--> A`; output is `10`.
- Excluding the Moore initial-state output `0`, both outputs are `10`.

## 8. Scope and assumptions

For M1, define the supported input model as:

- Deterministic machines.
- Finite, non-empty state set.
- Finite, non-empty input alphabet.
- Finite, non-empty output alphabet.
- Exactly one initial state.
- Exactly one transition for every state/input pair (complete transition function).
- One output symbol per Mealy transition.
- One output symbol per Moore state.

If partial transition functions are supported later, define their behaviour explicitly. Do not silently treat missing transitions as valid.

The initial version may use single-character symbols for a simpler input format, but the design should avoid assumptions that prevent future support for multi-character labels.

## 9. Proposed user workflow

1. Open the simulator.
2. Select **Mealy → Moore** or **Moore → Mealy**.
3. Choose a sample machine or enter a custom machine.
4. Validate the input.
5. View the original transition table and state diagram.
6. Run conversion.
7. View the conversion explanation and converted machine.
8. Enter an input string.
9. View both execution traces and output strings.
10. Compare outputs using the initial-output convention.

## 10. Proposed architecture

Separate the application into these logical modules:

1. **UI module:** machine selection, forms, examples, results.
2. **Machine model module:** data structures for states, alphabets, transitions, and outputs.
3. **Input parser module:** converts user input into machine objects.
4. **Validation module:** checks completeness, determinism, valid symbols, and initial state.
5. **Conversion module:** contains the two independent conversion algorithms.
6. **Visualization module:** renders state diagrams and transition tables.
7. **Simulation module:** runs input strings and returns execution traces and outputs.
8. **Testing module:** unit tests and sample test cases.

Suggested project structure:

```text
mealy-moore-simulator/
├── app.py
├── problem.md
├── README.md
├── requirements.txt
├── src/
│   ├── models.py
│   ├── parser.py
│   ├── validator.py
│   ├── mealy_to_moore.py
│   ├── moore_to_mealy.py
│   ├── simulator.py
│   └── visualization.py
├── tests/
│   ├── test_mealy_to_moore.py
│   ├── test_moore_to_mealy.py
│   └── test_validation.py
└── docs/
    ├── architecture.md
    ├── flowchart.md
    └── test-cases.md
```

## 11. Suggested technology stack

Use a simple Python-based stack for a fast academic prototype:

- Python 3.10 or later.
- Streamlit for the interface.
- Graphviz for state diagrams.
- Pandas for transition-table presentation.
- Pytest for automated tests.

Use only dependencies that are actually needed. If Graphviz system installation is a barrier, provide a fallback diagram representation rather than blocking the application.

## 12. M1 design artifacts to create

Prepare these artifacts in `docs/`:

1. **Problem analysis:** background, problem statement, objectives, scope, assumptions.
2. **Existing-tool study:** concise comparison of relevant tools. Distinguish verified facts from the proposed project's intended contribution. Do not claim that existing tools lack a feature unless verified.
3. **Feasibility study:** technical, operational, and economic feasibility.
4. **System architecture:** module diagram and descriptions.
5. **Flowchart:** end-to-end simulator workflow, including validation and both conversion branches.
6. **UI wireframe:** proposed screens for machine entry, conversion results, and testing.
7. **Algorithms:** both algorithms with pseudocode and complexity discussion.
8. **Manual validation:** both worked examples in Section 7.
9. **Test plan:** normal cases, state-splitting case, same-output incoming edges, invalid/missing transitions, and input-string tests.

Also prepare a polished M1 report and a short presentation if requested by the user. Use placeholders for missing names and submission details.

## 13. Complexity discussion to include

Let `|Q|` be the number of original states and `|Σ|` the number of input symbols.

- Moore-to-Mealy conversion processes every state/input pair, so its time complexity is `O(|Q| × |Σ|)`.
- Mealy-to-Moore conversion creates at most `|Q| × |Δ|` state/output pairs in a straightforward upper bound. Building the transitions for each created pair takes `O(|Q'| × |Σ|)`, where `|Q'|` is the number of generated Moore states. State that the exact number of generated states depends on distinct incoming outputs and reachability.

Do not claim a tighter bound unless the implementation and assumptions justify it.

## 14. M1 acceptance criteria

The M1 work is complete when:

- [ ] Problem statement and objectives are clear.
- [ ] Mealy and Moore machines are formally defined.
- [ ] Existing tools and feasibility are discussed without unsupported claims.
- [ ] Architecture and module responsibilities are documented.
- [ ] A readable flowchart is included.
- [ ] A UI wireframe is included.
- [ ] Both conversion algorithms and pseudocode are included.
- [ ] Both worked examples are correct.
- [ ] Output alignment is explicitly explained.
- [ ] A test plan is included.
- [ ] Report and presentation contain no invented team or faculty details.
- [ ] All diagrams and tables are legible and consistent with the algorithms.

## 15. Instructions to Codex

Work in this order:

1. Inspect the repository and report what already exists.
2. Create or update `problem.md` using this specification if it is not already present.
3. Create the M1 documentation files under `docs/`.
4. Check all examples and pseudocode for mathematical consistency.
5. If time allows, build a minimal Streamlit prototype with both conversion directions and the two sample machines.
6. Add automated tests for the two worked examples and validation errors.
7. Run the tests and fix failures.
8. Update `README.md` with setup and run instructions.
9. Clearly distinguish implemented functionality from planned M2 functionality.

Do not spend time on authentication, databases, deployment, or decorative features for M1. Do not fabricate test results: run tests before reporting them as passed.

**Priority:** Correct theory and conversion logic > M1 design artifacts > basic working demonstration > visual polish.
