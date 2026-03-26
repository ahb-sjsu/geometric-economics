# Front Matter

---

## Title Page

**Geometric Economics: Decision Manifolds, Equilibria, and the Geometry of Markets**

Andrew H. Bond
Senior Member, IEEE
Department of Computer Engineering
San Jose State University

Book 4 of the Geometric Series

*San Jose, 2026*

---

## Series Foreword

This is the fourth volume in the Geometric Series.

The series began with a simple observation: across domains --- ethics, law, economics, cognition, communication, medicine --- the standard methodology compresses multi-dimensional structure into scalar numbers and then wonders why the numbers behave badly. GDP does not capture economic wellbeing. Utility functions do not capture decision-making. Cost-benefit analyses do not capture policy tradeoffs. The pattern is universal and the diagnosis is the same: scalar reduction destroys geometric structure, and the destruction is irreversible.

*Geometric Methods in Computational Modeling* (Book 1) assembled the mathematical toolkit: Riemannian geometry, hyperbolic embeddings, persistent homology, SPD manifolds, gauge theory. *Geometric Reasoning: From Search to Manifolds* (Book 2) developed the parent framework --- the heuristic field formalism, geodesic deviation, the four failure modes, gauge invariance, and the Scalar Irrecoverability Theorem that unifies them. *Geometric Ethics* (Book 3) was the first domain instantiation, demonstrating the framework on the 9-dimensional stratified moral manifold with its $D_4 \times U(1)_H$ symmetry group.

This book is the second domain instantiation, and in many ways the most confrontational. Economics is the discipline most committed to scalar reduction --- the utility function is its central construct, the price system is its organizing principle, and GDP is its measure of success --- and the discipline where the consequences of scalar reduction are most consequential. When a moral philosopher collapses nine dimensions to one, the result is an impoverished ethical theory. When an economist collapses nine dimensions to one, the result is a policy apparatus that optimizes GDP while inequality deepens, communities disintegrate, financial systems become fragile, and the planet warms.

The central construction of this volume is the **Bond Geodesic Equilibrium** (BGE), a generalization of Nash equilibrium to the full nine-dimensional economic decision manifold. We prove that Nash equilibrium is the scalar projection of BGE --- the special case obtained when all dimensions except monetary payoff are collapsed. The projection is lossy: the Scalar Irrecoverability Theorem demonstrates that the information destroyed by this collapse is mathematically irrecoverable. The homo economicus of classical theory is not wrong. It is a shadow on the wall of a nine-dimensional cave, and the shadow cannot be used to reconstruct the object that cast it.

The empirical validation is substantial. The companion library `eris-econ` implements the full pipeline --- decision manifold construction, A* pathfinding, BGE computation --- and validates against published experimental data from game theory, prospect theory, and cross-cultural behavioral economics. The results: 16 of 16 behavioral predictions correct at 2.70% mean absolute error, including the cross-cultural variation in ultimatum game offers that has resisted satisfactory explanation within the classical paradigm. The framework does not catalogue biases. It predicts them, from geometry alone.

Subsequent volumes extend the framework further: *Geometric Law* (Book 5) takes the manifold into courts and constitutions, *Geometric Cognition* (Book 6) turns it inward on the mind, *Geometric Communication* (Book 7) applies it across species and millennia, and *Geometric Medicine* (Book 8) brings it to the bedside where the stakes are highest. Each domain instantiation reveals new structure. Each confirms the same theorem: scalar reduction is irrecoverable, and the geometry matters.

---

## Preface

### The Price of Everything

Oscar Wilde defined a cynic as someone who knows the price of everything and the value of nothing. He meant it as a joke. This book treats it as a theorem.

The modern economic apparatus is the most sophisticated price-computing system ever devised. It produces prices for coffee and crude oil, for labor and leisure, for risk and insurance, for the right to emit a ton of carbon dioxide into an atmosphere shared by eight billion people. The prices are computed with extraordinary precision, transmitted at the speed of light, and aggregated into indices --- GDP, CPI, the S&P 500 --- that serve as the vital signs of civilization. The system is, by any standard, a triumph of institutional engineering.

The thesis of this book is that the system computes the wrong thing. Not because the prices are miscalculated --- markets are often remarkably efficient at computing prices --- but because prices are scalars, and the decisions they guide are not. An economic decision lives on a nine-dimensional manifold whose dimensions include monetary consequences, rights, fairness, autonomy, trust, social impact, identity, institutional legitimacy, and epistemic quality. The price system projects this manifold onto a single dimension and declares the result to be "the economy." It is as if a physician measured only a patient's temperature, declared them healthy when the thermometer read 98.6, and sent them home with an undetected tumor. The temperature is correct. The diagnosis is catastrophic.

