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

## Status / TODO before submission (updated 2026-09-10)

Two source files exist. `part2_manuscript.tex` is the committed draft.
`part2_manuscript_revised.tex` is a later revision pass (22 `\rev{}` blocks,
13 `[TODO:]` notes) that was found untracked on 2026-09-10 and committed as
found (cf2d85c). The revision pass is the one to finish; its TODOs are the
submission blockers. A repository survey on 2026-09-10 sorted them by what
the repo already contains.

**Closed 2026-09-10.** CPC18 Zenodo record (Plonsky, Erev, Ert 2019, "All raw
data for CPC18", verified on DataCite); Wright and Leyton-Brown GEB 106:16-37
(CrossRef); Plonsky et al. is now Nature Human Behaviour 9:2271-2284 (2025),
entry completed. Section VII citations were verified earlier.

**Answerable from the repo, text to be written (about a week).**

- Unit of analysis (L383): `projection-gap/analyze.py` computes Delta and paired
  Cohen's d over subjects (model x persona, n = 216; 202 for A2.1), per-model
  sign counts from per-model means, Benjamini-Hochberg FDR at q = 0.05 applied
  separately to the real and placebo-corrected families. Rows in
  `results_full_analysis.json` and `results_full.jsonl`.
- Two failure cells (L402-403): loss reversal placebo-corrected Delta = +0.058
  (raw +0.085, predicted -0.089), d = 0.204, cross-model 1/6; dose-response
  peak at level 4 of 4 (predicted 2), Spearman +1.00 observed vs -0.95
  cost-dependent (`RESULTS_ri_temperature.md`). A per-model sign count for the
  dose contrast does not exist yet; computable from the D9 rows of
  `results_full.jsonl`.
- Cross-lingual methods (L313): `RESULTS_crosslingual.md` (LaBSE leg, en + es,
  zh, ar, hi, sw; real 0.818 vs placebo 0.604) and
  `RESULTS_crosslingual_behavioral.md` (6 languages x 6 models x 12 personas x
  13 contrasts = 5,616 choices; demeaned mean pairwise cosine 0.737 vs 0.008
  shuffled). Needs a short methods subsection, not just a footnote.
- Hash provenance (L288): every registration hash is an ancestor of
  `origin/main` (public repo). First-add commits are all 2026-07-14, later than
  the signed tags of 2026-07-04/07, so the public-posting date is 2026-07-14
  and must be stated as such. No OSF registration exists for any of them.
- Panel identity (L375): six models run (gemma-small, qwen3-small, gemma,
  gpt-oss, glm-5, qwen3), temperature 0.9 (`panel_run.py`), prompts in
  `contrasts.py`. Missing: NRP alias to checkpoint mapping, and the `llmpanel`
  persona package is not vendored. Persona ids are recoverable from
  `results_full.jsonl`.
- Data and code availability (L542): the public repo and its signed tags are
  the pointer; missing a Zenodo release for Part II and the two items above.

**Needs a re-run (a few days of compute).**

- Paired per-fold CPC18 differences (L167): `fit_transfer.py` uses seeds 0-19
  shared across models but persists only mean and sd. Re-run with per-fold
  NLL/MAE written to CSV; the folds are reproducible.

**Needs new work or an explicit "not done" sentence.**

- BEAST / CPC18 leaderboard positioning (L175): no BEAST implementation in the
  repo. Either cite Plonsky et al. 2025 for the leaderboard and state the
  Trial-1-only scope, or implement.
- Nested cross-validation for the structural search (L243): none exists.
- Rank-1 loadings on d6/d7/d9 (L367): the fitted loading vector is never saved,
  and the constrained fuzz works in a 5-feature space, not the 9 coordinates.
  The sentence must be softened or the loadings computed.
- Angle-lock registration (L239): nothing registers the polar decomposition
  before the transfer runs. Keep the disclosure.

**Discrepancy found by the survey, to be fixed in the text.** The Delta-BIC of
about 140 and the dose-response Spearman come from an in-sample fit of three
temperature laws on the projection-gap panel (16,688 choices), not from CPC18
and not from a held-out split. Any sentence that says the information-price
temperature "improves held-out fit" must be reworded or the held-out test run.

**Estimate.** Four to six weeks to submission if the re-run and the explicit
"not done" sentences are accepted; longer if BEAST, nested CV, or the loadings
are implemented.

- Optional: add figures (Pareto/transfer/dose-response) if the venue wants them;
  the current draft is table-only and self-contained.
