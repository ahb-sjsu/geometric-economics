# The Geometry of Economic Choice: Scalar Irrecoverability, Projection Nesting, and Strict Subsumption

*Keystone (theory) paper. Draft. States the central reframing as mathematics: the theorems on which
the empirical pillars (cross-domain transfer; the projection-gap experiments) rest. Written to be
honest about which results are mathematically necessary and therefore scientifically empty on their
own, and which acquire content only through the empirics.*

---

## Abstract

We formalize economic choice as movement on a low-dimensional decision manifold under a Mahalanobis
cost metric with a stochastic (softmax) choice rule, and prove four results relating this geometry to
the two dominant descriptive theories. **(Representation)** any finite stochastic choice model embeds
in a one-dimensional geometric cost model — a triviality we state only to disarm it. **(Nesting)**
Nash equilibrium is the restriction of the geometry to the monetary coordinate under single-step best
response, and cumulative prospect theory is a scalar contraction of a lottery submanifold; both are
**degenerate projections** of the full model. **(Scalar irrecoverability)** if choice genuinely
depends on two or more independent coordinates, no continuous scalar utility can represent it without
information loss — a topological impossibility, not a modeling preference. **(Strict subsumption)**
one can construct decision problems that are identical under *every* projection in the scalar class
yet differ on an active non-monetary coordinate; the entire class is then *forced* to predict no
behavioral difference, while the geometry predicts a signed gap whose **sign is invariant to any
admissible re-encoding of the coordinate**. The mathematical nesting is necessary and hence carries no
empirical weight by itself; all scientific content lives in (i) the *parsimony* of a shared metric
and (ii) the *empirical confirmation of a projection gap*. We state exactly where each obligation
falls.

---

## 1. The honest frame

A high-dimensional model can subsume lower-dimensional ones by construction; a universal approximator
"explains" everything and therefore nothing. We take this objection as the organizing principle of the
paper rather than a footnote. Our theorems separate cleanly into two classes:

- **Necessary (empirically empty):** the representation and nesting results (Thms 1–2). They show the
  older theories *can* be written as projections. This is a fact about notation, not about behavior,
  and we flag it as such.
- **Contentful (empirically loaded):** scalar irrecoverability (Thm 3) and strict subsumption
  (Thms 4–5). These bite only under an empirical antecedent — that choice is genuinely ≥2-dimensional
  — and they specify exactly the experiment that would establish it.

The theory's job is to make the empirical claim *sharp and falsifiable*, not to win by subsumption.

## 2. Setup

An economic situation is a point `a ∈ E ⊆ ℝ^d`. A choice alternative `x` induces a displacement
`Δ_x ∈ ℝ^d`. The behavioral cost of `x` is the Mahalanobis distance
`C(x) = √(Δ_xᵀ Σ⁻¹ Δ_x)` for a positive-definite `Σ`, and choice is stochastic,
`P(x) = exp(−C(x)/T) / Σ_y exp(−C(y)/T)`. A **coordinate k is inactive** when `σ_k² → ∞` (movement
along `k` is free); the active set is `{k : σ_k² < ∞}`. A **projection** `π_S : ℝ^d → ℝ^{|S|}` retains
coordinates `S`; a **degenerate projection** sends `σ_k² → ∞` for `k ∉ S`.

Let `𝒫` be the **scalar-theory class**: all models whose predictions factor through a rank-≤1
projection of `(E, Σ)` — the monetary-payoff projection (expected utility, Nash, inequality aversion)
and the lottery projection onto `(outcomes, probabilities)` (cumulative prospect theory).

## 3. Representation and nesting (necessary; stated to be disarmed)

**Theorem 1 (Representation; a remark).** *Any finite stochastic choice model with strictly positive
choice probabilities `p(a_i)` embeds in a one-dimensional geometric cost model.* Set
`C(a_i) = K − T log p(a_i)` with `K` large enough for nonnegativity; softmax over `−C/T` returns
`p`. ∎

We label this a remark, not a theorem, because it proves only that embedding is *possible* — precisely
the criticism, not a defense. It is never load-bearing in what follows.

**Theorem 2 (Projection nesting).** *(a) For a finite normal-form game, define `C_i(s_i;s_{−i}) =
K_i − u_i(s_i,s_{−i})`; then `s_i` is a best response iff it minimizes `C_i`, so a Nash equilibrium is
exactly a profile in which every agent minimizes geometric cost on the `d₁`-only projection. (b) For a
lottery `L`, `V_CPT(L) = φ(π_CPT · e(L))` for the projection onto reference-dependent risk coordinates
and the CPT scalar valuation `φ`; softmax over `−(K − V_CPT)` reproduces stochastic CPT, and the
deterministic preference is the `T→0` limit.* Both are immediate from the definitions. ∎

Interpretation: classical game theory and prospect theory are **degenerate projections** — special
cases at specific singular limits of `Σ`. This is genuine structure (it fixes *which* projection each
theory is), but it is not yet evidence that the fuller geometry is *true*.

## 4. Scalar irrecoverability (the load-bearing theorem)

**Theorem 3 (Scalar irrecoverability).** *If `d ≥ 2`, there is no continuous injection
`φ : [0,1]^d → ℝ`. Consequently, if the choice correspondence depends on two or more independent
coordinates, no continuous scalar utility represents it without information loss.*

