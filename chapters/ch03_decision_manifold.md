# Chapter 3: The Economic Decision Manifold

> *"The first step toward wisdom is calling things by their right name."*
> -- Confucius (attributed)

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria is thinking about hiring a new barista. On the surface, this looks like a simple business decision: can she afford the salary? But sit with Maria for an hour as she thinks it through, and you will hear her navigate a space far richer than a profit-and-loss statement.*
>
> *"The salary is $3,200 a month -- I can cover it if the weekend traffic holds" -- that is $d_1$, monetary cost. "I'd need to put them on a real contract, not just day-to-day like last time" -- that is $d_2$, contractual obligation. "I want to pay at least $18 an hour; anything less isn't right for this city" -- that is $d_3$, fair wage. "They need to be able to set their own pace behind the counter, not be micromanaged" -- that is $d_4$, worker autonomy. "Can I trust this person with the register, the keys, the customers?" -- that is $d_5$, trust in the hire. "If I hire from the neighborhood, that matters; people notice" -- that is $d_6$, community impact. "I want to be the kind of employer people are proud to work for" -- that is $d_7$, Maria's identity as employer. "I need to make sure everything is above board -- payroll taxes, workers' comp, the whole thing" -- that is $d_8$, regulatory compliance. "But honestly, I don't know if the neighborhood is going to keep gentrifying or if there's a downturn coming" -- that is $d_9$, uncertainty about business outlook.*
>
> *Nine dimensions. One decision. The economic decision manifold is the space that Maria is actually navigating. This chapter gives it a name and a mathematical structure.*

---

## The Space Where Decisions Live

Every economic decision lives somewhere. Classical economics says it lives on a line: the real-valued utility axis, where the agent picks the point with the highest number. This book says it lives in a richer space -- a space with nine dimensions, a metric that encodes how those dimensions interact, and boundaries where the rules change discontinuously.

This chapter constructs that space. We define the economic decision complex $\mathcal{E}$, identify its nine dimensions, explain why nine and not one (or three, or thirty), define the multi-dimensional edge weights that encode the cost of moving between states, and characterize the moral-economic boundaries that partition the manifold into regimes. The construction is formal, but the motivation is practical: every definition corresponds to something that real decision-makers navigate, and every mathematical structure earns its place by explaining phenomena that the scalar framework cannot.

We begin with the dimensions.

---

## 3.1 The Nine Dimensions of Economic Decision-Making

Economic decisions are evaluated on nine dimensions. These are the same nine dimensions of the moral manifold identified in *Geometric Ethics* (Bond, 2026), re-interpreted for economic contexts. They were empirically validated across 20,030 texts and 11 languages, and independently replicated across 6 additional languages (Thiele, 2026).

> **Definition 1 (Dimensions of the Economic Decision Manifold).** The economic decision manifold has nine coordinate dimensions $d_1, \ldots, d_9$:

1. $d_1$: **Consequences** -- monetary cost, material outcome, risk-adjusted expected value. This is the *only* dimension visible to Homo economicus.

2. $d_2$: **Rights/Entitlements** -- property rights, contractual obligations, Hohfeldian positions. "This is mine" vs. "this is available."

3. $d_3$: **Fairness** -- distributional justice, procedural justice, proportionality, reciprocity. "Is this a fair deal?"

4. $d_4$: **Autonomy** -- freedom of choice, coercion aversion, voluntariness. "Am I choosing freely or being forced?"

5. $d_5$: **Privacy/Trust** -- information asymmetry, disclosure norms, fiduciary duty. "Can I trust this counterparty?"

6. $d_6$: **Social impact** -- externalities, community effects, reputational consequence. "What will people think?"

7. $d_7$: **Virtue/Identity** -- self-image, moral identity, character consistency. "Is this the kind of person I am?"

8. $d_8$: **Legitimacy** -- institutional trust, rule compliance, procedural regularity. "Are the rules being followed?"

9. $d_9$: **Epistemic status** -- information quality, confidence, ambiguity. "Do I understand what I'm getting?"

These dimensions are not arbitrary. They derive from a systematic decomposition of moral space developed in *Geometric Ethics*, where three normative modes (consequentialist, deontological, virtue-based) are crossed with three evaluative scopes (individual, relational, institutional), yielding a $3 \times 3$ structure that maps onto nine independent dimensions. The economic adaptation relabels the dimensions for economic contexts while preserving the mathematical structure.

**[Empirical.]** The claim that these nine dimensions are empirically operative is supported by factor analysis of behavioral economic data, cross-cultural replication, and the eris-econ validation results (Appendix C), which show that the framework correctly predicts 16/16 behavioral phenomena with 2.70% mean absolute error.

---

## 3.2 Why Nine Dimensions, Not One

