# Chapter 2: Historical Precursors

> *"The ideas of economists and political philosophers, both when they are right and when they are wrong, are more powerful than is commonly understood. Indeed the world is ruled by little else."*
> -- John Maynard Keynes, *The General Theory of Employment, Interest, and Money* (1936)

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Every school of economic thought has something to say about Maria Esperanza's coffee shop on Valencia Street. The classical economist sees a profit-maximizing firm: Maria should set prices where marginal cost equals marginal revenue and hire workers until the marginal product of labor equals the wage. The behavioral economist sees a loss-averse decision-maker: Maria's visceral resistance to the 40% rent increase is stronger than her attraction to an equivalent gain, because losses loom larger than gains. The institutional economist sees a web of contracts: Maria's lease terms, her supplier agreements, her employment obligations, and the zoning regulations that constrain her options matter more than any utility function. The capabilities theorist sees a person whose substantive freedoms are at stake: not just her income, but her freedom to run a business, to employ her neighbors, to be part of her community.*
>
> *Each school captures something real. None captures everything. The geometric framework does not reject any of these insights -- it shows that each one is a projection of the same multi-dimensional reality onto a different axis. This chapter traces the geometry that was always latent in the tradition.*

---

The geometric approach to economics did not spring from nowhere. For two and a half centuries, the most perceptive economic thinkers have been circling the same insight: that economic life has structure that a single number cannot represent. They did not always have the mathematical vocabulary to say what they meant. Some came close. This chapter traces their paths -- not to claim intellectual priority, but to show that the framework developed in this book is the formalization of intuitions that the tradition has carried, imperfectly expressed, for generations.

For each school of thought, we present the core contribution, identify where it falls short, and offer a "Geometric Reading" that reinterprets the school's insights in the language of manifolds, metrics, and geodesics. The pattern is consistent: every major school of economics has discovered one or more dimensions of the decision manifold, studied it in isolation, and then struggled to explain phenomena that arise from the *interaction* between dimensions. The geometric framework does not supersede these schools. It provides the common mathematical structure that connects them.

## 2.1 Classical Rational Choice: The First Coordinate

### The Core Contribution

The expected utility framework, axiomatized by von Neumann and Morgenstern (1944) and extended by Savage (1954), is the foundation of modern economic theory. The framework is built on four axioms: completeness (the agent can compare any two alternatives), transitivity (if A is preferred to B and B to C, then A is preferred to C), independence (preferences between lotteries are not affected by adding a common alternative), and continuity (small changes in probabilities produce small changes in preference). If an agent's preferences satisfy these axioms, there exists a utility function $u$ such that the agent's behavior is equivalent to maximizing $\mathbb{E}[u]$.

This is an achievement of extraordinary elegance. It reduces the complexity of choice to a single optimization problem: find the action that maximizes a real-valued function. The mathematics is clean, the predictions are sharp, and the welfare implications are direct -- Pareto optimality, the welfare theorems, and the foundations of mechanism design all follow from this framework.

**[Empirical.]** The behavioral economics programme has shown that the axioms are systematically violated. Independence fails in the Allais paradox. Transitivity fails in context-dependent choice (Tversky, 1969). Completeness is questionable when agents genuinely cannot compare alternatives. These are not edge cases or laboratory curiosities -- they are stable, replicable phenomena observed across populations and cultures.

The standard defense -- that humans are "approximately" rational, or rational "in the limit" -- has been empirically falsified. The deviations are not random noise around rational behavior. They are *systematic*, *predictable*, and *stable*. They have structure. The question is: what structure?

### Geometric Reading

**[Modeling Axiom.]** The classical framework captures exactly one dimension of the decision manifold: $d_1$ (consequences -- monetary cost, material outcome, risk-adjusted expected value). The utility function $u: X \to \mathbb{R}$ is a coordinate function on this single dimension.

The axioms hold *on the full manifold*. They fail *on the scalar projection*. Consider transitivity. A preference relation that is transitive in nine dimensions can appear intransitive when projected to one dimension, just as a helix -- a curve that is monotonically ascending in three dimensions -- appears to reverse direction when projected onto a plane. Tversky's (1969) demonstrations of intransitive preferences are not evidence that human preferences lack structure. They are evidence that the structure is multi-dimensional and that different pairwise comparisons activate different dimensions of the manifold (Theorem 16).

The Allais paradox dissolves similarly. The agent's preference reversal between "certain \$1M" and "89% chance of \$1M, 10% chance of \$5M, 1% chance of \$0" reflects the activation of $d_9$ (epistemic certainty has value beyond expected monetary value) and $d_7$ (identity: "I am prudent"). On the scalar projection, the independence axiom is violated. On the full manifold, preferences are consistent: the attribute-vector difference between certainty and risk includes non-zero components on $d_7$ and $d_9$ that the expected-value calculation discards.

The classical framework is not wrong. It is *incomplete*. It sees $d_1$ clearly and is blind to $d_2$ through $d_9$. For anonymous commodity markets with enforceable contracts -- settings where the non-monetary dimensions are approximately inactive -- the classical predictions are excellent. The framework breaks down precisely when additional dimensions become active: face-to-face bargaining, morally loaded goods, trust-dependent exchange, decisions involving identity or community.

