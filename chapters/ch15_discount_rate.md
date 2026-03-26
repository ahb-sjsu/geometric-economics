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

The discount rate is the most consequential single number in economics. It determines whether climate action is urgent or optional, whether infrastructure investment is worthwhile or wasteful, whether future generations matter or can be ignored. A change of two percentage points in the social discount rate swings the optimal climate policy from "spend 2% of GDP now to prevent catastrophe" (Stern) to "spend 0.5% of GDP now and adapt later" (Nordhaus). No other parameter in any economic model has such outsized influence on such momentous decisions.

And yet the discount rate is treated as a preference parameter — a number to be chosen, debated, and imposed by the analyst. The geometric framework reframes it as a *measurable property of the decision manifold*: the temporal curvature, which is as much a fact about the economic landscape as the interest rate or the inflation rate.

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

### The Holonomy of Intergenerational Obligation

Consider an obligation vector $\mathbf{O}$ at time $t = 0$: "preserve a livable planet for future generations." This obligation has components on multiple dimensions:

- $O_1$ (monetary): invest in mitigation technologies
- $O_2$ (rights): preserve the right to a livable environment
- $O_3$ (fairness): distribute costs proportionally to responsibility
- $O_6$ (social impact): protect vulnerable communities
- $O_9$ (epistemic): fund climate science to reduce uncertainty

Parallel-transporting this obligation 100 years forward on a curved manifold introduces holonomy. The components rotate: the $O_1$ component (invest in mitigation) may become more or less relevant as technology changes. The $O_2$ component (rights of future generations) may acquire new meaning as the rights framework evolves. The $O_9$ component (fund climate science) may become obsolete if the science is settled or intensify if new uncertainties emerge.

The total rotation angle — the holonomy — measures how much the obligation's content has drifted through temporal transport. A large holonomy means the obligation arrives in the future with significantly different content than it had in the present. This is not a failure of the obligation. It is a geometric property of the temporal manifold.

The practical implication: long-term policy commitments should be specified in *gauge-invariant* terms wherever possible — terms whose content does not depend on the specific temporal coordinate. "Maintain atmospheric CO₂ below 450 ppm" is approximately gauge-invariant: the meaning of the commitment does not change over time. "Spend 2% of GDP on climate mitigation" is gauge-variant: the meaning depends on future GDP levels, technology costs, and the composition of the economy. Gauge-invariant commitments resist holonomy; gauge-variant commitments drift.

## 15.4 Hyperbolic Discounting and Present Bias

**[Empirical.]** The empirically observed pattern of hyperbolic discounting — high discount rates for near-future outcomes, declining discount rates for distant-future outcomes — has a natural geometric explanation.

On a manifold with non-constant temporal curvature, the discount function is the integral of curvature along the temporal geodesic (Definition 15.1). If the curvature is high near the present (steep temporal manifold at short horizons) and low at distant horizons (flat temporal manifold at long horizons), the integrated discount function is:

$$D(t) = \exp\left(-\int_0^t K(\tau) \, d\tau\right)$$

For a curvature that decreases with time — $K(\tau) = K_0 / (1 + \alpha\tau)$ — this integral yields:

$$D(t) = (1 + \alpha t)^{-K_0/\alpha}$$

which is a hyperbolic discount function. The parameters $K_0$ (initial curvature) and $\alpha$ (rate of curvature decline) determine the specific shape.

The geometric explanation for why curvature is high near the present: nearby outcomes activate more dimensions of the decision manifold. A reward available *now* engages $d_1$ (monetary value), $d_4$ (autonomy — I can use it immediately), $d_7$ (identity — I am someone who seizes opportunities), $d_9$ (epistemic certainty — the reward is concrete and observable). A reward available in ten years engages primarily $d_1$, with the other dimensions attenuated by temporal distance. More active dimensions = higher-dimensional displacement = steeper curvature = higher effective discount rate.

