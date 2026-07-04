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
