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
