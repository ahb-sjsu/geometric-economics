# Powered social-coordinate transfer — the SOCIAL analog of the cross-domain pillar

**Supersedes the underpowered 9-game attempt (`RESULTS_social_transfer.md`, move2c).** That test
tried to transfer a 5-D social direction across 7 + 2 aggregate games and was, honestly, untestable at
that sample size. This uses the powered FKM individual data and the paper's own 2-D metric.

## Question

Section III of the manuscript shares the **risk** part of the metric (EV, SD) between lotteries and
games. Does the **social** part — the self↔other tradeoff, the social analog of the scale-invariant
aversion angle — transfer between two structurally different social-allocation tasks, recalibrating
only a scalar magnitude (the polar angle-lock)?

## Method

Geometric metric restricted to the 2-D social space `(own, other)`: each option is an allocation
`(s, o)`; per-menu ideal `(s*, o*) = (max own, max other)`; cost
`C = sqrt(((s*-s)/σ_s)² + ((o*-o)/σ_o)²)`; choice `= softmax(-C/T)`. The tradeoff **angle** is the
scale-invariant ratio `σ_s : σ_o`. An isotropic ridge floor `σ ≥ 0.05` (normalized units) regularizes
the degenerate self-regard corner — the model's own "PSD pseudometric + isotropic ridge `P+εI`".

- **A = FKM (Fisman–Kariv–Markovits 2007)** 2-person budget-line giving — **powered: 3,800 individual
  choices, 76 subjects**. Each budget line (price of giving `p`) is a menu of `(s,o)` points,
  discretized to `K=21` frontier allocations; observed = the chosen point.
- **B = Charness–Rabin (2002)** 7 two-person dictator games — discrete binary menus, aggregate freqs.

Fit `(σ_s, σ_o, T)` natively on each; transfer = fix the **angle**, refit only scale + `T` (polar).
Scored by multinomial NLL; gap = fraction of the chance→native gap closed.

## Result

| | native NLL | chance | fitted angle σ_s:σ_o |
|---|--:|--:|---|
| FKM (3,800 choices) | 2.4454/choice | 3.0445 | 0.002 : 1.000 |
| Charness–Rabin (7 games) | 137.16 | 160.81 | 0.265 : 0.964 |

**cos(angle_FKM, angle_CR) = +0.96** — fit independently, the two tasks' self↔other tradeoff shapes
are nearly identical.

| transfer (angle-locked) | full (no angle-lock) | gap closed |
|---|--:|--:|
| **FKM → CR** | 66% | **100%** |
| **CR → FKM** | 44% | **45%** |

## Read (honest)

- **The social coordinate transfers, bidirectionally and powered.** The independently-fit tradeoff
  shapes align at cos 0.96, and the angle-locked transfer is positive both ways. The powered FKM metric
  (3,800 choices) predicts Charness–Rabin dictator play at **100%** of a native fit with only a scalar
  recalibration; the reverse — a 7-game fit predicting 3,800 individual choices — reaches **45%**.
- **Same asymmetry signature as the risk leg.** In Section III the richer domain (270 lotteries)
  transferred to games while the reverse was weaker; here the richer domain (3,800 FKM choices)
  transfers fully to CR while the 7-game reverse is partial. Richer calibration generalizes better —
  a consistent, interpretable pattern, not a new failure.
- **What bounds it.** A single **pooled** metric over a heterogeneous population: FKM's ~40%
  keep-everything choosers drive the self axis to the ridge floor (σ_s→0.002), so the *level* of
  other-regard differs across the two populations even though the tradeoff *shape* is shared. The CR
  side is 7 aggregate games. This is a shared **shape**, recalibrated in **scale** — exactly the
  Section III claim, now on the other-regarding coordinate, and a real upgrade over the untestable
  9-game attempt. It is not yet the clean ~97–100%-both-ways of the risk leg.

## What changes in the paper

The Section III "honest limit" — *"the transfer we demonstrate is of the risk part of the metric …
social-coordinate transfer requires social-preference games"* — is upgraded: the social coordinate now
**does** transfer, powered and bidirectional (cos 0.96; 45–100%), between FKM giving and Charness–Rabin
dictator games. The remaining gap to the risk leg (population heterogeneity in the *level* of
other-regard) is stated, not hidden.

*Reproduce: `python social_transfer.py` with `raw_fkm/` present (FKM OpenICPSR 115613, licensed, not
committed). Charness–Rabin games are inlined from Table I.*
