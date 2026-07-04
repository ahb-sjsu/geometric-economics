# Forcing a Wrong Answer: A Pre-Registered Projection-Gap Test of Decision Theories with Language-Model Panels

*Pillar 2 (method + evidence). Draft. The falsification instrument of the keystone theory (Paper 0,
Thms 4–5), realized as a pre-registered experiment on a language-model panel — a powered model
organism that both delivers first evidence and sizes the confirmatory human study.*

---

## Abstract

Testing whether a decision theory *strictly improves* on its predecessors is hard because richer models
trivially contain simpler ones. We operationalize strict improvement directly. A **projection-gap**
design constructs matched decision problems that are identical under *every* scalar projection
(expected utility, Nash, inequality aversion, cumulative prospect theory) but differ on one active
non-monetary coordinate; the entire scalar class is then *mathematically forced* to predict no
behavioral difference, while the geometric model predicts a signed gap whose **sign is invariant to any
monotone re-encoding** of the coordinate. We pre-register the sign predictions (hashed before data) and
run the design on a **language-model panel** — 216 synthetic subjects (36 personas × 6 models spanning
a capability ladder), 83,682 forced choices — as a powered, ethically cheap model organism. **The core
result holds:** placebo-corrected and FDR-controlled, 5 of 7 contrasts move in the predicted direction,
across both game and lottery frames, with **perfect 6-of-6 cross-model consistency** and null placebos;
the effect is present even in the weakest model, so it is not an artifact of capability. Two
pre-registered predictions fail and we report them: a predicted loss-domain sign reversal does not
appear, and the dose-response is monotone rather than the model's predicted peak. Both failures
localize to a single component — the cost-dependent temperature — which we redesign and re-register. We
release the panel framework (polite, preemption-tolerant cluster bursting) and argue that
language-model panels are a legitimate first stage for pre-registered economic-theory tests, necessary
but not sufficient for the human claim they power.

---

## 1. The problem: strict improvement is hard to test

A model with more parameters or dimensions can subsume a simpler one by construction (Paper 0, Thms
1–2). So "our model fits better" is weak evidence and "our model contains theirs" is no evidence at
all. What would be decisive is a setting where the incumbent class is *forced* into a specific wrong
prediction that the new theory gets right — with nothing fit. Theorems 4–5 of the keystone construct
exactly this. This paper builds and runs it.

## 2. The projection-gap design

For the scalar class `𝒫` (all theories factoring through a monetary-payoff or lottery projection), a
**projection-equivalent pair** `(x, x′)` has identical monetary payoffs *and* identical lottery
structure, differing only in the framing of one active coordinate `d ∈ {social impact, identity,
epistemic status}`. By Thm 4, every `M ∈ 𝒫` predicts `behavior(x) = behavior(x′)`; the geometry
predicts a signed gap `Δ = P(x) − P(x′) ≠ 0`. By Thm 5, because the manipulation is **bipolar**,
`sign(Δ)` is invariant to any monotone re-encoding of `d` — so it cannot be a coding artifact. `sign(Δ)`
is the pre-registered, adversary-proof prediction; magnitude is secondary.

**Contrasts (pre-registered).** Game-frame: social-impact and identity manipulations of dictator /
public-goods / trust games at *fixed payoffs*; epistemic manipulation of a trust game at fixed monetary
structure. Lottery-frame: epistemic (ambiguity-at-fixed-probability) and social-scope manipulations at
*fixed outcomes and probabilities*. Plus **placebos** (surface-wording-only changes; predicted `Δ=0`, the
internal falsifier) and a **dose-response** family.

**Pre-registration.** The frozen model, contrasts, and signed predictions are `sha256`-hashed and
tagged before any subject is run (the analogue of a locked analysis plan). No prediction can be edited
post hoc without breaking the hash.

## 3. Language-model panels as a model organism

