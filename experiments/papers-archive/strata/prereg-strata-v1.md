# prereg-strata-v1. Refusing the early projection: a stratified encoding of lotteries

**Freezing.** Section 11. Nothing here is a registered claim until the bundle is hashed, committed
with a signed commit, tagged with a signed tag, and pushed. Every constant lives in `fit_strata.py` and
`grade_strata.py`. The corpus list (Appendix A) was fixed from stimulus files and documentation only,
before any choice in any test corpus was scored.

**Author.** Andrew H. Bond, San José State University.
**Companion to.** Parts I and II (IEEE TCSS), the theory paper (`../theory/`), `prereg-psych101-v1`.

## 1. Why this study exists

The geometric programme holds that standard decision theories fail because they compress an option
into too few numbers before choosing (*The Geometry of Good*: "Maybe is what you say when you see the
tensor and refuse to contract it prematurely"). On lotteries, `prereg-psych101-v1` found the geometric
model's own encoding doing exactly that. It reads a lottery only through its expected value and standard
deviation. Frozen CPT beat it out of corpus by 0.017 nats per choice, and it did not separate from
expected value. An unregistered breakdown after grading (`../psych101/explore_deficit.py`) showed people
taking risk at 38% in gains and 50% in losses, a reflection the encoding cannot produce, and both models
predicting near chance at small stakes where people chose decisively.

The parable names three things a scalar discards: which direction the change lies in, the shape of the
uncertainty, and which regime the outcome lands in. This study restores those three in the encoding,
fixes the encoding before seeing any new data, and asks whether it closes the gap to CPT on corpora the
programme has never used.

The explanation "it failed because it contracted too early" can be applied to any failure after the
fact. That is why the encoding is fixed here, in advance, and why the bars below can fail.

## 2. The stratified encoding (GDT-S)

**Stake coding (theory paper, Proposition 3).** In each problem, every outcome is divided by the
problem's stake `S`, the largest absolute outcome across both options. Outcomes become shares in
[−1, 1]. Choice predictions are therefore unchanged when all payoffs in a problem are multiplied by the
same positive number.

**Coordinates.** For an option with share outcomes `x_i` and probabilities `p_i`:

| Coordinate | Definition | What the parable calls it |
|---|---|---|
| `g` | expected gain, `Σ p_i max(x_i, 0)` | direction: how much lies on the good side |
| `l` | expected loss, `Σ p_i max(−x_i, 0)` | direction: how much lies on the bad side |
| `π+` | probability the outcome lands in the gain stratum, `Σ p_i [x_i > 0]` | regime |
| `π−` | probability the outcome lands in the loss stratum, `Σ p_i [x_i < 0]` | regime |
| `s` | standard deviation of the share outcome | shape |

Expected value (`g − l`) and standard deviation are functions of these coordinates, so GDT-S keeps
everything the old encoding read and adds sign and stratum occupancy.

**Cost.** The reference is the best value of each coordinate on the menu: the largest `g` and `π+`, the
smallest `l` and `π−`, zero spread. With `Δ` the option's displacement from that reference,

    C = sqrt( w_g Δg² + w_l Δl² + w_+ Δπ+² + w_− Δπ−² + w_s s² ) + β · [π− > 0],

where `β ≥ 0` is a boundary penalty for any chance of entering the loss stratum (theory paper,
Proposition 4: with a symmetric metric, asymmetries enter through boundary penalties). Choice is logit in
`−C`, with the temperature absorbed into the weights. Six parameters: five weights and `β`. CPT has five.

This encoding was chosen from the parable and the theory paper, and from the Wulff breakdown, which is
why Wulff is excluded below. It was not fitted to anything. Whether it can produce reflection depends on
`w_−` against `w_s`, which are fitted on CPC18 only.

## 2b. The consumer arm (GDT-C): the read is chosen by a budgeted observer

GDT-S still has a modeller choosing what the decision maker reads. In Observation Theory an observer is
`O = (C, G, B)`: a read operator, a metric, and a budget, and the decision cost is the pullback
`P_C = Jᵀ G J` with the encoding as the consumer (`geometric-observation/paper/observer-representation.tex`).
A consumer with a finite budget must compress. GDT-C lets the compression follow from the budget and
the environment instead of from the modeller.

**What is read, and with what noise.** For each branch of an option, the share outcome `|x|` is read on
a log scale and its probability on a log-odds scale. Each reading passes through an efficient code for
the environment: the value is mapped through the cumulative distribution of that quantity across the
environment's lotteries (the probability-integral transform, as in decision by sampling), Gaussian noise
of standard deviation `σ_k` is added on the probit of that rank, and the decision maker decodes the
posterior mean under the same environment distribution. Decoded probabilities are renormalised to sum to
one.

**The environment is the corpus's stimuli.** The distributions that define the code are computed from
each corpus's lottery descriptions alone (all branch probabilities and share magnitudes over its
problems), never from choices. On CPC18 they come from CPC18's stimuli. So the decision maker's
distortions are predicted to differ between corpora by an amount fixed before any choice is opened.

