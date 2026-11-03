# Cross-attribute risk attitudes: a test of a full Mahalanobis metric with late contraction

**Status: DRAFT, 2026-11-02.** Not registered, not sealed, nothing run. Sealing needs the owner's OK.

## Why this design

Every test of GDT against CPT in risky choice (Part II on CPC18, Psych-101, strata, strata2) used a
diagonal metric (`../../papers-archive/strata/strata_models.py:55, 75, 128`), contracted each option to one cost before
choice, and used coordinates chosen by hand (EV and SD; g, l, π+ and π−). Each lottery was reduced to
expectations over its outcomes before the metric acted. That is the reverse of the programme's own
rule of deferred contraction (Geometric Ethics v1.24, §15.8). And in money-only lotteries a metric has
one attribute to act on, so those tests could not see one. The full metric has been fit only twice:
Part II's low-rank legs, where it beat the diagonal, and Part III's learned metric, where it beat a
linear score.

Here every outcome carries two attributes, so the metric acts inside each outcome before the outcomes
are combined. A full Mahalanobis metric with late contraction then has two consequences that no
incumbent shares in this form.

1. **Correlation attitude.** A definite preference between two lotteries with identical marginals that
   differ only in how the attributes line up across outcomes.
2. **Background dependence.** Risk attitude over one attribute changes with the level of the other.

Both are fixed by the metric that riskless choices measure. Neither needs a new free parameter.

## Model

Attributes are self points `m` and charity points `c`, each on a 0 to 100 scale. The ideal is
`r = (100, 100)`, shown on screen as the top of each scale and the same on every trial, so the
reference does not move with the menu (Theorem 2 of the archived theory draft assumes a fixed reference). An
outcome `s` has shortfall `Δ_s = (a_s, b_s) = (100 − m_s, 100 − c_s)`. A lottery is a rank-2 object,
outcome index `s` by attribute index `μ`.

- **Cost of an outcome.** `C_s = sqrt(Δ_sᵀ P Δ_s)`, with `P` symmetric positive definite and full
  (`P11`, `P12`, `P22`).
- **Late contraction.** `V(L) = Σ_s p_s f(C_s)`, with `f(C) = C^κ` and `κ ≥ 1`. The metric acts first,
  then the outcomes are summed.
- **Early contraction**, the order the risky-choice tests used. `Δ̄ = Σ_s p_s Δ_s`, then `C(Δ̄)`,
  optionally with per-attribute spreads. Two lotteries with the same marginals get the same value.
- **Choice.** `Pr(L1 over L2) = σ((V(L2) − V(L1)) / T)`. A sure bundle is a one-outcome lottery, so
  riskless and risky choices share one model.

## What the model predicts

Write `U = −f(C)` as a function of the attributes. Correlation aversion is `∂²U/∂m∂c < 0` (Richard
1975). Background dependence is a change of risk attitude over `m` with `c`.

**Correlation.** For a shortfall in both attributes (`a, b > 0`),

    ∂²C/∂a∂b = −det(P) · a · b / C³.

- With `κ = 1` (expected distance), `∂²U/∂m∂c = det(P)·a·b / C³ > 0` for every positive-definite `P`.
  The evaluator prefers the lottery whose outcomes are both good or both bad. The strength is
  proportional to `det(P)` and vanishes when `P` has rank one, because a rank-one metric is a linear
  score.
- With `κ = 2` (expected squared distance), `∂²U/∂m∂c = −2·P12`. The preference turns to the
  anticorrelated lottery exactly when `P12 > 0`.
- In general, `∂²U/∂m∂c = −f''(C)·C_a·C_b + f'(C)·det(P)·a·b / C³`. A convex `f` pushes toward
  correlation aversion, and the metric's curvature pushes toward correlation seeking.

**Background dependence.**

    ∂²C/∂a² = det(P) · b² / C³.

