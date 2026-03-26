# Chapter 8: Market Symmetries and Gauge Invariance

> *"The universe is an enormous direct product of representations of symmetry groups."*
> -- Hermann Weyl, *Symmetry* (1952)

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria is pricing her signature latte. She charges $5.50. A tourist from Berlin glances at the chalkboard, converts mentally, and thinks: "About €5.10 -- reasonable." A cryptocurrency enthusiast opens his phone: "0.000088 BTC -- sure." A local regular doesn't convert at all: "Five-fifty, same as last week."*
>
> *Three descriptions of the same economic state. Three different labels for the same cup of coffee. The latte is the same latte. The decision to buy or not should be the same decision. If a customer would buy at $5.50 but refuse at €5.10 -- for the same coffee, at the same real cost -- something has gone wrong. Not with the coffee, but with the customer's evaluation.*
>
> *This chapter is about what "going wrong" means mathematically. The evaluation should be invariant under the relabeling. When it isn't, we have a gauge violation -- a crack in the rationality of the economic agent, measurable, quantifiable, and (in principle) correctable.*

---

## The Principle That Prices Should Not Matter

The previous chapters built a decision manifold, equipped it with a metric, showed that prices are heuristic fields on that manifold, proved that scalar compression destroys irrecoverable information, and constructed the Bond Geodesic Equilibrium. Throughout, one assumption has been implicit: the framework should not depend on how we describe things.

This chapter makes the assumption explicit. It identifies the symmetry group of the economic decision manifold -- the set of transformations that change the *description* of an economic state without changing the state itself -- and investigates what happens when economic agents violate the invariance that the symmetry demands.

The result is a precise geometric account of some of the most persistent puzzles in behavioral economics: money illusion, sunk cost fallacy, currency effects, and denomination effects. These are not separate biases to be catalogued. They are manifestations of a single geometric phenomenon: *gauge symmetry breaking* on the economic decision manifold.

## 8.1 The Bond Invariance Principle for Economics

The Bond Invariance Principle (BIP), developed in *Geometric Reasoning* (Bond, 2026c) and applied to ethics in *Geometric Ethics* (Bond, 2026), states that evaluations must be invariant under meaning-preserving transformations. The principle is domain-general: in ethics, it requires that moral judgments not change under morally irrelevant re-descriptions of the scenario; in law, it requires that legal outcomes not depend on protected characteristics; in cognition, it requires that reasoning be invariant under representational format.

In economics, the BIP takes a specific and powerful form.

> **Definition 34 (Economic Bond Invariance Principle).** An economic evaluation function $J: \mathcal{E} \to \mathbb{R}^k$ satisfies the *economic BIP* if, for every meaning-preserving transformation $\tau$ of the economic description:
>
> $$J(\tau(x)) = J(x)$$
>
> where "meaning-preserving" means that $\tau$ changes the labels, units, or accounting conventions used to describe the economic state $x$ without changing the underlying economic reality.

What counts as "meaning-preserving" in economics? Three classes of transformations are immediately apparent:

1. **Currency relabeling**: expressing the same monetary value in dollars, euros, yen, or bitcoin. The transformation $\tau_{\text{currency}}: d_1 \mapsto \alpha \cdot d_1$ (where $\alpha$ is the exchange rate) changes the numerical label on the monetary dimension without changing the purchasing power.

2. **Unit scaling**: expressing the same quantity in different units -- ounces vs. grams, barrels vs. liters, hourly wage vs. annual salary. The transformation $\tau_{\text{unit}}: d_k \mapsto \lambda_k \cdot d_k$ rescales dimension $k$ without changing the physical quantity.

3. **Numeraire choice**: expressing prices relative to different reference goods. When we say "a latte costs $5.50," we are expressing the latte's value relative to the dollar. We could equally express it as "a latte costs 1.1 sandwiches" or "a latte costs 0.55 hours of minimum-wage labor." The numeraire transformation $\tau_{\text{num}}$ permutes the role of which good serves as the measuring stick.

The economic BIP says: a rational economic evaluation must be invariant under all three. If your decision to buy Maria's latte changes when you express the price in euros instead of dollars -- at the same exchange rate, for the same coffee -- your evaluation violates the BIP. The decision is gauge-variant.

**[Modeling Axiom.]** The economic BIP is not a normative preference. It is a *consistency condition*. An agent whose evaluations depend on the currency label is making different decisions about the same economic state depending on how it is described. This is the economic analogue of an ethical agent whose moral judgment changes depending on whether a dilemma is described in English or Japanese -- not a difference of values, but a failure of invariance.

### The BIP and Classical Economics

Classical economics implicitly assumes the BIP -- indeed, it assumes a much stronger version. The Homo economicus model says that agents maximize expected utility, and expected utility is defined over *outcomes*, not descriptions. An outcome is a bundle of goods and services; the utility function $U(x_1, x_2, \ldots, x_n)$ takes the bundle as input, not the price labels attached to it. In this sense, classical economics is gauge-invariant by construction.

The problem is that *real economic agents* violate the BIP in systematic, predictable, and economically consequential ways. The violations are not random noise. They have geometric structure -- they are stronger along some dimensions than others, they interact with the metric in specific ways, and they can be measured using a gauge violation tensor. The rest of this chapter develops this structure.

## 8.2 The Economic Gauge Group

In physics, a gauge group is the group of transformations that leave the physical content of a theory invariant while changing the mathematical representation. In electromagnetism, the gauge group is $U(1)$: the electromagnetic potential can be shifted by any function of spacetime without changing the electric and magnetic fields. In general relativity, the gauge group is the diffeomorphism group: the physical content is invariant under smooth coordinate changes.

In economics, the gauge group captures the transformations that change the *description* of economic states without changing the states themselves.

