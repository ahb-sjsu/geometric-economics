# Corrections applied to part2_manuscript_revised.tex, 2026-10-30

Pre-edit copy: scratchpad `part2_manuscript_revised.before-2026-10-30.tex` (session scratch, not in repo).
Every number below was re-derived on 2026-10-30 from the cited file.

| Claim | Old | New | Source |
|---|---|---|---|
| Projection-gap scorecard | 5 confirmed "across both frames", table row "Social (lottery) +0.17 d 0.56" | All 7 contrasts by ID. The +0.17/0.56 row is A1.1, a game. Lottery frame 1 of 3 passes | `projection-gap/results_full_analysis.json` placebo_corrected |
| B2.1 lottery social | omitted | Delta -0.006, d -0.03, p 0.34, raw 4/6, corrected 4/6, fails | same, plus per-model from `results_full.jsonl` via `analyze.per_subject_delta` |
| B1L.1 loss reversal | "[TODO]", 1/6 | Delta +0.058 (predicted negative), d 0.20, raw 1/6, corrected 3/6 | same |
| Cross-model counts | 6/6 on all five | raw 6/6 on all five; placebo-corrected A1.1 5/6 (gemma-small -0.056), others 6/6 | per-model recomputation |
| Dose | "monotone", count TODO | k = 4, peak level 4 vs predicted 2, per-model monotone 3/6 | `contrasts.py:170`, analysis JSON H4, per-model tally |
| Magnitude | "roughly five times larger" | fails coverage on all 7, A3.1 +0.46 vs +0.09 predicted | `projection-gap/RESULTS.md:40-41` |
| Temperature dBIC | "~140, improves held-out fit" on CPC18 implied | in-sample, 16,688 choices, LM dry run of advice letters, 26 cells; cost-dep vs fixed-T 124.4, vs RI 141.6, RI vs fixed-T 17 | `projection-gap/RESULTS_ri_temperature.md`, `ri_temperature.py:38` |
| CPC18 protocol | 20-fold CV by problem | 20 random 70/30 splits by GameID, 27,780 Trial-1 choices, one free T per split | `datasets/RESULTS_cpc18.md:11`, `fit_transfer.py:55` |
| Registration | "hashed and tagged before data" | July files committed locally 2026-07-04 before analysis, public 2026-07-14, byte-identical, order rests on commit timestamps; sigma-v1 has no hash file; OSF only for boundary | git tags vs origin/main |
| prereg-coupling-v1 | "frozen and hashed, awaiting GPS data" | scored on GPS and FAILED (risk-altruism r 0.086 vs bound 0.10; not low-rank); angle-to-angle follow-up frozen, no data | `RESULTS_coupling_scorecard.md`, `PREREG_coupling_angle_to_angle_v1.md` |
| Angle-lock | "confirmatory version belongs to prereg-v2" | deleted; exploratory, post hoc | commit order 1a32634 then 4a98383 |
| Cross-lingual 0.74 | conflated "shape 0.74" | axis cosine 0.818 (n 35) vs placebo 0.604 (n 10); behavioral 0.737 mean pairwise r over 7 contrasts, 15 language pairs, null 0.008 | `datasets/RESULTS_crosslingual*.md` |
| Rank-1 loadings | TODO claim about d6/d7/d9 | loadings not saved; legs fit on 5 encoded features, not 9 coordinates | `constrained_sigma_fuzz.py:11,39`, `ruggeri.py:7`, `social_games.py:15` |
| Theorems in Part II | full proofs, binary-menu restriction | statements citing companion theory paper; binary restriction removed | `theory/STATEMENTS.md` Thm 1-2 |
| Part I cite | in press | DOI 10.1109/TCSS.2026.3734068 | ORCID notice 2026-10-29 |

Added: Section "Money Enters Through Income Units" from `boundary/RESULTS.md` and `analysis/grade.json`
(P1 g 0.817 SE 0.147 p 2.3e-10; P2 p 0.19, ratio 2.32 [1.13, 9.70]; P3 0.165 per decade p 0.46;
P4 within 0.003 nats; P5 FAIL +0.033/+0.060/+0.325, sigma1^2 at bound; P6 pass).
Added: "What these contrasts discriminate" (Ellsberg, belief change, Andreoni/Charness-Rabin, Akerlof-Kranton).
Per owner scope change, no Learned Coordinates section; one future-work sentence names Part III.

Open: OSF registration visibility (osf.io/ead4x) to be confirmed; bib entries marked `% verify vol/pages on final`
(Part I, Andersen, Slonim-Roth, Cameron, Falk et al.).