This explanation makes a testable prediction: hyperbolic discounting should be *weaker* for goods that activate few dimensions at any time horizon (e.g., abstract monetary rewards — pure $d_1$) and *stronger* for goods that activate many dimensions at short horizons but few at long horizons (e.g., visceral rewards like food or social status). The experimental evidence confirms this pattern (McClure et al., 2004; Laibson, 1997).

### Time-Inconsistency as Curvature Change

The classic problem with hyperbolic discounting is *time-inconsistency*: a preference expressed today about future trade-offs changes when the future arrives. Today, I prefer $110 in 31 days to $100 in 30 days. When day 30 arrives, I prefer $100 today to $110 tomorrow. My preferences have reversed.

In the geometric framework, this is not a "bias." It is the natural consequence of position-dependent curvature. The curvature at time $t$ determines the discount rate at time $t$. When the agent moves forward to time $t + 30$, the curvature at that position is different (higher, because the manifold is steeper near the present). The "reversal" is the agent experiencing the same manifold from a different position — seeing different curvature because they are at a different point.

This reframing has a practical consequence: *commitment devices* (Laibson, 1997) are not corrections for irrationality. They are tools for navigating a manifold with position-dependent curvature. An agent who locks up their savings in a long-term account is not fighting their own bias. They are choosing to follow the geodesic computed from their current position (where the curvature favors long-term investment) and committing to it before they reach a future position where the curvature will favor short-term consumption. The commitment device is a boundary — a regulation the agent imposes on their own manifold — that prevents the geodesic from changing when the curvature changes.

> **MARIA'S COFFEE SHOP — DISCOUNTING IN PRACTICE**
>
> *Maria thinks about the solar panels differently depending on her time horizon. When she imagines next month (high temporal curvature), the $30,000 cost looms large — it is a full month's revenue, tangible, immediate, visceral. Her System 1 fires a boundary alarm on $d_1$. When she imagines the 25-year lifespan of the panels (low temporal curvature), the cost becomes a small investment relative to the total energy savings, the community signaling, and the regulatory anticipation. Her System 1 fires an identity alarm on $d_7$: "I am the kind of person who invests in the future."*
>
> *The discount rate she applies is different on different dimensions. On $d_1$ (monetary cost), she discounts at roughly 5% — the cost becomes manageable when spread over years. On $d_7$ (identity), she discounts at roughly 0% — the identity benefit of being an environmentally responsible business owner does not diminish with time. On $d_6$ (community impact), she discounts at roughly 1% — the neighborhood's appreciation of her environmental commitment persists but fades slightly as newer buildings adopt solar as standard.*
>
> *Her decision to install the panels is the Bond geodesic on a manifold with dimension-dependent temporal curvature. On the $d_1$-only manifold, the investment is marginal. On the full manifold, it is strongly positive — because the dimensions that matter most to Maria ($d_6$, $d_7$, $d_8$) have lower temporal curvature than the dimension that the spreadsheet captures ($d_1$).*

## 15.5 The Tragedy of the Horizon

Mark Carney, as Governor of the Bank of England, coined the phrase "tragedy of the horizon" to describe the disconnect between the time horizons of climate change (decades to centuries) and the time horizons of financial markets (quarters to years), political cycles (2-6 years), and regulatory mandates (5-10 years). Each institutional actor operates on a temporal manifold with curvature calibrated for its own horizon. None has curvature appropriate for the climate problem.

**[Empirical.]** The geometric framework formalizes this precisely. Let $K_i(t)$ be the temporal curvature of institution $i$'s decision manifold at horizon $t$:

| Institution | Short-horizon curvature $K_i(0)$ | Long-horizon curvature $K_i(100)$ | Effective discount rate |
|------------|----------------------------------|-----------------------------------|------------------------|
| Financial markets | Very high | Very high | 8-15% |
| Corporate management | High | High | 5-12% |
| Political cycles | High | Moderate | 3-8% |
| Infrastructure planning | Moderate | Moderate | 3-5% |
| Climate physics | Low | Very low | 0-1% |

