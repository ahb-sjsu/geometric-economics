# CPC18 fit-and-transfer — paired per-fold differences

Answers the Part II revision note at `part2_manuscript_revised.tex` L167: the
CPC18 comparison used seeds 0–19 shared across models but persisted only the
mean and sd of each model's held-out score, so no paired statement could be
made. `fit_transfer.py` now writes every fold and reports the paired contrasts.

Nothing about the protocol changed. Same data, same 70/30 split by `GameID`,
same n-weighted binomial NLL, same seeds. The headline table below reproduces
`RESULTS_cpc18.md` to the digit, so the re-run confirms the published numbers
rather than replacing them.

## Protocol

Unchanged from `RESULTS_cpc18.md`: CPC18 description choices (Trial 1), 270
games, 27,780 choices, 20 random 70/30 splits by `GameID`, 189 train and 81
test games per fold. Every model sees the identical fold, which is what makes
the differences pairable.

## Headline table (re-run 2026-09-10, identical to the published record)

| Model | #params | TEST MAE | TEST NLL |
|---|--:|--|--|
| constant (train B-rate) | 1 | 0.1991 ± 0.0115 | — |
| Expected Value (logit) | 1 | 0.1491 ± 0.0075 | 0.6442 ± 0.0105 |
| linear RUM (dEV, dSD, amb) | 4 | 0.1280 ± 0.0097 | 0.6322 ± 0.0125 |
| Geometric (Mahalanobis-from-ideal) | 4 | 0.1238 ± 0.0089 | 0.6286 ± 0.0114 |
| CPT (alpha,beta,lambda,gamma + T) | 5 | 0.1179 ± 0.0076 | 0.6237 ± 0.0113 |

## Paired per-fold differences

Negative favours the geometric model. `wins` counts folds in which the
geometric model scored lower. Confidence intervals are Student-t on the 20
paired differences; both a paired t-test and a Wilcoxon signed-rank test are
reported because n = 20.

| Contrast | Metric | Mean diff | 95% CI | t p | Wilcoxon p | Wins |
|---|---|--:|---|--:|--:|--:|
| Geometric − EV | MAE | −0.02531 | [−0.02839, −0.02224] | 4.6e−13 | 1.9e−06 | 20/20 |
| Geometric − EV | NLL | −0.01556 | [−0.01748, −0.01363] | 6.7e−13 | 1.9e−06 | 20/20 |
| Geometric − RUM | MAE | −0.00417 | [−0.00575, −0.00258] | 2.6e−05 | 3.6e−05 | 18/20 |
| Geometric − RUM | NLL | −0.00353 | [−0.00528, −0.00179] | 4.4e−04 | 1.9e−05 | 19/20 |
| Geometric − CPT | MAE | +0.00587 | [+0.00345, +0.00830] | 6.7e−05 | 1.3e−04 | 2/20 |
| Geometric − CPT | NLL | +0.00493 | [+0.00270, +0.00717] | 1.9e−04 | 5.9e−04 | 3/20 |

Paired on shared folds, so these test the per-fold difference and not the
difference of two independent means. No multiplicity correction is applied;
three contrasts on two metrics are reported together and should be read as one
family.

## Honest read

- **The "beats EV and RUM" claim survives pairing, and gets stronger.** Against
  Expected Value the geometric model wins every fold on both metrics. Against
  linear RUM it wins 18 of 20 folds on MAE and 19 of 20 on NLL, with the
  confidence interval clear of zero. The unpaired presentation understated
  this, because the fold-to-fold spread that dominates each model's sd is
  common to both models and cancels in the difference.

- **The gap to CPT is real, and the published wording understates it.**
  `RESULTS_cpc18.md` says the geometric model "comes within ~0.006 MAE (< 1 sd)
  of CPT". The 0.006 is right, but "< 1 sd" invites the reading that the two
  are statistically indistinguishable, and paired on shared folds they are not:
  CPT is better on 18 of 20 folds, the 95% interval on the difference excludes
  zero, and p ≈ 7e−05. The correct sentence is that CPT holds a small but
  consistent advantage on its home turf, roughly 0.006 MAE, with one more
  parameter. That is the same conclusion the paper already draws in prose; only
  the statistical hedge needs repair.

- **What this does not show.** These are held-out folds of one benchmark under
  one encoding. The two-outcome approximation caveat in `RESULTS_cpc18.md`
  still applies to every row, and it applies equally to all four models, so it
  is unlikely to drive a difference. Nothing here speaks to the cross-domain
  transfer claim, which is the geometric model's distinct one and is measured
  elsewhere.

## Files

- `results_cpc18_perfold.csv` — 100 rows, 20 folds × 5 models. Columns: `seed`,
  `model`, `n_params`, `MAE`, `NLL`, `n_train_games`, `n_test_games`,
  `n_test_choices`, `theta` (the fitted parameter vector as JSON).
- `fit_transfer.py` — writes the CSV and prints the paired table. The original
  summary table is unchanged and still printed first.

*Reproduce: `python fit_transfer.py` in this directory. Runtime about one
minute. The script is deterministic given seeds 0–19, and this record was
produced by two independent runs that agreed to the digit.*
