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

## 10.3 Objective Hijacking: When the Optimizer Serves the Wrong Master

### Regulatory Capture

**[Empirical.]** Regulatory capture occurs when the regulator's objective function shifts from public welfare (the full manifold) to the regulated industry's preferences (a projected subspace). In the geometric framework, this is *objective hijacking*: the search is guided by a different objective than the one it was designed to optimize.

The captured regulator's decision manifold has been contracted: dimensions $d_3$ (fairness to the public), $d_6$ (social impact), and $d_8$ (institutional legitimacy) are suppressed, and the regulator's effective objective becomes alignment with $d_1$ interests of the regulated industry. The geodesic shifts from the public-welfare path to the industry-welfare path.

The geometric framework predicts that capture is easier when the public-welfare dimensions ($d_3$, $d_6$, $d_8$) are diffuse (many citizens each affected a little) and the industry dimensions ($d_1$) are concentrated (few firms each affected a lot). This is because concentrated interests produce steep gradients on the captured manifold, while diffuse interests produce flat gradients — the regulator's corrupted heuristic follows the steep gradient.

### Short-Termism

Quarterly earnings pressure is objective hijacking in the temporal dimension. The firm's true geodesic optimizes over the full temporal manifold — including long-term trust ($d_5$), institutional legitimacy ($d_8$), and social capital ($d_6$). The quarterly proxy contracts the optimization horizon, collapsing the temporal manifold to a single period and destroying the geodesic's long-term structure.

The geometric prediction: short-termism is most damaging for firms whose value depends heavily on evaluative dimensions ($d_5$–$d_9$) — technology companies (trust in data handling), financial institutions (trust in solvency), and community-serving businesses like Maria's coffee shop. For commodity producers whose value is primarily $d_1$, short-term optimization is less distortionary because the relevant manifold is closer to the scalar projection.

## 10.4 Local Minima: Bubbles and Poverty Traps

### Asset Bubbles as Overvalued Basins

**[Modeling Axiom.]** An asset bubble is a local minimum in the economic decision manifold — a configuration that appears optimal on the projected manifold ($d_1$ shows rising values) but is suboptimal on the full manifold ($d_5$ trust is eroding, $d_9$ epistemic quality is degrading, $d_8$ institutional legitimacy is strained).

The bubble basin has depth: the more participants invest, the deeper the basin becomes (positive feedback). Exiting the basin requires a coordinated jump — a perturbation large enough to overcome the basin walls. But individual agents face a coordination problem: the first to exit pays the highest cost (selling at the peak of the bubble looks like leaving money on the table on $d_1$).

The geometric characterization: a bubble exists when the metric on the perceived manifold (where asset values look high) diverges from the metric on the true manifold (where the underlying value does not support the prices). The divergence is measurable — it shows up as increasing curvature on the true manifold, as small perturbations produce increasingly large responses. Chapter 11 develops this into a full singularity analysis.

### Poverty Traps as Low-Income Basins

**[Empirical.]** A poverty trap is a basin of attraction on the economic manifold from which the escape energy exceeds what agents trapped within it can accumulate. The basin is defined by low $d_1$ (low income), constrained $d_4$ (limited autonomy — can't invest in education, can't move to opportunity), degraded $d_9$ (limited information about opportunities), and high boundary penalties on the paths leading out (education costs, relocation costs, credential requirements).

The geometric prediction: poverty traps are deepest when multiple dimensions reinforce each other — low income ($d_1$) constrains autonomy ($d_4$), which limits information ($d_9$), which prevents discovery of escape paths. Breaking a poverty trap requires simultaneous intervention on multiple dimensions, not just income transfer ($d_1$ alone). This is precisely what the empirical evidence on effective anti-poverty programs shows: the most successful interventions combine cash transfers ($d_1$), skills training ($d_9$), asset provision ($d_2$), and social support ($d_5$, $d_6$).

## 10.5 Gauge Breaking: Nominal vs. Real Confusion

Money illusion — confusing nominal and real values — is a gauge violation (Chapter 8). But it has a specific geometric signature in market failures: it causes agents to follow geodesics on the nominal manifold rather than the real manifold, producing systematically suboptimal decisions.

**[Empirical.]** The most consequential gauge violation in modern economies is inflation illusion in housing markets. Nominal house prices rise at 5% per year. Real house prices (inflation-adjusted) are flat. The nominal gauge assigns high $d_1$ value to homeownership; the real gauge assigns moderate $d_1$ value. Agents operating on the nominal gauge over-invest in housing, under-invest in productive assets, and take on excessive leverage — because the nominal heuristic is inadmissible on the real manifold.

The geometric fix is gauge-invariant pricing: express all economic quantities in real (inflation-adjusted) terms. This is the economic equivalent of the BIP — evaluations invariant under the inflation gauge transformation. The persistence of money illusion, despite its well-known irrationality, reflects the fact that the nominal gauge is *more salient* (Chapter 4's framing analysis applies): the nominal number is vivid and concrete, while the real number requires computation.

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
