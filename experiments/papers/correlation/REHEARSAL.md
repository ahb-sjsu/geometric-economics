# Rehearsal of the correlation-attitude design. Run record

Exploration on simulated people only. No human data exist for this design, and none were used.

## Setup (2026-11-02)

- **Stimuli.** `stimuli.py`, seed 20261102: 40 riskless pairs (R), 32 single-attribute lotteries (S),
  24 correlation pairs (X), 8 attention checks (A, unused here).
  - Calibration: R plus the S cells at the other attribute's ideal (48 trials).
  - Test: the rest of S plus X (48 trials).
- **Truths.** GEO1 and GEO2 (full metric, late contraction, kappa 1 and 2), EARLY (metric on the mean
  bundle), RDU (additive value, pessimistic weight on even odds), CAG (concave aggregator) and ADD
  (linear additive). Parameter ranges are in `rehearsal.py`.
  - Each simulated person's scale is set so that the median |logit| over R is about 1.5.
  - Each person gets a left bias drawn from N(0, 0.3).
- **Fitted models.** GEO, EARLY, RDU and CAG, each by maximum a posteriori per person on the
  calibration trials, with the weak fixed priors in `models.py`. Each predicts the test trials with
  no refit.
- **Scale.** 60 simulated studies of 200 people per truth. Tests are run on the first 60, 120 and 200
  people.
- **Where it ran.** NRP, one CPU Job per truth (`submit_nrp.py`), driver on Atlas in screen
  `corr-reh`, outputs in `/archive/experiments/correlation/nrp_reh`.
- **Smoke test on Atlas.** REHEARSAL_QUICK, 30 people, one study each.
  - Peak RSS 0.10 GiB, 99% of one CPU, about 0.2 s per simulated person.
  - GEO1 truth: GEO beat EARLY, RDU and CAG by 0.06, 0.14 and 0.05 nats per test trial. The
    correlated option was chosen 20 points above even, the predicted direction. Lottery choice fell
    11 points when the other attribute left its ideal.
  - RDU truth: GEO lost to RDU by 0.40, and the correlated option was chosen 29 points below even.
  - One small study each, so these numbers show the code runs, not the rates.

## Version 1 (no lapse, one fitting pass): the analysis failed its own truth

GEO1 truth, 60 studies of 200 people:
- **The model-free checks see the effects.** The correlated option was chosen 17 points above even, in
  every study. Lottery choice fell 6 points when the other attribute left its ideal, in 85% of studies
  at n = 60 and all at n = 120.
- **The model comparisons did not.** GEO beat EARLY in 7% of studies at n = 200, RDU in 48% and CAG in
  42%. The rate did not rise with n.
- **On average, the fitted models were worse than chance on the test trials.** Held-out log-loss per
  trial, averaged over studies, was GEO 0.736, RDU 0.754 and CAG 0.916, against 0.693 for chance.
  Only EARLY did better (0.679), because it predicts even odds on block X.
  - The median study was better than average (GEO 0.675, EARLY 0.663, RDU 0.746, CAG 0.738). A few
    studies with near-certain wrong predictions pull the average up.
  - *Correction, 2026-11-02:* an earlier version of this record called the averages medians.
- **The predictions were right in direction and wrong in size.** GEO's person-level predictions
  correlated with behaviour in block X (Spearman about 0.4). But kappa was overestimated (mean 1.37
  for a true 1), and because cost is raised to the power kappa, a small overestimate inflates the
  predicted differences on test trials far from the calibration region. A few near-certain wrong
  predictions dominate the mean.
- **The person-level test was not specific.** In the smoke test it also passed under RDU. Pessimism and
  kappa > 1 both show as risk aversion at the ideal, so GEO's fitted kappa tracks RDU's pessimism.
- **The complete run confirmed both failures.** All six truths are in `results/summary_v1.json`.
  - GEO beat EARLY in at most 45% of studies under any truth.
  - The non-comparative H4 passed in every study at n = 200 under RDU and CAG, as well as under
    GEO1 and GEO2.

## Version 2 (2026-11-02)

- Simulated people lapse at a rate drawn from U(0, 0.06).
- Every model chooses with a fixed 4% lapse, so no trial costs more than 3.9 nats.
- Every model is fit twice. The second pass uses an empirical-Bayes prior: the median and MAD of the
  first-pass estimates over the first 60 people.
- H4 is comparative. GEO's person-level predictions must track behaviour in block X better than RDU's
  and CAG's do, with a bootstrap interval.

Atlas smoke test, 2 studies of 30 people:
- **GEO1 truth.** Held-out log-loss was GEO 0.582, CAG 0.618, EARLY 0.619 and RDU 0.643. Recovery of
  the metric's correlation reached 0.74, and of its ratio 0.90. Kappa was 1.28 on average, still
  above the true 1. The H4 gap was +0.10.
- **RDU truth.** Held-out log-loss was RDU 0.553, GEO 0.565, CAG 0.569 and EARLY 0.636. The H4 gap was
  −0.11.
- In both truths the true model wins, and the second pass improves every model.

## Version 6 (2026-11-03): the table the new rules read

