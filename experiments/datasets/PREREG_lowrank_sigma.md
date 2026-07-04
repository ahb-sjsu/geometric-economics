# Pre-registration — the low-rank Σ structural hypothesis

The constrained-Σ fuzz (`RESULTS_constrained_sigma.md`) found, on CPC18 + choices13k (lotteries) +
bogota (games), that a **rank-1 precision matrix** matches the full metric on fit and beats it on
cross-domain transfer, at diagonal-parameter-count. That was a **search over structures** — a
hypothesis, not a result. This document **freezes** the hypothesis and its falsifiable predictions
**before** re-testing on **held-out** datasets, per the anti-meta-overfitting discipline.

## The frozen hypothesis

> The behavioral decision metric Σ⁻¹ is **effectively low-rank**: a rank-1 (or rank-2) precision matrix
> captures nearly all the structure. Specifically, on decision datasets encoded in the (EV, SD, skew,
> worst, p-favorable) space, a rank-1 Σ⁻¹ will:
> **(H1)** fit within **0.02 NLL** of the full metric in each domain (low-rank sufficiency);
> **(H2)** transfer cross-domain at **≥ 85%** of the chance→native gap (polar angle-lock);
> **(H3)** **beat the diagonal Σ at equal parameter count** (lower native NLL *and* higher transfer);
> **(H4)** rank-2 improves transfer over rank-1 by **< 5 percentage points** (low-rank, not full-rank).

## Falsifiers (stated up front)

- H1 fails if rank-1 native NLL exceeds full by > 0.02 in either held-out domain → the metric is *not*
  low-rank; interactions need full rank.
- H2 fails if rank-1 transfer < 85% gap-closed on held-out domains → the low-rank structure does not
  transfer.
- H3 fails if diagonal matches or beats rank-1 at equal params → the off-diagonal structure is not real.
- H4 fails if rank-2 (or full) transfers substantially better than rank-1 → higher rank is needed.

Any of these is a publishable negative that revises the structural claim.

## Held-out re-test plan (datasets NOT used in the fuzz)

The fuzz used CPC18 + choices13k + bogota. The **held-out** confirmatory datasets:
1. **Social-preference games** — Fraser–Nettle public-goods (`eris-econ/data/fraser_nettle_exp{1,2}.csv`)
   and any dictator/trust panels: a *social* domain the fuzz never saw.
2. **Ruggeri prospect-theory replication** (19 countries) — a distinct lottery corpus.
3. **Cross-lingual** (LaBSE) — the same letters across languages: does the low-rank structure survive
   translation (universality)?

The re-test freezes the analysis to the same `constrained_sigma_fuzz.py` pipeline (rank-1 vs diagonal
vs full; native fit, held-out transfer, BIC), applied to the held-out datasets, scored against H1–H4.

## Provenance

- Discovery run: `constrained_sigma_fuzz.py` on CPC18+choices13k+bogota, K=5 features.
- rank-1 discovery values (for reference, NOT the confirmatory test): lot 0.636 / games 0.873 /
  transfer 90%; full 0.634 / 0.867 / 88%; diagonal 0.660 / 0.928 / 89%.
- Frozen at tag `prereg-sigma-v1`. The confirmatory result must come from the held-out datasets above.
