# Test plan

| ID | Setup / action | Expected result |
|---|---|---|
| T01 | Convert specification Mealy sample and run 01 | Four pair states plus S, exact worked table, post-start tokens 0, 1 |
| T02 | Convert specification Moore sample and run 01 | Original destinations, outputs from destinations, aligned tokens 1, 1; for 00, aligned tokens 1, 0 |
| T03 | One Mealy state with two self-loops emitting red | One pair state plus S |
| T04 | Add a disconnected state emitting a distinct symbol | Its pair is absent from the generated Moore machine |
| T05 | Enter a repeated or missing transition row | Identify duplicate or missing state/input key |
| T06 | Enter unknown destination, invalid output or unknown initial state | Reject definition with a targeted diagnostic |
| T07 | Run empty input on a converted pair | Empty aligned lists; Moore raw list has one entry |
| T08 | Run an unknown input symbol | Reject and identify the symbol and position |
| T09 | Enter whitespace-separated multi-character tokens | Preserve tokens through conversion, simulation and alignment |
| T10 | Load a sample in Streamlit, switch direction and perform both conversions | Results and traces follow the current definition |
| T11 | Inspect original and converted diagrams in a browser | Start arrow and all state and edge labels are readable |
| T12 | Create two distinct pairs with the same preferred display label | Preserve both pairs using distinct display names |

The nine automated tests passed under Python 3.14 with Streamlit 1.63.0, including the Streamlit AppTest smoke test. T11 remains a manual browser check. The local server could not bind a port in the verification environment. A matching trace demonstrates agreement for that input. The algorithm invariants establish agreement for all inputs.
