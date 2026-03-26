# Chapter 6: Economic Tensors and Scalar Irrecoverability

> *"The ideas of economists and political philosophers, both when they are right and when they are wrong, are more powerful than is commonly understood. Indeed, the world is ruled by little else. Practical men, who believe themselves to be quite exempt from any intellectual influences, are usually the slaves of some defunct economist."*
> -- John Maynard Keynes, *The General Theory of Employment, Interest, and Money* (1936)

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *An appraiser has valued Maria's coffee shop at $200,000. The number sits on a single sheet of paper -- clean, precise, authoritative. The REIT that owns her building wants to buy her out. The number is what they will negotiate from.*
>
> *But what does the number contain? The appraiser used a standard discounted-cash-flow model: projected revenue minus projected costs, discounted at the market rate, summed over a reasonable time horizon. The methodology is impeccable -- on $d_1$. The number captures the monetary value of the business as a going concern.*
>
> *What the number cannot contain:*
>
> *The community value ($d_6$): Maria's shop is where neighborhood families gather, where immigrant workers find help with paperwork, where the local parent group organizes. This value exists, is real, and benefits both the community and Maria's business (through loyalty and word-of-mouth), but it does not appear in the cash-flow projection.*
>
> *The fair-trade supply chain ($d_3$, $d_7$): Maria sources from a small Oakland roaster who sources from cooperatives in Ethiopia and Colombia. This supply chain embodies six years of relationship-building, fair prices to growers, and quality development. Switching to a commodity supplier would lose this infrastructure. The value is real but invisible to the DCF model.*
>
> *The jobs created ($d_4$, $d_6$): Four employees depend on the shop. Their wages, their autonomy, their contribution to the neighborhood -- none of this enters the valuation.*
>
> *The cultural identity ($d_7$): The shop is part of what makes the Mission District the Mission District. Its displacement would be one more step in the homogenization that erodes the neighborhood's character. This is value of a kind that no scalar can express.*
>
> *The Scalar Irrecoverability Theorem proves that these dimensions cannot be recovered from the $200,000 alone. The appraiser's number is not an approximation. It is a projection that has destroyed information -- mathematically, irreversibly.*

---

## The Problem of the Single Number

Economics traffics in single numbers. A company is "worth" $4.2 billion. A policy "costs" $300 million. A worker "earns" $85,000. A nation's economy "grew" 2.3%. In each case, a complex, multi-dimensional economic reality has been compressed to a scalar -- a single point on the real line.

The previous chapters have built the apparatus to understand what this compression does. Chapter 3 constructed the economic decision complex $\mathcal{E}$ with its nine-dimensional attribute vectors. Chapter 4 equipped it with a metric that encodes the interactions between dimensions. Chapter 5 showed that the price signal is a heuristic field on $d_1$ alone, unable to capture the full manifold structure.

This chapter proves the central negative result: the information destroyed by scalar compression is *mathematically irrecoverable*. No amount of sophistication in the scalar model -- no refinement of the utility function, no cleverness in the aggregation rule -- can compensate for the dimensional collapse. The theorem is not a practical limitation (we could recover the information if we tried harder). It is a mathematical impossibility (the information does not exist in the scalar, and no procedure can reconstruct it).

The chapter then develops the positive alternative: the *economic tensor*, a mathematical object that preserves the full multi-dimensional structure that the scalar destroys, and shows how GDP, utility, and business valuation are specific *contractions* of this richer object.

## The Scalar Irrecoverability Theorem

We begin with the central negative result.

> **Theorem 14 (Scalar Irrecoverability).** *Let $\phi: \mathbb{R}^9 \to \mathbb{R}$ be any continuous function that maps a 9-dimensional attribute vector to a scalar utility value. Then:*
>
> 1. *$\phi$ is not injective (multiple distinct attribute vectors map to the same scalar).*
>
> 2. *The information lost under $\phi$ is irrecoverable: there exists no continuous function $\psi: \mathbb{R} \to \mathbb{R}^9$ such that $\psi \circ \phi = \text{id}$.*
>
> 3. *The optimal path on $\mathcal{E}$ (the Bond geodesic) is in general different from the path that maximizes $\phi$-utility, and the difference is not bounded by any function of $\phi$ alone.*

This theorem is the mathematical core of the book's argument. Let us prove it in full.

