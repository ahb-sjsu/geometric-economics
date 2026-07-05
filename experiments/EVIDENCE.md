# Geometric Decision Theory (GDT) — Consolidated Evidence Ledger

*The honest state of the body of work. Distinguishes the results that survived pre-registered,
held-out testing (the pillars) from those that did not (the graveyard) and those that are real but
supporting. Written so the thesis rests weight only on what can hold it.*

*Name: the theory is **Geometric Decision Theory (GDT)** — "decision," not "economics," because its
distinctive content (encoding-invariant non-monetary coordinates, moral/epistemic and LLM choice)
spans decision-making beyond economic choice. "GDT" and, informally, "the geometry" / "the geometric
model" are used interchangeably below.*

---

## The thesis, in one sentence

**Geometric Decision Theory:** choice is movement on a low-dimensional decision manifold under a
Mahalanobis cost metric Σ with a softmax choice rule; the empirically load-bearing claims are that
(a) the metric is **low-rank**,
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

## Track A status (the reflection-motif push) — RESOLVED with real data

Completed on **Charness & Rabin (2002 QJE), Table I** — the seven two-person dictator games (real 2-D
allocation choice; own and other vary independently). Fehr-Schmidt fit: α≈0 (no envy in these games),
**β=0.34** (real advantageous-inequality aversion — people pay to reduce being ahead), self-regard as
the σ_s-reflection-breaking. The position asymmetry is a **significant main effect** (α=β rejected,
LR χ²=24.8, p<0.001) — not the pure interaction a V₄ needs.

**Verdict:** the *reflection + aversion motif* generalizes (self↔other reflection broken by self-regard,
mirroring value-reflection broken by loss aversion), but the **full V₄ does not** — swapping self↔other
*is* the inequality-sign flip, so the social domain has **one** reflection axis (ℤ/2), not risk's two
independent axes. Social = one reflection + main-effect inequality aversion, **not a V₄**. This
confirms the a-priori Fehr-Schmidt prediction on real data (`RESULTS_social_reflection.md`).

## Independent literature corroboration (from the social-preference PDFs)

Mining Fehr & Charness (JEL 2025), the Nunnari–Pozzi (2022) meta-analysis, Cooper–Kagel, and the
Fehr lecture surfaced independent, large-sample support for two of this program's own claims — from a
literature that never set out to test them:

- **Low-dimensional structure of preferences (supports Pillar 1, low-rank Σ, in the *social* domain).**
  Unsupervised **Dirichlet-process-means clustering** of distributional preferences independently
  recovers **~3 robust clusters** (altruistic, inequality-averse, predominantly selfish) across Swiss
  (N=816/916), Danish (N=3,691), German (N=2,583/2,794), and US (N=1,000) samples; the whole
  distribution is essentially the **2 parameters (α, β)**. Heterogeneous social behavior collapses onto
  a low-dimensional latent structure — the same shape as the low-rank metric finding, in a different
  domain, from independent data.
- **POWERED individual-level confirmation on FKM (2007) real data** (`RESULTS_fkm.md`, 76 subjects ×
  50 budget-line choices = 3,800 decisions). **T1:** 96% of subjects have convex, downward-sloping
  giving demand — choice is **utility/metric-governed** (the geometric premise; FKM's own GARP ≈90%).
  **T2:** a **2-parameter CES fits each subject** (mean R²=0.54) — the social preference is
  **low-dimensional**, the social analog of low-rank Σ, at the individual level. **T3:** strong
  self-regard (79% kept; median own-weight α=0.78) is the σ_s **reflection-breaking**. This is the
  powered social evidence the 9-game transfer test (Move 2c) could not reach — and it corroborates
  *both* load-bearing shapes (metric-governed + low-dimensional) in the social domain.
- **Reflection-symmetric social value function (corroborates the reflection + aversion motif).**
  The Fehr–Schmidt utility is a **kinked, reference-dependent value function around the equality line**,
  with the disadvantageous branch (envy α) weighted more than the advantageous branch (guilt β) — α ≥ β
  is exactly a **loss-aversion-role asymmetry** in social space (Fehr & Charness §4.1.4; Offerman 2002:
  negative emotions after unkind acts exceed positive after kind). This is the *self↔other reflection
  broken by an aversion field* that Move 2/2b found — here confirmed as the established functional form.
- **External check on the Move-2b fit.** Our Charness–Rabin dictator fit gives **β = 0.34**, matching
  the Nunnari–Pozzi meta-analytic dictator **β = 0.39** (41 studies). The advantageous-inequality
  aversion that drives the social reflection-breaking replicates the meta-analysis.
- **Scale/encoding-invariance (supports the invariance angle).** α, β are found **invariant to income /
  stake level** (Epper–Senn–Fehr); Fehr–Schmidt normalizes non-pecuniary terms by (n−1) and Rabin
  kindness by the payoff range — built-in scale-invariance, echoing the encoding-invariance of Pillar 2.
- **Cross-game transfer methodology (supports the transfer claim).** The canonical social-preference
  test is exactly *fit parameters in one game (ultimatum), transfer to others (dictator, public goods,
  trust, third-party punishment) with the same parameters* — the same fit-and-transfer logic as the
  cross-domain leg, long-established in this literature.

Net: the two load-bearing shapes of the thesis — **low dimensionality** and **a reflection-symmetric,
aversion-broken value structure** — are independently present in the mainstream social-preference
literature. That is corroboration, not proof, but it is corroboration the program did not manufacture.

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
