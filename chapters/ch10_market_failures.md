# Chapter 10: Market Failures as Geometric Pathologies

> *"The curious task of economics is to demonstrate to men how little they really know about what they imagine they can design."*
> — F. A. Hayek, *The Fatal Conceit* (1988)

*Part IV: Failure Modes*

---

> **RUNNING EXAMPLE — MARIA'S COFFEE SHOP**
>
> *Maria Esperanza's neighborhood is gentrifying, and everything is failing simultaneously. The price of commercial real estate does not reflect the community value her coffee shop creates — an externality, which is heuristic corruption on the price field. The zoning board has been captured by developers who optimize for tax revenue rather than neighborhood welfare — objective hijacking. Property values are in an unsustainable bubble, and everyone knows it but no one can exit the position — a local minimum. And the nominal property value increase of 200% masks a real community-value decline — gauge breaking, where nominal and real are confused.*
>
> *These are not four separate problems. They are four manifestations of the same geometric pathology: the market's search process has been derailed from the geodesic. This chapter catalogs how.*

---

## 10.1 The Four Pathologies

**[Modeling Axiom.]** *Geometric Reasoning* (Bond, 2026c, Chapters 5–8) established a taxonomy of four failure modes for any search process on a geometric manifold. These four pathologies are not specific to moral reasoning or AI systems — they are structural features of search on curved spaces with imperfect heuristics. This chapter instantiates them on the economic decision manifold.

| Pathology | General Form | Economic Instantiation |
|-----------|-------------|----------------------|
| Heuristic corruption | $\nabla h$ points away from geodesic | Externalities, information asymmetry |
| Objective hijacking | Search optimizes wrong objective | Regulatory capture, short-termism |
| Local minima | Search trapped in suboptimal basin | Bubbles, poverty traps |
| Gauge breaking | Output depends on description, not content | Money illusion, framing effects |

## 10.2 Heuristic Corruption: When Prices Lie

The price system is the economy's heuristic field (Chapter 5). When prices accurately reflect the full manifold cost of a transaction, the heuristic is admissible and the market's search process finds near-optimal paths. When prices fail to reflect true costs, the heuristic is corrupted and the search is misdirected.

### Externalities as Heuristic Corruption

**[Empirical.]** An externality exists when the price of a good does not include the full cost on the decision manifold. A factory that pollutes a river imposes costs on dimensions $d_6$ (social impact — downstream communities), $d_5$ (trust — breach of implicit social contract), and $d_8$ (legitimacy — violation of environmental norms). If these costs are not reflected in the factory's output price, the price heuristic $h(n)$ systematically underestimates the true cost-to-go from pollution-intensive production states.

The result is predictable: the market's A* search, guided by the corrupted heuristic, follows a trajectory that avoids the true geodesic (which would include pollution costs) and instead converges on a cheaper-seeming path that ignores dimensions $d_5$, $d_6$, and $d_8$. This is not market failure in the traditional sense — the market is functioning correctly *on the projected manifold*. It is a dimensional failure: the price heuristic operates on $d_1$ while the true cost lives on all nine dimensions.

**Pigouvian taxes** are heuristic corrections: they add a penalty to the price that approximates the missing manifold dimensions. A carbon tax adds $\Delta h(n) = \beta_{\text{climate}} \cdot \text{emissions}(n)$ to the price heuristic, partially restoring admissibility. The geometric framework explains why Pigouvian taxes are hard to calibrate: the correct penalty depends on the covariance matrix $\Sigma$ (how the missing dimensions interact with $d_1$), which varies across contexts and is difficult to estimate.

### Information Asymmetry as Heuristic Degradation

**[Empirical.]** Akerlof's market for lemons is a specific distortion of dimension $d_9$ (epistemic status). When buyers cannot observe product quality, their heuristic estimate $h(n)$ for the quality dimension is unreliable — it assigns average quality to all products, causing the price to reflect average rather than actual value.

