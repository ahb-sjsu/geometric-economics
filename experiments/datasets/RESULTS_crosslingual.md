# Cross-lingual universality (LaBSE) — the coordinate directions survive translation

**Held-out leg #3 of `prereg-sigma-v1`.** The geometric theory claims the decision
*coordinate directions* (societal / epistemic / identity) are **universal** while the *scale*
(temperature) recalibrates per culture. Test: translate the projection-gap letters into 5
typologically diverse languages (Spanish · Chinese · Arabic · Hindi · Swahili — Romance,
Sino-Tibetan, Semitic, Indo-Aryan, Niger-Congo) with an NRP LLM (qwen3), then measure with
**LaBSE** (a *separate* model) whether the coordinate axis `emb(hi) − emb(lo)` is preserved.
All 65 lang×contrast translations passed the LaBSE fidelity gate (0.75).

## 1. Axis invariance — is the hi−lo direction the same across languages?

`cos(axis_en, axis_lang)`, mean over languages:

| coordinate | mean axis-invariance | n | min |
|---|--:|--:|--:|
| societal | **0.858** | 15 | 0.75 |
| epistemic | **0.789** | 15 | 0.69 |
| identity | **0.783** | 5 | 0.71 |
| **all real** | **0.818** | 35 | |
| **placebo (control)** | **0.604** | 10 | |

**Real coordinates are +0.214 more language-invariant than placebos.** The direction that
distinguishes the two poles of a real coordinate contrast is preserved under translation into
all five languages; the placebo direction is not (it degrades to 0.60, near translation noise).

## 2. Cross-contrast coherence — is there ONE universal direction per coordinate? (the discriminating test)

Within-contrast invariance can be inflated by mere translation fidelity. The stronger test:
do *different* contrasts sharing a coordinate point the **same way** (one universal axis),
distinct from other coordinates, in **every** language? Placebos should not load on any axis.

| lang | within-coord | cross-coord | separation | placebo→coord |
|---|--:|--:|--:|--:|
| en | 0.211 | 0.039 | **+0.172** | −0.017 |
| ar | 0.176 | 0.040 | +0.136 | 0.085 |
| es | 0.171 | 0.058 | +0.113 | −0.015 |
| hi | 0.137 | 0.050 | +0.088 | 0.028 |
| sw | 0.216 | 0.038 | +0.178 | 0.027 |
| zh | 0.199 | 0.026 | +0.173 | 0.106 |

- **Within-coord > cross-coord in every language** (separation +0.09 to +0.18): same-coordinate
  contrasts align ~4–5× more than different-coordinate contrasts. Coordinates are **distinguishable
  directions, not one blob** — and the separation is preserved across all five languages.
- **Real within-coord 0.211 vs placebo→coord 0.036 (+0.175):** placebos do not load on any
  coordinate centroid — the coherence is a property of the *real* coordinates, not the letter format.

## What this establishes — and what it does not

**Establishes (representational universality):** the societal / epistemic / identity coordinate
*directions* are language-invariant. A model (LaBSE) trained on 109 languages, given translations
from a *different* model (qwen3), reconstructs the same three coordinate axes in every language,
and only for the *real* coordinates — not placebos. This is the keystone encoding-invariance
(Thm 5) extended from "any scalar projection" to "any language."

**Does NOT yet establish (behavioral universality):** that *choices* shift in the predicted
direction in every language. That is the separate, stronger leg — the per-language LLM panel
(fit the metric on one language's choices, predict another's; "universal shape, culture-specific
scale" = shared aversion angle, recalibrated temperature). The instrument (`translate.py` +
`llm_pilot_run.py`) is built for it.

## Honest caveats

- **Absolute within-coord coherence is low (~0.21 cosine).** The coordinate is a *weak shared
  component* across otherwise-different scenarios; the signal is the **separation** (within ≫ cross,
  ~4–5×) and the **real−placebo gap**, not high absolute alignment. Do not overstate.
- **Translation-artifact check passes:** one LLM produced the translations, which could in principle
  impose shared structure — but the placebos went through the *same* translator and do *not* cohere,
  and LaBSE is a *separate* model, so the coherence is not a translator fingerprint.
- **Small n** (7 real contrasts, 3 coordinates). Confirmatory, not definitive; the behavioral leg
  and more contrasts strengthen it.

## Verdict for `prereg-sigma-v1`

Leg #3 (cross-lingual) **supports** the universality half of the theory at the representational
level: the coordinate directions are real, distinct, and language-invariant, and placebos are not.
The low-rank Σ re-test itself still needs the *behavioral* cross-lingual choices (per-language
panel) and the social-preference-game leg to be scored against H1–H4.

*Reproduce: `translate.py` (Atlas/NRP) → `labse_crosslingual.py --translations translations.json`.*