**The budget, allocated by the consumer.** One budget `B` (bits per branch reading) is split between the
magnitude and probability readings by reverse water-filling weighted by how much each reading moves the
consumer's cost: weight `w_g + w_l` for magnitudes and `w_+ + w_−` for probabilities, the GDT-S metric
weights (the consumer-relative rate–distortion function, Gaussian case). The split is not fitted.

**Choice.** GDT-S cost on the decoded coordinates, logit, averaged over `[code]` fixed noise draws. Seven
parameters: GDT-S's six and `B`, all frozen on CPC18.

**Prior work this arm rests on, credited.** Efficient coding produces small-stakes risk aversion from
noisy magnitude representations (Khaw, Li and Woodford, *Review of Economic Studies* 88(4):1979–2013,
2021). A bounded log-odds code explains probability distortion as approximately information-maximising
(Zhang, Ren and Maloney, *PNAS* 117(36):22024–22034, 2020). Probability weighting moves with the prior
over probabilities, and the inverse-S shape requires a U-shaped prior (Frydman and Jin, NBER Working Paper
31573, 2023). Decision by sampling implements efficient coding through the rank transform (Bhui and
Gershman, *Psychological Review* 125(6):985–, 2018, doi 10.1037/rev0000123). What this arm adds is the
read chosen by a consumer whose budget is allocated by the decision metric, and one observer construction
shared with the programme's games and ethics work. `% verify page ranges on final`

**A simpler version failed here before.** `experiments/datasets/efficient_coding.py` (choices13k) tested
whether a fixed risk weight is rescaled by the environment's variance. The normalised weight changed sign
across risk levels instead of staying constant (`RESULTS_efficient_coding.md`). That rescaled fixed
coordinates. GDT-C changes what is read and how precisely, which is a different hypothesis, but the
earlier failure is the reason not to expect it to work.

## 2c. Identification: why the consumer arm has content

GDT-S and GDT-C are evaluation objects in the sense of Geometric Evaluation Theory
(`geometric-evaluation-theory/paper/geometric-evaluation-theory.tex`): the world supplies the consequence
map (here the stratified coordinates of each lottery), and the evaluator supplies the metric, the ideal,
the budget and the admissible set. The reference is the best value on the menu, so both are GET's
menu-relative evaluators. GET notes that loss aversion is not representable by a symmetric metric and
needs an asymmetric metric or the admissible set. GDT-S puts it in the boundary penalty `β`, a soft form
of an admissibility boundary at zero.

