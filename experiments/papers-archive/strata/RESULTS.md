# prereg-strata-v1. Run record

**Run 2026-10-30 on Atlas**, after the registration commit `3b69bae` and signed tag `prereg-strata-v1`
were on public `main`. The seal was verified intact before and after the run
(`results/seal_check_after_run.txt`). No fit was void: every frozen model converged, and the consumer
arm passed its budget-recovery check (V4). Outputs as executed: `results/results_strata_real.json`
(sha256 `bb2f43b0…`), `results/graded_strata_real.json` (sha256 `28c95064…`), `results/run_real.log`.

Data: five corpora, 68,826 choices, every model frozen on CPC18 and carried over unchanged. On each
corpus the problems are split in half. The calibration half sets one scale per model, and for CPT the
payoff coding. The test half scores.

| Corpus | Choices | Problems (cal / test) | Participants | CPT coding chosen |
|---|---|---|---|---|
| Glöckner and Pachur 2012 | 12,160 | 80 / 81 | 64 | money unit |
| Pachur et al. 2017 | 10,370 | 42 / 43 | 122 | stake share |
| Pachur et al. 2018, Exp. 2 | 6,200 | 25 / 26 | 120 | stake share |
| Zilker et al. 2020 | 28,976 | 56 / 56 | 318 | stake share |
| Babula 2018 | 11,120 | 80 / 80 | 70 | stake share |

## Verdicts

One prediction passes, the weak one. Each stands alone. Pooled differences weight the five corpora
equally. The pooled margin is 0.0009 nats per choice.

| | Prediction | Verdict | Numbers (test log-loss difference per choice, nats) |
|---|---|---|---|
| H1 | Stratified beats two-number, pooled and in at least 3 corpora | **FAIL** | GDT-S minus GDT-2 −0.0202 [−0.0377, −0.0061]; clears the margin in 2 corpora |
| H2 | At least half the gap to CPT closes | **FAIL** | point 0.52 (bar 0.5), interval [0.22, 0.70], lower bound below the 0.25 floor |
| H3 | Stratified beats CPT, pooled | **FAIL** | GDT-S minus CPT +0.0185 [+0.0135, +0.0239]; 0 corpora |
| H4 | People move with stake less than GDT-2 predicts | **PASS** | +0.088 [+0.007, +0.166], 6 stake groups, all in Pachur 2018 |
| H5 | Stratified reproduces at least 4 of 6 effects, and more than GDT-2 | **FAIL** | 2 against 3 (decided at freezing) |
| H6 | Consumer beats stratified | **NOT ASSESSABLE** | V5: the arms differ by 0.0019 in mean choice probability; consumer minus stratified −0.00005 nats |
| H7 | Distortion shifts as the frozen geometry predicts from stimuli | **FAIL** | opposite sign in 4 of 5 corpora |
| H8 | Consumer reproduces the rare-event effects | **FAIL** | decided at freezing |

Test log-loss per choice:

| Corpus | Constant | EV | RUM | GDT-2 | GDT-S | GDT-C | CPT |
|---|---|---|---|---|---|---|---|
| Glöckner and Pachur 2012 | 0.6928 | 0.6039 | 0.5812 | 0.5787 | 0.6019 | 0.6016 | **0.5663** |
| Pachur et al. 2017 | 0.7060 | 0.6991 | 0.6913 | 0.6952 | 0.6495 | 0.6495 | **0.6369** |
| Pachur et al. 2018 | 0.6741 | 0.5800 | 0.5959 | 0.5904 | 0.5534 | 0.5538 | **0.5336** |
| Zilker et al. 2020 | 0.6936 | 0.5363 | 0.5329 | 0.5359 | 0.5238 | 0.5233 | **0.5019** |
| Babula 2018 | 0.6616 | 0.6259 | 0.6305 | 0.6310 | 0.6015 | 0.6018 | **0.5990** |

## The reading

**The stratified encoding is a real improvement on Part II's two numbers, but not a clean one.** Pooled,
it beats GDT-2 by 0.020 nats per choice with an interval clear of the margin. Its point estimate is
better in four corpora. It is worse on Glöckner and Pachur 2012 (0.602 against 0.579), the one corpus
where CPT also preferred the money unit to the stake share. Per corpus, the interval clears the margin
in only two, and H1 required three. The record stores the count, not which two.

**CPT is best on every corpus.** Frozen GDT-S closes about half the distance from GDT-2 to CPT, which
misses H2 only on the lower bound of its interval. GDT-2 again does not separate from expected value
(−0.0028 [−0.0087, +0.0033]), repeating `prereg-psych101-v1` on new data.

**The share coding is supported, from two sides.** H4 passes: across the six stake groups, people move
with stake less than the money-unit model GDT-2 predicts. In the rehearsal H4 failed when CPT in the
money unit was the truth. And on its calibration half, CPT itself chose the stake share in four of the
five corpora. The interval on H4 is wide and all six groups come from one corpus.

**H7 fails in the wrong direction, and this is the main finding.** γ is the CPT weighting exponent:
1 reads probabilities linearly, lower is a stronger inverse-S. CPC18 gives 0.89 observed and 0.90
predicted by the frozen geometric model. On the new corpora the frozen geometry predicts γ between 0.99
and 1.06, almost linear, everywhere. People's γ refit on each calibration half:

| Corpus | Predicted shift from CPC18 | Observed γ | Observed shift |
|---|---|---|---|
| Glöckner and Pachur 2012 | +0.09 | 0.72 | −0.17 |
| Pachur et al. 2017 | +0.15 | 0.71 | −0.17 |
| Pachur et al. 2018 | +0.11 | 0.81 | −0.08 |
| Zilker et al. 2020 | +0.16 | 0.66 | −0.23 |
| Babula 2018 | +0.10 | 1.02 | +0.13 |

The stratified coordinates take probabilities only through expectations (g = Σ p·x⁺, l = Σ p·x⁻) and the
two strata masses π⁺, π⁻, all linear in p. Nothing in the frozen model can bend a probability. The
consumer arm could, by regressing noisy readings toward its prior, but CPC18 set its budget to 15 bits,
so it reads probabilities exactly. People in four of these five corpora weight probabilities more
nonlinearly than CPC18's people did. The missing piece is probability weighting.

## Notes on the record

- **Babula 2018 margin.** The margin is 1% of expected value's calibration gain over the constant. On
  Babula's calibration half expected value was very slightly worse than the constant, so its per-corpus
  margin is −0.00002, a slightly lenient bar. It enters only the per-corpus win counts and the pooled
  margin (mean 0.0009 over five corpora; the other four alone average 0.0012). The record does not keep
  per-corpus intervals, so whether Babula's lenient bar decided one of H1's two wins is not recoverable
  from it. Either way H1 fails, since it would need a third.
- **H5, H6 and H8** were fixed by the frozen parameters and stimuli alone, and recorded in the
  registration before any choice was read.
- **Part II's CPT.** This registration uses the standard rank- and sign-dependent CPT. Part II's
  `fit_transfer._cpt_value`, used as registered in `prereg-psych101-v1`, misplaces the weights on
  losses and mixed gambles. That is a caveat on the psych101 comparison, not on this one.

## What this does not settle

These five corpora are now spent for confirmation. Any model revised in response to this result, such
as a geometric reader of probabilities, must be tested on corpora not used here, or the test would be
in-sample.
