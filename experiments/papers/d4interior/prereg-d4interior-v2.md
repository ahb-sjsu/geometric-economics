# prereg-d4interior-v2 — Does the Unpooled Interior Chirality Replicate on an Independent Corpus?

**Status:** v2, FROZEN 2026-09-13 (Section 9 steps 1 and 2 executed; the signed
tag is step 3 and OSF registration is the owner's step, its GUID recorded in
`prereg-d4interior-v2.sha256` and not here so this file's hash stays fixed). No
fit has been run on the outcome column of choices13k.

**Supersedes:** `prereg-d4gate-v1`, which is VOID. That registration asked
whether the interior chirality is gated by certainty. Its analysis code
reimplemented `_opt_coords` instead of importing it and got both the form and the
sign convention wrong, so its run did not test what it registered. The void
record is kept at `experiments/papers/d4gate/`.

**Companion to:** `experiments/datasets/RESULTS_d4_rotation.md`,
`experiments/datasets/D4_REHABILITATION.md`,
`experiments/papers/d4gate/analysis/diagnostic_pooling.json`.

**Author:** Andrew H. Bond, San José State University.

> **What has been done before this draft.** The choices13k stimulus columns and
> the per-problem subject count `n` were read, to build the design matrix and to
> run the power simulation of Section 7. The choice column `bRate` has not been
> read and no model has been fitted to it. The CPC18 results quoted below are on
> record in the pooling diagnostic and are treated here as prior knowledge.

---

## 1. The question, and why it changed

The pooling diagnostic reproduced `RESULTS_d4_rotation.md` Part B exactly, at
`d·q = +0.0032` against the published `+0.003`, and then decomposed it. Dropping
the seventeen Kahneman and Tversky corner rows and standardising over CPC18 alone
moves the interior chirality to **`+0.4438`**. Keeping the corners in the
likelihood while standardising over CPC18 alone leaves it at `−0.0002`, which
locates the masking in the corner rows' own contribution to the fit.

So the earlier conclusion, that the fourfold chirality vanishes in the interior,
describes a pooled estimate rather than the interior. Unpooled, the interior
carries a chirality of about `+0.44` on CPC18.

**That number was discovered on CPC18 and cannot be tested on CPC18.** This
registration tests whether it replicates on a corpus that played no part in
finding it.

## 2. Corpus

choices13k, `experiments/datasets/raw/choices13k/c13k_selections.csv`, the
decision-from-description condition `Block == 1` and `Feedback == 0`, which
matches CPC18's `Trial == 1`. 2,380 rows after dropping incomplete records, with
a median of subjects per problem taken from the file's own `n` column.

**Prior use, declared.** choices13k has been used by this programme before, in
`move3_heldout.py`, for the V₄ pure-interaction question. It has not been used
for the chirality question registered here, and no fit of the model below has
been run on it. It is independent of the CPC18 estimate this registration tests,
which is the property that matters.

It is also a better design for the question than CPC18. The domain coordinate
is continuous across the full range, taking 1,033 distinct values at six decimals
and 849 at three, against the three values the voided registration's
mis-implementation produced, and both signs are well represented, 573 rows with
`d < 0` against 1,793 with `d > 0`.

## 3. Coordinate and model, inherited rather than restated

`analysis/c13k_rows.py` **imports** `_opt_coords` from `d4_rotation` and asserts
at import time that a pure-gain certain option returns `d = +1`. Nothing in this
registration restates a definition it inherits. That condition is the direct
lesson of the voided v1 and it is the reason this document names it here.

The model is the six-term kappa of `d4_rotation` part_b, unchanged:

```
kappa(d,q) = c0 + c1 (d²+q²) + c2 (d·q) + c3 d + c4 q + c5 (d²−q²)
```

with the logistic choice likelihood `bEV·ΔEV + kappa·ΔSD` on the per-problem
rate. There is no gate. The gating question of v1 is not revived here and is not
tested by anything below.

## 4. The estimand

`c2`, the coefficient on `d·q`, fitted on choices13k.

## 5. Predictions

Bars are from the Section 7 simulation and live in `analysis/d4int_grade.py`,
which was written before any fit touched `bRate` and is the only place they live.

- **V1, sign and presence.** `c2 > T_pos`, one-sided, because the CPC18 estimate
  is positive and the sign is part of what is being replicated. A negative
  estimate of any size fails this.
- **V2, magnitude agreement.** `c2` lies within a factor of two of the CPC18
  estimate, that is in `[0.5 × 0.4438, 2 × 0.4438]`. This is an equivalence-style
  claim and is the stronger of the two.

Both are reported separately. **No composite verdict is registered.**

## 6. Falsifiers

- **F1.** `c2 ≤ T_pos` means the interior chirality does not replicate. The
  CPC18 `+0.44` is then corpus-specific, the interior question is not settled by
  it, and the earlier record's conclusion is not disturbed by anything in the
  pooling diagnostic beyond the arithmetic it already established.
- **F2.** `c2` below the negative of `T_pos` is a sign reversal, which is a worse
  outcome than a null and must be reported as such rather than as a near miss.
- **F3.** If the two optimizer starts disagree in the objective by more than
  `1e-6`, the run is void and is reported as void rather than retried with other
  starts.
- **F4, stated against ourselves.** V1 passing with V2 failing means the
  chirality replicates in sign but not in size. That is a weaker result than it
  will look, because a small positive coefficient is compatible with many
  mechanisms, and it must not be reported as confirming the CPC18 magnitude.

## 7. Power and size

`power/power_d4interior.py`, stimulus columns and subject counts only, `bRate`
never read. Rows and coordinate come from the same shared module the fit uses.
Generative coefficients are **read at run time** from fit B of
`diagnostic_pooling.json` and are not transcribed, after an earlier draft of that
script transcribed them and got five of six wrong.

Run with 300 replicates at seed 20260913 on 2,380 rows, 1,033 distinct values of
the domain coordinate, 2,127 rows with a nonzero chirality regressor, and a median
of 16 subjects per problem.

**Bar.** `T_pos` = **0.18774979541410625**, the 95th percentile of the null,
one-sided. **Band for V2** = [0.2218875240708106, 0.8875500962832424], a factor
of two either side of the CPC18 estimate of 0.4437750481416212.

| True chirality | V1 sign and presence | V2 within the band |
|---|---|---|
| 0.0000 | 0.053 | 0.007 |
| 0.2219 | 0.960 | 0.947 |
| 0.4438 | 1.000 | 1.000 |
| 0.8876 | 1.000 | 0.190 |

V1 has size 0.053 against a nominal 0.05 and detects half the CPC18 effect 96
percent of the time. V2 correctly rejects a chirality twice the CPC18 estimate,
which is what its 0.190 at 0.8876 means and is the behaviour an equivalence claim
should have.

**A bias the simulation exposed, stated because it bears on V2.** Under a true
chirality of zero this estimator returns **+0.092** on average in this design, and
the upward bias runs between roughly 0.06 and 0.12 across the alternatives tested.
V1 is unaffected, because its bar is the 95th percentile of that same null and is
therefore calibrated for size, as the 0.053 confirms. V2 is affected, because it
compares a raw choices13k estimate against a raw CPC18 estimate and the two
designs need not carry the same bias. **V2 is therefore registered as the weaker
and approximate claim, and a V2 pass must be reported with this paragraph
attached.** Removing the bias would need a bias-corrected estimator, which is not
registered here and would be a change of instrument rather than of threshold.

## 8. What a pass would and would not license

A pass on V1 and V2 licenses the claim that the interior chirality of the
fourfold pattern is real and of consistent size across two lottery corpora, and
that `RESULTS_d4_rotation.md`'s reading of Part B is an artifact of pooling the
corners with the interior. It is a correction to that record and not a new
mechanism.

It does not license D₄. Part A of the earlier test breaks the exact group at the
corners at `χ² = 75.4` and nothing here touches the corners. It does not license
a continuous rotation, which nothing here tests. It does not revive the gating
reading, which v1 was written to test and which is not tested here.

## 9. Freezing procedure

1. Complete Section 7 from the simulation output and write the bars into
   `analysis/d4int_grade.py`.
2. `sha256` of this document and `power/power_d4interior.py` into
   `prereg-d4interior-v2.sha256`, in the `prereg-boundary-v1.sha256` JSON form,
   computed after this document is final.
3. Commit, sign the tag `prereg-d4interior-v2`, push. OSF registration is the
   owner's step and its GUID is recorded in the `.sha256` file, which is not
   edited again.
4. Only then run any fit on `bRate`.

## 10. Errors carried forward from v1, recorded

Three, all made before any outcome was read and all fixed here.

1. **A coordinate was reimplemented rather than imported, and was wrong in form
   and sign.** Fixed by importing it and asserting on it at import time.
2. **A power simulation drew one choice per row** where the target is a rate over
   many subjects, overstating noise by about an order of magnitude. Fixed here
   and in v1 before any bar was adopted.
3. **Generative coefficients were transcribed and five of six were wrong.** Fixed
   by reading them from the record at run time.

The first was caught only by a diagnostic that imported the original code instead
of restating it. The seal, the signature, the grader separation and the power
analysis all worked and none of them caught it.
