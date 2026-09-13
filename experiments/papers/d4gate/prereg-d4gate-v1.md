# prereg-d4gate-v1 — Is the Fourfold Chirality Absent in the Interior, or Gated?

**Status:** v1, FROZEN 2026-09-13 (Section 9 steps 1 and 2 executed; the signed
tag is step 3 and OSF registration is the owner's step, its GUID recorded in
`prereg-d4gate-v1.sha256` and not here, so this file's hash stays fixed). No fit
has been run on the outcome column.

**Companion to:** `experiments/datasets/RESULTS_d4_rotation.md` (the test this
one follows), `experiments/datasets/D4_REHABILITATION.md` (the reading this one
tests), `stratification-thesis.md`, and the registrations `prereg-v1`,
`prereg-v2`, `prereg-sigma-v1`, `prereg-coupling-v1`, `prereg-dimensions-v1`,
`prereg-boundary-v1`.

**Author:** Andrew H. Bond, San José State University.

> **What has been done before this draft.** The CPC18 stimulus columns and the
> per-game subject counts were read, to build the design matrix, to cross-tabulate
> the gate against the domain coordinate, and to run the power simulation of
> Section 7. The choice column `B` and the rate `brate` derived from it have not
> been read, and no model has been fitted to them. The pooled coefficients of the
> earlier test, quoted in Section 3, are a published result of that test and are
> treated here as prior knowledge.

---

## 1. The question

`RESULTS_d4_rotation.md` reported the rotation-covariant chirality `d·q` at
**+0.003** in the interior against the rotation-breaking `d²−q²` at **+0.340**,
and concluded that the fourfold pattern is a corner phenomenon and not a
continuous rotation. `D4_REHABILITATION.md` observes that the D₄ account of
`sqnd-probe` never claimed a continuous rotation, claims a *gated* one, and
reports a generator asymmetry in the moral domain, exact reflection and gated
rotation, that matches the shape of the risk-domain result.

Two readings of the interior estimate are then available and they differ.

- **Absent.** There is no rotation in the interior. The chirality is zero
  everywhere in it, and zero in every subset of it.
- **Gated.** The chirality is present where a gate fires and absent where it does
  not. The pooled estimate near zero is the mixture, which is the attenuation the
  original record already names as a caveat.

This registration tests the second against the first.

## 2. The gate, declared

A choice set is **CERTAIN** when at least one of its two options has zero
standard deviation, that is when a sure outcome is on the menu. Otherwise it is
**UNCERTAIN**.

The gate is fixed by the stimulus and requires no fitting, which is the property
that makes it admissible. It is chosen before any refit and for a stated reason.
The gates of the D₄ account are discrete triggers, and the certainty effect is
the classic discrete trigger of risky choice and is already the `σ_p` reflection
of the confirmed V₄ structure.

**One gate is registered.** The adversarial split that the original record's own
caveat names, Kahneman and Tversky problems against normal CPC18, is recorded
here as a *named alternative that is not being run*. It is not a second attempt
and no result from it may be reported under this registration.

## 3. Data and analysis set

CPC18, `experiments/datasets/raw/cpc18_raw.csv`, sha256
`cb0dab5ca34adebc49f2dfe57f98096ab74468dea5a12a4558ce5c50ef07952d`, the
description regime only, `Trial == 1`, aggregated to one row per `GameID`. The
target is the per-game choice rate over a median of 120 subjects.

The Kahneman and Tversky corners are **excluded**. Prediction G is a claim about
the interior and Part A of the earlier test already covers the corners.

Coordinates are those of `d4_rotation.py` and are not changed. The domain
coordinate `d` is `+1` for a pure-loss option, `−1` for a pure gain, and `0` for
a mixed gamble. The probability coordinate is `q = 2p − 1`.

Published pooled coefficients of the earlier test, used only to generate
synthetic outcomes in the power simulation: const `−0.265`, `d²+q²` `−0.058`,
`d·q` `+0.003`, `d` `−0.194`, `q` `+0.144`, `d²−q²` `+0.340`.

## 4. The model, and why the cells are not fitted separately

One fit over all interior rows, with only the chirality allowed to differ by gate:

```
kappa(d,q) = c0 + c1 (d²+q²) + c2 (d·q) + c3 d + c4 q + c5 (d²−q²)
                + gamma · 1[certain] · (d·q)
```

so `c2` is the chirality where the gate does not fire, `gamma` the increment
where it does, and `c2 + gamma` the chirality where it does. The choice
likelihood is the same logistic form as the earlier test, `bEV·ΔEV + kappa·ΔSD`.

**Separate per-cell fits were considered and rejected on a covariates-only
ground, before any outcome was read.** The chirality is an interaction requiring
both signs of `d`. The cross-tabulation of the gate against `d` is

| | `d = −1` gain | `d = 0` mixed | `d = +1` loss |
|---|---|---|---|
| CERTAIN | 73 | 80 | 16 |
| UNCERTAIN | 40 | 57 | **4** |

Four pure-loss rows do not identify a chirality, so a two-cell design is not
estimable here and is not registered. The interaction design uses all twenty
pure-loss rows and estimates the gating as one coefficient.

## 5. Predictions

Bars are the 95th percentiles of the null distribution in Section 7 and are fixed
before the fit. They live in `analysis/d4gate_grade.py`, which was written before
the fit was run and holds them and nothing else holds them.

- **G1, gating.** `|gamma| ≥ T_gamma`.
- **G2, presence where gated.** `|c2 + gamma| ≥ T_presence`.

Both are reported separately. **No composite verdict is registered.**

## 6. Falsifiers

- **F1.** `|gamma| < T_gamma` **and** `|c2 + gamma| < T_presence` together mean
  the chirality is not recovered anywhere under the declared gate. The gated
  reading fails, the rotation is absent in the interior, and the verdict of
  `RESULTS_d4_rotation.md` stands as written.
- **F2.** If the fit does not converge from both starts to within `1e-6` in the
  objective, the run is void and is reported as void rather than retried with
  different starts.
- **F3, stated against ourselves.** A pass on G1 with a failure on G2 means the
  cells differ but no chirality is present in either. That is not evidence for a
  gated rotation and must not be reported as one.

## 7. Power and size

`power/power_d4gate.py`, covariates and subject counts only, outcomes never read.
Null is `c2 = 0` and `gamma = 0`. The alternative is `c2 = 0`, `gamma = x`.
Synthetic targets are drawn as rates at the true per-game subject counts, because
the fitted target is a rate over a median of 120 subjects and drawing a single
choice per game would overstate the noise by about an order of magnitude. An
earlier version of this simulation made exactly that error and is recorded in
Section 10.

Run with 400 replicates at seed 20260912. The interior holds 270 rows, 169
certain and 101 uncertain, with a nonzero chirality regressor on 81 certain and
36 uncertain rows, and a median of 120 subjects per game.

**Bars, at a size of 0.05 under the null.**

| Bar | Value |
|---|---|
| `T_gamma`, 95th percentile of `|gamma|` | **0.2778192266034961** |
| `T_presence`, 95th percentile of `|c2 + gamma|` | **0.18095219285614153** |

**Power, reported and not used as a bar.**

| True gated chirality | G1 gating | G2 presence |
|---|---|---|
| 0.10 | 0.045 | 0.075 |
| 0.25 | 0.293 | 0.603 |
| 0.50 | 0.953 | 1.000 |
| 1.00 | 1.000 | 1.000 |

**Stated plainly.** This design detects a gated chirality of 0.5 or larger and
does not detect one of 0.1. At 0.25 it is better than even on presence and worse
than even on gating. A failure of either prediction is therefore evidence of
absence only for effects at 0.5 and above, and below 0.25 a failure says the
design was too small and nothing else. That sentence belongs in any report of
this registration whichever way it falls.

## 8. What a pass would and would not license

A pass on G1 and G2 licenses the claim that the interior chirality is gated by
the presence of a sure outcome, on this corpus, under this coordinate. It does
not license exact D₄, which Part A of the earlier test already refuted at the
corners at `χ² = 75.4`. It does not license a continuous rotation, which nothing
here tests. The most it supports is a gated rotation over exact reflections.

A pass is also a single-corpus result. The original record's own recommendation,
that a stimulus set designed to sit at intermediate domain and probability angles
would settle the interior test cleanly, is unaffected by any outcome here.

## 9. Freezing procedure

1. Complete Section 7 from the simulation output and write the bars into
   `analysis/d4gate_grade.py`.
2. `sha256` of `prereg-d4gate-v1.md`, `analysis/d4gate_grade.py` and
   `power/power_d4gate.py` into `prereg-d4gate-v1.sha256`, in the
   `prereg-boundary-v1.sha256` JSON form.
3. Commit, sign the tag `prereg-d4gate-v1`, push. OSF registration is the owner's
   step and its URL is recorded in the `.sha256` file, which is not edited again.
4. Only then run any fit on the outcome column.

## 10. Errors made before freezing, recorded

The first power simulation drew one Bernoulli per game rather than a rate at the
per-game subject count, overstating the noise by roughly an order of magnitude.
Its bars were meaningless, at `T = 3.15` against coefficients of order `0.1`, and
its apparent power of `0.06` to `0.10` at every alternative was an artifact. It
was corrected before any bar was adopted and no threshold from it is used.

The first design fitted the two gate cells separately. The cross-tabulation in
Section 4 shows why that is not estimable. The design was changed before any
outcome was read.