> *Proof.*
>
> **(1) $\phi$ is not injective.** Restricting to the compact subset $[0,1]^9 \subset \mathbb{R}^9$, the continuous image $\phi([0,1]^9)$ is a compact subset of $\mathbb{R}$, hence a closed bounded interval $[a, b]$. Suppose $\phi$ were injective. Then $\phi|_{[0,1]^9}: [0,1]^9 \to [a,b]$ is a continuous bijection from a compact space to a Hausdorff space, hence a homeomorphism onto its image -- an embedding of $[0,1]^9$ into $\mathbb{R}$. But $[0,1]^9$ has topological dimension 9, while any subspace of $\mathbb{R}$ has topological dimension $\leq 1$. Since homeomorphisms preserve topological dimension, this is a contradiction (by Brouwer's invariance of dimension theorem). Therefore $\phi$ is not injective.
>
> (If $\phi$ is additionally differentiable, this also follows from the rank-nullity theorem: the kernel of $d\phi_x$ has dimension $\geq 8$ at every point, so $\phi$ cannot be locally injective.)
>
> **(2) The information loss is irrecoverable.** Since $\phi$ is not injective, there exist $\mathbf{a} \neq \mathbf{a}'$ with $\phi(\mathbf{a}) = \phi(\mathbf{a}')$. Any left inverse $\psi$ must map $\phi(\mathbf{a})$ to both $\mathbf{a}$ and $\mathbf{a}'$, which is impossible since $\psi$ must be a function. Therefore no left inverse exists. The lost information is not merely hard to recover -- it is mathematically nonexistent in the scalar representation. No procedure, however sophisticated, can reconstruct $\mathbf{a}$ from $\phi(\mathbf{a})$ alone, because the mapping $\phi^{-1}(\phi(\mathbf{a}))$ is a level set of dimension $\geq 8$ -- a vast family of attribute vectors that all map to the same scalar, with no way to determine which element of the family was the original.
>
> **(3) The optimal path diverges.** The minimum-cost path on $\mathcal{E}$ depends on the full 9-dimensional edge weights: $w(v_i, v_j) = \Delta\mathbf{a}^T \Sigma^{-1} \Delta\mathbf{a} + \sum_k \beta_k \cdot \mathbf{1}[\text{boundary } k \text{ crossed}]$. The $\phi$-optimal path depends only on $\phi$-values at the vertices: it follows the steepest ascent in $\phi$. Two edges with identical $\phi$-differences but different attribute-vector differences will have different weights on $\mathcal{E}$ but identical weights under $\phi$. The $\phi$-optimal path may therefore cross moral boundaries (adding infinite penalty on $\mathcal{E}$) while achieving maximal $\phi$-gain. The difference between the $\mathcal{E}$-optimal and $\phi$-optimal paths is unbounded because the boundary penalty $\beta_k$ can be infinite while the $\phi$-difference is finite. No function of $\phi$ alone can bound the divergence, because $\phi$ cannot distinguish boundary-crossing edges from non-boundary-crossing edges that have the same scalar effect. $\square$

### What the Theorem Says

The theorem establishes three things:

**First**, scalar utility is not merely an imprecise approximation -- it is a lossy compression that maps entire families of distinct economic states to the same number. Maria's coffee shop valued at $200,000 occupies a *level set* -- an eight-dimensional surface of all possible business configurations that happen to generate the same discounted cash flow. Some of these configurations involve exploitative labor practices, broken supplier relationships, and community-destroying operations. Others involve fair wages, trusted relationships, and community enrichment. The scalar cannot distinguish them.

**Second**, the information destroyed by the projection is *mathematically irrecoverable*. This is not a claim about measurement difficulty or data availability. It is a topological impossibility: you cannot continuously embed a nine-dimensional space in a one-dimensional space. The "missing dimensions" do not exist in the scalar representation and cannot be reconstructed from it by any means.

**Third**, the economic consequences are unbounded. The gap between what the scalar recommends and what the full manifold recommends can be arbitrarily large -- infinite, in cases where the scalar-optimal path crosses a moral boundary that the scalar cannot see.

### The Allais and Ellsberg Paradoxes

The theorem immediately resolves two classical paradoxes that have troubled expected utility theory since the 1950s.

> **Corollary 15 (The Allais and Ellsberg Paradoxes Are Not Paradoxes).** *The Allais paradox (violation of the independence axiom) and the Ellsberg paradox (violation of subjective expected utility under ambiguity) are both consequences of Scalar Irrecoverability.*
>
> 1. **Allais**: *The agent's preference reversal between "certain $1M" and "89% chance of $1M, 10% chance of $5M, 1% chance of $0" reflects the activation of $d_9$ (epistemic certainty has value beyond expected monetary value) and $d_7$ (identity: "I am prudent"). On the scalar projection, independence is violated. On the full manifold, preferences are consistent: the attribute-vector difference between certainty and risk includes non-zero components on $d_7$ and $d_9$ that the expected-value calculation discards.*
>
> 2. **Ellsberg**: *Ambiguity aversion (preferring known to unknown probabilities) reflects $d_9$ directly: known probabilities have higher epistemic-status scores than ambiguous ones. The Mahalanobis distance from the ambiguous gamble to the goal is larger than from the known-probability gamble, even when expected values are equal, because $\Delta d_9 \neq 0$ for the ambiguous case.*

The resolution is not to add "certainty preference" or "ambiguity aversion" as ad hoc modifications to the utility function. It is to recognize that the utility function was computing on the wrong manifold. The "paradoxes" are artifacts of the $d_1$ projection. On the full manifold, the behavior is consistent, transitive, and predictable.

## Projected Intransitivity

The irrecoverability theorem has a particularly striking consequence for the transitivity of preferences -- one of the foundational axioms of rational choice theory.