> **Definition 35 (Economic Gauge Group).** The *economic gauge group* $\mathcal{G}$ is:
>
> $$\mathcal{G} = \mathbb{R}^+ \times S_n$$
>
> where:
>
> - $\mathbb{R}^+$ is the multiplicative group of positive reals, acting by *scaling*: for any $\lambda > 0$, the transformation $\sigma_\lambda: d_1 \mapsto \lambda \cdot d_1$ rescales the monetary dimension. This includes currency conversion ($\lambda$ = exchange rate), inflation adjustment ($\lambda$ = price index ratio), and unit changes ($\lambda$ = conversion factor).
>
> - $S_n$ is the symmetric group on $n$ elements, acting by *relabeling*: for any permutation $\pi \in S_n$, the transformation $\rho_\pi$ permutes the roles of $n$ goods as potential numeraires. If we have three goods (coffee, sandwiches, labor-hours), $S_3$ permutes which one serves as the measuring unit.

The gauge group acts on the attribute vector $\mathbf{a} \in \mathbb{R}^9$ primarily through the monetary dimension $d_1$, but the action extends to all transferable dimensions ($d_1$--$d_4$) that have quantitative units. The evaluative dimensions ($d_5$--$d_9$) are invariant under the gauge group -- trust, identity, and community impact do not have units that can be rescaled.

> **Remark 36 (Structure of the Gauge Group).** The economic gauge group $\mathcal{G} = \mathbb{R}^+ \times S_n$ is a semidirect product when the scaling and relabeling interact. In the simplest case, where scaling applies uniformly to all monetary quantities and relabeling permutes the numeraire independently, the group is a direct product. The full structure depends on the number of commodities and the complexity of the accounting system. For most applications in this book, we work with the direct product $\mathbb{R}^+ \times S_n$ and note where the semidirect structure matters.

### Comparison with Other Domain Gauge Groups

The economic gauge group is structurally different from the gauge groups of other domains in the geometric series:

| Domain | Gauge Group | Generator | What It Permutes |
|---|---|---|---|
| Ethics | $D_4 \times U(1)_H$ | Hohfeldian symmetries + harm phase | Rights-duty pairs, harm conservation |
| Economics | $\mathbb{R}^+ \times S_n$ | Scaling + relabeling | Currency units, numeraire choice |
| Law | $D_4$ | Hohfeldian symmetries | Jural relations |
| Communication | Translation gauge | Language mapping | Natural languages |

The ethics gauge group is discrete ($D_4$ is finite); the economics gauge group is continuous ($\mathbb{R}^+$ is a connected Lie group). This difference has consequences: continuous gauge symmetries produce *conservation laws* via Noether's theorem (Chapter 9), while discrete symmetries produce selection rules. The economic gauge group's continuous component is what makes economic conservation laws possible.

## 8.3 Gauge Invariance of the Metric

The economic metric must be invariant under the gauge group. If it were not, the cost of an economic action would depend on the units used to describe it -- which would be absurd.

> **Theorem 37 (Gauge Invariance of the Economic Metric).** *The Mahalanobis metric on the economic decision complex is invariant under the economic gauge group $\mathcal{G} = \mathbb{R}^+ \times S_n$:*
>
> $$w(\sigma_\lambda(v_i), \sigma_\lambda(v_j)) = w(v_i, v_j)$$
>
> *for all $\lambda \in \mathbb{R}^+$ and all vertices $v_i, v_j \in \mathcal{E}$, where $\sigma_\lambda$ acts on the attribute vectors by scaling the monetary dimension.*

> *Proof.* The edge weight is $w(v_i, v_j) = \Delta\mathbf{a}^T \Sigma^{-1} \Delta\mathbf{a} + \sum_k \beta_k \cdot \mathbf{1}[\text{boundary } k \text{ crossed}]$. Under the scaling $\sigma_\lambda$, the monetary component of the attribute vector changes as $d_1 \mapsto \lambda \cdot d_1$, so the monetary component of $\Delta\mathbf{a}$ changes as $\Delta d_1 \mapsto \lambda \cdot \Delta d_1$. But the covariance matrix $\Sigma$ transforms as $\Sigma_{11} \mapsto \lambda^2 \Sigma_{11}$ (the variance of a scaled random variable scales quadratically), so $\Sigma^{-1}_{11} \mapsto \lambda^{-2} \Sigma^{-1}_{11}$. The contribution to the Mahalanobis distance from the monetary dimension is:
>
> $$\frac{(\lambda \cdot \Delta d_1)^2}{\lambda^2 \cdot \sigma_1^2} = \frac{(\Delta d_1)^2}{\sigma_1^2}$$
>
> which is invariant. The off-diagonal terms $\Sigma_{1k}$ for $k > 1$ scale as $\lambda \cdot \Sigma_{1k}$ (covariance of a scaled with an unscaled variable), and the corresponding $\Delta\mathbf{a}$ components provide the compensating factor. The boundary penalties $\beta_k$ depend on the underlying economic state, not on the description, so they are gauge-invariant by definition. $\square$

The theorem confirms that the geometric framework is internally consistent: the cost of a decision, measured on the full manifold, does not depend on which currency you use to describe it. This is the *manifold* being gauge-invariant. The violations we study in the rest of this chapter are violations of gauge invariance in the *heuristic* -- in the System 1 assessment that guides actual human economic behavior.

## 8.4 Money Illusion as Gauge Violation

The most celebrated gauge violation in economics has a name: *money illusion*.

Money illusion is the tendency to think in terms of nominal values (the number on the price tag) rather than real values (what the number actually buys). When inflation runs at 3% and your salary increases by 2%, you are experiencing a real wage *cut* of approximately 1%. But it *feels* like a raise, because the number on the paycheck is bigger. The nominal description has changed ($\tau: d_1 \mapsto 1.02 \cdot d_1$); the real economic state has worsened; but the evaluation has improved. This is a gauge violation: the evaluation $J$ depends on the description $\tau(x)$, not on the state $x$.

> **Theorem 38 (Money Illusion as Gauge Violation).** *Money illusion is a violation of the economic BIP under the scaling subgroup $\mathbb{R}^+ \subset \mathcal{G}$. Specifically, for an agent with heuristic function $h(n)$:*
>
> $$h(\sigma_\lambda(n)) \neq h(n) \quad \text{when } \lambda \neq 1$$
>
> *even though $\sigma_\lambda(n)$ and $n$ represent the same real economic state (because the scaling is offset by a corresponding change in the price level). The manifold cost $w$ is gauge-invariant (Theorem 37), but the heuristic $h$ is not. The agent's System 1 responds to the nominal label rather than the real state.*

