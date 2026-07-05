# FKM 3-person split — an exchange symmetry of the social metric

The 2-person FKM data showed choice is metric-governed and giving is low-dimensional
(`RESULTS_fkm.md`). The 3-person budgets answer the question pure giving cannot: how does the same
agent allocate *among others* (self held aside)? Data_3D: **65 subjects × 50 budget-line choices**;
each row [self, other₁, other₂] on a budget `Σ πᵢ/maxᵢ = 1`. Per-subject 3-good CES fit (weights
α_self, α_o1, α_o2 + substitution σ).

## The clean result — an o₁↔o₂ exchange symmetry

**100% of subjects weight the two interchangeable others within 0.1** (median |α_o1 − α_o2| = 0.01).
The two anonymous others receive *equal weight* in every subject's social metric; the split between
them is driven entirely by their **prices**, not by favoritism. This is a genuine **permutation
symmetry (o₁ ↔ o₂)** of the social metric — the among-others analog of the reflection symmetries found
in risk and 2-person social choice. It is the kind of symmetry that is robust by construction (basic
impartiality among indistinguishable recipients), and it holds universally here.

## Confirmed (consistent with 2-person and FKM)

- **Self-regard persists:** median weight on self **α_self = 0.72** (others combined 0.28); 69% put
  >50% weight on self — the same σ_s reflection-breaking as the 2-person data (α=0.78) and Charness-Rabin.
- **Efficiency-leaning among others:** **71%** of subjects have σ > 1 (the two others are substitutes —
  give to whichever is cheaper, i.e., maximize others' total), 29% σ < 1 (equality-leaning). Matches
  FKM's finding that a majority are efficiency/aggregate-payoff concerned.

## The honest weak spot

The single-ρ 3-good CES fit is **noisy**: mean within-subject R² = 0.30 (median 0.13) vs 0.54 for the
2-person CES. A *single* substitution parameter for both the self-vs-others and the among-others
trade-offs is restrictive, and 3-good share-matching is a harder fit than the 2-good log-ratio OLS. So
"one low-dimensional metric governs among-others allocation" is supported **structurally** (self-regard,
exchange symmetry, efficiency-leaning all recovered) but **not as a tight fit**. FKM use a nonlinear
Tobit and a richer specification; this is a lightweight reanalysis.

## What the 3-person layer adds to the thesis

- A **clean, robust symmetry** of the social metric (o₁↔o₂ exchange / impartiality) — real powered
  evidence that the decision metric carries the symmetries of the problem's structure, the same theme
  as the reflection symmetries, now in the among-others layer.
- Self-regard and efficiency-leaning **replicate** at the individual level in a second, independent pool.
- Honestly: the *tight* low-dimensional fit does not extend cleanly to the among-others trade-off with a
  single-ρ CES — a real limit, not papered over.

*Data: FKM (2007) 3-person replication, OpenICPSR 115613 (licensed; not committed). Reproduce:
`python fkm_3d.py` with `raw_fkm/` present.*
