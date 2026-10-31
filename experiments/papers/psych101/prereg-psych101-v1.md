# prereg-psych101-v1. Part II's risky-choice models, frozen, on a corpus they have not seen

**Author.** Andrew H. Bond, San José State University.
**Companion to.** Geometric Prediction of Economic Behavior I (IEEE TCSS, doi 10.1109/TCSS.2026.3734068)
and II (in preparation), and the theory paper (`../theory/`).
**Freezing.** Section 9. Nothing here is a registered claim until the bundle is hashed, committed with a
signed commit, tagged with a signed tag, and pushed to the public repository. No choice in the corpus is
scored before that.

## 1. Question

Part II compared the geometric model (GDT) with expected value, linear random utility and cumulative
prospect theory (CPT) on CPC18, fitting and testing on splits of the same corpus. GDT beat expected value
and random utility and trailed CPT. This study asks whether that ordering holds when every model is fit
on CPC18 and carried, frozen, to a corpus from a different literature, with different participants,
different problems and a different payoff unit. It also asks whether the shape of the geometric metric,
the ratio of its money and risk scales, carries over. The theory paper (Proposition 2) says the shape is
identified and the scale is not. If the shape is a property of people and not of one problem set, the
CPC18 shape should fit the new corpus.

## 2. Data

`wulff2018description/exp1.csv` in Psych-101 (Binz et al. 2025, Hugging Face `marcelbinz/Psych-101`, the
copy cached on Atlas on 2026-09-13). The study is Wulff, Mergenthaler-Canseco and Hertwig's
description-condition data: 1,981 participants, each choosing between two described lotteries, one key
press per problem, in points converted to a bonus.

**What was read before freezing.** The file list and transcript format, with every choice token masked
(`inspect_stimuli.py`). The option descriptions, to key problems against CPC18 (`overlap_stimuli.py`).
The count of choice tokens, in 2026-09 (`../../datasets/wulff_coverage.py`, which fitted nothing) and
here. `build_rows.py` parses each press into a separate outcome file. No choice rate, and no statistic of
any choice, was computed before freezing. The rehearsal (Section 8) reads only the covariate file.

**Rows.** Every press token is assigned to a named bucket, and the buckets must sum to the token count:

| bucket | presses |
|---|---|
| two described options, kept | 24,124 |
| repeats a CPC18 problem, dropped | 3,630 |
| an option with more than two outcomes, dropped | 318 |
| stated probabilities do not sum to one, dropped | 81 |
| total | 28,153 |

Kept: 24,124 choices on 991 distinct problems. A CPC18 repeat is a problem whose two options have the
same expected values and minimum outcomes as a CPC18 problem's (6 problems, frequently shown).

**Not used.** Other Psych-101 risk files were inspected and set aside: `peterson2021using` is choices13k,
used in this programme before. `ruggeri2022globalizability` was a Part II leg. `plonsky2018when` repeats
CPC18 (42 of its 48 problems match). `wulff2018sampling` is the experience paradigm. `frey2017cct` (a card
task), `frey2017risk` (balloon pumping) and `hilbig2014generalized` (cue-based inference) are not choices
between described lotteries, so none of these models can be scored on them.

## 3. Models, frozen on CPC18

The four models of Part II's CPC18 table, imported from `experiments/datasets/fit_transfer.py` and not
restated, fit on all 270 CPC18 games (description choices) by `freeze_cpc18.py`. Parameters are in
`frozen_cpc18.json`, which is sealed.

- **EV.** Logit on the difference in expected value.
- **RUM.** Logit, linear in the differences in expected value and standard deviation, plus an intercept.
- **GDT.** Cost is the distance from the better expected value and zero risk, with money scale `s_ev`
  and risk scale `s_sd`; logit in the cost difference. The aversion angle is the ratio `s_ev / s_sd`. Its
  CPC18 value is 0.105.
- **CPT.** Cumulative prospect theory, five parameters.
- **CPT_TK92** (reported, not graded). CPT at Tversky and Kahneman's 1992 estimates (0.88, 0.88, 2.25,
  0.61) with only its temperature fit on CPC18. The code has one weighting exponent for gains and losses,
  so the 1992 loss exponent of 0.69 is not represented.

Option A is the lottery listed first and B the second.

**Common unit.** In each corpus, payoffs are divided by the standard deviation of option expected
values over that corpus's problems, computed from the stimuli alone (CPC18 11.84; this corpus in
`fit_psych101.py`). The models are frozen in that unit and applied in it. Without it, CPT's unequal
curvature for gains and losses would make "frozen CPT" depend on the currency, shekels in CPC18 and
points here (Section 8, round 2). In this unit the CPC18 aversion angle is 0.105.

## 4. Procedure

The 991 problems are split at random (seed 20261031) into a calibration half and a test half. All rows of
a problem fall in the same half.

**Transfer.** Each frozen model refits one number on the calibration half, a multiplier `kappa` on its
frozen logit. A metric's scale is not identified across contexts and its shape is, so a transferred
model keeps its shape and recalibrates its scale. Every model gets the same single free number.

