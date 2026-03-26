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

### Dimension-Dependent Discounting

A critical prediction of the geometric framework is that different dimensions should be discounted at different rates, because the temporal curvature varies across dimensions.

**Proposition 15.2 (Dimension-Dependent Discounting — Extended).** *The discount rate on dimension $d_k$ is:*

$$\delta_k = K(t, d_k)$$

*where $K(t, d_k)$ is the sectional curvature of the temporal-$d_k$ plane. If $K(t, d_1) > K(t, d_6)$ — if the temporal manifold curves more steeply on the monetary axis than on the social-impact axis — then monetary value is discounted faster than social value.*

**[Empirical.]** This prediction is testable. Ask subjects: "Would you rather receive $100 today or $110 in a year?" (monetary discounting on $d_1$). Then ask: "Would you rather your neighborhood park be clean today or slightly cleaner in a year?" (social-impact discounting on $d_6$). The monetary discount rate is typically 5–15% (subjects require $105–$115 in a year to match $100 today). The social-impact discount rate is much lower — subjects treat future community benefits as nearly as valuable as present ones.

The standard approach of applying a single discount rate to all dimensions — computing the net present value of a policy by discounting monetary costs, environmental benefits, health impacts, and community effects at the same rate — is a scalar contraction. The Scalar Irrecoverability Theorem (Chapter 6) says this contraction destroys information. The lost information is *which dimensions are properly discounted at which rates*.

The practical consequence is enormous. A highway project with immediate monetary benefits ($d_1$, discounted at 3%) and long-term environmental costs ($d_6$, which should be discounted at 0.5%) will be approved under a single 3% rate and rejected under dimension-dependent discounting. The single rate effectively discounts the environment into irrelevance — not because anyone decided that the environment does not matter, but because the choice to use one rate for all dimensions implicitly makes that decision.

## 15.2 The Stern-Nordhaus Debate

The most consequential disagreement about discount rates is in climate economics. Nicholas Stern (2006) used a near-zero social discount rate ($\delta \approx 0.1\%$) and concluded that immediate, aggressive climate action is economically justified. William Nordhaus (2008) used a market-calibrated rate ($\delta \approx 3\%$) and concluded that gradual action is optimal.

**[Modeling Axiom.]** In the geometric framework, this is not a disagreement about preferences. It is a disagreement about the *curvature of the intergenerational manifold*.

Stern's manifold is nearly flat along the temporal axis: future people's welfare counts almost as much as present people's. The geodesic on this manifold avoids catastrophic climate trajectories even at high present cost, because the distant future is "close" on Stern's metric.

Nordhaus's manifold has positive curvature along the temporal axis: distant future welfare is geometrically farther away than present welfare. The geodesic on this manifold accepts some climate risk in exchange for faster present growth, because the distant future is "far" on Nordhaus's metric.

The geometric framework does not resolve the disagreement. But it makes the disagreement *precise*: Stern and Nordhaus are not arguing about whether to discount. They are arguing about the curvature tensor $R_{t i t j}$ along the temporal dimension of the social decision manifold. This is an empirical question — measurable, in principle, from revealed intergenerational preferences — not a philosophical one.

### The Ramsey Equation, Geometrized

The Ramsey equation is the standard formula for the social discount rate:

$$\delta = \rho + \eta \cdot g$$

where $\rho$ is the pure rate of time preference (how much we discount purely because something is in the future), $\eta$ is the elasticity of marginal utility (how quickly additional consumption becomes less valuable), and $g$ is the growth rate of consumption.

In the geometric framework, each term has a curvature interpretation:

- **$\rho$ (pure time preference)** is the *intrinsic* temporal curvature — the curvature that would exist even on a manifold where all other dimensions are constant. Stern sets $\rho \approx 0$ (no intrinsic preference for the present over the future — a flat temporal manifold). Nordhaus calibrates $\rho$ from market interest rates, arriving at $\rho \approx 1.5\%$ (moderate intrinsic curvature).

- **$\eta \cdot g$ (growth-adjusted discounting)** is the *extrinsic* temporal curvature induced by growth. If future people are richer ($g > 0$) and additional wealth has diminishing returns ($\eta > 0$), then a dollar in the future is "worth less" to them — the manifold curves away from the monetary axis as time progresses. Stern uses $\eta = 1$, $g \approx 1.3\%$, yielding $\eta g \approx 1.3\%$. Nordhaus uses $\eta \approx 2$, $g \approx 2\%$, yielding $\eta g \approx 4\%$.

The total discount rate is the sum of intrinsic and extrinsic curvature: $\delta = \rho + \eta g$. Stern: $\delta \approx 0.1 + 1.3 = 1.4\%$. Nordhaus: $\delta \approx 1.5 + 4 = 5.5\%$.

The geometric framework reveals a critical hidden assumption in the Ramsey equation: it assumes that all dimensions are discounted at the same rate — that the curvature is isotropic across dimensions. But there is no reason to believe this. Growth-adjusted discounting ($\eta g$) applies to dimensions where future people will be "richer." On $d_1$ (monetary wealth), growth is plausible — future generations may indeed be materially richer. On $d_6$ (environmental quality), growth is implausible — future generations may inherit a degraded environment. On $d_5$ (institutional trust), growth is uncertain. On $d_2$ (rights of future populations), growth is not even well-defined.

The Ramsey equation with a single $\delta$ conflates these dimensions. A multi-dimensional Ramsey equation would specify:

$$\delta_k = \rho + \eta_k \cdot g_k \quad \text{for each dimension } k$$

where $g_k$ is the growth rate of dimension $d_k$ and $\eta_k$ is the elasticity of the manifold in that dimension. For monetary wealth ($k=1$), $g_1 \approx 2\%$ and $\delta_1 \approx 4\%$. For environmental quality ($k=6$), $g_6 < 0$ (declining) and $\delta_6 < \rho$ (the discount rate should be *below* the pure time preference rate, because future environmental quality will be scarcer, not more abundant). For some dimensions, $\delta_k$ may even be negative — meaning that future values on that dimension should count *more* than present values, because the dimension is deteriorating.

This is the geometric resolution of the Stern-Nordhaus debate: both are correct on different dimensions. Nordhaus's rate is appropriate for $d_1$ (monetary value, which grows over time). Stern's rate is appropriate for $d_6$ (environmental quality, which does not grow and may decline). The error is in using a single rate for a multi-dimensional problem — a scalar contraction, once again, destroying the information that matters most.

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
