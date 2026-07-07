# prereg-coupling-angle-v1 — The Gold-Standard Cross-Domain Coupling Test (same-subject, angle-to-angle)

**Status:** DRAFT for author review — not yet frozen (see §9). Nothing here is a registered claim until the freeze in §9 is executed.
**Supersedes-as-gold-standard, does not retract:** `prereg-coupling-v1` (`PREREG_cross_domain_coupling.md`, sha256 `1eac580f…`). That prediction stands as frozen; it was scored on the Global Preferences Survey and **failed on the proxy** (`RESULTS_coupling_scorecard.md`): GPS ships preference *scores*, not choice-fit angles, and its P2 (rank-1) failed decisively. This document specifies the test the proxy could not be — fitting the geometric angles from each person's **raw choices** in both domains — which is the only test that can *confirm* the coupling.
**Author:** Andrew H. Bond, San José State University. **Companion:** GDT Part I & II; `prereg-sigma-v1`, `prereg-dimensions-v1`.

> **Global caveat, stated first.** Per-person angles fit from a finite number of choices are
> **noisy**. A raw across-subject angle correlation is *attenuated* by that noise; a naive raw
> correlation therefore under-states the true coupling and is not, by itself, the test. The
> confirmatory statistic is **measurement-error-corrected** (§4.3), and every threshold below is set
> on the corrected quantity with the raw reported alongside. This is pre-committed, not a post-hoc
> rescue.

---

## 1. What GDT predicts, restated at the level this test measures

Geometric Decision Theory says one low-rank metric Σ governs choice across domains. Its individual-level
consequence, from `prereg-coupling-v1`:

- **P1 (sign).** The **risk aversion angle** θ_risk (fit from a person's *lottery* choices, Part II §III
  risk encoding) and the **other-regard angle** θ_social (fit from that *same* person's *allocation*
  choices, Part II Result 4 social encoding) are **positively coupled** across individuals.
- **P2 (rank-1).** Across ≥ 3 choice-fit coordinate angles (§3), a **single latent factor** explains the
  cross-domain association — partialling it out removes the risk↔social correlation. This is the
  individual-level image of the Pillar-1 low-rank Σ result and is what goes *beyond* the known
  "preferences somewhat correlate" regularity.
- **P3 (encoding-invariance).** The **sign** of P1 is invariant to any monotone re-encoding of the
  social coordinate (Theorem 2, dominance case), so it is not a coding artifact.

**Why angles and not scores (the Keep-the-Angle grounding).** That the *angle*, not the magnitude, is
the geometry-carrying invariant is not a GDT stipulation — it is a general principle with independent
support and a theorem. `the-angular-observer` (Bond 2026; `theorem.md`, `crosssubstrate.py`) shows that
in spectral embeddings the **radial** coordinate is *provably* geometry-free (von Luxburg–Radl–Hein
resistance degeneracy: radius → local-degree noise) while the **angular** coordinate carries the
geodesic geometry universally across substrates (angle-ρ ≈ 0.82–0.93 vs a random-mode control ≈ 0). The
same "keep the scale-invariant direction, discard the magnitude" move recurs in PolarQuant KV-cache
compression, Ng–Jordan–Weiss row-normalization, and — listed there explicitly — the GDT **aversion
angle**. Two consequences for this test:
  1. **It is the right instrument.** The coupling, if it exists, lives in the *angles*; testing it
     angle-to-angle is an instance of a theorem-backed principle, not an internal choice.
  2. **It diagnoses the proxy failure.** GPS preference *scores* are magnitude-laden survey indices —
     the radial, geometry-free coordinate in the Keep-the-Angle picture — which is one reason the
     `prereg-coupling-v1` proxy could not see the structure even if it were present. This test removes
     that confound by fitting angles from choices directly.

