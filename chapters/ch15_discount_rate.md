# Chapter 15: The Discount Rate as Geodesic Curvature

> *"We do not inherit the earth from our ancestors; we borrow it from our children."*
> — often attributed to Indigenous proverb

*Part V: Applications*

---

> **RUNNING EXAMPLE — MARIA'S COFFEE SHOP**
>
> *Maria Esperanza is deciding whether to invest $30,000 in solar panels for her coffee shop. The payback period is 8 years. At a 3% discount rate (her personal rate), the investment has positive net present value. At a 12% discount rate (her landlord's REIT rate), it does not. The same investment, evaluated by two agents, produces opposite decisions — not because they disagree about the facts, but because they experience different curvature on the temporal manifold.*
>
> *The discount rate is not a preference parameter. It is the curvature of the agent's decision manifold along the time axis — and the Stern-Nordhaus debate about climate change is, at bottom, a disagreement about this curvature.*

---

## 15.1 Discounting as Temporal Curvature

**[Modeling Axiom.]** Classical economics models the discount rate $\delta$ as a preference parameter: future utility is worth $e^{-\delta t}$ times present utility. This is exponential discounting — the unique form consistent with time-consistency (if you prefer A today to B tomorrow, you'll still prefer A today to B tomorrow when asked a week in advance).

But human discounting is not exponential. It is *hyperbolic*: $R/(1 + kt)$ rather than $R \cdot e^{-\delta t}$. This produces preference reversals (present bias) and has been documented across cultures, species, and decision domains.

**Proposition 15.1 (Hyperbolic Discounting as Temporal Curvature).** Expanding on the result first stated in Chapter 4 (Proposition 38), *hyperbolic discounting arises because the decision manifold's curvature is non-constant along the temporal dimension. Near the present ($t \to 0$), the manifold is sharply curved — short-term consequences loom large in all dimensions. At distant horizons ($t \to \infty$), the manifold flattens — distant consequences affect fewer dimensions. The overall discount function is the integral of curvature along the temporal axis, which yields a hyperbolic rather than exponential form.*

**[Empirical.]** The geometric explanation: present-bias is stronger for visceral goods (food, sex, drugs) than for abstract goods (money, career). Visceral goods activate more dimensions of the manifold at short horizons ($d_6$ social, $d_7$ identity, $d_4$ autonomy are all engaged by immediate visceral choice), while abstract goods primarily affect $d_1$ (consequences) at all horizons. Higher-dimensional activation at short horizons = steeper curvature near $t = 0$ = more hyperbolic discounting.

## 15.2 The Stern-Nordhaus Debate

The most consequential disagreement about discount rates is in climate economics. Nicholas Stern (2006) used a near-zero social discount rate ($\delta \approx 0.1\%$) and concluded that immediate, aggressive climate action is economically justified. William Nordhaus (2008) used a market-calibrated rate ($\delta \approx 3\%$) and concluded that gradual action is optimal.

**[Modeling Axiom.]** In the geometric framework, this is not a disagreement about preferences. It is a disagreement about the *curvature of the intergenerational manifold*.

Stern's manifold is nearly flat along the temporal axis: future people's welfare counts almost as much as present people's. The geodesic on this manifold avoids catastrophic climate trajectories even at high present cost, because the distant future is "close" on Stern's metric.

Nordhaus's manifold has positive curvature along the temporal axis: distant future welfare is geometrically farther away than present welfare. The geodesic on this manifold accepts some climate risk in exchange for faster present growth, because the distant future is "far" on Nordhaus's metric.

The geometric framework does not resolve the disagreement. But it makes the disagreement *precise*: Stern and Nordhaus are not arguing about whether to discount. They are arguing about the curvature tensor $R_{t i t j}$ along the temporal dimension of the social decision manifold. This is an empirical question — measurable, in principle, from revealed intergenerational preferences — not a philosophical one.

## 15.3 Intergenerational Equity as Parallel Transport

**[Speculation/Extension.]** When we ask "what do we owe future generations?", we are asking a parallel-transport question. An obligation formulated in the present — "preserve a livable climate" — must be transported along the temporal geodesic to the future. But the manifold has curvature, and parallel transport on a curved manifold introduces holonomy: the obligation may arrive "rotated" — its content may have shifted through the transport.

What climate preservation *means* in 2026 (reduce CO₂ emissions) may differ from what it means in 2100 (maintain a specific temperature band, preserve specific ecosystems, support specific population levels). The holonomy of temporal parallel transport is the drift in obligation-content over time — and the discount rate is, in this framework, the rate at which the obligation's magnitude attenuates during transport.

A zero discount rate says: obligations transport without attenuation (the manifold is flat). A positive discount rate says: obligations attenuate proportionally to the curvature they traverse. The question is not which rate is "correct" but what the actual temporal curvature of the social manifold is — a question that, in principle, admits empirical investigation.

---

## Worked Example: Maria's Solar Panel Decision

Maria evaluates the solar panel investment on two manifolds.

**Nordhaus manifold ($\delta = 3\%$, high temporal curvature):**

| Year | Cash flow | PV factor | PV |
|------|-----------|-----------|-----|
| 0 | -$30,000 | 1.00 | -$30,000 |
| 1-8 | +$4,500/yr | $\sum e^{-0.03t}$ | +$31,200 |
| NPV | | | **+$1,200** |

Positive but marginal. The investment barely clears the hurdle.

**Full-manifold analysis (including evaluative dimensions):**

Beyond $d_1$, the solar investment generates:
- $d_6$ (social impact): reduces neighborhood carbon footprint, signals environmental commitment (+0.3/yr for 25 years)
- $d_7$ (identity): aligns with Maria's values as ethical business owner (+0.5/yr)
- $d_8$ (legitimacy): anticipates likely future carbon regulations (+0.2/yr)
- $d_9$ (epistemic): reduces uncertainty about future energy costs (+0.4)

The Mahalanobis distance on the full manifold heavily favors the solar investment because the evaluative dimensions accumulate over the panel's 25-year lifetime. The investment that is marginal on $d_1$ is strongly positive on the full manifold.

**The geometric insight**: Maria's "irrational" enthusiasm for solar panels (she installed them despite the marginal financial case) is rational on the correct manifold. Her implicit discount rate on the evaluative dimensions is lower than her financial discount rate — not because she's inconsistent, but because the temporal curvature on evaluative dimensions is lower than on monetary dimensions. Community value, identity, and legitimacy persist with less attenuation than dollars.

---

## Technical Appendix

**Definition 15.1 (Temporal Curvature).** The *temporal curvature* of the economic decision manifold at time $t$ is the sectional curvature $K(t, d_k)$ in the plane spanned by the temporal direction and dimension $d_k$. The discount function for dimension $d_k$ is:

$$D_k(t) = \exp\left(-\int_0^t K(\tau, d_k) \, d\tau\right)$$

When $K$ is constant, this yields exponential discounting. When $K$ decreases with $t$ (the manifold flattens at long horizons), this yields hyperbolic discounting.

**Proposition 15.2 (Dimension-Dependent Discounting).** **[Conditional Theorem.]** If temporal curvature varies across dimensions — $K(t, d_1) \neq K(t, d_6)$ — then the discount rate is dimension-dependent. Monetary value ($d_1$) may be discounted at 3% while community value ($d_6$) is discounted at 0.5%. The standard approach of applying a single discount rate to all dimensions is a scalar contraction that violates the Scalar Irrecoverability Theorem.

---

## References

Nordhaus, W. D. (2008). *A Question of Balance.* Yale University Press.
Stern, N. (2006). *The Economics of Climate Change: The Stern Review.* Cambridge University Press.
Laibson, D. (1997). "Golden Eggs and Hyperbolic Discounting." *Quarterly Journal of Economics*, 112(2), 443–478.
