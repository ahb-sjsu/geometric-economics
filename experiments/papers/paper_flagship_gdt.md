# Choice Has a Shape: Geometric Decision Theory

*Flagship synthesis. Draft. A **projection theory of behavioral failure**: it names what each incumbent
scalar projection discards, builds matched problems identical under that projection, varies the
discarded coordinate, pre-registers the geometry's sign, and asks whether behavior moves. States the
model as equations, the claims as theorems with proofs, reports the evidence that has survived held-out
testing, and names precisely what remains unproven. It sits above the four modular papers (theory,
cross-domain transfer, projection-gap, symmetry). The ambition is in the sharpness of the claim and the
honesty of the ledger, never in inflated results.*

---

## Abstract

Decision theories scalarize too early. Expected utility, payoff-based game theory, social-preference
models, and cumulative prospect theory each reduce an option to a **domain-local sufficient statistic** —
money, own-payoff, a payoff vector, a probability-weighted value — and discard the rest before choice.
**Geometric Decision Theory (GDT)** instead represents an option as a displacement on a low-dimensional
**decision manifold** and evaluates it with a single **metric shared across domains** before a final
stochastic contraction. The target of the theory is not scalarity but **premature projection**.
Classical theories appear as *limiting projections* of this one object: payoff-only cost minimization
yields logit response, and Nash equilibrium in the zero-temperature best-response limit, while a
suitable contraction of a reference-dependent lottery submanifold yields CPT-like scalar valuation. The
theory is falsifiable through **projection-gap** designs — matched problems identical under the incumbents'
projections but differing on one active non-monetary coordinate. Such projections are *forced* to
predict no difference; in the dominance-case designs used here, GDT predicts a **signed** gap whose
direction is invariant to monotone re-encoding of the manipulated coordinate. On pre-registered,
held-out tests two claims survive that a domain-local projection cannot make: the projection-gap appears
in a language-model panel, across models, and **one low-rank metric *shape* transfers between risky and
strategic choice in both directions, with only scale recalibration**. We are explicit about
what has *not* survived — a catalogue of rejected structural conjectures — and about the one decisive
test not yet run: confirmation in humans.

---

## 1. The fragmentation, and its single cause

A person choosing a gamble, splitting a pie, playing a game, and judging a moral trade-off is, to the
theories, four different animals. Expected utility, game theory, social-preference models, and prospect
theory share almost no machinery. This is usually read as a division of labor. We read it as a
**symptom**.

Each theory summarizes an option by a single number — but so, in the end, does any decision rule that
outputs a choice. The trouble is not that the theories end in a scalar; it is that each computes its
scalar **domain-locally and prematurely**, from a projection that keeps only its own subspace (money,
or own-payoff, or a payoff vector) and discards the other coordinates *before* any option is compared.
**Premature, domain-local scalarization is what makes the theories incompatible** — each throws away
what another keeps — and it is what makes each of them wrong, in a specific and testable way, whenever
a discarded coordinate is behaviorally active. The target of the theory is therefore not scalarity but
**premature projection**.

## 2. The model

An option is a point `x ∈ ℝᵈ` on a **decision manifold** `M` whose coordinates are the attributes a
decider weighs — monetary consequence together with a few non-monetary ones (social impact, fairness,
identity, epistemic status). A reference `r ∈ M` fixes the status quo and `Δ(x) = x − r` is the
displacement an option demands. Preference is a **Mahalanobis cost**

> (1)  `C(x) = √( Δ(x)ᵀ P Δ(x) )`,   `P ⪰ 0`,   `rank(P) = k`.

`P` is a positive-semidefinite precision matrix; with `k < d` it is a **pseudometric on the active
subspace**, made a proper metric by an isotropic ridge (`P + εI`, `ε ↓ 0`). The **low-rank hypothesis**
is `k ∈ {1,2}`: the active subspace is small. Choice over a menu `𝒳 ⊆ M` is logit in the cost,

> (2)  `Pr(x ; 𝒳) = exp(−C(x)/T) / Σ_{y∈𝒳} exp(−C(y)/T)`,   `T > 0`,

with `T` a temperature the theory takes to be a fixed **information price** (rational inattention), not
a free parameter. Equations (1)–(2) are the whole of GDT; §5 supplies the two facts — that `k` is small
and `T` fixed — that keep them from being vacuous.

