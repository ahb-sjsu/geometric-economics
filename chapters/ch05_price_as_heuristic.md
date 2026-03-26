# Chapter 5: The Price Signal as Heuristic Field

> *"The most important single central fact about a free market is that no single person or committee needs to know all the relevant facts. The price system is a mechanism for communicating information."*
> -- Friedrich A. Hayek, "The Use of Knowledge in Society" (1945)

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria is staring at her wholesale invoice. Her Oakland roaster, Elena, has raised the price of fair-trade Ethiopian Yirgacheffe by 18%. Her System 1 fires instantly: this feels wrong -- she has been loyal to this supplier for six years, and the increase feels like it violates the relationship. Her System 2 opens a spreadsheet: current margin per cup is $2.10; the increase cuts it to $1.53; at 200 cups a day, that is $114/day in lost margin, $3,420/month.*
>
> *But the decision Maria faces is not "absorb or pass through." It is a pathfinding problem on a nine-dimensional manifold. Absorb the cost and her monetary position erodes ($d_1$). Pass the full increase to customers and she risks losing the price-sensitive regulars who are also her community ($d_6$). Switch to a cheaper, non-fair-trade supplier and she violates her identity as an ethical sourcer ($d_7$) and breaks faith with the Oakland roaster ($d_5$). Split the increase -- raise prices modestly, absorb some margin loss, and negotiate a smaller increase with the roaster -- and she navigates a path through the manifold that balances all nine dimensions.*
>
> *The price signal told her something was changing. But the price alone could not tell her what to do. For that, she needed the full evaluation function: $f = g + h$.*

---

## The Two Voices in Every Economic Decision

Every economic agent carries two decision systems. Daniel Kahneman, in *Thinking, Fast and Slow* (2011), called them System 1 and System 2. System 1 is fast, automatic, and effortless -- it is the voice that says "that price is outrageous" before you have done any arithmetic. System 2 is slow, deliberate, and effortful -- it is the voice that opens the spreadsheet, runs the numbers, and computes whether the price is actually above your break-even point.

Kahneman's framework transformed behavioral economics. But it left a critical question unanswered: what is the *mathematical relationship* between System 1 and System 2? Are they competing modules that sometimes cooperate and sometimes conflict? Is one rational and the other biased? When they disagree, which one is right?

The geometric framework provides a precise answer. System 1 and System 2 are not competing systems. They are *components of a single optimization algorithm*: A* search on the economic decision complex $\mathcal{E}$. System 2 computes $g(n)$ -- the accumulated cost from the starting state to the current node. System 1 computes $h(n)$ -- the heuristic estimate of the remaining cost to the goal. The decision is $f(n) = g(n) + h(n)$, not one or the other.

This identification is not a metaphor. It is a computational-level claim in the sense of David Marr's (1982) tri-level analysis: it specifies *what is computed* (the minimum-cost path on a nine-dimensional manifold) and *why* (optimality under resource constraints). The brain may implement this computation using satisficing, drift-diffusion processes, or fast-and-frugal heuristics at the algorithmic level -- the framework makes no claim about the neural implementation. The claim is that the *function being computed* is A* search, regardless of the algorithm that computes it.

This chapter develops that claim in detail. It defines economic decision-making as pathfinding, maps every component of A* search onto its economic counterpart, proves that moral and cultural heuristics are *admissible* search heuristics (not cognitive biases), and derives the precise conditions under which heuristic-guided economic reasoning is optimal, near-optimal, or genuinely biased.

## Economic Decision as Pathfinding

The starting point is the formal definition of an economic decision as a search problem.

> **Definition 6 (Economic Decision as Pathfinding).** An economic decision is a pathfinding problem on the economic decision complex $\mathcal{E}$:
>
> - **Start node** $v_0$: The agent's current economic state (endowment, obligations, relationships).
> - **Goal region** $G$: The set of states the agent prefers (higher wealth, fulfilled obligations, maintained relationships) -- *on all nine dimensions*.
> - **Path** $\gamma$: A sequence of actions (transactions, decisions) taking the agent from $v_0$ to a state in $G$.
> - **Cost function**: $f(n) = g(n) + h(n)$, where:
>   - $g(n)$ is the *accumulated cost* from $v_0$ to the current state $n$ -- the sum of edge weights along the path so far. This is the **System 2** component: explicit, deliberate cost-benefit calculation.
>   - $h(n)$ is the *heuristic estimate* of the remaining cost from $n$ to the nearest goal state in $G$ -- the agent's *intuitive assessment* of "how far I still need to go." This is the **System 1** component: fast, automatic, based on moral rules, cultural norms, and past experience.

This definition reframes every economic choice as a question about paths, not points. The classical economist asks: "Which outcome maximizes utility?" The geometric economist asks: "Which *path* through the decision manifold reaches the goal region at minimum total cost -- where cost is measured on all nine dimensions?"

The distinction matters. Two paths may reach the same monetary outcome ($d_1$) but at radically different costs on the other dimensions. A company that reaches $10M in revenue through fair dealing and one that reaches $10M through fraud arrive at the same $d_1$ destination, but the second has accumulated catastrophic costs on $d_2$ (rights violations), $d_5$ (trust destruction), $d_7$ (identity corruption), and $d_8$ (legitimacy erosion). The scalar economist sees identical outcomes. The geometric economist sees two paths with vastly different total costs -- and correctly predicts that the second path is unstable, because the accumulated non-monetary costs will eventually cascade back into $d_1$ (through lawsuits, loss of customers, regulatory action).

### The System 1 / System 2 Mapping

The correspondence between A* search and dual-process theory is not approximate. It is exact:

| A* Component | Economic Decision Counterpart |
|---|---|
| Start node $v_0$ | Current endowment / situation |
| Goal region $G$ | Desired economic outcome |
| Edge cost $w(v_i, v_j)$ | Full cost of action (all 9 dimensions) |
| $g(n)$: accumulated cost | System 2: deliberate cost-benefit analysis |
| $h(n)$: heuristic estimate | System 1: moral/cultural/intuitive assessment |
| Boundary penalty $\beta_k$ | Moral rule ("do not steal," "keep promises") |
| Open list | Options under consideration |
| Closed list | Options already evaluated and dismissed |
| Optimal path $\gamma^*$ | Chosen course of action |
| Path not found | Decision paralysis / no acceptable option |

Consider what each component does. The $g(n)$ function accumulates *actual costs* as the agent moves through the decision complex. This is the spreadsheet work: Maria knows she has spent $14,000 this month on rent, $6,200 on supplies, $9,800 on wages. These are recorded, verifiable, deliberate calculations. System 2 is slow because it operates on concrete data that must be retrieved, processed, and summed.

