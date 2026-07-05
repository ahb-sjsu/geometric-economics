# Rational-inattention temperature model — rigorous test vs the alternatives

The program's recurring nemesis is the temperature/magnitude architecture. Three temperature laws,
each mapping a temperature-free cost-gap `g = c_B − c_A` to `P(A) = σ(g/T)`, fit to the projection-gap
panel (16,688 choices, 26 contrast×pole cells) by binomial NLL:

| model | #p | NLL | BIC |
|---|--:|--:|--:|
| fixed-T | 1 | 11511.2 | 23032.1 |
| **cost-dependent (original)** | 3 | 11563.7 | **23156.5** (worst) |
| **rational inattention** (λ + prior) | 2 | 11497.7 | **23014.9** (best) |

## 1. The dose falsifier — decisively confirmed against cost-dependent T

The original `T(Δ)=max(0.5, 0.24·Δ^2.13)` was designed to predict a *peaked* dose curve. The data is
monotone. Predicted dose gaps vs the four increasing dose levels:

| level | g_hi | obs gap | fixed-T | cost-dep | RI |
|---|--:|--:|--:|--:|--:|
| D9.1 | 0.53 | −0.020 | +0.007 | +0.048 | +0.006 |
| D9.2 | 1.40 | +0.034 | +0.018 | **+0.000** | +0.016 |
| D9.3 | 2.63 | +0.093 | +0.034 | **+0.000** | +0.030 |
| D9.4 | 5.26 | +0.134 | +0.067 | **+0.000** | +0.060 |

Spearman(predicted gap, dose level): **observed +1.00, fixed-T +1.00, RI +1.00, cost-dependent −0.95**.
The cost-dependent T predicts the effect **washes out** (peak at level 1, → 0.000 after) — the exact
opposite of the monotone rise. **The cost-dependent temperature is rejected** (wrong dose shape +
worst BIC by ~140). A **fixed information price** (RI / fixed-T) predicts the correct monotone curve.

## 2. Magnitude — direction explained, calibration residual remains

The fitted information price is **high (λ = 21.75)** → compressed gaps. This explains the *direction*
of the original falsifier: the frozen model's small T over-predicted magnitudes; the data wants a
**high info price** (capacity-limited → choices anchored near the prior → small gaps), exactly the
rational-inattention account. But a *single* λ **under-predicts the real contrasts ~4×** (|pred|/|obs|
= 0.25) while fitting the dose — so one info price does not calibrate all contrast types. The real
contrasts (d6 social, d7 identity) carry more signal per unit cost-gap than the model assigns: a
**coordinate-calibration** residual (the σ_k scaling), not a temperature problem.

## 3. What RI does NOT explain (stated plainly)

The **fourfold sign-flip** (risk weight flips with stakes) is a *utility-curvature / diminishing-
sensitivity* effect, not a temperature effect. RI is silent on it. The prior term here is also
negligible (b = +0.08, prior P(A) = 0.52) — the baseline was near-symmetric — so on this data RI ≈
fixed-T; its win over fixed-T (ΔBIC 17) is marginal. **The decisive result is the ~140-BIC rejection
of cost-dependent T in favor of a fixed information price.**

## Verdict

- **Rational inattention (fixed information price + prior) is the correct temperature architecture.**
  It wins BIC and predicts the monotone dose; the cost-dependent T that generated the original
  falsifier is rejected (dose Spearman −0.95, worst BIC).
- **λ is high** — decisions are capacity-limited, which explains why the frozen near-rational model
  over-predicted magnitudes.
- **Two of the three magnitude anomalies resolved:** the dose shape (fully) and the magnitude
  *direction* (via a high info price). **Two remain, and they are not temperature problems:** the
  coordinate-calibration residual (σ_k scaling) and the fourfold sign-flip (utility curvature).

The principled upshot: **temperature = the price of a bit, fixed, not cost-dependent.** That closes the
falsifier that has haunted the program, and it correctly localizes the *remaining* magnitude issues to
the utility/coordinate side, not the noise side.

*Reproduce: `python ri_temperature.py`.*