One clarification forestalls the obvious objection. GDT too contracts to a single number, the cost
`C(x)`, before the choice in (2); it is not "non-scalar" at the moment of decision. What distinguishes
it is *when* and *how* the contraction happens. The incumbents contract **domain-locally and
prematurely** — each discards the coordinates outside its subspace before any comparison — whereas GDT
carries every active coordinate in `Δ` and contracts them through **one metric shared across domains**.
The target of the theory is therefore not scalarity but *premature projection*.

Make this precise. Call a model **domain-local scalar** if its choice depends on `x` only through a
sufficient statistic `u(x) = φ(π(x))` for a projection `π : ℝᵈ → ℝᵐ`, `m < d`, onto a proper subspace.
Expected utility takes `π` to money; Nash, to own-payoff; Fehr–Schmidt inequality aversion, to the
`(own, others)` payoff vector; cumulative prospect theory, to a scalar value over *stated*
probabilities. Write `𝒫` for this class. (A model may always be enlarged by appending a coordinate to
`π`; §4 and §7 return to that move and show what it costs.)

## 3. Results

**Theorem 1 (projection irrecoverability).** *Let `π` discard a coordinate `z`, and let
`u(x) = φ(π(x))` be any model in `𝒫` with that projection. Then `u` is invariant to `z`, so for every
matched pair `(x, x′)` with `π(x) = π(x′)` but `z(x) ≠ z(x′)`, the model predicts `Pr(x) = Pr(x′)`. If
observed choice varies systematically with `z`, then `z` is behaviorally active and `π`-scalarization
is false for that domain.* — Immediate: `u(x) = φ(π(x)) = φ(π(x′)) = u(x′)`, and choice depends on `x`
only through `u`. ∎

This is the load-bearing result, and it is not the impossibility of scalar utility — a model *with the
right projection* fits perfectly. It is that a projection which **omits an active coordinate** is forced
into a false equality, exactly the equality a projection-gap exhibits (§4).

**Corollary (information loss).** No continuous contraction `u : M → ℝ` is injective on a
full-dimensional region of `M`; any scalar summary therefore loses coordinate information. Whether the
lost information is behaviorally active is an empirical question, settled by Theorem 1's matched pair.

**Proposition 2 (limiting correspondence).** *(i) Encode the monetary coordinate as cost-equivalent
payoff loss, `Δ_money ∝ K − u_i(s_i, s_{−i})`, so that minimizing `C` on that axis is maximizing payoff.
Then the finite-`T` rule (2) is a logit-response model, and in the zero-temperature best-response limit
`T → 0` its fixed points are the Nash equilibria. (ii) On a lottery submanifold, (1)–(2) can be embedded
as a scalar contraction over reference-dependent, probability-weighted coordinates, yielding CPT-like
scalar valuation.* — *Sketch.* (i) Under the payoff-loss encoding, `argmin_x C(x)` is best response; its
fixed points are the Nash equilibria, and the finite-`T` form is McKelvey–Palfrey quantal response.
(ii) A quadratic form contracted onto one axis is a curved value function, and probabilities enter the
contracted valuation non-linearly; we assert the *correspondence*, not an exact recovery of prospect
theory's weighting function, which would require an explicit construction (deferred to a companion). ∎
The incumbents are thus limiting projections of (1)–(2), exact on their subspace and silent off it. On
their own these correspondences establish only *containment*, not improvement; the improvement is
Theorem 3 and the empirics.

**Theorem 3 (dominance-case projection-gap invariance).** *Let `x_lo` and `x_hi` be matched menus in
which the manipulation changes coordinate `d` for one alternative only (say `A`), with the comparator
`B` fixed on `d`, all other coordinates held fixed, and no active cross-term involving `d`; let both
`d`-displacements of `A` lie on the same side of the reference. Then for any strictly increasing
reparameterization `g` of coordinate `d`,*

> `sign[ Pr(A ; x_hi) − Pr(A ; x_lo) ]`  *is invariant under `g`.*