The $h(n)$ function estimates *remaining costs* from the current state to the goal. This is the intuitive assessment: Maria feels that switching to a non-fair-trade supplier would "cost too much" -- not in dollars, but in identity ($d_7$), trust ($d_5$), and community standing ($d_6$). She does not compute these costs; she *perceives* them, the way you perceive that a dark alley is dangerous without computing the conditional probability of assault. System 1 is fast because it operates on compressed, pre-computed estimates -- heuristics -- rather than on raw data.

The genius of A* search is that it combines both: $f(n) = g(n) + h(n)$. The decision is not "trust your gut" (use only $h$) or "run the numbers" (use only $g$). It is the sum. And the sum has a mathematical property that neither component has alone: when $h$ is *admissible* -- when it never overestimates the true remaining cost -- A* is guaranteed to find the optimal path.

### The Price Signal as Scalar Heuristic

Where does the *price signal* fit in this architecture? Prices are the most ubiquitous heuristic in economic life. When Maria sees that fair-trade Ethiopian Yirgacheffe costs $8.20 per pound and conventional Colombian costs $4.50 per pound, the prices are providing her with a *scalar estimate* of the cost of transitioning between states on the decision manifold.

But prices are heuristics about $d_1$ only. The price of a good does not encode its fairness ($d_3$), the labor conditions under which it was produced ($d_4$), the trust relationship with the supplier ($d_5$), or its environmental impact ($d_6$). The price is a *projection* of the full edge weight onto the monetary dimension:

$$h_{\text{price}}(n) = \pi_{d_1}(w(v_n, v_{\text{goal}}))$$

where $\pi_{d_1}$ is the projection onto the first coordinate.

This is why Hayek was both profoundly right and profoundly incomplete. Hayek argued that prices communicate dispersed information that no central planner could aggregate. This is correct -- on $d_1$. Prices are an extraordinarily efficient mechanism for communicating monetary cost-to-go. But they communicate *nothing* about the other eight dimensions. The price of a diamond does not encode the labor conditions in the mine. The price of a house does not encode the community it displaces. The price of carbon does not encode its intergenerational cost.

The geometric framework says: the price system is a heuristic field over the economic decision complex, but it is a heuristic on the *scalar projection*, not on the full manifold. An "efficient market" is one where the price heuristic is admissible *on $d_1$* -- prices never overestimate the true monetary cost of reaching the goal. But a market can be efficient on $d_1$ and catastrophically misleading on the full manifold. Surge pricing during a crisis is $d_1$-efficient and $d_3$-catastrophic. Pharmaceutical price gouging is $d_1$-rational and $d_7$-devastating. The price signal guides the search optimally *on the wrong manifold*.

## Moral Heuristics as Admissible Search Heuristics

We now arrive at the central theoretical claim of this chapter: moral and cultural heuristics -- "do not steal," "keep your promises," "reciprocate kindness," "charge a fair price" -- are not cognitive biases that contaminate rational economic calculation. They are *admissible search heuristics* that enable tractable computation on a nine-dimensional manifold.

### Admissibility

In A* search, a heuristic $h(n)$ is *admissible* if it never overestimates the true cost-to-go: $h(n) \leq h^*(n)$ for all nodes $n$, where $h^*(n)$ is the true minimum remaining cost on the full manifold. An admissible heuristic guarantees that A* finds the optimal path.

> **Theorem 7 (Heuristic Truncation Theorem).** *Let $h_M(n)$ be a moral heuristic -- a function that assigns high cost to actions violating moral rules and zero cost to actions consistent with them:*
>
> $$h_M(n) = \sum_k \beta_k \cdot P(\text{action from } n \text{ crosses boundary } k)$$
>
> *If the boundary penalties $\beta_k$ are lower bounds on the true moral cost of crossing boundary $k$ (i.e., $\beta_k \leq \beta_k^*$ where $\beta_k^*$ is the actual cost including legal penalty, social sanction, and psychological distress), then $h_M$ is admissible, and A* search with $h_M$ is guaranteed to find the optimal path on $\mathcal{E}$.*
>
> *Proof.* By construction, $h_M(n) \leq h^*(n)$: the true remaining cost includes the actual boundary penalties $\beta_k^*$ plus the Mahalanobis distance to the goal, both of which are non-negative. Since $\beta_k \leq \beta_k^*$ and the Mahalanobis component is non-negative, $h_M$ underestimates the true cost-to-go. By the admissibility theorem for A*, the search finds the optimal path. $\square$

This theorem reframes the entire relationship between moral intuition and economic calculation.

> **Corollary 8 (Moral Rules Are Not Biases).** *If moral heuristics are admissible search heuristics, then following them does not produce suboptimal behavior on the full manifold. It produces behavior that appears suboptimal only when projected onto a lower-dimensional subspace (e.g., scalar utility). Calling moral heuristics "biases" is a dimensional-projection error.*

The corollary is a direct challenge to the standard framing in behavioral economics. When an agent rejects an unfair offer in the ultimatum game, forgoing real money, behavioral economics catalogs this as a "bias" -- a deviation from rational self-interest. The geometric framework says: the behavior is optimal on the full manifold. It appears irrational only because the economist is projecting onto $d_1$. The "bias" is in the economist's projection, not in the agent's decision.

### When Heuristics Are Inadmissible

> **Remark 9 (When Heuristics Are Inadmissible).** Not all moral heuristics are admissible. A heuristic that *overestimates* moral cost -- e.g., excessive guilt, irrational fear of social disapproval, pathological risk aversion -- is inadmissible and may cause the search to miss the optimal path. This corresponds to *genuine* bias: the agent avoids options that are actually available. The framework distinguishes between rational heuristic use (admissible: the "bias" is in the projection, not the behavior) and genuine cognitive distortion (inadmissible: the heuristic itself is miscalibrated).

This distinction gives behavioral economics a sharper taxonomy. Instead of the blunt classification "rational vs. biased," we have:

1. **Admissible heuristic, observed on the full manifold**: The agent's behavior is optimal. No correction needed.
2. **Admissible heuristic, observed on the scalar projection**: The agent's behavior *appears* irrational. The error is in the observer's model, not in the agent.
3. **Inadmissible heuristic**: The agent's behavior is genuinely suboptimal. The heuristic overestimates cost and causes the agent to miss better paths. This -- and only this -- deserves the label "bias."

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria's System 1 tells her instantly that her landlord's 40% rent increase is unfair. This is $h(n)$ firing a fairness boundary penalty on $d_3$. Her gut says: "This is wrong. He is taking advantage of gentrification that my business helped create."*
>
> *Is this a bias? The classical economist says yes -- Maria should evaluate the rent increase purely on monetary terms ($d_1$). If the business remains profitable at the higher rent, she should pay it; if not, she should close or relocate.*
>
> *But Maria's fairness heuristic is admissible. The true cost of the rent increase on the full manifold includes the fairness violation ($d_3$), the trust erosion ($d_5$), the signal to other landlords in the district that they can extract similar increases ($d_6$, $d_8$), and the identity cost of accepting a deal she considers exploitative ($d_7$). These are real costs, not cognitive errors. Maria's System 1 is estimating them -- imprecisely, but as a lower bound. The heuristic underestimates the true manifold cost. It is admissible.*
>
> *Her System 2 then runs the spreadsheet ($g(n)$): current revenue, projected revenue at different price points, cost of relocating versus staying. The decision is $f = g + h$: the sum of the spreadsheet calculation and the moral-intuitive assessment. Neither alone gives the right answer.*