Climate physics operates on a nearly flat temporal manifold: the atmosphere does not discount. CO₂ emitted today has the same radiative forcing in 2126 as it does in 2026. The physical system has $K \approx 0$ on the climate dimension. But every human institution that must *respond* to the physical system operates on a curved temporal manifold with $K \gg 0$. The result: no institution has the temporal curvature appropriate for the problem. The climate trajectory that the physical manifold requires (rapid decarbonization, starting now) is not a geodesic on any human institution's temporal manifold (because the near-term costs are high and the near-term curvature is steep).

The tragedy of the horizon is, geometrically, a *temporal curvature mismatch*: the problem lives on a flat manifold, but the decision-makers live on curved manifolds. The solution is not to change the physics (impossible) but to change the institutional curvature — to create institutions whose temporal manifolds are flatter than those of existing ones. Central banks with climate mandates, sovereign wealth funds with century-long horizons, constitutional provisions that encode intergenerational obligations — these are all attempts to create institutional agents with low temporal curvature, capable of computing geodesics on the flat manifold that the climate problem requires.

## 15.6 Discount Rates and Inequality

**[Empirical.]** The discount rate is not uniform across agents. Wealthy individuals discount at lower rates than poor individuals — not because the poor are "impatient" but because their temporal manifold has higher curvature. A person living paycheck to paycheck has intense temporal curvature near the present: next month's rent is a towering obstacle on the $d_1$ dimension, making the present enormously "close" and the future enormously "far." A wealthy individual experiences a flatter temporal manifold: next month's rent is a negligible perturbation, and the future is nearly as accessible as the present.

The geometric framework predicts that poverty traps (Chapter 10) are deepened by temporal curvature: poor agents discount the future steeply, which makes them less likely to invest in education ($d_9$), health ($d_2$), and relationship-building ($d_5$) — investments whose returns are delayed. The high discount rate is not a cause of poverty; it is a *consequence* of the curvature of the poverty-trap basin. An agent trapped in a high-curvature basin rationally discounts the future steeply, because the future is genuinely far away on their manifold — not in calendar time, but in the cost of getting there.

This has profound implications for policy. A payday lender charging 400% APR is exploiting the temporal curvature of poor agents' manifolds. The lender offers a path to the near future (cash today) at a cost calibrated to the agent's high curvature (the future $d_1$ cost is discounted by the agent at a rate that makes the loan appear affordable). On the borrower's manifold — where the present is sharply curved and the future is distant — the loan is on the geodesic. On a flatter manifold — the manifold the borrower would occupy if they were not in the poverty-trap basin — the loan is a catastrophic detour.

The geometric policy implication: reducing the temporal curvature of poor agents' manifolds (through income stabilization, safety nets, universal basic income) is not just an income transfer ($d_1$). It is a *manifold transformation*: it flattens the temporal curvature, making the future more accessible, making long-term investment rational, and changing the geodesic from one that loops through payday lenders to one that passes through education and savings. The income transfer is the mechanism; the manifold transformation is the effect.

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

## 15.7 Infrastructure Investment and Temporal Manifold Shaping

**[Modeling Axiom.]** Infrastructure investment is fundamentally an act of temporal manifold shaping. When a society builds a bridge, a power grid, or a transit system, it is reducing the curvature of future agents' decision manifolds — making transitions that are currently costly (crossing a river, accessing electricity, commuting to work) into transitions that are nearly costless.

The discount rate determines which infrastructure investments appear justified. At $\delta = 7\%$, a bridge with a 50-year lifespan whose benefits begin in year 5 has most of its value discounted away. At $\delta = 2\%$, the same bridge is strongly positive. At dimension-dependent rates — $\delta_1 = 5\%$ for monetary benefits, $\delta_6 = 1\%$ for community connectivity, $\delta_4 = 2\%$ for mobility autonomy — the bridge is even more clearly justified, because the community and autonomy benefits persist with little attenuation.

