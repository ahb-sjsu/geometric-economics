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
rule. Restrict this geometry to the monetary coordinate under a single best response, and the Nash
condition reappears; contract a lottery submanifold onto one scalar, and cumulative prospect theory
reappears — each incumbent recovered exactly on its own subspace and silent off it. GDT makes a
distinctive, falsifiable prediction the dominant scalar theories cannot: a
**projection-gap** — matched problems identical under each of those scalar projections but differing on
one active non-monetary coordinate, so that each is *mathematically forced* to predict no difference
while the geometry predicts a signed gap whose **sign is invariant to any monotone re-encoding** of the
coordinate (and, because no single scalar carries every coordinate, a model patched to survive one gap
must fail on another). On pre-registered, held-out tests the theory earns two things no
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

Two operations on this single object are worth carrying out. Set every coordinate but money to zero and
let each player respond to the others' choices; the fixed points of the choice rule are its
equilibria — quantal-response equilibria in general, and the Nash equilibria as the temperature
vanishes. Collapse a lottery submanifold onto its monetary axis; what remains is a nonlinear value
function over outcomes with probabilities entering non-linearly — an object of the same kind as
cumulative prospect theory (the correspondence is structural; we do not claim to derive prospect
theory's particular weighting function). Neither operation adds anything to the geometry — each only
removes coordinates from it, and each result is exact on the subspace that survives and silent on the
axes that were switched off.

## 3. Why the scalar class must fail (the load-bearing theorem)

**Scalar irrecoverability.** Let choice depend continuously on coordinates including two that vary
independently. Then no continuous scalar `u` can reproduce the choice function without collapsing
distinct options that the decider distinguishes. The proof is topological: there is no continuous
injection of a space of dimension ≥ 2 into ℝ, so any scalar summary must identify options the decider
keeps distinct; information is necessarily lost. This is the *only* theorem GDT strictly needs, and it is only conditionally
load-bearing — it has teeth **only** where an experiment exhibits two options a scalar must equate but
a decider does not (§4). The other formal results (that any finite choice model embeds in a
one-dimensional cost model; that the incumbents are projections) are stated precisely so they can be
**disarmed**: they are true and, on their own, scientifically empty. GDT earns its keep only through
the empirics.

## 4. The instrument: forcing a wrong answer

The distinctive move is not to fit better but to **design a question the competitor must get wrong**.
A **projection-gap** is a matched pair of decision problems constructed so that each of the dominant
scalar theories — expected utility, Nash, Fehr-Schmidt inequality aversion, cumulative prospect theory —
assigns them identical value, while they differ on one active non-monetary coordinate. Each is thereby
forced to predict *no behavioral difference*. GDT predicts a **signed** difference, and — crucially —
the *sign is invariant to any monotone re-encoding* of the coordinate, so the prediction cannot be
reverse-engineered by a clever choice of units. A scalar model can, of course, be patched to carry the
offending coordinate; but by the theorem of §3 no single scalar carries them all, so a patch that
rescues one contrast has conceded the coordinate is real and will fail on the next. Pre-register the
signs before data, and a single experiment adjudicates the dominant theories of risky, strategic, and
social choice at once. This is the falsification engine that a within-domain goodness-of-fit contest
can never be.

## 5. What has survived held-out testing (the two pillars)

- **Pillar 1 — the metric is low-rank, and it transfers.** A single geometric metric, calibrated on
  risky choice, predicts human play in strategic games it was never shown (cross-domain transfer at
  ~97–100% of a native fit, at half the parameters). Pre-registered as a low-rank structural claim and
  re-tested on three held-out corpora — social-preference games, a 19-country prospect-theory
  replication (99% cross-country transfer), and a cross-lingual panel — it holds: **diagonal is beaten,
  full is unnecessary, rank 1–2 suffices** (the structural claim is strongest in the gain domain; the
  loss/reflection domain required a separate, and honestly weaker, reflection encoding). No ensemble of
  domain-specialized scalar models can do this at any parameter count, because they share no coordinates
  to transfer.
- **Pillar 2 — the projection-gap appears.** On a pre-registered language-model panel (216 subjects, a
  six-model ladder, ~84k choices), the core prediction holds: the predicted signed gap appears on 5 of
  7 real contrasts, placebo-corrected, **cross-model (6/6)**, and not capability-gated — present in the
  weakest model, which rules out "only sophisticated agents show it." Each of the enumerated scalar
  theories predicts zero, by construction, on all of them.

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

## 7. The decisive experiment

Two problems. In the first, a respondent chooses between a sure \$40 and a 50% chance of \$100, the
probability precisely known and machine-verified. In the second, the wording is the same to the letter,
except that the "50%" is now a vague estimate from a source described as unreliable.

Nothing about the payoffs has changed, and nothing about the stated probability. The
probability-weighted monetary value — the number expected utility computes, the number cumulative
prospect theory computes after its weighting — is, in both problems, exactly the same. Every theory
that values a gamble by its money and its odds is therefore obliged to treat these as one problem, and
to predict a single rate of choice.

The one thing that changed was how well the probability is known. No scalar valuation carries that
quantity; Geometric Decision Theory does. It predicts a shift toward the certain option, and predicts
the *sign* of the shift rather than its size, in a form that survives any monotone re-encoding of the
coordinate. Posed once more in a strategic setting — a trust game entered on an unverified rumor rather
than an audited record — the same coordinate returns the same predicted sign, from the same metric.

For the full set of such contrasts the signs were fixed and hashed before observation, and the design
has been carried through on a language-model panel, where the predictions held across models. The
corresponding measurement in human respondents has not been made.

## 8. What we claim, exactly

The claim is that choice is governed by a low-rank metric on a low-dimensional decision manifold; that
this geometry makes an **encoding-invariant, pre-registered prediction the scalar class is forced to
fail**; and that **one metric transfers across risky and strategic choice** — the first confirmed
out-of-sample in a model organism, the second on real human choice data spanning risky and strategic
tasks (and corroborated in social choice). The incumbent theories it does not oppose; §2 recovered them
within it. We do **not** claim it is proven in humans (the gate),
that it is a superior within-domain predictor (it is not — its advantage is unification and
falsification), or that its every structural flourish generalizes (most did not).

Geometric Decision Theory is a falsifiable geometry of choice with two pillars that have survived
held-out testing and one measurement outstanding. The predictions are frozen and the apparatus is
built; the measurement is in human respondents.
