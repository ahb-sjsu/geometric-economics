# Lean check of the path definitions

Checked 2026-11-10 on Atlas, Lean 4 v4.32.2 with Mathlib (rev in `lake-manifest.json`).
`lake build` completed with no errors and no `sorry` (twelve theorems after the additions of the same day). `axioms.log` is the audit: every theorem rests
only on Lean's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

`DecisionPaths.lean` formalises Definitions 6.1 and 6.2 of `geometric-methods` Chapter 6: states, a
weight on each ordered pair made of a symmetric distance term plus boundary penalties, and a decision
as a walk of least total weight to a goal set. Weights are extended non-negative reals, so a penalty
may be infinite.

## What is proved

| Theorem | Statement |
|---|---|
| `cost_append` | The weight of a history followed by a continuation is the sum of the two |
| `ranking_history_free` | Two histories of finite weight that end in the same state rank any two continuations the same way |
| `best_continuation_history_free` | They therefore have the same best continuations to any goal set |
| `history_can_matter_if_weight_reads_the_past` | If a weight may also read the previous state, two histories ending in the same state can prefer different next states |
| `ranking_depends_on_state_and_reference` | If each edge weight reads a reference that is updated after every step, two histories that end in the same state and the same reference rank continuations the same way. History enters through the reference and through nothing else |
| `costRef_const` | A weight that ignores the reference gives back the original cost, so Definition 6.1 is the special case |
| `last_step_suffices_when_reference_is_previous_state` | If the reference is the state just left, two histories that share their last step rank continuations the same way |
| `direction_difference` | With a symmetric distance term, the weights of the two directions of one pair differ by the boundary penalties alone |
| `boundary_edge_costs_its_penalty` | Of two moves at equal distance, one crossing exactly one boundary and one crossing none, the first costs that boundary's penalty more |
| `weight_top_of_sacred` | An infinite penalty on a crossed boundary makes the edge weight infinite |
| `cost_eq_top_of_crossesTop`, `no_finite_path_through_sacred` | If every walk to the goal uses such an edge, no walk to the goal has finite weight (Chapter 6, Theorem 6.4) |

## What this does and does not establish

These are consequences of the definitions. They say nothing about what people do.

- The second and third theorems are the formal ground for the correction in `../DESIGN.md`, Section 3.
  Under Definition 6.2 as written, history does not matter once the state is fixed. The fourth shows
  the door through which it can: a weight that reads the past, such as a reference point that moves.
  A measured effect of history with the state held fixed would therefore show that the definition
  needs that addition, and would not refute or confirm pathfinding.
- The three reference theorems, added 2026-11-10, turn that diagnosis into one measurable quantity. A
  reference that reads no further back than m steps cannot produce an effect of history between two
  walks that share their last m steps. The depth of memory is then the smallest shared suffix at
  which the effect of history is zero: 0 for Definition 6.2 as written, 1 if the reference is the
  previous state. `../chess/analyze_memory.py` estimates that curve. Only the cases m = 0 and m = 1
  are proved here. The statement for general m is the same argument and is not yet formalised.
- `direction_difference` is the identification result the sealed transition study
  (`../../d4transition/`) relies on. It holds for any symmetric distance term, so it does not depend
  on the metric being Mahalanobis or on its coordinates.
- `boundary_edge_costs_its_penalty` is the formal content of the chess test of engine-equal moves.

**Not formalised.** The Mahalanobis form of the distance term (only its symmetry is used). The
stratified structure of `geometric-ethics` Chapter 8 and the Whitney conditions. Bounded search with
a heuristic (Chapter 6, Section 6.5), which is the second way history could enter. Any choice rule
that turns weights into probabilities.

## Build

On Atlas, with the shared Mathlib packages linked as in the other Lean projects there:

```
mkdir -p .lake && ln -s /home/claude/dmo-lean/.lake/packages .lake/packages
export PATH=$HOME/.elan/bin:$PATH
lake build && lake env lean Axioms.lean
```
