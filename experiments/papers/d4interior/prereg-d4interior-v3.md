# prereg-d4interior-v3 — Does the Unpooled Interior Chirality Replicate on an Independent Corpus?

**Status:** v3, FROZEN 2026-09-13 (Section 10 steps 1 and 2 executed; the signed
tag is step 3 and OSF registration is the owner's step, its GUID recorded in
`prereg-d4interior-v3.sha256` and not here so this file's hash stays fixed). No
fit has been run on `bRate`.

**Supersedes:** `prereg-d4interior-v2`, which was VOID under its own F3 when two
Powell starts disagreed by 0.018 in the objective. The question is unchanged. The
estimator is replaced and every bar is recomputed.

**Author:** Andrew H. Bond, San José State University.

> **What has been done before this draft.** The choices13k stimulus columns and
> the per-problem subject count `n` were read, to build the design, to run the
> conditioning check of Section 5, to verify the estimator of Section 4 on
> synthetic data, and to run the power simulation of Section 8. `bRate` has not
> been read and no model has been fitted to it. The CPC18 numbers quoted are on
> record in the pooling diagnostic.

---

## 1. The question

Unchanged from v2. Dropping the seventeen Kahneman and Tversky corner rows moves
the CPC18 interior chirality from `+0.003` to `+0.4438`, so the earlier reading
that it vanishes in the interior describes a pooled estimate. That number was
discovered on CPC18. This asks whether it replicates on choices13k, which played
no part in finding it.

## 2. Corpus

choices13k, `Block == 1` and `Feedback == 0`, 2,380 rows, a median of 16 subjects
per problem. Declared prior use: choices13k was used by this programme in
`move3_heldout.py` for the V₄ pure-interaction question, not for this one.

## 3. Coordinate, inherited rather than restated

`analysis/c13k_rows.py` imports `_opt_coords` from `d4_rotation` and asserts at
import that a pure-gain certain option returns `d = +1`. This condition is the
lesson of the voided `prereg-d4gate-v1`, whose code reimplemented that function
and got its form and sign wrong.

## 4. The estimator, and why it changed

The linear predictor is `b0·dEV + Σ_k c_k·T_k·dSD`, linear in the parameters, so
with a logistic link and log loss **the objective is convex**, its Hessian being
`X'diag(p(1−p))X`. It is strictly convex where the design has full column rank,
which Section 5 confirms. The maximum likelihood estimate therefore exists, is
unique, and is reached by a gradient method.

`analysis/kappa_mle.py` solves it by Newton with a backtracking line search on
simple decrease, and reports the infinity norm of the gradient. Convergence is
declared at `1e-5`, which the simulation reaches on every draw.

**v2 did not fail because of the data.** On synthetic data with a known chirality
of `+0.4438`, Newton returns `+0.4532` from six different starts with gradient
norms near `1e-14` and identical objectives, while Powell returns `+0.5889` and
`+0.6274` from two starts at a **worse** likelihood. Powell was not finding the
optimum of a convex problem. Most of the `+0.092` bias v2 reported was that
failure, and this estimator's null mean is `−0.0012`.

## 5. Conditioning, checked on covariates before freezing

The effective design is `dEV` beside each kappa term times `dSD`. With columns
scaled to unit norm its condition number is **6.1** on choices13k and **6.0** on
the CPC18 interior, with every variance inflation under 6 and the chirality
column the least inflated at 2.8. The term set is not collinear and is not the
problem, which is why v3 changes the estimator and not the terms.

## 6. The estimand

`c2`, the coefficient on `d·q`, fitted on choices13k by the estimator of
Section 4.

## 7. Predictions

Bars live in `analysis/d4int_grade_v3.py` and nowhere else.

- **V1, sign and presence.** `c2 > 0.10431881348530625`, one-sided, the 95th percentile
  of the null. The CPC18 estimate is positive and the sign is part of what is
  being replicated, so a negative estimate of any size fails.
- **V2, magnitude agreement.** `c2 ∈ [0.2218875..., 0.8875501...]`, a factor of
  two either side of the CPC18 estimate. An equivalence-style claim.

Reported separately. **No composite verdict is registered.**

## 8. Power and size

500 replicates, seed 20260913, generative coefficients read at run time from fit
B of `diagnostic_pooling.json` rather than transcribed. Targets drawn as rates at
the true per-problem subject counts.

| True chirality | mean estimate | V1 | V2 |
|---|---|---|---|
| 0.0000 | +0.0003 | 0.034 | 0.000 |
| 0.2219 | +0.2234 | 0.966 | 0.514 |
| 0.4438 | +0.4448 | 1.000 | 1.000 |
| 0.8876 | +0.8897 | 1.000 | 0.514 |

Null mean `−0.0011965`, null sd `0.0638`, and **zero non-convergence in all 2,000
draws**. The estimator is unbiased to three decimals at every alternative, which
v2's was not.

V1 has size 0.034 against a nominal 0.05, slightly conservative, and detects half
the CPC18 effect 97 percent of the time. V2 reads 0.514 at both 0.2219 and
0.8876 because those are the band's own endpoints, so a truth sitting exactly on
an endpoint is accepted about half the time. That is the expected behaviour of a
bounded equivalence test and not a defect, and it means **V2 discriminates the
centre of the band from its edges and nothing finer.**

## 9. Falsifiers

- **F1.** `c2 ≤ T_pos` means the chirality does not replicate. The CPC18 `+0.44`
  is then corpus-specific and the interior question is not settled by it.
- **F2.** `c2 < −T_pos` is a sign reversal, a worse outcome than a null, to be
  reported as such and not as a near miss.
- **F3.** A gradient infinity norm above `1e-5` voids the run, which is reported
  as void and not retried. The simulation reached this on 2,000 of 2,000 draws,
  so a failure here would indicate something about the real data that the
  synthetic draws do not contain.
- **F4, against ourselves.** V1 passing with V2 failing is replication in sign
  only. A small positive coefficient is compatible with many mechanisms and must
  not be reported as confirming the CPC18 magnitude.

## 10. Freezing procedure

1. Write the bars into `analysis/d4int_grade_v3.py`. Done.
2. Finalise this document, **then** hash it with `power/power_d4interior_v3.py`
   into `prereg-d4interior-v3.sha256`. v1 hashed before finalising and had to
   recompute.
3. Commit, sign the tag `prereg-d4interior-v3`, push.
4. Only then run any fit on `bRate`.

## 11. Errors in this lineage, all recorded

1. **v1: a coordinate reimplemented rather than imported, wrong in form and
   sign.** Fixed by importing and asserting at import.
2. **v1: a power simulation drawing one choice per row** where the target is a
   rate over many subjects. Fixed by drawing at the real counts.
3. **v1 lineage: generative coefficients transcribed, five of six wrong.** Fixed
   by reading them from the record at run time.
4. **v2: a derivative-free optimizer on a convex problem**, which did not reach
   the optimum and produced bars measuring its own failure. Fixed by solving the
   convex problem with Newton and verifying against a known answer.
5. **v3 drafting: a convergence threshold of `1e-6`** that excluded draws
   settling at `1e-6` to `3e-6`, which measured the threshold rather than the
   estimator. Set to `1e-5`, at which nothing is excluded.

Each is now prevented by construction rather than by attention. The first was
caught by a diagnostic that imported the original code, the fourth by verifying
an estimator against a known answer before trusting it, and the fifth by counting
failures instead of aborting on them.