> **Remark 1 (Why Nine Dimensions, Not One).** The claim is not that these dimensions are *optional* extras that "nice" people care about. The claim is that these dimensions are *computationally active in every economic decision*, including the decisions of self-interested agents.

This remark deserves expansion, because it is the most common source of misunderstanding about the framework.

Consider a purely selfish agent -- someone with no altruistic impulses, no concern for others' welfare, no moral commitments beyond self-interest. Even this agent cares about:

- **Rights** ($d_2$): "Can I be punished for this? Will my property be protected? Is this contract enforceable?"
- **Social impact** ($d_6$): "Will this damage my reputation? Will people stop doing business with me?"
- **Legitimacy** ($d_8$): "Will the contract be enforced? Can I trust the legal system to back me up?"
- **Epistemic status** ($d_9$): "Do I have enough information to make a good bet? What am I not seeing?"

These are not moral preferences layered on top of economic calculation. They are the *constraint structure* of the decision space itself. A selfish agent who ignores $d_2$ (rights) will be punished. A selfish agent who ignores $d_6$ (reputation) will lose trading partners. A selfish agent who ignores $d_8$ (legitimacy) will find contracts unenforced. A selfish agent who ignores $d_9$ (epistemic status) will be systematically exploited.

The nine dimensions are not nine moral values. They are nine *information channels* that any agent -- altruistic, selfish, or anything in between -- must process to make decisions that achieve their goals. Homo economicus fails not because it is too selfish but because it processes information along only one channel. It is not morally deficient; it is *informationally impoverished*.

### The Transferable/Evaluative Distinction

A structural distinction runs through the nine dimensions that will matter throughout the book.

> **Definition 2 (Transferable and Evaluative Dimensions).** Dimensions $d_1$, $d_2$, and $d_4$ are *transferable*: a gain to one party on a transferable dimension requires a corresponding cost to another party. Monetary value ($d_1$), rights and obligations ($d_2$), and autonomy/coercion ($d_4$) are conserved in closed bilateral exchanges. Dimensions $d_3$ and $d_5$ through $d_9$ are *evaluative*: they are not necessarily conserved. Fairness ($d_3$) is evaluative because both parties can simultaneously perceive an exchange as fairer -- a well-negotiated compromise can increase each party's sense of fairness without diminishing the other's. Similarly, both parties may simultaneously gain trust ($d_5$), social standing ($d_6$), virtuous self-image ($d_7$), institutional confidence ($d_8$), or epistemic clarity ($d_9$).

This distinction formalizes a deep intuition about economic exchange. On the transferable dimensions, trade is zero-sum: your gain is my loss. On the evaluative dimensions, trade can create mutual value: a transaction that builds trust benefits both parties; a deal that enhances both parties' sense of fairness is positive-sum on $d_3$; a deal that enhances both parties' reputations is positive-sum on $d_6$. The coexistence of zero-sum transferable dimensions and positive-sum evaluative dimensions is the structural basis of the intuition that trade "creates value" -- the value it creates is on the evaluative dimensions, while the value it transfers on the transferable dimensions sums to zero (Chapter 9 formalizes this as the Attribute Conservation Law).

---

## 3.3 The Decision Complex: Primary Construction

With the dimensions identified, we can construct the mathematical object on which economic decisions live.

> **Definition 3 (Economic Decision Complex).** The *economic decision complex* $\mathcal{E}$ is a weighted simplicial complex constructed as follows:
>
> - **Vertices (0-simplices):** Each vertex $v_i$ represents an *economic state* -- a configuration of goods, services, obligations, and relationships available to the agent. The vertex carries an *attribute vector* $\mathbf{a}(v_i) \in \mathbb{R}^9$, whose components are scores along the nine dimensions.
>
> - **Edges (1-simplices):** An edge $(v_i, v_j)$ represents an available *action* -- a transaction, decision, or behavioral choice that moves the agent from state $v_i$ to state $v_j$. The edge carries a weight $w(v_i, v_j) \geq 0$ representing the *total cost* of the action on the full manifold.
>
> - **Higher simplices:** A $k$-simplex $[v_0, \ldots, v_k]$ represents a *bundle* -- a set of mutually available actions that can be taken jointly (e.g., a package deal, a multi-attribute trade).

The decision complex is not a smooth manifold in the technical sense -- it is a simplicial complex, a combinatorial object. But for decision problems with many finely graded alternatives, the complex approximates a smooth manifold, and the continuous-manifold language of geodesics, curvature, and metrics provides powerful analytical tools. Throughout this book, we move freely between the discrete (simplicial complex) and continuous (manifold) descriptions, using whichever is more natural for the problem at hand.

### Vertices as Economic States

A vertex $v_i$ in $\mathcal{E}$ represents a complete description of the agent's economic situation along all nine dimensions. For Maria considering whether to hire a new barista, two key vertices might be:

