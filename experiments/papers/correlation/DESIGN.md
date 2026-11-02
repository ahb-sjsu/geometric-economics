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

The exact set is `stimuli.py` (seed 20261102): 40 riskless pairs, 32 single-attribute lotteries, 24
correlation pairs and 8 attention checks. The crossing set described below is not built yet. The
rehearsal may still change the set before it is registered.

- **Charity.** Each participant first picks one charity from a short list, so that charity points
  carry value.
- **Payment.** One trial is drawn and paid for real. Self points go to the participant and charity
  points are donated, at the same rate per point. Receipts for the donations are published. A coin
  flip resolves any lottery. There is no deception.
- **Block R, riskless calibration, about 40 choices.** Pairs of sure bundles spread across directions
  in the shortfall plane. They measure the tilt and shape of `P`.
- **Block S, single-attribute lotteries, about 32 choices.** Even-odds lotteries over self points
  against sure self points, at four charity levels (charity shortfall 0 and three larger values), and
  the mirror over charity points. The `b = 0` cells measure `κ` alone, because the metric adds nothing
  there.
- **Block X, correlation pairs, about 24 choices.** Correlated against anticorrelated even-odds
  lotteries with equal marginals, at several base points and spreads. Sides are counterbalanced.
- **Attention checks.** About 8 dominated pairs.
- **Ordering.** Block R comes first. Blocks S and X are interleaved at random, so the correlation pairs
  do not read as a family.
- **Avoiding equality crossings.** In the main set every charity shortfall exceeds every self
  shortfall, so no outcome crosses `m = c` and inequality aversion predicts nothing. A smaller,
  registered secondary set does cross, to show inequality aversion's signature if it is there.
- **Length.** About 25 to 30 minutes, online or in the lab.

## Analysis (to be registered)

- **Calibration set.** Block R plus the `b = 0` and `a = 0` cells of block S.
- **Test set.** The other cells of block S, plus block X.
- **Fitting.** Each model is fit per person on the calibration set, hierarchically, and predicts the
  test set with no refit.

Intervals are clustered by person, the unit `P` lives on. Margins are set in noise units by the
rehearsal.

- **H1.** Late-contraction Mahalanobis beats early contraction on held-out log-loss. Early contraction
  is the additive value for equal-marginal pairs.
- **H2.** It beats RDU on additive value per outcome, calibrated on the same set.
- **H3.** It beats EU with a concave aggregator, calibrated on the same set.
- **H4.** Across people, the size of both effects rises with `det(P)` from block R. This is a
  rank-correlation test.
- **Model-free checks, reported first.**
  - Does the choice rate in block X depart from even odds?
  - Does risk attitude over self points change with the charity level?
  - If both are null, additive value wins and the metric is not detected for these attributes.

The registered secondary is the crossing set, scored against inequality aversion.

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
3. **Human study**, sealed with a signed tag before recruitment.

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
- The ideal point: fixed at the top of the scales (this draft) or estimated. Under GET's uniqueness
  theorem the ideal is identified up to the metric's kernel.
- Whether to keep the crossing set.
- Sealing.