Observer-Limited Geometric Cognition (`geometric-cognition/paper/olgc.tex`, Proposition "Vacuity without
modular identification") proves that if representation, metric, budget and admissible set are all fitted
to the record being predicted, the account fits any record and predicts nothing. Its Definition "Modular
identification" gives the condition for content: each component estimated from evidence disjoint from
the record, and the admissible set fixed in advance. The consumer arm adds a budget, which is exactly the
kind of component that can absorb anything. This design meets the condition component by component:

| Component | How it is fixed | Evidence | Disjoint from the test choices? |
|---|---|---|---|
| Representation (stratified coordinates, log and log-odds reads) | rule, Sections 2 and 2b | none | yes |
| Reference (best on menu) | rule | none | yes |
| Admissible set | none, beyond the penalty `β` | none | yes |
| Metric weights, `β` | fitted | CPC18 choices | yes |
| Budget `B` | fitted | CPC18 choices | yes |
| Budget allocation | derived from the metric | none | yes |
| Environment code (prior) | computed | the test corpus's stimuli | yes, stimuli only |
| Scale `κ` | fitted | the test corpus's calibration half | yes, disjoint problems |

**Identification inside CPC18.** OLGC also shows that a component can be fixed in advance and still be
unidentified (its rank-budget case: no spectral gap, so the recovered direction is noise). The budget
here could trade off against the metric weights. Before sealing, frozen GDT-C is used to simulate
choices on CPC18's own stimuli, the model is refit, and the recovery of `B` and of the probability-to-
magnitude allocation is reported. **V4** below makes failure of that recovery void the consumer arm.

**What is not tested.** GET's hull law and menu-dependent violations of regularity need menus of three
or more options. If a qualifying corpus has them, regularity is checked and reported without a bar.

## 3. Data

**Freezing corpus.** CPC18 description choices (trial 1), the 230 games without ambiguity, with the
two-outcome approximation Part II used for multi-outcome shapes (`experiments/datasets/cpc18.py`). Every
model is fitted here once and frozen.

**Test corpora.** Every corpus that meets all of these, fixed before any choice is opened:
1. Choices between lotteries whose outcomes and probabilities are stated (description, not experience).
2. Choice-level records. Price lists and certainty-equivalent tasks qualify when each row can be recoded
   as a binary choice between a lottery and a sure amount, and that recoding is written in `[code]`
   before the choices are read.
3. At least 1,000 choices after exclusions.
4. Publicly obtainable, or obtained from the authors before sealing.
5. Never used in this programme: not CPC15/CPC18, choices13k (`peterson2021using`), Ruggeri et al.
   2020, `plonsky2018when`, or `wulff2018description`. Wulff is excluded because its test half shaped
   this encoding.

Problems that repeat a CPC18 problem are dropped, keyed as in `../psych101/overlap_stimuli.py`. Problems
with ambiguous or unstated probabilities are dropped. Every choice token is accounted for in named
buckets that must sum to the corpus total, as in `../psych101/build_rows.py`.

**Corpus list.** Appendix A: five corpora, 68,826 choices after exclusions and de-duplication.

**What was read before freezing.** File lists, codebooks, column headers, and the stimulus columns.
To confirm formats, a handful of individual choice values in two files were displayed (the first rows
of `par_stab1_new.csv`, and two cells of the Pachur 2017 choice matrix). No choice statistic of any
test corpus was computed. Parsers write choices to separate files that nothing before the seal opens.
The results of these studies are published, and their papers were not read for this design beyond
stimulus tables and codebooks.

## 4. Models compared

All are fitted on CPC18 and frozen.

- **GDT-S**, Section 2.
- **GDT-C**, Section 2b. On each test corpus its code is rebuilt from that corpus's stimuli; its seven
  parameters stay frozen.
- **GDT-2**, Part II's geometric model (expected value and standard deviation), as in
  `prereg-psych101-v1`.
- **CPT**, five parameters: Tversky and Kahneman's 1992 rank- and sign-dependent form, with one
  weighting exponent for gains and losses. Part II's code (`fit_transfer._cpt_value`) is this form only
  for gains-only problems; on losses and mixed problems it attaches the decision weights to the wrong
  outcomes. The standard form is used here because it is the stronger incumbent, and
  `prereg-psych101-v1`'s CPT result is to be read with this caveat. `fit_strata.py selfcheck` confirms
  the two agree on gains-only CPC18 problems. Fitted twice on CPC18, in the common payoff unit of
  `prereg-psych101-v1` and in the stake coding above. On each test corpus the calibration half chooses which coding is used. CPT
  gets its better coding, so a GDT-S win cannot come from stake coding alone.
- **EV** and **RUM**, as in Part II, reported.

## 5. Procedure

Per corpus, as in `prereg-psych101-v1`. Problems are split at random into calibration and test halves.
Each frozen model refits one multiplier on its logit on the calibration half. Every model is scored on
the test half by log-loss per choice, with a paired bootstrap over test problems (`[code]`: 2,000
resamples, seed). The margin `m` is 1% of EV's calibration gain over a constant, per corpus. Pooled
results weight corpora equally, so one large corpus cannot decide the study.

## 6. Predictions

- **H1. Restoring structure helps.** Frozen GDT-S beats frozen GDT-2, pooled (interval below `−m`), and
  in a majority of corpora.
- **H2. Most of the gap closes.** Pooled, GDT-S closes at least half the distance from GDT-2 to CPT:
  `(L_GDT2 − L_GDTS) / (L_GDT2 − L_CPT) ≥ 0.5`, with the bootstrap lower bound above 0.25. If CPT does
  not beat GDT-2 pooled, H2 is not assessable and is reported as such.
- **H3. The strong claim.** Frozen GDT-S beats frozen CPT, pooled. This is the prediction the thesis
  makes at full strength. `prereg-psych101-v1` makes it unlikely, and it is registered so that it can
  fail.
- **H4. Stake invariance is real.** A stake group is a set of problems identical in stake coding but
  at different stakes. For each group, the lowest- and highest-stake problems are compared: the statistic
  is `|Δ_pred| − sign(Δ_pred)·Δ_obs`, where `Δ_pred` is GDT-2's predicted change in choice rate and
  `Δ_obs` the observed change. Positive means people moved less with stake than GDT-2 predicts. Pass if
  the mean over groups has a bootstrap interval above zero. Assessable with at least five groups. From
  stimuli: only Pachur et al. 2018 has stake groups (six, mixed gambles), so H4 is a weak test.
- **H5. The documented effects.** On a fixed set of constructed lotteries (Section 7), GDT-S reproduces
  more of the documented effects than GDT-2, and at least four of the six.

- **H6. The consumer helps.** Frozen GDT-C beats frozen GDT-S, pooled, and in a majority of corpora.
  Assessable only if the two frozen models predict differently on the test stimuli: mean
  `|p_GDT-C − p_GDT-S|` of at least 0.005 over problems (V5).
- **H7. Distortions shift between corpora as the frozen geometric model predicts from stimuli.** For each test corpus, CPT is
  refit on its calibration half and its probability-weighting exponent `γ_c` is the observed summary. The
  predicted summary is the `γ` of CPT fitted to choices simulated by frozen GDT-C on that corpus's
  stimuli. CPT is in the stake coding throughout. Pass if the predicted and observed shifts from CPC18,
  `γ_c − γ_CPC18`, have the same sign in every corpus where the predicted shift exceeds 0.05, with at
  least three such corpora; otherwise not assessable. Frozen CPT predicts no shift, so the incumbent
  cannot pass this test by construction. The rehearsal (Section 9) showed that H7 passes when GDT-S or
  GDT-2 generate the choices, not only GDT-C. It therefore tests whether the frozen geometric family
  predicts how risk distortions move between environments. It does not isolate the consumer's coding.
- **H8. The consumer produces the rare-event effects.** GDT-C, with the code built from CPC18's stimuli,
  reproduces effects 4 and 5 of Section 7 (the long shot and the insurance). GDT-S is expected to miss
  both. Frydman and Jin's result says this needs CPC18's probabilities to be U-shaped; their histogram is
  computed from stimuli and reported before sealing, so the prediction is made knowing whether the
  condition holds.

Each prediction stands alone. No composite verdict.

## 7. Documented effects, on constructed lotteries (no human data)

Lotteries built in `[code]`, scored with the frozen parameters, nothing fitted to them. An effect is
reproduced when the predicted choice probability is on the documented side of one half in every
instance listed.

1. **Reflection.** Sure 3,000 over 80% of 4,000, and 80% of −4,000 over sure −3,000 (Kahneman and
   Tversky 1979).
2. **Certainty effect, common ratio.** Sure 3,000 over 80% of 4,000, and 20% of 4,000 over 25% of
   3,000.
3. **Loss aversion in mixed gambles.** A 50/50 gamble of +X against −X rejected for X in {10, 100, 1,000}.
4. **Possibility effect for gains.** 0.1% of 5,000 over sure 5.
5. **Insurance for losses.** Sure −5 over 0.1% of −5,000.
6. **Stake invariance.** Problem 1 at stakes ×0.01, ×1 and ×100 predicted on the same side.

Effect 6 counts as reproduced when the prediction is on the same side at all three stakes, whichever
side that is. It holds by construction for GDT-S (the stake coding), and on this gains-only problem it
also holds for GDT-2 and CPT, whose predictions here are homogeneous in payoffs. It is listed so the
count is honest.

## 8. Void conditions

- **V1.** A corpus fails its press or row accounting. That corpus is void, the rest stand.
- **V2.** A frozen fit on CPC18 fails the convergence check (a restart from the solution changes the
  loss by more than 1e-6 relative).
- **V3.** Fewer than two test corpora qualify. The study then runs on what exists and H1–H3 are reported
  without bars.
- **V4.** On CPC18 stimuli with choices simulated from frozen GDT-C, the refit recovers `B` outside
  a factor of two of the truth, or recovers the allocation with the wrong ordering. The consumer arm is
  then void, H6 to H8 are not graded, and the rest stand.
- **V5.** Frozen GDT-C and GDT-S predict nearly the same on the test stimuli (mean absolute difference in
  predicted choice probability below 0.005). H6 is then not assessable: no data could separate them.

## 9. Rehearsal (before sealing)

The chain runs on each corpus's real covariates with simulated choices from four truths: GDT-C, GDT-S,
GDT-2 and CPT, each frozen. It must find GDT-S when GDT-S is true (H1 pass, H3 pass), must not prefer
GDT-S when GDT-2 is true (H1 fail), must prefer CPT when CPT is true (H3 fail), must find the consumer
when GDT-C is true (H6 pass, H7 pass where assessable), and must not prefer GDT-C when GDT-S is true
(H6 fail). Rounds and fixes are
recorded here, as in Parts III and Psych-101.

**Freezing record (CPC18, 230 games, before any test choice was scored).** In-sample log-loss per choice:
EV 0.6339, RUM 0.6183, GDT-2 0.6162, CPT in the common unit 0.6110, CPT in the stake coding 0.6028,
GDT-S 0.5990, GDT-C 0.5989. Every fit converged. In sample, GDT-S fits CPC18 better than either CPT;
that is a fit, not a prediction. GDT-S's frozen weights put almost all of the metric on expected gain and
expected loss (`w_g` 33, `w_l` 28), little on the probability of a gain (0.53), almost none on the
probability of a loss (0.007) or on spread (under 1e-5), with a boundary penalty `β` of 0.73. GDT-C's
frozen budget is 15.1 bits per reading, so its reading noise is small (probit-rank standard deviations
0.0017 for magnitudes and 0.017 for probabilities).

**V4 passed.** Refits on three simulated CPC18 datasets recovered budgets of 14.9, 21.1 and 13.1 bits
against 15.1, all within a factor of two, with the allocation order (probabilities noisier than
magnitudes) recovered each time (`recovery_v4.json`).

**Three predictions are decided at freezing, before any test choice.** They depend only on the frozen
parameters and on stimuli, and they are stated here as facts, not as predictions.
- **H5 fails.** GDT-S reproduces two of the six effects (loss aversion and stake invariance). GDT-2
  reproduces three (those two and insurance). CPT reproduces four (reflection, common ratio, insurance,
  stake invariance). Frozen on CPC18, the stratified encoding does not produce reflection or the
  certainty effect: its fitted weights leave the spread and the probability of a loss almost unweighted.
- **H8 fails.** GDT-C reproduces neither the long shot nor the insurance effect. CPC18's probabilities
  are not cleanly U-shaped (Appendix A), which Frydman and Jin's result says the inverse-S needs.
- **H6 is not assessable (V5).** On the test stimuli, frozen GDT-C and GDT-S differ in predicted choice
  probability by 0.0006 to 0.0030 on average per corpus, below 0.005. At the budget CPC18 calls for, the
  consumer reads lotteries almost exactly, and no choice data could separate it from GDT-S.

The live predictions are H1, H2, H3, H4 and H7.

**Round 1** passed the GDT-S, GDT-2 and CPT truths and failed the GDT-C truth: H6 could not detect the
consumer even when it generated the choices, because at the frozen budget it predicts what GDT-S does.
Round 1 also showed H7 passing under the GDT-S and GDT-2 truths, not only GDT-C, and an error in the
effect-6 check (it required a fixed side instead of the same side at every stake). Fixes: V5 added, H7
restated as a test of the geometric family, a rehearsal requirement that H7 not pass under the CPT
truth, and effect 6 corrected. Round 2 passed all four truths: under GDT-S, H1, H2, H3, H4 and H7 passed
and H6 was not assessable; under GDT-2, H1 and H3 failed; under CPT, H1 to H4 and H7 failed; under GDT-C,
the same as under GDT-S. Outputs are in `rehearsal/`.

## 10. Not claimed

A pass on H3 would mean the stratified geometric encoding predicts lottery choice better than CPT on
these corpora with frozen parameters. It would not show the encoding is the right one, only that it is
better than these alternatives here. A failure of H3 with a pass on H1 and H2 would mean that refusing
the early projection helps but that CPT's reading of a lottery still holds structure GDT-S lacks. That
is a result about which structure to keep, and would be reported as such. A pass on H6 or H7 supports a
budgeted-observer account of lottery choice; much of that account is the efficient-coding literature
credited in Section 2b, and a pass would be reported as support for it as much as for this programme.

## 11. Freezing procedure

1. Appendix A fixed from stimulus files and documentation. Scripts written, rehearsal run.
2. Hash the bundle, commit with a signed commit, tag `prereg-strata-v1` with a signed tag, and push.
3. Only then open the choice files and run the fit and the grader.

## Appendix A. Test corpora

Fixed 2026-10-30 from stimulus files and documentation. Counts are after exclusions and after dropping
problems that repeat CPC18, choices13k or Wulff (`stimuli_check.py`, stimulus keys only).

| Corpus | Source | Choices | Problems | People | Overlap dropped |
|---|---|---|---|---|---|
| Glöckner and Pachur 2012 | osf.io/7khwj | 12,160 | 161 | 64 (2 sessions) | 76 problems in Wulff (5,504 choices) |
| Pachur, Mata and Hertwig 2017 | osf.io/35pf6 | 10,370 | 85 | 122 | 16 in Wulff, 4 in CPC18 (2,440 choices) |
| Pachur et al. 2018, Experiment 2 | osf.io/5semf | 6,200 | 51 | 120 | none |
| Zilker, Hertwig and Pachur 2020, studies 1 and 2 | osf.io/nzwx4 (CC BY 4.0) | 28,976 | 112 | 318 | none; 17,848 complex-safe trials excluded by rule, 320 unparseable |
| Babula 2018 | doi 10.5281/zenodo.7770917 (CC BY 4.0) | 11,120 | 160 | 70 | none; 46 rows without a problem id |

Branch probabilities strictly inside (0, 1), share in fifths of the unit interval (stimuli only):

| Environment | 0–.2 | .2–.4 | .4–.6 | .6–.8 | .8–1 | U-index |
|---|---|---|---|---|---|---|
| CPC18 | .22 | .14 | .28 | .08 | .28 | +0.23 |
| Glöckner and Pachur | .15 | .18 | .33 | .16 | .17 | −0.01 |
| Pachur 2017 | .17 | .20 | .27 | .17 | .20 | +0.09 |
| Pachur 2018 | .10 | .09 | .62 | .08 | .11 | −0.40 |
| Zilker | .25 | .14 | .21 | .13 | .27 | +0.32 |
| Babula | .18 | .23 | .38 | .13 | .08 | −0.12 |

The U-index is the share in the outer fifths minus the share in the middle fifth. CPC18 is not cleanly
U-shaped: its middle fifth is as heavy as its outer ones.

**Excluded, decided before any choice was scored.** Basel–Berlin Risk Study: its lottery task is
adaptive, each item set by the participant's earlier choices, so the stimuli carry the choices; its
description task reuses Hertwig et al. 2004 problems given only as labels. l'Haridon and Vieider 2019
and Bernheim and Sprenger 2020: price lists, recoding to binary choices not implemented. Great Brain
Experiment and Frydman and Jin 2021: a single probability throughout, so they cannot separate the
probability-reading arms, and no parser was built. Bruhin, Fehr-Duda and Epper 2010: licence restricts
use beyond replication. Hey and Orme 1994, Harless and Camerer 1994, the Erev et al. 2010 tournament:
not located. Rieskamp 2008: choices need an author request. Pachur et al. 2018 Experiment 1: problems
exist only as a table in the paper.