**$v_0$ (current state, no hire):**
$$\mathbf{a}(v_0) = (a_1^0, a_2^0, a_3^0, a_4^0, a_5^0, a_6^0, a_7^0, a_8^0, a_9^0)$$

where $a_1^0$ reflects her current revenue and costs, $a_2^0$ reflects her current contractual obligations, and so on through all nine dimensions.

**$v_1$ (after hiring Jamie from the neighborhood):**
$$\mathbf{a}(v_1) = (a_1^0 - c_{\text{salary}}, a_2^0 + \delta_2, a_3^0 + \delta_3, a_4^0 - \delta_4, a_5^0 + \delta_5, a_6^0 + \delta_6, a_7^0 + \delta_7, a_8^0 + \delta_8, a_9^0 - \delta_9)$$

where $c_{\text{salary}}$ is the salary cost (reducing $d_1$), $\delta_2$ is the increased contractual obligation, $\delta_3$ is the fairness improvement from paying a living wage, $\delta_4$ is the slight reduction in Maria's autonomy (she now has an employee to manage), $\delta_5$ is the trust built by hiring locally, $\delta_6$ is the community impact, $\delta_7$ is the identity reinforcement, $\delta_8$ is the regulatory compliance (proper employment contract), and $\delta_9$ is the increased uncertainty (will the new hire work out?).

The point is that *every* economic state has a nine-dimensional description, and *every* economic action produces a nine-dimensional displacement. Classical economics tracks only the first component. The full framework tracks all nine.

### Edges as Actions

An edge $(v_i, v_j)$ connects two states and represents the action that transforms one into the other. The edge carries a weight -- the total cost of the action on the full manifold. This weight is not a scalar arbitrarily assigned; it is computed from the attribute-vector change and the manifold's metric structure.

---

## 3.4 Multi-Dimensional Edge Weights

The weight of an edge is the central computational object of the framework. It encodes the total cost of an economic action, measured across all nine dimensions.

> **Definition 4 (Multi-Dimensional Edge Weights).** The weight of an edge $(v_i, v_j)$ in $\mathcal{E}$ is:
>
> $$w(v_i, v_j) = \underbrace{\Delta \mathbf{a}^T \, \Sigma^{-1} \, \Delta \mathbf{a}}_{\text{Mahalanobis distance}} + \underbrace{\sum_k \beta_k \cdot \mathbf{1}[\text{moral boundary } k \text{ crossed}]}_{\text{heuristic boundary penalties}}$$
>
> where $\Delta \mathbf{a} = \mathbf{a}(v_j) - \mathbf{a}(v_i)$ is the attribute-vector difference, $\Sigma$ is the $9 \times 9$ *dimensional covariance matrix* estimated from observed economic behavior, and $\beta_k$ is the penalty for crossing the $k$-th moral-economic boundary.

This formula has two components, and both matter.

### The Mahalanobis Distance

The first component, $\Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a}$, is the Mahalanobis distance between the current state and the post-action state. Unlike the Euclidean distance (which treats all dimensions as independent and equally weighted), the Mahalanobis distance accounts for *correlations between dimensions* and *differences in dimensional variance*.

**[Modeling Axiom.]** The covariance matrix $\Sigma$ is the core empirical object of the framework. Its diagonal entries $\sigma_k^2$ encode the variance of each dimension -- how much that dimension typically fluctuates in normal economic activity. Its off-diagonal entries $\sigma_{jk}$ encode the covariation between dimensions -- how changes in one dimension typically accompany changes in another.

Economic dimensions are *not independent*:

- Fairness ($d_3$) interacts with consequences ($d_1$): a price that seems fair at one income level seems exploitative at another.
- Autonomy ($d_4$) modulates the weight of social impact ($d_6$): an agent who feels free to choose is less sensitive to social pressure than one who feels coerced.
- Trust ($d_5$) gates access to higher-consequence transactions ($d_1$): you cannot engage in high-value trades without counterparty trust.
- Identity ($d_7$) amplifies fairness sensitivity ($d_3$): an agent who sees herself as fair-minded reacts more strongly to perceived unfairness.

An $L_1$ or $L_2$ norm (which treats dimensions as orthogonal) would systematically mispredict behavior by ignoring these interactions. The Mahalanobis distance, by encoding the full covariance structure, captures the dimensional interactions that drive real decision-making.

### The Boundary Penalties

The second component, $\sum_k \beta_k \cdot \mathbf{1}[\text{moral boundary } k \text{ crossed}]$, encodes the cost of crossing moral-economic boundaries. These are the discontinuous transitions that the Mahalanobis distance (which is smooth) cannot capture.

Some boundary penalties are infinite ($\beta_k = \infty$): the transition from "buy" to "steal" crosses a rights boundary that most agents treat as absolute. Some are large but finite: the transition from "keep promise" to "break promise" has high cost but can be outweighed by extreme circumstances. Some vary with context, culture, and individual temperament.