The evaluator's aversion to risk in self points is `f''(C)·C_a² + f'(C)·det(P)·b²/C³`.

- The first term is the same at every charity level.
- The second is zero when charity is at its ideal (`b = 0`). It grows with the charity shortfall, peaks
  near `b = √2·a`, and then falls slowly.
- Risk attitude over charity points mirrors this.

**Who shows it.** Both effects scale with `det(P)`. People who trade the two attributes off should
show them, and people who weigh only one attribute (`P` close to rank one) should show neither.

**Worked numbers**, for illustration only, with `P11 = P22 = 1`. The correlated lottery pays shortfalls
(2, 2) or (6, 6) with even odds. The anticorrelated one pays (2, 6) or (6, 2). The table gives the
anticorrelated lottery's value minus the correlated one's, in cost units. Positive means the
correlated lottery is preferred.

| `P12` | `κ = 1` | `κ = 2` |
|---|---|---|
| 0 | +0.67 | 0 |
| +0.5 | +0.28 | −8 |
| −0.5 | +1.29 | +8 |

Background dependence with `P = I` and `κ = 1`: an even-odds shortfall of 2 or 6 in self points,
against a sure shortfall of 4. The lottery's extra expected cost is 0 at charity shortfall `b = 0`,
0.18 at `b = 4`, 0.18 at `b = 8` and 0.11 at `b = 16`.

## Competitors

| Model | Correlation pair | Risk over self as the charity level changes |
|---|---|---|
| Additive EU, `u(m) + v(c)` | indifferent | unchanged |
| Early-contraction GDT (the tested version) | indifferent | unchanged |
| RDU or CPT on additive value per outcome (late contraction, no metric) | anticorrelated preferred if `w(0.5) < 0.5` | unchanged |
| EU with a concave aggregator, `φ(v(m) + w(c))` | anticorrelated preferred | changes, through `φ` only |
| Inequality aversion, outcomes never cross `m = c` | indifferent | unchanged |
| Inequality aversion, outcomes cross `m = c` | correlated preferred (equal outcomes) | changes at the crossing |
| Multiattribute EU with free `u(m, c)` | either sign | either, with no link to riskless choices |
| **Late-contraction Mahalanobis** | **set by `P` and `κ` from the calibration blocks** | **rises with the other shortfall, by `det(P)`, then falls slowly** |

The two strongest rivals are RDU on additive value and EU with a concave aggregator.
- **RDU on additive value** produces correlation aversion without a metric. It cannot produce
  background dependence.
- **EU with a concave aggregator** produces both effects, but its correlation effect is always
  aversion. Its effect sizes are not tied to the riskless tradeoffs.

## Stimuli and procedure

The exact set is `stimuli.py` version 4 (seed 20261102), 140 trials in all.
- **The main set, 120 trials.** 40 riskless pairs, 48 single-attribute lotteries, 24 correlation pairs
  and 8 attention checks. Version 2 had 32 single-attribute lotteries; version 3 added 16 at the
  ideal, because `κ` fitted from 4 per attribute was biased upward (`REHEARSAL.md`).
- **The crossing set, 20 trials (version 4).** Described below.

The rehearsal may still change the set before it is registered.

- **Charity.** Each participant first picks one charity from a short list, so that charity points
  carry value.
- **Payment.** One trial is drawn and paid for real. Self points go to the participant and charity
  points are donated, at the same rate per point. Receipts for the donations are published. A coin
  flip resolves any lottery. There is no deception.
- **Comprehension quiz,** before block R. Four questions: what self and charity points become, how a
  lottery is resolved, and how many trials are paid. Two attempts (`PILOT.md`).
- **Block R, riskless calibration, about 40 choices.** Pairs of sure bundles spread across directions
  in the shortfall plane. They measure the tilt and shape of `P`.
- **Block S, single-attribute lotteries, 48 choices.** Even-odds lotteries over self points against
  sure self points, at four charity levels (charity shortfall 0 and three larger values), and the
  mirror over charity points.
  - At the other attribute's ideal there are 12 per attribute, with varied spreads and levels. These
    cells measure `κ` alone, because the metric adds nothing there.
  - Off the ideal there are 4 per level.
- **Block X, correlation pairs, about 24 choices.** Correlated against anticorrelated even-odds
  lotteries with equal marginals, at several base points and spreads. Sides are counterbalanced.
- **Attention checks.** About 8 dominated pairs.
- **Ordering.** Block R comes first. Everything else is interleaved at random, so the correlation
  pairs do not read as a family.
- **Avoiding equality crossings in the main set.** Every charity shortfall exceeds every self
  shortfall, so no outcome crosses `m = c` and inequality aversion predicts nothing there.
- **The crossing set crosses on purpose,** to show inequality aversion's signature if it is there. It
  is a registered secondary and never enters H1 to H4.
  - **8 crossing correlation pairs.** The correlated option pays an equal split in both outcomes
    (shortfalls 10 and 50, 20 and 60, 30 and 70, 40 and 80 on both attributes). The anticorrelated
    option pays one split favouring self and one favouring the charity. Both orders are shown.
  - **12 straddle lotteries.** An even-odds lottery against its expected value on one attribute,
    with the other attribute held at 50. Sure shortfalls are 25, 50 and 75, with spreads 10 and 20.
    At 50 the outcomes straddle `m = c`. The 25 and 75 cells are controls with the same spread.
- **Length.** About 35 minutes for 140 trials, online or in the lab.

## Analysis (to be registered)

- **Calibration set.** Block R plus the `b = 0` and `a = 0` cells of block S.
- **Test set.** The other cells of block S, plus block X.
- **Fitting.** Each model is fit per person on the calibration set, hierarchically, and predicts the
  test set with no refit.
- **Inclusion.** Finished the session, passed the comprehension quiz within two attempts, and chose the
  dominated option in at most 2 of the 8 attention checks (`PILOT.md`). Recruitment continues until n
  people qualify.
- **Sample size.** n is 120, 160, 200 or 240, chosen from the pilot by a rule sealed with this design
  (`PILOT.md`).

Intervals are clustered by person, the unit `P` lives on.

**The margin is 0.005 nats per trial,** set by the owner on 2026-11-02 from rehearsal version 3. Each
of H1 to H3 passes when the upper end of the 95% interval on GEO's held-out log-loss difference lies
below −0.005.
- At margin 0, the claim passed in one CAG study of 50 at each n.
- At 0.005 it passed in none.
- The cost was 2 points of power at n = 120 under distance-like cost (`REHEARSAL.md`).

- **H1.** Late-contraction Mahalanobis beats early contraction on held-out log-loss. Early contraction
  is the additive value for equal-marginal pairs.
- **H2.** It beats RDU on additive value per outcome, calibrated on the same set.
- **H3.** It beats EU with a concave aggregator, calibrated on the same set.
- **The claim that the metric is supported requires H1, H2 and H3 together.** Each H is still reported
  on its own, but none alone counts as support. The rehearsal (`REHEARSAL.md`, version 2) shows why
  each is needed.
  - **H3 guards against a concave aggregator.** With CAG as the truth, the fitted GEO mimics the true
    model almost exactly (median held-out log-loss 0.511 against CAG's 0.508). It beat RDU (0.600) in
    every simulated study at n = 60, 120 and 200, so H2 passed while the metric was false. H3 failed
    in every one of those studies.
  - **H1 guards against additive value.** With linear additive value as the truth, H2 and H3 passed
    together in 24%, 34% and 38% of studies at n = 60, 120 and 200. RDU's and CAG's noisy fits
    predict correlation attitudes that are not there, and GEO wins those comparisons by default. H1
    failed in every one of those studies, because EARLY, the metric on the mean bundle, contains
    linear additive value.
  - With all three required, the conjunction passed in no simulated study under any of the four truths
    without the metric (EARLY, RDU, CAG and ADD, 50 studies each at every n). Under EARLY, H2 again
    passed by default in 54%, 74% and 82% of studies, while H1 and H3 never did.
  - The registration states the three-way conjunction as the claim.
- **Power depends on the kind of cost.** Figures are from rehearsal version 3, with the stimulus set
  above, at n = 60, 120 and 200.
  - If cost behaves like distance (`κ = 1`), the conjunction passed in 96%, 100% and 100% of studies at
    margin 0, and in 84%, 98% and 100% at margin 0.005. Version 2's stimuli gave 70%, 92% and 96%.
  - If it behaves like squared distance (`κ = 2`), it passed in only 32%, 48% and 68% at margin 0, and
    in 16%, 30% and 46% at 0.005. Squared distance has no background dependence. Its correlation
    attitude takes its sign from `P12`, which varies across people. So little separates it from
    EARLY's even odds.
  - Under the four truths without the metric, the conjunction passed in none of the 200 studies per n
    at margin 0.005. At margin 0 it passed in one, a CAG study.
  - Rehearsal version 4 added the crossing set and IA as a truth. The conjunction again passed in no
    study under the five truths without the metric (EARLY, RDU, CAG, ADD and IA) at margin 0.005. It
    passed in 84%, 94% and 100% under GEO1.
  - The design is therefore powered against distance-like cost: 98% at n = 120 with margin 0.005. A
    null result does not rule out squared distance.
- **H4. Comparative test across people.** Each fitted model predicts each person's preference for the
  correlated option in block X from the calibration set alone. GEO's predictions must track the
  observed preferences better than RDU's and CAG's do.
  - The statistic is GEO's Spearman correlation with the observed preferences, minus the larger of
    RDU's and CAG's. It passes when the lower end of a bootstrap interval over people is above zero.
  - An earlier, non-comparative version required only that the size of the effects rise with
    `det(P)`, tested through GEO's correlation alone. In the version 1 rehearsal that test passed in
    every simulated study at n = 200 when RDU or CAG was the truth, not only GEO. Pessimism, a
    concave aggregator and `κ > 1` all show as risk aversion at the ideal, so GEO's fitted `κ` tracks
    them.
- **Model-free checks, reported first.**
  - Does the choice rate in block X depart from even odds?
  - Does risk attitude over self points change with the charity level? This compares only the 4
    lotteries offered at every level. Comparing all lotteries at the ideal with those off it compared
    different gambles, and gave false positives in rehearsal version 3.
  - If both are null, additive value wins and the metric is not detected for these attributes.
- **Secondary: the population `κ`.** This says whether cost behaves like distance (`κ` near 1) or like
  squared distance (near 2), which is what decides how to read a null on the claim.
  - Method: GEO fitted hierarchically on the calibration set and sampled by NUTS (`hier.py`). It
    reports the posterior median and 95% interval of the population median `κ`.
  - Per-person `κ` is not interpreted. At any feasible session length the per-person estimate is
    biased upward, through small samples and the incidental-parameter problem (`REHEARSAL.md`).
  - A null on the claim with the interval excluding 1 means cost is not distance-like, and the design
    had little power. A null with the interval excluding 2 counts against the metric.
  - In rehearsal version 3 (10 studies per truth, n = 120), the interval excluded 2 in every study
    under GEO1 and covered 1 in 9. Under GEO2 it excluded 1 in every study but covered 2 in only 7,
    so the intervals may be somewhat narrow.
  - **It means something only if GEO is the right model.** In rehearsal version 3 the fitted
    population `κ` was 1.64 under RDU and 1.86 under CAG, because the misspecified GEO absorbs
    pessimism or concavity into `κ`. A null on the claim with a high `κ` therefore cannot tell squared
    distance from those. The H2 and H3 comparisons, and the sign of MF1, have to carry that
    distinction.

**The registered secondary: the crossing set, scored against inequality aversion.**
- **The model (IA).** Inequality aversion in the Fehr-Schmidt form. Over shortfalls it is additive
  value minus a penalty `γ |a − b|`, which is linear inside the main set and kinked at `m = c`. It is
  calibrated, like the other models, on the calibration set alone. The calibration set never crosses,
  but its two regions identify the kink.
- **SH1.** On the crossing set, IA predicts held-out choices better than GEO, at the registered margin
  of 0.005. The reverse, GEO better than IA, is reported too.
- **SH2.** At the straddle lotteries, the lottery-choice rate minus the mean of the same-spread controls
  falls below GEO's zero-fit prediction of that difference. This is the kink.
- **The secondary claim, inequality aversion, requires SH1 and SH2 together.** The figures below are
  from rehearsal version 4, seven truths, 50 studies each at n = 60, 120 and 200.
  - With IA as the truth (`γ` from 0.1 to 0.6), the conjunction passed in every study at every n.
  - Under the six other truths it passed in none.
  - Taken alone, SH1 or SH2 passed in up to 12% of studies under truths without inequality aversion
    (SH2 under EARLY and GEO2). So neither counts alone.
  - **Power depends on the strength of the aversion.** `γ` is the penalty for each point of
    inequality, in units of the participant's own points. At n = 120 the conjunction detected `γ` =
    0.10 in 98% of studies, 0.05 in 26%, and 0.02 in none.
  - So a null rules out strong inequality aversion toward the charity, not weak. For scale, two-person
    money-game estimates correspond to `γ ≈ 0.6`.
- **SH3, reported only.** It asks whether the equal-split option in the crossing pairs is chosen more
  than GEO predicts. Rehearsal version 4 showed it is not specific.
  - The plain form passed in 28% to 58% of studies under GEO1, and in 90% to 100% under ADD.
  - The difference-in-differences form passed in 8% to 18% under GEO1, and in 22% to 66% under ADD.
  - GEO's zero-fit prediction for these pairs, far from the calibration region, is biased. Fitted
    `κ` is too high, so GEO under-predicts correlation seeking.

## Stages

1. **Rehearsal on NRP.** Simulate participants from every model in the table through the exact
   stimulus set. Check three things:
   - `P` and `κ` are recovered;
   - each hypothesis passes when its model is true and fails otherwise;
   - which N gives adequate power at the person level.

   Noise attenuates `det(P)`, and with it the predicted effects, so recovery has to be checked rather
   than assumed. Code: `rehearsal.py` with `models.py`, run on NRP by `submit_nrp.py` and summarised by
   `aggregate_rehearsal.py`. The run record is `REHEARSAL.md`.
2. **Language-model panel, optional.** An instrument check of wording and answer format only. It is
   not evidence about people.
3. **Pilot, 40 people** (`PILOT.md`). It measures the person-level quantities the rehearsal assumed
   and checks the instrument. It reads no test or secondary choice. A power table and a sample-size
   rule are sealed with this design before it runs, and the pilot only says which row of the table
   applies.
4. **Human study.** The design is sealed with a signed tag before the pilot. The n the pilot selects
   is recorded under a second signed tag before recruitment.

## What each result would mean

- **Neither effect.** Value is additive in these attributes. A full metric with late contraction is
  not supported for self and charity points. Other attribute pairs stay open.
- **Correlation aversion without background dependence.** Rank-dependent weighting of per-outcome
  value. Late contraction yes, metric no.
- **Both effects, matching the calibrated `P` and `κ`.** One metric acting inside outcomes, contracted
  late. This is the strongest evidence the programme could get for its first two commitments.
- **Both effects, sizes not matching.** Value is non-additive, but not through this metric.

## Scope

- **Commitment 1, full Mahalanobis.** `P12` and `det(P)` are what the test measures.
- **Commitment 2, the rank-n tensor with deferred contraction.** The test separates metric-then-sum
  from sum-then-metric over the outcome index.
- **Commitment 3, discovered coordinates.** Not addressed. The two coordinates here are given by the
  stimuli. Discovery is a separate exploration, done the way the moral-spectrum-analyzer does it, on
  the spent risky corpora.

## Prior art to read before sealing

None of these has been read for this design yet. The citations are from memory and must be checked.

- Richard (1975), multivariate risk aversion. Correlation aversion is the sign of the cross-partial.
- Epstein and Tanny (1980), increasing generalized correlation.
- Keeney and Raiffa (1976), utility independence. Background dependence is a structured violation of
  it.
- Laboratory measurements of correlation aversion, for example Andersen, Harrison, Lau and Rutström on
  correlation aversion over time, and measurements in the health domain.
- Social preferences under risk: Brock, Lange and Ozbay (2013), and Saito (2013), on ex ante against
  ex post fairness. These matter for the crossing set.

## Open decisions (owner)

- Population and platform, and who runs it.
- The charity list and the point-to-dollar rate.
- The cap on the sample size. The pilot's power table runs to 240 (`PILOT.md`).
- The ideal point: fixed at the top of the scales (this draft) or estimated. Under GET's uniqueness
  theorem the ideal is identified up to the metric's kernel.
- Whether to keep the crossing set. It adds 20 trials, about 5 minutes. In rehearsal version 4 it
  detected inequality aversion in every study and gave no false positive.
- Sealing.
