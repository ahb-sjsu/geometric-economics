# Choice Has a Shape: Geometric Decision Theory

*Flagship / landmark synthesis. Draft. The single paper that sets the stage — it states the one idea,
proves why the incumbents must fail, describes the instrument that forces the failure, reports the
evidence that has survived held-out testing, and names precisely what remains unproven. It sits above
the four modular papers (theory, cross-domain transfer, projection-gap, symmetry) and is written to
the program's standard: the ambition is in the sharpness of the claim and the honesty of the ledger,
never in inflated results.*

---

## Abstract

Decision theory is fragmented: expected utility for risk, equilibrium and behavioral game theory for
strategy, social-preference models for fairness, cumulative prospect theory for the anomalies. Each is
**scalar** — it collapses an option onto a single number (a utility, a payoff, a value). We argue this
is not a modeling convenience but the source of the fragmentation, and we prove it is a **topological
impossibility**: if choice depends on two or more independent coordinates (money, fairness, identity,
epistemic status), *no continuous scalar utility can represent it without information loss*.
**Geometric Decision Theory (GDT)** replaces the scalar with a **geometry** — choice is movement on a
low-dimensional decision manifold under a Mahalanobis cost metric Σ with a stochastic (softmax) choice
rule. Every incumbent theory is then a **degenerate projection** of this geometry onto a subspace
(Nash = the monetary coordinate under best response; CPT = a scalar contraction of a lottery
submanifold). GDT makes a distinctive, falsifiable prediction the entire scalar class cannot: a
**projection-gap** — matched problems identical under *every* scalar projection but differing on one
active non-monetary coordinate, where the scalar class is *mathematically forced* to predict no
difference and the geometry predicts a signed gap whose **sign is invariant to any monotone
re-encoding** of the coordinate. On pre-registered, held-out tests the theory earns two things no
scalar account can: the projection-gap appears (in a language-model panel, cross-model), and **one
low-rank metric transfers across risky and strategic choice** at near-native accuracy. We are equally
explicit about what has *not* survived — a catalogue of falsified structural conjectures — and about
the one decisive test not yet run: confirmation in humans.

---

## 1. The fragmentation, and its single cause

A person choosing a gamble, splitting a pie, playing a game, and judging a moral trade-off is, to the
theories, four different animals. Expected utility, game theory, social-preference models, and prospect
theory share almost no machinery. This is usually treated as a division of labor. We treat it as a
**symptom**.

Every one of these theories is scalar: it maps an option `x` to a real number `u(x)` and predicts the
option with the highest number (up to noise). Scalarity is what makes them incompatible — each picks a
*different* scalar (money, own-payoff, a fairness-adjusted payoff, a probability-weighted value), and
there is no canonical way to reconcile them, because **there is no scalar that carries all the
coordinates at once**. That is not a failure of ingenuity; it is a theorem (§3).

## 2. The one idea: choice has a shape

GDT posits that an option is a point in a **low-dimensional decision manifold** whose axes are the
coordinates a decider actually weighs — monetary consequence, but also social impact, fairness,
identity, epistemic status, and a few more. Preference is a **Mahalanobis cost metric** Σ on this
manifold: the disutility of moving from a reference to an option is `√(Δᵀ Σ⁻¹ Δ)`, and choice is
`softmax(−cost/T)`. Two empirical facts, established below, give this content it would otherwise lack:
the metric is **low-rank** (a rank-1–2 precision matrix suffices — the coordinates are few and
coupled), and the temperature `T` is a **fixed information price** (rational inattention), not a free
knob.

The incumbents are not competitors but **shadows**. Restrict Σ to the monetary axis and take a single
best-response step: Nash equilibrium. Contract a lottery submanifold onto one scalar: cumulative
prospect theory. GDT does not discard them — it **locates** them, as projections that are exactly right
on their subspace and silent off it.

## 3. Why the scalar class must fail (the load-bearing theorem)

**Scalar irrecoverability.** Let choice depend continuously on coordinates including two that vary
independently. Then no continuous scalar `u` can reproduce the choice function without collapsing
distinct options that the decider distinguishes. The proof is topological: a continuous map from a
≥2-dimensional preference structure to ℝ cannot be injective on the relevant fibers; information is
necessarily lost. This is the *only* theorem GDT strictly needs, and it is only conditionally
load-bearing — it has teeth **only** where an experiment exhibits two options a scalar must equate but
a decider does not (§4). The other formal results (that any finite choice model embeds in a
one-dimensional cost model; that the incumbents are projections) are stated precisely so they can be
**disarmed**: they are true and, on their own, scientifically empty. GDT earns its keep only through
the empirics.

## 4. The instrument: forcing a wrong answer

The distinctive move is not to fit better but to **design a question the competitor must get wrong**.
A **projection-gap** is a matched pair of decision problems constructed so that *every* scalar
projection — expected utility, Nash, inequality aversion, CPT — assigns them identical value, while
they differ on one active non-monetary coordinate. The entire scalar class is then forced to predict
*no behavioral difference*. GDT predicts a **signed** difference, and — crucially — the *sign is
invariant to any monotone re-encoding* of the coordinate, so the prediction cannot be reverse-engineered
by a clever choice of units. Pre-register the signs before data, and a single experiment can *falsify
an entire class of theories at once*. This is the falsification engine that a within-domain
goodness-of-fit contest can never be.

## 5. What has survived held-out testing (the two pillars)