The boundary penalties are not free parameters. They are empirically measurable via the "taboo trade-off" paradigm (Tetlock et al., 2000): offer increasing monetary compensation for crossing the boundary and observe whether any finite offer is accepted. If no finite offer suffices, $\beta_k = \infty$. For finite boundaries, $\beta_k$ is estimated from the compensation amount at which agents become willing to cross the boundary -- the *reservation price for norm violation*.

---

## 3.5 Moral-Economic Phase Transitions

Not all economic transitions are smooth. Some are discontinuous, and the discontinuities matter enormously for economic behavior.

> **Definition 5 (Moral-Economic Boundary).** A *moral-economic boundary* is a threshold in the decision complex $\mathcal{E}$ where the local decision regime changes discontinuously.

Four types of boundaries appear repeatedly in economic life:

### The Theft Boundary

The transition from "buy" to "steal" crosses a deontological boundary ($d_2$: rights violation) with $\beta_{\text{theft}} = \infty$ for most agents. This is why Homo economicus cannot explain why people do not steal: on the scalar projection, theft has positive expected utility (free goods minus probability-weighted detection cost); on the full manifold, the edge weight is infinite.

**[Empirical.]** This example is not hypothetical. The expected-utility calculation for shoplifting yields a positive expected value for most small items (the probability of detection times the cost of punishment is far less than the value of the goods). Homo economicus should shoplift constantly. The observation that most people do not is not an anomaly to be explained by "risk aversion" or "warm-glow altruism" -- it is evidence that the decision is being made on a manifold where the theft boundary has infinite weight.

### The Promise Boundary

The transition from "keep promise" to "break promise" crosses a social-norm boundary ($d_6$, $d_7$) with high but finite $\beta$. Promises can be broken -- people do break them -- but the cost is substantial and includes reputational damage ($d_6$), identity damage ($d_7$), and often fairness violations ($d_3$). The finiteness of this boundary penalty explains why promise-breaking is more common than theft: the cost is large but not infinite, so sufficiently large gains can outweigh it.

### The Sacred-Value Boundary

Certain goods are *incommensurable* -- no monetary offer can compensate for their loss. "How much to sell your child?" has $\beta = \infty$ along the cultural-taboo dimension. Tetlock's "forbidden tradeoffs" are precisely the infinite-weight boundaries on the decision manifold. These boundaries are not irrational -- they reflect a structural feature of the manifold: certain transitions are not on any finite-weight path.

### The Market-Norm / Social-Norm Boundary

Introducing monetary payment into a social relationship ("paying a friend for dinner") crosses a regime boundary that changes the entire metric structure. The Mahalanobis weights shift because the covariance matrix $\Sigma$ is different in market-norm space vs. social-norm space. This is Ariely's (2008) finding that market norms and social norms are "two different worlds" -- in geometric terms, they are different *strata* of the decision manifold, with different metrics.

> **RUNNING EXAMPLE -- MARIA'S BOUNDARIES**
>
> *Maria faces several boundaries in her hiring decision. The labor-law boundary ($d_8$): she must comply with minimum wage, workers' compensation, and non-discrimination requirements. Crossing this boundary (hiring off the books, paying below minimum wage) would reduce $d_1$ cost but carries $\beta_{\text{regulatory}} = \text{large}$ -- fines, legal liability, and the identity cost of being "the kind of employer who cuts corners." The social-norm boundary ($d_6$, $d_7$): in her neighborhood, hiring locally is the norm. Hiring someone from outside the community when a qualified local candidate is available would cross a social boundary with $\beta_{\text{social}} = \text{moderate}$. Maria navigates these boundaries intuitively -- her System 1 heuristic $h(n)$ encodes the boundary penalties, generating the "gut feeling" that certain options are "just not right" without requiring explicit calculation of edge weights.*

---

## 3.6 Proposition 5: Why "Irrational" Refusal Is Rational

The interaction between Mahalanobis distance and boundary penalties generates one of the framework's most important results: a formal explanation of why agents refuse economically advantageous transactions.

> **Proposition 5 (Infinite-Weight Boundaries Explain "Irrational" Refusal).** *An agent who refuses a transaction with positive expected monetary value ($\Delta d_1 > 0$) is acting rationally on the full manifold $\mathcal{E}$ whenever the transaction crosses a boundary with $\beta_k > \Delta d_1 / \sigma_1^2$. The refusal appears "irrational" only when the decision is projected onto the $d_1$ axis alone.*

**Proof.** The total edge weight is $w = \Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a} + \beta_k$. Even if the Mahalanobis component contributes a net decrease in distance along $d_1$ (the action improves monetary position), the boundary penalty $\beta_k$ makes the total weight positive. The action is therefore not on the minimum-cost path -- the agent rationally avoids it. Projection onto $d_1$ discards $\beta_k$, making the refusal appear unmotivated. $\square$