This theorem formalizes a distinction that Chapter 4 introduced for framing effects: the manifold is gauge-invariant; the heuristic may not be. Loss aversion is a structural feature of the manifold (losses genuinely traverse more dimensions). Money illusion is a heuristic miscalibration (the heuristic responds to labels, not states). The geometric framework distinguishes the two precisely.

### Experimental Evidence

The empirical evidence for money illusion is extensive:

**Shafir, Diamond, and Tversky (1997)** presented subjects with two scenarios:

*Scenario A:* You receive a 2% salary increase in a year with 4% inflation (real wage: -2%).

*Scenario B:* You receive a 1% salary decrease in a year with 0% inflation (real wage: -1%).

Subjects rated Scenario A as better, despite Scenario B being superior in real terms. The evaluation was based on the nominal change ($+2\%$ vs. $-1\%$), not the real change ($-2\%$ vs. $-1\%$). The gauge transformation $\sigma_{1.04}$ (inflation) changed the description; the evaluation followed the description rather than the state.

**Fehr and Tyran (2001)** demonstrated money illusion in experimental markets. After a nominal shock (the money supply was reduced), subjects took significantly longer to adjust prices to the new equilibrium when thinking in nominal terms, even though the real equilibrium was unchanged. The gauge transformation was a rescaling of the monetary unit; the adjustment friction measured the degree of gauge violation.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria's neighborhood has a mix of long-term residents and newcomers. The long-term residents remember when a latte cost $3.50; they see $5.50 as expensive. The newcomers, arriving from Manhattan where lattes cost $7.00, see $5.50 as a bargain. Same latte. Same real cost (measured by the fraction of median neighborhood income required to buy it). Different evaluations -- because the reference nominal price differs.*
>
> *This is a gauge violation on the time dimension of the scaling group: the long-term residents are evaluating the latte against the nominal anchor of $3.50, while the newcomers evaluate against $7.00. Neither group is evaluating the real cost of the latte relative to their current purchasing power -- they are responding to the nominal gap between the current price and their reference price.*
>
> *Maria's pricing decision must account for this gauge violation in her customer base. If she raises the price to $6.00, the long-term residents experience it as a $2.50 increase from the remembered baseline (71% markup); the newcomers experience it as a continued $1.00 discount from the Manhattan baseline (14% savings). Same fifty-cent increase, two different gauge frames, two different psychological responses. Rational pricing on the manifold must account for the gauge-variant heuristics of the agents she serves.*

---

## 8.5 Sunk Cost Fallacy as Path-Dependence Violating Re-description Invariance

The sunk cost fallacy -- continuing an endeavor because of previously invested resources that cannot be recovered -- is one of the most robust findings in behavioral economics. The standard account is straightforward: sunk costs are irrelevant to future decisions because they cannot be changed. A rational agent evaluates only the marginal cost and benefit of continuing versus stopping.

The geometric account goes deeper. The sunk cost fallacy is a violation of *re-description invariance* -- a specific form of gauge breaking where the evaluation depends on the *path* by which the current state was reached, even though the current state is the same regardless of the path.

> **Definition 39 (Re-description Invariance).** An economic evaluation function $J$ satisfies *re-description invariance* if the evaluation of a current state $x$ does not depend on the path $\gamma$ by which $x$ was reached:
>
> $$J(x; \gamma_1) = J(x; \gamma_2)$$
>
> for all paths $\gamma_1, \gamma_2$ that terminate at $x$.

Re-description invariance is a gauge condition: the "description" that must be stripped away is the history of how you got here. Two agents standing at the same point on the decision manifold -- same wealth, same opportunities, same constraints -- should evaluate future actions identically, regardless of whether one arrived at that point through a series of profitable investments and the other through a series of losses that happened to cancel out.

The sunk cost fallacy violates this condition. An agent who has invested $100,000 in a project that is now worth $50,000 evaluates "continue vs. abandon" differently from an agent who starts fresh at the $50,000 point -- even though the future costs and benefits are identical. The $100,000 already spent is not part of the current state; it is part of the *path* to the current state. The evaluation depends on the path, not the state. This is gauge-variant.

> **Theorem 40 (Sunk Cost as Gauge Violation).** *The sunk cost fallacy is a violation of re-description invariance under the path history transformation. Specifically, for an agent with path-dependent heuristic $h(n; \gamma)$:*
>
> $$h(n; \gamma_{\text{invested}}) \neq h(n; \gamma_{\text{fresh}})$$
>
> *even when $\gamma_{\text{invested}}$ and $\gamma_{\text{fresh}}$ terminate at the same state $n$. The agent's System 1 assessment incorporates the sunk cost into the heuristic estimate, inflating the perceived cost of abandoning the project (because abandonment would "waste" the sunk investment) and deflating the perceived cost of continuing (because the investment has already been "committed").*

> *Proof.* Let $x$ be the current economic state and let $c_s$ be the sunk cost (already expended, irrecoverable). The future-only evaluation of continuing is $J_{\text{continue}}(x) = w(x, x_{\text{continue}})$, and the future-only evaluation of abandoning is $J_{\text{abandon}}(x) = w(x, x_{\text{abandon}})$. These depend only on the current state $x$ and the future states -- they are gauge-invariant.
>
> The sunk-cost-laden evaluation modifies the abandonment cost:
>
> $$\tilde{J}_{\text{abandon}}(x; c_s) = w(x, x_{\text{abandon}}) + \phi(c_s)$$
>
> where $\phi(c_s) > 0$ is an increasing function of the sunk cost. This additional term has no counterpart in the manifold structure -- it is a heuristic artifact that makes abandonment seem more costly when more has been invested. Since $\phi(c_s)$ depends on the path history (the amount previously invested), the evaluation $\tilde{J}$ is path-dependent and violates re-description invariance. $\square$

### Why the Sunk Cost Fallacy Is Geometrically Distinct from Money Illusion

