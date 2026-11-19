# Mealy–Moore Machine Conversion Simulator

CSET302 · Automata Theory and Computability · Topic 14  
M1 · Problem Analysis and Simulator Design

Start with [the standalone M1 report](M1-Report.html). Open it in a browser. It includes the design, figures, worked examples and test plan, and can be printed from the browser. The original assignment is preserved in [problem.md](problem.md).

## Run the prototype

From the extracted project directory, with Python 3.10 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`. Open the local address Streamlit prints.

Choose a conversion direction and **Specification example**, then click **Validate and convert**. With input `01`, Mealy → Moore displays `01` and `ε01`, aligned to `01`. Moore → Mealy displays `011` and `11`, aligned to `11`. The specification’s §7.2 trace labeled `01` corresponds to `00` under its table. Each run begins at q0. A blank input runs zero steps.

For a custom machine, use comma-separated declarations and CSV transition rows. A Mealy row is `from,input,to,output`. A Moore row is `from,input,to`, with a separate `state,output` row for each state. Input symbols contain no whitespace. Enter adjacent characters for a single-character alphabet, or space-separated tokens when any symbol has multiple characters. The ε output is reserved for the generated Moore start marker. Comparison drops exactly one Moore entry before comparing the token lists.

## Run the tests

```sh
python -m unittest discover -s tests -v
```

The standard library runs the core suite. Installing the requirements enables the Streamlit AppTest smoke test, which exercises both sample conversions and error feedback. The core suite checks the worked tables, shared-output pairs, unreachable pairs, naming collisions, invalid definitions, tokenization and all binary sample inputs through length four. See the [test plan](docs/test-cases.md) for the separate browser readability check.

## Deliverables

| Item | File |
|---|---|
| Problem analysis and notation | [Problem analysis](docs/problem-analysis.md) |
| Study of related tools and feasibility | [Tool study](docs/tool-study.md) · [Feasibility](docs/feasibility.md) |
| System architecture | [Design notes](docs/architecture.md) · [Diagram](docs/architecture.svg) |
| Workflow | [Design notes](docs/flowchart.md) · [Flowchart](docs/flowchart.svg) |
| UI design | [Design notes](docs/wireframes.md) · [Wireframes](docs/wireframes.svg) |
| Pseudocode and correctness | [Algorithms](docs/algorithms.md) |
| Manual checks | [Worked examples](docs/worked-examples.md) |
| Verification | [Test plan](docs/test-cases.md) |

The prototype includes both converters, custom input validation, transition tables, state diagrams with DOT source fallback, reachable split-state metadata, and trace comparison. The M2 design identifies an editable transition grid and clearer navigation for larger diagrams as follow-on work.