This proposition explains a vast range of economic phenomena that classical economics cannot account for:

- **Ultimatum game rejections:** Responders reject unfair offers ($\Delta d_1 > 0$) because the fairness boundary penalty $\beta_{\text{fairness}}$ exceeds the monetary gain.
- **Altruistic punishment:** Agents pay to punish norm violators ($\Delta d_1 < 0$) because tolerating the violation has higher total manifold cost than the monetary cost of punishment.
- **Refusal to sell sacred objects:** No finite offer can compensate for crossing a sacred-value boundary ($\beta = \infty$).
- **Rejection of exploitative contracts:** Workers refuse below-subsistence wages even when the alternative is unemployment, because the dignity boundary ($d_3$, $d_7$) has high $\beta$.

In each case, the behavior is "irrational" only on the scalar projection. On the full manifold, it is the minimum-cost path.

### The Grocery Store Example

To make this concrete, consider the simplest possible application.

An agent stands in a grocery store. Two paths are available:

**Path A (buy):** Pay \$50. Attribute-vector change: $\Delta d_1 = -50$, all other dimensions approximately 0. Edge weight: $w_A = 50^2 / \sigma_1^2$.

**Path B (steal):** Pay \$0. Attribute-vector change: $\Delta d_1 = 0$, but $\Delta d_2 = -\infty$ (rights violation), $\Delta d_6 = -\text{large}$ (social sanction risk), $\Delta d_7 = -\text{large}$ (identity violation). Edge weight: $w_B = \infty$.

Under scalar utility ($\phi = d_1$): $\phi(B) > \phi(A)$, so Homo economicus steals.

On the full manifold: $w_B = \infty > w_A$, so the rational agent buys.

The agent is not "irrational" for buying. The economist is computing on the wrong manifold. This is, in miniature, the entire argument of the book. Classical economics operates on the $d_1$ projection and is puzzled by behavior that makes perfect sense on the full decision complex. The solution is not to add epicycles to the utility function -- it is to expand the dimensionality of the evaluation space.

---

## 3.7 Formal Properties of the Decision Complex

### Dimensionality

The decision complex $\mathcal{E}$ has nine dimensions. This is a structural commitment of the framework, not a free parameter. It is derived from the $3 \times 3$ decomposition of moral-economic space (three normative modes crossed with three evaluative scopes) and validated by factor analysis of behavioral data. The commitment is falsifiable: if a replicable economic behavior is discovered that cannot be decomposed into any subset of the nine dimensions, the framework is wrong.

**[Modeling Axiom.]** The specific number nine is a modeling choice inherited from Geometric Ethics. It is possible that finer-grained analysis would identify sub-dimensions within each of the nine (e.g., distributional fairness and procedural fairness as sub-dimensions of $d_3$), or that some dimensions could be merged. The framework's predictions are robust to modest changes in dimensionality -- the key claim is that the dimension is significantly greater than one, not that it is exactly nine.

### The Covariance Matrix

The covariance matrix $\Sigma$ is a $9 \times 9$ symmetric positive semi-definite matrix with at most $9(9+1)/2 = 45$ free parameters. Empirical regularities further constrain it: cross-lingual validation shows that the rank of $\Sigma$ (the number of active dimensions) is stable across cultures at approximately 9, even though individual entries vary. This is a structural prediction: any culture that reduces $\operatorname{rank}(\Sigma) < 9$ would provide evidence against the framework.

$\Sigma$ is estimated *before* prediction, not after. The estimation procedure parallels standard psychometric practice: administer a battery of moral-economic scenarios, measure attribute-vector activations via validated instruments (the MoralVector probes), and compute $\Sigma$ from the calibration sample. Once $\Sigma$ is fixed, the framework generates *a priori* predictions for novel scenarios.

### Metric Structure

The Mahalanobis distance $d(\mathbf{a}, \mathbf{b}) = \sqrt{(\mathbf{b} - \mathbf{a})^T \Sigma^{-1} (\mathbf{b} - \mathbf{a})}$ defines a metric on the attribute-vector space $\mathbb{R}^9$. This metric has several important properties:

1. **Coordinate invariance:** The Mahalanobis distance is invariant under linear transformations of the coordinate system. If we rotate, scale, or re-parameterize the nine dimensions, the distance between any two states remains unchanged. This is the economic analogue of the requirement in physics that physical laws be invariant under coordinate transformations.

2. **Correlation sensitivity:** The distance accounts for correlations between dimensions. Two states that differ by the same amount on $d_1$ and $d_3$ are closer if $d_1$ and $d_3$ are positively correlated (because correlated changes are "expected" and therefore less costly) and farther apart if they are negatively correlated.

3. **Scale normalization:** The division by $\sigma_k^2$ normalizes each dimension by its typical variance. A \$100 change in monetary value ($d_1$) is a small displacement in a high-income context (where $\sigma_1$ is large) but a large displacement in a low-income context (where $\sigma_1$ is small). The metric automatically adjusts for scale.

