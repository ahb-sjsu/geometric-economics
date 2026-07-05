# TCSS Part II — the follow-up manuscript

`part2_manuscript.tex` — **"Geometric Prediction of Economic Behavior II:
Held-Out and Cross-Domain Validation."** A complete IEEE TCSS
(`IEEEtran`, journal) manuscript, written to follow smoothly from the accepted
Part I ("Geometric Prediction of Economic Behavior: Cross-Domain Validation
Across Game Theory and Prospect Theory").

It reuses Part I's notation (9-D manifold `E`, Mahalanobis cost `C = √(Δᵀ Σ⁻¹ Δ)`,
softmax choice, cost-dependent temperature) and voice (modest, held-out, honest),
and answers the Part I reviewer's central asks — *individual-level, held-out,
common-protocol* — entirely with **computational** results. No human trials are
claimed; the confirmatory human projection-gap study is stated as future work.

## What it reports (all held-out / pre-registered)

1. **Held-out prediction + bidirectional cross-domain transfer** (§III) —
   CPC18 out-of-sample (geometric beats EV/RUM, ties CPT with one fewer param);
   lotteries→games transfer; polar angle-lock → 97–100% both directions.
   Source: `../paper_01_cross_domain.md`, `datasets/RESULTS_cpc18.md`,
   `datasets/RESULTS_cross_domain.md`.
2. **Pre-registered low-rank Σ** (§IV) — `prereg-sigma-v1`, four frozen claims,
   three held-out legs (Fraser–Nettle, Ruggeri 19-country, 6-language cross-lingual);
   diagonal superseded. Source: `datasets/RESULTS_prereg_sigma_scorecard.md`.
3. **Projection-gap instrument** (§V) — `prereg-v1`, 216 model agents / 83,682
   choices, 5/7 contrasts 6/6 cross-model; two registered failures reported.
   Source: `../paper_02_projection_gap.md`, `projection-gap/`.
4. **Temperature repair** (§VI) — fixed information price (Sims / Matějka–McKay);
   dose Spearman −0.95 → +1.0, ΔBIC ≈ 140. Source: `RESULTS_choice_rule.md`,
   `projection-gap/ri_temperature.py` results.

Plus independent social-preference corroboration (§VII: FKM, Charness–Rabin,
DP-means) and the honest graveyard (§VIII).

## Build

```
pdflatex part2_manuscript.tex && pdflatex part2_manuscript.tex
```

Compiles clean (7 pages, no undefined refs/cites). References are inlined in a
`thebibliography` block, mirroring Part I's submission `.tex`.

## Status / TODO before submission

- §VII citations added and verified: Bruhin–Fehr–Schunk (JEEA 2019, 17(4):1025–1069),
  Fehr–Charness (JEL 2025, 63(2):440–514), Nunnari–Pozzi (CESifo WP 9851, 2022;
  the pooled mean advantageous-inequality aversion β = 0.33 that the Charness–Rabin
  fit β = 0.34 matches).
- Verify the CPC18 Zenodo record author list/date and Wright–Leyton-Brown GEB 2017
  page range against the final published versions before submission.
- Optional: add figures (Pareto/transfer/dose-response) if the venue wants them;
  the current draft is table-only and self-contained.
