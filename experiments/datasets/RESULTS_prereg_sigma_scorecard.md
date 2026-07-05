# `prereg-sigma-v1` — final scorecard

The constrained-Σ fuzz found (on lotteries + level-k games) that the decision metric is
**effectively low-rank**: a rank-1/rank-2 precision matrix matches the full metric and beats the
diagonal. That was a search winner — a hypothesis. `prereg-sigma-v1` froze it as four falsifiable
claims and named three held-out domains. All three have now been run.

## The frozen hypotheses

- **H1** rank-1 fits within 0.02 NLL of full (low-rank sufficiency)
- **H2** transfers ≥ 85% of the chance→native gap (structure transfers, scale recalibrates)
- **H3** rank-1 beats diagonal at equal parameter count (off-diagonal structure is real)
- **H4** rank-2 adds little over rank-1 (low, not full, rank)

## Results across the three held-out legs

| leg | data | H1 | H3 | H4 | H2 (transfer) |
|---|---|:--:|:--:|:--:|---|
| **#1 social games** | Fraser-Nettle ultimatum (responder) | PASS (rank1=full) | **PASS** (rank1 0.290 < diag 0.335) | PASS (rank1=rank2) | 99%/99% across hunger condition |
| **#2 Ruggeri** | 17 KT problems × 19 countries | PASS* (0.0195, marginal) | **PASS** (rank1 0.667 < diag 0.680) | PASS (rank2=full; rank2 sweet spot) | **99%/99%** across countries |
| **#3 cross-lingual** | projection-gap letters × 6 languages | — (representational + behavioral universality) | — | — | shape 0.74 (behavioral), axis +0.214 vs placebo (LaBSE) |

\* rank-1 marginal (right at the 0.02 line); rank-2 is the tighter low-rank choice on Ruggeri —
consistent with the original fuzz, where rank-2 had the best BIC.

## Verdict

**The low-rank Σ survives pre-registered, out-of-sample testing.** In every domain where it can be
tested, **diagonal is beaten, full is unnecessary, and rank 1–2 suffices** — the parsimony win the
free-diagonal Σ lacked (the gap the ensemble test exposed). The metric **transfers at ~99%** across
conditions and across 19 countries, and its coordinate directions are language-invariant.

## The standing caveat (stated everywhere)

The **loss / reflection domain** is the consistent weak spot: raw geometric features do not capture
the sign-flip of risk attitudes under losses (Ruggeri gain→loss transfer 0%; the B1L.1 cross-lingual
falsifier; the temperature/loss issue prereg-v2 redesigns). The confirmed low-rank result is a
**gain-domain** result; reflection needs the separate domain-flip encoding. This bounds the claim
honestly and points at the next modeling target.

## What changes in the theory

Replace the diagonal Σ with a **rank-1/rank-2** precision matrix: same fit as the full metric at
~diagonal parameter count, real off-diagonal structure, and cross-domain/cross-cultural transfer. The
diagonal default (which the TCSS reviewer flagged as "convenient but severe") is superseded, on
pre-registered held-out evidence.