> **Theorem 16 (Projected Intransitivity).** *Let $\succ_E$ denote the preference relation on the full manifold ("$x \succ_E y$ iff $w(v_0, x) < w(v_0, y)$") and let $\succ_\phi$ denote the projected preference ("$x \succ_\phi y$ iff $\phi(x) > \phi(y)$"). Then:*
>
> 1. *$\succ_E$ is transitive (it is a total order induced by path cost from $v_0$).*
>
> 2. *$\succ_\phi$ may be intransitive: there exist alternatives $x, y, z$ such that $\phi(x) > \phi(y) > \phi(z) > \phi(x)$ is possible when the projection $\phi$ discards different dimensions for different pairwise comparisons.*

> *Proof.*
>
> (1) Path cost $w(v_0, \cdot)$ is a real-valued function on vertices of $\mathcal{E}$; the induced ordering is a total preorder, hence transitive.
>
> (2) Consider three alternatives with attribute vectors $\mathbf{a}(x) = (3,1,5)$, $\mathbf{a}(y) = (5,3,1)$, $\mathbf{a}(z) = (1,5,3)$ in a 3-dimensional example. If $\phi$ is context-dependent -- comparing $x$ vs. $y$ on dimensions $\{1,2\}$ (where $y$ wins), $y$ vs. $z$ on dimensions $\{2,3\}$ (where $z$ wins), and $z$ vs. $x$ on dimensions $\{1,3\}$ (where $x$ wins) -- then $\succ_\phi$ is cyclic. This context-dependence is precisely what Tversky's experiments on intransitive preferences demonstrate: the "relevant" dimension shifts with the comparison pair. On $\mathcal{E}$ with a fixed metric, preferences are transitive; the intransitivity is an artifact of context-dependent projection. $\square$

This is a remarkable result. Intransitivity of preferences -- one of the most documented "irrationalities" in behavioral economics -- is not a property of the agent's preferences. It is a property of the *projection*. On the full manifold, with a fixed metric, the same agent's preferences are perfectly transitive. The intransitivity appears only when the projection $\phi$ selectively discards different dimensions for different comparisons, which is precisely what happens in the Tversky experiments where the framing of each pairwise comparison activates different dimensions.

The analogy is a helix -- a curve that is monotonically ascending in three dimensions. Project it onto a plane, and it appears to reverse direction periodically. The reversals are not in the helix; they are in the projection.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria exhibits exactly this "intransitivity" when comparing three options for her business:*
>
> *Option X: Higher-margin menu with conventional beans ($d_1$ = 5, $d_7$ = 1)*
>
> *Option Y: Current menu with fair-trade beans ($d_1$ = 3, $d_7$ = 5)*
>
> *Option Z: Expand seating and raise volume ($d_1$ = 4, $d_6$ = 5, but $d_7$ = 2 because expansion requires displacing the community bulletin board)*
>
> *Asked to compare X vs. Y, she focuses on identity ($d_7$) and chooses Y. Asked to compare Y vs. Z, she focuses on community impact ($d_6$) and revenue ($d_1$) and chooses Z. Asked to compare Z vs. X, she focuses on pure economics ($d_1$) and chooses X. The cycle $Y \succ X$, $Z \succ Y$, $X \succ Z$ appears intransitive.*
>
> *But Maria's preferences are perfectly transitive on the full manifold. Each comparison activates a different dimension because the comparison itself changes which aspects of the options are salient. On $\mathcal{E}$ with a fixed metric that weights all dimensions consistently, the three options have well-defined total costs from her current state, and the ordering is total.*

---

## The Grocery Store Example

To make the irrecoverability theorem concrete, consider the example from the paper that illustrates how the full manifold produces radically different evaluations than the scalar.

> **Example 17 (The Grocery Store).** An agent stands in a grocery store. Two paths are available:
>
> - **Path A (buy):** Pay $50. Attribute-vector change: $\Delta d_1 = -50$, all other dimensions $\approx 0$. Edge weight: $w_A = 50^2 / \sigma_1^2$.
>
> - **Path B (steal):** Pay $0. Attribute-vector change: $\Delta d_1 = 0$, but $\Delta d_2 = -\infty$ (rights violation), $\Delta d_6 = -\text{large}$ (social sanction risk), $\Delta d_7 = -\text{large}$ (identity violation). Edge weight: $w_B = \infty$.
>
> Under scalar utility ($\phi = d_1$): $\phi(B) > \phi(A)$, so Homo economicus steals.
>
> On the full manifold: $w_B = \infty > w_A$, so the rational agent buys.

The agent is not "irrational" for buying. The economist is computing on the wrong manifold. The scalar utility function $\phi = d_1$ maps both paths to their monetary cost, discarding the rights violation, the social sanction, and the identity damage that make stealing infinitely costly on the full manifold. The Scalar Irrecoverability Theorem tells us why this error cannot be fixed by making the utility function more sophisticated: any continuous $\phi: \mathbb{R}^9 \to \mathbb{R}$ will map some pair of attribute vectors to the same scalar, and the pair it confuses may include the exact distinction that determines the decision.

This is the deepest implication of the theorem: it is not that scalar utility needs to be *improved*. It is that scalar utility is *structurally incapable* of representing the information that drives actual economic behavior. The fix is not a better $\phi$. It is a higher-dimensional representation.

## The Economic Tensor

Having established what the scalar destroys, we now construct what preserves it: the economic tensor.

### From Scalars to Tensors