Both money illusion and sunk cost are gauge violations, but they violate different subgroups of the gauge group:

- **Money illusion** violates the *scaling* subgroup $\mathbb{R}^+$: the evaluation responds to the nominal magnitude rather than the real magnitude.

- **Sunk cost** violates *re-description invariance* under path history: the evaluation responds to the historical path rather than the current state.

The geometric framework distinguishes them because they occupy different positions in the gauge violation tensor (Section 8.7). Money illusion is a diagonal component (scaling self-interaction); sunk cost is an off-diagonal component (path-state cross-interaction). Different violations, different signatures, different remedies.

### The Sunk Cost Fallacy in Practice

The sunk cost fallacy is ubiquitous:

**The Concorde fallacy.** The British and French governments continued funding the Concorde supersonic jet long after it was clear the project would never be commercially viable, because of the billions already invested. The future-only evaluation (abandon and save the remaining budget) was dominated by the path-dependent evaluation (we cannot "waste" what we have already spent).

**Escalation of commitment.** Staw (1976) demonstrated that business school students allocated more resources to a failing division when told they had been personally responsible for the initial investment, compared to students told that someone else had made the initial decision. Same current state, different path history, different evaluation. Gauge violation.

**Consumer behavior.** Arkes and Blumer (1985) showed that people who had paid more for theater tickets were more likely to attend a performance they no longer wanted to see. The sunk cost (ticket price) influenced the consumption decision (attend or skip), even though the ticket price was the same regardless of attendance.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria spent $15,000 on a high-end espresso machine two years ago. The machine is now unreliable -- the repair costs are $300/month, and a new machine would cost $8,000 but would be more efficient and reliable. The future-only analysis is clear: the $300/month repair cost exceeds the amortized cost of a new machine ($8,000 over 5 years = $133/month), plus the new machine saves on energy costs and reduces customer wait times.*
>
> *But Maria hesitates. "I just paid $15,000 for this machine. I can't throw it away after two years." The $15,000 is sunk -- it is gone regardless of her decision. The gauge-invariant evaluation compares only the future costs: $300/month in repairs versus $133/month for the new machine. The sunk-cost-laden evaluation adds the "waste" of the $15,000 to the cost of replacement, making replacement seem $15,000 more expensive than it actually is.*
>
> *Maria's heuristic $h(n)$ is path-dependent: it evaluates the "replace the machine" path as more costly because of the historical investment in the current machine. This is a gauge violation -- the same future economic state evaluated differently depending on the path by which Maria arrived at the current decision point.*

---

## 8.6 Other Gauge Violations in Economic Behavior

Money illusion and sunk cost are the most studied gauge violations, but they are not the only ones. The gauge group $\mathcal{G} = \mathbb{R}^+ \times S_n$ admits violations along each of its generators, and real economic agents violate most of them.

### Denomination Effects

Raghubir and Srivastava (2009) demonstrated the *denomination effect*: people spend more freely when a given sum is in small denominations than when it is in a single large denomination. A person given four $5 bills spends more than a person given one $20 bill. The real economic state is identical ($20 of purchasing power). The description differs (four pieces of paper vs. one piece of paper). The evaluation differs. Gauge violation.

Geometrically, the denomination effect is a violation under the scaling subgroup applied to the *granularity* of the monetary representation. The gauge transformation $\tau: \{4 \times \$5\} \mapsto \{1 \times \$20\}$ is meaning-preserving (same total purchasing power), but the heuristic $h$ assigns different costs to spending from the two representations. The small-denomination representation has lower heuristic *spending cost* -- because breaking a large bill triggers a psychological "payment pain" boundary that spending small bills does not.

In the manifold formalism:

$$h(n; \text{four fives}) < h(n; \text{one twenty})$$

for the same spending action $n$. The manifold cost $w$ is identical; the heuristic diverges. The gauge violation tensor captures this as a non-zero component along the denomination-scaling axis.

### Currency Effects in International Trade

Firms making international pricing decisions exhibit currency effects: the same real price elicits different demand depending on the currency in which it is expressed. Wertenbroch, Soman, and Chattopadhyay (2007) found that consumers in cross-border shopping situations systematically underspend in foreign currencies they perceive as "strong" (each unit buys more) and overspend in currencies they perceive as "weak" (each unit buys less), even after controlling for exchange rates and purchasing power parity.

This is a violation of the relabeling subgroup $S_n$ of the gauge group. The currency label is a gauge choice; the real purchasing power is the gauge-invariant quantity. When agents respond to the label rather than the invariant, the BIP is violated.

### Accounting Frame Effects

Thaler's (1985) mental accounting research demonstrated that people categorize money into different "accounts" -- housing money, food money, entertainment money -- and exhibit different spending behavior depending on which account a windfall is assigned to. A $500 tax refund assigned to "savings" is treated differently from $500 found in a coat pocket, which is assigned to "free money." The real economic state is identical (net worth increased by $500). The accounting frame differs. The evaluation differs. Gauge violation.

In the language of the gauge group, mental accounting is a violation under the *partition* subgroup of $S_n$: the permutation group permutes not just the numeraire but the *categories* into which monetary value is sorted. The gauge-invariant quantity is total net worth; the gauge-variant behavior is differential treatment of identical values based on categorical assignment.

### The Gauge Violation Taxonomy

We can now organize the gauge violations systematically:

| Gauge Violation | Subgroup Violated | Description Changes | Economic Consequence |
|---|---|---|---|
| Money illusion | $\mathbb{R}^+$ (scaling) | Nominal vs. real | Wage rigidity, price stickiness |
| Sunk cost fallacy | Path history | History vs. current state | Escalation of commitment |
| Denomination effect | $\mathbb{R}^+$ (granularity) | Bill composition | Spending pattern distortion |
| Currency effect | $S_n$ (relabeling) | Currency label | Trade flow distortion |
| Mental accounting | $S_n$ (partition) | Account category | Spending category rigidity |
| Numeraire illusion | $S_n$ (numeraire) | Reference good | Relative price misjudgment |

