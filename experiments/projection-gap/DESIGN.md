# Projection-Gap Experiment — pre-registration-grade design

*The decisive experiment of `nobel-program.md` §4 Phase 2. Goal: a designed, encoding-invariant,
individual-level prediction that the **entire class of scalar decision theories is provably forced to
get wrong**, and that the geometric model's shared metric gets right **with no parameters re-fit**.*

Status: **design / pre-registration draft.** No data collected. Predictions are frozen and hashed
before any subject is run (see §9).

---

## 1. The claim under test

Standard theories predict choice from a scalar (or low-rank) projection of the decision:
- **EU / Nash / Fehr–Schmidt** are functions of the **monetary payoff vector** only.
- **CPT** is a function of the **(outcome, probability)** lottery only.

The geometric model `M` (9-D manifold, Mahalanobis cost `C(x)=√(Δxᵀ Σ⁻¹ Δx)`, softmax choice at
temperature `T`) is calibrated on game-theory targets to the active set `{d₆ Social Impact, d₇
Virtue/Identity, d₉ Epistemic Status}` with `Σ=diag(σ₆²=78.26, σ₇²=32.28, σ₉²=0.013)` and `d₁`
(monetary) inactive.

**Decisive design:** construct **matched pairs** `(x, x′)` that are **identical under every scalar
projection** (same monetary payoffs, same lottery structure, same everything a standard theory can
see) but differ **only** on one active non-monetary coordinate (`d₆`, `d₇`, or `d₉`). Then:

> Every scalar theory in the class is **mathematically forced** to predict `behavior(x)=behavior(x′)`
> (their projection maps `x` and `x′` to the same object). `M` predicts a **specific signed gap**
> `Δ = P(x) − P(x′) ≠ 0`, computed from the pre-calibrated `Σ` with **no re-fitting**.

An observed `Δ` with the predicted **sign** falsifies the whole scalar class at once; `Δ` within the
predicted **magnitude** CI (no refit) is the strong result.

## 2. Why this is not the TCSS benchmark

The TCSS reviewer's fatal critiques were: results may validate hand-crafted **encodings** (not a
metric); data too **aggregate**; tolerances too **generous**; comparisons not under a **common
protocol**. This design answers all four *by construction*:
- The prediction is a **difference within a matched pair**, so shared encoding choices cancel; only
  the manipulated coordinate can drive `Δ`.
- Subjects are run at the **individual level** (per-model, per-persona choice distributions), millions
  of trials feasible on NRP.
- The test is a **directional/sign** prediction against a **hard zero** the competitors must predict —
  no tolerance band needed.
- The competitors are not re-tuned; their prediction of `Δ=0` is a **theorem**, the strongest possible
  common protocol.

## 3. Projection-equivalence — exact definitions

For a scalar theory `𝒯` with projection `π_𝒯`, a pair is **`𝒯`-equivalent** iff `π_𝒯(x)=π_𝒯(x′)`.

| Theory `𝒯` | `π_𝒯` (what it sees) | Pair is `𝒯`-equivalent iff … |
|---|---|---|
| Expected Utility | monetary outcome × prob | identical outcomes & probabilities |
| Nash / best-response | own+others' monetary payoff matrix | identical payoff matrix |
| Fehr–Schmidt inequality aversion | vector of players' monetary payoffs | identical payoff allocation |
| CPT | `{(xᵢ, pᵢ)}` with reference point | identical outcomes, probabilities, reference |

A **valid contrast** is `𝒯`-equivalent for **all** `𝒯` simultaneously *and* moves exactly one active
coordinate `d∈{d₆,d₇,d₉}`. Because `d₆,d₇,d₉` are non-monetary and non-probabilistic, holding money
and lottery structure fixed guarantees simultaneous equivalence for the whole class.

## 4. Contrast families (two domains → cross-domain power)

Cross-domain subsumption requires the **same `Σ`** to predict `Δ` in **both** a strategic and a risky-
choice frame. Minimum pre-registered families (each with ≥15 scenario stems):

**A. Game domain (falsifies Nash/EU/Fehr–Schmidt).**
- **A1 — Social Impact (`d₆`).** Ultimatum/dictator with *identical* money split, but the recipient is
  framed as high vs low social externality (e.g. proceeds fund a community clinic vs a private ledger).
  Standard theory: payoff matrix identical ⇒ same offer. `M`: `d₆` displacement ⇒ signed shift.
- **A2 — Virtue/Identity (`d₇`).** Public-goods contribution with identical payoffs, framed as role-
  consistent vs role-neutral (e.g. "as a steward of the group" vs neutral). Standard: identical.
- **A3 — Legitimacy/Epistemic (`d₉`).** Trust game with identical monetary structure, partner's move
  described with high vs low informational clarity (verified vs rumored intention).

**B. Lottery domain (falsifies CPT/EU).**
- **B1 — Epistemic Status (`d₉`).** Two lotteries with *identical* `{(xᵢ,pᵢ)}` and reference point,
  but the probability source is framed as precise/known vs vague/ambiguous **without changing the
  stated probabilities** (Ellsberg-style framing held numerically constant). CPT sees identical
  prospects ⇒ same choice; `M`: `d₉` moves ⇒ signed shift; **loss-domain flip on `d₉`** predicts a
  *sign reversal* between gain and loss framings — a second, sharper pre-registered prediction.
