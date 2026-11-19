# Conversion algorithms

## Mealy → Moore

Create one state per reachable destination/output pair. The prototype discovers pairs in breadth-first order using Σ declaration order. The fresh state S models the original start before any input. The pair’s second component records the latest Mealy output. It cannot affect outgoing transitions.

```text
MEALY_TO_MOORE(M):
    create fresh S with display output ε
    queue ← [S]
    while queue is nonempty:
        x ← pop front
        p ← q0 if x = S, otherwise first component of x
        for a in Σ:
            y ← (δ(p, a), λ(p, a))
            if y is new:
                create y with state output equal to its second component
                append y to queue
            add x --a--> y
    return generated Moore machine with initial state S
```

Labels prefer p_z, with numeric suffixes to avoid display-name collisions. Metadata retains p and z independently. The initial label prefers S with a suffix if S is already an original state. Two distinct reachable outputs entering p yield two copies. Unreachable pairs are omitted.

**Correctness.** After the first input a, the new state has the original destination and emitted output. Inductively, after k inputs its first component equals the current original state, and its second equals the kth emitted output. Taking another transition preserves both claims. Dropping the pre-input ε gives equality on every word, including the empty word.

**Cost.** With k = |Σ|, the breadth-first construction visits |Q′| states and creates |Q′|k transitions, with |Q′| ≤ 1 + |Q||Δ|. With keyed dictionary lookup, construction takes O(|Q′|k + |Q|) time and space including the original-state set used for naming. Validation separately scans the original table in O(|Q|k) time, plus alphabet declarations. Exact size depends on distinct reachable incoming outputs. Bounds count symbols as units and assume expected constant-time hashing.

## Moore → Mealy

```text
MOORE_TO_MEALY(M):
    preserve Q, Σ, Δ, δ and q0
    for q in Q:
        for a in Σ:
            p ← δ(q, a)
            assign Mealy output λ(p) to transition (q, a)
    return resulting Mealy machine
```

**Correctness.** Both runs visit the same states because δ and q0 are unchanged. When input a takes the machine to p, the Mealy edge emits the same λ(p) as the Moore destination. The comparison drops the initial Moore entry, which precedes the first transition.

**Cost.** Conversion takes O(|Q||Σ|) time and space for the copied table and edge outputs. Simulation uses O(n + |Σ|) time and space for n input tokens, including construction of a symbol lookup set.
