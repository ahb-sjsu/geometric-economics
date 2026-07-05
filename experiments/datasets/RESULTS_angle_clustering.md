# The universal aversion-angle measurement — what clusters, what doesn't

The polar principle (shape transfers, scale recalibrates) held on every transfer axis, but we had
never *measured* the aversion angles to ask whether they are literally the same. This is that
measurement: the mean-variance preference direction from a conditional logit over the choice options,
`angle = atan2(β_SD, β_EV)`, features z-scored per domain (so the angle is comparable). Convex, stable,
handles multi-option games. Bootstrap (200×) for CIs. It **prevented an overclaim** and produced a
sharper, honest result.

## Angles by domain

| domain | angle | 95% CI | n |
|---|--:|--:|--:|
| CPC18 (gain lotteries) | −3.5° | [−7.0, 0.2] | 270 |
| choices13k (lotteries) | −0.8° | [−2.8, 1.5] | 1500 |
| bogota (strategic games) | +2.0° | [−15, 21] | 110 |
| Ruggeri gains | −174.2° | [−177, −163] | 190 |
| Ruggeri loss (raw) | +167.2° | [125, 173] | 133 |
| Ruggeri loss (reflected) | −167.2° | [−173, −152] | 133 |

## What clusters (two comparable regimes)

**Representative corpora — lotteries AND strategic games share one angle.**
CPC18, choices13k, bogota: mean −0.8°, **between-domain sd 2.2° vs within-domain bootstrap sd 4.4°
→ ratio 0.51**. The between-domain spread is *half* the sampling noise: the three domains are
statistically indistinguishable in aversion angle. **Risky choice and strategic choice share the same
mean-variance direction** — a genuine cross-domain angle agreement, not just "shape transfers."

**KT/Ruggeri — reflection unifies gains and losses at one angle.**
Ruggeri gains and *reflected* losses: mean −170.7°, **between-sd 3.5° vs within 5.9° → ratio 0.59**.
Again indistinguishable: the reflected loss domain sits at the gain angle.

## Reflection is a clean angle sign-flip

gains **−174.2°** | loss RAW **+167.2°** (the mirror) | loss REFLECTED **−167.2°** — the reflected
loss rejoins gains **within 7°**. The reflection effect, at the level of the aversion angle, is
literally a sign-flip across the value axis. This confirms `polar_reflection.py` at the angle level.

## What does NOT cluster — and why (the confound the measurement caught)

Representative corpora sit near **−1°** (β_EV > 0: people follow EV, small risk term); KT/Ruggeri sit
near **−171°** (β_EV < 0). The KT problems are **adversarially selected to violate EV** (the certainty
effect: choose the lower-EV sure thing), which flips the sign of β_EV. So the raw mean-variance angle
is **confounded by problem selection**: it is a within-sample invariant, **not** a universal constant
across adversarial and representative problem sets.

## Verdict — the honest, publishable claim

- **Polar invariance holds *within comparable problem samples*, across domains:** lotteries and
  strategic games share one aversion angle (ratio 0.51); gains and reflected-losses share one (0.59).
- **Reflection is an angle sign-flip** (reflected loss rejoins gains within 7°).
- **There is NO single universal angle across *all* domains** — the raw angle depends on problem
  selection (EV-following vs EV-violating sets). Claiming a universal constant would have been wrong;
  the measurement caught it.

So the paper-worthy statement is a **conditional invariance**: *given a comparable problem sample, the
aversion angle is shared across risk and strategic domains, and the loss domain is its mirror.* That is
strong and true. "One universal aversion constant for all of decision-making" is **not** supported —
and saying so is the difference between a real finding and an overclaim.

*Reproduce: `python angle_clustering.py`.*
