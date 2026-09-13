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
- **Social-coordinate transfer** (`social_transfer.py`, `RESULTS_social_transfer_powered.md`): the
  *social* self↔other tradeoff transfers between FKM budget-line giving (3,800 individual choices) and
  Charness–Rabin dictator games — independently-fit shapes align at **cos 0.96**, angle-locked transfer
  **FKM→CR 100% / CR→FKM 45%** (same richer-domain-transfers-better asymmetry as the risk leg).
  **Supersedes** the underpowered 9-game move2c ("untestable"). Powered, bidirectional; honest bound is
  population heterogeneity in the *level* of other-regard (shared shape, recalibrated scale).
- **Reflection + aversion motif** (`polar_reflection.py`, `move2_social.py`): the loss domain is the
  gain domain mirrored across the value axis (ρ_SD = −0.8); the *same* motif recurs socially (self↔
  other reflection broken by inequality aversion). A real cross-domain structural through-line.

## The graveyard (tested, died — reported so no one re-walks these)

| conjecture | how it died |
|---|---|
| a **universal aversion angle** (one constant across all domains) | problem-selection confound: adversarial KT sets shift the angle; only holds within comparable samples |
| a **Shannon-Hartley conserved quantity** in the polar encoding | the normalized risk weight sign-flips with stakes (fourfold) — adaptation, not conservation. The real link is rational inattention (about *form*, not a conserved quantity) |
| **D₄ dihedral symmetry** (a rotation mixing value and probability) | V₄ only; at the corners the rotation-breaking E component is significant (χ² = 75.4, p = 4×10⁻¹⁷; free V₄ beats D₄-constrained on BIC). Rectangle, not square. **Corrected 2026-09-13:** this row previously read "the rotation-covariant term vanishes in the interior". That `+0.003` was pooled over 17 corner rows, and the interior chirality is neither zero nor stable — `prereg-d4stability-v2` moves it from `+0.23` to `−0.50` across stake quartiles of one corpus (Q = 103, p = 0.0005). The D₄ rejection stands on the corner E component alone |
| **V₄ as a general law** of risky choice | pre-registered held-out test on representative gambles: **0/3**. The V₄ is specific to the *curated* KT problem set, not choice in general; and it is **not** derived from the metric (low-rank Σ is EV-dominated, ≈0 weight on the risk coordinate) |

**Pattern:** every pretty structural overclaim was killed by a held-out or derivation test. That is the
method working. The survivors above are what remains after the firing squad.

**The graveyard is not exempt from re-examination.** The D₄ row retired a conjecture on the ground that
the interior chirality vanishes. It does not vanish, the number that said so was masked by pooling, and
the conjecture stays retired only because a second and independent ground holds. A rejection filed for
the wrong reason is a claim like any other.

**The `d·q` chirality is an artifact of the coordinate's endpoints, established on six lines.** `|d| = 1`
is not a place in the (d, q) plane, it is the set of gambles with no loss branch (`d = +1`) or no gain
branch (`d = −1`), verified on all 95,748 rows. There `d·q` degenerates into `±q`, so a pooled chirality
cannot be told apart from a probability effect of opposite sign in the two domains. Separating regimes:
pooled `d·q` = **+0.2506 ± 0.0423**, but **inside mixed gambles, where `d·q` is a genuine product, it is
−0.0303 ± 0.0728**. Replicated on the description arm, the full 382,992-decision experience arm, and each
of four experience press indices: never more than 0.8 se from zero in any of the six. The interior term
is `d²−q²` at **−0.6943 ± 0.0873**. Do not read D₄ or V₄ onto the fourfold pattern; the pattern lives
exactly where the coordinate degenerates. See `papers/d4stability/SEAM.md`.

**A caveat that now attaches to every κ coefficient in this file.** Estimating κ freely over the (d, q)
plane, with no functional form imposed, the six-term quadratic explains a weighted **R² = 0.361** of the
resulting surface, with a largest cell residual of 6.39 standard errors and a discontinuity of 1.29 in κ
across Δd = 0.038 at the |d| = 1 boundary. The six coefficients are **projections of a surface the basis
fits badly**, not parameters, and they move with whatever stimuli are in the sample. See
`papers/d4stability/RESULTS-v2.md`.

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
   confirmed — not a re-description of a known regularity. **Registered** (`prereg-coupling-v1`,
   `PREREG_cross_domain_coupling.md`): the choice-fit *risk* aversion angle predicts the same
   individual's choice-fit *social* other-regard angle, rank-1 coupling; incumbents predict zero.
   Confirmation gated on same-subject risk+social data (GPS, registration-gated) — registered, not yet
   confirmed.

The symmetry work (V₄, D₄, angles) is honest texture and a memorable hook, but the load is carried by
the low-rank Σ and the encoding-invariant projection-gap. Consolidate there.