---

## The Admissibility Spectrum and Infinite Boundaries

### The Jean Valjean Problem

A natural and powerful objection arises at this point. Consider the moral rule "never steal." In the framework, this assigns $\beta_{\text{theft}} = \infty$ to the theft boundary. But the true cost of stealing a loaf of bread to survive is *finite* -- a small fine, a brief social sanction. So $h(n)$ has *overestimated* the true cost-to-go. The heuristic is inadmissible. And A* loses its optimality guarantee. Does this not invalidate the entire mapping?

No. The objection conflates two different cost functions, and the resolution illuminates the deepest feature of the framework.

> **Theorem 10 (Admissibility Depends on the Manifold).** *Let $h_\mathcal{E}^*(n)$ denote the true minimum remaining cost on the full manifold $\mathcal{E}$, and let $h_1^*(n)$ denote the true minimum remaining cost on the scalar projection $d_1$ alone. A moral heuristic $h_M(n)$ with $\beta_k = \infty$ for some boundary $k$ satisfies:*
>
> 1. *$h_M(n) \leq h_E^*(n)$ (admissible on the full manifold) whenever the true cost of crossing boundary $k$ on $\mathcal{E}$ -- including legal penalty, social sanction, psychological distress, identity damage, and downstream path costs on all nine dimensions -- is indeed infinite or exceeds $h_M(n)$.*
>
> 2. *$h_M(n) > h_1^*(n)$ (inadmissible on the scalar projection) whenever the monetary cost alone of crossing boundary $k$ is finite.*
>
> *The heuristic is admissible or inadmissible relative to the manifold on which optimality is defined.*

*Proof.* The true cost $h_\mathcal{E}^*(n)$ includes all nine dimensions. For the theft boundary, the true manifold cost includes: legal penalty ($d_1$, $d_4$: loss of liberty), social sanction ($d_6$: reputation destruction), identity cost ($d_7$: "I am a thief"), rights violation ($d_2$: criminal record creates lasting Hohfeldian disability), and epistemic cost ($d_9$: future uncertainty about consequences). For most agents, the sum of these costs across all dimensions is effectively unbounded -- a felony conviction forecloses entire regions of the decision manifold permanently. Thus $\beta_{\text{theft}} = \infty$ is not an overestimate on $\mathcal{E}$; it is a reasonable lower bound. On the scalar projection, only the monetary component ($d_1$) of this cost survives, and $h_M(n) > h_1^*(n)$. $\square$

The critic who objects that "never steal" overestimates the cost of theft is implicitly computing $h^*$ on the scalar projection $d_1$. On that manifold, the objection is correct -- and the conclusion is that Homo economicus *should* steal, which is empirically false. On the full manifold $\mathcal{E}$, $\beta_{\text{theft}} = \infty$ is admissible because the true cost of theft on $\mathcal{E}$ is effectively infinite for most agents in most contexts.

### Jean Valjean Steals Bread

For extreme cases, the framework predicts *exactly what we observe*. Consider Jean Valjean stealing bread to survive. The framework predicts that:

1. **$h(n)$ and $g(n)$ disagree.** The moral heuristic says "do not steal" ($h(n) = \infty$ for the theft path). But the accumulated cost of the non-theft path has become catastrophic: starvation drives $\Delta d_1 \to -\infty$ on the non-theft path. System 2 ($g(n)$) can compute that the alternative path cost exceeds $\beta_{\text{theft}}$ in this extreme case.

2. **The decision is agonizing, not automatic.** When $h(n)$ and $g(n)$ agree, decisions are fast and confident (most economic decisions). When they disagree -- when the heuristic screams "stop" but the accumulated cost screams "you must" -- the agent experiences intense moral conflict. This is precisely what we observe in Valjean's case: the decision to steal is not casual. It is a crisis.

3. **Society treats the transgression with nuance.** The community recognizes that the agent's manifold was distorted by starvation ($\Delta d_1 \to -\infty$ on the non-theft path), making the theft boundary the *lower-cost* path on the true manifold even though $\beta_{\text{theft}}$ is very large. The heuristic's overestimate is detected precisely because System 2 ($g(n)$) can compute that the alternative path cost exceeds $\beta_{\text{theft}}$ in this extreme case.

This is not a failure of the framework. It is one of its most striking predictions: moral heuristics are designed by evolution and culture to be *conservative overestimates* in the vast majority of cases (to prevent catastrophic boundary crossings), with the result that in rare extreme cases -- cases where the non-transgression path is genuinely more costly than the transgression -- the agent experiences *exactly the kind of agonizing moral conflict* that literature, law, and everyday experience document.

## $\varepsilon$-Admissibility and Bounded Suboptimality

Strict admissibility ($\beta_k \leq \beta_k^*$) guarantees optimal search. But evolution and culture did not design System 1 for strict admissibility. They designed it for something more practical.

> **Definition 11 ($\varepsilon$-Admissibility and Bounded Suboptimality).** A heuristic $h(n)$ is $\varepsilon$-admissible if $h(n) \leq (1 + \varepsilon) \cdot h^*(n)$ for all $n$. When A* uses an $\varepsilon$-admissible heuristic, the returned path has cost at most $(1 + \varepsilon)$ times the optimal path cost.

This is the key concept. Evolution did not need to find globally optimal decisions. It needed to find *good enough* decisions in constant time, without exploring the full nine-dimensional manifold. The solution: inflate boundary costs by a factor of $w = 1 + \varepsilon$ (overestimating sacred-value penalties), prune the search space catastrophically, find a near-optimal path in $O(1)$ time, and survive.

> **Theorem 12 (The Bounded Suboptimality Theorem).** *Evolution and culture did not design System 1 for strict admissibility (globally optimal decisions). They designed it for $\varepsilon$-admissibility with small $\varepsilon$: decisions that are provably close to optimal, computed in $O(1)$ time rather than the exponential time required for exact optimization. Specifically:*
>
> 1. **Infinite boundaries are strictly admissible on $\mathcal{E}$ in the common case.** *For boundaries whose true manifold cost is effectively infinite (theft, murder, incest), $\beta_k = \infty$ is a lower bound, hence admissible. The search is optimal.*
>
> 2. **Finite moral boundaries are $\varepsilon$-admissible.** *For boundaries whose true cost is large but finite (promise-breaking, queue-jumping, stinginess), the heuristic $\beta_k$ may slightly overestimate or underestimate $\beta_k^*$. Evolution calibrates $\beta_k$ via emotional feedback (guilt, shame, pride) to be close to $\beta_k^*$, yielding $\varepsilon$-admissibility with small $\varepsilon$.*
>
> 3. **Genuine biases are large-$\varepsilon$ errors.** *Phobias, framing effects, and probability-weighting errors correspond to heuristics where $\varepsilon$ is large -- the heuristic substantially over- or underestimates $h^*$. These are the only phenomena that deserve the label "bias."*

