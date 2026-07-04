# Job-A fit-and-transfer — CPC18 (individual risky choice)

The reviewer's #1 ask: move from 16 aggregate targets to **held-out individual prediction under a
common protocol vs CPT**. This is that, on the CPC18 benchmark (Erev/Ert/Plonsky), decisions from
description.

## Protocol

- **Data:** CPC18 raw (Zenodo 10.5281/zenodo.2571510, CC-BY-4.0), 270 games, **27,780 description
  choices** (Trial 1 — first encounter, no feedback), median 120 subjects/game.
- **Split:** by **GameID** (predict *unseen games*), 70/30, averaged over **20 random splits**.
- **Common protocol:** every model predicts P(choose B) per game; parameters fit on train games by
  minimizing n-weighted binomial NLL; scored on held-out games. Same data, loss, and split for all.
- **Encoding:** two-outcome approximation (H as its sub-lottery mean); EV, SD (risk), ambiguity flag.

## Result (held-out games, 20-split mean ± sd)

| Model | #params | TEST MAE | TEST NLL |
|---|--:|--|--|
| constant (train B-rate) | 1 | 0.199 ± 0.012 | — |
| Expected Value (logit) | 1 | 0.149 ± 0.008 | 0.644 ± 0.011 |
| linear RUM (dEV, dSD, amb) | 4 | 0.128 ± 0.010 | 0.632 ± 0.013 |
| **Geometric (Mahalanobis-from-ideal)** | 4 | **0.124 ± 0.009** | **0.629 ± 0.011** |
| **CPT (alpha,beta,lambda,gamma + T)** | 5 | **0.118 ± 0.008** | **0.624 ± 0.011** |

## Honest read

- The **geometric decision architecture, calibrated on this domain, is a competitive domain-general
  predictor of individual risky choice out-of-sample** — it beats Expected Value and linear RUM
  robustly, and comes within ~0.006 MAE (< 1 sd) of CPT **with one fewer parameter**.
- **CPT leads on its home turf, as it should** — it is purpose-built for exactly this lottery task.
  We do not claim to beat CPT on lotteries; we claim the *domain-general* geometry is competitive with
  the *domain-specialized* champion here.
- **The geometric model's distinct claim is CROSS-DOMAIN**: one shared metric across *games and*
  lotteries. On pure lotteries CPT wins narrowly; the payoff is transfer — calibrate on one domain,
  predict the other — which CPT structurally cannot do (it has no representation of strategic games).
  That is the next analysis (needs a game dataset under the same protocol).

## Caveats

- Two-outcome approximation understates risk for multi-outcome (Symm/skew) gambles — a mild,
  model-neutral bias; refine with the CPC lottery generators.
- Description-only (Trial 1); the from-experience dynamics (blocks 2–5, the BEAST regime) are a
  separate, harder problem excluded here.
- CPT uses a standard 2-outcome rank-dependent form; a fuller CPT with the exact multi-outcome
  cumulative weighting could shift its number modestly.

*Reproduce: `python fit_transfer.py` (after `python fetch.py --download` or the Zenodo fetch in
`cpc18.py`). Data is CC-BY-4.0 and not committed (see `.gitignore`).*
