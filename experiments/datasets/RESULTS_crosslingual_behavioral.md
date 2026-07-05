# Behavioral cross-lingual panel — universal shape, culture-specific scale

**The behavioral leg of the cross-lingual test** (companion to `RESULTS_crosslingual.md`, which
established the *representational* universality via LaBSE). Here we run the projection-gap letters
themselves through the NRP panel **per language** and measure whether *choices* carry the same
coordinate structure. Between-subjects design: 6 languages (en · es · zh · ar · hi · sw) × 6 models
× 12 personas × 13 contrasts = **5,616 forced choices**, one pole per subject per contrast. The
per-language projection-gap vector is `g_lang = [ P(A|hi,c) − P(A|lo,c) ]` over the 7 real contrasts.

## 1. Direction universality

| lang | sign-match (real) | RMS gap (scale) | shape cos→en |
|---|--:|--:|--:|
| en | 7/7 | 0.318 | 1.000 (ref) |
| ar | 7/7 | 0.254 | 0.924 |
| hi | 5/7 | 0.271 | 0.938 |
| es | 6/7 | 0.274 | 0.863 |
| zh | 5/7 | 0.223 | 0.883 |
| sw | 5/7 | 0.249 | 0.688 |

Every language recovers the predicted gap direction on **5–7 of 7** real contrasts. Per contrast,
the sign agrees across **all six** languages for A1.2, A3.1, B1.1 (unanimous), and 5/6 for A1.1,
A2.1. The dissenters are the *already-known-weak* contrasts: **B1L.1** (epistemic **loss** domain,
3/6) — the same loss/temperature falsifier flagged in the English work and addressed by prereg-v2 —
and **B2.1** (4/6).

## 2. Universal shape (the core result)

- raw mean pairwise `cos(g_lang, g_lang')` across languages: **0.844** (shuffled-label null 0.463;
  **+0.382** above chance).
- **demeaned** (pattern beyond the shared positive valence — 6/7 contrasts have sign_pred=+1):
  **0.737** (shuffled null **0.008**; **+0.730** above chance).

The demeaned number is the clean one: after removing each language's overall gap level, the
*relative* pattern — which coordinates elicit larger vs smaller choice shifts — is **73% aligned
across six typologically diverse languages**, versus ~0 for shuffled labels. The coordinate
*structure* is language-invariant.

## 3. Culture-specific scale

RMS gap ranges **0.223 (zh) .. 0.318 (en)**, a **1.43×** spread. The overall magnitude of the
projection-gap recalibrates by language while the shape holds — the theory's "universal shape,
culture-specific scale," observed directly: the *direction/pattern* is shared (cos 0.74–0.94), the
*scale* differs (1.43×).

## What this shows — and the honest limits

**Shows:** the behavioral coordinate structure (not just the LaBSE representation) transfers across
languages. Direction replicates 5–7/7 everywhere; the relative pattern is 73% aligned beyond valence;
magnitude recalibrates. Both halves of "universal shape, culture-specific scale" appear in the choices.

**Limits (stated plainly):**
- **Language, not culture.** Only the *letter* was translated; the personas were English-prompted.
  So the "scale" differences are driven by *language/model competence*, not a genuine cultural
  sample. This is cross-lingual *stimulus* invariance, a necessary precondition for — but not proof
  of — cross-cultural preference variation. A real cultural test needs in-culture personas or human
  samples per region.
- **Swahili is the weak spot** (shape→en 0.688, lowest): a lower-resource language where translation
  and model competence are weaker — a competence confound, not necessarily a preference difference.
- **The loss-domain contrast (B1L.1) is least universal**, consistent with the known temperature/loss
  falsifier; prereg-v2's fixed-temperature redesign is the fix under test.
- **LLMs, not humans.** This validates the instrument and the theory's language-invariance claim at
  scale; the human capstone remains the decisive test.

## Verdict for the cross-lingual leg of `prereg-sigma-v1`

Representational (LaBSE) **and** behavioral (panel) legs now **both support** universality: the
coordinate directions are language-invariant in embedding space, and the choice-level projection-gap
carries the same shape across six languages with a recalibrated scale. This strengthens leg #3, with
the honest caveat that it is *language* invariance (translated stimulus), not yet demonstrated
*cultural* variation. The remaining held-out leg for the low-rank Σ (H1–H4) is the social-preference
games.

*Reproduce: `crosslingual_panel.py` (Atlas/NRP) → `crosslingual_analyze.py --data xling.jsonl`.*