The geometric framework explains a puzzle in infrastructure economics: why do societies systematically under-invest in infrastructure (the "infrastructure gap"), even though the long-term returns are high? The answer: infrastructure's benefits are primarily on evaluative dimensions ($d_4$: autonomy of movement, $d_6$: community connectivity, $d_8$: institutional functionality) that should be discounted at low rates, but the costs are primarily on $d_1$ (construction expense), which budget authorities discount at market rates. The mismatch between the appropriate discount rates for costs (high, monetary) and benefits (low, evaluative) causes systematic under-investment.

The remedy is dimension-dependent discounting in cost-benefit analysis: discount monetary costs at the market rate, discount evaluative benefits at their dimension-specific rates. This is not a methodological novelty — it is a correction of a methodological error. The error is using a single rate for a multi-dimensional quantity, which is the same scalar contraction that the Scalar Irrecoverability Theorem shows destroys information.

## 15.8 Existential Risk and Zero Discounting

**[Speculation/Extension.]** Existential risks — events that would permanently end or catastrophically reduce human civilization (nuclear war, engineered pandemics, unaligned artificial superintelligence, certain climate tipping points) — pose a unique challenge to discounting theory.

On any positive discount rate, the cost of civilizational extinction in 2126 is finite and relatively small: $C \cdot e^{-\delta \cdot 100}$ for whatever value $C$ we assign to civilization. At $\delta = 3\%$, a 2126 extinction is discounted to $C \cdot e^{-3} \approx 0.05C$. At $\delta = 5\%$, it is $C \cdot e^{-5} \approx 0.007C$. The future destruction of everything is, on a curved temporal manifold, worth less than 1% of its face value.

The geometric framework says: the discount rate for existential risk should be zero or negative. The argument:

1. Existential risk is irreversible. It is a Type 1 boundary (Section 14.2's terminology): once crossed, the boundary crossing cannot be undone.
2. Irreversible boundaries should have $\beta = \infty$ (infinite boundary penalty).
3. An event with infinite penalty cannot be discounted — $\infty \cdot e^{-\delta t} = \infty$ for all $\delta$ and $t$.

Therefore, existential risks should not be discounted at all. The temporal curvature on the existential-risk dimension is zero: the future destruction of civilization is exactly as costly as the present destruction of civilization. This is not a moral intuition; it is a consequence of the boundary structure. Any policy analysis that discounts existential risk at a positive rate is committing a dimensional error: applying the temporal curvature of $d_1$ (monetary value, which grows and can therefore be discounted) to $d_2$ (the right of future people to exist, which is a sacred-value boundary with infinite penalty).

## 15.9 The Geometric Resolution: Why Discounting Is Not One Problem

This chapter has argued that the discount rate is not a single parameter to be chosen but a *tensor* — a multi-dimensional structure that varies across dimensions, across time, and across agents. The Stern-Nordhaus debate, the hyperbolic discounting puzzle, the infrastructure gap, the tragedy of the horizon, and the poverty trap deepening all dissolve when the scalar discount rate is replaced with its geometric generalization.

The resolution has four components:

**1. Dimension-dependent discounting.** Different dimensions of the decision manifold have different temporal curvatures. Monetary value ($d_1$) is properly discounted at market rates because it grows over time. Environmental quality ($d_6$) should be discounted at near-zero or negative rates because it is not growing — it is declining. Community bonds ($d_5$, $d_6$), institutional legitimacy ($d_8$), and existential security ($d_2$) each have their own temporal curvature, and each should be discounted at the rate that curvature implies.

**2. Position-dependent discounting.** The temporal curvature of the manifold varies with the agent's position. Wealthy agents experience flat temporal manifolds (low discount rates); poor agents experience steep temporal manifolds (high discount rates). This is not a preference difference — it is a curvature difference, measurable and predictable from the agent's position on the manifold.

**3. Path-dependent discounting.** The discount rate along a trajectory depends on the trajectory itself. A path through a period of crisis (high curvature) has a higher effective discount rate than a path through stability (low curvature). The "correct" discount rate for a policy depends on which future the policy envisions — which is why cost-benefit analyses are so sensitive to scenario assumptions.

**4. Conservation of obligation.** Intergenerational obligations, when formulated in gauge-invariant terms, are conserved quantities that should not be discounted. The obligation to preserve a livable planet does not diminish with time because it is not a monetary quantity — it is a sacred-value boundary ($\beta = \infty$) that is immune to temporal curvature.

The scalar discount rate — a single number applied uniformly to all dimensions, all agents, all paths, and all types of value — is the most consequential scalar contraction in economics. It takes a richly structured geometric object (the temporal curvature tensor) and crushes it to a point. The Scalar Irrecoverability Theorem says the information destroyed by this contraction cannot be recovered. The information that is destroyed includes: which dimensions should be discounted, how much, by whom, and under what conditions. This is, arguably, the most important information in the entire framework of intertemporal choice. And it is precisely the information that the scalar discount rate discards.

---

## Technical Appendix

**Definition 15.1 (Temporal Curvature).** The *temporal curvature* of the economic decision manifold at time $t$ is the sectional curvature $K(t, d_k)$ in the plane spanned by the temporal direction and dimension $d_k$. The discount function for dimension $d_k$ is:

$$D_k(t) = \exp\left(-\int_0^t K(\tau, d_k) \, d\tau\right)$$

When $K$ is constant, this yields exponential discounting. When $K$ decreases with $t$ (the manifold flattens at long horizons), this yields hyperbolic discounting.

**Proposition 15.2 (Dimension-Dependent Discounting).** **[Conditional Theorem.]** If temporal curvature varies across dimensions — $K(t, d_1) \neq K(t, d_6)$ — then the discount rate is dimension-dependent. Monetary value ($d_1$) may be discounted at 3% while community value ($d_6$) is discounted at 0.5%. The standard approach of applying a single discount rate to all dimensions is a scalar contraction that violates the Scalar Irrecoverability Theorem.

**Proposition 15.3 (Commitment Value as Curvature Reduction).** **[Conditional Theorem.]** A commitment device — a mechanism that constrains an agent's future choices — has positive value on a manifold with position-dependent temporal curvature. The value of commitment is:

$$V_{\text{commit}} = \text{BF}(\gamma_{\text{uncommitted}}) - \text{BF}(\gamma_{\text{committed}})$$

where $\gamma_{\text{uncommitted}}$ is the path an uncommitted agent follows (subject to curvature changes at each future time step) and $\gamma_{\text{committed}}$ is the path an agent follows when committed to the plan formulated at $t = 0$. When $V_{\text{commit}} > 0$ — when the uncommitted path has higher total friction due to curvature-induced deviations — the commitment device is welfare-improving.

This formalizes Laibson's (1997) insight that agents who recognize their own hyperbolic discounting will voluntarily adopt commitment devices. In the geometric framework, the agent is not fighting a "bias." They are recognizing that the manifold's curvature will change at future positions, causing their future geodesic to deviate from their current one, and pre-committing to the current geodesic before the curvature shift occurs.

---

## References

Nordhaus, W. D. (2008). *A Question of Balance.* Yale University Press.
Stern, N. (2006). *The Economics of Climate Change: The Stern Review.* Cambridge University Press.
Laibson, D. (1997). "Golden Eggs and Hyperbolic Discounting." *Quarterly Journal of Economics*, 112(2), 443–478.
Ramsey, F. P. (1928). "A Mathematical Theory of Saving." *Economic Journal*, 38(152), 543–559.
McClure, S. M., Laibson, D., Loewenstein, G., and Cohen, J. D. (2004). "Separate Neural Systems Value Immediate and Delayed Monetary Rewards." *Science*, 306(5695), 503–507.
Carney, M. (2015). "Breaking the Tragedy of the Horizon — Climate Change and Financial Stability." Speech at Lloyd's of London, September 29, 2015.
Gollier, C. (2012). *Pricing the Planet's Future: The Economics of Discounting in an Uncertain World.* Princeton University Press.