The mathematical framework that makes this precise is the geometry of the economic decision manifold. The manifold is not a metaphor. It is a weighted simplicial complex whose vertices are economic states, whose edges are economic actions, and whose edge weights are computed from the full Mahalanobis distance on the nine-dimensional attribute vector plus boundary penalties for crossing moral and institutional constraints. Economic decision-making is pathfinding on this complex: the agent stands at the current state and seeks the minimum-cost path to an acceptable outcome. The minimum-cost path is the Bond geodesic. It is, formally, the best thing to do --- not just financially, not just ethically, but on the full manifold where financial and ethical considerations are not competing claims but dimensions of a single space.

The central result of the book is the Bond Geodesic Equilibrium (BGE), the multi-agent extension of this pathfinding. A BGE is a profile of paths --- one for each agent --- where no agent can reduce their total behavioral friction by unilaterally switching to a different path. We prove three things about this equilibrium. First, BGE is exactly Nash equilibrium of the augmented game --- the game defined on the full manifold rather than the scalar projection. Second, classical Nash equilibrium is the limiting case of BGE obtained by collapsing all non-monetary dimensions. Third, BGE *refines* Nash: it excludes equilibria that require crossing moral boundaries, because the boundary penalties on the full manifold make boundary-crossing strategies strictly dominated by boundary-respecting alternatives.

The relationship between BGE and Nash is the same as the relationship between general relativity and Newtonian mechanics: the simpler theory is the limiting case of the richer theory, obtained by collapsing the relevant structure. Nash equilibrium is not wrong. It is incomplete. It computes on a projected subspace and therefore misses the equilibria that exist on the full manifold. This is why experimental subjects in the ultimatum game reject unfair offers that Nash predicts they should accept, why cooperation emerges in one-shot prisoner's dilemmas that Nash predicts should end in mutual defection, and why cross-cultural variation in game-theoretic behavior correlates with social institutions rather than with "irrationality." The subjects are not irrational. They are playing the game on the full manifold, where the Nash-predicted equilibrium does not exist.

I did not set out to write a critique of economics. The project began as a chapter in *Geometric Ethics* --- Chapter 20, on economic applications of the moral manifold --- and grew into a book when the mathematics proved richer than expected. The Bond Geodesic Equilibrium was originally a worked example; it became the central construction when I realized it subsumed Nash equilibrium as a theorem rather than merely generalizing it as an analogy. The empirical validation was supposed to take a week; it took three months, because each prediction the framework made turned out to be correct against published data, and the accumulation of correct predictions demanded explanation.

The explanation, ultimately, is geometric. The economic decision manifold has structure --- curvature, symmetry, boundaries, singularities --- and that structure determines behavior. When the manifold is flat and unbounded (the classical case: all dimensions zero except monetary payoff), the framework reduces to standard economics. When the manifold is curved (loss aversion, risk framing, fairness norms), the framework predicts the departures from classical theory that behavioral economists have documented. When the manifold develops singularities (financial crises, market freezes, pricing breakdowns), the framework predicts the catastrophic amplification that standard models cannot explain. The geometry unifies classical economics, behavioral economics, and financial crisis theory into a single mathematical structure. The unification is not ecumenical compromise; it is a theorem.

This book is written for three audiences, and it asks something different of each.

For **economists** --- whether classical, behavioral, or heterodox --- the book provides a mathematical framework that resolves the "rationality wars" by showing that the combatants are arguing about projections of the same higher-dimensional object. The homo economicus model is the scalar projection; behavioral economics is the catalogue of phenomena that the projection fails to capture; this book provides the manifold on which both live. The mathematics is self-contained (Appendix A covers the prerequisites), and the reader who has encountered game theory, general equilibrium, or welfare economics will find the constructions natural extensions of familiar ideas.

For **mathematicians and physicists** curious about applications of differential geometry, gauge theory, and simplicial topology to the social sciences, the book provides a worked example of what it means to apply these tools with full rigor --- not as loose analogy but as formal construction with definitions, theorems, proofs, and falsifiable predictions. The economic gauge group $\mathbb{R}^+ \times S_n$ has structure distinct from the gauge groups of physics, and the conservation laws it produces via Noether's theorem are genuine economic predictions, not metaphors for physical conservation.