Each row is a different component of the gauge violation tensor. Each has a distinct geometric signature. Each requires a different correction.

## 8.7 The Gauge Violation Tensor

To make gauge violations measurable, we need a mathematical object that captures both the *type* and *magnitude* of the violation. In physics, gauge violation is measured by the failure of a field to transform correctly under the gauge group. In economics, we define the analogous object.

> **Definition 41 (Economic Gauge Violation Tensor).** For an agent with heuristic function $h$ and a gauge transformation $\tau \in \mathcal{G}$, the *gauge violation tensor* $V$ is defined by:
>
> $$V_{\tau}(n) = h(\tau(n)) - h(n)$$
>
> For a family of gauge transformations $\{\tau_i\}$ and a family of economic states $\{n_j\}$, the full gauge violation tensor is:
>
> $$V_{ij} = h(\tau_i(n_j)) - h(n_j)$$
>
> A gauge-invariant heuristic has $V_{ij} = 0$ for all $i, j$. The Frobenius norm $\|V\| = \sqrt{\sum_{ij} V_{ij}^2}$ measures the total magnitude of gauge violation.

The gauge violation tensor is a direct analogue of the object defined in *Geometric Reasoning* (Bond, 2026c, Ch. 8) and applied to ethics in *Geometric Ethics* (Bond, 2026, Ch. 17). In ethics, the gauge violation tensor measures the degree to which moral judgments change under morally irrelevant re-descriptions (e.g., switching the language of the dilemma, swapping the gender of the characters). In economics, it measures the degree to which economic evaluations change under economically irrelevant re-descriptions (e.g., switching the currency, relabeling the accounts).

### Properties of the Gauge Violation Tensor

> **Proposition 42 (Properties of $V$).**
>
> 1. *$V$ is antisymmetric under inverse transformations: $V_{\tau^{-1}}(n) = -V_{\tau}(\tau^{-1}(n))$.*
>
> 2. *For composable transformations, $V_{\tau_1 \circ \tau_2}(n) = V_{\tau_1}(\tau_2(n)) + V_{\tau_2}(n)$. The gauge violation of a composed transformation is the sum of the violations along the composition path. This is the "cocycle condition" -- it says that gauge violations accumulate along chains of transformations.*
>
> 3. *The trace of $V$ over gauge transformations, $\text{tr}_\tau(V) = \sum_i V_{\tau_i}(n)$, measures the total directional bias of the heuristic: whether it systematically over- or underestimates when descriptions change.*

> *Proof.* (1) If $h(\tau(n)) - h(n) = V_\tau(n)$, then $h(\tau^{-1}(\tau(n))) - h(\tau(n)) = h(n) - h(\tau(n)) = -V_\tau(n) = V_{\tau^{-1}}(\tau(n))$. Substituting $m = \tau^{-1}(n)$ gives $V_{\tau^{-1}}(m) = -V_\tau(\tau(m)) = -V_\tau(\tau(\tau^{-1}(n)))$, which requires $m = \tau^{-1}(n)$. (2) $V_{\tau_1 \circ \tau_2}(n) = h(\tau_1(\tau_2(n))) - h(n) = [h(\tau_1(\tau_2(n))) - h(\tau_2(n))] + [h(\tau_2(n)) - h(n)] = V_{\tau_1}(\tau_2(n)) + V_{\tau_2}(n)$. (3) By definition. $\square$

The cocycle condition in property (2) is particularly important. It says that if you convert dollars to euros (violation $V_1$), then convert euros to yen (violation $V_2$), the total violation equals the violation of converting dollars directly to yen ($V_{12}$) only if the violations are "consistent." When they are not -- when converting $\to€\to$¥ produces a different evaluation than converting $\to$¥ -- the agent's gauge violations form a non-trivial cohomology class. This is the economic analogue of holonomy: the evaluation picks up a "rotation" as it is parallel-transported around a loop of currency conversions.

### Measuring the Gauge Violation Tensor

The gauge violation tensor is empirically measurable. The measurement protocol mirrors the BIP experiments from *Geometric Ethics* (Bond, 2026, Ch. 17):

1. **Select a set of economic states** $\{n_j\}$ -- e.g., wage offers, prices, investment proposals.

2. **Select a set of gauge transformations** $\{\tau_i\}$ -- e.g., currency conversions, nominal-to-real adjustments, denomination changes.

3. **Present each state under each transformation** to the same subjects (within-subjects) or matched subjects (between-subjects).

4. **Record the evaluation** -- purchase decision, willingness to pay, satisfaction rating, negotiation behavior.

5. **Compute $V_{ij}$** as the difference in evaluation between the transformed and original descriptions.

6. **Test $H_0: V_{ij} = 0$** for each component. Significant departures indicate gauge violations.

The gauge violation tensor has been measured, though not under this name, in the studies cited throughout this section. Shafir, Diamond, and Tversky's (1997) money illusion experiment measures $V$ along the inflation-scaling axis. Raghubir and Srivastava's (2009) denomination experiment measures $V$ along the granularity-scaling axis. The geometric framework unifies these scattered measurements into a single mathematical object.

---