*Argument.* The computer science result is precise: standard A* guarantees a perfectly optimal path if and only if $h(n)$ never overestimates the true remaining cost ($h(n) \leq h^*(n)$ for all $n$). When this condition is relaxed, the algorithm *Weighted A** -- which uses $f(n) = g(n) + w \cdot h(n)$ with inflation weight $w > 1$ -- sacrifices perfect optimality in exchange for dramatically faster search: it finds a path guaranteed to cost at most $w$ times the optimum, while exploring exponentially fewer nodes. This is the exact trade-off that evolutionary biology faces. A brain that computed the globally optimal action on a 9-dimensional manifold with $\varepsilon = 0$ would require exhaustive search -- computationally intractable in the milliseconds available for predator avoidance, mate selection, or social negotiation. A brain that inflates moral boundary costs by a factor $w = 1 + \varepsilon$ (overestimating sacred-value penalties) prunes the search space catastrophically, finds a near-optimal path in $O(1)$ time, and survives. Human System 1 is weighted A*, not standard A*: it trades optimality for tractability.

The evolutionary logic is compelling. The fitness cost of crossing a sacred-value boundary (theft, betrayal, incest) is catastrophic: expulsion from the group, loss of cooperative partners, death. An organism that *underestimates* these costs (inadmissible in the other direction -- $\beta_k < \beta_k^*$) takes the "optimal" path through theft, is detected, and is eliminated from the gene pool. An organism that *overestimates* ($\beta_k > \beta_k^*$) pays a small opportunity cost but survives. Natural selection therefore produces heuristics that are biased toward overestimation of sacred-boundary costs -- i.e., toward *conservatively admissible* heuristics that may sacrifice global optimality but never cross a catastrophic boundary. This is precisely $\varepsilon$-admissible A* with $\varepsilon > 0$: the agent finds a near-optimal path that avoids catastrophic edges, at the cost of occasionally missing the true optimum. The suboptimality is bounded, and the bound is set by evolutionary calibration of $\beta_k$.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria's heuristic about fair pricing -- "I should not charge more than people can afford" -- is $\varepsilon$-admissible. It slightly overestimates the cost of raising prices (the true cost on $d_6$ of a small price increase is lower than her gut estimate), so she may underprice slightly relative to the full-manifold optimum. The suboptimality cost is small: she earns slightly less than she could while maintaining slightly more community goodwill than necessary.*
>
> *Her friend Carlos, who runs a tech startup, has the opposite miscalibration. His heuristic underestimates the cost of cutting corners on employee welfare ($d_4$, $d_5$). He is inadmissible on those dimensions -- his search misses paths that would produce better outcomes on the full manifold. His high employee turnover is not bad luck; it is the manifold correcting for his heuristic error.*

---

## The Hierarchy of Heuristic Quality

The framework classifies System 1 heuristics into a precise hierarchy:

> **Remark 13 (The Hierarchy of Heuristic Quality).** The framework classifies System 1 heuristics into a precise hierarchy:
>
> 1. **Strictly admissible** ($\beta_k \leq \beta_k^*$): the heuristic underestimates or exactly estimates the true boundary cost. The search is optimal. *Examples*: the taboo on murder, life imprisonment, complete social exclusion, where the true cost (execution, life imprisonment, complete social exclusion) genuinely exceeds any finite heuristic estimate.
>
> 2. **$\varepsilon$-admissible** ($\beta_k \leq (1 + \varepsilon)\beta_k^*$): the heuristic slightly overestimates. The search finds a near-optimal path. *Examples*: most social-norm heuristics (tipping, queue etiquette, gift reciprocity).
>
> 3. **Inadmissible** ($\beta_k \gg \beta_k^*$): the heuristic substantially overestimates. The search may miss genuinely good paths. *Examples*: phobias (irrationally high $\beta$ for harmless stimuli), excessive guilt, pathological risk aversion.
>
> 4. **Gauge-variant** ($\beta_k$ depends on framing, not on the state): the heuristic is not even a consistent function of the manifold position. *Examples*: framing effects, anchoring, availability bias.

Categories 1-2 are features of the architecture. Categories 3-4 are genuine cognitive errors. Behavioral economics has conflated all four categories under the single label "bias." The geometric framework separates them -- and in doing so, reveals that most of what behavioral economics calls "irrational" falls into categories 1 and 2: optimal or near-optimal behavior on the full manifold, misidentified as bias because the observer is computing on the wrong manifold.

This is the framework's strongest empirical claim about heuristics: the *majority* of documented "biases" in the behavioral economics literature are admissible or $\varepsilon$-admissible heuristics operating on the full decision manifold. They appear irrational only when evaluated on the $d_1$ projection. The *minority* -- phobias, framing effects, probability-weighting errors -- are genuinely inadmissible or gauge-variant, and these are the only phenomena that warrant the label "bias" in the technical sense.

## The Price Signal Reconsidered

With the A* framework in hand, we can now give a precise geometric account of the price signal.

### Prices as $d_1$-Heuristics

The price of a good or service is a scalar estimate of the $d_1$ cost of a transition on the economic decision manifold. When Maria sees that a pound of coffee beans costs $8.20, the price is telling her: "The monetary cost of transitioning from the state 'I do not have these beans' to the state 'I have these beans' is approximately $8.20 along $d_1$."

This is a heuristic in the technical A* sense: it estimates the cost-to-go without requiring the agent to trace through the full sequence of intermediate states (sourcing, shipping, roasting, packaging, retailing). The market aggregates this information and presents it as a single number.

### The Efficient Market Hypothesis as Admissibility

Hayek's claim that prices communicate dispersed information is, in the geometric framework, the claim that the price heuristic is *admissible on $d_1$*: prices do not systematically overestimate the true monetary cost of reaching the goal. The Efficient Market Hypothesis, in its strongest form, is the claim that $h_{\text{price}}(n) = h_1^*(n)$ -- the price heuristic is not merely admissible but *exact* on the monetary dimension.

The framework immediately reveals the limitation: even a perfectly efficient market (exact $d_1$ heuristic) provides no information about the other eight dimensions. The price of a good does not encode:

- $d_2$: Whether its production violated property rights or contractual obligations
- $d_3$: Whether the price is fair relative to production cost and worker compensation
- $d_4$: Whether the buyer has genuine alternatives or is choosing under coercion
- $d_5$: Whether the seller's claims about quality are trustworthy
- $d_6$: Whether the production process damaged communities or ecosystems
- $d_7$: Whether purchasing the good is consistent with the buyer's identity and values
- $d_8$: Whether the transaction complies with the spirit (not just the letter) of regulations
- $d_9$: Whether the buyer has adequate information to assess what they are getting

Market failures, in this framing, are not failures of the price mechanism to clear markets. They are failures of the price heuristic to capture manifold dimensions that are relevant to the agent's actual decision problem. An externality is a $d_6$ cost that the price heuristic ignores. Information asymmetry is a $d_9$ miscalibration. Coercive pricing is a $d_4$ violation invisible to $d_1$. Each "market failure" cataloged by welfare economics is a specific dimensional gap between the price heuristic and the full-manifold cost.

### Why Some Markets "Behave Classically" and Others Don't

The framework generates a sharp prediction: markets will approximate the classical model when the active dimensions of the decision collapse to $d_1$ alone, and will deviate systematically when additional dimensions are active.

Consider:

- **Anonymous commodity markets** (wheat futures, currency exchange): The participants are trading standardized goods with no personal relationship, no fairness norm beyond the contract, no identity stake, and no community impact. Dimensions $d_3$ through $d_9$ are effectively zero. The decision manifold collapses to $d_1$. Price is the only relevant heuristic. Classical prediction is accurate.

- **Labor markets**: Workers care about wages ($d_1$) but also about autonomy ($d_4$), trust in the employer ($d_5$), social status ($d_6$), alignment with identity ($d_7$), and procedural fairness ($d_3$). The decision manifold is high-dimensional. Price (wage) is a $d_1$ heuristic that misses most of the structure. Classical prediction fails systematically: workers accept lower-paying jobs that score higher on other dimensions; they refuse higher-paying jobs that violate identity or fairness constraints.