Version 5 found that the pilot's rules needed changing (PILOT.md). The five open rule decisions were taken
on 2026-11-03, before any data ("Decisions taken" there). This version computes what they need.

- **Cells.** 79, listed in `rehearsal.py` as `TABLE_V6`, 50 studies of 240 people each, tests on the first
  60, 120, 160, 200 and 240. 63 went out first; the last 16 are the target-0.7 rows below.
  - The 22 version 5 cells, rerun.
  - Rows at `κ` = 0.5 and 0.75 at noise targets 1.0, 1.5 and 2.0 (`G050`, `G075`), with the hierarchical
    `κ` on 10 studies each, to see how `hier.py` does near its floor of 0.5.
  - Rank-one shares of 20%, 40% and 60% (`S20`, `S40`, `S60`) at the six rows that reached 0.80 by
    n = 240 with nobody of rank one (`G100T10`, `G100T15`, `G100T20`, `G125T15`, `G125T20`, `G200T20`) and
    at the six new rows.
  - Added after the second pilot rehearsal (PILOT.md, sequence step 4): a noisier row, target 0.7, at every
    `κ` (`G050T07` to `G200T07`), with the three shares at `κ` up to 1. In up to 17% of simulated pilots the
    pilot's agreement fell below every target-1.0 row, and the rule then had no noise position. These 16
    cells ran with the same code; only `TABLE_V6`'s list grew afterwards.
- **Two populations per study.** The claim is scored over every simulated person, as DESIGN.md registers
  it, and over the people the main study's self-only flag does not catch: the self-favouring option in at
  least 15 of block R's 20 pairs at ratios 2 and 3 (`rehearsal.flagged`). For the second, people are
  recruited until there are n unflagged. The extra people come from their own random stream and use the
  study's prior, so nothing in the first population changes.
- **Stimuli version 5.** Only the eight attention checks moved (PILOT.md, inclusion rule). On Atlas, the
  140 trials of version 4 and version 5 differ in ids 112 to 119 alone, the order is identical, and so
  are the pilot-only trials. The digest is now `4abe1d59…` (version 4: `35a806ad…`). The rehearsal never
  reads the checks, and each simulated person draws one uniform number per trial whatever the trial
  holds, so no other simulated choice changes.
- **Checks on Atlas before launch.** `G100T15S40` and `G150T10` with REHEARSAL_QUICK under the version 5
  code and stimuli and under version 6: every claim and recovery record identical. `G050T15` and
  `G100T15S60` ran through the new path; a quick cell used 0.10 GiB.
- **Where it ran.** NRP, 79 one-CPU Jobs, at most 3 attempts each, from five drivers on Atlas (screens
  `corr-reh6a`, `-b1`, `-b2`, `-c` and `-e`, outputs `nrp_reh_v6`). Only the six rows below 1 ran `hier.py`.
- **Expected before the run.** Written while the jobs ran, before any result.
  - The 22 version 5 cells reproduce their version 5 pass counts exactly, over everyone.
  - With nobody of rank one, the claim over unflagged people passes about as often as over everyone,
    within a study or two of 50. The pilot's flag catches 0.6% to 2% of people who trade off, and
    recruitment refills to n.
  - With rank-one people, power over everyone falls with the share, as in version 5. Over unflagged people
    it stays near the share-0 row. It is lower where the flag misses more rank-one people (`κ = 2` and the
    noisy rows), since those it misses still dilute the mean.
  - The rows below 1 have at least the power of the `κ = 1` row at every target. Concave cost makes both
    terms of the cross-partial favour the correlated lottery (DESIGN.md), and makes the evaluator risk
    seeking at the ideal, which neither EARLY nor CAG (`ρ ≥ 1`) can produce. RDU with `η < 1` can, so H2
    is the comparison most at risk.
  - Specificity holds in both populations: at most 1 pass in 50 at every n.
  - The main study's flag catches fewer rank-one people than the pilot's, since it lacks the four ratio-6
    pairs, the clearest test of ignoring the charity.

### Results (2026-11-04)

The table is `results/power_table_v6.json` (sha256 `e160b1e1…`), built from the 79 cell files in
`results/rehearsal_v6/`, gzipped. Each file's sha256 before gzip is in the table's `inputs_sha256`. Figures
are percent of 50 studies passing the main claim at n = 120, at noise target 1.5 unless stated.

| `κ`, target 1.5 | share 0, everyone | share 0, unflagged | 0.2 | 0.4 | 0.6 (everyone / unflagged) |
|---|---|---|---|---|---|
| 0.5 | 100 | 100 | 98 / 100 | 98 / 100 | 88 / 98 |
| 0.75 | 100 | 100 | 94 / 98 | 86 / 100 | 44 / 98 |
| 1 | 96 | 96 | 88 / 100 | 58 / 90 | 10 / 96 |
| 1.25 | 72 | 76 | 58 / 84 | 18 / 62 | 2 / 70 |
| 1.5 | 40 | 38 | | 4 / 34 | |

- **With nobody of rank one, the two populations agree** within a few points (κ 2 at target 2.0: 72 and 72).
  Prediction held.
- **The rows below 1 have more power than `κ = 1` at every target.** At target 1.0: 100, 98 and 84 at `κ`
  of 0.5, 0.75 and 1; at target 0.7: 90, 68 and 20. Prediction held.
