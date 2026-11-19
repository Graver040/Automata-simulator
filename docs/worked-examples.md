# Worked examples

Both exercises use Σ = Δ = {0, 1}, Q = {A, B} and q0 = A. The tables follow the specification.

## Mealy → Moore

| State | Input 0 | Input 1 |
|---|---|---|
| A (initial) | B/0 | A/1 |
| B | A/0 | B/1 |

A receives output 0 from B on 0 and output 1 from A on 1. B receives output 0 from A on 0 and output 1 from B on 1. Create A_0, A_1, B_0 and B_1 plus S. From S, use A's outgoing transitions. Both A copies inherit A's destinations as pairs and both B copies inherit B's destinations as pairs. All four pairs are reachable.

| State | Output | Input 0 | Input 1 |
|---|---|---|---|
| S (initial) | ε | B_0 | A_1 |
| A_0 | 0 | B_0 | A_1 |
| A_1 | 1 | B_0 | A_1 |
| B_0 | 0 | A_0 | B_1 |
| B_1 | 1 | A_0 | B_1 |

| Step | Input | Original Mealy | Converted Moore |
|---|---|---|---|
| 0 | — | A, no output | S, ε |
| 1 | 0 | A → B, 0 | S → B_0, 0 |
| 2 | 1 | B → B, 1 | B_0 → B_1, 1 |

Mealy emits 01 and Moore displays ε01. Removing the first Moore entry gives 01.

## Moore → Mealy

| State | Output | Input 0 | Input 1 |
|---|---|---|---|
| A (initial) | 0 | B | A |
| B | 1 | A | B |

Every transition entering A gets output 0. Every transition entering B gets output 1. Keep all transition destinations and the initial state.

| State | Input 0 | Input 1 |
|---|---|---|
| A (initial) | B/1 | A/0 |
| B | A/0 | B/1 |

| Step | Input | Original Moore | Converted Mealy |
|---|---|---|---|
| 0 | — | A, 0 | A, no output |
| 1 | 0 | A → B, 1 | A → B, 1 |
| 2 | 1 | B → B, 1 | B → B, 1 |

For input 01, Moore emits 011 and Mealy emits 11. Removing the first Moore entry gives 11.

**Correction to specification §7.2.** Its table sends B to B on input 1. The printed A → B → A path, raw Moore output 010 and Mealy output 10 correspond to input 00. The table and conversion rule above are unchanged.