- **Medical markets**: Patients face decisions where $d_1$ (cost) interacts with $d_4$ (autonomy over one's body), $d_5$ (trust in the physician), $d_6$ (impact on family), $d_7$ (identity -- "the kind of patient I am"), and $d_9$ (epistemic uncertainty about outcomes). The manifold is maximally high-dimensional. Price is nearly irrelevant to the decision architecture. Classical prediction is maximally wrong: patients routinely choose more expensive treatments that preserve autonomy, maintain trust, and align with identity.

The pattern is not random. It is predicted by the dimensionality of the active manifold. Tell me which dimensions are active, and I will tell you whether the price heuristic is sufficient or misleading. This is a falsifiable claim.

## Worked Example: Maria's Coffee Pricing Decision

Let us work through a complete A* analysis of a concrete economic decision: Maria is considering whether to raise her coffee prices from $4.50 to $5.00 per cup in response to her supplier's 18% cost increase.

### Step 1: Define the Search Space

**Start node** $v_0$: Maria's current state.
- $d_1$: Revenue $18,900/month; costs $17,500/month; margin $1,400/month
- $d_3$: Prices perceived as fair by customers and community
- $d_5$: High trust with regulars and supplier
- $d_6$: Community anchor -- known gathering place for neighborhood
- $d_7$: Identity as ethical, community-oriented business owner

**Goal region** $G$: A state where the business remains viable ($d_1$ positive), relationships are maintained ($d_5$, $d_6$), identity is preserved ($d_7$), and fairness norms are respected ($d_3$).

### Step 2: Enumerate the Paths

**Path A: Absorb the full cost increase.** No price change; margin drops to roughly $-$2,020/month (from $1,400 to -$620 after the $3,420/month cost increase from the 18% supplier price hike on $19,000 of annual bean costs). Business becomes unsustainable within months.

| Dimension | $\Delta$ | Assessment |
|-----------|----------|------------|
| $d_1$ | $-3,420$/month | Catastrophic: business closes in ~4 months |
| $d_3$ | 0 | Prices unchanged; fairness maintained |
| $d_5$ | 0 | Customer trust maintained |
| $d_6$ | $-\infty$ (delayed) | Business closure destroys community hub |
| $d_7$ | $+$ slight | Maintains "I don't pass costs to customers" identity |

Total cost: Very high. The $d_1$ catastrophe eventually cascades to $d_6$ (closure), making this path dominated despite its short-term preservation of $d_3$ and $d_5$.

**Path B: Pass the full cost increase ($4.50 $\to$ $5.50/cup).** A $1.00 increase covers the cost increase and adds margin.

| Dimension | $\Delta$ | Assessment |
|-----------|----------|------------|
| $d_1$ | +$2,580/month | Strong: margin increases to $3,980 |
| $d_3$ | $-$ large | 22% price jump feels unfair; crosses fairness boundary |
| $d_5$ | $-$ moderate | Price-sensitive regulars feel betrayed |
| $d_6$ | $-$ moderate | Some community members priced out |
| $d_7$ | $-$ slight | "I raised prices sharply" conflicts with self-image |

Total cost: The $d_1$ gain is offset by boundary penalties on $d_3$ (fairness threshold crossed for a jump over 15%) and friction on $d_5$ and $d_6$. The edge weight $w_B$ includes $\beta_{\text{fairness}}$ for the sharp increase.

**Path C: Moderate increase ($4.50 $\to$ $5.00/cup) + negotiate with supplier + slight menu adjustment.** Raise prices by $0.50, negotiate a 5% reduction in the supplier's increase (from 18% to 13%), and slightly reduce the proportion of the most expensive beans in the house blend.

| Dimension | $\Delta$ | Assessment |
|-----------|----------|------------|
| $d_1$ | +$600/month | Modest improvement; margin $2,000/month |
| $d_3$ | $-$ slight | 11% increase is within the "fair adjustment" range |
| $d_5$ | 0 | Regulars understand cost pressures; supplier relationship preserved |
| $d_6$ | 0 | No customers priced out |
| $d_7$ | 0 | Consistent with "reasonable business owner" identity |

Total cost: Low friction on all dimensions. No boundary penalties triggered. The Mahalanobis distance from $v_0$ to the goal state is minimized.

**Path D: Switch to cheaper non-fair-trade supplier.** Drop the Oakland roaster entirely and source conventional beans at 45% lower cost.

| Dimension | $\Delta$ | Assessment |
|-----------|----------|------------|
| $d_1$ | +$4,200/month | Excellent: margin jumps to $5,600 |
| $d_3$ | $-$ moderate | Abandoning fair-trade sourcing feels unfair to growers |
| $d_5$ | $-\infty$ | Destroys six-year trust relationship with Oakland roaster |
| $d_6$ | $-$ moderate | Impact on supplier's workers and community |
| $d_7$ | $-$ large | Violates core identity as ethical sourcer |

Total cost: The $d_5$ boundary penalty ($\beta_{\text{trust}} = \infty$ for a complete betrayal of a six-year relationship) makes this path infinitely costly on the full manifold, despite its $d_1$ superiority. Homo economicus chooses Path D. Maria does not -- and she is right.

### Step 3: Compute $f = g + h$ for Each Path

For each path, System 2 computes $g(n)$ (the accumulated monetary costs and benefits) and System 1 computes $h(n)$ (the heuristic estimate of remaining costs on all dimensions):

| Path | $g(n)$ (System 2) | $h(n)$ (System 1) | $f(n) = g + h$ | Rank |
|------|-------------------|--------------------|-----------------|------|
| A: Absorb all | Very high (bankruptcy) | Low (no boundaries crossed) | Very high | 4th |
| B: Full pass-through | Low (strong $d_1$) | High (fairness boundary) | Moderate-high | 3rd |
| C: Moderate + negotiate | Moderate ($d_1$ OK) | Low (no boundaries) | **Lowest** | **1st** |
| D: Switch supplier | Lowest ($d_1$ optimal) | Infinite (trust boundary) | Infinite | Last |

A* search selects **Path C** -- the moderate increase with negotiation. This is the Bond geodesic: the minimum-cost path on the full manifold.

### Step 4: What the Scalar Economist Misses

A $d_1$-only analysis ranks the paths: D > B > C > A. Homo economicus switches suppliers. The geometric analysis ranks them: C > B > A > D. The optimal path on the full manifold is *third-best* on the monetary projection. The discrepancy is not noise. It is the information content of eight dimensions that the scalar discards.

Note that Maria's actual decision process matches the geometric prediction, not the scalar prediction. She does not run a formal optimization. She "considers the options" (generates paths), "sleeps on it" (lets System 1 process the heuristic costs), "runs some numbers" (System 2 computes $g$), and arrives at the moderate increase -- the path that *feels right and works financially*. The feeling and the arithmetic are not in conflict. They are $h$ and $g$, components of a single evaluation function.

## Heuristic Fields Over the Decision Complex

We can now generalize from individual prices to the concept of a *heuristic field* -- a function defined over the entire economic decision complex that estimates the cost-to-go from any state.

### The Price Field

The price system defines a scalar field $h_{\text{price}}: V(E) \to \mathbb{R}$ over the vertices of the decision complex. At each economic state $v$, $h_{\text{price}}(v)$ estimates the monetary cost of reaching the goal. This field has the properties of a classical potential field: agents move in the direction of decreasing $h_{\text{price}}$, and equilibrium occurs where the gradient vanishes.

Hayek's insight is that this field is *decentralized*: no single agent computes it. Instead, it emerges from the aggregation of all agents' local information through market transactions. The price field is the emergent heuristic of a distributed computation.

### The Moral-Heuristic Field

But prices are not the only heuristic field on $\mathcal{E}$. Cultural norms, moral rules, and social expectations define additional fields:

- **The fairness field** $h_{\text{fair}}: V(E) \to \mathbb{R}$ estimates the $d_3$ cost of reaching the goal from any state. It assigns high cost to states where the agent has taken unfair advantage or been unfairly treated.
- **The trust field** $h_{\text{trust}}: V(E) \to \mathbb{R}$ estimates the $d_5$ cost. It assigns high cost to states where trust has been broken or relationships damaged.
- **The identity field** $h_{\text{identity}}: V(E) \to \mathbb{R}$ estimates the $d_7$ cost. It assigns high cost to states inconsistent with the agent's self-image.

The total heuristic is the sum over all active fields:

$$h(n) = h_{\text{price}}(n) + h_{\text{fair}}(n) + h_{\text{trust}}(n) + h_{\text{identity}}(n) + \cdots$$

This is why economic decisions "feel" multi-dimensional: the agent is simultaneously consulting multiple heuristic fields, each estimating cost on a different dimension of the manifold. System 1 integrates these estimates into a single $h(n)$ -- the "gut feeling" about a decision -- which System 2 then combines with the computed $g(n)$ to produce the total evaluation $f(n)$.

### Heuristic Calibration and Cultural Variation

Different cultures calibrate their moral-heuristic fields differently. The Mahalanobis weights in the covariance matrix $\Sigma$ determine how strongly each heuristic field contributes to the total $h(n)$.

In cultures with high market integration and strong rule of law (Henrich et al.'s Western undergraduate samples), the price field dominates: $h_{\text{price}}$ receives high weight, while $h_{\text{fair}}$ and $h_{\text{trust}}$ receive lower weights. Economic decisions in such contexts approximate the classical model because the $d_1$ heuristic dominates the sum.

In cultures with low market integration and high cooperative dependence (Henrich et al.'s Lamelara whale-hunting community), the trust and social-impact fields dominate: $h_{\text{trust}}$ and $h_{\text{social}}$ receive high weights. Economic decisions in such contexts deviate sharply from classical predictions because the non-$d_1$ heuristics dominate the sum.

The cross-cultural variation in economic behavior -- documented by Henrich, Boyd, Bowles, Camerer, Fehr, Gintis, and McElreath (2001, 2005) -- is not random. It is predicted by the relative weights of the heuristic fields, which are in turn calibrated by the culture's ecological and social environment. The framework does not explain this variation post hoc; it predicts it from the metric structure.

## The Interaction of System 1 and System 2

### When They Agree

In most economic decisions, $h(n)$ and $g(n)$ point in the same direction. The gut feeling ("this is a good deal") aligns with the arithmetic ("the numbers work"). In these cases, decisions are fast and confident. The agent does not experience conflict because the heuristic and the accumulated cost agree on the minimum-cost path.

This is the *typical* case, not the exception. Most grocery purchases, routine business transactions, and standard economic exchanges occur in regions of the decision manifold where the moral-heuristic field is smooth and the price field is a good approximation to the full cost. The classical model works in these regions precisely because the additional dimensions add little to the $d_1$ heuristic.

### When They Disagree

The interesting cases are those where System 1 and System 2 conflict -- where the gut says "no" but the numbers say "yes," or vice versa.

**System 1 says no, System 2 says yes.** Maria's landlord offers a deal: if she signs a ten-year lease at the 40% higher rent, he will guarantee no further increases for the decade. System 2 computes that this is financially advantageous over the long term (the net present value of the guarantee exceeds the cost of the higher rent). But System 1 fires a fairness alarm: "He is locking me into an exploitative rate by dangling stability."

In this case, $g(n)$ is low (good deal on $d_1$) but $h(n)$ is high (fairness and trust costs). The question is whether $h(n)$ is admissible. If the fairness alarm is tracking a real manifold cost -- for instance, if signing the lease at an exploitative rate damages Maria's negotiating position with other vendors ($d_5$), signals to the community that she accepts unfair treatment ($d_6$), or erodes her self-respect ($d_7$) -- then the heuristic is admissible and Maria should trust it. If the alarm is a mis-calibrated overreaction to any rent increase, then the heuristic is inadmissible and Maria should override it.

**System 1 says yes, System 2 says no.** A customer offers to buy Maria's entire stock of specialty beans at double the retail price for a corporate event. System 1 says: "Great opportunity!" System 2 computes: if she sells all the specialty stock, she cannot serve her regular customers for three days until the next shipment arrives. The regulars -- her community, her $d_6$ base -- will go elsewhere and some may not return.

Here $h(n)$ is low (the deal *feels* good on $d_1$) but $g(n)$ is high when all dimensions are traced forward. System 1's heuristic is inadmissible because it is responding to the immediate $d_1$ gain without estimating the downstream costs on $d_5$ and $d_6$. This is a genuine case where deliberate System 2 analysis should override intuition -- precisely because the heuristic is failing to estimate the full-manifold cost.

### Marr's Levels of Analysis

A critical clarification is necessary. The claim that economic decision-making is A* search must be understood at the correct level of David Marr's (1982) tri-level analysis:

- **Computational level** (what is computed and why): A* search on the decision manifold -- the agent finds the minimum-cost path given a heuristic. This is our claim.
- **Algorithmic level** (how it is computed): The brain may use satisficing, fast-and-frugal heuristics (Gigerenzer), accumulator models, or drift-diffusion processes that are algorithmically very different from A* but converge to the same computational-level solution. We make no claim here.
- **Implementational level** (the neural substrate): Which circuits, neurotransmitters, and brain regions execute the computation. We make no claim here.

The framework predicts the *outcome* of the computation (which path the agent selects); it does not predict the neural implementation of the selection process. Cognitive scientists who object that "the brain does not run A*" are objecting at Marr's algorithmic level, while the framework's claims are at the computational level. The two are compatible.

## Implications for Economic Policy

### Market Design as Heuristic Engineering

If the price signal is a heuristic field, then market design is *heuristic engineering*: the construction of institutional structures that make the price heuristic a better approximation to the full-manifold cost.

A carbon tax adds $d_6$ costs to the price heuristic: the price of carbon-intensive goods now partially reflects their environmental impact, making $h_{\text{price}}$ a better estimate of the full edge weight. Fair-trade certification adds $d_3$ and $d_4$ information to the price: consumers can distinguish goods produced under fair conditions from those that were not, improving the heuristic's coverage beyond $d_1$.

Disclosure requirements (nutrition labels, financial product disclosures, environmental impact reports) are attempts to make the price heuristic less inadmissible on $d_9$ (epistemic status): they provide information that allows the agent to better estimate the cost-to-go on dimensions the price does not capture.

In every case, the policy intervention has the same geometric structure: *it improves the admissibility of the price heuristic by incorporating information from dimensions that the unregulated price ignores*. The framework provides a unifying language for diverse policy tools that appear unrelated in classical analysis.

### When to Trust the Heuristic, When to Override

The hierarchy of heuristic quality (Remark 13) provides a practical decision rule:

1. **If the heuristic is strictly admissible** (the moral rule tracks a genuinely infinite or very large boundary cost): *follow it*. "Do not steal" is not a bias. "Do not exploit captive customers" is not a bias. These rules are tracking real costs that the spreadsheet cannot see.

2. **If the heuristic is $\varepsilon$-admissible** (the moral intuition slightly overestimates the true cost): *follow it unless the overestimate is clearly identifiable*. Tipping 20% when 15% would suffice is a small $\varepsilon$-overestimate of the social cost of undertipping. The suboptimality is bounded and the social-norm preservation is worth the small monetary cost.

3. **If the heuristic is inadmissible** (a genuine phobia, excessive guilt, or pathological risk aversion is causing the agent to avoid options that are actually available): *override it*. This requires System 2 to identify the heuristic failure -- which is exactly what therapy, financial advising, and good mentorship do.

4. **If the heuristic is gauge-variant** (the intuition changes depending on how the problem is framed, not on its actual content): *pause and reframe*. Framing effects are the clearest signal that the heuristic is not tracking the manifold but is instead responding to surface features of the description. The remedy is to re-describe the decision in multiple frames and check for consistency.

---

## Worked Example: Why People Don't Steal (The Grocery Store Revisited)

To solidify the A* interpretation, consider the economic decision that classical economics cannot explain: why people do not steal.

An agent stands in a grocery store. Two paths are available:

**Path A (buy):** Pay $50. Attribute-vector change: $\Delta d_1 = -50$, all other dimensions $\approx 0$. Edge weight: $w_A = 50^2 / \sigma_1^2$ (Mahalanobis distance on $d_1$ alone).

**Path B (steal):** Pay $0. Attribute-vector change: $\Delta d_1 = 0$, but $\Delta d_2 = -\infty$ (rights violation), $\Delta d_6 = -\text{large}$ (social sanction risk), $\Delta d_7 = -\text{large}$ (identity violation). Edge weight: $w_B = \infty$ (boundary penalty dominates).

Under scalar utility ($\phi = d_1$): $\phi(B) > \phi(A)$, so Homo economicus steals.

On the full manifold: $w_B = \infty > w_A$, so the rational agent buys.

The agent's moral heuristic $h_M$ assigns $\beta_{\text{theft}} = \infty$ to Path B. This is admissible on $\mathcal{E}$ because the true cost of theft -- legal penalty, social sanction, identity damage, rights violation, epistemic uncertainty about future consequences -- is effectively unbounded for most agents. The agent is not "irrational" for buying. The economist is computing on the wrong manifold.

In A* terms: System 1 immediately assigns $h(B) = \infty$, removing Path B from the open list. System 2 never needs to evaluate it. The search terminates instantly at Path A. This is why the decision to buy rather than steal is not experienced as a *decision* at all -- the heuristic prunes the theft path before deliberation begins. We do not stand in grocery stores agonizing over whether to pay. The heuristic is so strongly admissible, and the boundary penalty so clearly infinite, that the path is never even generated.

The only cases where the theft path enters deliberation are those where the non-theft path cost approaches infinity: Jean Valjean's bread, the parent stealing medicine for a dying child. These are the cases where $g(A) \to \infty$ on the non-theft path, making the A* evaluation $f(A) = g(A) + h(A) > f(B) = g(B) + h(B)$ even though $h(B) = \beta_{\text{theft}}$ is very large. The framework predicts that these cases produce agonizing moral conflict (large $h(B)$ fighting against large $g(A)$), which is exactly what we observe.

---

## Technical Appendix

### A* Search: Formal Definition

**[Established Mathematics.]** A* search (Hart, Nilsson, Raphael, 1968) is a best-first graph search algorithm. Given a weighted graph with start node $v_0$ and goal set $G$:

1. Initialize the *open list* with $v_0$, setting $g(v_0) = 0$ and $f(v_0) = h(v_0)$.
2. Select the node $n$ from the open list with the lowest $f(n) = g(n) + h(n)$.
3. If $n \in G$, return the path from $v_0$ to $n$. Terminate.
4. For each neighbor $n'$ of $n$:
   - Compute $g(n') = g(n) + w(n, n')$.
   - Compute $f(n') = g(n') + h(n')$.
   - If $n'$ is not on the open list or the new $g(n')$ is lower, add/update $n'$ on the open list.
5. Move $n$ to the *closed list*. Go to step 2.

**Theorem (A* Optimality).** If $h(n) \leq h^*(n)$ for all $n$ (admissibility) and $h$ is consistent ($h(n) \leq w(n, n') + h(n')$ for all edges), then A* finds the minimum-cost path from $v_0$ to $G$.

### Weighted A* and the Optimality-Tractability Tradeoff

**[Established Mathematics.]** Weighted A* uses $f(n) = g(n) + w \cdot h(n)$ with $w > 1$. The algorithm finds a path with cost at most $w$ times the optimal cost, while exploring at most $O(N / w)$ nodes compared to standard A* (Pohl, 1970). The tradeoff is:

| Weight $w$ | Optimality guarantee | Search space explored |
|------------|---------------------|-----------------------|
| $w = 1$ | Exact optimal | Full (exponential worst case) |
| $w = 1 + \varepsilon$ | $(1 + \varepsilon)$-optimal | Dramatically reduced |
| $w \to \infty$ | Greedy (no guarantee) | Minimal (follows heuristic blindly) |

Human System 1 operates with $w > 1$ (weighted A*): it inflates heuristic estimates to prune the search space, trading bounded suboptimality for computational tractability. The inflation weight $w$ is calibrated by evolution and cultural learning to be close to 1 for common decisions and larger for novel or high-stakes decisions where the heuristic is less reliable.

### The Admissibility Theorem Applied to Economics

**[Conditional Theorem.]** Let the economic decision complex $\mathcal{E}$ have edge weights $w(v_i, v_j) = \Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a} + \sum_k \beta_k \cdot \mathbf{1}[\text{boundary } k \text{ crossed}]$. Let $h_M(n) = \sum_k \beta_k \cdot P(\text{path from } n \text{ crosses boundary } k)$ be the moral heuristic. Then:

1. $h_M$ is admissible on $\mathcal{E}$ if and only if $\beta_k \leq \beta_k^* + \Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a}$ for all boundaries $k$ that the optimal path crosses.

2. $h_M$ is $\varepsilon$-admissible on $\mathcal{E}$ if $\beta_k \leq (1 + \varepsilon)(\beta_k^* + \Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a})$ for all $k$.