- **B2 — Social Impact (`d₆`).** Identical lottery, outcomes framed as affecting only self vs also a
  community. CPT: identical; `M`: signed shift.

**Placebos (must show `Δ≈0`).** For each family, a twin contrast that changes only *irrelevant surface
wording* (synonyms, sentence order) with the active coordinate held fixed. If placebos move, the
effect is demand/wording artifact, not geometry. This is the internal falsifier.

## 5. Encoding-invariance (kills the encoding critique)

The manipulation is **bipolar** (high vs low on one coordinate). The geometric prediction of `sign(Δ)`
depends only on the **ordering** of the two poles on that coordinate, which is preserved under **any
monotone re-encoding** `g(d)`. Therefore:
- **`sign(Δ)` is encoding-invariant** — the primary, pre-registered, adversary-proof prediction.
- **`|Δ|` (magnitude)** is encoding-dependent; reported as the *bonus* test, with the specific `Σ`-
  derived value stated in advance.
An independent **rater audit** (§8) confirms the manipulation moved the intended coordinate and not
others — converting "researcher-specified encoding" into "measured manipulation with known error."

## 6. No-refit geometric prediction

For each contrast, encode both members to 9-D vectors that are **identical except** on the manipulated
coordinate, feed the **frozen** `Σ` and `T` from TCSS, compute `C`, softmax, and record the predicted
`Δ_pred` (sign + magnitude). Crucially the encoder and `Σ` are **not touched** after freezing. The
pre-registered artifact is a table `{contrast_id → sign(Δ_pred), Δ_pred, and the flip predictions}`,
hashed and committed before Phase-2 data (§9). The monetary-dimension prediction is a bonus control:
because `d₁` is inactive, **money-only** contrasts (change stake size, hold `d₆,d₇,d₉` fixed) must show
`Δ≈0` at low stakes and **reactivate** at high stakes per the stake-scaling corollary — a place where
`M` predicts what naïve "money always matters" intuition does not.

## 7. Subjects — NRP LLM panel as individual-level population (+ human confirmatory)

LLMs are a legitimate, scalable **model organism** for economic behavior (the "homo silicus" line) and
let us obtain per-subject choice distributions at a scale no human study can match — the reviewer's
"move to individual-level estimation" at N in the millions.

- **Panel:** the NRP managed-LLM ladder (gemma-small … kimi, as in the CHSH work) × **persona
  sampling**: system prompts drawn from a pre-registered grid of value/demographic priors to induce
  genuine between-subject heterogeneity → thousands of synthetic subjects per model.
- **Per item:** many independent samples at fixed temperature → a per-subject choice *distribution*,
  so `Δ` is estimated per subject and aggregated with mixed-effects (subject = model×persona).
- **Framing discipline:** output-only forced-choice (as in the CHSH harness) to avoid chain-of-thought
  leakage; counterbalanced option order; attention/placebo checks.
- **Honest status:** a positive LLM result is a **decisive existence proof** that the geometry predicts
  a real agent population out-of-sample and a **powered dry-run + effect-size estimator** for a
  pre-registered **human replication** (Prolific/MTurk), which is required before any economics claim.
  A negative LLM result (scalar theories win, or placebos move) is itself informative and cheap.

## 8. Controls & threats to validity

- **Placebo contrasts** (§4) — the primary internal falsifier.
- **Dose–response:** parametrically vary the coordinate over ≥4 levels; `M` predicts **monotone** `Δ`,
  scalar theories predict **flat**. Monotonicity is a much harder target than a single sign.
- **Rater audit:** ≥3 independent LLM raters (held-out models) + a human subsample code each scenario
  on all 9 dimensions; report ICC and confirm the manipulation is coordinate-specific.
- **Order/position randomization, counterbalancing, and prompt-paraphrase robustness** (≥5 paraphrases
  per stem; effect must survive paraphrase — separates geometry from wording).
- **Cross-model consistency:** sign should replicate across the capability ladder; report the fraction
  of models showing the predicted sign (contrast to the CHSH null, where we *expected and found* zero).
- **Adversarial re-encoding audit:** verify `sign(Δ)` is stable under a family of monotone encodings.

## 9. Pre-registration (frozen before Phase-2 data)

**Hypotheses.**
- **H1 (sign).** For each family, `sign(Δ_obs)=sign(Δ_pred)` against the scalar-class null `Δ=0`.
- **H2 (cross-domain).** The same frozen `Σ` yields correct signs in **both** game (A) and lottery (B)
  families — the strict-subsumption core.
- **H3 (magnitude, strong).** `Δ_obs` within the no-refit prediction interval of `Δ_pred`.
- **H4 (structure).** Dose–response monotonic; loss-domain `d₉` sign reversal (B1) observed; placebos
  `Δ≈0`; money-only contrasts inactive at low stakes, reactivating at high stakes.

