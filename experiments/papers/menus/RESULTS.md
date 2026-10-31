# prereg-menus-v1. Run record

**Run 2026-10-31 on Atlas**, after the registration commit `03fc3a7` and signed tag `prereg-menus-v1`
were on public `main`. Before the run, the seal was verified on the Atlas copy of the bundle and the
row accounting was confirmed identical to the sealed one. After the run, the seal was intact again
(`results/seal_check_after_run.txt`).

Outputs as executed: `results/results_menus_real.json` (sha256 `790b274a…`) and
`results/graded_menus_real.json` (sha256 `c231671a…`). The verdict is GRADED, not void: 1 of 735
calibration fits did not converge.

Data: 147 participants and 24,933 scored HV-or-LV choices on distractor trials. 1,526 presses on the
unavailable distractor were excluded as registered.

## Verdicts

The main prediction fails, and not narrowly. Range scaling at Molter's exponent predicts the effect of
an unavailable distractor *worse* than additive value does.

| | Prediction | Verdict | Numbers (distractor-trial log-loss per choice, nats; margin 0.0027) |
|---|---|---|---|
| H1 | Range scaling at ρ\* = 0.526 beats additive value | **FAIL** | RNG − ADD = +0.0146 [+0.0078, +0.0216] |
| H2 | It beats divisive normalisation | **FAIL** | RNG − DN = +0.0092 [+0.0005, +0.0178] |
| H3 | It beats full range normalisation | PASS (uninformative) | RNG1 loses 26 nats per choice; see below |
| H4 | Universality: the exponent transfers | **FAIL** | median free ρ 0.356 [0.314, 0.389], below Molter's IQR 0.381–0.746 |
| H5 | Square-root-to-Weber crossover | NOT ASSESSABLE | declared before the run |

Test loss per choice: ADD 0.5331, DN 0.5385, RNG 0.5477, RNG1 26.2. The RNG − ADD difference by
experiment is +0.002, +0.028, +0.005 and +0.013. RNG is worse in all four experiments.

## The reading

**On these data an unavailable distractor does not move choice the way Molter's menus did.**

- Additive value, which predicts no context effect at all, is best.
- Divisive normalisation does not beat it either (DN − ADD = +0.005 [−0.003, +0.013]).
- This agrees with Cao and Tsetsos 2022, who found the distractor effects reported in these
  experiments vanish once covariation between attributes is controlled.
- The partial range scaling that reproduced Molter's attraction and compromise effects does not carry
  over to a speeded task with perceptually coded attributes and a distractor that cannot be chosen.

**H3's pass carries no weight.** With only two options on the calibration trials, full normalisation
divides every gap by itself. Each attribute then contributes only the sign of its difference, so the
calibrated weights grow without bound and the predictions on distractor trials are near-certain and
often wrong. The rehearsal showed the same heavy tail. H3 was badly posed: it compared RNG with a model
that cannot be calibrated on binary trials. It is reported as registered.

**H4: universality fails, and the free exponent is confounded.** Gluth's median ρ, 0.36, is clearly
above 0 and clearly below Molter's range. With two options, though, dividing a gap by the range raised
to ρ is the same as raising the gap to the power 1 − ρ. On binary trials ρ therefore measures
diminishing sensitivity to differences, not context. RNGfree was fit on binary and distractor trials
together, so its ρ mixes the two. The same confound applies in part to Molter: on any menu where the
third option does not extend a range, ρ acts as gap curvature. This was not seen before sealing.
The registered H4 still fails as written.

## What this does to the menus line

The menu-dependent scale was the one positive geometric result left from the development work. On its
first out-of-sample test it fails, and the exponent does not transfer. Molter's result remains a
development finding on one dataset. Before any further claim, two things need separating:

- context effects proper (a third option that changes a range), against curvature of gaps;
- choosable decoys (Molter), against unchoosable distractors (Gluth).

That needs a dataset with choosable decoys and varied ranges, which has not yet been identified.
