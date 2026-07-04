# Redesigning the choice rule (the caught culprit) — via fuzzing

The projection-gap panel and the CPC18 magnitudes convicted the **cost-dependent temperature**
`T(Δ)=max(T_floor, T_base·Δ^α)` with `α=2.13`. Since α>1, the effective signal `Δ/T ~ Δ^(1−α)`
*decreases* for large cost gaps → the model predicts **washout** (a dose peak) and **tiny magnitudes**,
while the data are **monotone** and **large**. We fuzzed over response-function families, scored on
CPC18 (individual, 15-split held-out CV), requiring monotonicity.

## Result (CPC18 held-out)

| Choice rule | #params | TEST MAE | TEST NLL | monotone |
|---|--:|--:|--:|:--:|
| **`temp_power`, α FROZEN at 2.13** (the culprit) | 4 | 0.1263 | **0.6328** (worst) | yes* |
| `logit_fixed` (fixed temperature) | 3 | 0.1225 | 0.6290 | yes |
| **`temp_power`, α FREE** | 5 | 0.1204 | **0.6273** (best) | yes, **α = 0.42** |
| `probit` (Gaussian noise) | 3 | 0.1236 | 0.6297 | yes |
| `luce` (power-law) | 3 | 0.1427 | 0.6391 | yes |

\*the frozen-α rule stays monotone only within the plotted gap range; it fits worst on real data.

## Diagnosis (the smoking gun)

**When the temperature is calibrated on individual data, the exponent falls from 2.13 → 0.42.**
- `α > 1` (=2.13, from the Part I *aggregate* targets): super-linear temperature → signal shrinks with
  the cost gap → **washout**, the dose-peak the panel falsified, and ~5× magnitude under-prediction.
- `α ≈ 0.42` (from CPC18 *individual* choices): **sub-linear** → signal grows with the gap → monotone,
  matching the panel's observed monotone dose-response, and the best held-out fit.

The pathology was never the model form; it was **fitting the temperature exponent on aggregates.** The
individual-level data wants a gentle sub-linear (or flat) temperature.

## Recommended redesign

Two good options, both eliminating the washout that failed the panel:
1. **Fixed-temperature logit (`α = 0`)** — *recommended for parsimony.* Monotone by construction, 2
   fewer parameters, held-out NLL 0.629 (within 0.0017 of the best), and it removes the whole
   cost-dependent-temperature apparatus the Part I reviewer flagged. Occam wins: the extra flexibility
   of the temperature buys almost nothing.
2. **Cost-dependent temperature with sub-linear `α ≈ 0.4`** — marginally best fit (0.627) if the two
   extra parameters are justified; keeps a mild gap-dependence.

Either way, **magnitude** becomes a single per-population scale (humans vs LLMs differ), fit on data,
rather than being throttled by a super-linear temperature.

## Why this resolves the falsifiers

- **Dose-response:** the redesigned rule predicts a **monotone** dose curve — matching the panel
  (observed monotone, peak at the top level), where the old `α=2.13` predicted the inverted-U that was
  rejected.
- **Magnitude:** a flat/sub-linear temperature no longer suppresses effect sizes; the fit chooses the
  scale that matches the observed d≈0.5–0.9.
- **Held-out fit:** strictly better than the frozen-α rule on CPC18.

## Scope

This is a **Part III proposal**, established by fuzzing on human data. It is **not** applied to the
frozen pre-registered projection-gap model (`geometric_model.py`, `prereg-v1`), whose hash must stay
intact — the panel was scored against the *original* predictions, and that record stands. The
redesigned rule is the forward change for the next round (re-derive predictions, re-register, re-run).

*Reproduce: `python choice_rule_search.py`.*
