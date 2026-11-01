# Completeness and restrictiveness of GDT, CPT and baselines on risky choice

Written 2026-10-31, before any score was computed. Descriptive, not a pre-registered test: every
corpus here has already been used (CPC18 for freezing, the five strata corpora for prereg-strata-v1
and strata2). Fresh corpora stay reserved for confirmation.

## Why

The sealed tests compared models pairwise in nats. Economics has two standard measures that place
a theory on the field's own scale:

- **Completeness** (Fudenberg, Kleinberg, Liang and Mullainathan, "Measuring the Completeness of
  Economic Models", JPE 2022): the share of the predictable variation a theory captures, between a
  naive baseline (0) and the best available predictor (1).
- **Restrictiveness** (Fudenberg, Gao and Liang, "How Flexible Is That Functional Form? Quantifying
  the Restrictiveness of Theories"): how badly a theory fits randomly generated behaviour,
  relative to the naive baseline. Near 1: it cannot fit arbitrary patterns. Near 0: it fits
  anything, so its fit on real data says little.

A good theory is both complete and restrictive. Theorem 1 of the roadmap (any choice model embeds
in a one-dimensional geometric model) describes a theory of restrictiveness 0.

## Data

Six corpora of binary lottery choice, reduced to problems (identical stimuli pooled) exactly as in
`../strata/fit_strata.py`: CPC18 (230 games, description trials, no ambiguity) and gp2012,
pachur2017, pachur2018, zilker2020, babula2018 (51 to 161 problems, 64 to 318 choices each).

## Models

The strata families, refit natively (all parameters free) on each training set: EV (1 parameter),
RUM (3), GDT2 (Part II, 2), GDTS (stratified GDT, 6), CPT_unit and CPT_share (5 each). GDT-C is
left out: in prereg-strata-v1 it predicted the same as GDT-S (difference 5e-5 nats) at many times
the cost.

## Completeness

- 10-fold cross-validation over problems, folds fixed by seed 20261101.
- Each model is fit on the training problems by binomial log-loss (5 starts, as in strata) and
  predicts the held-out problems' choice rates.
- **Naive baseline:** the training mean choice rate.
- **Best predictor:** the better, by out-of-fold error, of two machine-learning regressors on
  problem features (gradient boosting and a random forest, fixed settings in `score.py`), trained
  on the same folds. Picking the better of the two on the same out-of-fold error makes the ceiling
  slightly optimistic, so completeness is slightly understated.
- **Error (primary):** noise-corrected squared error on choice rates, averaged over problems,
  e = mean[(p̂ − f)² − p̂(1 − p̂)/(n − 1)]. The subtracted term is an unbiased estimate of the
  sampling variance of the observed rate p̂, so e estimates the error against the true rate.
- **Completeness vs ML** = (e_naive − e_model) / (e_naive − e_ML), the FKLM definition.
  **Completeness vs ceiling** = (e_naive − e_model) / e_naive, against a perfect predictor of the
  true rates. On small corpora the ML predictor can be weak, so completeness vs ML can exceed 1;
  the ceiling version cannot.
- Secondary: out-of-fold log-loss per choice, completeness vs ML on that scale.
- 95% intervals: 2,000 bootstrap resamples of problems over the out-of-fold predictions (fits are
  not redone). Pooled numbers weight corpora equally.

## Restrictiveness

- For each corpus's problem set, 100 random behaviours f (seed 20261102). For each problem: if one
  option first-order stochastically dominates the other, f is uniform on [0.5, 1] toward the
  dominant option; otherwise uniform on [0, 1]. Dominance is the one regularity imposed; FGL also
  restrict the admissible behaviours, and this is the minimal version.
- Each model is fit to f in-sample by least squares on the rates (3 starts). The naive baseline is
  the best constant, whose error is the variance of f.
- **Restrictiveness** = mean over draws of (error of the model / error of the naive baseline),
  with its standard error over draws.

## Reading

No pass or fail. The output is a table per corpus and pooled: completeness (both versions) and
restrictiveness per model. What would matter:

- whether GDTS or GDT2 is less complete than CPT at similar restrictiveness (dominated), or more
  complete only by being less restrictive;
- how much of the predictable variation the best theory leaves for the ML predictor.

## Where it runs

`prep.py` on Atlas writes one small problems file per corpus. `score.py` runs on NRP, one CPU
Job per corpus (1 CPU, 2 GiB, the policy-exempt shape), submitted through burst.submit, data and
code staged as a ConfigMap, results printed to the Job log. `aggregate.py` pools them.

## Result (2026-11-01; `results/`)

All six Jobs ran on NRP at the first attempt (`results/driver.log`), 2 to 3 minutes each.

Pooled over the six corpora, equal weight. Completeness: 0 = naive constant, 1 = the ML predictor
(vs ML) or a perfect predictor of the true rates (vs ceiling). Restrictiveness: 1 = fits random
behaviour no better than a constant.

| Model | Completeness vs ML [95%] | Completeness vs ceiling [95%] | Restrictiveness (SE) |
|---|---|---|---|
| EV | 0.643 [0.583, 0.692] | 0.531 [0.475, 0.574] | 1.002 (0.001) |
| RUM | 0.776 [0.732, 0.819] | 0.641 [0.598, 0.677] | 0.977 (0.001) |
| GDT2 (Part II) | 0.722 [0.663, 0.772] | 0.594 [0.540, 0.635] | 0.995 (0.001) |
| GDTS (stratified) | 0.899 [0.859, 0.941] | 0.743 [0.705, 0.773] | 0.974 (0.001) |
| CPT, unit coding | 0.902 [0.855, 0.958] | 0.744 [0.706, 0.776] | 0.964 (0.001) |
| CPT, share coding | **0.967** [0.922, 1.022] | **0.798** [0.766, 0.824] | 0.950 (0.001) |

The ML predictor itself reaches 0.83 of the ceiling on average (0.75 to 0.94 by corpus).

Paired differences (same bootstrap resamples), completeness vs ML:

| | Difference [95%] | Restrictiveness difference (SE) |
|---|---|---|
| GDTS − CPT share | −0.068 [−0.103, −0.041] | +0.024 (0.001) |
| GDTS − CPT unit | −0.003 [−0.043, +0.030] | +0.010 (0.001) |
| GDTS − GDT2 | +0.177 [+0.140, +0.224] | −0.021 (0.001) |
| GDT2 − CPT share | −0.245 [−0.303, −0.204] | +0.045 (0.001) |

By corpus (completeness vs ML), GDTS against CPT share: ahead on CPC18 (0.95 vs 0.93), the corpus
its form was developed on, and on babula2018 (0.57 vs 0.55); level on gp2012 (0.98 vs 0.99);
behind on pachur2017 (0.99 vs 1.19), pachur2018 (1.05 vs 1.17) and zilker2020 (0.86 vs 0.98).
Values above 1 mean the model beat the ML predictor out of sample, which happens on the small
corpora.

What this says:

- **GDTS sits on the same frontier as CPT, not beyond it.** It ties CPT in unit coding on
  completeness and is slightly more restrictive. CPT in share coding is more complete by 0.07 and
  slightly less restrictive. Neither dominates the other on both measures, so the honest reading
  is a trade-off, not a win.
- **Part II's GDT2 is dominated.** It is 0.25 less complete than CPT share and closer to EV
  (+0.08) than to CPT; its restrictiveness near 1 comes from fitting little.
- **The models leave about 3 to 10% of the ML-predictable variation unexplained** and about
  20 to 26% of the variation in true rates. The ML predictor leaves about 17%.
- **Restrictiveness separates the models only slightly here.** Random behaviour drawn
  independently per problem is far from anything a smooth two-alternative model can fit, so every
  model scores 0.95 to 1.00. A generator with smoother random behaviour would separate them more.
  What it does show: none of these parameterised models can fit arbitrary behaviour, so
  roadmap Theorem 1's "a geometric model can fit anything" applies to the general construction,
  not to GDTS.
- EV scores above 1 because it has no intercept: on random data it can do worse than a constant.

Spent corpora, refit natively; descriptive, not confirmatory.

## Partial stake scaling (exploration)

Written 2026-11-01, before any fit. Owner: "run the partial scaling exploration. run the sealed test
only after you're certain of how it works". Same six spent corpora; nothing here is confirmatory.

**Question.** Stake-scaled coding raised CPT's completeness by 0.065 [0.045, 0.087] on all six
corpora. Is full scaling right, or partial, as in the menus work (range scaling rho ~ 0.5)?

**Coding.** Outcomes divided by s = unit^(1-rho) * stake^rho, where unit is the corpus scale (SD of
option EVs) and stake the largest absolute outcome in the problem. rho = 0 is the one-unit coding,
rho = 1 the stake-scaled one; rho is free and may leave [0, 1].

**What rho does, worked out before fitting.** With a power value function, (x/s)^alpha =
x^alpha / s^alpha, so rho mostly sets how choice sensitivity falls with the stake: the logit scales as
stake^(-rho*alpha). rho is separated from alpha only through the shape of values within a problem
(different alpha and beta for gains and losses, and lambda). So rho can be confounded with alpha,
and recovery has to be checked before any estimate is believed.

**Prior art to beat.** Wilcox (2011), "Stochastically more risk averse: a contextual theory of
stochastic discrete choice under risk" (J. Econometrics): the utility difference is divided by the
range of utilities of the outcomes in the problem. For gains-only problems this is close to full
stake scaling. If stake^rho does no better than contextual utility, the scaling is Wilcox's, not new.

**Models (`explore_rho.py`).** CPT_unit, CPT_share (as before), CPT_rho (rho free, 6 parameters),
CPT_CU (CPT values in the unit coding, logit = theta * dV / range of v over the problem's outcomes,
5 parameters), GDTS_rho (GDTS on the rho coding, 7 parameters).

**Per corpus:**
- the spread of stakes (max/min stake), since rho is unidentified when stakes barely vary;
- profile log-loss over rho in {-0.5, -0.25, 0, ..., 1.5}, full data, other parameters refit;
- rho fitted per fold and on all data;
- completeness vs ML, same 10 folds and ML predictor as before, with paired bootstrap differences
  CPT_rho - CPT_share, CPT_rho - CPT_CU, CPT_share - CPT_CU, GDTS_rho - CPT_rho;
- recovery: simulate CPT_rho at rho = 0, 0.5, 1 (other parameters at the all-data fit) on the
  corpus's stimuli and counts, 3 replicates each, refit, and report the recovered rho;
- restrictiveness of CPT_rho and CPT_CU, 100 draws, as before.

**What "certain of how it works" means here, for the sealed test:**
1. rho recovers in simulation (within 0.15 of truth at each of 0, 0.5 and 1) on the corpora used.
2. The profile picks a consistent rho across corpora (intervals overlapping), or a stated law
   explains the differences.
3. CPT_rho or CPT_share beats contextual utility, with a paired interval excluding zero; otherwise
   the sealed test would test Wilcox's idea, and should be framed that way.
The sealed test is designed only after these are read, and only with the owner's go-ahead.

### Result (2026-11-01; `results_rho/`)

All six Jobs ran on NRP at the first attempt.

| Corpus | Stake spread (max/min) | rho, all data | rho over folds | Profile: rho = 1 worse by (milli-nats) |
|---|---|---|---|---|
| CPC18 | 242 | 0.73 | 0.67 to 0.76 | 1.9 (best 0.75) |
| gp2012 | 12 | 0.79 | 0.45 to 0.89 | 0.8 (best 0.75) |
| zilker2020 | 12.5 | 0.92 | 0.87 to 0.99 | 0 (best 1.0) |
| babula2018 | 2.5 | 0.96 | 0.78 to 1.54 | 0 (best 1.0; flat) |
| pachur2018 | 10 | 1.08 | 1.00 to 1.14 | 0 (best 1.0) |
| pachur2017 | 12.5 | 1.39 | 1.30 to 1.52 | 0.75 (best 1.5) |

Completeness vs ML, pooled, with paired differences:

| | Value [95%] |
|---|---|
| CPT_rho (free rho) | 0.959 [0.913, 1.013] |
| CPT_share (rho = 1) | 0.967 [0.922, 1.022] |
| CPT_CU (Wilcox contextual utility) | **0.987** [0.941, 1.043] |
| CPT_rho − CPT_unit | +0.057 [+0.033, +0.082] |
| CPT_rho − CPT_share | −0.008 [−0.021, +0.001] |
| CPT_rho − CPT_CU | −0.028 [−0.054, −0.005] |
| CPT_share − CPT_CU | −0.019 [−0.042, +0.002] |
| GDTS_rho − CPT_rho | −0.061 [−0.099, −0.032] |

Restrictiveness: CPT_rho 0.891 to 0.979 by corpus, CPT_CU 0.893 to 0.984; the two match closely.

The three conditions set before the run:

1. **Recovery: met, with one marginal miss.** 53 of 54 refits land within 0.15 of the true rho; one
   pachur2017 replicate at rho = 0.5 recovered 0.655.
2. **A consistent rho: not met.** CPC18's folds (0.67 to 0.76) and pachur2018's (1.00 to 1.14) do not
   overlap, and pachur2017 sits above 1. Partial scaling shows clearly only on CPC18, the one corpus
   whose stakes span a wide range (242-fold); the other corpora span 2.5- to 12.5-fold, which may be
   too narrow to tell partial from full. One wide corpus cannot establish that law.
3. **Beating contextual utility: not met.** Wilcox's model is the most complete of the five, ahead
   of free rho by 0.028 [0.005, 0.054] and level with full stake scaling. It is ahead on CPC18 (0.98 vs
   0.93) and gp2012 (1.08 vs 0.99); stake scaling is ahead on pachur2018 and zilker2020.

What this says:

- **Scaling each problem's outcomes is real and large** (+0.057 over the one-unit coding), but a free
  partial exponent adds nothing out of sample over full scaling.
- **The existing contextual-utility model captures the gain as well or better.** Its scale is the
  range of utilities in the problem, not the stake, and it handles mixed gambles by spanning losses.
- **GDTS gains nothing from rho** (0.898, against 0.899 with share coding).
- **Not ready for a sealed test.** Conditions 2 and 3 fail. A sealed test of stake^rho now would test
  a model that a known one already matches.

What might be worth exploring next (not run): the same partial exponent on the utility range
(contextual utility with range^rho), to see whether partial scaling holds inside Wilcox's form, and
whether one law covers risky choice and the menus result (range scaling, rho 0.36 to 0.53). The
cross-domain law, not the scaling in one domain, is what the geometry would add.

## Diameter scaling: Wilcox inside the geometry (exploration)

Written 2026-11-01, before any fit. Owner: "why can't we incorporate Wilcox into our model?" then
"yes, run it". Same six spent corpora; exploration only.

**The law.** logit = theta * dC / D^rho: dC is the difference between the two options (CPT value or
GDTS cost), D the problem's diameter, the spread between its best and worst outcomes measured in the
same terms. rho = 1 is Wilcox's contextual utility; rho = 0 is no context scaling. The menus work
fitted the same form with D the menu's range: Molter rho 0.526, Gluth (sealed) 0.356 [0.314, 0.389].

**Models (`explore_cu.py`).**
- CPT_CUr: CPT values on the one-unit coding, D = range of v over the problem's outcomes, rho free
  (6 parameters). Nests CPT_unit (rho = 0) and CPT_CU (rho = 1).
- GDTS_D: GDTS costs on the one-unit coding, D = range of outcomes in units, rho free (7).
- Baselines: CPT_unit, CPT_share, CPT_CU, GDTS (share coding).

**Per corpus, as before:** profile log-loss for CPT_CUr over rho in {0, 0.125, ..., 1.5}; rho per
fold and on all data; completeness vs ML on the same folds, paired differences CPT_CUr − CPT_CU,
CPT_CUr − CPT_share, CPT_CU − CPT_share, GDTS_D − GDTS, GDTS_D − CPT_CUr; recovery of CPT_CUr at
rho = 0, 0.5, 1; restrictiveness of CPT_CUr and GDTS_D.

**Pooled rho.** The six profiles summed in total nats (per-choice log-loss times choices); the
pooled rho is the grid minimum, with an approximate 95% interval where the summed profile stays
within 1.92 nats of it. Also per corpus, the same within-1.92 interval.

**Conditions, fixed now, for considering a sealed test:**
1. Recovery within 0.15 of truth at rho = 0, 0.5 and 1.
2. One rho across risky corpora: the per-corpus intervals overlap a common value.
3. CPT_CUr at least level with CPT_CU (paired interval includes or exceeds 0); otherwise the
   free exponent adds nothing over Wilcox.
4. Cross-domain: the pooled risky rho interval overlaps the menus range [0.31, 0.53]. If it sits
   near 1, risky choice and menus scale differently and there is no single law, as posed.

**Known confound.** With power values, D^rho scales like stake^(alpha*rho) and dV like stake^alpha,
so rho trades off against alpha; it is separated through mixed gambles and the shape within a
problem. The recovery check covers this. The menus rho has its own confound (with two options
gap/range^rho = gap^(1-rho)), so condition 4 compares two estimates each with a known weakness.

### Result (2026-11-01; `results_cu/`)

All six Jobs ran on NRP at the first attempt.

Completeness vs ML, pooled, with paired differences:

| | Value [95%] |
|---|---|
| **CPT_CUr (CPT values, diameter scaling, free rho)** | **0.999** [0.955, 1.056] |
| CPT_CU (Wilcox, rho = 1) | 0.987 [0.941, 1.043] |
| CPT_share | 0.967 [0.922, 1.022] |
| GDTS / GDTS_D | 0.899 / 0.886 |
| CPT_CUr − CPT_CU | **+0.013** [+0.004, +0.022] |
| CPT_CUr − CPT_share | +0.032 [+0.014, +0.051] |
| GDTS_D − GDTS | −0.013 [−0.038, +0.008] |
| GDTS_D − CPT_CUr | −0.113 [−0.155, −0.083] |

rho for CPT_CUr (profile minimum and within-1.92-nats interval, grid step 0.125; all-data fit):

| Corpus | Profile rho [interval] | All-data rho | Folds | rho = 1 worse than 0.75 by (nats) |
|---|---|---|---|---|
| CPC18 | 0.75 [0.75, 0.75] | 0.73 | 0.70 to 0.75 | 91.0 |
| zilker2020 | 0.625 [0.625, 0.625] | 0.65 | 0.62 to 0.69 | 287.6 |
| pachur2017 | 0.625 [0.625, 0.75] | 0.65 | 0.61 to 0.71 | 20.3 |
| babula2018 | 0.875 [0.75, 0.875] | 0.84 | 0.74 to 0.93 | 20.9 |
| gp2012 | 0.875 [0.875, 0.875] | 0.93 | 0.89 to 0.96 | −19.0 |
| pachur2018 | 0.875 [0.875, 1.0] | 0.91 | 0.80 to 0.99 | −1.8 |
| **Pooled** | **0.75** [0.75, 0.75] | | | 399 |

Restrictiveness: CPT_CUr 0.87 to 0.97 by corpus, GDTS_D 0.92 to 0.99.

Conditions set before the run:

1. **Recovery: met.** Every refit within 0.15 of truth at 0, 0.5 and 1 on all six corpora.
2. **One rho across corpora: not met, narrowly.** Every corpus puts rho below 1 except pachur2018,
   whose interval reaches 1. The per-corpus values span 0.63 to 0.93, much tighter than the stake
   exponent (0.73 to 1.39), but the intervals do not share a common grid value (zilker2020 and
   pachur2017 at 0.625, gp2012 and pachur2018 at 0.875).
3. **At least level with Wilcox: met, and better.** CPT_CUr beats contextual utility by 0.013
   [0.004, 0.022], and is the most complete model in this work.
4. **Overlap with menus: not met as posed.** The pooled rho, 0.75, is above the menus range
   [0.31, 0.53].

What this says:

- **Partial diameter scaling improves on Wilcox.** Full contextual scaling (rho = 1) is rejected by
  the profile in four of six corpora; the pooled profile prefers 0.75 over 1 by 399 nats. Choice
  sensitivity falls with the problem's spread in utility, but less than proportionally:
  "anchored but leaky", as in menus.
- **The gain lives with CPT's values and weights, not GDTS's costs.** Diameter scaling does
  nothing for GDTS (−0.013, n.s.).

**Post-hoc, not a condition: the units of rho.** The risky rho divides a utility range, and utility
grows like outcome^alpha, so in raw-outcome units the exponent is about alpha × rho. The menus rho
was fitted on raw attribute ranges. alpha × rho by corpus: 0.37 (zilker2020), 0.38 (pachur2017),
0.40 (gp2012), 0.51 (CPC18), 0.68 (pachur2018), 0.71 (babula2018); four of six fall inside the
menus range [0.31, 0.53]. This conversion was found after seeing the results, ignores beta for
losses, and the menus rho carries its own confound, so it is a hypothesis for the next design, not
support for a single law.

**Readiness for a sealed test.** By the conditions as written, not yet: 2 and 4 fail. What a
sealed test would need to fix in advance: which units rho is stated in (utility range, or raw range
via alpha × rho), and one frozen value, then a fresh risky corpus and a fresh menus dataset.

## Building confidence on the spent data (exploration)

Written 2026-11-01, before any fit. Owner: "Why not build confidence on previous datasets first?",
then "go ahead".

**Two corrections to the diameter-scaling reading, found while designing this, before any new fit.**

- Condition 4 compared the risky rho, fitted on choice rates pooled over participants, with the menus
  range [0.31, 0.53], which comes from per-participant medians (Gluth 0.36, Molter 0.55). Pooled over
  participants, Molter's rho was 0.84 (`../menus/DEVELOPMENT.md`, round 2). The like-for-like
  comparison is pooled against pooled. Condition 4 as written stays failed; the comparison below is
  the corrected one, stated as such.
- The post-hoc alpha × rho conversion assumed the menus rho was in raw outcome units. It is not: the
  menus model scales gaps in the coordinates (W(p), (m/20)^alpha), which already carry a power on
  magnitude. The conversion is withdrawn.

### A. Risky choice, leave one corpus out (`confidence.py risky`)

A rehearsal of the sealed test on the six spent corpora.
- Per corpus: profile of CPT_CUr on all data over rho in {0, 0.025, ..., 1.5} (other parameters
  refit), and 10-fold CV predictions (same folds and ML predictor as before) with rho fixed at each
  value in {0.40, 0.425, ..., 1.10}.
- For each held-out corpus, rho is frozen at the minimum of the other five corpora's summed profiles
  (total nats), and its held-out completeness at that rho is compared with rho = 1 (Wilcox).
- **A passes** if frozen rho beats rho = 1 on held-out completeness, pooled over the six held-out
  corpora with a paired 95% interval above 0, and in at least four of six corpora.

### B. Menus, pooled over participants (`confidence.py menus`)

Molter 2022 (9,000 trials, three available options) and Gluth 2018 (all four experiments; HV and LV
choices, the distractor shown but not available; trials where it was pressed, or no choice was
made, are dropped). The sealed menus model RNG (`../menus/menus_models.py`), fitted pooled over
participants with rho fixed.
- Per dataset: profile over rho in {0, 0.025, ..., 1.5} on all trials, and 5-fold CV over
  participants with rho fixed at each of {0, 0.40, 0.425, ..., 1.10}.
- **Corrected comparison:** each menus dataset's profile interval (within 1.92 nats) against the
  pooled risky interval.
- **Transfer:** rho frozen from the six risky corpora (summed profiles), applied to each menus
  dataset, against rho = 0 (additive) and rho = 1 (full range scaling), paired over participants.
- **B passes** if, in both menus datasets, the risky-frozen rho beats both rho = 0 and rho = 1 on CV
  log-loss with paired 95% intervals excluding 0.
- Reported, not graded: the reverse transfer, rho frozen from the two menus datasets, applied to the
  risky corpora against Wilcox.

### What follows

- A and B pass: a cross-domain sealed test is designed (one frozen rho, fresh risky and menus data).
- A passes, B fails: the sealed test is risky-only (Wilcox plus a frozen rho on a fresh risky
  corpus); the cross-domain law is not supported.
- A fails: no sealed test of diameter scaling.

Known limits: Gluth's trials are mostly two available options, where rho partly acts as curvature
of the gap (`../menus/RESULTS.md`, H4); the risky ranges are over outcomes, not options, so that
confound does not carry over the same way. All eight datasets are spent.

### Result (2026-11-01)

Run on NRP (`submit_nrp.py`, tags geconf and geconf2; Gluth split into six parts over the rho grid).
Outputs in `results_conf/`; summary `results_conf/conf_summary.json` from `aggregate_conf.py`.

**A passes, at the minimum.** Frozen rho beats Wilcox on held-out completeness by +0.013
[+0.002, +0.024], pooled over the six corpora, and in 4 of 6.

| held out | frozen rho | completeness, frozen | completeness, rho = 1 | difference [95%] |
|---|---|---|---|---|
| cpc18 | 0.725 | 1.011 | 0.982 | +0.029 [+0.011, +0.048] |
| gp2012 | 0.675 | 1.079 | 1.081 | -0.002 [-0.035, +0.031] |
| pachur2017 | 0.725 | 1.232 | 1.205 | +0.028 [+0.008, +0.053] |
| pachur2018 | 0.725 | 1.140 | 1.144 | -0.004 [-0.029, +0.016] |
| zilker2020 | 0.800 | 0.980 | 0.968 | +0.013 [-0.000, +0.027] |
| babula2018 | 0.725 | 0.557 | 0.543 | +0.014 [-0.023, +0.060] |

The frozen rho is stable across held-out corpora (0.675 to 0.80). Pooled over all six: 0.725
[0.70, 0.725].

**B fails.** Risky-frozen rho 0.725, CV log-loss per participant (lower is better), paired
differences:

| dataset | own rho [interval] | loss at 0.725 / 0 / 1 | vs rho = 0 | vs rho = 1 | beats both |
|---|---|---|---|---|---|
| Molter | 0.85 [0.825, 0.85] | 0.9488 / 1.0412 / 0.9522 | -0.092 [-0.115, -0.068] | -0.003 [-0.046, +0.044] | no |
| Gluth | 0.425 [0.40, 0.45] | 0.5711 / 0.5767 / 0.5807 | -0.006 [-0.008, -0.003] | -0.010 [-0.011, -0.008] | yes |

Molter cannot tell 0.725 from full range scaling. Neither menus interval overlaps the risky one,
and the two menus datasets do not overlap each other (0.85 against 0.425). Pooled, the two menus
datasets put rho at 0.725, the same grid point as the risky corpora, but that is the minimum of two
disagreeing profiles, not a shared value. The reverse transfer (reported only) is therefore the
same rho, and gives +0.014 over Wilcox on the risky corpora.

**Verdict, by the rule written above: A passes, B fails.** The next step is a risky-only sealed test
(Wilcox against CPT_CUr with rho frozen at 0.725 on a fresh risky corpus). The cross-domain law is
not supported. Designing that test waits for the owner.

Before designing it:
- The edge is small (+0.013 completeness pooled; significant in 2 of 6 corpora alone). One fresh
  corpus may not resolve it; a power calculation from the six per-corpus intervals comes first.
- Profile intervals treat every choice as independent. Choices cluster within participants and
  problems, so these intervals are too narrow; the non-overlaps above are not precise.
- Gluth is mostly two available options, where rho partly acts as gap curvature (known limit above).

Fix during aggregation: `wins` was a numpy integer and broke the JSON write; cast to int. No number
changed.

## Power of the risky-only sealed test (2026-11-01)

Owner: "run the power calculation". `power.py`, run on Atlas (21 s); output `results_conf/power.json`.

The test considered: CPT_CUr with rho frozen at 0.725 against Wilcox (rho = 1) on fresh data, passing
when the 95% interval on the completeness difference is above 0. A fresh corpus is simulated by
resampling problems from one spent corpus's held-out per-problem errors. The interval is the
delta-method interval for the ratio; it matches the bootstrap intervals of part A on the real
corpora (e.g. cpc18 [0.0104, 0.0478] against [0.0106, 0.0482]).

**One fresh corpus of N problems, like each spent corpus** (P(interval above 0), 4,000 draws):

| N | cpc18 | gp2012 | pachur2017 | pachur2018 | zilker2020 | babula2018 | mean |
|---|---|---|---|---|---|---|---|
| 50 | .32 | .01 | .46 | .02 | .15 | .02 | .16 |
| 100 | .54 | .02 | .81 | .01 | .34 | .04 | .29 |
| 200 | .81 | .02 | .98 | .00 | .60 | .08 | .42 |
| 300 | .94 | .02 | 1.00 | .01 | .78 | .13 | .48 |
| 500 | .99 | .02 | 1.00 | .00 | .95 | .22 | .53 |
| 1200 | 1.00 | .02 | 1.00 | .00 | 1.00 | .50 | .59 |

Power depends on which kind of corpus the fresh one is, not mainly on its size. In two of the six
(gp2012, pachur2018) the edge over Wilcox is zero, and no size helps. Averaged over the six, power
stays below 0.6 even at 1,200 problems; the spent corpora have 51 to 230.

**Several fresh corpora pooled, as in part A** (k corpora drawn from the six, each at its own size):

| k | 1 | 2 | 3 | 4 | 6 | 8 |
|---|---|---|---|---|---|---|
| power | .34 | .42 | .47 | .55 | .68 | .75 |
| median 95% half-width | .022 | .017 | .014 | .012 | .010 | .009 |

The pooled edge is about +0.013, and the half-width falls below it only at about four corpora.
80% power needs roughly nine or ten fresh corpora of the usual size.

Limits: the spread between corpora is estimated from six corpora only; each simulated corpus keeps
its source corpus's choices per problem; the effect sizes are the leave-one-out estimates, not
known true values.

Reading: a sealed test on one fresh corpus would most likely fail even if diameter scaling is real
on average, and a failure would say little. A sealed test that can carry weight needs many fresh
corpora, or a claim restated as "beats Wilcox on average across corpora" and tested pooled. Which,
and whether at all, is the owner's decision.

## Fresh risky corpora: candidates, designs checked from the papers (2026-11-01)

Owner: "find fresh risky choice corpora we could pool", then "verify the four candidates' designs from
their papers". Designs read from the papers only; no data file was downloaded or opened.

| corpus | problems | people | outcomes | domain | fits the test? |
|---|---|---|---|---|---|
| Spiliopoulos & Hertwig 2023, JEP:G (OSF p924g) | 120 pairs, same for all | 96 | 1-4 per prospect, 0-200 | gains | yes (description session) |
| Rieskamp 2008 Study 2 (OSF eypgb, via Nilsson et al. 2011) | 180 pairs, random, no dominance | 30 | 2 per option, -100 to 100 | 60 gain, 60 loss, 60 mixed | yes |
| Baillon, Bleichrodt & Spinu 2020, MS (INFORMS supplement) | 70, fixed optimal design, listed in Appendix A | 139 | 1-4 per option, all positive | gains | yes, with a caveat |
| Frydman & Jin 2022, QJE (Dataverse, CC0) | 600 trials each, payoffs drawn per trial; 30 common problems per condition | 149 analysed | lottery (X, .5; 0) vs sure C | gains | poorly |

- Spiliopoulos & Hertwig: description session first, on its own day; incentivised (two lotteries paid);
  EV gap at most 10% of the larger EV, so problems are hard. Experience and belief sessions follow on
  later days and are not used.
- Rieskamp: design from Kellen et al. (2020, Cognitive Psychology, sec. 6); one pair paid. Whether
  pairs repeated across sessions is not confirmed (the original paper is closed access).
- Baillon et al.: prospects shown as bars sized by probability with payoffs printed (Fig. 1), not as
  text; one-third chance of real payment, stakes up to a week's pay in Moldova. The display differs
  from the other corpora.
- Frydman & Jin: only the 30 common problems repeat across people, in two volatility contexts that
  the authors show shift behaviour; p is always 0.5. As a problem-rate corpus it is 30 or 60 problems
  under a context manipulation the model does not represent.

Three usable corpora, about 370 problems. By the power table, pooled power with three or four corpora
like the spent ones is about 0.47-0.55.

## Power of a proposed new study (2026-11-01; `power_study.py`, `power_tree.py`, `aggregate_power.py`)

A study built to vary the range: 60 base pairs (20 gain, 20 loss, 20 mixed) each at scales k = 1, 4,
16, three Latin-square lists of 60 choices; then a tree section of 48 adaptive choices (six Psi
staircases: 50% of +-20k against a sure amount, k = 1, 4, 16). Simulated people follow CPT_CUr with
rho = 0.725 or 1 and the other parameters fitted to each of the six spent risky corpora; sensitivity
varies between people by exp(N(0, sigma)), sigma = 0 or 0.5. 60 studies per cell, N = 60-240. Run
on NRP, one pod per cell.

### The estimand

With sigma = 0.5 the freely fitted rho comes out near 0.757 when every simulated person has 0.725
(sigma = 0: 0.722-0.730). The person-clustered SE matches the spread of the estimates, so this is
not an SE problem: pooling over people of different sensitivity flattens the high-stakes problems
most, and the pooled rho sits nearer Wilcox than any individual's. The frozen 0.725 was fitted to
pooled rates, so it is the same, population-level, quantity. Adopted (owner, 2026-11-01): the rho
claims are directional (interval excludes 1 and 0), 0.725 is checked against a band of +-0.05
(fails if the 95% interval is wholly outside; confirmed if the 90% interval is wholly inside), and
a mixed logit with a random sensitivity per person is a secondary, individual-level estimate.
Point tests of 0.725 rejected it in up to 44% of studies at sigma = 0.5, N = 240.

### Result (ladder 24/24 cells, tree 22/24)

Means over the six corpora; per-corpus minima in `results_conf/power_new_study_partial.json`.

| | N=60 | 120 | 180 | 240 |
|---|---|---|---|---|
| ladder, rho=.725: excludes 1 and 0 (sigma 0 / .5) | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| ladder, rho=.725: H1 alone (sigma 0 / .5) | .91 / .87 | 1.00 / .97 | 1.00 / 1.00 | 1.00 / 1.00 |
| ladder, rho=.725: band fails .725 (sigma 0 / .5) | .00 / .01 | .00 / .00 | .00 / .00 | .00 / .01 |
| ladder, rho=.725: 90% interval inside band (sigma 0 / .5) | .01 / .01 | .28 / .11 | .50 / .21 | .69 / .27 |
| ladder, rho=1: rejects rho=1 (sigma 0 / .5) | .05 / .06 | .04 / .03 | .05 / .08 | .04 / .10 |
| ladder, rho=1: band fails .725 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| tree, rho=.725: exponent differs from 0 (sigma 0 / .5) | 1.00 / .99 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| tree, rho=1: exponent differs from 0 (sigma 0 / .5) | .08 / .05 | .04 / .04 | .05 / .03 | .06 / .05 |
| tree, rho=.725: excludes 1 (sigma 0 / .5) | .81 / .49 | .94 / .69 | 1.00 / .77 | 1.00 / .80 |
| tree, rho=.725: band fails .725 (sigma 0 / .5) | .01 / .09 | .00 / .12 | .00 / .12 | .00 / .16 |

H1 pooled with three stand-in public corpora passes .74-.85 when rho = .725, limited by the
stand-ins; it also passes .09-.12 when rho = 1, because the stand-ins are resampled from spent
corpora where .725 beat Wilcox, so that rate is not the study's false-alarm rate.

Reading: 120 participants carry every primary claim (ladder excludes Wilcox and plain CPT; H1 alone;
tree exponent against Wilcox). Confirming 0.725 to +-0.05 succeeds in at most 27% of studies (N = 240) when
people differ. The tree's rho is a cross-check only: it is weak and over-fails 0.725 when people
differ.
