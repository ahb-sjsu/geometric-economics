# Upgrading V₄ from brick to pillar — three moves, and what they revealed (mostly negative)

Three tests were built to elevate the "fourfold pattern = V₄ + loss aversion" result from a supporting
description to a load-bearing structural claim. They largely **failed**, and the failures are
informative. Reported straight.

## Move 1 — derive the reflections from the metric Σ. **FAILED.**

Claim under test: the low-rank metric forces risk attitude = |u_SD|·d·q (pure pseudoscalar), which
would make V₄ a *consequence* of Σ.

- The rank-1 metric fit on CPC18+choices13k is **EV-dominated**: normalized loadings
  EV=0.98, **SD=0.00**, skew=0.06, worst=0.18, pfav=0.00.
- With |u_SD|≈0 the metric predicts **~no** risk attitude, yet the data show a strong V₄ (b_dq=0.80).
  The risk/V₄ structure lives in the **subdominant** risk dimension the metric does not carry.
- One metric-consistent prediction (b_q=0) holds; b₀ is small but significant; the D₄-anisotropy test
  is unreliable (both loadings ≈0).

**Conclusion:** the V₄ is **not** derived from the fitted low-rank Σ. The dominant metric direction is
expected value; risk attitude is a small residual, and the reflections are additional structure, not a
metric consequence.

## Move 2 — does the reflection structure generalize to the social domain? **PARTIAL.**

The self↔other reflection σ_s (swap own/other) is the social analog of the value reflection. A fair
agent is σ_s-symmetric; the ultimatum responder is not:
- efficiency (σ_s-symmetric) weight vs signed-inequality (σ_s-antisymmetric) weight → the
  **antisymmetric term dominates (breaking fraction 0.72)**: inequality aversion.

So the **reflection + aversion** structure recurs: risk = value-reflection broken by *loss* aversion;
social = self↔other-reflection broken by *inequality* aversion. **The single reflection generalizes.**
But the ultimatum is 1-D (own+other=const), so the *second* social reflection — and a genuine social
V₄ — is not testable here; it needs 2-D allocation data (Charness-Rabin / Bruhin), not on Atlas.

## Move 3 — pre-register the V₄ constraints and confirm held-out. **FAILED, 0/3.**

Predictions frozen from Ruggeri (sha256 e156d5f7…): R1 interaction dominates, R2 no probability main
effect, R3 loss aversion present. Held-out corpus: 1,044 pure-domain gambles from CPC18+choices13k.

| held-out fit | value |
|---|--:|
| b_dq (interaction) | +0.221 |
| b_q (probability main effect) | **−0.187** |
| b_d (loss aversion) | +0.026 |

- **R1 FAIL** (|b_dq| = 0.22 is *not* > 2|b_q| = 0.37).
- **R2 FAIL** (b_q is comparable to b_dq, not small).
- **R3 FAIL** (b_d ≈ 0).

**The V₄ does not replicate out-of-sample.** On representative gambles, probability has a *substantial*
main effect on risk attitude — the "pure interaction" (b_q≈0) that defined V₄ on Ruggeri **is not
there**. (Cell counts are also imbalanced: pure-loss gambles are scarce, 37+76 vs 931 gain — but the
b_q failure is driven by the abundant gain cells, so it is robust.)

## What this means — an honest downgrade

The three moves were meant to make V₄ a pillar. Instead they bound it:
- **Not derived** from the metric (Move 1).
- **Only the single reflection** generalizes to social; not the full V₄ (Move 2).
- **Does not replicate** on representative gambles (Move 3) — it is a property of the **adversarially
  curated Kahneman–Tversky problem set**, which is *designed* to isolate the fourfold interaction, not
  of risky choice in general.

The defensible claim shrinks to: *the classical fourfold demonstration (KT's own problems) has
Klein-four structure with a loss-aversion field, and the reflection-plus-aversion motif recurs across
risk and social domains.* That is real but modest — closer to an elegant re-description of a curated
demonstration than a general law. **V₄ is a nice observation, not a pillar.** The load-bearing results
of the program remain the low-rank Σ (pre-registered, held-out) and the encoding-invariant
projection-gap — which did survive their held-out tests, unlike this one.

*Reproduce: `python move1_derive.py`, `move2_social.py`, `move3_heldout.py`.*