*Proof.* With no `d`-cross-term, `C_A` depends on `d` only through `P_dd Δ_{d,A}²`, while `C_B` is
unchanged between the menus. A monotone `g` preserves the common sign and order of `Δ_{d,A}`, hence the
direction in which `C_A` moves between `x_lo` and `x_hi` relative to the fixed `C_B`, hence the sign of
the change in `C_B − C_A`, hence — through the strictly increasing logistic in (2) — the sign of the gap
in `Pr(A)`. ∎ Because the manipulated coordinate changes the relative cost of one option monotonically
while the comparator is fixed on that coordinate, a monotone re-encoding of `d` cannot reverse the sign.
(If both alternatives move on `d`, invariance needs a further single-crossing assumption; under a
general low-rank metric `d` couples to other coordinates, where the sign is invariant provided the
cross-term does not dominate. We state the dominance case, which the designs here satisfy, and defer the
rest.)

## 4. The instrument: forcing a wrong answer

Theorem 1 and Theorem 3 together define the experiment. Construct a matched pair `(x_lo, x_hi)`
identical under the sufficient statistics of the standard incumbents — expected utility, Nash/payoff,
inequality aversion, and cumulative prospect theory as conventionally specified over stated
probabilities — but differing on one active non-monetary coordinate `d`. By Theorem 1 **each of those
projections is forced to a null**, `Pr(A ; x_hi) = Pr(A ; x_lo)`. By Theorem 3 **GDT predicts a signed
gap** whose direction survives any monotone re-encoding of `d`. Freeze the sign before data.

A scalar model can, of course, be enlarged to carry `d` — `u = CPT(x) − λ · d(x)` is still scalar and
would predict the gap. But such a patch **concedes the projection-gap result**: it appends precisely the
coordinate the geometry already represents. Repeated patches, coordinate by coordinate, become an
*implicit coordinate system*; GDT's contribution is to **specify** that system, **constrain** it with a
shared low-rank metric, and **test** its transfer across domains — which an ad hoc sequence of patches
does not. A within-domain goodness-of-fit contest cannot produce this adjudication; a pre-registered
projection-gap settles the standard domain-local theories of risky, strategic, and social choice on a
single matched pair.

## 5. What has survived held-out testing

Two claims survive out-of-sample that a domain-local projection cannot make.

- **Pillar 1 — one low-rank metric transfers between domains, in both directions.** A single metric,
  fit on one domain, predicts the other with **no re-fit of the metric shape** — only a one-parameter
  scale recalibration: risk-trained metrics predict strategic play and game-trained metrics predict
  risky choice, at ~97–100% of a native fit and half the parameters, the scale-invariant tradeoff
  *shape* transferring across.
  Pre-registered as a low-rank structural claim and re-tested on three held-out corpora, it holds —
  diagonal beaten, full unnecessary, rank 1–2 sufficient — strongest in the gain domain (the
  loss/reflection domain needed a separate, and honestly weaker, reflection encoding). Standard
  domain-specialized models do not transfer without an additional cross-domain representation map —
  they share no coordinates to carry across.
- **Pillar 2 — the projection-gap appears.** On a pre-registered panel of **216 model agents** (LLM
  respondents across a six-model ladder, ~84k choices), the predicted signed gap appears on 5 of 7 real
  contrasts, placebo-corrected, **across all six models**, and not capability-gated — present in the
  weakest model. Each incumbent projection predicts zero, by construction, on every one.

The temperature is not tuned per contrast. A single **information price** `T` is fixed once on the
projection-gap panel — a fixed-`T` logit outperforms the original cost-dependent temperature there
(ΔBIC ≈ 140) — and held constant across all contrasts and dose levels; the gaps are therefore not a
temperature artifact.

| claim | data | N | pre-registered | held-out | baseline | result | status |
|---|---|--:|:--:|:--:|---|---|---|
| low-rank transfer (both directions) | CPC18 lotteries ↔ bogotá games | 694k choices / 110 games | structural (`prereg-sigma-v1`) | yes | native / diagonal / full | 97–100% | survived |
| prospect replication | Ruggeri 19-country PT | 4,098 resp. / ~69k | signs frozen | yes | CPT / diagonal | 99% cross-country (H1 marginal) | survived (gain domain) |
| projection-gap | LLM panel | 216 model agents / 84k | `prereg-v1` | yes | scalar zero-gap | 5/7, 6/6 models | survived |
| social low-dimensionality | Fisman–Kariv–Markovits budget lines | 76 resp. / 3,800 | — | corroboration | — | ~96% utility-consistent, 2-param CES | corroborates |
| human projection-gap | human respondents | ~500 (not run) | signs frozen (`prereg-v2`) | pending | scalar zero-gap | pending | **gate** |