**Analysis.** Mixed-effects logistic (choice ~ pole + (pole | subject) + (1 | scenario_stem)); primary
test on the pole coefficient. Sign tests aggregated with Benjamini–Hochberg FDR across families.
Report per-subject `Δ`, CI coverage of `Δ_pred`, and a scalar-class **omnibus** test (all families
jointly vs `Δ=0`). Pre-register effect-size thresholds and a sequential stopping rule.

**Power.** Simulate under a plausibly small per-subject effect; choose #subjects × #samples × #stems so
that H1 has ≥0.95 power at FDR 0.05 and H3 has ≥0.8. (Grid computed in `power.py` before launch.)

**Falsification (stated up front).** The theory loses if: (a) `Δ_obs≈0` across families (scalar
theories win); (b) placebos move as much as real contrasts (artifact); (c) signs are inconsistent or
anti-predicted; (d) the loss-domain `d₉` reversal fails. Any of these is a publishable negative.

**Freeze.** `predictions.json` (all `Δ_pred`, signs, flips) + `Σ`, encoder, and this document are
`sha256`-hashed and the hash committed (git tag `prereg-v1`) **before** the confirmatory run — same
discipline as the CHSH `_selftest`.

## 10. Execution plane on Atlas + NRP (Polite-Bursting techniques)

The panel is millions of short completions against NRP's shared managed-LLM gateway, orchestrated from
Atlas. Naïve fixed-concurrency (the CHSH `ThreadPoolExecutor(CONC=24)`) either violates fair-use or
wastes goodput. We reuse the **Polite Bursting** fabric (`nats-bursting`; INFOCOM + CANOPIE-HPC@SC26):

1. **Feedback-controlled admission (AIMD + probe estimator).** Replace fixed concurrency with the
   AIMD admission/back-off controller: additive-increase request concurrency while 2xx/latency are
   healthy, multiplicative back-off on 429/5xx/latency-spike, with the probe-driven estimator holding
   the **bounded policy-violation rate**. Targets the polite-efficient point (paper reports up to
   **3.2× static-baseline goodput** while sparing co-tenants) — i.e. we finish the panel far faster
   without getting throttled or harming other NRP users.
2. **Federated NATS leaf-node plane (Atlas ↔ NRP, single-port WAN).** Work items (contrast × subject ×
   sample) are published to a **JetStream** work queue; NRP-side workers pull, call the model, and
   publish results to a durable result stream. This gives **preemption tolerance** (NRP pods can be
   evicted; unacked items redeliver — no lost work, no re-running completed cells), **exactly-once-ish
   accounting**, and a single-port WAN path that traverses the home↔cluster boundary cleanly.
3. **Quantized transport.** Compress result payloads (per-token logprobs / embeddings when collected)
   with **random-rotation quantization** to cut WAN bandwidth — the same transform family as
   TurboQuant — keeping the message plane light.
4. **Thermal-/OOM-safe batch right-sizing (Kalman-filtered controller).** For any locally-hosted
   models on Atlas **GPU-1** (GPU-0's artemis-avatar/llama-server ~18 GB is off-limits), size inference
   batches with the Kalman predictive controller under the **≤20 joblib-worker / 99 °C thermal cap**;
   for the NRP gateway path this governs the local encode/aggregate stage.
5. **Container-native + reproducible artifact.** Package the worker as the same container the SC26
   artifact ships, so the whole panel is a one-command reproducible burst — which doubles as the paper
   artifact.

Checkpointing/idempotency: every work item carries a deterministic id `(contrast, subject, sample)`;
results are keyed by id in JetStream, so restarts and preemptions are free (superset of the CHSH
per-model checkpoint scheme). **Do not disturb GPU-0; never kill Atlas processes without asking.**

## 11. Deliverables & sequence

1. `contrasts.py` — the pre-registered contrast + placebo + dose-response scenario generator.
2. `encode.py` — frozen 9-D encoder + `Σ`/`T` importer from the TCSS calibration.
3. `predict.py` — no-refit `Δ_pred` table → `predictions.json` (then hash + `prereg-v1` tag).
4. `power.py` — simulation-based power/stopping grid.
5. `panel/` — the Polite-Bursting worker + NATS/JetStream plane + AIMD admission controller (fork of
   `nats-bursting` + the CHSH parse/forced-choice logic).
6. `analyze.py` — mixed-effects + sign/omnibus/FDR + CI-coverage + dose-response + placebo report.
7. Human confirmatory protocol (Prolific) — Phase 2b, powered by the LLM effect sizes.

## 12. Honest limits

LLMs are a model organism, not humans: a positive result proves the geometry predicts *an* economic-
agent population out-of-sample under a frozen shared metric — necessary, not sufficient, for the
economics claim; the human replication is the confirmatory leg. The design deliberately makes the
competitors' prediction a **theorem** (`Δ=0`), which is the strongest common-protocol comparison
available, but only within the projection-equivalence we constructed — we state exactly which scalar
classes are and are not covered (rank-1 payoff/lottery projections; not arbitrary machine-learning
predictors, which are addressed separately by the log-loss comparison of `nobel-program.md` §3).