> **MARIA'S COFFEE SHOP -- THE CLASSICAL VIEW**
>
> *The classical economist advises Maria to maximize profit. Set the price of a latte at the point where the marginal customer is just willing to pay. If the rent increase makes the shop unprofitable, close it -- the resources (Maria's labor, the building, the equipment) will flow to higher-valued uses. This analysis is correct on $d_1$. It is silent on $d_2$ through $d_9$. It cannot explain why Maria stays open at a loss for three months while she negotiates, or why the neighborhood petitions the landlord on her behalf, or why the REIT's own long-term returns depend on the community vitality that Maria's shop creates.*

## 2.2 Behavioral Economics and Prospect Theory: Cataloguing the Curvature

### The Core Contribution

Kahneman and Tversky's prospect theory (1979), and the subsequent behavioral economics programme developed by Thaler, Ariely, Camerer, and others, is the most important empirical contribution to economics since the marginalist revolution. The findings are now textbook:

- **Loss aversion:** Losses loom larger than equivalent gains ($\lambda \approx 2.25$).
- **Reference dependence:** Utility is evaluated relative to a reference point, not in absolute terms.
- **Framing effects:** Logically equivalent descriptions produce different choices.
- **Probability weighting:** Small probabilities are overweighted; large probabilities are underweighted.
- **Present bias:** Immediate rewards are overvalued relative to future rewards (hyperbolic discounting).
- **Fairness constraints:** Agents sacrifice material payoff to punish unfairness.

Prospect theory replaced expected utility with a descriptive model incorporating an S-shaped value function (concave for gains, convex for losses, steeper for losses) and a probability-weighting function that overweights small probabilities. The model fits the data with remarkable precision.

**[Empirical.]** The limitation is that prospect theory is a *parameterization*, not an *explanation*. It tells you the shape of the value function but not *why* evolution or culture produced that shape. It tells you that $\lambda \approx 2.25$ but not what determines the value of $\lambda$ or why it should vary across contexts. Each documented bias is a separate entry in a catalogue. The catalogue grows (the "bias" Wikipedia page now lists over 180 entries), but the entries are not connected by any unifying mathematical structure.

Kahneman's own dual-process theory -- System 1 (fast, automatic, heuristic) and System 2 (slow, deliberate, calculating) -- provides the psychological architecture. What it lacks is the mathematical content: What is the space on which System 1 and System 2 operate? What is the formal relationship between them? Why does their interaction produce the specific pattern of "biases" that behavioral economics has catalogued?

### Geometric Reading

**[Conditional Theorem.]** The behavioral economics programme is, in geometric terms, a comprehensive empirical survey of the decision manifold's curvature, metric asymmetry, and gauge violations -- conducted without the geometric vocabulary to describe what was being measured.

Loss aversion is not a psychological quirk. It is a *metric asymmetry*: losses traverse more dimensions of the decision manifold than equivalent gains. A monetary loss of \$100 activates not only $d_1$ (consequences) but also $d_2$ (rights: "I had this; now it's taken"), $d_3$ (fairness: "this is unfair"), $d_6$ (social status: "I've lost standing"), $d_7$ (identity: "I am a loser"), and $d_9$ (epistemic anxiety: "what else might I lose?"). The gain of \$100 activates primarily $d_1$. The loss-aversion coefficient $\lambda = w_- / w_+$ is not a free parameter -- it is a *derived quantity*, computable from the manifold's metric structure (Theorem 34). This is why $\lambda$ varies: it depends on how many dimensions are activated by the specific loss, not on some fixed property of the value function. Chapter 4 develops this in full.

Reference dependence is not a bias. It is the natural coordinate system for pathfinding. A* search computes edge costs from the *current* node, not from the origin. The cost of moving from "here" to "there" depends on where "here" is. On a curved manifold, this is not approximate -- it is exact. The metric is position-dependent. A path that costs little from one starting point may cost a great deal from another, not because the agent is "biased" but because the manifold's curvature varies (Proposition 36).

Framing effects are genuine cognitive errors -- but they have a specific mathematical signature. They are *gauge symmetry violations*: the agent's heuristic function $h(n)$ assigns different costs to the same economic state under different descriptions. The Bond Invariance Principle requires that evaluations be invariant under meaning-preserving transformations. Framing effects violate this principle (Theorem 37). The framework thus draws a precise boundary between rational responses to manifold structure (loss aversion, reference dependence) and genuine cognitive errors (framing effects, some probability-weighting distortions).

> **MARIA'S COFFEE SHOP -- THE BEHAVIORAL VIEW**
>
> *The behavioral economist sees Maria's resistance to the rent increase as loss aversion: she weights the threatened loss of her shop more heavily than she would weight an equivalent gain. The geometric economist agrees but goes further: the threatened loss activates $d_2$ (her right to the space she has occupied for twelve years), $d_5$ (the trust relationship with her landlord, now broken), $d_6$ (the community impact of closure), and $d_7$ (her identity as a business owner). The "loss aversion" is not irrational -- it is the rational response to a displacement that crosses multiple dimensions simultaneously. The $\lambda \approx 2.25$ that Kahneman measured is the average ratio $w_- / w_+$ across experimental contexts. Maria's $\lambda$ for this specific decision is higher, because more dimensions are active.*

## 2.3 Bounded Rationality: The Heuristic as Architecture

### The Core Contribution

Herbert Simon's bounded rationality (1955) is the most profound critique of the classical framework. Simon recognized that real agents have finite computational resources. They cannot enumerate all alternatives, compute all consequences, or optimize over all possible futures. Instead, they *satisfice* -- they search until they find an alternative that exceeds an aspiration level, and then they stop.

Gigerenzer and colleagues (1999) extended Simon's insight into the "fast and frugal heuristics" programme. They showed that simple decision rules -- "take the best," "recognition heuristic," "1/N allocation" -- can outperform optimal statistical procedures in uncertain environments. This is the "less is more" effect: simpler rules, using less information, can produce better outcomes than complex rules using all available information, because the complex rules overfit to noise.

**[Empirical.]** The bounded rationality programme demonstrated something the classical framework could not accommodate: that the computational architecture of the decision-maker matters. The same information, processed by different algorithms, produces different choices. Optimization is not the only rational procedure; in many environments, it is not even the best one.

### Geometric Reading

The geometric framework formalizes what Simon intuited and Gigerenzer demonstrated. Moral and cultural heuristics are not approximations to an ideal optimizer. They are *components of a different optimization architecture*. Specifically, they serve as the $h(n)$ function in A* search -- they estimate the cost-to-go, prune the search space, and guarantee that the resulting path is optimal *given the heuristic*.

This is not satisficing. It is *heuristic-guided optimal search* on the full manifold. The distinction matters. Satisficing says: "the agent stops searching because computational resources are limited." The geometric framework says: "the agent uses a heuristic function to guide search efficiently, and the quality of the outcome depends on the quality of the heuristic." A good heuristic (admissible, in the A* sense) guarantees optimal outcomes. A poor heuristic (inadmissible) produces genuine errors. The framework classifies heuristics into a precise hierarchy:

1. **Strictly admissible** ($\beta_k \leq \beta_k^*$): the heuristic underestimates or exactly estimates the true boundary cost. The search is optimal. Example: the taboo on murder.
2. **$\varepsilon$-admissible** ($\beta_k \leq (1+\varepsilon)\beta_k^*$): the heuristic slightly overestimates. The search finds a near-optimal path. Example: most social-norm heuristics (tipping, queue etiquette).
3. **Inadmissible** ($\beta_k \gg \beta_k^*$): the heuristic substantially overestimates. Genuine errors occur. Example: phobias, excessive guilt.
4. **Gauge-variant** ($\beta_k$ depends on framing): the heuristic is not even a consistent function of the manifold position. Example: framing effects, anchoring.

Categories 1-2 are features of the architecture. Categories 3-4 are genuine cognitive errors. Behavioral economics has conflated all four categories under the single label "bias." The geometric framework separates them.

> **MARIA'S COFFEE SHOP -- THE BOUNDED RATIONALITY VIEW**
>
> *Simon would say that Maria cannot compute the optimal response to the rent increase -- the problem is too complex, the future too uncertain, the alternatives too numerous. She satisfices: she negotiates, tries to find a workable arrangement, and accepts the first one that meets her aspiration level. The geometric framework agrees about the complexity but reframes the story: Maria's System 1 provides a heuristic field $h(n)$ that estimates the cost-to-go on the full manifold. Her gut feeling that the rent increase is "unfair" is not noise -- it is a boundary-penalty estimate based on $d_3$ (fairness). Her instinct to negotiate rather than litigate reflects $h(n)$ assigning lower cost to the negotiation path than the litigation path, based on $d_5$ (trust preservation) and $d_6$ (community impact). The heuristic is not optimal in the classical sense. It is $\varepsilon$-admissible on the full manifold.*

## 2.4 Game Theory and Nash Equilibrium: Interaction on the Projection

### The Core Contribution

Nash equilibrium (1950) is the dominant solution concept in non-cooperative game theory: a strategy profile where no player can unilaterally improve their payoff. The Nash framework assumes common knowledge of rationality, where "rationality" means scalar utility maximization.

The framework is magnificent in its generality. Any strategic interaction can be modeled as a game. Any game has at least one Nash equilibrium in mixed strategies. The concept has been extended to handle incomplete information (Bayesian Nash), sequential moves (subgame perfection), and repeated interaction (folk theorems).

**[Empirical.]** The well-known failures of Nash equilibrium in behavioral games are extensive and systematic. In the ultimatum game, Nash predicts that the proposer offers the minimum possible amount and the responder accepts (because any positive amount beats zero). Observed behavior: proposers typically offer 40-50% of the endowment, and responders reject offers below 20-30%. In the prisoner's dilemma, Nash predicts mutual defection. Observed behavior: substantial cooperation, especially with face-to-face interaction or shared group identity. In public goods games, Nash predicts zero contribution. Observed behavior: initial contributions of 40-60%, declining but rarely reaching zero.

The standard response is to modify the utility function: add fairness terms (Fehr-Schmidt inequality aversion), reciprocity terms (Rabin's reciprocity model), or other-regarding preferences (Bolton-Ockenfels ERC). Each modification captures one behavioral anomaly. But each is *ad hoc* -- there is no unified principle that generates all the modifications.

### Geometric Reading

The geometric framework provides that principle. Agents do not maximize a scalar utility function (with or without social-preference modifications). They minimize path cost on the full decision manifold. The "social preferences" are not modifications to the utility function -- they are *dimensions of the manifold* that the utility function was projecting away.

The Bond Geodesic Equilibrium (BGE) replaces Nash equilibrium as the solution concept when agents optimize on the full manifold. The BGE nests Nash as a special case: when all non-monetary dimensions are zeroed out ($\beta_k = 0$ for all $k$, and $\Sigma = \sigma_1^2 \mathbf{e}_1 \mathbf{e}_1^T$), the BGE coincides with Nash equilibrium of the standard monetary game (Theorem 21). When boundary penalties are non-zero, the BGE *refines* Nash by excluding equilibria that require crossing moral boundaries. This is not a modification of the utility function -- it is a change of the manifold on which optimization occurs.

The ultimatum game illustrates the point. Player 2's decision is pathfinding on $\mathcal{E}_2$ with dimensions including $d_3$ (fairness). Accepting an unfair offer ($\leq$ \$2 out of \$10) yields $\Delta d_1 = +2$ (monetary gain) but $\Delta d_3 = -\text{large}$ (fairness violation) and $\Delta d_7 = -\text{large}$ (identity: "I am a pushover"). The total edge weight for accepting exceeds the weight for rejecting. Player 2 rationally rejects. Player 1, anticipating this, offers approximately \$5.

> **MARIA'S COFFEE SHOP -- THE GAME THEORY VIEW**
>
> *Maria's lease negotiation is a bargaining game. Nash bargaining theory predicts a split based on outside options and discount rates. But the observed dynamics are richer: Maria's willingness to accept terms depends not only on her outside options ($d_1$) but on whether the terms feel fair ($d_3$), whether the process respects her rights as a long-term tenant ($d_2$), and whether the landlord's behavior signals trustworthiness for future interactions ($d_5$). The REIT's negotiator, optimizing on $d_1$ alone, is surprised when Maria rejects an offer that is "rational" on the scalar projection but crosses moral boundaries on the full manifold.*

## 2.5 Arrow's Impossibility and Sen's Capabilities: The Multi-Dimensional Intuition

### The Core Contribution

Arrow's impossibility theorem (1951) is one of the deepest results in social choice theory. It proves that no social welfare function can simultaneously satisfy unrestricted domain, Pareto efficiency, independence of irrelevant alternatives, and non-dictatorship when aggregating ordinal preferences over three or more alternatives. The result has shaped welfare economics for seven decades, generating a pervasive pessimism about the possibility of rational collective choice.

Amartya Sen's capability approach (1999) offers a constructive alternative. Sen argues that welfare should be evaluated not as scalar utility but as a vector of *capabilities* -- substantive freedoms to achieve various "functionings." A functioning is an achievement (being nourished, being sheltered, participating in community life); a capability is the freedom to achieve that functioning. The capability approach insists on irreducible plurality: no single index can capture the multidimensional character of human well-being.

**[Empirical.]** The capability approach has been enormously influential in development economics -- it underpins the Human Development Index -- but it has been criticized for lacking a formal aggregation procedure. If welfare is multi-dimensional, how do we compare states where one dimension improves while another worsens? The capability approach provides the philosophical argument for multi-dimensionality but not the mathematical structure for working with it.

### Geometric Reading

The geometric framework provides the mathematical structure that the capability approach lacks -- and it explains *why* Arrow's impossibility holds.

Arrow's theorem operates on *ordinal rankings* -- one-dimensional orderings of alternatives. The impossibility arises from projecting multi-dimensional evaluations onto one-dimensional orderings. When agents evaluate alternatives as attribute vectors in $\mathbb{R}^9$ rather than as ordinal rankings, a component-wise social welfare mapping $W: (\mathbb{R}^9)^n \to \mathbb{R}^9$ can satisfy analogues of all four Arrow conditions simultaneously (Proposition). The impossibility reappears only when $W$ is composed with a projection $\phi: \mathbb{R}^9 \to \mathbb{R}$ -- that is, when the multi-dimensional social evaluation is collapsed to a scalar ranking.

Arrow's theorem is, in this reading, a *theorem about dimensional collapse*. It is a mathematical proof that certain desirable properties of social choice are compatible in high-dimensional space but incompatible after projection to one dimension. The impossibility is not a deep feature of social choice -- it is a consequence of the representational format.

Sen's capabilities *are* dimensions of the decision manifold. Autonomy/freedom maps to $d_4$. Material capability maps to $d_1$. Epistemic capability maps to $d_9$. The Mahalanobis-weighted structure of the economic decision complex provides the formal aggregation procedure that the capability approach has been seeking: a metric that encodes how dimensions interact, which trade-offs are permissible, and how displacements along different dimensions relate to one another.

> **MARIA'S COFFEE SHOP -- THE CAPABILITIES VIEW**
>
> *Sen would evaluate Maria's situation not by her income (which a scalar analysis emphasizes) but by her capabilities: Can she run her business freely ($d_4$)? Can she employ her neighbors ($d_6$)? Can she participate in her community on her own terms ($d_7$)? Does she have the information she needs to make good decisions ($d_9$)? The rent increase threatens not one capability but several simultaneously. The geometric framework formalizes this: the Mahalanobis distance from Maria's current state to her post-increase state is large because multiple capability-dimensions shift at once, and the covariance matrix $\Sigma$ amplifies displacements along dimensions that co-vary.*

## 2.6 Information Economics and Market Failure: Miscalibration on the Manifold

### The Core Contribution

Akerlof's "market for lemons" (1970) demonstrated that information asymmetry can cause market collapse. When sellers know product quality but buyers do not, adverse selection drives good products out: sellers of high-quality goods cannot credibly signal quality, buyers assume average quality and offer average prices, and high-quality sellers exit the market. Stiglitz and colleagues (1981) generalized this to insurance, credit, and labor markets, showing that information asymmetry produces systematic market failures that competitive equilibrium cannot resolve.

The information economics tradition -- Akerlof, Stiglitz, Spence -- established that *what agents know* matters as much as *what agents want*. Market outcomes depend not only on preferences and endowments but on the structure of information: who knows what, when, and at what cost.

### Geometric Reading

In the geometric framework, information asymmetry is a specific distortion of dimension $d_9$ (epistemic status) and $d_5$ (trust). A "lemon" market is one where the edge weights perceived by buyers differ from the true edge weights because the epistemic dimension is miscalibrated:

$$w_{\text{perceived}}(v_i, v_j) \neq w_{\text{true}}(v_i, v_j) \quad \text{when } d_9(v_j) \text{ is unobservable}$$

Market institutions -- warranties, reputation systems, regulation, professional licensing -- function as *manifold calibration mechanisms*: they align $w_{\text{perceived}}$ with $w_{\text{true}}$ by providing information that corrects the $d_9$ component. A warranty tells the buyer: "the seller is so confident in quality that they will bear the cost of failure." This raises the buyer's $d_9$ score for the product, bringing perceived edge weights closer to true edge weights.

Market failure, in this reading, is not a failure of the price mechanism. It is a failure of *manifold calibration*. The price ($d_1$) cannot do the work of $d_9$ (epistemic status) because they are different dimensions. Collapsing the manifold to $d_1$ and hoping that prices will convey all relevant information is asking a scalar to do a tensor's job. This is precisely Hayek's insight about the price system -- that prices aggregate dispersed information -- reframed geometrically: prices aggregate information *along $d_1$*, but the information along other dimensions must be conveyed by other mechanisms.

## 2.7 Commons Governance and Collective Action: Calibrating the Boundary Penalties

### The Core Contribution

Elinor Ostrom's Nobel-winning work on governing the commons (1990) overturned the standard prediction that common-pool resources inevitably suffer a "tragedy of the commons" -- overexploitation due to individual incentives to free-ride. Ostrom documented hundreds of cases where communities successfully managed shared resources without either privatization or centralized regulation, through institutions that create *conditional cooperation norms*.

Ostrom identified eight "design principles" for successful commons governance: clearly defined boundaries, proportional equivalence between benefits and costs, collective-choice arrangements, monitoring, graduated sanctions, conflict-resolution mechanisms, minimal recognition of rights to organize, and nested enterprises for larger systems. These principles are not theoretical derivations -- they are empirical regularities extracted from decades of field research.

### Geometric Reading

In the geometric framework, Ostrom's design principles are *boundary-penalty calibration rules* -- institutional mechanisms that maintain the decision manifold's parameters so that cooperation lies on the Bond geodesic for each participant.

- **Clearly defined boundaries** establish which agents are on the decision complex and which edges exist. Without boundaries, the manifold is not well-defined: agents cannot compute path costs if they do not know who else is on the manifold.
- **Graduated sanctions** calibrate $\beta_k$ values: small violations incur small boundary penalties, escalating with severity. This ensures that the heuristic function $h(n)$ accurately reflects the true costs of norm violation -- neither so low that free-riding seems costless nor so high that minor infractions trigger disproportionate punishment.
- **Collective-choice arrangements** ensure $d_4$ (autonomy) is preserved -- agents participate in setting the rules, so the legitimacy dimension $d_8$ supports compliance. If rules are imposed externally, $d_4$ and $d_8$ are violated, and the boundary penalties may be insufficient to sustain cooperation.
- **Monitoring** maintains $d_9$ (epistemic status) -- agents can observe whether others comply, keeping the manifold calibrated. Without monitoring, agents cannot estimate the boundary penalties that others face, and the epistemic dimension degrades.

Ostrom showed empirically that these institutions work. The geometric framework shows *why*: they maintain the calibration of the decision manifold so that the Bond geodesic for each agent includes cooperation. When any design principle is violated, the manifold becomes miscalibrated, and the individual Bond geodesic shifts away from cooperation -- not because the agent is selfish, but because the manifold no longer supports cooperative paths.

> **MARIA'S COFFEE SHOP -- THE COMMONS VIEW**
>
> *Maria's block of Valencia Street is, in some respects, a commons. The neighborhood's vitality -- foot traffic, community trust, cultural character -- is a shared resource that no single business owns but all depend on. Ostrom's framework explains why Maria and her neighboring business owners informally coordinate: they refer customers to each other, participate in street fairs, maintain the sidewalks. The geometric framework formalizes the mechanism: the boundary penalties for defection ($\beta_{\text{social}}$, $\beta_{\text{reputation}}$) are maintained by the tight social monitoring ($d_9$) that a walkable commercial street provides. When the REIT raises Maria's rent, it is not just extracting money -- it is degrading the commons-governance mechanism by removing a node from the community's decision complex.*

## 2.8 Moral Foundations Theory: The Dimensions Emerge

### The Core Contribution

Jonathan Haidt's Moral Foundations Theory (2012) identifies five (later six) moral "taste receptors": care/harm, fairness/cheating, loyalty/betrayal, authority/subversion, sanctity/degradation, and liberty/oppression. Haidt's central insight is that moral judgments are primarily *intuitive* -- they are fast, automatic, affectively laden responses that precede (and often override) deliberate moral reasoning. Moral reasoning, in Haidt's account, is typically *post hoc rationalization* of intuitive judgments, not the cause of those judgments.

**[Empirical.]** The Moral Foundations framework has been validated across cultures, political orientations, and age groups. The foundations predict political affiliation (liberals weight care and fairness more heavily; conservatives weight all six foundations more equally), moral judgments about specific scenarios, and even consumer behavior.

### Geometric Reading

The overlap between Haidt's moral foundations and the nine dimensions of the decision manifold is substantial:

| Haidt Foundation | Decision Manifold Dimension(s) |
|---|---|
| Care/Harm | $d_1$ (consequences), $d_6$ (social impact) |
| Fairness/Cheating | $d_3$ (fairness) |
| Loyalty/Betrayal | $d_5$ (trust), $d_7$ (identity/virtue) |
| Authority/Subversion | $d_8$ (legitimacy) |
| Sanctity/Degradation | $d_7$ (identity/virtue), boundary penalties $\beta_k$ |
| Liberty/Oppression | $d_4$ (autonomy) |

Haidt's insight that moral judgments are intuitive maps directly onto the System 1 / $h(n)$ interpretation developed in the geometric framework. The moral foundations are the *content* of the heuristic function: they specify which boundary penalties are active and how they are weighted. Haidt shows that humans *have* moral intuitions that constrain economic behavior; the geometric framework shows that these intuitions have *geometric structure* that can be computed.

The contribution relative to Haidt is mathematical formalization. In Moral Foundations Theory, the foundations are qualitative categories. In the geometric framework, they become dimensions of a metric space with measurable distances, gauge symmetry, and conservation laws. The difference matters: qualitative categories can describe behavior after the fact, but metric spaces generate quantitative predictions that can be tested against data.

## 2.9 Experimental Economics: The Empirical Terrain

### The Core Contribution

The experimental economics tradition -- from Vernon Smith's (1962) pioneering market experiments through Camerer's (2003) comprehensive synthesis -- has produced the empirical base that any new theory must explain. The key findings are:

**(a)** Double-auction markets converge to competitive equilibrium even with few traders. This is the strongest result in favor of classical theory: when the setting strips away moral dimensions (anonymous trading, enforceable contracts, homogeneous goods), the $d_1$-only prediction is accurate.

**(b)** Bargaining games show systematic fairness-driven deviations from Nash prediction. In the ultimatum game, dictator game, and their variants, agents consistently sacrifice material payoff to enforce or express fairness norms.

**(c)** Trust games show substantial trust and reciprocity even in one-shot anonymous settings. Agents send money to strangers, trusting that the stranger will return a share, even when the stranger has no material incentive to do so.

**(d)** Punishment of norm violators persists even when costly to the punisher ("altruistic punishment"). In public goods games with punishment options, agents pay to reduce the payoff of free-riders, even though the punishment benefits the group, not the punisher individually.

### Geometric Reading

The geometric framework explains *why some markets behave classically and others do not*. Classical behavior emerges when the active dimensions collapse to $d_1$ -- anonymous commodity markets with enforceable contracts. Behavioral anomalies emerge when additional dimensions are activated -- face-to-face bargaining ($d_5$, $d_6$, $d_7$), trust-dependent exchange ($d_5$), morally loaded goods ($d_3$, $d_7$), punishment opportunities ($d_3$, $d_8$).

This is a testable, quantitative prediction. For any experimental setting, the framework specifies which dimensions are active (based on the features of the setting that activate moral-economic considerations) and therefore whether classical or behavioral predictions should hold. A commodity double-auction with anonymous electronic trading should collapse to $d_1$ and converge to competitive equilibrium. The same auction conducted face-to-face, with identifiable traders and morally loaded goods, should activate additional dimensions and deviate from classical predictions in specific, predictable ways.

Finding (d) -- altruistic punishment -- is particularly important. On the scalar projection, punishment is irrational: the punisher pays a cost and receives no material benefit. On the full manifold, punishment is a rational response to a fairness-boundary violation ($d_3$): the boundary penalty $\beta_{\text{fairness}}$ exceeds the monetary cost of punishment. The punisher is not altruistic -- they are minimizing path cost on the full manifold, where tolerating unfairness has higher total cost than paying to punish it.

---

## Worked Example: Maria's Hiring Decision Through Four Lenses

Maria needs to hire a new barista. She has two candidates: Alex, who has more experience and would generate higher revenue, and Jamie, who is from the neighborhood, has less experience, but would benefit enormously from the job. Let us analyze this decision through four economic schools, and then through the geometric lens.

### The Classical Analysis

**Maximize profit.** Alex generates higher revenue per hour. Hire Alex. End of analysis.

- Dimension considered: $d_1$ (consequences/monetary value)
- Prediction: Hire Alex
- What it misses: Everything else

### The Behavioral Analysis

**Account for biases.** Maria may exhibit status quo bias (preferring to hire someone similar to her current employees), anchoring (fixating on Alex's higher productivity number), or affect heuristic (feeling emotionally drawn to Jamie's story). The behavioral economist would "debias" Maria by presenting the decision in neutral terms, removing irrelevant anchors, and focusing on expected monetary outcomes.

- Dimensions considered: $d_1$ (consequences), plus corrections for "biases"
- Prediction: Hire Alex (after debiasing)
- What it misses: The "biases" may be admissible heuristics encoding real information about non-monetary dimensions

### The Institutional Analysis

**Consider the contracts and constraints.** Does Maria face any legal obligation to hire locally? Are there community development incentives? What are the terms of employment, and how do they constrain future decisions? The institutional economist sees the decision as embedded in a web of rules, norms, and enforcement mechanisms.

- Dimensions considered: $d_2$ (rights/contractual obligations), $d_8$ (legitimacy/regulatory compliance)
- Prediction: Depends on the institutional environment
- What it misses: The non-institutional moral dimensions ($d_3$, $d_5$, $d_7$)

### The Capabilities Analysis

**Evaluate substantive freedoms.** Hiring Jamie expands Jamie's capabilities (employment, income, dignity, community participation) more than hiring Alex expands Alex's capabilities (Alex has other options). A capabilities analysis focuses on which hiring decision most expands the least-advantaged person's freedom to achieve valuable functionings.

- Dimensions considered: $d_4$ (autonomy), $d_1$ (material capability), $d_6$ (social impact)
- Prediction: Hire Jamie (capabilities-maximizing)
- What it misses: The interaction between Maria's own capabilities and her employees', and the specific metric structure that determines how much each dimension matters

### The Geometric Analysis

Maria's hiring decision lives on the full 9-dimensional decision manifold. The two paths are:

**Path A (hire Alex):** $\Delta d_1 = +\text{high}$ (higher revenue), $\Delta d_3 \approx 0$ (no particular fairness issue), $\Delta d_5 = 0$ (no trust differential), $\Delta d_6 = -\text{small}$ (missed opportunity for community impact), $\Delta d_7 = -\text{small}$ (identity: "I could have helped but chose profit").

**Path B (hire Jamie):** $\Delta d_1 = -\text{moderate}$ (lower initial revenue, training costs), $\Delta d_3 = +\text{moderate}$ (giving opportunity to someone who needs it), $\Delta d_5 = +\text{moderate}$ (neighborhood trust strengthened), $\Delta d_6 = +\text{high}$ (community impact: local employment), $\Delta d_7 = +\text{moderate}$ (identity: "I am the kind of employer who invests in the neighborhood").

The edge weights are:

$$w_A = \frac{(\Delta d_6)^2}{\sigma_6^2} + \frac{(\Delta d_7)^2}{\sigma_7^2} + \text{cross terms}$$

$$w_B = \frac{(\Delta d_1)^2}{\sigma_1^2} - \text{covariance benefits from } d_3, d_5, d_6, d_7 \text{ improvements}$$

The Mahalanobis distance accounts for correlations: improvements on $d_5$ (trust) and $d_6$ (community impact) reduce the effective cost of the $d_1$ sacrifice, because trust and community impact are positively correlated with long-term revenue. The covariance matrix $\Sigma$ encodes this interaction.

**Prediction:** The geometric framework does not automatically favor Alex or Jamie. It specifies the *conditions* under which each is optimal. If Maria's covariance matrix weights $d_6$ and $d_7$ heavily (as it does for a community-oriented business owner in a gentrifying neighborhood), the Bond geodesic favors Jamie. If the covariance matrix is approximately diagonal with $\sigma_1^2 \gg \sigma_k^2$ for $k \neq 1$ (as it would for a purely profit-oriented owner), the Bond geodesic favors Alex. The framework makes the trade-offs explicit and computable.

**What each school was right about:** The classical school was right that monetary consequences matter ($d_1$). Behavioral economics was right that the decision involves more than cold calculation (but wrong to call the additional considerations "biases"). Institutional economics was right that the contractual and regulatory environment constrains the decision ($d_2$, $d_8$). The capabilities approach was right that substantive freedoms are at stake ($d_4$, $d_6$). The geometric framework unifies these insights by locating each school's contribution on the appropriate dimension of the decision manifold.

---

## 2.10 The Pattern

A pattern has emerged across these nine schools of economic thought. Each school:

1. **Discovered** one or more dimensions of the decision manifold.
2. **Studied** those dimensions in isolation, developing deep insight into how they function.
3. **Struggled** to explain phenomena that arise from the *interaction* between dimensions -- phenomena that require the full manifold, not just a single axis or a pair of axes.
4. **Generated** a research programme with important empirical findings but without the mathematical structure to connect those findings to the findings of other schools.

The geometric framework does not reject any of these schools. It provides the mathematical structure -- the manifold, the metric, the boundary penalties, the geodesic -- that connects them. Classical economics is the study of $d_1$. Behavioral economics is the empirical survey of metric asymmetry, curvature, and gauge violations. Bounded rationality is the theory of heuristic-guided search. Game theory is interaction on the scalar projection. Social choice theory (Arrow, Sen) is the study of dimensional collapse and its consequences. Information economics is the study of $d_9$ miscalibration. Commons governance is the study of boundary-penalty maintenance. Moral foundations theory is the empirical catalogue of the heuristic function's content. Experimental economics is the laboratory measurement of manifold structure under controlled conditions.

Each school has been drawing one face of the same geometric object. This book provides the object.

---

## Technical Appendix

**Theorem (Projected Intransitivity).** **[Conditional Theorem.]** Let $\succ_{\mathcal{E}}$ denote the preference relation on the full manifold ("$x \succ_{\mathcal{E}} y$ iff $w(v_0, x) < w(v_0, y)$") and let $\succ_\phi$ denote the projected preference ("$x \succ_\phi y$ iff $\phi(x) > \phi(y)$"). Then:

1. $\succ_{\mathcal{E}}$ is transitive (it is a total order induced by path cost from $v_0$).
2. $\succ_\phi$ may be intransitive: there exist alternatives $x, y, z$ such that $\phi(x) > \phi(y) > \phi(z) > \phi(x)$ is possible when the projection $\phi$ discards different dimensions for different pairwise comparisons.

*Proof sketch.* (1) Path cost $w(v_0, \cdot)$ is a real-valued function on vertices of $\mathcal{E}$; the induced ordering is a total preorder, hence transitive. (2) Consider three alternatives with attribute vectors $\mathbf{a}(x) = (3, 1, 5)$, $\mathbf{a}(y) = (5, 3, 1)$, $\mathbf{a}(z) = (1, 5, 3)$ in a 3-dimensional example. If $\phi$ is context-dependent -- comparing $x$ vs. $y$ on dimensions $\{1,2\}$ (where $y$ wins), $y$ vs. $z$ on dimensions $\{2,3\}$ (where $z$ wins), and $z$ vs. $x$ on dimensions $\{1,3\}$ (where $x$ wins) -- then $\succ_\phi$ is cyclic. On $\mathcal{E}$ with fixed metric, preferences are transitive; the intransitivity is an artifact of context-dependent projection.

**Historical Mapping.** **[Modeling Axiom.]** The following table maps each school's core mathematical commitment to its location on the decision manifold:

| School | Active Dimensions | Mathematical Object | Geometric Interpretation |
|---|---|---|---|
| Classical (vNM, Savage) | $d_1$ | Utility function $u: X \to \mathbb{R}$ | Coordinate function on $d_1$ |
| Behavioral (Kahneman-Tversky) | $d_1$ + metric anomalies | Value function $v(x)$, weighting $w(p)$ | Metric asymmetry, curvature |
| Bounded rationality (Simon, Gigerenzer) | All, via heuristics | Satisficing, fast-frugal heuristics | $h(n)$ in A* search |
| Game theory (Nash) | $d_1$ + strategic interaction | Nash equilibrium | Fixed point on scalar projection |
| Social choice (Arrow, Sen) | Multiple, aggregated | Impossibility theorem, capabilities | Dimensional collapse, manifold coordinates |
| Information economics (Akerlof, Stiglitz) | $d_5$, $d_9$ | Adverse selection, moral hazard | Manifold miscalibration |
| Commons governance (Ostrom) | $d_4$, $d_8$, $d_9$ | Design principles | Boundary-penalty calibration |
| Moral foundations (Haidt) | $d_3$, $d_4$, $d_5$, $d_7$, $d_8$ | Moral taste receptors | Heuristic function content |
| Experimental economics (Smith, Camerer) | Varies by setting | Laboratory data | Manifold measurement |

---

## Notes on Sources

The classical expected utility framework is presented in von Neumann and Morgenstern (1944), *Theory of Games and Economic Behavior*, and Savage (1954), *The Foundations of Statistics*. The behavioral economics canon includes Kahneman and Tversky (1979), "Prospect Theory," *Econometrica*; Kahneman (2011), *Thinking, Fast and Slow*; and Thaler and Sunstein (2008), *Nudge*. Simon's bounded rationality appears in Simon (1955), "A Behavioral Model of Rational Choice," *Quarterly Journal of Economics*; Gigerenzer's extension in Gigerenzer, Todd, and the ABC Research Group (1999), *Simple Heuristics That Make Us Smart*. Nash equilibrium is in Nash (1950), "Equilibrium Points in $n$-Person Games," *PNAS*. Arrow (1951), *Social Choice and Individual Values*; Sen (1999), *Development as Freedom*. Akerlof (1970), "The Market for 'Lemons'," *QJE*; Stiglitz and Weiss (1981), "Credit Rationing in Markets with Imperfect Information," *AER*. Ostrom (1990), *Governing the Commons*. Haidt (2012), *The Righteous Mind*. Smith (1962), "An Experimental Study of Competitive Market Behavior," *JPE*; Camerer (2003), *Behavioral Game Theory*. The geometric reinterpretations are developed in Bond (2026), "Geometric Economics," and Bond (2026), *Geometric Ethics*.
