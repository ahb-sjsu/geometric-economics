# prereg-boundary-v1 — Locating the Stake Boundary of the Share-Normalized Geometric Model on Three High-Stakes Ultimatum Datasets

**Status:** v1-rc1, release candidate. NOT frozen. Nothing in this document is a registered claim until Section 11 is executed (hash committed, pushed to the public repository, and registered on OSF) and the hash appears in the paper.
**Companion to:** Geometric Prediction of Economic Behavior I (IEEE TCSS, accepted 2026-09-06; Section VII.A states the income-scaled coordinate as an untested construction) and II; registrations `prereg-v1`, `prereg-v2`, `prereg-sigma-v1`, `prereg-coupling-v1`, `prereg-dimensions-v1`.
**Author:** Andrew H. Bond, San José State University.
**Drafted:** 2026-09-10.

> **What has and has not been done before this draft.** The bundled data were opened once, on 2026-09-10, to identify variables and to compute the descriptive table in Section 3. No model of any kind has been fitted to them. Andersen et al.'s own logit of rejection on the offered amount in days of wages is part of the published record and is treated here as prior knowledge, not as a result of this study.

---

## 1. Background and the claim to be tested

Part I encodes money as a share of the stake, `s_1 = q(x)(1 - x)`, so the calibrated model predicts that ultimatum offers and acceptance are invariant to the stake. Part I tested the offer side on Andersen et al. (2011) and reported the invariance as a failed prediction: offers fall from 24.2% to 12.1% as the stake rises from Rs 20 to Rs 20,000. Part I, Section VII.A, then proposed an income-scaled monetary coordinate, `s_1 = (Lambda/Y) q(x)(1 - x)` with reference `r_1 = Lambda/Y`, as the construction that would make stake effects predictable, and stated it as untested.

This study tests that construction. The question is not whether the share-normalized model is wrong (Part I already says it is), but **where the boundary lies and on which side of the game it lies**: whether one finite monetary variance, entering through the amount at stake measured in the responder's own income units, accounts for how acceptance changes with the stake across three countries, and whether proposer behaviour is captured by the same coordinate or by population-specific reference points.

## 2. Data (fixed)

One file: openICPSR replication package 112485-V1 for Andersen, Ertaç, Gneezy, Hoffman, and List, "Stakes matter in ultimatum games," *AER* 101(7), 2011. Its `20100982_DATA.dta` contains 1,456 responder decisions from three studies, flagged by the indicator columns `SR`, `C`, `IN`:

| Flag | Study | N | Stakes | Currency |
|---|---|---|---|---|
| SR | Slonim and Roth, *Econometrica* 66(3), 1998, Slovakia | 820 | 60, 300, 1,500 | Sk |
| C | Cameron, *Econ. Inquiry* 37(1), 1999, Indonesia | 178 | 5,000, 40,000, 200,000 | Rp |
| IN | Andersen et al., 2011, Meghalaya, India | 458 | 20, 200, 2,000, 20,000 | Rs |

Variables used: `stakes` (pie, local currency), `percent_offer` (offer share `x`), `accept` (0/1), `DaysW` (offered amount in days of wages, as constructed by Andersen et al.), `wealth` (IN only: earnings from prior tasks, 0/1), `SR`/`C`/`IN`. For SR the column `offer` is in points (1,000 = pie); `moneyoffer` is in Sk. For C and IN `offer` is in local currency.

**Derived constants (fixed at freeze).** The daily wage implied by `DaysW / offered amount` is constant within each study: IN Rs 100, C Rp 2,666.7, SR 240 Sk. The pie in days of wages is therefore `pie_days = stakes / daily wage`:

| Study | pie_days at each stake |
|---|---|
| SR | 0.25, 1.25, 6.25 |
| C | 1.875, 15, 75 |
| IN | 0.2, 2, 20, 200 |