On the decision manifold, this appears as a degenerate metric along the quality axis: the Mahalanobis distance between a high-quality and a low-quality product is small (because the buyer's $\Sigma$ has a large variance on $d_9$), even though the true distance is large. Good products are undervalued and bad products are overvalued. The geodesic on the true manifold (buy good products, avoid bad ones) differs from the geodesic on the perceived manifold (treat all products as average).

Market institutions — warranties, reputation systems, regulation, certification — function as *manifold calibration mechanisms*: they reduce the variance on $d_9$, tightening the metric along the quality axis and bringing the perceived manifold closer to the true one.

The geometric framework classifies information asymmetry into three progressively severe forms:

1. **Noise** ($\sigma_9$ large but unbiased): the buyer's estimate of quality varies around the true value. The heuristic is admissible in expectation but imprecise. Market institutions can calibrate by reducing $\sigma_9$. This is the case for most consumer goods where reviews, returns, and repeat purchase provide gradual calibration.

2. **Bias** ($\sigma_9$ large and systematically shifted): the buyer's estimate is consistently wrong in one direction. The used-car market is the canonical example: sellers know the quality and buyers do not, so buyers' estimates are biased downward (they assume average quality, which is below-average because good sellers exit). The heuristic is inadmissible — it systematically overestimates the cost of high-quality goods and underestimates the cost of low-quality ones.

3. **Corruption** ($d_9$ is actively manipulated): the seller deliberately distorts the buyer's epistemic state. Fraudulent advertising, deceptive labeling, and insider trading are not mere information asymmetries — they are active attacks on the buyer's manifold calibration. The heuristic is not merely inadmissible; it has been weaponized. The seller profits precisely by ensuring that the buyer's heuristic is maximally wrong.

The progression from noise to bias to corruption corresponds to increasing severity of heuristic failure — and, critically, to different policy remedies. Noise is addressed by information provision (reviews, disclosures). Bias is addressed by institutional design (warranties, reputation systems). Corruption is addressed by prohibition and enforcement (fraud law, securities regulation). The geometric framework predicts that policies designed for one level of severity will fail at another — disclosure requirements (effective against noise) will not stop deliberate fraud (corruption), and fraud enforcement (effective against corruption) is overkill for honest markets with simple noise.

### Moral Hazard as Manifold Decoupling

**[Empirical.]** Moral hazard — the tendency of insured agents to take greater risks because they do not bear the full cost — is a specific form of heuristic corruption where the agent's perceived manifold decouples from the true manifold.

Consider a bank with deposit insurance. On the bank's perceived manifold, the cost of risky lending ($d_1$ losses from loan defaults) is partially borne by the insurer, not the bank. The bank's effective edge weight for risky transitions is lower than the true edge weight. The bank's Bond geodesic — the path of least behavioral friction on its perceived manifold — therefore passes through regions that the true geodesic would avoid.

In the geometric framework, deposit insurance modifies the bank's covariance matrix $\Sigma_{\text{bank}}$ by reducing the variance weight on the risk dimension. The bank experiences a "flatter" manifold in the risk direction — transitions that involve more risk appear less costly — leading to a geodesic that is risk-seeking relative to the true manifold. The standard remedy (capital requirements, risk-based deposit insurance premiums) works by *restoring the curvature*: adding back the risk penalty that the insurance removed, so that the bank's perceived manifold more closely approximates the true one.

> **MARIA'S COFFEE SHOP — HEURISTIC CORRUPTION**
>
> *Maria experiences a mild form of heuristic corruption every time she checks the real estate listings. The listing prices — $1.2M, $1.8M, $2.5M for commercial spaces near hers — tell her the price heuristic on $d_1$. They tell her nothing about whether the spaces have community value ($d_6$), whether the landlords are trustworthy ($d_5$), or whether the neighborhoods have the social infrastructure that makes a coffee shop viable ($d_3$, $d_7$). Maria's System 1 unconsciously fills in these dimensions using the price as a proxy: "expensive neighborhood = good neighborhood." But the proxy is corrupted by gentrification dynamics: the neighborhoods with the highest prices may have the lowest community value, because the high prices reflect speculative demand, not social infrastructure. Maria's heuristic is inadmissible on the full manifold — and the inadmissibility is generated by the price system itself.*

## 10.3 Objective Hijacking: When the Optimizer Serves the Wrong Master

### Regulatory Capture

**[Empirical.]** Regulatory capture occurs when the regulator's objective function shifts from public welfare (the full manifold) to the regulated industry's preferences (a projected subspace). In the geometric framework, this is *objective hijacking*: the search is guided by a different objective than the one it was designed to optimize.

The captured regulator's decision manifold has been contracted: dimensions $d_3$ (fairness to the public), $d_6$ (social impact), and $d_8$ (institutional legitimacy) are suppressed, and the regulator's effective objective becomes alignment with $d_1$ interests of the regulated industry. The geodesic shifts from the public-welfare path to the industry-welfare path.

The geometric framework predicts that capture is easier when the public-welfare dimensions ($d_3$, $d_6$, $d_8$) are diffuse (many citizens each affected a little) and the industry dimensions ($d_1$) are concentrated (few firms each affected a lot). This is because concentrated interests produce steep gradients on the captured manifold, while diffuse interests produce flat gradients — the regulator's corrupted heuristic follows the steep gradient.

### Short-Termism

Quarterly earnings pressure is objective hijacking in the temporal dimension. The firm's true geodesic optimizes over the full temporal manifold — including long-term trust ($d_5$), institutional legitimacy ($d_8$), and social capital ($d_6$). The quarterly proxy contracts the optimization horizon, collapsing the temporal manifold to a single period and destroying the geodesic's long-term structure.

The geometric prediction: short-termism is most damaging for firms whose value depends heavily on evaluative dimensions ($d_5$–$d_9$) — technology companies (trust in data handling), financial institutions (trust in solvency), and community-serving businesses like Maria's coffee shop. For commodity producers whose value is primarily $d_1$, short-term optimization is less distortionary because the relevant manifold is closer to the scalar projection.

**Theorem 10.1 (Temporal Hijacking and Evaluative Erosion).** *Let $V_E(t) = \sum_{k=5}^{9} d_k(t)$ be the total evaluative value at time $t$. A firm optimizing $d_1$ on a single-period horizon will, if the off-diagonal covariance terms between $d_1$ and $d_5$–$d_9$ are positive, deplete $V_E$ over time:*

$$\frac{dV_E}{dt} < 0 \quad \text{when } \text{Cov}(d_1, d_k) > 0 \text{ and the agent maximizes } d_1^{(\text{short-term})}$$

*Proof sketch.* When short-term $d_1$ gains come at the expense of evaluative dimensions — which they do when the covariance structure implies that quick monetary gains require trust erosion, community degradation, or identity compromise — the evaluative dimensions decline. The positive covariance means that maintaining $d_k$ is positively associated with $d_1$ in the long run, but the short-term optimizer sacrifices the long-run $d_1$ benefit for immediate gain. Each period, the evaluative stock $V_E$ falls; eventually, the erosion cascades back into $d_1$ as customer defection, regulatory action, and reputational collapse. $\square$

**[Empirical.]** Boeing's shift from engineering-led to finance-led management in the 2000s is a textbook case of temporal hijacking. Each quarterly decision to reduce inspection procedures ($d_8$: legitimacy), accelerate production timelines ($d_4$: worker autonomy compressed), and prioritize stock buybacks over R&D ($d_9$: epistemic investment sacrificed) improved short-term $d_1$. The cumulative evaluative erosion materialized as the 737 MAX crisis — a catastrophic boundary crossing on $d_2$ (safety rights), $d_5$ (trust with regulators and airlines), and $d_8$ (institutional legitimacy) that cost tens of billions on $d_1$ and 346 lives on $d_2$.

### Goodhart's Law as Objective Hijacking

**[Modeling Axiom.]** Charles Goodhart's observation — "when a measure becomes a target, it ceases to be a good measure" — is, in the geometric framework, a theorem about objective hijacking. The mechanism is precise:

1. A multi-dimensional objective (the full-manifold geodesic) is measured by a scalar proxy (a specific contraction).
2. Agents are incentivized to maximize the proxy.
3. The Scalar Irrecoverability Theorem (Chapter 6) guarantees that the proxy discards information.
4. Agents exploit the discarded dimensions: they improve the proxy while degrading the unmonitored dimensions.
5. The proxy diverges from the original objective.

University rankings maximize a scalar index (combining research output, student selectivity, alumni donations). The index becomes the objective. Universities then optimize the index — recruiting international students for selectivity scores, encouraging faculty to split papers for citation counts, investing in amenities that attract high-income alumni — while the actual educational mission ($d_9$: genuine knowledge creation, $d_4$: student intellectual autonomy, $d_6$: community contribution) degrades. The index goes up. The education goes sideways. This is not a bug in the ranking system. It is the mathematically inevitable consequence of replacing a tensor with a scalar and then optimizing the scalar.

> **MARIA'S COFFEE SHOP — OBJECTIVE HIJACKING**
>
> *The REIT that owns Maria's building is managed by a property management firm whose CEO's compensation is tied to the REIT's quarterly distribution per unit. The CEO's objective has been hijacked from "maximize long-term property value on the full manifold" to "maximize quarterly cash distribution." This objective favors raising rents to market rate immediately ($d_1$ maximized this quarter) over maintaining tenant relationships ($d_5$), preserving neighborhood character ($d_6$), and building long-term occupancy stability ($d_8$). The CEO is not corrupt. The CEO is optimizing the objective placed before them. The corruption is in the objective, not the optimizer.*

## 10.4 Local Minima: Bubbles and Poverty Traps

### Asset Bubbles as Overvalued Basins

**[Modeling Axiom.]** An asset bubble is a local minimum in the economic decision manifold — a configuration that appears optimal on the projected manifold ($d_1$ shows rising values) but is suboptimal on the full manifold ($d_5$ trust is eroding, $d_9$ epistemic quality is degrading, $d_8$ institutional legitimacy is strained).

The bubble basin has depth: the more participants invest, the deeper the basin becomes (positive feedback). Exiting the basin requires a coordinated jump — a perturbation large enough to overcome the basin walls. But individual agents face a coordination problem: the first to exit pays the highest cost (selling at the peak of the bubble looks like leaving money on the table on $d_1$).

The geometric characterization: a bubble exists when the metric on the perceived manifold (where asset values look high) diverges from the metric on the true manifold (where the underlying value does not support the prices). The divergence is measurable — it shows up as increasing curvature on the true manifold, as small perturbations produce increasingly large responses. Chapter 11 develops this into a full singularity analysis.

### Poverty Traps as Low-Income Basins

**[Empirical.]** A poverty trap is a basin of attraction on the economic manifold from which the escape energy exceeds what agents trapped within it can accumulate. The basin is defined by low $d_1$ (low income), constrained $d_4$ (limited autonomy — can't invest in education, can't move to opportunity), degraded $d_9$ (limited information about opportunities), and high boundary penalties on the paths leading out (education costs, relocation costs, credential requirements).

The geometric prediction: poverty traps are deepest when multiple dimensions reinforce each other — low income ($d_1$) constrains autonomy ($d_4$), which limits information ($d_9$), which prevents discovery of escape paths. Breaking a poverty trap requires simultaneous intervention on multiple dimensions, not just income transfer ($d_1$ alone). This is precisely what the empirical evidence on effective anti-poverty programs shows: the most successful interventions combine cash transfers ($d_1$), skills training ($d_9$), asset provision ($d_2$), and social support ($d_5$, $d_6$).

**Theorem 10.2 (Multi-Dimensional Poverty Trap Depth).** *The depth $D(s^*)$ of a poverty trap at state $s^*$ is a function of the number of simultaneously constrained dimensions. If $k$ dimensions are constrained (below their boundary thresholds), the basin depth scales superlinearly:*

$$D(s^*) \propto k^2 \cdot \bar{\beta}$$

*where $\bar{\beta}$ is the average boundary penalty for crossing the constraint boundaries. The quadratic scaling arises from the Mahalanobis structure: when multiple dimensions are constrained, the covariance matrix amplifies the effective distance because displacements on constrained dimensions interact.*

**[Empirical.]** This prediction is testable. Banerjee and Duflo's (2011) evidence on "graduation programs" — multi-dimensional anti-poverty interventions — shows that simultaneous intervention on income ($d_1$), assets ($d_2$), training ($d_9$), and social support ($d_5$) produces persistent escape from poverty, while single-dimension interventions (cash alone, training alone) produce only temporary improvement. The geometric explanation: single-dimension interventions move the agent along one axis of the manifold but do not escape the basin, because the other constrained dimensions pull the agent back. Multi-dimensional interventions move the agent diagonally across the basin, exploiting the covariance structure to escape with lower total energy.

The Mahalanobis geometry is key. If the covariance matrix $\Sigma$ has large positive off-diagonal terms between $d_1$ and $d_9$ (income and information are correlated — rich people have more information), then a diagonal move (simultaneously improving income and information) covers more Mahalanobis distance than two sequential single-dimension moves of the same total magnitude. The diagonal move escapes the basin; the sequential moves do not. This is why integrated anti-poverty programs work and single-instrument policies often fail.

### Herding as Heuristic Convergence

**[Empirical.]** Asset bubbles are sustained by *herding* — the tendency of agents to follow the crowd rather than their private information. In the geometric framework, herding is *heuristic convergence*: agents replace their individual heuristic $h_i(n)$ with the market consensus heuristic $\bar{h}(n)$, even when $h_i$ and $\bar{h}$ disagree.

On the decision manifold, herding flattens the heuristic field: instead of $n$ independent heuristic estimates pointing in different directions (which, by the wisdom-of-crowds effect, tend to cancel out individual errors), all agents follow the same estimate. If the consensus estimate is wrong — if $\bar{h}(n)$ systematically underestimates the cost of the asset-price path — then all agents simultaneously follow a suboptimal trajectory, creating a coordinated deviation from the geodesic that individual agents could not produce.

The bubble pops when a perturbation (a margin call, a credit downgrade, a piece of bad news) pushes some agents' $g(n)$ high enough that the sum $f = g + h$ exceeds the cost of exiting the basin. These agents exit. Their exit raises the cost for remaining agents (falling prices increase $g$). More agents exit. The cascade is the A* search, restarted with updated costs, converging on a different geodesic — one that leads away from the bubble rather than deeper into it.

## 10.5 Gauge Breaking: Nominal vs. Real Confusion

Money illusion — confusing nominal and real values — is a gauge violation (Chapter 8). But it has a specific geometric signature in market failures: it causes agents to follow geodesics on the nominal manifold rather than the real manifold, producing systematically suboptimal decisions.

**[Empirical.]** The most consequential gauge violation in modern economies is inflation illusion in housing markets. Nominal house prices rise at 5% per year. Real house prices (inflation-adjusted) are flat. The nominal gauge assigns high $d_1$ value to homeownership; the real gauge assigns moderate $d_1$ value. Agents operating on the nominal gauge over-invest in housing, under-invest in productive assets, and take on excessive leverage — because the nominal heuristic is inadmissible on the real manifold.

The geometric fix is gauge-invariant pricing: express all economic quantities in real (inflation-adjusted) terms. This is the economic equivalent of the BIP — evaluations invariant under the inflation gauge transformation. The persistence of money illusion, despite its well-known irrationality, reflects the fact that the nominal gauge is *more salient* (Chapter 4's framing analysis applies): the nominal number is vivid and concrete, while the real number requires computation.

### The Sunk Cost Fallacy as Path-Dependence Violation

**[Empirical.]** The sunk cost fallacy — the tendency to continue investing in a losing project because of what has already been spent — is a gauge violation of a specific type: it violates *re-description invariance along the temporal dimension*.

The BIP requires that the evaluation of a decision depend only on the current state and the available future paths, not on the path that led to the current state. A decision between "continue" and "abandon" should be evaluated from the current node forward ($g(n)$ measured from $v_0$ to the current state is fixed and the same for both options). The sunk cost fallacy introduces $g_{\text{past}}$ — the cost already incurred — into the evaluation of future paths, where it does not belong.

In A* terms, the fallacy is a bookkeeping error: the agent includes the sunk cost in $g(n)$ for the "abandon" path but not for the "continue" path, making abandonment appear more costly than it actually is. The correct A* comparison evaluates $f(n) = g(n_{\text{current}}) + h(n)$ for both options, using the same $g(n_{\text{current}})$. The sunk cost is in $g(n_{\text{current}})$ and cancels out of the comparison.

The geometric reading: the sunk cost fallacy is a violation of gauge invariance under temporal re-description. The same current state, described as "we have invested $2M and need $1M more" versus "we need $1M to complete a project," produces different decisions. The first description activates a path-dependent evaluation; the second does not. The economic content is identical. The violation is measurable: agents who are given the "sunk cost" framing are approximately 35% more likely to continue than agents given the "fresh start" framing, even when the projects are identical from this point forward (Arkes and Blumer, 1985).

### Currency-Denomination Effects

**[Empirical.]** Raghubir and Srivastava (2002) demonstrated that tourists spend more when prices are denominated in a foreign currency with a large numeric value relative to their home currency. A Japanese tourist in Indonesia, seeing prices in thousands of rupiah, perceives them as "large numbers" even though the amounts are trivial in yen terms. The evaluation depends on the denomination — a pure gauge transformation that should leave the evaluation invariant.

The geometric characterization: the agent's heuristic function $h(n)$ is not gauge-invariant. It responds to the *numeral* attached to the price, not to the *real value* the numeral represents. The gauge violation tensor $V_{ij}$ (Chapter 8) can be measured directly: present the same basket of goods in two currencies and compare purchase decisions. The difference is the gauge violation. It is large for unfamiliar currencies and small for familiar ones — suggesting that the gauge invariance of the heuristic is learned through experience, not innate.

## 10.6 The Interaction of Pathologies

The four pathologies are not independent failures. They interact, amplify each other, and create feedback loops that make isolated correction insufficient.

**Proposition 10.2 (Pathology Cascade).** *The four pathologies form a directed causal graph:*

$$\text{Heuristic corruption} \to \text{Objective hijacking} \to \text{Local minima} \to \text{Gauge breaking} \to \text{Heuristic corruption}$$

*At each arrow, the upstream pathology enables or deepens the downstream one. The cycle is self-reinforcing.*

**[Empirical.]** Consider the cascade in the 2008 financial crisis:

1. **Heuristic corruption**: Mortgage-backed securities were priced using models that ignored tail risk on $d_9$ and counterparty risk on $d_5$. The price heuristic was inadmissible — it systematically underestimated the true manifold cost of these instruments.

2. **Objective hijacking**: Rating agencies, whose stated objective was accurate risk assessment (full-manifold evaluation), had their objective hijacked by revenue dependence on the institutions they rated. The agencies' effective geodesic shifted from "assess risk accurately" to "maintain revenue from issuers."

3. **Local minima**: The housing bubble created a basin of attraction where all agents — homeowners, lenders, investors, regulators — were trapped. Exiting the basin required accepting immediate losses ($d_1$), which no individual agent had the incentive to do. The basin deepened with each new entrant.

4. **Gauge breaking**: Nominal house prices rose while real house prices (adjusted for income, rental equivalence, and construction costs) were flat or declining. The nominal gauge told agents they were getting richer; the real gauge showed they were accumulating leverage. The gauge violation sustained the bubble by masking the divergence between perceived and actual manifold position.

5. **Return to heuristic corruption**: The nominal price increase was incorporated into future price estimates, further corrupting the heuristic. The model said: "prices always go up." This became the heuristic for a generation of market participants, completing the cycle.

The cascade explains why the crisis was so difficult to prevent. Correcting any single pathology would not have broken the cycle. Fixing the models (heuristic repair) would not have helped if the rating agencies were still captured (objective hijacking). Fixing the agencies would not have helped if agents were still trapped in the bubble basin (local minima). Popping the bubble would not have helped if the nominal gauge was still masking real values (gauge breaking). Effective prevention required addressing all four pathologies simultaneously — which is why it did not happen.

---

## Worked Example: Maria's Gentrifying Neighborhood

Maria's Mission District neighborhood illustrates all four pathologies simultaneously.

**Heuristic corruption (externalities).** The REIT's rent increase of 40% reflects the gentrification premium on $d_1$ — comparable properties command higher rents. But it does not price the community displacement (4 jobs lost, community meeting point destroyed, cultural identity eroded). On the full manifold, the true cost of the rent increase includes $\Delta d_3 = -$large (fairness), $\Delta d_6 = -$large (social impact), $\Delta d_7 = -$large (community identity). The price heuristic, operating on $d_1$ alone, is inadmissible.

**Objective hijacking (zoning).** The local planning commission was established to preserve neighborhood character (full manifold objective). Over time, developer lobbying shifted its effective objective to maximizing property tax revenue ($d_1$ projection). Zoning variances that allow luxury condos are approved; requests for affordable housing protections are denied. The commission's geodesic has been hijacked from public welfare to developer welfare.

**Local minimum (bubble).** Commercial real estate in the Mission is in an overvalued basin. The REIT paid a premium based on projected rental income that assumes continued gentrification — a trajectory that depends on displacing businesses like Maria's. But displacing those businesses degrades the neighborhood character that attracted gentrifiers in the first place. The basin is self-undermining: the deeper agents commit to the gentrification trajectory, the more they destroy the value that trajectory depends on.

**Gauge breaking (nominal vs. real).** The neighborhood's nominal property values have tripled. But community value — the density of local businesses, social services, cultural institutions, long-term residents — has declined. The nominal gauge shows explosive growth; the real gauge (including all nine dimensions) shows net decline. Agents operating on the nominal gauge celebrate; agents experiencing the real manifold mourn.

The four pathologies interact. Heuristic corruption (externalities not priced) enables objective hijacking (developers capture the zoning process because externalities are invisible to the $d_1$ heuristic). Objective hijacking deepens the bubble (captured regulators approve more development, inflating the basin). The bubble is sustained by gauge breaking (nominal values look good, masking real decline). And gauge breaking prevents correction (agents can't see the problem because they're measuring on the wrong manifold).

The geometric framework doesn't just catalog these failures. It explains why they co-occur and reinforce each other — they are coupled pathologies on a single manifold, not independent market failures requiring independent policy responses.

---

## Technical Appendix

**Definition 10.1 (Heuristic Corruption Index).** The *heuristic corruption* of the price system for good $g$ is:

$$\text{HCI}(g) = \frac{|p(g) - w^*(g)|}{w^*(g)}$$

where $p(g)$ is the market price ($d_1$ component only) and $w^*(g)$ is the full manifold cost of producing and distributing $g$. $\text{HCI} = 0$ means the price is admissible; $\text{HCI} > 0$ means the price heuristic underestimates true cost by a factor proportional to the missing dimensions.

**Proposition 10.1 (Pathology Coupling).** **[Conditional Theorem.]** On the economic decision manifold, the four pathologies are not independent. Heuristic corruption on dimension $d_k$ increases the probability of objective hijacking toward $d_k$-aligned objectives, which deepens local minima on the $d_k$-projected manifold, which is sustained by gauge breaking between the projected and full manifolds.

**Definition 10.2 (Basin Depth for Economic Local Minima).** The *depth* of an economic local minimum at state $s^*$ is:

$$D(s^*) = \min_{\gamma: s^* \to \partial B} \text{BF}(\gamma) - \text{BF}(\gamma^*)$$

where $\partial B$ is the boundary of the basin, $\gamma^*$ is the optimal path within the basin, and $\text{BF}(\gamma)$ is the behavioral friction along path $\gamma$. A poverty trap has $D(s^*) > A(s^*)$, where $A(s^*)$ is the maximum accumulation rate achievable within the basin.

---

## References

Akerlof, G. A. (1970). "The Market for 'Lemons'." *Quarterly Journal of Economics*, 84(3), 488–500.
Hayek, F. A. (1945). "The Use of Knowledge in Society." *American Economic Review*, 35(4), 519–530.
Pigou, A. C. (1920). *The Economics of Welfare.* Macmillan.
Shiller, R. J. (2005). *Irrational Exuberance.* Princeton University Press.
Stigler, G. J. (1971). "The Theory of Economic Regulation." *Bell Journal of Economics*, 2(1), 3–21.
