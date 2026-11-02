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

## Results

Pending.
