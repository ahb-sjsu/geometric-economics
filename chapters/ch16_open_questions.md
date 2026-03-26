# Chapter 16: Open Questions

> *"The formulation of a problem is often more essential than its solution."*
> — Albert Einstein

*Part VI: Horizons*

---

> **RUNNING EXAMPLE — MARIA'S COFFEE SHOP**
>
> *Maria Esperanza retires in 2050. She sells her coffee shop to a former employee — a transaction whose Bond geodesic includes not just the sale price but the continuation of fair wages, community presence, and ethical sourcing. The geometric economics framework, which began as an academic exercise, has become standard practice: commercial real estate is valued on multi-dimensional manifolds, trade agreements specify geodesic constraints on all nine dimensions, and financial regulation is calibrated to manifold curvature rather than scalar volatility.*
>
> *Or perhaps none of this happens. The framework remains academic — elegant but untested, compelling but unimplemented. Which future materializes depends on whether the open questions below can be answered.*

---

## 16.1 Measuring the Economic Metric

The framework assumes a 9×9 covariance matrix $\Sigma$ that encodes the interaction structure of economic dimensions. The eris-econ library calibrates $\Sigma$ from behavioral data — game theory experiments, prospect theory studies, cross-cultural comparisons. The calibration produces 16/16 correct behavioral predictions at 2.70% MAE.

**[Empirical.]** But the calibration is partial. The open questions:

**Open Problem 16.1.** Can $\Sigma$ be estimated from large-scale observational data (transaction records, market data, survey panels) rather than controlled experiments? The experimental data covers ~1,000 subjects across a handful of games. A manifold-based analysis of millions of economic transactions could estimate $\Sigma$ at much higher resolution — but requires disentangling the nine dimensions from observational data where they are confounded.

**Open Problem 16.2.** Is $\Sigma$ stable across time, or does it evolve? If the covariance structure changes (e.g., trust dimensions become more important during a pandemic), the geodesics shift even when the physical economy does not. A time-varying $\Sigma(t)$ would require dynamic manifold estimation.

**Open Problem 16.3.** Is $\Sigma$ universal or culture-specific? The cross-cultural data (Henrich et al.) shows systematic variation in game behavior across societies. The framework attributes this to different $\Sigma$ values — the Machiguenga have low off-diagonal terms between $d_1$ and $d_3$ (weak fairness-cost coupling) while the Lamalera have high terms (strong coupling from cooperative whale hunting). Measuring $\Sigma$ across cultures would test this explanation.

## 16.2 The Economic No Escape Theorem

*Geometric Ethics* (Chapter 18) proves the No Escape Theorem: an AI system operating within a geometrically constrained evaluation space cannot circumvent the constraints through representational manipulation. The constraints are *structural*, not behavioral — they are properties of the space, not rules the agent can reinterpret.

**Open Problem 16.4.** **[Speculation/Extension.]** Is there an economic analogue? Can we construct an economic decision manifold with structural constraints that market participants cannot circumvent through financial engineering? If so, such constraints would be qualitatively different from regulation (which can be evaded) — they would be features of the economic space itself.

The candidate: sacred-value boundaries ($\beta = \infty$). If these are genuinely topological features of the decision manifold (not just very high penalties), then no financial instrument can bridge the disconnected components. Organ markets remain impossible not because they are prohibited but because the manifold has no path from "organ" to "money" — the components are topologically disconnected.

## 16.3 Mechanism Design on the Manifold

**Open Problem 16.5.** Classical mechanism design (Hurwicz, Myerson, Maskin) operates on scalar utilities. What does mechanism design look like on the full decision manifold?

The revelation principle — that any mechanism can be replaced by a direct mechanism where agents truthfully report their types — relies on scalar payoffs. On the manifold, "truthfully reporting your type" means revealing your full attribute vector $\mathbf{a}(v)$ and your covariance matrix $\Sigma$, which is a nine-dimensional private signal. Can we design mechanisms that are incentive-compatible on the full manifold?