3. $h_M$ is inadmissible on the scalar projection $d_1$ whenever $\beta_k > 0$ and the monetary cost of crossing boundary $k$ is less than $\beta_k$. This is the source of the "irrationality" label: the behavior appears suboptimal on $d_1$ because the heuristic includes costs that the $d_1$ projection discards.

### Simon's Bounded Rationality, Formalized

Herbert Simon (1955) proposed that agents *satisfice* -- they choose the first option that exceeds an aspiration level -- because they lack the computational resources for full optimization. The framework formalizes this: satisficing is the limiting case of weighted A* with $w \to \infty$, where the agent follows the heuristic greedily and terminates at the first goal-region state encountered. The aspiration level is the boundary of the goal region $G$. When $w = \infty$, the search explores only the greedy path and accepts any state in $G$ -- exactly satisficing behavior.

The framework interpolates between Simon and the neoclassical model:

| $w$ value | Economic behavior | Traditional name |
|-----------|-------------------|-----------------|
| $w = 1$ | Perfect optimization | Homo economicus |
| $1 < w < \infty$ | Near-optimal heuristic search | Bounded rationality |
| $w = \infty$ | Greedy heuristic following | Satisficing |

Simon was right that agents do not optimize perfectly. The neoclassical economists were right that the behavior has a rational structure. Both were describing the same algorithm at different parameter values. The framework unifies them by showing that the difference is a single parameter $w$ that trades optimality for tractability.