> **WORKED EXAMPLE: Measuring Money Illusion in a Wage Negotiation**
>
> *Consider a wage negotiation between Maria and a prospective employee, Alex. Maria offers Alex a salary. We measure the gauge violation tensor by presenting the same real salary under different nominal descriptions.*
>
> **Setup.** The real salary is $48,000/year in purchasing-power terms. We present it under three descriptions:
>
> | Description ($\tau_i$) | Nominal value | Framing |
> |---|---|---|
> | $\tau_0$: Baseline | $48,000/year | Annual salary |
> | $\tau_1$: Monthly | $4,000/month | Monthly salary |
> | $\tau_2$: Hourly | $23.08/hour | Hourly wage |
> | $\tau_3$: Post-inflation | $49,440/year (3% inflation) | Nominal raise from $48K |
>
> All four descriptions are gauge-equivalent: they represent the same real purchasing power ($\tau_0 = \tau_1 = \tau_2$ by unit conversion; $\tau_3 = \tau_0$ by inflation adjustment).
>
> **Measurement.** We present each description to a separate group of 100 subjects and ask: "How attractive is this job offer?" on a 1-10 scale. Hypothetical results (consistent with the existing literature):
>
> | Description | Mean attractiveness $\pm$ SE |
> |---|---|
> | $\tau_0$: $48,000/year | $6.2 \pm 0.3$ |
> | $\tau_1$: $4,000/month | $5.8 \pm 0.3$ |
> | $\tau_2$: $23.08/hour | $5.1 \pm 0.3$ |
> | $\tau_3$: $49,440/year (after 3% inflation) | $7.1 \pm 0.3$ |
>
> **Gauge violation tensor components:**
>
> $$V_{\tau_1, n} = 5.8 - 6.2 = -0.4 \quad \text{(monthly framing less attractive)}$$
> $$V_{\tau_2, n} = 5.1 - 6.2 = -1.1 \quad \text{(hourly framing substantially less attractive)}$$
> $$V_{\tau_3, n} = 7.1 - 6.2 = +0.9 \quad \text{(inflation-masked raise more attractive)}$$
>
> **Interpretation.** The gauge violation tensor is non-zero with distinct components:
>
> - The *unit scaling* violation ($V_{\tau_1}$, $V_{\tau_2}$) shows that smaller unit descriptions reduce perceived attractiveness. The hourly framing ($23.08) activates a different comparison set than the annual framing ($48,000) -- the small number triggers a "low wage" heuristic even though the annual equivalent is the same. The magnitude increases with the granularity of the unit ($|V_{\tau_2}| > |V_{\tau_1}|$), consistent with the denomination effect.
>
> - The *inflation scaling* violation ($V_{\tau_3}$) is money illusion in its purest form. A 3% nominal increase with 3% inflation is a zero real change, but the evaluation improves by 0.9 points. The heuristic responds to the nominal change ($+\$1,440$) rather than the real change ($\$0$).
>
> **Frobenius norm:** $\|V\| = \sqrt{0.4^2 + 1.1^2 + 0.9^2} = \sqrt{0.16 + 1.21 + 0.81} = \sqrt{2.18} \approx 1.48$
>
> This is the total magnitude of gauge violation in this negotiation context. A perfectly gauge-invariant agent would have $\|V\| = 0$. Maria, as an employer, should be aware that Alex's evaluation of the offer will vary by approximately 1.5 attractiveness points depending on how the same salary is described.
>
> **Practical implication:** If Maria wants to attract Alex, she should quote the annual salary ($\tau_0$ or $\tau_3$), not the hourly rate ($\tau_2$). If Maria wants Alex to accept a real wage cut, she should offer a nominal increase below the inflation rate ($\tau_3$). These are not deceptive strategies in the usual sense -- the real economic content is identical under all descriptions. They are gauge-frame selections that exploit the non-zero gauge violation tensor of the human heuristic.

---

## 8.8 The Geometry of Gauge Correction

If gauge violations are heuristic miscalibrations, they should be correctable. The geometric framework suggests a specific correction procedure: *gauge-fixing* the heuristic.

> **Definition 43 (Gauge-Fixed Heuristic).** A *gauge-fixed heuristic* $\hat{h}$ is constructed from a gauge-variant heuristic $h$ by averaging over the gauge group:
>
> $$\hat{h}(n) = \frac{1}{|\mathcal{G}_{\text{disc}}|} \sum_{\tau \in \mathcal{G}_{\text{disc}}} h(\tau(n))$$
>
> where $\mathcal{G}_{\text{disc}}$ is a finite discretization of the gauge group. For the continuous scaling subgroup $\mathbb{R}^+$, the average is taken over a representative set of scales (e.g., hourly, daily, monthly, annual).

The gauge-fixed heuristic has the property that $V_\tau(\hat{h}) \approx 0$ for all $\tau$ in the discretization -- the gauge violations cancel by averaging. This is the economic analogue of the physicist's gauge-fixing procedure, where a specific gauge is chosen to eliminate the redundancy. In economics, the "specific gauge" is the average across all reasonable descriptions.

### Practical Gauge Correction

In practice, gauge correction does not require averaging over the full gauge group. It requires:

1. **Awareness of the gauge frame.** Know which description you are using and what alternatives exist. When evaluating a salary, consider it in annual, monthly, and hourly terms. When evaluating a price, consider it in multiple currencies and relative to different baskets.

2. **Conversion to a canonical frame.** Pick one description and stick with it. For monetary evaluations, the canonical frame is *real* (inflation-adjusted) *annual* values. For international comparisons, the canonical frame is purchasing power parity (PPP).

3. **Suspicion of frame-dependent reactions.** When your evaluation changes under a gauge transformation, ask: has the underlying economic state changed, or just the description? If just the description, the changed evaluation is gauge artifact, not information.

This is the economic instantiation of the general debiasing strategy from *Geometric Reasoning* (Bond, 2026c, Ch. 14): heuristic augmentation. The heuristic $h$ is biased (gauge-variant); the correction is to augment it with gauge-awareness so that the augmented heuristic $\hat{h}$ is approximately gauge-invariant.

**[Empirical.]** Gauge correction is effective. Training programs that teach "think in real terms" reduce money illusion in experimental settings (Fehr and Tyran, 2001, Study 2). Financial literacy programs that teach unit conversion reduce denomination effects. The gauge violation tensor is not a fixed property of the human cognitive system; it is a heuristic calibration parameter that responds to training.

## 8.9 Gauge Invariance and Market Efficiency

The Efficient Market Hypothesis (EMH), in its strongest form, asserts that market prices reflect all available information. The geometric framework offers a precise restatement: *the market price heuristic is gauge-invariant*.

An efficient market is one where the price of an asset does not depend on the currency in which it is quoted (after exchange-rate adjustment), the denomination in which it is offered, or the accounting frame in which it is reported. Arbitrageurs enforce gauge invariance: when the price of a stock is $100 in New York and the equivalent of $101 in London (after exchange-rate conversion), arbitrageurs buy in New York and sell in London until the prices converge. The arbitrage trade is, literally, a gauge correction -- it eliminates the gauge violation in the price field.