**Native.** Each model is also refit in full on the calibration half, starting from its frozen values,
with Part II's fitter. A fit has converged if a restart from its solution changes the calibration loss by
less than 1e-6 relative.

**Scoring.** Log-loss per choice in nats on the test half. Comparisons are paired bootstrap differences,
2,000 resamples of test problems (the unit the covariates live on), 95% percentile interval.

**Margin.** `m` is 1% of the native EV model's calibration gain over a constant. "Beats" means the
interval lies entirely below `-m`.

**Angle interval.** Native GDT is refit on 500 bootstrap resamples of calibration problems. The 95%
percentile interval of `s_ev / s_sd` is the corpus's interval for the angle.

## 5. Predictions (bars live in `grade_psych101.py`)

- **H1.** Frozen GDT beats expected value refit on this corpus.
- **H2.** Frozen GDT beats frozen linear random utility.
- **H3.** Frozen CPT beats frozen GDT. This is Part II's ordering, and the prediction is that it
  replicates.
- **H4.** The CPC18 aversion angle lies inside this corpus's 95% interval for the angle.
- **H5.** GDT's deficit to CPT is larger on problems where some outcome is a loss than on gains-only
  problems. Part II reports that the encoding does not capture the reversal of risk attitudes under
  losses, and this is that statement made testable. Pass if the interval of the difference in
  differences lies entirely above `m`.

Each prediction stands alone. No composite verdict is registered.

## 6. Void conditions

- **V1.** The press accounting in `build_rows.py` fails (the script stops with an assertion).
- **V2.** The native EV or native GDT fit fails the convergence check. H1 and H4 depend on them.

## 7. Reported regardless

Test log-loss of every model in every form (frozen with `kappa`, native, and frozen with no refit at
all), every `kappa`, the native parameters, the transfer efficiency of GDT, CPT and RUM (the share of
the distance from chance to the native fit that the transferred model closes), CPT_TK92 against GDT, and
every comparison split by problems with and without a loss.

## 8. Rehearsal

The whole chain was run with the real covariates and the choices replaced by draws from a known model:
frozen GDT in one run and frozen CPT in the other. Under a GDT truth the chain had to find the angle
(H4 pass), beat expected value (H1 pass), and not prefer CPT (H3 fail). Under a CPT truth it had to
prefer CPT (H3 pass). Results are in `rehearsal/`. It took three rounds.

**Round 1 failed both checks.** Each model's logit was recovered by inverting its predicted
probability. Where the frozen model is sharp the inversion saturates, so the scale refit worked on a
clipped signal. Under a GDT truth, frozen GDT then lost to expected value. The logit is now read from
Part II's code before the sigmoid.

**Round 2 passed the GDT check and failed the CPT check.** Payoffs were in each corpus's own currency,
and the simulation rescaled them. A scale refit absorbs a change of currency for GDT, whose cost is
homogeneous in payoffs, but not for CPT, whose gain and loss curvatures differ. Under a CPT truth the
transferred CPT was therefore not the truth, and the chain did not prefer it. The same flaw would have
made H3 depend on the arbitrary currency in the real run. The common unit of Section 3 was added, the
models were refrozen in it (in-sample fit on CPC18 unchanged, CPT's loss aversion changing with the
unit), and the rehearsal was rerun. The raw-unit parameters are kept in `rehearsal/round2/`.

**Round 3 passed both checks.** Under the GDT truth, frozen GDT beat expected value by 0.0044 nats per
choice (interval −0.0072 to −0.0020, margin 0.0008), CPT did not beat GDT, the refit scale was 1.01,
and the angle interval was 0.082 to 0.121 around the true 0.105. Under the CPT truth, CPT beat GDT by
0.0055 (interval −0.0084 to −0.0029) and H5 passed.

**Two limits the rehearsal shows.** H4 also passed under the CPT truth, because when GDT is the wrong
model its angle is poorly determined (interval 0.006 to 0.133). A pass on H4 is therefore evidence
only alongside H3 failing. And H2 failed under both truths: on these problems linear random utility
and GDT make nearly the same predictions, so H2 is expected to fail whichever model is true and has
little power to tell them apart.

## 9. Not claimed

The corpus pays a bonus, so choices were incentivized, but the conversion from points to money is that
study's and is not modelled. One corpus is one test. A pass on H4 says the CPC18 shape fits this corpus,
not that it fits every corpus; Part II already records that adversarially chosen Kahneman–Tversky
problem sets shift the angle. A failure on H3 would mean GDT matches or beats CPT out of corpus, which
Part II did not find, and it would be reported as found here only.

## 10. Freezing procedure

1. Write `prereg-psych101-v1.sha256` with `seal_psych101.py --write`.
2. Commit with a signed commit, tag `prereg-psych101-v1` with a signed annotated tag, push both.
3. Only then run `fit_psych101.py` without `--simulate`, and `grade_psych101.py` on its output.