- **Target 0.7** has little power from `κ = 1` up: 20% at 1, 2% at 1.25, none above.
- **Rank-one people.** Over everyone, power collapses as the share grows. Over unflagged people it stays near
  the share-0 row, except where the flag misses many: at `κ = 2`, target 2.0, it is 72, 58, 52 and 40 at
  shares 0 to 0.6. Prediction held. On 2026-11-04 the owner chose the unflagged population for the main
  tests (PILOT.md), so the rule reads that column.
- **Specificity holds in both populations.** None of the five non-GEO cells passed in any study at any n.
  Prediction held.
- **The version 5 reruns did not reproduce exactly.** 17 of 22 cells did. G100T10, G125T10, G125T15 and
  G150T10 moved by one study of 50 at one n, and G125T20 by two. Prediction wrong. Every study's H
  estimates differ, typically in the sixth decimal (median 5×10⁻⁷, largest 7×10⁻³). On Atlas the old and
  new code gave identical records, so the likeliest cause is floating point differing between NRP nodes,
  which moves a study near the margin. That is not proven.
- **The main study's flag caught more rank-one people than the pilot's, not fewer.** In the cells, 70% to
  99.5% of rank-one people, and 0.7% to 4.2% of GEO people who trade off (0% to 5.6% under the other
  truths). The four ratio-6 pairs offer only 5 of one's own points, and rank-one people choose noisily
  there. Prediction wrong.
- **What restriction costs.** At a share of 0.6 a study needed 180 to 375 extra people to reach 240
  unflagged. Among unflagged people the rank-one share left was up to 30%, where the flag is weakest.
- **`hier.py` at 120 people below `κ = 1`.** At `κ = 0.75` its posterior medians were 0.72 to 0.76, and the
  95% interval covered the truth in 9 of 10 studies. At `κ = 0.5` it never covered: its population `κ` is
  0.5 + exp(·), so the truth sits on the boundary, and the medians were 0.59 to 0.63.