A scalar is a single number. A vector is an ordered list of numbers with transformation rules. A *tensor* is a multi-dimensional array of numbers with specific transformation rules that preserve geometric content under change of coordinates. The key property is that tensors encode *relationships between dimensions* -- exactly the information that scalars destroy.

In physics, the stress-energy tensor $T_{\mu\nu}$ encodes the full state of matter and energy at a point in spacetime: energy density, momentum flux, pressure, shear stress. Contracting this tensor (summing over indices) produces scalars like total energy or total pressure, but the contraction destroys the directional information: you cannot recover the full stress state from the total energy alone.

The same mathematical structure applies to economics.

### Economic Obligations as Vectors

Consider an economic obligation -- Maria's lease, for instance. The lease is not a scalar (a monthly rent payment). It is a *vector* on the decision manifold:

$$\mathbf{L} = (L_1, L_2, L_3, L_4, L_5, L_6, L_7, L_8, L_9)$$

where:

- $L_1 = -7{,}000$ (monthly rent payment, $d_1$)
- $L_2 = +1$ (the lease grants occupancy rights, $d_2$)
- $L_3 = -0.6$ (the 40% increase is perceived as unfair, $d_3$)
- $L_4 = -0.4$ (the increase constrains business autonomy, $d_4$)
- $L_5 = -0.7$ (the increase eroded trust with the landlord, $d_5$)
- $L_6 = +0.8$ (the lease preserves the community gathering space, $d_6$)
- $L_7 = -0.3$ (accepting the increase conflicts slightly with self-image, $d_7$)
- $L_8 = +0.5$ (the lease is a legitimate legal contract, $d_8$)
- $L_9 = -0.5$ (uncertainty about future increases, $d_9$)

The monthly rent payment $L_1 = -7{,}000$ is the scalar projection. It captures one component of a nine-dimensional object. The remaining eight components -- the rights, the fairness, the trust, the community value, the identity, the legitimacy, the epistemic status -- are all real, all measurable (at least ordinally), and all relevant to Maria's decisions about the lease.

### Economic Interests as Covectors