### Gigerenzer's Fast-and-Frugal Heuristics

Gerd Gigerenzer's research program (Gigerenzer & Goldstein, 1996; Gigerenzer, Todd, & the ABC Research Group, 1999) demonstrated that simple heuristics can outperform complex optimization in uncertain environments -- the "less is more" effect.

In the geometric framework, Gigerenzer's heuristics are specific implementations of $h(n)$ that exploit environmental structure. The "recognition heuristic" (choose the recognized alternative) is an $h(n)$ that assigns lower cost-to-go to states associated with familiar entities -- admissible in environments where familiarity correlates with quality. The "take-the-best" heuristic (choose on the single most discriminating cue) is an $h(n)$ that projects the full manifold onto the dimension with the highest diagnostic value -- a dimensionally reduced heuristic that is admissible when the projection captures most of the variance.

Gigerenzer showed empirically that these heuristics work. The geometric framework shows *why*: they are admissible or $\varepsilon$-admissible projections of the full-manifold cost function, designed by evolution to exploit the statistical structure of the environments in which they evolved.

---

## Notes on Sources

The dual-process theory of System 1 and System 2 is developed in Kahneman (2011), *Thinking, Fast and Slow*. The computational-level interpretation follows Marr (1982), *Vision*. The A* search algorithm is due to Hart, Nilsson, and Raphael (1968), "A Formal Basis for the Heuristic Determination of Minimum Cost Paths," *IEEE Transactions on Systems Science and Cybernetics*. Weighted A* and $\varepsilon$-admissibility are developed in Pohl (1970), "Heuristic Search Viewed as Path Finding in a Graph," *Artificial Intelligence*.

Hayek's account of the price system as information aggregation appears in "The Use of Knowledge in Society" (1945), *American Economic Review*. The Efficient Market Hypothesis originates with Fama (1970), "Efficient Capital Markets," *Journal of Finance*. The geometric reinterpretation -- prices as admissible $d_1$ heuristics -- is original to this framework.

Simon's bounded rationality is developed in "A Behavioral Model of Rational Choice" (1955), *Quarterly Journal of Economics*, and *Models of Bounded Rationality* (1982). Gigerenzer's fast-and-frugal heuristics program is summarized in Gigerenzer, Todd, and the ABC Research Group (1999), *Simple Heuristics That Make Us Smart*. The unification of satisficing and optimization as parameter values of a single algorithm (weighted A*) is original to this framework.

The cross-cultural data on economic game behavior is from Henrich et al. (2001), "In Search of Homo Economicus," *American Economic Review*; and Henrich et al. (2005), "Economic Man in Cross-Cultural Perspective," *Behavioral and Brain Sciences*. The interpretation of cultural variation as metric variation in the heuristic field weights is original to this framework.