**Open Problem 16.6.** **[Speculation/Extension.]** Can the BGE be computed in polynomial time for general multi-agent problems? The single-agent case reduces to A* search ($O(|E| + |V| \log |V|)$). The multi-agent case requires iterated best response, which may cycle. Under what conditions does it converge, and how quickly?

## 16.4 Falsifiable Predictions

The framework generates specific, testable predictions that distinguish it from both classical and behavioral economics:

**[Empirical.]** **Prediction 1: Dimensional activation.** Increasing the salience of fairness ($d_3$) in an ultimatum game should increase rejection rates — not because preferences change but because the active manifold expands, increasing the effective boundary penalty. This is testable by manipulating fairness framing while holding monetary stakes constant.

**Prediction 2: Loss-aversion variability.** $\lambda$ should vary with the number of active dimensions (Chapter 4). Transactions that activate more dimensions should show higher loss aversion. Pure monetary gambles should show $\lambda \approx 1$ (no extra dimensions activated); morally loaded gambles should show $\lambda > 2$ (multiple dimensions activated by loss).

**Prediction 3: Cross-cultural $\Sigma$ variation.** The covariance matrix $\Sigma$ should vary across cultures in ways that predict game-theoretic behavior. Cultures with strong cooperative norms should have high off-diagonal terms between $d_1$ and $d_3$/$d_6$; individualistic cultures should have low off-diagonal terms.

**Prediction 4: Sacred-value boundaries.** Willingness to accept compensation for sacred-value violations should be discontinuous (not merely very high). If boundaries are genuine topological features, no finite compensation can induce crossing — the willingness-to-accept function has a discontinuity at the boundary, not just a steep slope.

**Prediction 5: Factor analysis recovers ~9 dimensions.** Principal component analysis of behavioral economic data across a broad enough set of decisions should recover approximately 9 independent factors corresponding to the nine dimensions.

**Prediction 6: Bond Index correlates with behavior.** The Bond Index (the gauge-violation measure from Chapter 8) should predict deviations from classical economic behavior: transactions with high Bond Index are morally loaded and should show larger deviations from $d_1$-optimal behavior.

## 16.5 Connections to Other Frameworks

**Open Problem 16.7.** Information geometry (Amari, 1998) equips statistical models with a natural Riemannian metric — the Fisher information metric. The decision manifold has a different metric (Mahalanobis + boundary penalties). Under what conditions are these metrics related? If the agent's decision process is Bayesian, is the Fisher metric on the belief space related to the Mahalanobis metric on the decision space?

**Open Problem 16.8.** Optimal transport (Villani, 2003) studies the cheapest way to transform one distribution into another. Economic exchange is a transport problem: transforming one distribution of goods into another. Is the BGE related to the Wasserstein geodesic on the space of economic distributions?

## 16.6 Closing

This book has argued that economic decisions have geometric structure that scalar models cannot capture. The Bond Geodesic Equilibrium generalizes Nash equilibrium to the full decision manifold. Prospect theory's anomalies are geometric properties, not cognitive biases. Conservation laws distinguish transferable from evaluative dimensions, explaining why trade creates non-monetary value. Market failures are geometric pathologies — heuristic corruption, objective hijacking, local minima, gauge breaking — that co-occur and reinforce each other.

The framework is young. The empirical validation, while promising (16/16 predictions at 2.70% MAE), covers only a fraction of economic behavior. The open questions above define a research program that will take decades to complete.

But the central insight is already clear: *Homo economicus is not wrong because humans are irrational. It is incomplete because it computes on a projected subspace of the actual decision manifold.* The projection is the source of the anomalies, the paradoxes, and the persistent gap between economic theory and economic reality. The full manifold has been there all along. This book provides the vocabulary to describe it.

The work begins here.

---

## References

Amari, S. (1998). "Natural Gradient Works Efficiently in Learning." *Neural Computation*, 10(2), 251–276.
Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* SJSU.
Bond, A. H. (2026b). *Geometric Ethics.* SJSU.
Bond, A. H. (2026c). *Geometric Reasoning.* SJSU.
Hurwicz, L. (1972). "On Informationally Decentralized Systems." *Decision and Organization*, 297–336.
Villani, C. (2003). *Topics in Optimal Transportation.* AMS.