Independent corroboration, which we did not design, comes from the mainstream social-preference
literature: on real individual data (Fisman–Kariv–Markovits; Charness–Rabin), choice is
utility-consistent (~96% of subjects), giving is low-dimensional (a two-parameter CES fits each
subject), and the social metric carries clean symmetries (self↔other reflection; an o₁↔o₂ exchange
symmetry among recipients) — the same low-dimensional, symmetric shape the model posits, in a domain we
did not build.

## 6. The discipline, and the graveyard

A theory is only as trustworthy as the tests it *failed*. Ours are on the record. We conjectured a
**universal aversion constant** (rejected — the angle is confounded by problem selection), a
**Shannon–Hartley-style conserved quantity** in the polar encoding (rejected — it is adaptation, not
conservation), a **dihedral D₄ symmetry** of the fourfold pattern (rejected — the structure is
Klein-four, a rectangle not a square), and the **generality of that group structure** (rejected — it
does not replicate on representative gambles; it is a property of the curated Kahneman–Tversky set).
Each was retired by a held-out or derivation test, not by taste. What remains — the two pillars, the
fixed information price that repaired the temperature rule, the reflection motif that recurs across risk
and social choice — remains *because* it survived. A reader can see exactly where the theory's weight
sits and where it does not; that visibility is the point.

## 7. The decisive experiment

Two problems. In the first, a respondent chooses between a sure \$40 and a 50% chance of \$100, the
probability precisely known and machine-verified. In the second, the wording is the same to the letter,
except that the "50%" is now a vague estimate from a source described as unreliable.

Nothing about the payoffs has changed, and nothing about the stated probability. Expected utility and
cumulative prospect theory as conventionally specified both value the gamble by its money and its
*stated* odds; each is therefore obliged to treat these as one problem, and to predict a single rate of
choice.

The one thing that changed was how well the probability is known. Neither expected utility nor standard
cumulative prospect theory over stated probabilities carries that quantity; the geometry does — as
displacement on an epistemic coordinate — and predicts a shift toward the certain option, and predicts
its *sign* rather than its size, in a form that survives any monotone re-encoding. A reader will object
that ambiguity-sensitive scalar models — maxmin, smooth ambiguity, robustness — *do* carry it. They can
carry it only by appending precisely the coordinate the geometry already contains, which is the claim,
not its refutation. What no single such model does
is carry this coordinate *and* the social and identity coordinates the same instrument manipulates in
turn; that is the content of Theorem 1.

To separate the epistemic-status cost from a mere shift in believed probability, the design elicits, per
respondent, a subjective probability and a confidence/source-reliability rating, and tests whether
reliability moves choice **conditional on the elicited probability**. Posed once more in a strategic
setting — a trust game entered on an unverified rumor rather than an audited record — the same
coordinate returns the same predicted sign, from the same metric.

For the full set of such contrasts the signs were fixed and hashed before observation, and the design
has been carried through on the language-model panel, where the predictions held across models. The
corresponding measurement in human respondents has not been made.

## 8. What we claim, exactly

GDT is a **projection theory of behavioral failure**: standard decision theories fail not because they
end in scalars, but because their domain-local projections discard active coordinates; projection-gap
experiments expose those discarded coordinates, and a shared low-rank metric explains why the same
coordinates recur across risky, strategic, and social choice.

Precisely: the claim is that many choices are governed by a low-rank metric on a low-dimensional
decision manifold; that standard theories fail when their **domain-local projections omit an active
coordinate**; and that GDT exposes such failures through **pre-registered, dominance-case projection-gap
designs whose signs are invariant under monotone re-encoding** of the manipulated coordinate. The target
is not scalarity but premature projection. Its two positive obligations are met out-of-sample: the
projection-gap appears in a model-agent (LLM respondent) panel, and one metric *shape* transfers between
risky and strategic choice in both directions, with only scale recalibration (and is corroborated in
social choice). The incumbent theories it does not oppose; Proposition 2 places them within it as
limiting projections. We do **not** claim it is proven in humans (the gate), that it is a
superior within-domain predictor (it is not — its advantage is unification and falsification), or that
its every structural flourish generalizes (most did not).

Geometric Decision Theory is a falsifiable geometry of choice with two pillars that have survived
held-out testing and one measurement outstanding. The predictions are frozen and the apparatus is
built; the measurement is in human respondents.