- **The rank-one check** (version 5's `n(1 − s)`) missed in most share cells, as in version 5.
- Cells took 21 to 217 minutes. No Job was lost.

## Version 5 (2026-11-03): the power table the pilot reads

- **Purpose.** The pilot puts the study in one row of a power table that is computed and sealed before
  the pilot runs (`PILOT.md`). This is that table.
- **Cells.** 22 cells, listed in `rehearsal.TABLE_V5`.
  - **GEO, 15 cells.** `κ` of 1, 1.25, 1.5, 1.75 or 2, crossed with a noise target of 1.0, 1.5 or 2.0. The
    target is the centre of each person's median `|logit|` over block R, so a higher target means a less
    noisy chooser. Everyone trades the two attributes off, as in GEO1 and GEO2.
  - **Rank one, 2 cells.** In `G100T15S40` and `G150T15S40`, 40% of people weigh only their own points.
  - **Specificity, 5 cells.** EARLY, RDU, CAG, ADD and IA drawn as in version 4, at target 2.0, with
    lapses drawn from U(0, 0.15).
- **Scale.** 50 studies of 240 people per cell. Tests run on the first 60, 120, 160, 200 and 240.
- **The rank-one people.**
  - Each is drawn as a person who trades off and is scaled to the noise target. Then the charity weight
    is removed (`P12 = P22 = 0`).
  - Their sensitivity to their own points is kept. So they are not perfectly consistent. They chose the
    self-favouring option in 36.6 of the 40 block R pairs on average under `G100T15S40`, and in 34.1
    under `G150T15S40`.
  - With convex cost (`κ > 1`) they sit at small costs, where choices are noisier.
- **Checks on Atlas before launch.**
  - The version 4 truths reproduce exactly under the version 5 code. GEO1, RDU and IA05 were run with
    REHEARSAL_QUICK under both versions, and the outputs were identical apart from run time and the
    version fields.
  - `stimuli.build()` is unchanged: identical to `stimuli_v4.json`.
  - A quick cell used 0.10 GiB and about 0.3 s per simulated person.
- **Where it ran.** NRP, 22 one-CPU Jobs, at most 3 attempts per cell. Driver screen `corr-reh5`, outputs
  `nrp_reh_v5`.
- **Expected before the run.** This was written while the jobs ran, before any result. The `n(1 − s)` rule
  for the rank-one share should overstate power.
  - The claim's test puts the margin on the mean over all n people.
  - Rank-one people pull that mean toward zero, since every model predicts them alike.
  - Under true dilution the margin would apply to the traders' mean alone. Mixing them in acts like a
    margin of `0.005 / (1 − s)`, 0.008 at `s = 0.4`.
  - The effect should show where power is not already near 100%, so at `κ = 1.5` more than at `κ = 1`.

### Results (complete 2026-11-03)

- **Run.**
  - Every cell finished at its first attempt except G150T15. Its Job failed and lost its pod, and the
    driver then crashed trying to read the missing log.
  - The fix is in `submit_nrp.py`: a finished Job whose pod is gone counts as lost and is resubmitted.
  - G150T15 finished at its second attempt, under a second driver (`corr-reh5b`).
  - Cells took 43 to 132 minutes on one NRP CPU.
- **Files.** `results/rehearsal_v5_<CELL>.json`, and `results/power_table_v5.json` from `power_table.py`.

**The main claim (H1, H2 and H3 at margin 0.005).** Percent of 50 studies passing at n = 60 / 120 /
160 / 200 / 240. A higher noise target means a less noisy chooser.

| `κ` | Target 1.0 | Target 1.5 | Target 2.0 |
|---|---|---|---|
| 1 | 62 / 86 / 90 / 92 / 96 | 84 / 96 / 98 / 98 / 100 | 84 / 90 / 96 / 98 / 100 |
| 1.25 | 24 / 38 / 40 / 56 / 66 | 52 / 74 / 80 / 84 / 88 | 70 / 80 / 90 / 92 / 94 |
| 1.5 | 8 / 14 / 16 / 16 / 20 | 32 / 40 / 42 / 48 / 56 | 38 / 66 / 68 / 64 / 72 |
| 1.75 | 4 / 2 / 6 / 4 / 2 | 20 / 30 / 30 / 40 / 44 | 18 / 38 / 52 / 66 / 72 |
| 2 | 4 / 8 / 12 / 16 / 14 | 18 / 40 / 46 / 56 / 58 | 26 / 72 / 78 / 86 / 96 |

- **Precision.** With 50 studies per cell, a rate near 80% is known to about ±12 points. The table file
  gives 95% Wilson intervals.
- **The rerun cells agree with version 4** at n = 60 / 120 / 200:
  - G100T15 (GEO1) gave 84 / 96 / 98, against 84 / 94 / 100;
  - G200T15 (GEO2) gave 18 / 40 / 56, against 20 / 34 / 52.
- **Power falls fast with `κ` and with noise.**
  - At n = 120 and target 1.5 it is 96% at `κ = 1`, 74% at 1.25, 40% at 1.5, 30% at 1.75 and 40% at 2.
  - At target 1.0 and n = 120 it is under 40% for every `κ` above 1.
- **Power is not monotone in `κ`.** It is lowest around `κ` of 1.5 to 1.75, and recovers at `κ = 2` when
  choices are less noisy: at target 2.0 and n = 120 it is 66% at 1.5, 38% at 1.75 and 72% at 2.
  - H1 (GEO against EARLY) drives this. Medians over studies at n = 240:
    - on block X, GEO's held-out advantage over EARLY falls from 0.03 to 0.09 nats per trial at
      `κ = 1` to between −0.01 and 0.02 at `κ` of 1.75 and 2;
    - on block S, its advantage grows with `κ`, from 0.01 to 0.04 at `κ = 1` to 0.02 to 0.06 at
      `κ = 2`.
  - So the pilot's `κ` rule, which rounds up to the next row as the cautious choice, is not always
    cautious (PILOT.md).
- **Specificity holds.**
  - Under EARLY, RDU, CAG, ADD and IA at target 2.0, with lapses up to 0.15, the claim passed in no
    study at any n.
  - The secondary claim (SH1 and SH2) passed in every IA study and in no study of any other cell.
- **The rank-one check misses, in the direction predicted before the run.**
  - G100T15S40 passed in 58 / 66 / 74 / 80% at n = 120 / 160 / 200 / 240. The `n(1 − s)` rule predicts
    86 / 91 / 96 / 97% from G100T15. The misses are 2.8 to 3.5 standard errors.
  - G150T15S40 passed in 4 / 6 / 6 / 8% at the same n, against 34 / 37 / 40 / 41% predicted from
    G150T15. The misses are 4.3 to 5.1 standard errors.
  - The miss is larger at `κ = 1.5` than at `κ = 1`, as predicted. In absolute points it is 30 at
    `κ = 1.5` against 28 at `κ = 1` at n = 120, and 33 against 17 at n = 240. Relative to the predicted
    power it is far larger.
  - By PILOT.md's rule, `s` becomes a dimension of the table before the seal.

## Version 4 (complete 2026-11-02): the crossing set

- **Stimuli.** `stimuli.py` version 4 adds the crossing set: 8 crossing correlation pairs and 12
  straddle lotteries, role "secondary". The 120 main trials are identical to version 3 apart from
  presentation order; checked on the generated sets.
- **Truths and models.** IA, inequality aversion between self and charity (`models.v_ia`), is both a
  new truth (`γ` drawn from U(0.1, 0.6)) and a new fitted model.
- **Analysis.** The main tests are unchanged and never see the crossing set. The secondary tests SH1,
  SH2, SH3 and SH3_did are computed on the crossing set (`DESIGN.md`).
- **The hierarchical fit is off** (`--hier-sims 0`). Version 3 already checked it.
- **Atlas smoke test** (2 studies of 30 people):
  - Under IA the main claim failed, as it should.
  - SH2 (−0.25 against GEO's prediction) and SH3 (+0.24) passed in both studies, and SH1 in one.
  - Under GEO1, SH1 and SH2 stayed quiet.
  - **But the plain SH3 passed in both GEO1 studies (+0.08).** GEO's calibration bias under-predicts
    correlation seeking far from the calibration region. SH3_did passed in one of the two (+0.04).
- **Where it ran.** NRP, driver screen `corr-reh4`, outputs `nrp_reh_v4`, 7 truths of 50 studies of 200
  people each. Every truth finished at the first attempt, in 22 to 93 minutes.
- **Files.**
  - Per truth: `results/rehearsal_v4_<TRUTH>.json`.
  - Summary: `results/summary_v4.json`.

### Results

Percent of studies passing at n = 60 / 120 / 200.

| Truth | Main claim (margin 0.005) | SH1 and SH2 (secondary claim) | SH1 or SH2 |
|---|---|---|---|
| GEO1 | 84 / 94 / 100 | 0 / 0 / 0 | 2 / 0 / 0 |
| GEO2 | 20 / 34 / 52 | 0 / 0 / 0 | 6 / 8 / 10 |
| EARLY | 0 / 0 / 0 | 0 / 0 / 0 | 8 / 10 / 12 |
| RDU | 0 / 0 / 0 | 0 / 0 / 0 | 4 / 0 / 0 |
| CAG | 0 / 0 / 0 | 0 / 0 / 0 | 4 / 4 / 0 |
| ADD | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 2 / 0 |
| IA | 0 / 0 / 0 | 100 / 100 / 100 | 100 / 100 / 100 |

- **The main claim stays specific with the crossing set and IA as a truth.** It passed in no study
  under the five truths without the metric. Under GEO1 it reproduced version 3.
- **The secondary claim is SH1 and SH2 together.** It detected IA in every study at every n and passed
  under no other truth. Alone, SH1 or SH2 passed in up to 12% of studies without IA, mostly SH2
  under EARLY and GEO2.
- **SH3 is not specific in either form.**
  - The plain form passed in 28 / 44 / 58% under GEO1 and in 90 / 100 / 100% under ADD.
  - The difference-in-differences form passed in 14 / 8 / 18% under GEO1, 22 / 40 / 66% under ADD and
    10% under RDU.
  - GEO's zero-fit prediction for the crossing pairs, far from the calibration region, is biased by
    the fitted `κ`, and the bias differs between the crossing and main pairs. SH3 is reported only.
- **SH1r, GEO beating IA on the crossing set,** passed in 82 / 94 / 98% under GEO1 and 56 / 76 / 88%
  under GEO2. When the metric is true it accounts for the crossing set better than inequality
  aversion does.
- **The IA truth is a strong one** (`γ` from 0.1 to 0.6). Weaker aversion was rehearsed next, below.

### Weaker inequality aversion (2026-11-02)

- **Setup.** Four more truths with `γ` fixed at 0.02, 0.05, 0.10 and 0.20 (`IA02` to `IA20` in
  `rehearsal.py`, commit `75bbdfc`). There were 50 studies of 200 people each.
  - `γ` is the penalty for each unit of `|self shortfall − charity shortfall|`, in units of the
    marginal value of the participant's own points. So 0.10 means a point of inequality costs a tenth
    of a point of the participant's own money.
  - For scale, Fehr and Schmidt's two-person money-game estimates (`α ≈ 0.85`, `β ≈ 0.3`) correspond
    to `γ ≈ 0.6`.
- **Run.** NRP, driver screen `corr-reh4w`, every truth at the first attempt, 38 to 67 minutes.
- **Files.** `results/rehearsal_v4_IA02.json` to `IA20.json`, and `results/summary_v4_weak_ia.json`.

**Power of the secondary claim (SH1 and SH2 together).** Percent of studies passing at n = 60 / 120 /
200.

| `γ` | SH1 and SH2 | SH1 | SH2 | Main claim |
|---|---|---|---|---|
| 0.02 | 0 / 0 / 0 | 4 / 2 / 4 | 8 / 14 / 22 | 0 / 0 / 0 |
| 0.05 | 4 / 26 / 64 | 32 / 50 / 72 | 14 / 46 / 78 | 0 / 0 / 0 |
| 0.10 | 88 / 98 / 100 | 96 / 100 / 100 | 90 / 98 / 100 | 0 / 0 / 0 |
| 0.20 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 | 0 / 0 / 0 |
| 0.1 to 0.6 (version 4 IA) | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 | 0 / 0 / 0 |

- **At the planned n = 120, the secondary claim detects `γ` of 0.10 or more** (98%). It mostly misses
  0.05 (26%) and cannot see 0.02.
  - In the money-game scale above, it detects inequality aversion toward a charity if it is at least
    about a sixth as strong as aversion toward another person.
  - A null on the secondary claim therefore rules out strong inequality aversion toward the charity,
    not weak.
- **The main claim passed in no study under any of these truths.** Weak inequality aversion does not
  leak into it either.

## Version 3 (complete 2026-11-02)

- **Stimuli.** `stimuli.py` version 3: 12 calibration lotteries per attribute at the ideal instead of
  4, 120 trials in all.
- **The population `κ`.** The first 10 studies of each truth also get it, from their first 120
  people, by a hierarchical GEO sampled with NUTS (`hier.py`, NumPyro 0.22.0 on JAX 0.12.0.1, one
  chain of 500 warm-up and 500 draws).
- **Analysis.** Otherwise the analysis is version 2's.
- **First check on Atlas, one simulated study of 120 people per truth.**

| Truth | Population median `κ`, posterior median [95% interval] | Divergences | Run time |
|---|---|---|---|
| GEO1 (true 1) | 0.96 [0.86, 1.06] | 0 | 400 s |
| GEO2 (true 2) | 1.91 [1.75, 2.09] | 0 | 290 s |

  - The per-person bias does not appear, and each interval excludes the other truth.
  - Peak memory was 0.57 GiB.
- **Where it runs.** NRP, driver screen `corr-reh3`, outputs `nrp_reh_v3`, at cpu 1 and memory 2Gi
  (the exempt maximum).

### Two faults found during the run, both fixed

- **`hier.py` failed on NRP.** Every first attempt failed in NumPyro's initialization with an invalid
  Bernoulli probability. At an extreme draw `κ` reaches the tens, `C^κ` overflows to infinity, and
  `inf − inf` or `0 · inf` (the zero-probability outcome of a sure option) is NaN.
  - The overflow is platform-dependent. On Atlas the old code ran on the same data.
  - The fix (commit `7dc62b2`) computes `C^κ` in log space, capped at `exp(60)`. It clips the logit,
    turns off argument validation, and starts the chain at the hyperprior centre.
  - On the failing study's data, run on Atlas, the old and fixed code give the same posterior:
    1.784 [1.655, 1.925] against 1.786 [1.661, 1.930].
  - All six truths' version 3 results come from the fixed code. The retries used it. RDU and GEO2,
    parked after two old-code attempts, were rerun in their own drivers (`corr-reh3b`, `corr-reh3c`).
- **MF2 compared different gambles.** Version 3 has 12 lotteries per attribute at the ideal but 4 per
  level off it. The background check compares choice rates at and off the ideal, so it compared
  different gambles.
  - The fix (commit `66a2ce0`) uses only the 4 lotteries offered at every level.
  - `mf2_check.py` reran MF2 on 200 fresh studies per truth (`results/mf2_check.json`). Percent of
    studies passing at n = 60 / 120 / 200:

| Truth | Matched (corrected) | Unmatched (as version 3 ran) |
|---|---|---|
| GEO1, which has background dependence | 77 / 94 / 99 | 93 / 99 / 100 |
| CAG, which has background dependence | 8 / 20 / 24 | 4 / 3 / 3 |
| GEO2 | 8 / 4 / 4 | 34 / 58 / 81 |
| EARLY | 7 / 6 / 10 | 10 / 7 / 7 |
| RDU | 6 / 6 / 6 | 18 / 28 / 55 |
| ADD | 4 / 5 / 6 | 9 / 6 / 6 |

  - The MF2 figures in the version 3 NRP outputs are the unmatched check and should not be read.

### Results (all six truths)

- **Scale.** 50 studies of 200 people per truth, as in version 2.
- **Files.**
  - Per truth: `results/rehearsal_v3_<TRUTH>.json`.
  - Summary: `results/summary_v3.json`.
- **Runtime.** 23 to 214 minutes per truth on one NRP CPU.
- **Code.** All six truths ran the fixed `hier.py`.

**The claim: H1, H2 and H3 together.** Percent of studies passing at n = 60 / 120 / 200.

| Truth | Margin 0 | Margin 0.005 | Version 2, margin 0 |
|---|---|---|---|
| GEO1, distance | 96 / 100 / 100 | 84 / 98 / 100 | 70 / 92 / 96 |
| GEO2, squared distance | 32 / 48 / 68 | 16 / 30 / 46 | 36 / 28 / 42 |
| EARLY | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| RDU | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| CAG | 2 / 2 / 2 (one study) | 0 / 0 / 0 | 0 / 0 / 0 |
| ADD | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |

- **CAG's false positive is H3, GEO beating the true CAG in one study.** At margin 0.005 it does not
  pass.
- **H4 (comparative).**
  - GEO1: 30 / 60 / 80.
  - GEO2: 54 / 74 / 90.
  - ADD, RDU and EARLY: 0.
  - CAG: 4 / 0 / 2.
- **Held-out log-loss at n = 200, median over studies.** The true model is best, or tied with GEO
  under CAG (0.502 against 0.500). Under GEO1, GEO scored 0.579 against 0.620 to 0.627 for the
  others.
- **Per-person `κ` under GEO1.** It averaged 1.21, against 1.30 in version 2.
- **The population `κ` (hierarchical, 10 studies per truth).**

| Truth | Median | Interval excludes 1 | Interval excludes 2 | Covers the truth |
|---|---|---|---|---|
| GEO1 | 0.95 | 1 of 10 | 10 of 10 | 9 of 10 |
| ADD | 0.96 | 1 of 10 | 10 of 10 | (none defined) |
| RDU | 1.64 | 10 of 10 | 10 of 10 | (none defined) |
| CAG | 1.86 | 10 of 10 | 5 of 10 | (none defined) |
| GEO2 | 1.93 | 10 of 10 | 3 of 10 | 7 of 10 |
| EARLY | 1.13 | 9 of 10 | 10 of 10 | (none defined) |

  - **Coverage is defined only under the GEO truths.**
    - EARLY is not GEO. Its `κ`, drawn from 1 to 2, shapes only riskless choices, and its lotteries
      are risk-neutral, so GEO's fitted `κ` has no reason to equal it.
    - Version 3 ran with EARLY's "true" `κ` set to 1.5, the median of its draws. Against that, the
      coverage was 0 of 10, which means nothing.
    - *Correction, 2026-11-02:* `rehearsal.py` now sets EARLY to none, and `aggregate_rehearsal.py`
      reports coverage for GEO truths only.

- **Readings.**
  - **The extra calibration lotteries raised the power substantially for distance-like cost.** At
    n = 120 the claim now passes in 100% of studies at margin 0 and 98% at 0.005, against 92% in
    version 2. They did little for squared distance.
  - **The margin decides one false positive.**
    - At margin 0, the claim passed in 1 of the 200 studies per n under truths without the metric
      (four truths, 50 studies each). Each time it was a CAG study: study 35 at n = 60, and study 41
      at n = 120 and 200.
    - At 0.005 it passed in none.
    - The cost at n = 120 is 2 points of power for distance-like cost (100% to 98%) and 18 for
      squared distance (48% to 30%).
    - The owner chose 0.005 (2026-11-02). It keeps the claim free of false positives in these
      studies, with 98% power for distance-like cost at n = 120.
  - **The population `κ` means something only if GEO is the right model.** Under RDU and CAG the
    misspecified GEO absorbs pessimism or the aggregator's concavity into `κ`. So a null on the claim
    with a high `κ` cannot tell squared distance from either. The H2 and H3 comparisons, and MF1's
    sign, have to carry that distinction.
  - **The interval tells distance from squared distance when GEO is true.**
    - Under GEO1 it excluded 2 in 10 of 10 studies and covered 1 in 9.
    - Under GEO2 it excluded 1 in 10 of 10 but covered 2 in only 7. The GEO2 intervals may be too
      narrow. The hierarchical model's normal population distributions do not match the uniform ones
      the simulated people come from, and the lapse differs. Ten studies per truth are too few to be
      sure.

## Results (version 2, complete 2026-11-02)

- **Scale.** 50 simulated studies of 200 people per truth, with tests on the first 60, 120 and 200.
- **Runtime.** Each truth ran on one NRP CPU and took between 37 and 112 minutes.
- **Files.**
  - Per truth: `results/rehearsal_v2_<TRUTH>.json`.
  - Summary: `results/summary_v2.json`.
  - Version 1 summary: `results/summary_v1.json`.

**The registered claim: H1, H2 and H3 together.** Share of studies in which it passed.

| Truth | n = 60 | 120 | 200 |
|---|---|---|---|
| GEO1, distance (`κ = 1`) | 70% | 92% | 96% |
| GEO2, squared distance (`κ = 2`) | 36% | 28% | 42% |
| EARLY | 0 | 0 | 0 |
| RDU | 0 | 0 | 0 |
| CAG | 0 | 0 | 0 |
| ADD | 0 | 0 | 0 |

**Each test alone.** Percent of studies passing at margin 0, at n = 60 / 120 / 200. For the
model-free checks the median estimate is in brackets.

| Truth | H1 vs EARLY | H2 vs RDU | H3 vs CAG | H4 comparative | MF1 correlation | MF2 background |
|---|---|---|---|---|---|---|
| GEO1 | 82/94/98 | 82/94/98 | 88/96/96 | 20/36/58 | 100/100/100 (+0.17) | 72/100/100 (−0.05) |
| GEO2 | 38/32/42 | 78/90/98 | 80/88/100 | 40/72/86 | 2/6/2 | 4/4/8 |
| EARLY | 0/0/0 | 54/74/82 | 0/0/0 | 0/0/0 | 2/6/4 | 2/6/4 |
| RDU | 98/100/100 | 2/2/2 | 4/2/4 | 0/0/0 | 100/100/100 (−0.24) | 12/10/10 |
| CAG | 100/100/100 | 100/100/100 | 0/0/0 | 0/0/0 | 100/100/100 (−0.28) | 10/14/28 (+0.02) |
| ADD | 0/0/0 | 50/62/66 | 48/58/60 | 0/0/0 | 12/8/4 | 6/14/4 |

### Reading

- **The claim is specific.** It passed in none of the 600 simulated studies under truths without the
  metric (four truths, three values of n, 50 studies each). Each of H1, H2 and H3 passes under some
  false truth when taken alone, which is why the claim needs all three.
- **The power depends on the kind of cost.**
  - With distance-like cost, 120 people give 92% and 200 give 96%.
  - With squared distance it never passed in more than 42% of studies at any n tried.
- **H4 adds no specificity and costs power.** Adding it to the claim would cut power under GEO1 to
  20%, 36% and 56%, and it removes no false positive, because there were none.
- **The model-free checks behave as intended.**
  - The correlation check (MF1) finds an attitude whenever the population leans one way: seeking
    under GEO1, aversion under RDU and CAG. It finds nothing under GEO2, whose sign varies across
    people. Under truths with no attitude it passed in 2% to 12% of studies, so the false-positive
    rate reached 12% (ADD at n = 60).
  - The background check (MF2) finds GEO1's shift. CAG shows a weak shift in the opposite direction.
    Its false-positive rate was 2% to 14%.
- **The true model has the best held-out log-loss in every truth.** At n = 200, median over studies:
  - GEO1: GEO 0.591, against 0.631 to 0.639 for the others.
  - GEO2: GEO 0.621.
  - EARLY: EARLY 0.620.
  - RDU: RDU 0.562.
  - CAG: CAG 0.508, with GEO close behind at 0.511.
  - ADD: EARLY 0.588. ADD has no fitted model of its own, and EARLY contains it.
  - The second fitting pass improved every model under every truth. Under GEO1, for example, GEO
    went from 0.658 to 0.591.
- **Recovery under the GEO truths.**
  - The metric's correlation is recovered at 0.68 (GEO1) and 0.72 (GEO2).
  - Its log ratio is recovered at 0.89 and 0.90.
  - Each person's predicted preference for the correlated option correlates with the true one at
    0.56 and 0.69.
  - `κ` is recovered at 1.92 for a true 2. It is biased upward for a true 1 (1.30). The diagnosis
    is below.
  - Under the EARLY truth, whose `κ` is drawn from 1 to 2 (mean 1.5), GEO's fitted `κ` averages
    1.40 and does not track the individual values (correlation 0.06). *Correction, 2026-11-02:* an
    earlier line called this high, but it sits near the truth's mean.

### Open before sealing

- **The upward bias in `κ`: diagnosed, not yet fixed.** It does not break the claim's specificity.
  Its source is a small-sample bias of the estimator: `κ` is not only a curvature but also a carrier
  of sensitivity. Costs here are mostly above 1, so raising `κ` enlarges every utility difference.
  When a person's few choices are very consistent, the fit wants more sensitivity, the classic
  small-sample inflation of logit coefficients, and part of it flows into `κ`.
  - **Evidence** (`diag_kappa.py`, GEO1 truth, 300 simulated people per configuration;
    `results/diag_kappa_round1.json` and `round2.json`). Round 1 ran an earlier version of the
    script with a different configuration order, so the committed version does not reproduce its
    seeds exactly. It does reproduce round 2.
    - With the true metric known and `κ` fitted alone, the median `κ` was 1.63 from 8 lottery
      choices, 1.02 from 40 and 1.00 from 160.
    - The full fit fell from 1.38 (mean) with 48 choices to 1.16 with every trial answered five
      times.
    - It did not move with the prior (1.31 with the prior centred at 1, 1.57 with no prior), nor
      with the lapse (1.42 with no simulated lapse, 1.17 with the lapse matched exactly at 240
      choices).
    - It grew with sharper choosers (1.61 at three times the sensitivity), as separation makes it.
  - **The rehearsal's second pass cannot remove it.** It re-centres every person on the median of
    first-pass estimates, which share the bias.
  - **Fixes tried, 2026-11-02.** True `κ` = 1 throughout. Files: `results/diag_kappa_round3.json` and
    `round4.json` (version 2 stimuli, as in git history before this change) and `v3stim.json`
    (version 3 stimuli).
    - **Option 1, a pooled `κ` as the centre of the second-pass prior.** The profile maximum over 60
      people, with each person's other parameters re-fitted, was itself biased: 1.41. This is the
      incidental-parameter problem. With only 48 choices per person, maximizing over each person's
      nuisance parameters favours larger `κ`, however many people are pooled. Per-person estimates
      came out at 1.34, no better than the plain second pass (1.26).
    - **Option 1 with the nuisance parameters integrated out** (a Laplace approximation). The pooled
      centre was erratic: 0.68, 0.94 and 0.86 in three configurations. Per-person estimates landed at
      1.00 in one configuration only because a low centre cancelled an upward per-person pull. With
      sharper choosers they were 1.31. Option 1 is not adopted. `models.pooled_center` keeps both
      versions for the record.
    - **Option 2, more calibration lotteries.** `stimuli.py` version 3 has 12 lotteries per
      attribute at the ideal instead of 4, adding 16 trials (about 3 minutes).
      - The second pass fell from 1.26 to 1.19 (first pass 1.38 to 1.30).
      - Sharper choosers fell from 1.50 to 1.46.
      - Repeating the original 8 cells three times did better (1.15), so the new distinct cells carry
        less information about `κ` than repeats of the original ones.
    - **The bias decays slowly with session length.** In round 2, 240 calibration choices per person
      still left the first pass at 1.16. A per-person `κ` cannot be estimated without upward bias at
      any feasible session length.
  - **Still open.** Whether to keep version 3's extra lotteries. That needs a rehearsal rerun to
    check that power and specificity hold with the new set. The other open question is how to
    estimate the population `κ`, whether cost is distance-like or squared, without this bias. A
    hierarchical model fitted by full marginal likelihood (MCMC) is the standard route.
- **The crossing set is not built.** The secondary test of inequality aversion has neither stimuli
  nor rehearsal.
- **The parameter ranges are assumptions.** The scale target, the lapse range and the shape ranges
  were chosen, not measured. A pilot with people would check them.
- **N.** 120 gives 92% power if the cost behaves like distance.
