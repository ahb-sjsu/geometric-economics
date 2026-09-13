# prereg-d4stability-v1 — **VOID.** The design was mis-oriented against the outcome

**Run 2026-09-13 on Atlas, then voided the same day.** The seal verified, the
optimizer converged, the statistic was calibrated, and **the design matrix was
built the wrong way round.** Nothing in this run may be cited.

## The defect

`stability_rows.py` built the regressors as `A − B`, differencing the two options
in the order they were declared in the transcript:

    dEV = evA - evB
    dSD = sdA - sdB

and built the outcome as **chose the riskier option**:

    y = (chose_a == risky_is_a)

Those two orientations do not agree. When option B is the riskier one, `dSD` is
negative while `y = 1` still means the participant took the risk, so the model is
fitted with the sign of the risk term reversed on those rows. **Only 25.2 percent
of rows have A as the riskier option**, so the mismatch does not average out. It
reverses three quarters of the corpus.

`prereg-d4interior-v3` did not have this defect. It used `y = P(chose A)` against
`A − B` regressors, which is consistent. **v3 stands. This registration does
not.**

## How it was caught

Not by any check in the registration. An exploratory fit of the full kappa
surface, run afterwards to answer a question about what the structure actually is,
returned `bEV = −0.3251`. A negative coefficient on the expected-value difference
says people choose against expected value, which is not a finding, it is a symptom.

| diagnostic | as registered | reoriented |
|---|---|---|
| `corr(dEV, y)` | **−0.1579** | **+0.2736** |
| `bEV` | −0.3251 | **+0.5882** |
| negative log likelihood | 65008.3 | **62333.0** |
| `c2`, the chirality | **−0.1775** | **+0.2506** |

The reoriented model fits **2,675 log-likelihood units better** on the same rows
and the same parameter count. The registered fit was not a worse model of the
data, it was a model of the wrong quantity.

**The chirality changes sign.** Every number in the verdict below is therefore
not merely imprecise but pointed the wrong way.

## The void verdict, recorded rather than deleted

| | Prediction | Reported | Status |
|---|---|---|---|
| W1 | permutation `p < 0.05` on Q | `p` = 0.963, Q = 1.078 | **VOID** |
| W2 | range at least 0.5654 | range = 0.120 | **VOID** |
| W3 | fold estimates not all one sign | all four negative | **VOID** |

The fold estimates were −0.1817, −0.1345, −0.0885, −0.2089 and the whole-corpus
estimate was −0.1775. **None of these should be quoted.**

## What survives

**The machinery survives; the measurement does not.**

* The press accounting stands. All 1,097,375 tokens are still bucketed correctly
  and the corpus is still 95,748 first-press description trials over 5,674
  strictly two-outcome problems. That work was about parsing, not orientation.
* The statistic stands. Cochran's Q at a measured size of 0.025, and the finding
  that an unweighted spread has a size of 0.110, are properties of the test and
  not of the data it was pointed at.
* The power simulation is **compromised in one specific way**. It generated `y`
  from the same mis-oriented design it then fitted, so it was internally
  consistent and correctly measured the size and power of the procedure. What it
  could not detect is that the procedure was aimed at the wrong estimand. **A
  simulation that generates data from the model it fits can never find this class
  of error.**
* The clustering finding stands. The random-split null on Q had a mean of 13.015
  against the 3 a correct model gives, so the trial-level standard errors
  understate the truth by about 2.1. That is a property of the clustering.

## Why the existing checks did not catch it

This lineage has accumulated checks and every one of them passed.

* The coordinate was imported and asserted, not restated. It was correct.
* The estimator was verified against a published value to `6.2e-12`. It was
  correct, and it was being handed the wrong design.
* The bundle was hashed and verified on two machines. It sealed the defect.
* Covariates and outcomes were separated into different files so the power
  simulation could not read the choices. It could not, and the defect was in how
  the covariates related to the outcomes, which that separation does not touch.
* The press accounting balanced exactly. It was about parsing, not orientation.

**Every check tested a component and none tested the relationship between the
design and the outcome.** The one diagnostic that would have caught it in a
second is the sign of `bEV`, because more expected value must make an option more
attractive and any fit that says otherwise is broken. That check costs nothing
and was not in the registration.

## The fix, for v2

1. Orient the regressors to the risky option, `dEV = ev_risky − ev_safe` and
   `dSD = sd_risky − sd_safe`, so that `dSD > 0` on every row and `y = chose the
   riskier option` agrees with it. This also makes `dSD` positive by
   construction, which is easier to reason about than a signed difference.
2. **Add a sign check on `bEV` to the grader as a void condition.** `bEV ≤ 0`
   voids the run. It is a direction that the data cannot plausibly take and a
   registration that cannot detect its own design being reversed is not sealed
   against much.
3. Add an orientation assertion to the row builder, that `dSD > 0` on every kept
   row, so a future mis-orientation fails at build time rather than at
   interpretation time.
4. Re-run the power simulation. Its size and power numbers were measured for a
   procedure aimed at the wrong target and must be re-measured, even though the
   statistic itself is unchanged.

## Record of the lineage

| | Outcome | Cause |
|---|---|---|
| `prereg-d4gate-v1` | VOID | a coordinate reimplemented instead of imported, wrong in form and sign |
| `prereg-d4interior-v2` | VOID under its own F3 | a derivative-free optimizer did not reach the optimum of a convex problem |
| `prereg-d4interior-v3` | V1 FAIL, V2 FAIL, F2 fired | valid |
| `prereg-d4stability-v1` | **VOID** | the design matrix was oriented `A − B` against an outcome oriented `chose the riskier`, reversing 75 percent of rows |

Three of four registrations in this line have been void. Two of the three were
caught by machinery written in advance. **This one was not.** It was caught by a
number that looked wrong in an analysis nobody had registered, which is luck
wearing the clothes of diligence, and the correct response is to convert it into
a check that runs every time.