> **Proposition 44 (Market Efficiency as Gauge Invariance).** *A market is efficient with respect to the gauge group $\mathcal{G}$ if and only if the price heuristic $h_{\text{price}}$ satisfies the BIP:*
>
> $$h_{\text{price}}(\tau(n)) = h_{\text{price}}(n) \quad \text{for all } \tau \in \mathcal{G}$$
>
> *Market inefficiency is a non-zero gauge violation tensor of the price field.*

This restatement has a useful consequence: different types of market inefficiency correspond to different components of the gauge violation tensor.

- **Purchasing power parity failures** (the Big Mac Index deviations) are violations of the scaling subgroup for international price comparisons.

- **Dual-listed stock price discrepancies** (the same company trading at different prices on different exchanges) are violations of the relabeling subgroup.

- **Closed-end fund discounts** (a fund trading below the sum of its holdings) are violations of the partition subgroup -- the market values the collection differently from the sum of its parts, which is a gauge violation under the "relabel the container" transformation.

Each class of inefficiency lives in a specific sector of the gauge violation tensor, and each calls for a specific arbitrage strategy -- a gauge correction that eliminates the specific violation.

## 8.10 When Gauge Violation Is Information

Not every apparent gauge violation is a genuine miscalibration. Sometimes the violation signals that the transformation $\tau$ was not actually meaning-preserving -- that the different descriptions carry genuinely different economic content.

> **Remark 45 (Gauge Violation as Information).** A non-zero gauge violation tensor $V_\tau(n) \neq 0$ can arise from two sources:
>
> 1. *Genuine gauge violation:* The agent's heuristic is miscalibrated; the evaluation should be invariant but is not. Correction is appropriate.
>
> 2. *Pseudo-gauge violation:* The transformation $\tau$ is not actually meaning-preserving; the different descriptions carry genuinely different information. The non-zero $V$ reflects real economic content, not miscalibration.

Example: if Maria's latte is priced at $5.50 in the U.S. and €5.10 in Germany, and a customer prefers the dollar price, this might be because:

**(a)** The customer is exhibiting money illusion (the number "5.10" seems cheaper than "5.50" even though the real cost is identical). This is genuine gauge violation.

**(b)** The customer is in the U.S., where the $5.50 price comes with a U.S. supply chain, U.S. labor standards, and U.S. food safety regulation. The dollar price and the euro price are not actually describing the same economic state -- they describe the same cup of coffee in different institutional contexts. The different evaluation reflects the different institutional context, not a gauge miscalibration.

Distinguishing (a) from (b) requires checking whether the transformation $\tau$ is truly meaning-preserving. This is the economic analogue of the distinction in *Geometric Ethics* between genuine moral invariance (the judgment should not change when you switch languages) and apparent invariance failure (the judgment changes because the different language activates different cultural norms that carry genuine moral information).

The gauge violation tensor does not distinguish between (a) and (b) automatically. It measures the *total* sensitivity of the evaluation to the description. The decomposition into genuine violation and pseudo-violation requires domain knowledge -- understanding which transformations are truly meaning-preserving in the specific economic context.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria recently started accepting Bitcoin for coffee. She displays a small screen showing the BTC price updated in real time. When Bitcoin's price spiked to $90,000, a customer paid 0.0000611 BTC for a $5.50 latte. The customer remarked: "Wow, that's basically free!" When Bitcoin dropped to $30,000, the same latte cost 0.000183 BTC, and a different customer hesitated: "That seems like a lot of Bitcoin for a latte."*
>
> *Both customers are exhibiting gauge violation. The latte costs $5.50 regardless of Bitcoin's price. The BTC denomination is a gauge transformation -- a relabeling of the same monetary value in different units. The first customer's evaluation ("basically free") responds to the small number (0.0000611); the second customer's evaluation ("a lot") responds to the larger number (0.000183). Neither is responding to the real cost.*
>
> *Maria observes this gauge violation daily. She noticed that customers tip more generously when paying in Bitcoin during price peaks (the small BTC amounts feel trivial) and less during dips (the larger BTC amounts feel substantial). The gauge violation tensor for Bitcoin tipping has a large component along the denomination-scaling axis.*
>
> *Maria's response is practical gauge correction: she prominently displays both the BTC price and the dollar equivalent. The dual display forces the customer's heuristic to process both gauge frames, reducing (though not eliminating) the gauge violation. The dual-display customers tip approximately the same regardless of Bitcoin's price. The single-display customers do not.*

---

## 8.11 Connections to the Broader Framework

### Gauge Invariance and Conservation (Preview of Chapter 9)

The continuous subgroup $\mathbb{R}^+$ of the economic gauge group is a one-parameter Lie group. By Noether's theorem, if the economic Lagrangian is invariant under $\mathbb{R}^+$, there exists a conserved quantity. Chapter 9 develops this connection in full: the gauge invariance of the metric under currency rescaling implies a conservation law for value under re-description. Value cannot be created or destroyed by relabeling -- only by real transformation. This is the economic analogue of energy conservation (invariance under time translation), momentum conservation (invariance under spatial translation), and harm conservation (invariance under moral re-description, from *Geometric Ethics*).

### Gauge Breaking and Market Failure (Preview of Chapter 10)

The gauge violations catalogued in this chapter are individual-level phenomena -- cognitive miscalibrations of individual heuristics. Chapter 10 shows that these individual violations aggregate into *market-level* pathologies. When enough agents exhibit money illusion, the market itself behaves as if prices are sticky -- wage and price adjustments lag behind inflation, creating real economic distortions. The individual gauge violation becomes a collective market failure. The gauge violation tensor of the market is the aggregation of the individual tensors, and its structure determines which market failures arise and how severe they are.

### The BIP as Rationality Constraint

