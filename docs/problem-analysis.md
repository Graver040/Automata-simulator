# Problem analysis

Students converting output-producing finite-state machines must track both where a transition goes and when its output is emitted. A direct relabeling fails when two transitions enter the same state with different outputs. The simulator makes the construction inspectable and lets students verify the result one input symbol at a time.

## Formal model and scope

Both machine types use M = (Q, Σ, Δ, δ, λ, q0), with nonempty finite state set Q, input alphabet Σ and output alphabet Δ, a single q0 ∈ Q, and a total function δ: Q × Σ → Q. Mealy uses λ: Q × Σ → Δ and labels edges a / z. Moore uses λ: Q → Δ and labels states q / z. Every state/input pair has exactly one destination. Partial and nondeterministic machines are outside scope.

For input length n, retain n Mealy tokens and n + 1 Moore trace entries. The Moore trace begins with the initial-state output. Compare tokens after removing exactly the first Moore entry. For a generated Moore machine the fresh start uses a display-only ε, stored internally as None outside Δ, with no incoming edges. An empty input leaves the Mealy sequence empty and the Moore sequence with its initial entry only.

## Objectives and acceptance

| Objective | Evidence |
|---|---|
| Accept complete machines and diagnose invalid entries | Parser, validator and negative tests |
| Convert in both directions and explain state splitting | Algorithms, worked examples and sample conversions |
| Show both machines in table and diagram form | Prototype result views and UI design |
| Show trace, raw outputs and aligned comparison | Simulation view and expected traces in the examples |
| Provide repeatable demonstrations | Specification samples, README and test plan |
