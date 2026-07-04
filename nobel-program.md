# From TCSS to a Decisive Theory — a research program

*A critical companion to `nobel-roadmap.txt`. Written against the current TCSS manuscript
(`revised_manuscript_v2.tex`, MAE 2.70%, 16/16) and its reviewer report.*

## 0. The honest framing (read this first)

Economics Nobels reward a *body of work that reshapes how the field thinks and is adopted by it*
— prospect theory (Kahneman), equilibrium existence and refinements (Nash), governing the commons
(Ostrom), mechanism design (Hurwicz/Maskin/Myerson). None was a single paper; each paired a
**theoretical reframing** with **decisive, repeatedly-replicated empirics** and **downstream tools
others used**. So the target is not "prove a theorem" — it is a 5–10 year program with three legs:
a clean theory, an empirical result standard theory *cannot* produce, and a tool people adopt.

The good news: **the roadmap's Layer 3 and the TCSS reviewer's "Room for improvement" are the same
list.** Both say the mathematical nesting is the easy part and the science lives in adversarial,
out-of-distribution, individual-level prediction under a *shared, low-complexity* metric. That
convergence tells you exactly where to spend effort.

## 1. What the theorem package actually buys you (and what it doesn't)

The four theorems in `nobel-roadmap.txt` are correct but must be framed honestly, because a hostile
economist will otherwise dismiss the whole package in one sentence ("of course a higher-dimensional
model contains lower-dimensional ones").

| Roadmap result | Truth status | Real scientific weight |
|---|---|---|
| **Thm 1** — any finite stochastic choice embeds in a 1-D geometric cost model (`C = K − T log p`) | **Trivially true** (it's just a re-labeling of the likelihood) | **~Zero.** This is a *representation* remark, not evidence. Demote it to a Remark; never let it be load-bearing. It proves embedding is *possible*, which is the criticism, not the defense. |
| **Thm 2** — Nash = argmin of geometric cost with `C = K − u` | **Trivially true** (best response ≡ cost-min under negated payoff) | **Low.** Legitimate nesting, but it's a restatement. Its value is expository: it fixes the `d₁`-only projection precisely. |
| **Thm 3** — CPT = scalar contraction of a lottery submanifold | **True by construction** | **Low–moderate.** A definitional embedding. Value: it pins the *specific* projection `π_CPT` so the strict-subsumption claim later is falsifiable. |
| **Thm 4** — no continuous injection `ℝᵈ→ℝ` for `d≥2`; scalarization is information-losing | **Genuinely true** (compactness + connectedness/topology) | **This is the one with teeth** — but *only conditionally*. It bites **iff** behavior genuinely depends on ≥2 independent dimensions. That antecedent is an empirical claim, not a theorem. |

**The load-bearing sentence of the entire program:** mathematical nesting is *necessarily* true and
therefore scientifically empty on its own; all the content lives in (a) the **parsimony** of the
*shared* metric and (b) **out-of-distribution cross-domain prediction that a projection provably
cannot make.** Theorem 4 + a strict-subsumption experiment are a *coupled pair*: Thm 4 says "if
behavior is ≥2-D, scalar theory must fail somewhere"; the experiment must *find that somewhere and
predict it*.

### The theorem you should actually prove (and it's not in the roadmap yet)

The roadmap's "strict subsumption" definition (conditions 1–4) is right but soft. The sharp,
publishable theorem is an **impossibility/identification result**:

> **Projection-Gap Theorem (target).** Let `M` be the geometric model with shared metric `Σ` and let
> `𝒫` be the class of its scalar/low-rank projections (Nash, CPT, EU, Fehr–Schmidt as singular
> limits `σ_k²→∞`). Construct a pair of decision problems `(x, x′)` that are **identical under every
> projection in `𝒫`** (same monetary payoffs, same lottery structure) but differ on an active
> non-monetary coordinate (`d₆/d₇/d₉`). Then *every* model in `𝒫` is forced to predict
> `behavior(x) = behavior(x′)`, while `M` predicts a specific, signed separation `Δ`. Any observed
> `Δ ≠ 0` falsifies the entire projection class simultaneously and is predicted quantitatively by `M`
> with **no free parameters re-fit**.

That is a *designed* experiment, not a curated benchmark — and it's the difference between "promising
bridge" (reviewer's verdict) and "decisive." It is also immune to the encoding critique if the pair
is constructed so the *contrast* is encoding-independent (see §2).

## 2. The single most dangerous criticism, and how to kill it

Reviewer technical flaw #1 (and thematic flaw #1): **the results may validate a hand-crafted encoding,
not a metric.** The certainty nonlinearity, the gain/loss flip, and the scenario coefficients are all
researcher-chosen. If an adversary believes the encodings are doing the work, nothing else matters.

Three escalating defenses (do at least the first two):

1. **Pre-register and externalize the encodings.** Fix coding rules *before* seeing outcomes; have
   ≥3 independent raters (or an automated text→attribute LLM pipeline with held-out validation) code
   each scenario; report inter-rater reliability (κ / ICC). This converts "researcher-specified" into
   "measured with known error." (Reviewer Room-for-improvement #2.)
2. **Encoding-invariant contrasts.** Design the Projection-Gap pairs so the *prediction is a
   difference* that is invariant to monotone re-encodings of the active coordinate. If the sign/rank
   of `Δ` survives any admissible encoding, the result cannot be an encoding artifact.
3. **Encoding-robustness theorem.** Prove that the strict-subsumption prediction is stable under the
   group of admissible encoding transformations (monotone, affine within a coordinate). This is the
   theoretical analogue of the gauge-invariance chapter already in the monograph (`ch08`).

## 3. The empirical redesign (reviewer's list = the program)

The current benchmark (16 aggregate targets, heterogeneous studies, ±5/10% tolerances) is the ceiling
on credibility. Replace it, don't patch it:

- **Individual-level data + likelihood.** Move from aggregate pass/fail to per-subject choice
  likelihoods; do real train/validation/test splits; report held-out log-loss, not tolerance passes.
  (Reviewer RFI #1, #3.) This alone answers flaws #2, #3, #4, #8.
- **Common-protocol baselines.** Re-estimate CPT, Fehr–Schmidt, random-utility/discrete-choice, and a
  flexible ML baseline **on the same training data under one likelihood**, and compare with
  cross-validated log-loss + a proper model-comparison criterion (WAIC/LOO, not just AIC on aggregates).
  (Reviewer flaw #5, RFI #5.) Anticipate: the geometric model must win on *cross-domain transfer*, not
  within-domain fit — that's the only comparison it can win honestly, and it's the one that matters.
- **Off-diagonal metric.** The diagonal restriction (flaw #6) is a self-inflicted wound: the theory is
  *about* interactions among social/moral/epistemic dimensions, then rules them out. Estimate a full
  (regularized) `Σ`; if the off-diagonals are ~0 you've earned the diagonal, and if they're not, the
  interactions are a *finding*. Either way you convert a weakness into a result.
- **Money-zero, tested adversarially.** Don't leave `d₁≈0` as an interpretive by-product — design
  high-stakes and money-salient regimes where a projection predicts strong monetary sensitivity and
  test whether `d₁` reactivates as `M` says. (Reviewer RFI #7; you already started this with the
  ultimatum stake-scaling test — make it the centerpiece, not a footnote.)

## 4. Sequencing (each phase is independently publishable)

1. **Theory paper** — the Projection-Nesting + Projection-Gap + Encoding-Invariance theorems, stated
   cleanly, with Thm 1 demoted to a remark. Journal of Economic Theory / Theoretical Economics /
   Games and Economic Behavior. *This is mostly writing; the math is in hand.*
2. **Decisive experiment** — one pre-registered Projection-Gap study (encoding-invariant contrast,
   individual-level, out-of-sample), where standard theory is forced into a wrong equality and `M`
   predicts the signed gap with no re-fit. This is the paper that changes minds.
3. **Adoption tool** — a mechanism-design or policy-simulation artifact (the monograph's `ch10`–`ch14`
   territory) that lets others *use* the geometry to design interventions that move behavior without
   moving money. Nobel-track impact is adoption, not elegance.

## 5. What to do to the TCSS paper *right now*

TCSS is the beachhead, not the destination. Get it accepted, but stop over-claiming:
- Apply the proofread fixes (remove revision-facing language; kill the companion-paper sentence in
  §VII.B; fix response-letter over-statements re "sample-size-weighted MAE" and "AIC/BIC").
- Reframe the contribution as **"a promising cross-domain bridge with an interpretable shared metric,
  and a pre-registered program to test it decisively,"** which is *exactly* the reviewer's own verdict
  — agreeing with the reviewer's framing is the fastest acceptance path.
- Add a "Threats to validity" subsection that states the encoding-dependence and aggregate-data limits
  in your own words, and points to the Projection-Gap design as the next step. Reviewers accept papers
  that name their own limits precisely.

## 6. Bottom line

The theorem package is real but, by itself, scientifically empty — nesting is guaranteed. The prize
is not the nesting; it is **a designed, encoding-invariant, individual-level prediction that the entire
class of scalar theories is provably forced to get wrong and your shared low-complexity metric gets
right with no free parameters.** Build that one result and the theory legs and adoption legs follow.
The reviewer already told you this; the roadmap already told you this; they agree. The work now is to
execute §2–§4, hardest part first: **Phase 2, the decisive experiment.**