The economic BIP is not a description of how agents *do* behave. It is a prescription for how they *should* behave -- a rationality constraint. An agent who satisfies the BIP makes decisions based on economic substance, not economic description. The BIP does not prescribe *what* the agent should want (that is determined by the metric -- the agent's values and trade-offs). It prescribes that *whatever* the agent wants, the pursuit should be invariant under re-description.

This is a weaker condition than utility maximization. A BIP-satisfying agent need not maximize any scalar function. They need only be *consistent* -- responding the same way to the same economic state regardless of how it is described. The BIP separates the question of *what* to optimize from the question of *consistency* in optimization. Classical economics bundled these together (rational = maximize expected utility). The geometric framework unbundles them (rational = gauge-invariant on whatever manifold the agent occupies).

## Technical Appendix: The Gauge Group as Lie Group

For readers with background in differential geometry, this section develops the mathematical structure of the economic gauge group in more detail.

The scaling subgroup $\mathbb{R}^+$ is a one-dimensional connected Lie group with Lie algebra $\mathfrak{g} = \mathbb{R}$. The exponential map is $\exp: \mathbb{R} \to \mathbb{R}^+$, $t \mapsto e^t$. A gauge field on the economic manifold is a connection on a principal $\mathbb{R}^+$-bundle over $\mathcal{E}$.

The curvature of this connection is the *field strength* -- the analogue of the electromagnetic field tensor in physics. A flat connection (zero curvature) means that parallel transport of monetary value around any closed loop returns the same value. A non-flat connection means that the "exchange rate" between two currencies depends on the path by which you convert between them -- which is exactly what happens when arbitrage opportunities exist.

> **Definition 46 (Economic Connection).** An *economic connection* $A$ on the principal $\mathbb{R}^+$-bundle over $\mathcal{E}$ assigns to each edge $(v_i, v_j)$ a gauge transformation $\tau_{ij} \in \mathbb{R}^+$ representing the "exchange rate" for monetary value along that edge. The curvature $F$ of the connection is defined on each 2-simplex $[v_i, v_j, v_k]$ as:
>
> $$F_{ijk} = \log(\tau_{ij} \cdot \tau_{jk} \cdot \tau_{ki})$$
>
> A flat connection has $F_{ijk} = 0$ for all triangles: converting $i \to j \to k \to i$ returns the same value. A non-flat connection has $F_{ijk} \neq 0$: arbitrage is possible.

In this language:

- **Arbitrage-free markets** have flat connections ($F = 0$). The absence of arbitrage is a geometric condition on the connection -- the principal bundle is flat.

- **Arbitrage opportunities** are non-zero curvature ($F \neq 0$). The fundamental theorem of asset pricing (Harrison and Kreps, 1979; Delbaen and Schachermayer, 1994) states that a market is arbitrage-free if and only if there exists an equivalent martingale measure. In geometric language: the market is arbitrage-free if and only if the economic connection is flat -- if and only if there exists a gauge in which all exchange rates are consistent.

- **Covered interest rate parity** (the condition that forward exchange rates and interest rate differentials must be consistent) is the condition that the curvature vanishes on the triangle (domestic currency, foreign currency, forward contract). Violations of covered interest parity -- which were observed during the 2008 financial crisis -- are non-zero curvature, geometrically identical to the breakdown of gauge invariance that Chapter 11 will analyze as a curvature singularity.

> **Proposition 47 (No-Arbitrage as Flat Connection).** *A market is arbitrage-free if and only if the economic connection on the $\mathbb{R}^+$-bundle is flat: $F = 0$ on every 2-simplex. Equivalently, the holonomy group of the connection is trivial: parallel transport around any closed loop is the identity.*

> *Proof.* An arbitrage opportunity is a sequence of trades $v_0 \to v_1 \to \cdots \to v_m = v_0$ (a closed loop) with positive net value: $\prod_{i=0}^{m-1} \tau_{i,i+1} > 1$. Taking logarithms, this is $\sum_{i=0}^{m-1} \log \tau_{i,i+1} > 0$. By Stokes' theorem on the simplicial complex, the sum around a closed loop equals the sum of curvatures over the triangles enclosed by the loop: $\sum_{\text{loop}} \log \tau = \sum_{\text{enclosed}} F$. If $F = 0$ everywhere, no loop has positive sum, so no arbitrage exists. Conversely, if $F \neq 0$ on some triangle, the loop around that triangle has non-zero sum, and traversing the loop in the profitable direction constitutes an arbitrage. $\square$

This is a striking result: the fundamental theorem of asset pricing -- one of the deepest results in mathematical finance -- is a flatness condition on a gauge connection. The geometric framework does not merely restate the theorem; it places it in a broader context. No-arbitrage is the financial market's version of gauge invariance: the value of an asset does not depend on the path by which you arrive at it. When it does -- when the connection has curvature -- arbitrageurs exploit the curvature until it vanishes, restoring gauge invariance. Arbitrage is gauge correction.

---

## Summary

This chapter established the symmetry structure of the economic decision manifold:

1. **The economic BIP** requires that evaluations be invariant under meaning-preserving transformations: currency relabeling, unit scaling, and numeraire choice.

2. **The economic gauge group** $\mathcal{G} = \mathbb{R}^+ \times S_n$ captures these transformations as a Lie group (scaling) times a finite group (relabeling).

3. **The economic metric is gauge-invariant** (Theorem 37): the cost of a decision does not depend on the units used to describe it. Gauge violations are heuristic miscalibrations, not manifold features.

4. **Money illusion** is a gauge violation under the scaling subgroup: the heuristic responds to nominal values rather than real values.

5. **Sunk cost fallacy** is a gauge violation under path-history re-description: the heuristic responds to the path taken rather than the current state.

6. **The gauge violation tensor** $V_{ij}$ quantifies the type and magnitude of gauge violations. It is empirically measurable using within-subject or between-subject experimental designs.

7. **Market efficiency is gauge invariance** of the price field. Different types of inefficiency correspond to different components of the gauge violation tensor, each exploitable by a specific arbitrage strategy.

8. **No-arbitrage is flat connection** on the $\mathbb{R}^+$-bundle: the fundamental theorem of asset pricing is a gauge-theoretic statement.

The next chapter takes the continuous symmetry identified here -- the $\mathbb{R}^+$ scaling invariance -- and applies Noether's theorem to derive conservation laws for the economic manifold.
