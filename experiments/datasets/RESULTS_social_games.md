# Social-preference games — held-out leg #1 of `prereg-sigma-v1`

The constrained-Σ fuzz found its low-rank winner on **lotteries + level-k games**. The
pre-registration (`prereg-sigma-v1`) named the **Fraser & Nettle ultimatum game** as a *social*
held-out domain to re-test the low-rank hypothesis. This is that re-test — a domain the fuzz never
saw, in a social payoff space where Fehr-Schmidt inequality-aversion is literally a diagonal model,
so "does rank-1 beat diagonal?" is a sharp test.

## Setup

Fraser & Nettle ultimatum, stake = 10, 106 subjects each as responder and proposer.
- **responder**: accept vs reject offer `o` → accept pays `(o, 10−o)`, reject pays `(0,0)`. The
  acceptance curve is reconstructed from each subject's minimum-acceptable-offer (strategy method).
- **proposer**: choose an offer `o ∈ {0..10}` → proposer gets `(10−o, o)`.

Social feature space (K=5, analogous to the fuzz's risk features):
`[ own, other, disadvantageous_inequality, advantageous_inequality, efficiency ]`, z-scored.
Cost = Mahalanobis distance from each option to the **fair split (5,5)** under Σ⁻¹ = LLᵀ;
choice = softmax(−cost/T). Same Σ structures and fitting code as the fuzz.

## Fit by structure

| structure | #p | responder NLL | proposer NLL |
|---|--:|--:|--:|
| isotropic | 2 | 0.594 | 1.779 |
| **diagonal** | 6 | 0.335 | 1.762 |
| **rank-1** | 6 | **0.290** | 1.762 |
| rank-2 | 11 | 0.290 | 1.762 |
| banded | 10 | 0.290 | 1.762 |
| block | 10 | 0.291 | 1.762 |
| full | 16 | 0.290 | 1.762 |

## Pre-registered verdict (responder task — the genuinely multi-dimensional one)

- **H1 (low-rank sufficiency): PASS.** rank-1 (0.290) = full (0.290), gap +0.000. Low rank suffices.
- **H3 (rank-1 beats diagonal at equal params): PASS.** rank-1 0.290 vs diagonal 0.335 — rank-1 is
  **+0.045 better at the same 6 parameters**. The social decision loads on **one coherent direction**
  (a blend of own-payoff, disadvantageous inequality, and efficiency), not independent per-feature
  weights. This is the off-diagonal social structure the diagonal misses.
- **H4 (low, not full, rank): PASS.** rank-2 = rank-1 = full (0.290). No gain from higher rank.

**All three pre-registered hypotheses hold in a held-out social domain.** Combined with the fuzz's
original lottery+game finding, the low-rank Σ now replicates out-of-sample in a *third*, *social*,
domain.

## Generalization across the hunger manipulation

Fit the rank-1 social metric on one condition, recalibrate only temperature on the other:
**Breakfast → No-Breakfast 99% gap-closed; No-Breakfast → Breakfast 99%.** The social metric's
*shape* is invariant to the hunger manipulation; only its scale (temperature) moves — the same
"universal shape, culture-specific scale" pattern seen cross-lingually.

## Honest caveats

- **Proposer task is 1-dimensional.** The proposer's options all satisfy own+other=10 (constant
  efficiency), so they lie on a single line — every rank≥1 structure ties (all 1.762). This is a
  *consistency* check for low-rank, **not** an H3 test. H3 is tested only on the responder task.
- **One game, one dataset.** This is the ultimatum game only. The strongest possible H3 test would
  use binary **allocation** games (Charness-Rabin, Bruhin-Fehr-Schmerer) whose options vary all
  social dimensions independently — those are not on Atlas. The ultimatum responder still varies
  own-payoff, inequality, and efficiency enough to separate rank-1 from diagonal, but a richer
  allocation corpus would be a stronger confirmation.
- **Fixed fair-split ideal** is a theoretical assumption (Fehr-Schmidt equality reference), not
  fitted. Fitting it would add parameters equally to all structures and not change the *relative*
  H1/H3/H4 comparison, but the absolute fit depends on it.
- **Role-transfer (proposer↔responder) is weak and asymmetric** (the two roles have different
  intrinsic dimensionality), so no unification claim is made from it — the within-role structure and
  the condition-generalization are the clean results.

## Status of `prereg-sigma-v1`

| held-out leg | result |
|---|---|
| #1 social-preference games (this) | **H1/H3/H4 PASS** on the responder task; generalizes across conditions |
| #3 cross-lingual (LaBSE + behavioral) | universality supported (representational + behavioral) |
| #2 Ruggeri prospect-theory (19 countries) | data on Atlas; not yet run |

Two of three held-out legs now support the low-rank Σ. The Ruggeri lottery corpus (a clean
discrete-choice dataset, `ruggeri_prospect_theory.csv`) remains for a direct H1–H4 re-test.

*Reproduce: `python social_games.py` (needs `raw_social/fn1.csv` from eris-econ).*