**Incumbent contrast (why this is not free).** CPT (risk) and Fehr–Schmidt / CES giving (social) are
separate models with **no shared parameter**. Calibrated independently per person, they place **no
constraint** on corr(θ_risk, θ_social): the incumbent prediction is **0**. GDT predicts a specific,
positive, **rank-1** coupling. The gap between "0, unconstrained" and "positive, rank-1" is the test.
This test is a genuine discriminator **only if** it (a) fits angles from choices in each domain
(never done same-subject, angle-to-angle) and (b) tests rank-1 — a bare nonzero correlation confirms
neither GDT nor the incumbent and does not count (carried verbatim from `prereg-coupling-v1`).

---

## 2. Task design (same subjects, both domains)

Each subject completes, in one session, three incentivized blocks (block order counterbalanced; an
attention/consistency check per block):

- **R — Risk block.** K_R binary lottery choices spanning the (expected value, dispersion) plane,
  drawn from the CPC18 / Ruggeri KT item families used in Part II so the risk encoding is identical.
  **Split into balanced gain and loss sub-blocks** (K_R/2 gain-domain, K_R/2 loss-domain) — *both*
  adequately sized, because the reflection sub-angles θ_risk-gain and θ_risk-loss are each fit
  separately and their **difference is the primary coupling variable** (the loss-aversion analog,
  §4.2). This makes the loss block first-class, not an afterthought (correcting the standing "loss is a
  side subset" habit); a gain-only angle is never pooled with loss.
- **S — Social block.** K_S allocation choices between self and one anonymous other: budget-line
  (modified-dictator) menus in the Charness–Rabin / FKM style used in Part II Move 1, spanning the
  (own payoff s, other payoff o) plane, **balanced across advantageous (s > o) and disadvantageous
  (s < o)** regions (K_S/2 each) so θ_social-adv and θ_social-dis are each estimable and their
  difference — the inequality-aversion analog — is the social half of the aversion contrast (§4.2).
- **P — Patience block (auxiliary, for the rank test).** K_P intertemporal choices (smaller-sooner vs
  larger-later) yielding a third choice-fit angle θ_time, so that P2 (rank-1) is a **non-trivial**
  ≥ 3-angle test rather than a 2-variable tautology.

Incentives: one block chosen at random for real payment (standard random-incentive design); the social
block pays both the subject and a matched recipient. Stakes and exact menus are fixed in the frozen
bundle (§9).

---

## 3. Per-person angle estimation (the choice-fit angles)

For each subject and each block, fit the **frozen** GDT choice model of Part II — the Mahalanobis cost
on the 2-D subspace, the scale-invariant tradeoff **angle**, an isotropic ridge σ ≥ 0.05, and the
**fixed-temperature information-price rule** (Part II §VI; *not* the deprecated cost-dependent rule).
Only the one-parameter magnitude is recalibrated per subject; the angle is the estimand.

- **θ_risk-gain**, **θ_risk-loss** = the aversion angle σ_EV : σ_dispersion fit *separately* on the
  gain and loss sub-blocks of R. **θ_risk** (for the rank-0 P1) = the gain angle (loss never pooled in);
  the **aversion contrast a_risk = θ_risk-gain − θ_risk-loss** is the risk half of the primary statistic.
- **θ_social,adv**, **θ_social,dis** = the other-regard angles σ_s : σ_o fit separately on the
  advantageous and disadvantageous regions of S (envy/guilt — Fehr–Schmidt β vs α). **θ_social** (rank-0)
  = the pooled other-regard angle; the **aversion contrast a_social = θ_social,adv − θ_social,dis** is
  the social half of the primary statistic.
- **θ_time** = the impatience angle from block P.

Each subject thus yields ≥ 5 choice-fit sub-angles (2 risk, 2 social, 1 time). Angles are estimated by
penalized MLE (the softmax likelihood of the fixed-temperature rule) with the ridge; per-subject
standard errors come from the likelihood curvature and from split-half refits (§4.3). The **aversion
contrasts** (a_risk, a_social) are the primary Level-B variables (§4.2); the pooled angles feed the
rank-0 secondary; all sub-angles feed the joint-factor rank test.

---

## 4. Hypotheses, statistics, and thresholds

Resampling/uncertainty unit = **subject** throughout. Family for FDR = the three confirmatory tests.

### 4.1 P1 — positive coupling (sign + magnitude)
- **Estimand:** ρ = corr(θ_risk, θ_social) across subjects, **disattenuated** for angle measurement
  error (§4.3).
- **Pass:** ρ ≥ 0.20 with the 95% CI excluding 0 and the sign positive; **and** the *raw* (attenuated)
  correlation is also positive and significant (a sign-consistency guard so the correction cannot
  manufacture the result).
- **Falsify:** ρ ≤ 0.10, or n.s., or negative. (The 0.10 boundary is carried from `prereg-coupling-v1`;
  the 0.20 pass margin reflects that a shared-metric coupling should be substantial, not merely nonzero.)

### 4.2 P2 — the coupling across the RANK LADDER (a scalar angle is a rank-0 shadow)

A single shared metric Σ is a rank-2 tensor per domain; reducing it to one tradeoff **angle** keeps
only the rotation and discards the anisotropy and the **reflection** (symmetry) structure. A shared
metric therefore need not produce a correlation of *naively pooled* angles — and if it acts through
the reflection axis (the recurring "reflection broken by aversion" motif: loss aversion in risk,
inequality aversion in social), pooling **cancels** the shared factor and the scalar test reads ≈ 0.
That is exactly the GPS "two bundles / no coupling" outcome, and it is *consistent with* a shared
metric that the scalar encoding cannot see (`datasets/coupling_encoding_probe.py`). So P2 is
pre-registered as a **ladder of ranks**, all tested; B is supported if the coupling appears at **any**
rank, and *the rank at which it appears is itself the finding*.

- **Rank 0 — scalar angle (secondary, not decisive either way).** corr(pooled θ_risk, pooled
  θ_social). A pass supports a *simple* (non-reflection) coupling. **A null here does NOT falsify B**
  (reflection masks it); it is reported, not weighted.
- **Rank "reflection" — the aversion contrast (PRIMARY).** Each domain's **symmetry-breaking
  parameter** is a *task-defined* contrast (no fitting): a_risk = θ_risk-gain − θ_risk-loss (the
  loss-aversion analog), a_social = θ_social-adv − θ_social-dis (the inequality-aversion analog).
  **Pass:** the disattenuated corr(a_risk, a_social) has 95% CI lower > 0.10, sign positive. This is
  the sharpest Level-B prediction — a shared metric couples the aversion terms even when it leaves the
  angles uncoupled — and by simulation it is by far the best-powered (§6). Sign is pre-committed
  positive (more loss-averse ⇒ more inequality-averse).
- **Rank ≥ 2 — joint low-rank tensor factor (structure test).** A cross-fitted joint low-rank factor /
  CCA over the reflection-resolved sub-angles across [subject × coordinate × domain]; **rank-1** if one
  shared subject-factor explains the cross-domain covariance (PC1 share ≥ 0.60, λ1/λ2 ≥ 3, cross-domain
  partials → |r| < 0.10 after removing it). By simulation this cross-fitted factor is concordant with
  the aversion contrast (both decisive at N ≈ 200; §6.2). The **hierarchical latent model** of §4.3 is
  the preferred estimator for full error-propagation and the rank-1-vs-2 call, but is not required for
  detection. The aversion contrast is favored as *primary* only because it needs no fitting (the
  reflection axis is task-defined), making it the simplest and most transparent of the three.
- **Falsify B:** the coupling is null (CI excludes 0.10) at **every** rank — scalar **and** aversion
  contrast **and** joint factor. Only then is the shared-metric claim false at the individual level;
  this would replicate the GPS falsification at the gold standard, now with the reflection encoding
  given every chance.
- **Tier-B (rank-2 not rank-1):** the joint factor is low-rank at rank 2 but not rank 1 → broader
  low-rank coupling, distinctive rank-1 claim fails; reported as Tier B.

### 4.3 Measurement-error correction (pre-committed method)
Two independent estimators, both reported; the **hierarchical** one is the headline:
1. **Disattenuation:** split each block in half, fit angles on each half, compute the split-half
   reliability r_xx per angle; corrected ρ = ρ_obs / √(r_risk · r_social). Report ρ_obs and ρ_corr.
2. **Hierarchical / errors-in-variables model:** a Bayesian (or SEM) model with per-subject latent true
   angles, block-level likelihoods supplying the measurement error, and a subject-level covariance of
   the latent angles — the cross-domain correlation is read from the **latent** covariance, which is
   error-free by construction. Priors and sampler settings fixed in the bundle.
P1/P2 thresholds are evaluated on the corrected/latent quantity; the raw is the sign-consistency guard.

### 4.4 P3 — encoding-invariance
Re-encode the social coordinate o → g(o) for a pre-registered monotone increasing g (e.g. √o and
log(1+o)), re-fit θ_social, recompute ρ. **Pass:** sign(ρ) unchanged for every g. **Falsify:** any
monotone g flips the sign. (Theorem 2, dominance case, is the theoretical expectation.)

### 4.5 Incumbent contrast (report, not gated)
Fit CPT to block R and Fehr–Schmidt (α, β) to block S **independently** per subject; the incumbent
implies corr(θ_risk, θ_social) has no shared-parameter source (predicted 0). Report the GDT
shared-metric coupling against this 0 benchmark, and a likelihood/BIC comparison of the joint
shared-Σ model vs. the independent CPT+FS pair on held-out choices (§5).

### 4.6 Null-coupling control (the result is meaningless without it)
Adopting `the-angular-observer`'s discipline — *the control must fail (≈ 0) for the claim to mean
anything* (`crosssubstrate.py`'s random-mode ρ) — pre-register two null channels that GDT predicts to
be ≈ 0 and that must be so:
  1. **Subject-permutation null.** Recompute ρ after permuting subject identity between the two blocks
     (breaking the same-subject link). Pre-committed ≈ 0; a nonzero permuted ρ indicates a pipeline
     leak and voids P1.
  2. **Magnitude channel.** Compute the same across-subject correlation on the *magnitudes* (the
     recalibration constants) rather than the angles. Keep-the-Angle predicts the geometry-free radial
     coordinate carries little cross-domain structure, so this should be markedly weaker than the angle
     coupling; if the magnitude channel matches or exceeds the angle channel, the "coupling lives in the
     angle" claim is not supported and is reported as such.

### 4.7 Reused tooling (pinned in the frozen bundle)
The per-subject and coupling confidence intervals reuse `the-angular-observer/stats.py::boot_ci`
(paired bootstrap), and the null-control design mirrors `crosssubstrate.py::observer_rhos`
(claim + random control + baseline, reported together). Pin both by commit hash in the bundle so the
statistics are identical to the angular-observer results they are borrowed from.

---

## 5. Held-out discipline
Fit angles on a random 70% of each subject's within-block choices; evaluate the shared-Σ vs
independent-models comparison (§4.5) on the held-out 30% (per-subject, fixed seeds in the bundle). The
coupling correlation (P1/P2) uses full-data angle estimates (it is a between-subject statistic), but
the model comparison that adjudicates "shared metric vs two separate models" is out-of-sample.

---

## 6. Power (simulation, `datasets/coupling_power_sim.py`)
Simulation of the full §3–§4 pipeline — draw correlated latent angles, generate choices under the
fixed-temperature model, **refit** each angle by grid-MLE (so estimates carry realistic noise),
disattenuate via split-half reliability, and test H0: ρ ≤ 0.10 by a subject bootstrap CI (pass = CI
lower > 0.10 **and** raw sign positive). Implied per-choice accuracy ≈ 0.79 (realistic); the
disattenuated estimator recovers the true ρ across all cells (validation). Power to reject ρ ≤ 0.10,
200 reps:

| true ρ | design for ≥ 80% power | reliability at that K | notes |
|--------|------------------------|-----------------------|-------|
| **0.30** (moderate) | **N = 400 × K = 32** (power 0.82; K=48 → 0.89) | 0.66 (K=32), 0.76 (K=48) | the primary design |
| 0.25 (modest) | N ≈ 800 × K = 48 (0.91) | 0.76 | |
| 0.20 (at the pass threshold) | N ≈ 1600 × K = 48 (0.87); N=1200 → 0.78 | 0.76 | expensive; the boundary is hard by construction |

**Frozen primary design: N = 400 subjects × K_R = K_S = 32 × K_P = 16.** Powered (≥ 0.80) to confirm a
**moderate** coupling (true ρ ≥ 0.30) against the ρ ≤ 0.10 null; per-block angle reliability 0.66 > 0.5.
K ≥ 24 is required for reliability ≥ 0.5 (K=16 → 0.46 fails), so K=32 carries margin.

**Honest power boundary (pre-committed).** Because the pass threshold (0.20) sits only 0.10 above the
null (0.10) and measurement error attenuates the estimate, a *marginal* true coupling (ρ ≈ 0.15–0.20)
is **not** resolvable at feasible N with this statistic (needs N ≈ 1600). Therefore:
  - N = 400 is a decisive test of a **substantial** shared-metric coupling (ρ ≥ 0.30) — the magnitude a
    genuine one-Σ claim implies. A clear pass confirms; a clear fail (r_corr ≤ 0.10, CI excludes 0.20)
    falsifies.
  - An **intermediate** outcome (r_corr in ≈ 0.10–0.20, CI spanning both bounds) is a pre-registered
    **INCONCLUSIVE** zone at N = 400 — reported as such, never spun as confirmation.
  - **Sequential option (pre-registered stopping rule).** Run stage 1 at N = 400; if the stage-1
    r_corr is suggestive but inconclusive (point estimate ≥ 0.15, CI includes 0.10), extend to
    N = 1600 (stage 2) under a pre-committed alpha-spending rule fixed in the bundle. This spends the
    large sample only when the moderate sample warrants it.
The `coupling_power_sim.py` script + this table are pinned in the freeze bundle; re-run to reproduce.

### 6.2 Power for the rank-ladder / aversion-contrast primary (`coupling_tensor_sim.py`, `coupling_encoding_probe.py`)
The scalar table above is the **rank-0** test. The **primary P2 statistic (§4.2, the aversion
contrast)** is far cheaper because the reflection *difference* amplifies the shared factor (2×) while
pooling cancels it. Simulating a reflection-structured shared metric (one latent factor loading
oppositely across each domain's reflection axis) and the task-defined contrast test:

| statistic | power at N=200 × K=32 | false-positive (no coupling) | r recovered |
|-----------|:---------------------:|:----------------------------:|:-----------:|
| rank-0 scalar angle correlation | ≈ 0.00 (structurally blind under reflection) | 0.00 | +0.01 |
| **aversion contrast** (θ_gain−θ_loss ↔ θ_adv−θ_dis; axis task-defined, no fitting) | **1.00** | **0.000** | **+0.56** |
| joint CCA / factor over the reflection sub-angles (cross-fitted) | **1.00** | **0.000** | **+0.56** |

Under the reflection hypothesis **both** above-rank-0 tests are decisive at **N ≈ 200** (r ≈ 0.56,
FP ≈ 0), while the scalar angle sees nothing — the coupling lives in the reflection/aversion structure
the scalar discards. The frozen **N = 400** design is already *over*-powered for the coupling and stays
sized by the rank-0 scalar test (its only binding constraint). The **aversion contrast is the primary
confirmatory statistic** because it needs no fitting (the reflection axis is task-defined, so it is
stable and simplest); the cross-fitted joint factor is a concordant secondary, and the **hierarchical
latent model (§4.3)** remains the preferred estimator for full error-propagation and the rank-1-vs-2
structure test — but it is *not required for detection*. **Honest scope:** this power is *conditional on
B being reflection-structured* — it establishes the *instrument* is right and cheap **if** B lives in
the aversion terms, not that B exists. (An earlier version reported the plug-in factor as
"estimator-unstable, flat in N"; that was a data-shaping bug — corrected — not a real limit.)
`coupling_encoding_probe.py`/`coupling_tensor_sim.py` + this table are pinned in the bundle.

---

## 7. Data sources (in preference order)
1. **Bespoke online session** (Prolific/CloudResearch): the three blocks above, one session,
   random-incentive payment. The cheapest way to get *exactly* the same-subject choice data GPS lacks.
   Estimated cost is fixed in the bundle with the power-selected N.
2. **Existing same-subject choice data**, if a cohort ran both a lottery task and an allocation task
   with enough items to fit angles — verify at execution:
   - **Bruhin–Fehr–Schunk (2019)** individual social-preference choices (JEEA replication package) — if
     the same subjects have a companion risk task with adequate items.
   - Any lab dataset pairing a Holt–Laury / KT lottery block with a modified-dictator block per subject.
   These are checked first; a bespoke run is commissioned only if none supplies both blocks at the
   required item counts (that check, and its outcome, are logged, not skipped).

---

## 8. Decision rules (pre-committed)
The coupling is tested across the rank ladder (§4.2); B is supported if it appears at **any** rank, and
the rank is the finding. "Coupling detected at rank X" = that rank's CI lower > 0.10, sign positive.

| outcome | registered interpretation |
|---|---|
| coupling detected at the **aversion-contrast** rank **and** joint factor is **rank-1** **and** P3 holds | **GDT coupling confirmed at the gold standard** — the shared metric couples the domains through the reflection/aversion structure. The Tier-A result the program is built on; the *reflection* rank is itself the discovery (why GPS saw "two bundles"). |
| coupling at the aversion rank, joint factor **rank-2** not rank-1 | broader low-rank coupling; distinctive rank-1 claim fails → **Tier B**, reported as such |
| coupling **only** at the rank-0 scalar angle (aversion rank null) | a *simple* (non-reflection) coupling — supports B but not the reflection structure; reported at that rank |
| coupling at aversion rank but **P3 fail** | the coupling is a coding artifact; void |
| **inconclusive** (aversion-contrast CI spans 0.10 at N=400, point est ≥ 0.15) | **INCONCLUSIVE** — trigger the sequential N=1600 extension (§6) under the pre-committed alpha-spending rule; else report inconclusive |
| **null at EVERY rank** (scalar, aversion contrast, and joint factor all CI-exclude 0.10) | the shared-metric claim is **false at the individual choice level**, with the reflection encoding given every chance — the strongest falsification; graveyard, next to the GPS-proxy result |

No threshold, sign, or rank definition may change after the §9 freeze; a wrong sign is a reported
failure. A null at the rank-0 scalar **alone** never falsifies B (§4.2) — only a null at every rank does.

---

## 9. Freeze procedure (to execute, not yet executed)
1. Finalize: the exact R/S/P menus, stakes, encoder for angles (the frozen Part II fitter, pinned by
   commit), the error-correction priors/sampler, the fold seeds, the power analysis (§6) with the
   selected (N, K_R, K_S, K_P), and the sign-prediction table (all positive; loss-domain excluded).
2. Assemble the bundle: this protocol (final), the stimulus files, the analysis code (angle fitter +
   P1/P2/P3 + error model), fold seeds, power results.
3. `sha256` the bundle → `prereg-coupling-angle-v1.sha256`; **signed git tag** `prereg-coupling-angle-v1`
   and **OSF registration** (public, timestamped) *before* any data collection.
4. Only then recruit/collect (or pull the existing dataset) and score.

---

## 10. Reporting
Reported regardless of outcome, in the `prereg-sigma-v1` scorecard format, next to the GPS-proxy result
so the two levels (proxy vs gold-standard) sit side by side. The graveyard convention applies: if the
coupling fails here too, the cross-domain-coupling claim is retired and the surviving pillars (low-rank
Σ, projection-gap — both within-domain) stand on their own, stated plainly.
```