---

## 3.8 Worked Example: Maria's Lease Negotiation on the Decision Complex

Let us map Maria's lease negotiation onto the decision complex in detail.

### Setting Up the Vertices

Maria's landlord has offered three possible terms for lease renewal:

**$v_0$ (current state):** Lease at \$5,000/month, month-to-month.
$$\mathbf{a}(v_0) = (a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9)$$

Take this as the reference point -- all changes are measured relative to $v_0$.

**$v_1$ (accept 40% increase):** Lease at \$7,000/month, one-year term.
$$\Delta \mathbf{a}_1 = (-24000, +0.3, -0.5, -0.4, -0.6, -0.2, -0.3, +0.2, -0.5)$$

Breaking this down:
- $\Delta d_1 = -24000$: \$2,000/month additional cost over 12 months
- $\Delta d_2 = +0.3$: one-year lease provides slightly more contractual security than month-to-month
- $\Delta d_3 = -0.5$: the increase feels unfair -- Maria built the neighborhood value the REIT is capturing
- $\Delta d_4 = -0.4$: reduced autonomy -- must cut wages or quality to afford the increase
- $\Delta d_5 = -0.6$: trust with landlord damaged -- "they'll just raise it again next year"
- $\Delta d_6 = -0.2$: some community impact if Maria must reduce services or raise prices
- $\Delta d_7 = -0.3$: identity strain -- being forced to make choices she opposes
- $\Delta d_8 = +0.2$: the REIT is within its legal rights (legitimate process)
- $\Delta d_9 = -0.5$: uncertainty about future increases

**$v_2$ (negotiate to \$6,000 with five-year term):**
$$\Delta \mathbf{a}_2 = (-12000, +0.7, +0.1, -0.1, +0.2, +0.1, +0.2, +0.3, +0.4)$$

- $\Delta d_1 = -12000$: \$1,000/month additional cost over 12 months (but five-year certainty)
- $\Delta d_2 = +0.7$: five-year lease provides substantial contractual security
- $\Delta d_3 = +0.1$: the negotiated outcome feels approximately fair -- a compromise
- $\Delta d_4 = -0.1$: slight reduction in autonomy (committed to three years)
- $\Delta d_5 = +0.2$: trust partially restored through successful negotiation
- $\Delta d_6 = +0.1$: community sees Maria as a fighter who got a decent deal
- $\Delta d_7 = +0.2$: identity reinforced -- "I stood up for myself and my employees"
- $\Delta d_8 = +0.3$: legitimate process, both parties negotiated in good faith
- $\Delta d_9 = +0.4$: five-year term reduces uncertainty substantially

**$v_3$ (close the shop):**
$$\Delta \mathbf{a}_3 = (+\text{savings}, -0.8, -0.3, -0.7, -0.4, -0.9, -0.8, 0, +0.3)$$

- $\Delta d_1 = +\text{savings}$: no more rent, but also no more revenue; net depends on alternatives
- $\Delta d_2 = -0.8$: all contractual obligations with suppliers, employees must be unwound
- $\Delta d_3 = -0.3$: feels unfair to employees and community
- $\Delta d_4 = -0.7$: loss of economic autonomy -- Maria no longer has a business
- $\Delta d_5 = -0.4$: relationships built over years are disrupted
- $\Delta d_6 = -0.9$: severe community impact -- four jobs lost, community gathering space lost
- $\Delta d_7 = -0.8$: major identity disruption -- "I am no longer a business owner"
- $\Delta d_8 = 0$: no legitimacy issue -- closing is within her rights
- $\Delta d_9 = +0.3$: at least the uncertainty is resolved

### Computing Edge Weights

Using a representative covariance matrix $\Sigma$ (with standard deviations $\sigma_k$ calibrated from behavioral economic data, and off-diagonal terms reflecting known dimension correlations), we can compute the Mahalanobis distance for each path:

**Path to $v_1$ (accept 40% increase):**
$$w_1 = \Delta \mathbf{a}_1^T \Sigma^{-1} \Delta \mathbf{a}_1$$

The large negative displacements on $d_3$ (fairness), $d_5$ (trust), and $d_9$ (epistemic) compound because $\Sigma$ encodes positive correlations between these dimensions -- when trust erodes, fairness perception worsens, and epistemic uncertainty increases. The Mahalanobis distance amplifies these correlated displacements.

**Path to $v_2$ (negotiate to \$6,000):**
$$w_2 = \Delta \mathbf{a}_2^T \Sigma^{-1} \Delta \mathbf{a}_2$$