- **Pillar 1 — the metric is low-rank, and it transfers.** A single geometric metric, calibrated on
  risky choice, predicts human play in strategic games it was never shown (cross-domain transfer at
  ~97–100% of a native fit, at half the parameters). Pre-registered as a low-rank structural claim and
  re-tested on three held-out corpora — social-preference games, a 19-country prospect-theory
  replication (99% cross-country transfer), and a cross-lingual panel — it holds: **diagonal is beaten,
  full is unnecessary, rank 1–2 suffices**. No ensemble of domain-specialized scalar models can do
  this at any parameter count, because they share no coordinates to transfer.
- **Pillar 2 — the projection-gap appears.** On a pre-registered language-model panel (216 subjects, a
  six-model ladder, ~84k choices), the core prediction holds: the predicted signed gap appears on 5 of
  7 real contrasts, placebo-corrected, **cross-model (6/6)**, and not capability-gated — present in the
  weakest model, which rules out "only sophisticated agents show it." The scalar class predicts zero,
  by construction, on all of them.

Corroboration, not manufactured by us, comes from the mainstream social-preference literature: on real
individual data (Fisman–Kariv–Markovits; Charness–Rabin), choice is **utility-consistent** (~96% of
subjects), giving is **low-dimensional** (a two-parameter CES fits each subject), and the social metric
carries clean symmetries (self↔other reflection; an o₁↔o₂ exchange symmetry among recipients) — the
same low-dimensional, symmetric shape GDT posits, in a domain we did not design.

## 6. The discipline, and the graveyard

A theory is only as trustworthy as the tests it *failed*. Ours are on the record. We conjectured a
**universal aversion constant** (killed — the angle is confounded by problem selection), a
**Shannon-Hartley-style conserved quantity** in the polar encoding (killed — it is adaptation, not
conservation), a **dihedral D₄ symmetry** of the fourfold pattern (killed — the structure is Klein-four,
a rectangle not a square), and the **generality of that group structure** (killed — it does not
replicate on representative gambles; it is a property of the curated Kahneman–Tversky set). Every one
was retired by a held-out or derivation test, not by taste. What remains — the two pillars, the fixed
information price that repaired the temperature architecture, the reflection motif that recurs across
risk and social choice — remains *because* it survived. A reader can see exactly where the theory's
weight sits and where it does not; that visibility is the point.

## 7. The experiment — and why you should be the one to run it

We have done the hard part. What remains is a clean, cheap, decisive test, and we are trying to make it
irresistible.

**Look at one matched pair.** *Version A:* "a sure \$40, or a 50% chance at \$100 — the 50% is a
precisely known, machine-verified probability." *Version B:* identical wording, except "the '50%' is a
vague guess from an unreliable source." Same payoffs. Same stated probability. **Every scalar theory
you have ever used — expected utility, cumulative prospect theory, anything that scores the gamble by
its (probability-weighted) monetary value — is forced to predict that A and B are chosen at the same
rate.** They differ only in the *epistemic status* of the probability, a coordinate no scalar carries.
Geometric Decision Theory predicts, **in writing, before any data**, that people shift toward the sure
\$40 under B — and it predicts the **sign**, not a fitted magnitude, in a way you cannot dissolve by
re-scaling the coordinate: *any* monotone re-encoding of "how well-known is the probability" gives the
same prediction. Then the same instrument asks the *same coordinate in a trust game* (send \$10 on a
rumor vs an audited record) and predicts the *same sign* — one principle, two domains, no free
parameters.

**You win either way, and the result is clean.**
- If the gap is **absent**, you have falsified a newly-proposed theory on its own pre-registered turf —
  a crisp, publishable negative that no amount of our re-fitting can rescue (the signs were frozen and
  hashed).
- If the gap is **present**, you have shown that an *entire class* of decision theories — the scalar
  class, essentially all of behavioral and neoclassical choice — is provably incomplete on problems it
  cannot even distinguish, and you ran the experiment that showed it.

**The barrier is as low as we can make it.** The instrument is built and validated on 84,000
model-organism responses; the predictions are frozen (`prereg-v2`, sha256 `ca84eb4c`); the analysis
code is written (between-subjects, BH-FDR, placebo-corrected, attention-screened); the power analysis
is done. **N ≈ 500, roughly \$2,000 on Prolific, an eight-minute task, a couple of weeks.** You supply
the IRB and press go; everything else is in this repository.

**We especially want the skeptics.** The design is built for adversarial collaboration: pre-register
against us, choose your own coordinates, add your own scalar-model controls. The whole point of a
projection-gap is that a hostile experimenter and a friendly one must get the *same* answer, because
the scalar class's prediction is *forced*, not fit. There is no version of this experiment where the
result is ambiguous — and that is exactly why it is worth running.

## 8. What we claim, exactly

Choice is governed by a low-rank metric on a low-dimensional decision manifold; this geometry
**subsumes** the scalar incumbents as projections, makes an **encoding-invariant, pre-registered
prediction they are forced to fail**, and **transfers one metric across risky and strategic choice** —
both confirmed out-of-sample in a model organism and corroborated on real social-choice data. We do
**not** claim it is proven in humans (the gate), that it is a superior within-domain predictor (it is
not — its edge is unification and falsification), or that its every structural flourish generalizes
(most did not). Geometric Decision Theory is a **falsifiable geometry of choice with two pillars that
have survived held-out testing and one decisive experiment ahead**. That is the stage; the human study
is the next act.

Most theories ask to be believed. This one asks to be **shot at** — with a target we drew first, a gun
we loaded and handed you, and a wager that whichever way it fires, you publish. The stimuli are frozen,
the predictions are hashed, the code is written, the cost is two thousand dollars. The only thing
missing is the person who runs it. **Be that person.**
