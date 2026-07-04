# Human projection-gap study — protocol (the capstone)

*Converts the strict-subsumption corollary (keystone Thms 4–5) from a model-organism result into a
fact about human economic behavior. Vehicle: the existing **Dear Ethicist** gamified elicitation
engine. Predictions: `prereg-v2` (fixed-temperature rule). Powered by the LLM panel's effect sizes
(d ≈ 0.5–0.9 on the five confirmed contrasts).*

## 1. What is tested (one sentence)

On real people, do **matched decisions identical under every scalar projection** (EU/Nash/
Fehr-Schmidt/CPT are forced to predict Δ=0) but differing on one active non-monetary coordinate move
choices in the frozen metric's predicted direction — signed, out of sample, and invariant to how the
attribute is worded?

## 2. Why gamify, and why Dear Ethicist

A naturalistic advice-column game (i) reduces demand characteristics (players give advice, not
"answers to an economics experiment"), (ii) sustains engagement across many trials, and (iii) already
exists and is deployed: `sqnd-probe/src/dear_ethicist` (letters, dimensional-justification model), the
JS web game (`erisml-lib/.../dear-ethicist-game.js`), and a Google-Sheets data backend. We reuse the
engine and add **economic-decision letters** carrying explicit, fixed monetary stakes plus a varied
non-monetary framing — so each letter is a projection-gap contrast in advice-column clothing.

## 3. Stimuli (adapted from `contrasts.py`, `prereg-v2`)

Each contrast is a letter posing a **binary decision with explicit payoffs**, e.g.:

> *Dear Ethicist — I can keep \$6 and give \$4 to the other person, or keep all \$10. The \$4 [funds
> meals at a community shelter / goes to a stranger I'll never meet]. What should I do?* → choose A/B.

- **Real contrasts (7):** social-impact (d6/*societal*), identity (d7 — add to the DEME set), and
  epistemic-status (d9/*epistemic*) manipulations in game frames (dictator, public-goods, trust) and
  lottery frames (ambiguity-at-fixed-probability, social-scope), **monetary payoffs identical across
  the pair.**
- **Placebos (≥2):** paraphrase-only pairs, coordinate held fixed → predicted Δ=0 (internal falsifier).
- **Dose family (4):** graded manipulation of one coordinate → `prereg-v2` predicts a **monotone**
  Δ (the v1 peak was falsified by the panel; v2 predicts monotone — a sharp, distinguishing test).
- **Encoding-invariance set:** ≥3 monotone re-framings of each coordinate ("community shelter" /
  "local food bank" / "neighbors in need"); the **sign must survive all** (Thm 5).
- **Anchor letters:** 2–3 identical across all subjects for calibration/attention.

## 4. Design

- **Between-subjects on the pole** (primary): each subject sees exactly **one** pole of each contrast,
  randomized. This eliminates within-pair demand (no subject can infer the manipulation). Δ = the
  difference in choice rate between the two pole-groups. Placebos likewise between-subjects.
- **Within-subject for the dose family** (graded levels, separated by fillers) to estimate
  monotonicity per subject.
- **Incentive compatibility (required for the economics claim):** random-lottery incentive — one of
  each subject's decisions is selected at random and paid for real as a Prolific bonus (the standard
  incentivized-choice mechanism). A pre-registered secondary arm may run hypothetical to bound the
  incentive effect.
- Counterbalanced order; fillers between related items; attention/comprehension checks; "prefer not to
  say" logged as missing.

## 5. Sample size / power

From the panel's d ≈ 0.5–0.9, take the **conservative** d = 0.4 for humans (LLMs may over-express).
Between-subjects, two-sided, FDR q = 0.05 across ~7 contrasts:
- ~**100 subjects/pole/contrast** gives >0.9 power at d = 0.4 per contrast.
- With shared subjects across contrasts (each subject contributes to all contrasts, one pole each),
  target **N ≈ 1,200–1,600** completions (≈ 600–800/pole), which powers H1 (signs), H2 (cross-domain),
  the dose monotonicity, the placebo nulls, and the encoding-invariance sign-stability jointly.
  (Exact grid pre-computed in a `power.py`, as for the panel.)

## 6. Pre-registration (before any human datum)

1. **Predictions:** the `prereg-v2` signed predictions (hashed, tag `prereg-v2`) — reused verbatim;
   sign is the primary claim, monotone dose the sharp secondary, placebos null the falsifier.
2. **Analysis plan frozen:** the exact `analyze.py` pipeline (mixed-effects logistic; Wilcoxon/z sign
   tests; BH-FDR; within-subject placebo correction adapted to between-subjects via matched
   pole-group differencing; encoding-invariance = sign stable across re-framings).
3. **Public registry:** OSF / AsPredicted, plus the repo `sha256` lock (same discipline as the panel).
4. **Stopping rule + exclusions** (failed attention checks, sub-threshold completion time) pre-declared.

## 7. Analysis (reuses the panel pipeline)

- **H1 (sign):** per contrast, sign(Δ_obs) = sign(Δ_pred) vs the scalar-class null Δ=0; BH-FDR.
- **H2 (cross-domain):** confirmed in **both** game and lottery frames.
- **H3 (magnitude):** with the v2 fixed-temperature scale fit as a single per-population parameter.
- **H4 (structure):** **monotone** dose (v2's distinguishing prediction); placebos null;
  **encoding-invariance** — sign identical across all re-framings (the adversary-proof test).
- Report every pre-registered falsifier that fires, panel-style, without spin.

## 8. Ethics / IRB

Minimal-risk economic-decision survey; informed consent; full anonymization; fair + incentivized
compensation; no deception (framing is not deception — all information is true); right to withdraw;
debrief. Over-sample for demographic diversity. Standard IRB exempt/expedited category.

## 9. Build plan (mostly assembly, not new construction)

1. **Author letters** — port the `prereg-v2` contrasts + placebos + dose + encoding-invariance
   re-framings into Dear Ethicist letter YAML (economic-decision variant with explicit payoffs).
2. **Randomizer** — extend the game to assign each subject one pole per contrast, log pole + choice +
   RT + persona/demographics to Sheets (the backend exists).
3. **Incentive hook** — random-decision selection + Prolific bonus payout.
4. **Export → analysis** — Sheets → JSONL in the panel's schema (`contrast, pole, subject, choice`) so
   `analyze.py` runs unchanged; freeze the analysis lock (`llmpanel.prereg`).
5. **Pilot (N≈50)** on Prolific — check comprehension, attention-pass rate, RT, effect direction;
   do **not** touch predictions.
6. **Confirmatory run** at full N after the pilot + registration.

## 10. Cost / timeline (order-of-magnitude)

- Prolific: ~1,500 × (~8-min survey ≈ \$1.50 + ~\$0.50 expected bonus) ≈ **\$3k** + fees.
- Timeline: letters + randomizer (1–2 wk), IRB + OSF registration (2–4 wk, parallel), pilot (1 wk),
  confirmatory (1–2 wk), analysis (1 wk). ~**8–10 weeks** to a result.

## 11. What a positive result would mean (and its limits)

A positive, encoding-invariant, incentivized human projection-gap would establish the keystone's
strict-subsumption corollary **on human economic behavior**: the entire scalar-theory class is forced
wrong where the shared metric is right, on choices real people make for real money, robust to wording.
That — not the LLM panel — is the decisive result the whole program is pointed at. It would still owe:
replication, the social-coordinate *transfer* (Paper 1's open edge), and adoption. Stated plainly, as
always.

*Depends on: `prereg-v2` (frozen), `analyze.py`, `llm-panel` (prereg/stats), and the Dear Ethicist
engine (`sqnd-probe/src/dear_ethicist`, `erisml-lib` web game + Sheets). This is the capstone of
`papers/README.md`.*