The smaller monetary cost, combined with positive or near-zero displacements on most non-monetary dimensions, produces a much smaller total edge weight. The positive movements on $d_2$ (contractual security), $d_5$ (trust restoration), and $d_9$ (reduced uncertainty) actively *reduce* the Mahalanobis distance, because improvements on correlated dimensions offset the monetary cost.

**Path to $v_3$ (close shop):**
$$w_3 = \Delta \mathbf{a}_3^T \Sigma^{-1} \Delta \mathbf{a}_3$$

Despite the possible monetary savings, the large negative displacements on $d_4$ (autonomy), $d_6$ (community), and $d_7$ (identity) produce an enormous Mahalanobis distance. The closure crosses a moral-economic boundary -- the transition from "business owner" to "not business owner" -- that may carry its own boundary penalty $\beta_{\text{identity}}$.

### The Bond Geodesic

**[Conditional Theorem.]** The Bond geodesic -- the minimum-cost path on the full manifold -- is the path to $v_2$ (negotiate). This is not because Maria is "irrational" about the rent increase, or because she has "behavioral biases" that prevent her from accepting the market rate. It is because the negotiation path has the lowest total cost when all nine dimensions are accounted for.

The classical economist, optimizing on $d_1$ alone, might see the 40% increase as the "market rate" and advise Maria to either accept it or close. The geometric economist, optimizing on the full manifold, identifies the negotiation as the dominant strategy -- it minimizes total manifold distance by balancing a moderate monetary cost against positive movements on trust, security, identity, and epistemic dimensions.

---

## 3.9 The Relationship to Smooth Manifolds

The economic decision complex $\mathcal{E}$ is a simplicial complex -- a discrete combinatorial object. But many of the most powerful analytical tools in the framework come from the theory of smooth manifolds: metrics, curvature, geodesics, gauge invariance, conservation laws. How are the discrete and continuous descriptions related?

The relationship is analogous to the relationship between a lattice and a continuum in physics. A crystal is composed of discrete atoms arranged on a lattice, but its macroscopic behavior (elasticity, thermal conductivity, wave propagation) is well described by continuous field theories. The discrete structure is fundamental; the continuous description is a powerful approximation.

For economic decision complexes with many finely graded alternatives -- as when an agent chooses among a continuum of prices, quantities, or investment levels -- the complex approximates a smooth manifold $\mathcal{M} \subset \mathbb{R}^9$. In this regime:

- The Mahalanobis distance becomes a Riemannian metric $g_{\mu\nu} = (\Sigma^{-1})_{\mu\nu}$.
- Edge weights become line elements $ds^2 = g_{\mu\nu} \, da^\mu \, da^\nu$.
- The Bond geodesic becomes a geodesic on the Riemannian manifold.
- Boundary penalties become potential barriers in the metric.

The continuous description enables the use of differential geometry -- Christoffel symbols, curvature tensors, parallel transport -- to analyze how the decision manifold's structure shapes economic behavior. Chapter 4 exploits this to derive prospect-theoretic phenomena as geometric properties of the metric.

---

## 3.10 The Decision Complex and Existing Economic Formalism

A natural question arises: how does the decision complex relate to the mathematical objects that economists already use?

### General Equilibrium

Arrow-Debreu general equilibrium theory models the economy as a collection of agents, each with an endowment and a preference relation over commodity bundles. An equilibrium is a price vector and an allocation such that every agent maximizes utility subject to their budget constraint, and markets clear.

On the decision complex, an Arrow-Debreu economy is a special case where: (a) only $d_1$ (consequences) has non-zero metric weight, (b) boundary penalties are zero (no moral constraints), (c) the covariance matrix is $\Sigma = \sigma_1^2 \mathbf{e}_1 \mathbf{e}_1^T$ (only the monetary dimension has variance), and (d) all agents share the same metric (homogeneous preferences over dimensions). Under these restrictions, the Bond geodesic reduces to the utility-maximizing allocation, and the BGE reduces to the competitive equilibrium.

The restrictions are severe. Relaxing any one of them -- activating additional dimensions, introducing boundary penalties, allowing heterogeneous metrics -- produces behavior that the Arrow-Debreu framework cannot accommodate. The decision complex thus *nests* general equilibrium as a limiting case while generalizing it to the full nine-dimensional setting.

### The Edgeworth Box

The Edgeworth box -- the graphical tool for analyzing two-person, two-good exchange -- has a natural generalization on the decision complex. In the standard Edgeworth box, each point represents an allocation of two goods between two agents. The contract curve is the locus of Pareto-efficient allocations.

On the nine-dimensional decision complex, the "Edgeworth box" becomes a nine-dimensional attribute-vector space for each agent, and the "contract curve" becomes the set of allocations where no agent can be moved to a lower-cost state (on the full manifold) without increasing the cost for the other agent. The nine-dimensional contract curve is, in general, a surface of dimension greater than one -- there are multiple Pareto-efficient allocations that differ in which dimensions are traded off against which. The classical one-dimensional contract curve is the projection of this richer object onto the $d_1$ axis.

