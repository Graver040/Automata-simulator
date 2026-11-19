# Existing-tool study

| Tool | Documented capabilities | Relevance to this design |
|---|---|---|
| JFLAP | Graphical Mealy and Moore construction and step-by-step execution. Its Moore tutorial describes emitting the initial-state output at startup. | Reference for teaching notation, traces and startup behavior. |
| MathWorks Stateflow | Supports Mealy and Moore charts and documents changing chart semantics, action placement and timing differences. | Reference for output timing in an engineering workflow. Stateflow chart conversion is described in its own action and execution model. |

The proposed contribution is a table-first exercise for the course model, with an explicit mapping from original states and emitted symbols to generated states and a side-by-side aligned trace. The comparison is based on published documentation.

- [JFLAP Mealy tutorial](https://jflap.org/tutorial/mealy/mealyMachines.html)
- [JFLAP Moore tutorial](https://jflap.org/tutorial/mealy/mooreMachines.html)
- [MathWorks Stateflow chart conversion](https://www.mathworks.com/help/stateflow/ug/changing-the-chart-type.html)