`offer_days = DaysW = x * pie_days`. These constants are Andersen et al.'s, not ours; if the AER paper's stated wage rates differ, the paper's rates are used and the discrepancy reported.

**Known limitations of the file, stated in advance.** SR pools all rounds of a ten-round design (no round variable is present), so learning effects are absorbed into the study fixed effect. C and SR carry no `year` or `wealth`. Proposer and responder rows are the same rows (each row is one offer and its acceptance), so proposer analyses use `percent_offer` and responder analyses use `accept`.

## 3. Descriptives computed before freezing (2026-09-10, no fitting)

| Study | Stake | N | pie_days | Mean offer | Mean offer_days | Acceptance |
|---|---|---|---|---|---|---|
| SR | 60 | 240 | 0.25 | 44.5% | 0.11 | 0.83 |
| SR | 300 | 330 | 1.25 | 42.2% | 0.53 | 0.88 |
| SR | 1,500 | 250 | 6.25 | 42.7% | 2.67 | 0.91 |
| C | 5,000 | 115 | 1.875 | 42.5% | 0.80 | 0.78 |
| C | 40,000 | 34 | 15 | 44.6% | 6.69 | 0.91 |
| C | 200,000 | 29 | 75 | 41.2% | 30.9 | 0.90 |
| IN | 20 | 201 | 0.2 | 24.2% | 0.05 | 0.64 |
| IN | 200 | 124 | 2 | 17.4% | 0.35 | 0.57 |
| IN | 2,000 | 109 | 20 | 14.4% | 2.88 | 0.73 |
| IN | 20,000 | 24 | 200 | 12.1% | 24.2 | 0.96 |

Two facts are visible without a model and are therefore **not** claims of this study: (a) mean offers at comparable pie_days differ across populations by 20 pp or more (IN 17% at 2 days; SR 42% at 1.25 days; C 43% at 1.9 days), so the strong prediction "offers depend on the stake only through Lambda/Y" is already false at the level and is recorded here as falsified in advance; (b) acceptance rises with the stake in all three studies.

## 4. Models (fixed at freeze)

All responder models are binary logits for `accept`. Let `x` be the offer share, `m = offer_days` the offered amount in days of wages, `s ∈ {SR, C, IN}` the study.