---

## 3.11 What the Decision Complex Is Not

Intellectual honesty requires stating the boundaries of the claim.

**The decision complex is not a utility function.** A utility function maps states to a scalar. The decision complex maps states to nine-dimensional attribute vectors. These are different mathematical objects. The utility function is a *projection* of the decision complex -- a specific contraction that collapses nine dimensions to one. The Scalar Irrecoverability Theorem (Chapter 6) proves that what the projection destroys is mathematically irrecoverable.

**The decision complex is not a "more complicated" utility function.** The objection "you've just replaced one utility function with nine" misunderstands the mathematical structure. A vector in $\mathbb{R}^9$ is not a more complicated version of a number in $\mathbb{R}$. It has *directions*, *projections*, *inner products*, and *transformations* that a scalar does not. The Mahalanobis distance between two attribute vectors depends on the *direction* of the displacement (not just its magnitude), the *correlations* between dimensions (not just the marginals), and the *boundary penalties* for crossing regime thresholds (which have no scalar analogue). These are qualitative differences, not quantitative ones.

**The decision complex is not a claim about what agents should do.** It is a claim about the *space* in which decisions are made. Different agents, with different values, in different institutional settings, will follow different paths through the same decision complex. The framework does not prescribe optimal behavior; it describes the structure of the space within which agents -- prescriptive, descriptive, normative -- navigate.

---

## Technical Appendix

**Formal Definition of the Simplicial Complex.** Let $V$ be a finite set of economic states. Let $\mathbf{a}: V \to \mathbb{R}^9$ assign an attribute vector to each state. Let $E \subseteq V \times V$ be the set of feasible transitions (not every pair of states is connected by an available action). Let $w: E \to \mathbb{R}_{\geq 0} \cup \{\infty\}$ assign edge weights via Definition 4. The economic decision complex is the pair $\mathcal{E} = (V, E, w, \mathbf{a})$.

**Metric Properties.** The Mahalanobis distance $d_M(\mathbf{a}, \mathbf{b}) = \sqrt{(\mathbf{b} - \mathbf{a})^T \Sigma^{-1} (\mathbf{b} - \mathbf{a})}$ is a proper metric on $\mathbb{R}^9$ when $\Sigma$ is positive definite:
1. $d_M(\mathbf{a}, \mathbf{b}) \geq 0$ with equality iff $\mathbf{a} = \mathbf{b}$ (positive definiteness)
2. $d_M(\mathbf{a}, \mathbf{b}) = d_M(\mathbf{b}, \mathbf{a})$ (symmetry)
3. $d_M(\mathbf{a}, \mathbf{c}) \leq d_M(\mathbf{a}, \mathbf{b}) + d_M(\mathbf{b}, \mathbf{c})$ (triangle inequality)

When $\Sigma$ is only positive semi-definite (some dimensions have zero variance), $d_M$ is a pseudometric and certain directions in the manifold have zero cost -- movements that do not change any active dimension.

**Boundary Penalty Structure.** **[Modeling Axiom.]** Boundary penalties $\beta_k$ partition into three regimes:
- $\beta_k = \infty$ (sacred boundaries): Tetlock's "forbidden tradeoffs." No finite compensation suffices.
- $\beta_k \in (0, \infty)$ (finite boundaries): measurable via reservation-price experiments.
- $\beta_k = 0$ (no boundary): the transition is smooth along all dimensions.

The indicator function $\mathbf{1}[\text{boundary } k \text{ crossed}]$ is defined by threshold conditions on the attribute-vector components: boundary $k$ is crossed when the attribute vector passes through a codimension-1 surface in $\mathbb{R}^9$ defined by the boundary condition. For example, the theft boundary is crossed when $d_2$ changes sign (from "I have the right" to "I don't have the right"). The sacred-value boundary is crossed when a dimension enters a forbidden region (the set of states where, e.g., a family member is treated as a commodity).

---

## Notes on Sources

The nine-dimensional structure is developed in Bond (2026), *Geometric Ethics*, Chapter 5, and validated empirically in Chapters 6-8 of that work. The Mahalanobis distance is due to P.C. Mahalanobis (1936), "On the Generalized Distance in Statistics," *Proceedings of the National Institute of Sciences of India*. The simplicial complex framework draws on computational topology as presented in Nanda (2020), *Computational Algebraic Topology*, Oxford lecture notes. Tetlock's forbidden tradeoffs are in Tetlock et al. (2000), "The Psychology of the Unthinkable," *Journal of Personality and Social Psychology*. Ariely's market-norm/social-norm distinction is in Ariely (2008), *Predictably Irrational*. The Hohfeldian framework for rights is from Hohfeld (1913), "Some Fundamental Legal Conceptions as Applied to Judicial Reasoning," *Yale Law Journal*.
