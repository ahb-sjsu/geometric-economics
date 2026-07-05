# Ruggeri prospect-theory leg — held-out leg #2 of `prereg-sigma-v1`

Ruggeri et al. (2020, *Nature Human Behaviour*) replicated the 17 Kahneman-Tversky (1979) choice
problems across **19 countries, 4,098 subjects, 69,396 choices**. A clean binary-choice lottery
corpus in the **same 5-feature space** as the constrained-Σ fuzz (EV, SD, skew, worst, p-favorable),
so it is a direct, apples-to-apples re-test of the low-rank hypothesis on held-out data — plus a
cross-country universality test. Problem definitions transcribed from `eris-econ/prospect.py`
(economically-correct encoding: item 11 = effective two-stage; items 12–13 fold in the endowment).

## Fit by structure (pooled over 19 countries × 17 problems)

| structure | #p | native NLL |
|---|--:|--:|
| isotropic | 2 | 0.6821 |
| **diagonal** | 6 | 0.6799 |
| **rank-1** | 6 | 0.6673 |
| rank-2 | 11 | **0.6478** |
| banded | 10 | 0.6784 |
| block | 10 | 0.6786 |
| full | 16 | 0.6478 |

(chance = 0.6931)

## Pre-registered verdict

- **H1 (low-rank sufficiency): PASS (marginal).** rank-1 (0.6673) is within **0.0195** of full (0.6478)
  — just under the 0.02 threshold. rank-1 captures most, but not quite all, of the structure here.
- **H3 (rank-1 beats diagonal at equal params): PASS.** rank-1 0.6673 vs diagonal 0.6799 —
  **+0.0126 better at the same 6 parameters**. Off-diagonal structure is real; diagonal is suboptimal.
- **H4 (low, not full, rank): PASS.** **rank-2 (11 params) equals full (16 params) exactly** (0.6478);
  higher rank adds nothing. The honest nuance vs the social leg: here **rank-2 is the sweet spot** —
  it beats rank-1 by 0.0195 — whereas in the ultimatum data rank-1 already equalled full. This
  matches the *original* fuzz, where rank-2 had the best BIC and "low-rank (1–2)" was the conclusion.

**Net:** the low-rank claim holds — diagonal is beaten, full is unnecessary, rank 1–2 suffices —
with rank-2 the tighter choice on this corpus.

## Cross-country universality (H2 analog): **99% / 99%**

Split the 19 countries in half, fit the rank-1 metric on one group, recalibrate only temperature on
the other: **group A → B 99% gap-closed, B → A 99%.** The decision metric is shared across countries
— the lottery-domain analog of the cross-lingual "universal shape, culture-specific scale."

## The honest loss-domain caveat (gain vs loss)

| domain | native NLL | chance |
|---|--:|--:|
| gains | **0.568** | 0.693 |
| losses | 0.686 | 0.693 |

- On **gains**, the metric fits well (0.568 ≪ chance). On **losses**, it barely beats chance (0.686).
- **gain → loss transfer: 0% gap-closed.** The raw geometric features (EV, SD, …) **do not capture
  the reflection effect** — the sign-flip whereby risk-seeking appears in the loss domain. A metric fit
  on gains does not transfer to losses.

This is the **same loss-domain weakness** seen throughout: the B1L.1 cross-lingual falsifier, the
temperature/loss issue that prereg-v2 redesigns, and the reason `eris-econ/prospect.py` hand-codes a
domain-dependent flip of d5/d9. The raw-feature low-rank metric is a *gain-domain* result; capturing
reflection requires the domain-flip encoding, which is a separate (documented) modeling choice, not a
free consequence of the geometry.

## Verdict for the low-rank Σ

Leg #2 **confirms** the structural claim on a large, clean, cross-cultural lottery corpus: **diagonal
is beaten, full is unnecessary, rank 1–2 suffices, and the metric is 99% shared across 19 countries** —
with the standing caveat that this is a **gain-domain** result and the loss/reflection domain remains
the known open problem.

*Reproduce: `python ruggeri.py` (needs `raw_social/ruggeri.csv` from eris-econ).*
