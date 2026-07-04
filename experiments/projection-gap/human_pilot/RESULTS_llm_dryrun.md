# LLM-at-scale dry-run of the human instrument

Ran the EXACT human-pilot letters (economic-decision advice-column, `prereg-v2`) through the NRP panel
between-subjects, both incentive framings, and analyzed with the human `analyze_human.py`.

- **216 subjects** (6 models x 36 personas), 16,848 trials, **99% parse**, 3 samples/subject/contrast.

| metric | incentive OFF | incentive ON |
|---|---|---|
| H1 sign (placebo-corrected, FDR) | 5/7 | 5/7 |
| H2 cross-domain (game + lottery) | yes | yes |
| **H4 dose MONOTONE** (prereg-v2's redesigned prediction) | **yes** | **yes** |
| placebo null (raw; corrected in H1) | moves | moves |

## What this validates (before spending on humans)
1. **The advice-column letters reproduce the projection-gap** under the between-subjects analysis the
   human study will use. The instrument works end-to-end.
2. **Dose is monotone** — validates the `prereg-v2` fixed-temperature redesign *on the human letters*
   (v1's peaked prediction stays falsified).
3. **Incentive framing has no effect** (identical arms) — the gap is not a hypothetical-choice
   artifact; a useful control for the human study.
4. Placebos move (wording sensitivity), so the placebo-corrected H1 (5/7) is the clean read, as on the
   original panel.

## Status
This is still a MODEL-ORGANISM validation of the instrument, not the human claim. It clears the last
technical gate: letters + between-subjects analysis + incentive mechanism + monotone-dose all work at
scale. Remaining gates are procedural (OSF registration, IRB, N~50 comprehension pilot), not technical.