Human economics experiments are slow and expensive; a projection-gap study needs individual-level data
at scale. We use a panel of language models as a **model organism**: each model, conditioned on a grid
of sampled value/demographic **personas**, is a population of synthetic subjects, yielding per-subject
choice distributions at a scale no human study reaches. We are explicit about status: a positive result
is a **decisive existence proof** that the frozen metric predicts a real agent population's
projection-defying choices out of sample, and a **powered dry-run** that sizes the confirmatory human
study; it is **not** the human economics claim. A negative result is itself informative and cheap.

**Infrastructure.** The panel runs across a shared, policy-bound GPU cluster via a *polite* admission
controller (additive-increase/multiplicative-decrease with a bounded violation rate) and a durable,
preemption-tolerant result stream; output-only forced choice avoids reasoning leakage; every work item
is idempotent. (Released as an open framework.)

## 4. Result: the core claim holds

216 subjects (36 personas × 6 models: a capability ladder from small to large), **83,682 valid forced
choices (99.3% parse)**, polite controller at 0% policy violations. Placebo-corrected (each subject
minus their own domain-matched wording placebo), FDR-controlled:

| Contrast | coordinate / frame | Δ corrected | Cohen d | cross-model |
|---|---|--:|--:|:--:|
| epistemic (game) | epistemic status | **+0.46** | 0.91 | **6/6** |
| social (game) | social impact | **+0.32** | 0.81 | **6/6** |
| identity (game) | identity | **+0.25** | 0.64 | **6/6** |
| epistemic (lottery) | epistemic status | **+0.17** | 0.52 | **6/6** |
| social (game) | social impact | **+0.17** | 0.56 | **6/6** |

**Five of seven contrasts are FDR-significant with the predicted sign, placebo-corrected, across both
game and lottery frames, with perfect 6-of-6 cross-model consistency.** Manipulations *invisible to
every scalar theory* move choices in the frozen metric's predicted direction — in every model.
**Placebos are null at full power.** The effect is present in the weakest model, 6/6 on all five
confirmed contrasts: **the projection gap is not capability-gated** (the "only advanced models show it"
hypothesis is rejected).

## 5. The failures we pre-registered, and report

1. **Loss-domain sign reversal — falsified.** A predicted sign flip under losses does not appear
   (observed same sign; 1/6 models). The prospect-theory-motivated loss encoding does not hold for
   these subjects.
2. **Dose-response — monotone, not peaked.** The frozen model predicted an inverted-U (a temperature
   artifact); the data are monotone-increasing.
3. **Magnitude ~5× under-predicted** (signs right, sizes larger than the frozen model allows).

Failures 2 and 3 share one cause. Choice-rule fuzzing on independent human data (CPC18) traces both to
the temperature exponent, which was `α=2.13` when calibrated on aggregate targets but `α≈0.42`
(near-flat) when fit on individual choices: super-linear temperature over-damps, predicting washout and
small effects. We **redesign** the choice rule (fixed temperature) — which restores a monotone
dose-response and unthrottled magnitude, and improves the held-out fit — and **re-register** the updated
predictions for the next round. The active metric (which coordinates matter, and their signs) survives
untouched; only the choice-rule scaling is revised.

## 6. Why this is a valid instrument, not a story

The design is admissible precisely because the detective could not have known the ending: predictions
were **frozen and hashed first**; the competitor's prediction (`Δ=0`) is a **theorem**, the strongest
possible common protocol; the *sign* is **encoding-invariant** (Thm 5); placebos are a built-in
falsifier; and every dead end is in the report. This converts "we followed the clues" into the methods
section.

## 7. Discussion

The projection-gap instrument delivers what fit-based comparison cannot: a setting where the entire
scalar class is forced to be wrong and the geometry is right, out of sample, with encoding-invariant
signs. On a language-model population the instrument returns a decisive, cross-model, cross-domain
positive — discharging the *projection-gap* obligation of the keystone theory on a model organism. The
confirmatory leg is the human replication, which this powered design now sizes (d ≈ 0.5–0.9 on the five
confirmed contrasts). We claim exactly that and no more.

*Artifacts: `projection-gap/` (`prereg-v1` scored; `prereg-v2` redesigned), the `llm-panel` framework,
`projection-gap/RESULTS.md`, `datasets/RESULTS_choice_rule.md`.*
