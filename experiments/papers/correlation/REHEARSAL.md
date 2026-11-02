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
- **Every fitted model was worse than chance on the test trials.** Median held-out log-loss per trial
  was GEO 0.736, RDU 0.754 and CAG 0.916, against 0.693 for chance. Only EARLY did better (0.679),
  because it predicts even odds on block X.
- **The predictions were right in direction and wrong in size.** GEO's person-level predictions
  correlated with behaviour in block X (Spearman about 0.4). But kappa was overestimated (mean 1.37
  for a true 1), and because cost is raised to the power kappa, a small overestimate inflates the
  predicted differences on test trials far from the calibration region. A few near-certain wrong
  predictions dominate the mean.
- **The person-level test was not specific.** In the smoke test it also passed under RDU. Pessimism and
  kappa > 1 both show as risk aversion at the ideal, so GEO's fitted kappa tracks RDU's pessimism.

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

## Results

Pending. Version 2 runs on NRP (driver screen `corr-reh2`, outputs `nrp_reh_v2`).