- **M0 (share only, study intercepts and slopes):** `logit P(accept) = a_s + b_s * x`. This is the share-normalized model's responder side: no monetary variable.
- **M1 (shared monetary coordinate):** `logit P(accept) = a_s + b_s * x + g * log(1 + m)`. One coefficient `g` common to all studies. This is the one-finite-monetary-variance claim in logit form.
- **M1s (study-specific money):** `a_s + b_s * x + g_s * log(1 + m)`.
- **M2 (nominal stake added):** `M1 + h * log(pie_days)`. Tests whether the pie itself matters beyond the amount offered.
- **G (geometric responder):** the Part I responder encoding with the income-scaled coordinate: reference `r` = the responder's state after rejection, alternative `s(x)` = acceptance, with `Δa_1 = m / M` (M = 200, the largest pie_days in the data, so the coordinate lies in [0, 1]) and the non-monetary displacements of Part I's responder encoding (eris-econ 0.1.1, `targets._predict_responder_mao`), whose constants are copied verbatim into this section at freeze (Section 11, step 1); choice by softmax over {accept, reject} on cost `c = sqrt(Δa_1²/σ_1² + Δa_3²/σ_3²)` at fixed temperature `T` (Part II information-price rule; Part I's cost-dependent temperature is not used). Free parameters: `σ_1², σ_3², T`, shared across studies, plus a study intercept. `Δa_3` and the functional form are fixed here and will not be changed after freeze.

Proposer analysis: OLS of `percent_offer` on `log10(pie_days)` within each study, robust standard errors.

## 5. Registered predictions (frozen signs and thresholds)

- **P1 (money enters acceptance through the responder's own income units).** In M1, `g > 0`, and M1 improves on M0 by a likelihood-ratio test at α = 0.01.
- **P2 (one coordinate, not three).** M1s does not improve on M1: likelihood-ratio test of `g_SR = g_C = g_IN` is not rejected at α = 0.05, **and** the three `g_s` lie within a factor of 2 of each other (equivalence bound fixed here).
- **P3 (nominal stake adds nothing given m and x).** In M2, `h` is not significant at α = 0.05 and |h| < 0.25 per log10 unit.
- **P4 (leave-one-study-out).** Fit M1 on two studies, predict the third. Held-out log-loss of M1 is within 0.02 nats per decision of M1s fitted on the held-out study itself, for each of the three folds.
- **P5 (geometric responder matches the logit).** Model G attains held-out log-loss within 0.03 nats per decision of M1 on every fold, with `σ_1²` finite (upper bound 10⁴ on the unit-scaled coordinate).
- **P6 (the boundary is on the responder side).** Proposer slopes on `log10(pie_days)`: IN slope < −3 pp per decade (already known and recorded as prior); SR and C slopes within ±1.5 pp per decade (95% CI excludes ±3).

## 6. Falsifiers (pre-committed)

- P1 fails → money does not enter acceptance in income units; the income-scaled coordinate is not the boundary; the paper reports that the share-normalized responder model stands and the Andersen offer decline is unexplained by the coordinate.
- P2 fails (heterogeneous `g_s`) → no single monetary variance; the boundary is population-specific on both sides; the paper reports the three `g_s` and does not claim a shared coordinate.
- P3 fails → the pie matters beyond the offered amount; the coordinate must carry stake context (Part I's `d_9` reading), and the paper says so.
- P4 or P5 fails → the shared model does not transfer across countries; reported as a failed transfer.
- P6 fails in SR or C (a slope beyond ±3 pp per decade) → proposers also respond to the stake in those populations and the "responder side" conclusion is withdrawn.

The strong prediction "offers depend on the stake only through Lambda/Y" is not registered because Section 3 already shows it false at the level; the paper states this in its first results paragraph.

## 7. Analysis plan and what will be reported regardless of outcome

For every model: coefficients with 95% CIs, log-likelihood, AIC, BIC, held-out log-loss per fold, calibration plots of predicted against observed acceptance in ten offer_days bins per study. All six predictions are reported as pass or fail with the pre-set thresholds. Robustness (reported, not used to rescue a failure): `wealth` as a covariate in IN; SR excluded (pooled rounds); `m` in linear rather than log form.

## 8. Power (to be completed before freeze)

A bootstrap power script `power/power_boundary.py` will resample the 1,456 decisions under M1 with `g` at 0.5, 1.0, and 2.0 per log-day and report the power of P1 at α = 0.01 and the width of the equivalence test in P2. Freeze only if power for P1 at g = 0.5 exceeds 0.8; otherwise P1's α is left at 0.01 and the underpowered status is recorded.

## 9. Not claimed

Nothing here tests proposer beliefs, learning across rounds, or the origin of population reference points. The Cameron and Slonim–Roth data enter only through the bundled file; no additional data are collected.

## 10. Reporting

Venue: JEBO or Experimental Economics. Title form: "Where stake invariance breaks: locating the boundary of a geometric bargaining model on three high-stakes ultimatum datasets." Cites Slonim and Roth (1998), Cameron (1999), and Andersen et al. (2011) as the sources, and Part I for the model.

## 11. Freezing procedure

1. Complete Section 8 and fix the Part I responder encoding constants in Section 4 against `eris-econ` 0.1.1.
2. `sha256sum prereg-boundary-v1.md power/power_boundary.py` → `prereg-boundary-v1.sha256` (same JSON form as `prereg-dimensions-v1.sha256`).
3. Commit and push to the public repository; register the document and hash on OSF; record the OSF URL and the commit hash here in a final line, which is the only edit permitted after freezing.
4. Only then run any fit.
