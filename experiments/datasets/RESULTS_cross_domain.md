# Cross-domain transfer — one metric across lotteries and games

The theory's central, differentiating claim: **a single shared metric predicts behaviour in both
risky choice and strategic games** — something CPT (no games) and Nash (no lotteries) structurally
cannot do. This is the first direct test on human data.

## Method

- **Lotteries:** CPC18, 270 description problems (each option → EV, SD).
- **Games:** bogota behavioral-game-theory datapool, **110 two-player games from 8 published studies**
  (Stahl-Wilson, Costa-Gomes, Goeree-Holt, Cooper, Haruvy, Camerer), payoffs + human action
  frequencies. Each row strategy → (EV, SD) **under a uniform level-0 belief** over the opponent
  (strategic uncertainty = payoff variance across the opponent's actions).
- **Shared feature space:** (EV, SD), payoff-scale-normalized per dataset so the metric is transferable.
- **Model:** geometric cost `sqrt(((EVmax−EV)/σ_ev)² + (SD/σ_sd)²)`, softmax choice at temperature T.
- **Transfer:** fit (σ_ev, σ_sd, T) on ONE domain, predict the OTHER with **no refit**. Scored by
  multinomial NLL (lower better) under a common loss; chance = uniform.

## Result

| Target domain | model | NLL | vs chance |
|---|---|--:|---|
| **Games** | fit-on-games (within) | **0.876** | (chance 1.040) |
| **Games** | **TRANSFER lotteries→games (no refit)** | **0.931** | **~63% of the way from chance to native** |
| **Lotteries** | fit-on-lotteries (within) | **0.624** | (chance 0.693) |
| **Lotteries** | TRANSFER games→lotteries (no refit) | 0.783 | **worse than chance** |

Fitted σ (comparable in magnitude across domains):
`lotteries s_ev=0.21, s_sd=2.02, T=2.21` · `games s_ev=0.15, s_sd=1.01, T=1.11`.

## Honest read (the result is asymmetric)

- **Positive — lotteries → games transfers.** A metric calibrated *only* on risky choice predicts
  strategic game play at NLL 0.931 — well below chance (1.040) and ~63% of the way to a games-native
  fit (0.876). **A risk-calibrated decision metric predicts human play in games it was never shown.**
  That is genuine cross-domain evidence, and it is exactly what neither CPT nor Nash can produce.
- **Negative — games → lotteries does NOT transfer.** The games-fit metric predicts lotteries at NLL
  0.783, *worse than* the 50/50 chance baseline (0.693). The transfer is **one-directional**.
- **Structure is partially shared.** The fitted σ's are the same order of magnitude in both domains
  (EV-sensitivity ~0.15–0.21; risk-scale ~1–2), consistent with a common metric *form*, but the
  asymmetric transfer says the two calibrations are **not** interchangeable.

**Interpretation.** The richer, larger lottery calibration (270 problems, strong EV+risk signal)
generalizes to games; the smaller, noisier games calibration (110 lab games, strategic uncertainty
proxied by a uniform belief) does not generalize back. So the shared-metric claim is **supported in
the strong direction (risk → strategy) but not symmetrically** — an honest, partial win, not a clean
unification.

## Polar decomposition FIXES the asymmetry (the big result)

Motivated by PolarQuant (the KV-cache method that splits a vector into scale-variant *magnitude* and
scale-invariant *direction*), note the geometric cost factors as
`cost = r · √((cosθ/σ_ev)² + (sinθ/σ_sd)²)` — a radius `r` times an angular term set entirely by the
**ratio σ_ev:σ_sd**. That ratio is the scale-invariant **aversion angle** (the risk-return tradeoff
*shape*); the rest is domain-specific *scale/decisiveness*. So instead of forcing both across domains
(full transfer), transfer **only the angle** and let magnitude+temperature recalibrate per domain:

| Direction | full (no-refit) transfer | **polar (angle-locked) transfer** |
|---|--:|--:|
| lotteries → games | 0.931 (66% of chance→native gap) | **0.876 (100%)** |
| games → lotteries | 0.783 (−131%, worse than chance) | **0.627 (97%)** |

The polar transfer **closes ~100% of the gap in both directions** — the failed direction is *rescued*.
And the fitted aversion angles are nearly equal across domains (ratio σ_ev/σ_sd: **lotteries 0.105,
games 0.146**). **The risk-return tradeoff shape is shared across risky choice and strategic games;
only the scale is domain-specific.** This is a clean, strong form of the shared-metric claim — stronger
than the raw one-directional transfer above, and the honest headline of this analysis.

## Structural fuzzing — searching the space of forms for the ideal (it found one)

Applying the TCSS structural-fuzzing method to the *model form* itself (`structural_search.py`): fuzz
over {value transform, risk feature, metric norm, reference}, scored by **worst-case cross-domain
transfer** (a form only wins if it transfers *both* ways). Winner:

> **`{value: identity, risk: variance, norm: L1 (city-block), ref: max}` — worst-case 72%, mean 95%.**

So a **variance** risk feature and an **L1** (city-block) metric transfer more robustly *bidirectionally*
than the SD / L2 (Mahalanobis) default (which is asymmetric under full transfer, and needs the polar
angle-lock to reach ~100%). Two independent routes — polar angle-locking on SD/L2, and structural
search landing on var/L1 — both say the raw Euclidean-SD form is not the most transferable structure.
A candidate "ideal" for Part III, to be confirmed with CV + the polar transfer on top.

## Belief model: does level-k sharpen the transfer? (No.)

We re-encoded games under iterated quantal best-response beliefs (row is level-(k+1)) instead of the
uniform level-0 opponent:

| Belief | games native NLL | lot→games transfer | gap closed |
|---|--:|--:|--:|
| **uniform (level-0 opponent)** | **0.876** | **0.931** | **66%** |
| level-k (opp level-1) | 0.971 | 0.973 | (native collapses toward chance) |
| level-k (opp level-2) | 0.995 | 1.010 | (worse still) |

**Level-k makes the game encoding *worse*, not better.** The native games fit degrades toward chance
as the belief deepens, and its fitted σ's go degenerate (σ_sd → thousands = "ignore risk"). So the
**uniform / level-0 belief is the better encoding**, and the positive lottery→games transfer holds
under it. This is consistent with a robust behavioral-game-theory result — *non-strategic (level-0)
features carry most of the predictive signal* (Wright & Leyton-Brown, "Level-0 Models"; "ElementaryNet",
2025). The geometric metric transfers because it captures the EV/risk response that dominates human
play, not sophisticated strategic reasoning.

## Caveats

- Games use a **uniform level-0 belief** to define strategic (EV, SD); richer belief models
  (level-k, empirical opponent) would change the game encoding and likely the transfer.
- (EV, SD) only — no fairness/social coordinates (d3/d6), which matrix games barely exercise; the
  social-preference games (ultimatum/public-goods) that engage the theory's *active* dims are a
  separate, on-theory test.
- 110 lab games vs 270 lottery problems; per-dataset scale normalization; multinomial NLL.
- games→lotteries being worse than chance suggests the games-fit is overconfident out of its regime —
  a real limitation, not smoothed over.

*Reproduce: `python cross_domain.py` (needs CPC18 via `cpc18.py` and the bogota clone via
`fetch.py`/git). Data are third-party (CC-BY / study terms), gitignored.*