For **policymakers, regulators, and citizens** who sense that GDP does not measure what matters but lack a mathematical framework for saying why, the book provides that framework. GDP is a contraction of the economic tensor --- a specific operation that discards eight of nine dimensions. The Scalar Irrecoverability Theorem proves that no post-hoc correction can recover what GDP discards. Alternative metrics --- the Human Development Index, Genuine Progress Indicator, Stiglitz-Sen-Fitoussi dashboard --- are partial recoveries of discarded dimensions. The framework says exactly which dimensions each alternative recovers and which it still misses.

### A Note on Scope

This book does not claim that economics is "wrong." It claims that economics, as currently practiced, operates on a projection of the space where economic decisions actually occur, and that the projection is lossy in a mathematically precise and irrecoverable sense. The claim is supported by definitions, theorems, and empirical predictions that differ from classical predictions and match experimental data. The framework does not replace existing economic theory; it embeds it in a richer structure that resolves puzzles the scalar theory cannot address.

Chapter 16 is honest about what the framework cannot yet explain. The nine-by-nine covariance matrix has not been estimated from large-scale economic data. The boundary penalties are theoretically motivated but not empirically calibrated across cultures. The conservation laws are derived from symmetry but have not been tested in controlled economic experiments. The No Escape Theorem for economic complexity is conjectured but unproven. These are not hedges. They are the frontier, and the frontier is where the interesting work begins.

Each chapter opens with a running example --- Maria, who owns a small coffee shop in a gentrifying neighborhood --- that grounds the abstract framework in the decisions of a real business owner navigating a multi-dimensional economic landscape. Maria's rent negotiation, pricing decisions, supply chain choices, and responses to financial crisis each instantiate a different geometric structure. The reader who follows Maria's story through sixteen chapters will have seen every construct in the book applied to a single, coherent economic situation.

### How to Read This Book

- **The theoretical path**: Chapters 1--9. From the scalar failure through the full geometric framework, culminating in the Bond Geodesic Equilibrium and the conservation laws.
- **The empirical path**: Chapters 3, 4, 7, and the worked examples throughout. For readers who want data and predictions before formalism.
- **The applied path**: Chapters 1, 7, 10, 13--15. From motivation through equilibrium to trade, regulation, and environmental policy.
- **The fast path**: Chapters 1, 6, 7, 10. The scalar failure, irrecoverability, BGE, and market failures. The core argument in four chapters.

---

## Core Objects at a Glance

| Object | What It Is | Where Developed |
|--------|-----------|-----------------|
| **Economic decision complex** $\mathcal{E}$ | 9-dimensional weighted simplicial complex of economic states and transitions | Ch. 3 |
| **Decision manifold metric** | Mahalanobis distance + boundary penalties: $d(s,t) = \sqrt{(s-t)^T \Sigma^{-1} (s-t)} + \sum_k \beta_k \cdot \mathbb{1}[\text{boundary}_k]$ | Ch. 4 |
| **Price heuristic** $h(x)$ | The price signal as scalar field guiding economic search; admissible = efficient market | Ch. 5 |
| **Economic tensor** | Obligations as vectors, interests as covectors, GDP as a specific contraction | Ch. 6 |
| **Bond Geodesic Equilibrium** (BGE) | Multi-agent equilibrium on the full manifold; Nash is the d$_1$-only projection | Ch. 7 |
| **Economic gauge group** | $\mathbb{R}^+ \times S_n$ (scaling $\times$ relabeling); invariance under unit changes | Ch. 8 |
| **Value conservation** | Noether's theorem applied to economic BIP; value $\neq$ created by relabeling | Ch. 9 |
| **Scalar Irrecoverability** | No continuous $\phi: \mathbb{R}^9 \to \mathbb{R}$ is injective; GDP destroys 8 dimensions | Ch. 6 |

## Key Results at a Glance

| Finding | Source |
|---------|--------|
| Nash equilibrium is the scalar projection of BGE (Theorem 21) | eris-econ |
| Loss aversion varies 1.0--3.53 with dimensional activation (contradicts constant $\lambda$) | eris-econ |
| 16/16 behavioral predictions correct at 2.70% MAE | eris-econ validation |
| Kahneman & Tversky 17 problems: 13/17 predicted (76%) | eris-econ |
| Cross-cultural ultimatum offers explained by metric variation | Henrich et al. data |
| Public goods: 4.3% out-of-sample prediction error | Fraser & Nettle |
| Endowment ratio: 1.66 (consistent with experimental WTA/WTP) | eris-econ |