*Proof.* Suppose `φ` were a continuous injection. `[0,1]^d` is compact and `ℝ` is Hausdorff, so `φ` is
a homeomorphism onto its image, a compact connected subset of `ℝ`, i.e. an interval `I`. Removing an
interior point disconnects `I`; removing any point from `[0,1]^d` with `d ≥ 2` leaves it connected. A
homeomorphism preserves connectedness under point removal — contradiction. ∎

The economic force is conditional and we state the condition precisely: the theorem bites **iff** the
antecedent holds — that behavior genuinely varies along ≥2 independent coordinates. That antecedent is
**not** a theorem; it is an empirical claim, and it is exactly what the projection-gap experiments
(Pillar 2) are built to establish. Thm 3 and the empirics are therefore a *coupled pair*: the theorem
says "if choice is ≥2-D, scalar theory must fail somewhere"; the experiment must *find that somewhere*.

## 5. Strict subsumption and the projection gap (the falsifiable core)

**Definition (projection-equivalent pair).** A pair `(x, x′)` is `𝒫`-equivalent if `π(x) = π(x′)` for
every projection `π` in the scalar class — identical monetary payoffs *and* identical lottery
structure.

**Theorem 4 (Projection gap).** *Let `(x, x′)` be `𝒫`-equivalent but differ on an active coordinate
`d` (`σ_d² < ∞`). Then every model in `𝒫` predicts `behavior(x) = behavior(x′)`, whereas the geometry
predicts `C(x) ≠ C(x′)` and hence `P(x) ≠ P(x′)`. Any observed `behavior(x) ≠ behavior(x′)` falsifies
the entire class `𝒫` simultaneously and is predicted, in direction, by the geometry with no free
parameters.*

*Proof.* Each `M_𝒫 ∈ 𝒫` factors as `g ∘ π` for some scalar projection `π`; `π(x) = π(x′)` gives
`M_𝒫(x) = M_𝒫(x′)`. For the geometry, `x` and `x′` differ only on `d`, and `σ_d² < ∞`, so
`Δ` contributes to the Mahalanobis norm and `C(x) ≠ C(x′)`. ∎

**Theorem 5 (Encoding invariance / gauge).** *If the manipulation moving coordinate `d` is bipolar
(monotone: one pole strictly exceeds the other on `d`), then `sign(P(x) − P(x′))` is invariant under
every admissible re-encoding `g` of `d` (any strictly monotone reparameterization). Magnitude is not
invariant.*

*Proof.* The sign of the cost difference along `d` depends only on the ordering of the two poles on
`d`, which a strictly monotone `g` preserves; the softmax is monotone in `−C`. ∎

Theorem 5 is the answer to the sharpest objection — that the results merely validate a hand-crafted
encoding. The *sign* of the projection gap is a gauge-invariant prediction: it survives any monotone
re-encoding of the manipulated coordinate, so it cannot be an artifact of the researcher's coding
scale. (This is the decision-theoretic analogue of gauge invariance in the framework's field-theoretic
formulation.)

**Corollary (strict subsumption).** *The geometry strictly subsumes the scalar class `𝒫` if, in
addition to the nesting of Thm 2, there exists a `𝒫`-equivalent pair on which the sign predicted by
Thm 4 is empirically confirmed out of sample. Absent such a pair, the geometry merely contains `𝒫`;
with it, the geometry strictly improves on `𝒫`.*

## 6. What is proved, and what is owed

| Result | Status | Scientific weight |
|---|---|---|
| Thm 1 (representation) | necessary | none — a notational remark |
| Thm 2 (nesting) | necessary | fixes which projection each theory is; not evidence |
| Thm 3 (scalar irrecoverability) | topological fact | **decisive, but conditional** on ≥2-D behavior |
| Thm 4 (projection gap) | proved | **the falsification instrument** |
| Thm 5 (encoding invariance) | proved | neutralizes the encoding critique for the *sign* |

**The two obligations the theory cannot discharge on its own**, and which the empirical pillars must:

1. **Parsimony.** That a *single, low-complexity* metric `Σ` — not a bespoke fit per domain — governs
   behavior across domains. (Pillar 1: cross-domain transfer of one metric between risky choice and
   strategic games.)
2. **A confirmed projection gap.** That a `𝒫`-equivalent, encoding-invariant, out-of-sample prediction
   is empirically borne out — signed as Thm 4 requires. (Pillar 2: the pre-registered projection-gap
   experiments.)

The mathematics makes the claim sharp and falsifiable; it does not make it true. That is the correct
division of labor, and stating it plainly is what protects the program from the subsumption objection.

## 7. Relation to the empirical pillars

- **Pillar 1** supplies the parsimony obligation: it shows that the aversion-angle *shape* of `Σ`
  transfers across the risk and strategy domains (a shared metric, not two fits), which no member of
  `𝒫` can even express, since no scalar theory spans both domains.
- **Pillar 2** supplies the projection-gap obligation: it constructs `𝒫`-equivalent pairs, freezes the
  Thm-4 sign predictions before data, and tests them — first on a language-model panel (a powered
  model organism), then on humans.
- **The capstone** (human confirmation) is what converts "the geometry strictly subsumes `𝒫`" from a
  conditional corollary into an established fact about human economic behavior.

## Appendix (to be written)
- Full proofs (Thms 3–5), including the measure-theoretic statement of "depends on ≥2 independent
  coordinates" and the admissible-re-encoding group for Thm 5.
- The singular-limit topology of `Σ` (`σ_k² → ∞`) and its relation to the identified active set.
- Complexity accounting for `Σ` (the parsimony obligation made quantitative).