If obligations are vectors (they "point" in the direction of their impact on the agent's state), then economic *interests* are *covectors* (dual vectors) -- they assign a value to each direction.

Maria's interest in her business is a covector:

$$\mathbf{I} = (I^1, I^2, I^3, I^4, I^5, I^6, I^7, I^8, I^9)$$

where $I^k$ represents how much Maria cares about changes along dimension $k$. The *satisfaction* of an obligation-interest pair is the contraction (inner product):

$$S = \mathbf{I} \cdot \mathbf{L} = \sum_{k=1}^{9} I^k L_k$$

This is a scalar -- a single number. But it is a *derived* scalar, obtained from the contraction of a vector and a covector. The full tensor structure is preserved in $\mathbf{I}$ and $\mathbf{L}$; the scalar $S$ is a specific summary of their interaction.

### GDP as Tensor Contraction

The most consequential scalar in economics -- GDP -- is a specific contraction of the full economic tensor.

Define the *national economic tensor* $\mathbf{T}$ as the aggregate of all economic activity in a country over a period, with components $T_{k}$ representing the total change along each dimension $k$:

$$\text{GDP} = T_1 = \pi_{d_1}(\mathbf{T})$$

GDP is the $d_1$ component of $\mathbf{T}$ -- the projection onto the monetary dimension. The Stiglitz-Sen-Fitoussi Commission (2009) was arguing, in the language of this framework, that economic welfare should be assessed using $\mathbf{T}$ (or at least a higher-rank contraction of it), not $T_1$ alone.

The Scalar Irrecoverability Theorem tells us that the Commission was mathematically correct: the information in $\mathbf{T}$ that GDP discards is irrecoverable from GDP alone. Two economies with identical GDP can have radically different values on $d_3$ (fairness), $d_5$ (trust), $d_6$ (social cohesion), and $d_8$ (institutional legitimacy). No post-hoc adjustment to GDP -- no "GDP plus inequality adjustment," no "green GDP" -- can recover this information, because the projection has destroyed it.

What would recover it is *not projecting in the first place*: reporting the full vector $\mathbf{T}$ (or a sufficient subset of its components) rather than the scalar $T_1$.

### The Tensor Structure of Business Valuation

Maria's coffee shop valuation of $200,000 is a contraction of the full business tensor:

$$\text{Valuation} = \phi(\mathbf{B}) = \phi(B_1, B_2, \ldots, B_9)$$

where $\mathbf{B}$ is the attribute vector of the business and $\phi$ is the discounted-cash-flow function. The theorem says: this valuation maps many distinct businesses to the same number. Some businesses worth $200,000 in DCF terms are thriving community institutions with deep trust networks and ethical supply chains. Others worth $200,000 are extractive operations with high turnover, adversarial supplier relationships, and no community value. The number cannot distinguish them.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *What would a tensor valuation of Maria's coffee shop look like?*
>
> | Dimension | Component | Assessment |
> |-----------|-----------|------------|
> | $d_1$: Consequences | $B_1 = \$200{,}000$ | DCF valuation (the only thing the appraiser reported) |
> | $d_2$: Rights | $B_2 = 0.7$ | Strong: clear lease, business licenses, supplier contracts |
> | $d_3$: Fairness | $B_3 = 0.8$ | High: fair wages, fair prices, equitable supplier terms |
> | $d_4$: Autonomy | $B_4 = 0.6$ | Moderate: constrained by landlord's pricing power |
> | $d_5$: Trust | $B_5 = 0.9$ | Very high: six-year supplier relationship, loyal customers |
> | $d_6$: Social impact | $B_6 = 0.85$ | High: community hub, four jobs, neighborhood identity |
> | $d_7$: Identity | $B_7 = 0.9$ | Very high: Maria's identity as ethical business owner |
> | $d_8$: Legitimacy | $B_8 = 0.7$ | Moderate: standard regulatory compliance |
> | $d_9$: Epistemic | $B_9 = 0.4$ | Low: uncertainty about rent, neighborhood trajectory |
>
> *The full tensor $\mathbf{B} = (\$200K, 0.7, 0.8, 0.6, 0.9, 0.85, 0.9, 0.7, 0.4)$ contains information that the scalar $\$200K$ cannot. A buyer who acquires the business and replaces the fair-trade supplier with a commodity supplier, fires the long-term employees, and converts the community space to additional seating would preserve $B_1$ (maybe even increase it) while destroying $B_3$, $B_5$, $B_6$, and $B_7$. The scalar valuation would say: "Business maintained or improved." The tensor valuation would say: "Business gutted on five of nine dimensions."*
>
> *This is not a difference of opinion. It is a difference of *dimensionality*. The scalar and the tensor are making different mathematical claims, and the tensor's claim is richer, more informative, and -- by the irrecoverability theorem -- strictly non-recoverable from the scalar.*

---

## Worked Example: Maria's Valuation Under Different Projections

To demonstrate concretely how the valuation changes depending on which dimensions are included, let us compute the "value" of Maria's coffee shop under several different projection functions $\phi$.

### Projection 1: Pure DCF ($\phi = \pi_{d_1}$)

The standard discounted-cash-flow projection considers only the monetary dimension. Inputs: annual revenue $226,800 (from the monthly figure), annual costs $210,000 (rent + supplies + wages + utilities), discount rate 10%, assumed 10-year horizon with 2% growth.

$$\text{Value}_1 = \sum_{t=1}^{10} \frac{(226{,}800 \times 1.02^{t-1}) - 210{,}000}{1.10^t} \approx \$200{,}000$$

This is the appraiser's number. It captures one dimension.

### Projection 2: DCF + Community Value ($\phi = \pi_{d_1, d_6}$)

Suppose we attempt to monetize the community value. The shop serves as a gathering place for approximately 120 neighborhood residents who use it as their primary social space. If the closure of the shop forced even 20% of these residents to use alternative venues (coworking spaces, other cafes farther away), the additional cost to them would be approximately $50/month each -- $14,400/year in monetized community value. Adding this stream:

$$\text{Value}_2 \approx \$200{,}000 + \$88{,}000 = \$288{,}000$$

But this monetization is itself a projection -- converting $d_6$ to $d_1$ at an exchange rate that may not be well-defined. The community value of a neighborhood gathering place is not commensurable with monetary flow. The $88K figure is an estimate, not a measurement.

### Projection 3: DCF + Supply Chain Value ($\phi = \pi_{d_1, d_3, d_5, d_7}$)

The fair-trade supply chain represents six years of relationship-building. The cost of re-establishing an equivalent chain from scratch (finding reliable fair-trade cooperatives, building trust, achieving quality consistency) can be estimated at 18-24 months of procurement effort, or approximately $35,000-$50,000 in search costs, quality failures, and relationship development. Adding the supply chain's relational value:

$$\text{Value}_3 \approx \$200{,}000 + \$88{,}000 + \$42{,}000 = \$330{,}000$$

### Projection 4: Full Tensor Assessment

The full tensor does not produce a single number. It produces a vector:

$$\mathbf{B} = (\$200K, 0.7, 0.8, 0.6, 0.9, 0.85, 0.9, 0.7, 0.4)$$

This representation preserves the fact that the business is strong on trust ($B_5 = 0.9$) and identity ($B_7 = 0.9$) but weak on epistemic status ($B_9 = 0.4$ -- uncertainty about the future). A buyer can see which dimensions are strong and which are fragile. A scalar valuation hides this structure entirely.

The progression from $200K to $288K to $330K is not convergence toward a "true" scalar value. Each additional dimension reveals additional value, but the scalar still destroys the *structure* of the value. The $330K number does not tell you that the business is trust-rich and certainty-poor. Only the tensor does.

### The Irrecoverability in Action

Here is the critical point: given only the scalar $200,000, can you determine whether this is a community-embedded, trust-rich, fair-trade coffee shop or a sterile chain location with no community ties, adversarial supplier relationships, and high employee turnover? No. Both could generate identical cash flows. The scalar maps them to the same number. The information needed to distinguish them has been destroyed, and the Scalar Irrecoverability Theorem proves that no procedure can reconstruct it.

This is not an academic curiosity. It is the mechanism by which real economic damage occurs. When the REIT evaluates whether to buy Maria out and install a chain tenant, the DCF analysis says: "The chain tenant pays higher rent and generates higher cash flow. The acquisition is value-creating." On $d_1$, this is correct. On the full manifold, the acquisition destroys community value ($d_6$), trust networks ($d_5$), fair-trade supply chains ($d_3$, $d_7$), and neighborhood identity ($d_7$). The REIT cannot see what it is destroying because its valuation methodology operates on a scalar projection of a nine-dimensional reality.

## Implications of Irrecoverability

### For Utility Theory

The theorem strikes at the foundation of expected utility theory. Von Neumann and Morgenstern (1944) proved that if preferences satisfy four axioms (completeness, transitivity, independence, continuity), then there exists a utility function $u: X \to \mathbb{R}$ such that the agent's behavior is equivalent to maximizing $\mathbb{E}[u]$.

This is a *representation theorem*, not a behavioral theory. It says: *if* preferences satisfy the axioms, *then* they can be represented as scalar utility maximization. The behavioral economics program has shown that preferences systematically violate the axioms -- particularly independence (Allais) and transitivity (Tversky).

The geometric framework provides the diagnosis: the axioms are satisfied on the full manifold but violated on the scalar projection. A preference relation that is transitive in nine dimensions can appear intransitive when projected onto one dimension (Theorem 16). A preference relation that satisfies independence on the full attribute vector can violate independence when the projection discards dimensions that are differentially activated across comparisons (Corollary 15).

The fix is not to abandon the axioms or to catalog the violations as "biases." The fix is to recognize that the axioms hold on the correct manifold -- and that the correct manifold has nine dimensions, not one.

### For Welfare Economics

If scalar utility is irrecoverably lossy, then welfare functions defined on scalar utilities inherit the loss. Arrow's impossibility theorem (1951) proves that no social welfare function can simultaneously satisfy unrestricted domain, Pareto efficiency, independence of irrelevant alternatives, and non-dictatorship when aggregating ordinal rankings.

The geometric framework suggests that Arrow's impossibility is an artifact of the scalar domain. Arrow's theorem operates on one-dimensional ordinal rankings. When agents evaluate alternatives as attribute vectors in $\mathbb{R}^9$, a component-wise social welfare mapping $W: (\mathbb{R}^9)^n \to \mathbb{R}^9$ can satisfy analogues of all four Arrow conditions simultaneously; the impossibility reappears only when $W$ is composed with a projection $\phi: \mathbb{R}^9 \to \mathbb{R}$. A full treatment of multi-dimensional social choice is deferred to future work, but the geometric perspective suggests that the impossibility is in the *projection*, not in the aggregation.

### For Policy Analysis

Cost-benefit analysis requires converting all costs and benefits to a common monetary unit. The Scalar Irrecoverability Theorem says this conversion is *necessarily lossy*: the monetized value of environmental damage, social displacement, or trust erosion is a projection of a multi-dimensional cost onto $d_1$, and the projection cannot be inverted.

This does not mean cost-benefit analysis is useless. It means that the single number it produces should be understood as a *component* of the full evaluation, not as the evaluation itself. The geometric alternative: report the full cost-benefit vector, one component per active dimension, and make the trade-offs between dimensions explicit rather than hiding them inside an exchange rate that converts everything to dollars.

## The Structure of What Is Lost

The irrecoverability theorem tells us that information is destroyed. But what is the *structure* of the lost information? What, specifically, does the scalar discard?

### Cross-Dimensional Interactions

The covariance matrix $\Sigma$ encodes how the nine dimensions interact. The scalar discards $\Sigma$ entirely.

For Maria's coffee shop, the critical interactions include:

- **$d_1 \leftrightarrow d_5$ (money-trust interaction):** The monetary terms of the lease affect the trust relationship with the landlord, and the trust relationship affects the monetary stability of the business. These are not independent.

- **$d_3 \leftrightarrow d_6$ (fairness-community interaction):** Whether the shop's pricing is perceived as fair directly affects community engagement and loyalty, which in turn affects revenue. The $d_3$-$d_6$ cross-term in $\Sigma$ captures this coupling.

- **$d_5 \leftrightarrow d_7$ (trust-identity interaction):** Maria's identity as an ethical business owner depends on maintaining trust with her suppliers and employees. A betrayal of trust ($d_5$) produces an identity crisis ($d_7$) that is larger than either dimension's marginal change would suggest. The cross-term amplifies the effect.

A scalar valuation that monetizes each dimension independently and sums the results would capture the diagonal terms of $\Sigma$ but miss the cross-terms. The cross-terms are often the most economically significant: they represent *synergies* and *conflicts* between dimensions that drive the decisions that matter most.

### Boundary Information

The scalar discards all information about moral-economic boundaries. The boundary between "fair pricing" and "exploitation" ($d_3$), between "trustworthy partner" and "unreliable counterparty" ($d_5$), between "legal transaction" and "criminal act" ($d_2$) -- these boundaries define the phase structure of the decision manifold. They determine which paths are available and which are blocked by infinite-weight edges.

A scalar valuation cannot represent boundaries. A continuous function $\phi: \mathbb{R}^9 \to \mathbb{R}$ maps points near a boundary to values that are continuous with points far from the boundary. The discontinuous jump in decision regime -- the phase transition from "normal pricing" to "price gouging," from "tough negotiation" to "exploitation" -- is smoothed away by the continuity of $\phi$.

This is why scalar economic models consistently underestimate the severity of boundary crossings. The model sees a continuous increase in price; the agent (and the community) sees a discontinuous transition from fair dealing to exploitation. The scalar model predicts gradual response; the actual response is a sharp phase transition -- boycott, regulation, reputational destruction -- because the boundary penalty $\beta_k$ is not a continuous function of the scalar change. It is a discrete event: you cross the boundary or you don't.

### Directional Information

Perhaps most importantly, the scalar discards *direction*. A scalar change of $+\$50K$ in business value could mean:

- Revenue grew 25% while costs remained stable (pure $d_1$ improvement)
- Revenue grew 40% but only because the owner switched to exploitative suppliers ($d_1$ up, $d_3$ and $d_7$ down)
- Revenue was flat but a major liability was settled ($d_1$ up from liability resolution, $d_9$ up from uncertainty reduction)
- Revenue grew modestly from expanded hours that also increased community engagement ($d_1$ up, $d_6$ up)

Each of these represents a different *direction* of movement on the manifold. They have different implications for future decisions, different stability properties, and different effects on the other dimensions. The scalar $+\$50K$ erases all directional information.

A tensor representation preserves it. The change vector $\Delta\mathbf{B} = (50K, \Delta B_2, \ldots, \Delta B_9)$ specifies not just the magnitude of the change but its direction on the manifold. This directional information is precisely what investors, regulators, and communities need to assess whether an economic change is *genuinely* value-creating or merely value-extracting.

## The Fundamental Distinction: Transferable vs. Evaluative Dimensions

One structural feature of the economic tensor deserves special emphasis. Not all nine dimensions behave the same way in exchange.

**Transferable dimensions** ($d_1$: monetary value, $d_2$: rights/entitlements, $d_4$: autonomy) are *conserved* in bilateral exchange: what one party gains, the other loses. If Maria pays $7,000 in rent, the landlord receives $7,000. If a property right is transferred, one party gains it and the other loses it. These dimensions are zero-sum.

**Evaluative dimensions** ($d_3$: fairness, $d_5$: trust, $d_6$: social impact, $d_7$: identity/virtue) are *not conserved*. Both parties to an exchange can simultaneously perceive increased fairness. Both can experience increased trust. A fair exchange creates mutual value on $d_3$ that did not exist before the exchange. An unfair exchange can destroy value on $d_3$ for both parties (the exploiter loses self-respect on $d_7$ even as they gain on $d_1$).

This distinction -- formalized as the Attribute Conservation theorem in the broader framework -- explains why some aspects of trade are genuinely positive-sum (the evaluative dimensions allow mutual gain) while others are genuinely zero-sum (the transferable dimensions cannot be created by exchange). A theory that collapses all dimensions to $d_1$ cannot make this distinction: it sees all exchange as either zero-sum (monetary transfer) or positive-sum (welfare improvement from trade), but it cannot separate the mechanisms.

The economic tensor preserves the distinction. The transferable components of $\mathbf{T}$ sum to zero in bilateral exchange. The evaluative components can sum to a positive or negative value, depending on whether the exchange is conducted fairly, trustingly, and with respect for community impact.

## Beyond the Single Number

The Scalar Irrecoverability Theorem is, at bottom, a theorem about *information*. It says that the move from nine dimensions to one dimension destroys eight dimensions of information, and that this destruction is irreversible. No amount of cleverness in the scalar model can compensate for what it has discarded.

The practical implication is not that we should abandon scalar measures entirely. Scalars are useful summaries for routine decisions where only one or two dimensions are active. The $d_1$ price of groceries is a sufficient statistic for most grocery purchases, because the other dimensions are not activated.

The implication is that for *consequential* decisions -- business valuations, policy analysis, welfare assessment, institutional design -- scalar measures are structurally inadequate. They hide the information that makes these decisions difficult and important: which dimensions are at stake, where the boundaries lie, how the dimensions interact, and in which direction the economic state is moving.

The economic tensor makes this information explicit. It does not replace judgment with calculation -- you still need to decide how to weigh the dimensions against each other. But it ensures that the dimensions are visible, so that the judgment is made with full information rather than with eight-ninths of the information destroyed.

Maria's coffee shop is worth $200,000 on $d_1$. On the full manifold, it is something richer and more complex: a configuration of monetary value, contractual rights, fairness relationships, autonomy constraints, trust networks, community anchoring, personal identity, institutional standing, and epistemic uncertainty that no single number can capture, and that no single number should be asked to.

---

## Technical Appendix

### Brouwer's Invariance of Dimension

**[Established Mathematics.]** Brouwer's theorem (1911) states that $\mathbb{R}^m$ and $\mathbb{R}^n$ are homeomorphic if and only if $m = n$. Equivalently: there is no continuous bijection between Euclidean spaces of different dimensions. This is the topological foundation of the Scalar Irrecoverability Theorem.

The theorem is non-trivial (Cantor showed that $\mathbb{R}^m$ and $\mathbb{R}^n$ have the same cardinality for all $m, n$, so *bijections* exist -- they just cannot be continuous) and requires algebraic topology for its proof (typically via singular homology or the Borsuk-Ulam theorem).

### The Rank-Nullity Argument

**[Established Mathematics.]** For differentiable $\phi: \mathbb{R}^9 \to \mathbb{R}$, the derivative $d\phi_x: \mathbb{R}^9 \to \mathbb{R}$ is a linear map with rank $\leq 1$ and kernel dimension $\geq 8$ at every point $x$. By the inverse function theorem, $\phi$ cannot be locally injective at any regular point (where the rank is 1), because the kernel is non-trivial. At critical points (where the rank is 0), $\phi$ is constant to first order.

This means that every level set $\phi^{-1}(c)$ is either empty or has dimension $\geq 8$ in a neighborhood of any regular point. The pre-image of the appraiser's $200K figure is an eight-dimensional surface in the nine-dimensional attribute space -- a vast family of businesses that all produce the same cash flow but differ on every other dimension.

### Tensor Contraction in Index Notation

**[Established Mathematics.]** A rank-2 tensor $T_{ij}$ in $n$ dimensions has $n^2$ independent components (or $n(n+1)/2$ if symmetric). The contraction $T_{i}^{i} = \sum_i T_{ii}$ produces a scalar -- the *trace*. For the 9-dimensional economic tensor:

- The full tensor $T_{ij}$ has 81 components (45 independent if symmetric), encoding all pairwise interactions between the nine economic dimensions.
- GDP is the $(1,1)$ component: $T_{11}$ (or more precisely, the trace of $T$ restricted to the $d_1$ subspace).
- The trace $\text{tr}(T) = \sum_{i=1}^{9} T_{ii}$ would be a "total economic activity" scalar that at least includes the diagonal contributions from all nine dimensions -- a strictly more informative summary than $T_{11}$ alone, though still lossy (it discards the 36 independent off-diagonal components).

The hierarchy of summaries, from most informative to least:

| Representation | Components | Information retained |
|---------------|------------|---------------------|
| Full tensor $T_{ij}$ | 45 (symmetric) | Complete |
| Diagonal vector $(T_{11}, \ldots, T_{99})$ | 9 | Marginal changes per dimension |
| Trace $\text{tr}(T)$ | 1 | Total activity (all dimensions) |
| GDP = $T_{11}$ | 1 | Monetary activity only |

Each step down the hierarchy destroys information that cannot be recovered from the lower representation. The Scalar Irrecoverability Theorem is the formal statement that the bottom two rows are separated from the top two by an unbridgeable mathematical gap.

### Connection to Sen's Capability Approach

**[Modeling Axiom.]** Amartya Sen's capability approach (1999) argues that welfare should be evaluated not as scalar utility but as a vector of *capabilities* -- substantive freedoms to achieve various "functionings." Sen's capabilities correspond to dimensions of the decision manifold: $d_4$ (autonomy/freedom), $d_1$ (material capability), $d_9$ (epistemic capability -- the ability to make informed choices).

The Scalar Irrecoverability Theorem provides the mathematical backbone that Sen's approach lacked: it *proves* that the dimensional collapse Sen warned against is not merely inadequate but *mathematically irreversible*. Sen argued qualitatively that scalar measures miss important aspects of welfare. The theorem shows quantitatively that no scalar measure, however carefully constructed, can avoid missing them.

---

## Notes on Sources

The Scalar Irrecoverability Theorem is the economic application of a general topological result (Brouwer, 1911). The specific formulation for economic attribute vectors, including the three-part structure (non-injectivity, irrecoverability, path divergence) and the application to prospect-theoretic paradoxes, is original to Bond (2026b), *Geometric Ethics*, Chapter 15, here adapted for the economic context.

The Allais paradox is from Allais (1953), "Le Comportement de l'Homme Rationnel devant le Risque," *Econometrica*. The Ellsberg paradox is from Ellsberg (1961), "Risk, Ambiguity, and the Savage Axioms," *Quarterly Journal of Economics*. The interpretation as dimensional-activation effects rather than axiom violations is original to this framework.

The projected intransitivity result connects to Tversky (1969), "Intransitivity of Preferences," *Psychological Review*, and the experimental literature on context-dependent choice. The geometric reinterpretation -- intransitivity as projection artifact -- is original to this framework.

The tensor formulation of economic quantities, including the identification of GDP as a specific contraction, draws on the mathematical apparatus of differential geometry (see Lee, 2012, *Introduction to Smooth Manifolds*) applied to economic decision theory. The distinction between transferable and evaluative dimensions is original to this framework and formalizes intuitions present in Sen (1999), *Development as Freedom*, and Sandel (2012), *What Money Can't Buy*.

The Stiglitz-Sen-Fitoussi critique of GDP is developed in their (2009) report, *Mismeasuring Our Lives: Why GDP Doesn't Add Up*. Arrow's impossibility theorem is from Arrow (1951), *Social Choice and Individual Values*. The suggestion that the impossibility is an artifact of scalar aggregation is a conjecture of this framework, not yet fully proven.