---

## Epistemic Status Classification

| Tag | Meaning | Approx. Count |
|-----|---------|---------------|
| **[Established Mathematics.]** | Standard results from game theory, differential geometry, topology | ~25 |
| **[Empirical.]** | Claims supported by eris-econ validation data, published experimental results | ~20 |
| **[Modeling Axiom.]** | Structural choices (9 dimensions, Mahalanobis metric, BGE as equilibrium concept) | ~15 |
| **[Conditional Theorem.]** | Results that follow from stated assumptions (BGE-Nash, irrecoverability) | ~15 |
| **[Speculation/Extension.]** | Interpretive claims beyond what data directly supports | ~10 |

---

## Acknowledgments

A book that reaches from Adam Smith's invisible hand to the curvature singularities of the 2008 financial crisis is inevitably indebted to more people and traditions than any acknowledgment section can encompass. The debts are many.

The geometric framework that underpins this book was developed as part of the Geometric Ethics programme at San Jose State University, and the economic instantiation grew directly from the nine-dimensional moral manifold constructed in *Geometric Ethics* (Bond, 2026b). The transition from ethical to economic geometry was neither obvious nor smooth; the decision to make the Bond Geodesic Equilibrium the central construction rather than a corollary emerged through sustained engagement with the game-theoretic literature and the realization that the BGE-Nash relationship was a theorem, not an analogy. I am grateful to my colleagues in the SJSU Department of Computer Engineering for providing an environment where a computer scientist can work on economic geometry without having to justify the enterprise at every departmental meeting.

The empirical validation --- the eris-econ library and its predictions against experimental data --- owes debts in multiple directions. The cross-cultural data from Henrich et al.'s 15-society ultimatum game study, the public goods data from Fraser and Nettle, the prospect theory problems from Kahneman and Tversky, and the cross-cultural bargaining data from Ruggeri and collaborators provided the empirical targets against which the framework was tested. These researchers collected the data under conditions that a computational modeler can only appreciate from a distance. That the geometric framework predicts their results from first principles, rather than fitting them post hoc, is the strongest argument for taking the geometry seriously.

The behavioral economics community has been an invaluable, if unwitting, collaborator. The decades of experimental work by Kahneman, Tversky, Thaler, and their many colleagues produced the catalogue of "anomalies" that this book reinterprets as geometric predictions. Without their empirical work, the framework would have nothing to predict. The interpretation offered here --- that behavioral "biases" are not failures of rationality but consequences of optimizing on a richer manifold than classical theory admits --- is a tribute to their data, if a reframing of their theoretical conclusions.

The financial crisis analysis in Part IV benefited from the detailed accounts of the 2008 crisis by Kindleberger, Minsky, Brunnermeier, Gorton, and the Financial Crisis Inquiry Commission. The geometric reinterpretation --- singularity theory applied to collapsing covariance structures --- is new, but the raw material is theirs. Hyman Minsky's insight that stability breeds instability is, in the geometric framework, a statement about curvature dynamics on the economic manifold, and his intellectual legacy pervades Chapters 10--12.

I thank the welfare economics tradition --- particularly Sen, Stiglitz, Fitoussi, Rawls, and Atkinson --- for providing the intellectual foundation on which the critique of scalar reduction rests. The Stiglitz-Sen-Fitoussi Commission's report on the measurement of economic performance and social progress is, in retrospect, a demand for exactly the multi-dimensional framework that this book provides. Their critique was conceptual; the contribution here is to make it mathematical.

Institutional support came from the Department of Computer Engineering at San Jose State University, the College of Engineering, and the SJSU Research Foundation. Computing resources were provided by the Atlas workstation and the university's High-Performance Computing cluster.

The series editors and early readers of the manuscript --- including colleagues at the IEEE Computational Intelligence Society, workshop participants at NeurIPS 2025, and anonymous reviewers of the component papers --- improved the book through criticism that ranged from gentle to devastating. The errors that remain are evidence of finite bandwidth on an infinite-dimensional problem.

Finally, and as always: to my family, who have endured a year of dinner-table discussions about Mahalanobis distances, gauge violations, and whether the housing crisis was really a curvature singularity, and who have responded with patience, humor, and the well-calibrated heuristic that it is time to change the subject when the whiteboard comes out.

Andrew H. Bond
San Jose, California
March 2026
