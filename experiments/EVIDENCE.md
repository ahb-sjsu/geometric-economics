# Geometric Economics — Consolidated Evidence Ledger

*The honest state of the body of work. Distinguishes the results that survived pre-registered,
held-out testing (the pillars) from those that did not (the graveyard) and those that are real but
supporting. Written so the thesis rests weight only on what can hold it.*

---

## The thesis, in one sentence

Economic choice is movement on a low-dimensional decision manifold under a Mahalanobis cost metric Σ
with a softmax choice rule; the empirically load-bearing claims are that (a) the metric is **low-rank**,
(b) choice depends on **non-monetary coordinates in an encoding-invariant way** that no scalar utility
can represent, and (c) the same metric **transfers across domains**.

## The two pillars (survived pre-registered, held-out testing)

### Pillar 1 — the metric is low-rank Σ  ✅ CONFIRMED
`prereg-sigma-v1` froze four falsifiable claims (H1 rank-1 ≈ full; H2 ≥85% transfer; H3 rank-1 beats
diagonal; H4 low-not-full rank) **before** three held-out re-tests. All three ran:

| held-out leg | result |
|---|---|
| social-preference games (Fraser–Nettle ultimatum) | H1/H3/H4 pass; 99% cross-condition |
| Ruggeri prospect theory (17 KT × 19 countries) | H1/H3 pass; rank-2 sweet spot; **99% cross-country** |
| cross-lingual (LaBSE + behavioral panel, 6 languages) | universality supported (representational + behavioral) |

The parsimony win the free-diagonal Σ lacked, confirmed on frozen out-of-sample data. Standing bound:
the confirmed result is **gain-domain**; the loss/reflection encoding (below) is fit, not yet held-out.

### Pillar 2 — encoding-invariant projection-gap  ✅ CONFIRMED (LLM, cross-model)
`prereg-v1` froze predictions before any data. The panel (216 subjects, 6-model ladder, 83k choices):
core claim holds — **5/7 real contrasts** FDR-significant, placebo-corrected, predicted sign,
cross-domain, **6/6 cross-model**, not capability-gated. This is the theory's distinctive content: a
designed, encoding-invariant prediction the whole scalar class must get wrong.

### Keystone — the theory (paper_00)
Scalar irrecoverability (Thm 4) — if choice depends on ≥2 independent coordinates, no continuous scalar
utility represents it without loss — is the one *necessary* theorem, and it is only conditionally
load-bearing (it needs Pillar 2's empirics to have teeth). The nesting/representation theorems are
stated to be disarmed, not leaned on.

## Supporting results (real, but not pillars)

- **Rational-inattention temperature** (`ri_temperature.py`): a **fixed information price** beats the
  cost-dependent T (dose Spearman +1.0 vs −0.95; ΔBIC ~140). Closes the dose falsifier and reframes
  temperature as the price of a bit. Two magnitude residuals remain (σ_k calibration; fourfold), and
  they are utility-side, not temperature.
- **Cross-domain transfer** (paper_01; polar angle-lock): one shared metric spans risky and strategic
  choice, ~97–100% both ways, small within-domain price, half the parameters. The unification claim.
- **Reflection + aversion motif** (`polar_reflection.py`, `move2_social.py`): the loss domain is the
  gain domain mirrored across the value axis (ρ_SD = −0.8); the *same* motif recurs socially (self↔
  other reflection broken by inequality aversion). A real cross-domain structural through-line.

## The graveyard (tested, died — reported so no one re-walks these)

| conjecture | how it died |
|---|---|
| a **universal aversion angle** (one constant across all domains) | problem-selection confound: adversarial KT sets shift the angle; only holds within comparable samples |
| a **Shannon-Hartley conserved quantity** in the polar encoding | the normalized risk weight sign-flips with stakes (fourfold) — adaptation, not conservation. The real link is rational inattention (about *form*, not a conserved quantity) |
| **D₄ dihedral symmetry** (a rotation mixing value and probability) | V₄ only; the rotation-covariant term vanishes in the interior. Rectangle, not square |
| **V₄ as a general law** of risky choice | pre-registered held-out test on representative gambles: **0/3**. The V₄ is specific to the *curated* KT problem set, not choice in general; and it is **not** derived from the metric (low-rank Σ is EV-dominated, ≈0 weight on the risk coordinate) |

**Pattern:** every pretty structural overclaim was killed by a held-out or derivation test. That is the
method working. The survivors above are what remains after the firing squad.

## Track A status (the reflection-motif push) — honestly blocked

The proper test of whether the social domain has a **two-reflection** structure (a genuine social V₄)
needs choice-level 2-D allocation data (Charness–Rabin / Bruhin–Fehr–Schmerer). It is **not on Atlas**,
and public sources yield only *aggregate* dictator meta-studies (Engel 2011), not the (own, other)
choice structure. Moreover, **Fehr-Schmidt theory predicts the social domain is main-effect-dominated**
(envy α > guilt β, plus cost sensitivity) — i.e. *not* a pure-interaction V₄. So the expected and
observed social structure is **one reflection** (inequality aversion, Move 2), not two. A curated LLM
model-organism panel would re-confirm this at real cost; the honest open step is a real allocation
corpus.

## What the body of work can honestly claim — and what it needs for "Nobel-class"

**Can claim now:** a low-rank, transfer-capable decision metric whose non-monetary, encoding-invariant
predictions falsify the scalar-utility class — both confirmed on frozen, held-out/cross-model data.
That is a genuine, defensible contribution.

**Needs, to be more:**
1. **Human confirmation** of the projection-gap (the LLM panel is a model organism; humans are the
   decisive test). Protocol + gamified instrument built (`human_pilot/`), LLM-validated; the human run
   is the gate.
2. **Held-out confirmation of the loss-domain reflection** (the one Pillar-1 caveat).
3. A domain where the metric makes a **novel, quantitative, pre-registered prediction** that is then
   confirmed — not a re-description of a known regularity.

The symmetry work (V₄, D₄, angles) is honest texture and a memorable hook, but the load is carried by
the low-rank Σ and the encoding-invariant projection-gap. Consolidate there.
