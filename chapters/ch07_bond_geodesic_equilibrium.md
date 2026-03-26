# Chapter 7: The Bond Geodesic Equilibrium

> *"If I am not for myself, who will be for me? If I am only for myself, what am I? And if not now, when?"*
> -- Hillel the Elder, *Pirkei Avot* 1:14

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria's lease is up for renewal. Her landlord, the REIT, wants to raise the rent from $5,000 to $7,000 per month. Maria wants to keep the rent at $5,000. They are playing a game.*
>
> *The Nash equilibrium of this game -- computed on the monetary dimension $d_1$ alone -- is stark. The landlord has the property rights and the legal authority to set any rent the market will bear. Maria either pays or leaves. If comparable spaces in the Mission rent for $7,000, the Nash equilibrium is: landlord charges $7,000; Maria pays (if profitable) or closes (if not). There is no room for negotiation, no account of relationship, no consideration of community. The equilibrium is determined entirely by the outside option on both sides.*
>
> *But Maria and her landlord are not playing the game on $d_1$ alone. Their interaction unfolds on the full nine-dimensional manifold:*
>
> *The landlord values long-term tenant stability ($d_5$: trust reduces vacancy risk), neighborhood vitality ($d_6$: empty storefronts depress surrounding property values), and regulatory goodwill ($d_8$: cities with rent-stabilization movements punish landlords seen as extractive). Maria values fairness ($d_3$: she helped create the neighborhood value the landlord is capturing), autonomy ($d_4$: the increase forces operational changes she opposes), and identity ($d_7$: she will not be squeezed into compromising her values).*
>
> *On the full manifold, a different equilibrium emerges: a moderate rent increase ($5,000 $\to$ $6,000) with a five-year lease guaranteeing no further increases. The landlord gets stable, above-current income and a reliable tenant who maintains the property's neighborhood value. Maria gets a manageable increase with long-term certainty that allows business planning. Both parties are better off than under the $d_1$-only Nash equilibrium -- not because they are being altruistic, but because they are optimizing on a richer manifold.*
>
> *This is the Bond Geodesic Equilibrium. It does not replace Nash. It reveals Nash as a special case -- the equilibrium you get when you collapse the manifold to a single dimension.*

---

## From Single-Agent Pathfinding to Multi-Agent Equilibrium

The previous chapters solved the single-agent problem. Chapter 3 defined the economic decision complex $\mathcal{E}$. Chapter 4 equipped it with a metric. Chapter 5 showed that economic decision-making is A* search with evaluation function $f(n) = g(n) + h(n)$, where $g$ is System 2 (accumulated cost) and $h$ is System 1 (heuristic estimate). Chapter 6 proved that scalar utility destroys irrecoverable information.

But most economic decisions are not made in isolation. When Maria decides how to respond to the rent increase, her optimal path depends on the landlord's strategy. When the landlord decides what rent to charge, the optimal strategy depends on Maria's response. When a firm sets prices, the optimal price depends on competitors' prices. When a country sets tariffs, the optimal tariff depends on trading partners' tariffs.

This is the domain of game theory. And the question this chapter answers is: *what is the equilibrium when multiple agents pathfind simultaneously on the economic decision manifold?*

The answer is the **Bond Geodesic Equilibrium** (BGE) -- a generalization of Nash equilibrium to the full decision manifold. This chapter defines the BGE, proves that it subsumes Nash equilibrium as a special case, establishes existence and uniqueness conditions, and demonstrates the framework's predictions on three canonical games that have resisted satisfactory explanation within the classical paradigm.

This is the central theoretical contribution of the book.

## The Bond Geodesic

Before defining the multi-agent equilibrium, we need the single-agent concept on which it is built.

> **Definition 18 (Bond Geodesic).** The *Bond geodesic* $\gamma^*$ from an initial state $v_0$ to a goal region $G$ on the economic decision complex $\mathcal{E}$ is the minimum-cost path:
>
> $$\gamma^* = \arg\min_\gamma \sum_{i=0}^{m-1} w(v_i, v_{i+1})$$
>
> subject to $\gamma(0) = v_0$, $\gamma(\text{end}) \in G$
>
> where $w$ is the full multi-dimensional edge weight:
>
> $$w(v_i, v_j) = \Delta\mathbf{a}^T \Sigma^{-1} \Delta\mathbf{a} + \sum_k \beta_k \cdot \mathbf{1}[\text{boundary } k \text{ crossed}]$$

The Bond geodesic is the path that a rational agent takes when *all nine dimensions of the decision manifold are active*. It is named to distinguish it from the classical "utility-maximizing path," which is a geodesic only on the scalar projection. On a Riemannian manifold, a geodesic is the locally distance-minimizing path. The Bond geodesic is the discrete analogue -- the minimum-cost path on the weighted simplicial complex $\mathcal{E}$.

The key insight is that the Bond geodesic can differ dramatically from the scalar-optimal path. The scalar-optimal path maximizes $d_1$ (monetary payoff) without regard to the other eight dimensions. The Bond geodesic minimizes *total* cost on the full manifold, which may mean accepting a lower $d_1$ payoff in exchange for lower costs on fairness, trust, identity, and community impact. This is not altruism. It is optimization on the correct space.

## Bond Geodesic Equilibrium: Definition

When multiple agents pathfind simultaneously on the economic decision complex, each agent's optimal path depends on the paths chosen by others. This interdependence is the defining feature of game theory.

> **Definition 19 (Bond Geodesic Equilibrium).** A strategy profile $(\gamma_1^*, \ldots, \gamma_n^*)$ is a *Bond geodesic equilibrium* if each $\gamma_i^*$ is a Bond geodesic on agent $i$'s decision complex $E_i$, given the strategies of the other agents:
>
> $$\gamma_i^* = \arg\min_{\gamma_i} \text{BF}_i(\gamma_i \mid \gamma_{-i}^*) \quad \forall\, i = 1, \ldots, n$$
>
> where $\text{BF}_i$ is the total path cost (behavioral friction) on agent $i$'s manifold, and $\gamma_{-i}^*$ denotes the other agents' strategies.

This definition says: a BGE is a profile of paths where no agent can reduce their *total behavioral friction* -- their cost on the full nine-dimensional manifold -- by unilaterally switching to a different path. It is the Nash condition, applied to the full manifold rather than to the scalar projection.

The term "behavioral friction" is deliberate. On the scalar projection, friction is monetary cost. On the full manifold, friction includes the cost of crossing moral boundaries, the cost of eroding trust, the cost of violating identity, the cost of damaging community. An agent at the BGE has found the path of least total resistance on their manifold, given what everyone else is doing.

## The Augmented Game

To establish the precise relationship between BGE and Nash equilibrium, we construct the *augmented game* -- a standard normal-form game whose Nash equilibria are exactly the BGE of the manifold game.

> **Definition 20 (Augmented Game).** Given a multi-agent BGE game $\Gamma = (N, \{E_i\}, \{G_i\})$, the *augmented game* $\Gamma^+$ is the normal-form game $(N, \{S_i\}, \{u_i\})$ where:
>
> - $S_i$ is the finite set of simple paths from $v_0^{(i)}$ to $G_i$ in $E_i$ (agent $i$'s pure strategy set).
>
> - $u_i(\gamma_i, \gamma_{-i}) = -\text{BF}_i(\gamma_i \mid \gamma_{-i})$ is agent $i$'s payoff: the negative of the total behavioral friction along their chosen path, given others' paths.

This construction is canonical: it says that agents in the manifold game are maximizing the negative of their total cost on the full manifold -- i.e., they are minimizing behavioral friction, which is exactly what A* search does. The construction eliminates the cost-vs-payoff ambiguity: *every* BGE statement is a Nash statement about the augmented game. Minimizing $\text{BF}_i$ is maximizing $u_i$. We never need to mix "cost minimization" and "payoff maximization" languages.

## The BGE--Nash Relationship

We now prove the central result: the precise relationship between BGE and Nash equilibrium.

> **Theorem 21 (BGE--Nash Relationship).**
>
> 1. **Equivalence:** *A strategy profile $(\gamma_1^*, \ldots, \gamma_n^*)$ is a BGE of $\Gamma$ if and only if it is a Nash equilibrium of the augmented game $\Gamma^+$.*
>
> 2. **Scalar nesting:** *Consider a single-action game in which each agent $i$ chooses one action $a_i \in A_i$ (so $|S_i| = |A_i|$ and each "path" is a single edge). If $\beta_k = 0$ for all $k$ and $\Sigma = \sigma_1^2 \mathbf{e}_1 \mathbf{e}_1^T$, then $u_i(a_i, a_{-i}) = -(\Delta d_1(a_i \mid a_{-i}))^2 / \sigma_1^2$. The augmented game $\Gamma^+$ is then a monotone transformation of the standard monetary game: the action that maximizes monetary payoff $\Delta d_1$ also maximizes $u_i$ (since $u_i$ is maximized when $|\Delta d_1|$ is minimized relative to the goal, and the goal-reaching constraint forces the feasible set to payoff-maximizing actions -- see proof). The BGE coincides with the Nash equilibrium of the monetary game.*
>
> 3. **Refinement:** *When boundary penalties are non-zero ($\beta_k > 0$ for some $k$), the BGE excludes Nash equilibria of the scalar game that require crossing moral boundaries, because the augmented-game payoff $u_i$ penalizes boundary crossings.*

This is the central result of the book. Let us prove each part carefully.

> *Proof.*
>
> **(1) Equivalence.** By definition, $\gamma_i^*$ minimizes $\text{BF}_i(\cdot \mid \gamma_{-i}^*)$ over $S_i$ if and only if $\gamma_i^*$ maximizes $u_i(\cdot, \gamma_{-i}^*) = -\text{BF}_i(\cdot \mid \gamma_{-i}^*)$ over $S_i$. The BGE condition (Definition 19) is therefore identical to the Nash condition on $\Gamma^+$. $\square$ (Part 1)
>
> **(2) Scalar nesting.** In the single-action setting with $\beta_k = 0$ for all $k$ and $\Sigma = \sigma_1^2 \mathbf{e}_1 \mathbf{e}_1^T$, agent $i$'s augmented-game payoff for action $a_i$ is:
>
> $$u_i(a_i, a_{-i}) = -(\Delta d_1(a_i \mid a_{-i}))^2 / \sigma_1^2$$
>
> Each action corresponds to a single edge from $v_0^{(i)}$ to some state $v_{a_i}$, and the goal region $G_i$ is the set of states with highest attainable $d_1$-value. Since only the action achieving the maximal $\Delta d_1$ reaches $G_i$, the strategy set $S_i$ contains exactly one path per action, and the path-existence constraint (reaching $G_i$) restricts the feasible set to payoff-maximizing actions. Among these, $u_i$ selects the one with minimal friction, which in the single-action case is the wealth-maximizing action. This is the standard Nash best-response condition with monetary payoffs.
>
> For multi-step paths, the quadratic structure of Mahalanobis weights introduces a preference for gradual transitions (the total squared cost of two steps of size $\Delta/2$ is $\Delta^2/(2\sigma_1^2)$, less than one step of size $\Delta$ at cost $\Delta^2/\sigma_1^2$). This path-smoothness preference enriches the BGE beyond standard Nash, but reduces to it in the single-action limit. $\square$ (Part 2)
>
> **(3) Refinement.** Let $(\gamma_1, \ldots, \gamma_n)$ be a Nash equilibrium of the scalar monetary game that requires agent $i$ to cross boundary $k$. In the augmented game, the payoff for this strategy is $u_i(\gamma_i, \gamma_{-i}) = -\text{BF}_i^{\text{scalar}}(\gamma_i) - \beta_k$, while a boundary-avoiding alternative $\gamma_i'$ yields $u_i(\gamma_i', \gamma_{-i}) = -\text{BF}_i^{\text{scalar}}(\gamma_i')$. Whenever $\beta_k > \text{BF}_i^{\text{scalar}}(\gamma_i') - \text{BF}_i^{\text{scalar}}(\gamma_i)$ (the boundary penalty exceeds the scalar cost disadvantage of avoiding the boundary), agent $i$ deviates, and the boundary-crossing profile is not a BGE. $\square$ (Part 3)

### What the Theorem Means

The theorem says three things, each with profound implications:

**First**, BGE and Nash equilibrium of the augmented game are the same object. This is not an approximation or an analogy. Every BGE is literally a Nash equilibrium -- of the right game. The "right game" is $\Gamma^+$, where payoffs are measured on the full manifold. This means that all of Nash's mathematical machinery (existence theorems, fixed-point arguments, refinement concepts) applies to BGE. We do not need new equilibrium theory. We need the old theory applied to the right payoff structure.

**Second**, classical Nash equilibrium is the scalar projection of BGE. When all non-monetary dimensions are zeroed out, BGE reduces to Nash. This is the same relationship as between general relativity and Newtonian mechanics: the simpler theory is the limiting case of the richer theory, obtained by collapsing the relevant structure (curved spacetime $\to$ flat space, full manifold $\to$ scalar projection). Nash equilibrium is not wrong; it is incomplete. It computes on a projected subspace and therefore misses the equilibria that exist on the full manifold.

**Third**, BGE *refines* Nash. In games where moral dimensions are active, BGE excludes Nash equilibria that require crossing moral boundaries. The "exploit your counterparty" equilibrium that Nash permits may not be a BGE, because the boundary penalty on the full manifold makes the exploitative strategy strictly dominated by a boundary-respecting alternative. This is why real economic interactions often converge to outcomes that are "softer" than Nash prediction: the agents are not being irrational. They are playing the game on the full manifold, where the exploitative equilibrium does not exist.

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *The Maria-landlord game on $d_1$ alone:*
>
> | | Maria pays $7K | Maria leaves |
> |---|---|---|
> | **Landlord charges $7K** | Landlord: +$2K/mo; Maria: $-$2K/mo margin | Landlord: $0 (vacancy); Maria: $-$relocation |
> | **Landlord charges $5K** | Landlord: $0 increase; Maria: status quo | Landlord: $0; Maria: $-$relocation |
>
> *Nash on $d_1$: If Maria's business is viable at $7K, the landlord charges $7K and Maria pays. Nash outcome: ($7K, pay).*
>
> *The same game on the full manifold:*
>
> *The landlord's augmented payoff for charging $7K includes: $+\$2K/month$ on $d_1$, but $-\beta_{\text{fairness}}$ on $d_3$ (capturing community-created value), $-\beta_{\text{trust}}$ on $d_5$ (damaging a reliable tenant relationship), $-$ cost on $d_6$ (risking neighborhood degradation if Maria closes), and $-$ cost on $d_8$ (risking regulatory backlash in a gentrification-sensitive city).*
>
> *Maria's augmented payoff for paying $7K includes the $d_1$ cost plus identity costs ($d_7$: accepting exploitation) and autonomy costs ($d_4$: forced operational changes).*
>
> *The BGE of the augmented game: landlord offers $6K with a 5-year guarantee; Maria accepts. The total behavioral friction for both players is lower than under the $d_1$-only Nash, because the boundary penalties on $d_3$, $d_5$, and $d_7$ are avoided.*

---

## Mixed BGE and Existence

### Mixed Strategies on the Manifold

Not all games have pure-strategy equilibria. The classic example is matching pennies: no deterministic strategy survives, so agents must randomize. The same applies to the manifold game.

> **Definition 22 (Mixed Bond Geodesic Equilibrium).** A *mixed Bond geodesic equilibrium* is a profile of probability distributions $(\sigma_1^*, \ldots, \sigma_n^*)$ over paths, where each $\sigma_i^*$ is a distribution over the finite set $S_i$ of simple paths from $v_0^{(i)}$ to $G_i$ in $E_i$, such that each $\sigma_i^*$ minimizes agent $i$'s expected behavioral friction:
>
> $$\sigma_i^* \in \arg\min_{\sigma_i \in \Delta(S_i)} \mathbb{E}_{\sigma_i, \sigma_{-i}^*}[\text{BF}_i(\gamma_i \mid \gamma_{-i})] \quad \forall\, i = 1, \ldots, n$$

A BGE is *pure* if each $\sigma_i^*$ is degenerate (puts probability 1 on a single path). Definition 19 describes a pure BGE; the mixed BGE generalizes it to randomized path selection.

### Existence

> **Theorem 23 (Existence of Mixed Bond Geodesic Equilibrium).** *Let $\Gamma = (N, \{E_i\}_{i \in N}, \{G_i\}_{i \in N})$ be a finite game where $N$ is a finite set of agents, each $E_i$ is a finite economic decision complex with positive edge weights, and each $G_i$ is a non-empty goal region. If for each agent $i$ and each strategy profile $\gamma_{-i}$ of the other agents, there exists at least one path from $v_0^{(i)}$ to $G_i$ with finite total cost, then a mixed Bond geodesic equilibrium exists.*

> *Proof.* Each agent $i$'s pure strategy set $S_i$ is the finite set of simple paths from $v_0^{(i)}$ to $G_i$ in $E_i$, which is finite and non-empty by assumption. The mixed extension $\Delta(S_i)$ is a simplex, hence compact and convex. In the augmented game $\Gamma^+ = (N, \{S_i\}, \{u_i\})$ (Definition 20), each $u_i$ is multilinear (hence continuous) in the mixed-strategy profile. By Nash's existence theorem (1950), $\Gamma^+$ has a mixed-strategy Nash equilibrium, which is a mixed BGE by Theorem 21(1). $\square$

The proof is short because it leverages the equivalence between BGE and Nash equilibria of the augmented game. The augmented game is a finite normal-form game; Nash's theorem guarantees a mixed equilibrium; the equivalence theorem converts it to a mixed BGE. The mathematical heavy lifting was done by Nash (1950). Our contribution is the construction of the augmented game -- the *right* game to which Nash's theorem should be applied.

### Pure BGE Existence

> **Remark 24 (Pure BGE Existence).** A pure BGE need not exist in general, for the same reason that pure Nash equilibria need not exist in finite games: best-response cycles are possible. Pure BGE existence is guaranteed under additional structural conditions:
>
> 1. *Independent decision complexes:* If each agent's edge weights do not depend on other agents' strategies, each agent independently computes their optimal path, and the resulting profile is trivially a pure BGE. This covers single-agent decisions (Chapters 3-6) and many market settings.
>
> 2. *Potential game structure:* If there exists a function $\Phi: \prod_i S_i \to \mathbb{R}$ such that for all $i$, $\text{BF}_i(\gamma_i, \gamma_{-i}) - \text{BF}_i(\gamma_i', \gamma_{-i}) = \Phi(\gamma_i, \gamma_{-i}) - \Phi(\gamma_i', \gamma_{-i})$, then any profile minimizing $\Phi$ is a pure BGE. Many common-pool resource games and congestion games have this structure.
>
> 3. *Supermodular structure:* If the strategy spaces can be partially ordered such that each $\text{BF}_i$ has increasing differences in $(\gamma_i, \gamma_{-i})$, a pure BGE exists by Tarski's fixed-point theorem.

## Multiplicity and Uniqueness

How many BGE does a game have? This question matters for prediction: if the equilibrium is unique, the framework makes a sharp prediction; if multiple equilibria exist, the framework must specify which one is selected.

> **Theorem 25 (Multiplicity of the BGE).**
>
> 1. **Multiple BGE are generically possible.** *Even when each agent's best response to any fixed $\gamma_{-i}$ is unique, multiple pure BGE can exist. (Example: a coordination game where best-response to $A$ is uniquely $A$ and best-response to $B$ is uniquely $B$ yields two pure BGE.)*
>
> 2. **Uniqueness under weak coupling:** *See Lemma 26 below.*

### The Contraction Lemma

The key uniqueness result is the *contraction lemma*, which specifies when the best-response dynamics on the augmented game converge to a unique fixed point.

> **Lemma 26 (Contraction Condition for BGE Uniqueness).** *For each agent $i$, let $\alpha_i > 0$ measure the self-separation of agent $i$'s best-response mapping (how much $i$'s own behavioral friction changes with $i$'s own path choice) and let $\kappa_i \geq 0$ measure the cross-sensitivity (how much $i$'s behavioral friction changes with others' path choices). If*
>
> $$\alpha_i > \kappa_i \quad \text{for all } i \in N$$
>
> *then the best-response mapping on $\Gamma^+$ is a contraction with Lipschitz constant $L = \max_i(\kappa_i / \alpha_i) < 1$, and the BGE is unique.*

> *Proof.* The best-response mapping $T: S \to S$ maps each profile to the profile of individual best responses. For agent $i$, $\|T_i(s) - T_i(s')\| \leq (\kappa_i / \alpha_i) \|s_{-i} - s'_{-i}\|$ by the ratio of cross-sensitivity to self-separation. Taking the maximum over $i$:
>
> $$\|T(s) - T(s')\| \leq L \|s - s'\|$$
>
> with $L = \max_i(\kappa_i / \alpha_i) < 1$. By Banach's fixed-point theorem, $T$ has a unique fixed point. $\square$

### Interpretation of the Contraction Condition

> **Remark 27 (Interpretation).** BGE is unique when each agent's decision is dominated by their own manifold structure (high $\alpha_i$ -- the agent's costs are mostly determined by their own path) rather than by what others do (low $\kappa_i$ -- the agent's costs are insensitive to others' strategies). This is the "weak coupling" condition.

Intuitively: if Maria's business decisions are mostly about her own costs, her own values, and her own customers (high $\alpha$), and only weakly affected by the landlord's specific rent number (low $\kappa$), then the game has a unique BGE. Maria's optimal path is *almost* independent of the landlord's strategy, and the game converges quickly to the unique equilibrium where both parties are doing their individual best.

When coupling is strong ($\kappa_i \approx \alpha_i$), multiple BGE can coexist -- as in coordination games, where the equilibrium depends on which region of the manifold the agents coordinate on. The rent negotiation becomes a coordination problem: both Maria and the landlord would benefit from the $6K-with-guarantee outcome, but they might also end up at the $7K-with-adversarial-relationship outcome if neither party trusts the other enough to propose the cooperative path.

### Computation

> **Remark 28 (Computation).** When the contraction condition holds, the BGE can be computed by iterated best response: start with an arbitrary profile, compute each agent's best response (via A* search on their decision complex), update, and repeat. Convergence is geometric with rate $L$. Each iteration requires solving $n$ single-agent A* problems -- computationally tractable.
>
> When the contraction condition fails, the BGE computation requires Nash-equilibrium algorithms on the augmented game $\Gamma^+$. For small games, enumeration suffices. For larger games, the Lemke-Howson algorithm (for two-player games) or the support enumeration method provides exact solutions. For very large games, approximate methods (fictitious play, replicator dynamics) converge to approximate BGE.

## Welfare Properties

What can we say about the efficiency of BGE outcomes?

> **Theorem 29 (BGE Welfare).** *A BGE is Nash-optimal on the augmented game $\Gamma^+$: no agent can unilaterally reduce their behavioral friction by deviating.*
>
> *However, a BGE is not in general Pareto optimal. Consider the Prisoner's Dilemma on the manifold: if the fairness dimension $d_3$ is inactive, both agents defect (as in classical Nash); the mutual-cooperation profile has lower total BF but is not individually stable. The Pareto failure of Nash equilibrium persists in BGE for the same structural reason.*

> **Remark 30 (Welfare Theorems).** *In potential games -- where all agents' behavioral friction derives from a common potential function $\Phi$ -- the BGE does coincide with a Pareto optimum of the augmented game. This is a strong sufficient condition that holds in many economically important settings (congestion games, market entry games, common-pool resource games). The first welfare theorem ("competitive equilibrium is Pareto efficient") holds for BGE when the augmented game has potential structure -- i.e., when all agents' manifold costs derive from a common societal cost function.*

The welfare result is nuanced. BGE is not automatically efficient -- the Prisoner's Dilemma demonstrates that individual rationality on the manifold can still produce collectively suboptimal outcomes. But BGE is *more likely* to be efficient than Nash, because the additional dimensions create coupling between agents that can sustain cooperation. When $d_5$ (trust) is active, defection is costly not just in retaliation but in trust erosion -- a cost that is internalized by the agent's own manifold, not just imposed by the opponent's response. This shifts the equilibrium toward cooperation even in one-shot games.

## Three Canonical Games on the Manifold

The BGE framework resolves several longstanding puzzles in behavioral game theory. We examine three canonical games, showing how each "anomaly" is predicted -- not cataloged post hoc -- by the full-manifold equilibrium.

### Example 31: The Ultimatum Game

In the standard ultimatum game, a proposer is given $10 and makes an offer to split it with a responder. The responder can accept (both get their shares) or reject (both get nothing).

**Classical Nash prediction ($d_1$ only):** The proposer offers $0.01 (the smallest positive amount). The responder accepts, since $0.01 > $0. In subgame-perfect equilibrium, any positive offer is accepted.

**Experimental reality:** Offers below approximately 30% of the endowment are rejected roughly half the time. Modal offers are 40-50% of the endowment. The prediction fails spectacularly.

**BGE analysis:** The responder's decision complex includes $d_3$ (fairness). The attribute-vector change for accepting an unfair offer (say, $1 out of $10) is:

- $\Delta d_1 = +1$ (monetary gain)
- $\Delta d_3 = -\text{large}$ (accepting an unfair split violates fairness norms)
- $\Delta d_7 = -\text{moderate}$ (accepting exploitation conflicts with self-respect)

The edge weight for accepting is:

$$w_{\text{accept}} = \frac{1^2}{\sigma_1^2} + \frac{(\Delta d_3)^2}{\sigma_3^2} + \beta_{\text{fairness}} \cdot \mathbf{1}[\text{fairness boundary crossed}]$$

The edge weight for rejecting is:

$$w_{\text{reject}} = \frac{1^2}{\sigma_1^2}$$

(The monetary loss of $1 is the only cost, since rejection does not cross any moral boundary.)

When the fairness boundary penalty $\beta_{\text{fairness}}$ exceeds the monetary gain ($\$1^2/\sigma_1^2$), rejection is the Bond geodesic. The responder's $h(n)$ fires the fairness alarm (System 1: "this is insulting"), and System 2's calculation of the $1 gain cannot overcome the fairness penalty on the full manifold. The responder rejects -- rationally, on the correct manifold.

The proposer, anticipating this (via the BGE best-response dynamics), offers 40-50% to avoid triggering the responder's fairness boundary. The BGE of the ultimatum game is an approximately equal split -- exactly what the experiments show.

The framework goes further: it predicts that rejection rates should vary with the *salience* of $d_3$. Making fairness more salient (e.g., by framing the game explicitly as a fairness test) should increase rejections. Making it less salient (anonymous, one-shot, large stakes) should decrease them. Both predictions are confirmed by the experimental literature.

### Example 32: The Prisoner's Dilemma

Two agents simultaneously choose to cooperate (C) or defect (D). Payoffs:

|  | C | D |
|---|---|---|
| **C** | (3, 3) | (0, 5) |
| **D** | (5, 0) | (1, 1) |

**Classical Nash ($d_1$ only):** Both defect. (D, D) is the unique Nash equilibrium with payoff (1, 1).

**Experimental reality:** In one-shot Prisoner's Dilemma experiments, cooperation rates range from 20% to 60% depending on context, framing, and population. This is far above the 0% predicted by Nash.

**BGE analysis:** The active manifold dimensions beyond $d_1$ include:

- $d_5$ (trust): Cooperating signals trustworthiness. Even in a one-shot game, agents who value their trust dimension ($d_5$) pay a cost for defecting -- the identity cost of being someone who betrays trust.
- $d_7$ (identity): An agent who defects becomes "a defector" -- someone who exploits cooperative others. This identity shift has a real manifold cost, even if the specific counterparty never interacts with the agent again.
- $d_3$ (fairness): Mutual cooperation is the fair outcome; mutual defection is the "fair" punishment for a world of defectors; but (D, C) -- defecting against a cooperator -- violates fairness norms.

In the augmented game, the payoff for defecting against a cooperator is:

$$u_i(D, C) = -\text{BF}_i(D \mid C) = -\left[\frac{5^2}{\sigma_1^2} + \beta_{\text{trust}} + \beta_{\text{fairness}}\right]$$

The boundary penalties $\beta_{\text{trust}}$ and $\beta_{\text{fairness}}$ reduce the attractiveness of defection. When $\beta_{\text{trust}} + \beta_{\text{fairness}} > (5^2 - 3^2)/\sigma_1^2$, mutual cooperation becomes a BGE even in the one-shot game. The cooperation rate depends on the population distribution of $\beta_{\text{trust}}$ and $\beta_{\text{fairness}}$ -- which is why cooperation varies across contexts and cultures but is *always* above zero.

The framework predicts that cooperation in the Prisoner's Dilemma should increase with:
- Trust salience (e.g., playing with a partner you can see vs. anonymous play)
- Identity salience (e.g., framing the game as a "Community Game" vs. a "Wall Street Game")
- Fairness norms (e.g., in cultures with strong reciprocity norms vs. weak ones)

All three predictions are confirmed by the experimental literature (see, e.g., Liberman, Samuels, and Ross, 2004, on the "Wall Street Game" framing effect, where cooperation rates dropped from 70% to 33% when the identical game was relabeled).

### Example 33: Public Goods Provision

$N$ agents each receive an endowment of $10. Each can contribute any amount $c_i \in [0, 10]$ to a public pool. The pool is multiplied by a factor $m$ (with $1 < m < N$) and divided equally. The payoff to agent $i$ on $d_1$ is:

$$\pi_i = (10 - c_i) + \frac{m \sum_j c_j}{N}$$

**Classical Nash ($d_1$ only):** Since $m/N < 1$, each dollar contributed returns less than a dollar to the contributor. The dominant strategy is $c_i = 0$ for all $i$. Nash prediction: zero contribution.

**Experimental reality:** Average contributions are typically 40-60% of the endowment in the first round, declining toward but never reaching zero in repeated games. Agents contribute far more than Nash predicts.

**BGE analysis:** The active manifold dimensions include:

- $d_6$ (social impact): Contributing to the public good has positive social impact. Free-riding imposes negative externalities. The $d_6$ cost of free-riding creates a boundary penalty:

$$\beta_{\text{free-ride}} \propto \text{perceived social harm of withholding contribution}$$

- $d_7$ (identity): Contributing is consistent with the identity of a "cooperative community member." Free-riding conflicts with this identity.

- $d_3$ (fairness): If others contribute and the agent free-rides, the agent benefits unfairly. The fairness penalty increases with others' contributions.

In the augmented game, the payoff for contributing $c_i$ includes the $d_1$ payoff minus the behavioral friction from social impact, identity, and fairness dimensions. The BGE contribution level satisfies:

$$\frac{\partial}{\partial c_i}\left[-\text{BF}_i^{d_1}(c_i) - \text{BF}_i^{d_6}(c_i) - \text{BF}_i^{d_7}(c_i) - \text{BF}_i^{d_3}(c_i)\right] = 0$$

The $d_6$, $d_7$, and $d_3$ terms shift the optimal contribution upward from 0 (the $d_1$-only solution) to a positive level that depends on the weights of the active dimensions. The framework predicts:

- Contributions are positive but below the social optimum (because individual $d_1$ incentives still pull toward free-riding).
- Contributions decline in repeated play as the salience of $d_6$ and $d_7$ diminishes with repetition (habituation reduces the moral-heuristic sensitivity).
- Contributions are higher in smaller groups (where $d_6$ impact is more visible), in face-to-face interactions (where $d_5$ trust is activated), and in cultures with strong cooperative norms (where $\beta_{\text{free-ride}}$ is larger).

All three patterns are confirmed by decades of public goods experiments (see Ledyard, 1995, for a survey). The framework explains the patterns from the manifold structure rather than cataloging them as anomalies.

## Worked Example: Maria's Lease Negotiation as a Two-Player BGE

Let us work through the full BGE computation for the Maria-landlord lease negotiation.

### Players and Strategy Spaces

**Agent 1: The landlord (REIT)**
- Start state: Current lease at $5K/month, stable tenant, good neighborhood reputation
- Goal: Maximize return on property investment (on all relevant dimensions)
- Strategy set $S_1$: {Charge $5K, Charge $6K, Charge $6K + 5yr guarantee, Charge $7K, Charge $7K + buyout offer}

**Agent 2: Maria**
- Start state: Operating business with thin margins, strong community ties
- Goal: Maintain viable business with identity and community preserved
- Strategy set $S_2$: {Accept any offer, Accept $\leq$ $6K only, Accept $\leq$ $6K with guarantee only, Reject all increases, Negotiate + community campaign}

### Behavioral Friction Matrix

For each strategy pair, we compute the behavioral friction (total manifold cost) for each player. The BF includes the Mahalanobis distance on all active dimensions plus boundary penalties:

**Landlord's BF for each strategy pair:**

| Landlord \ Maria | Accept any | Accept $\leq$6K | Accept $\leq$6K+guar | Reject all | Negotiate+campaign |
|---|---|---|---|---|---|
| $5K (no change) | $d_1$: 0 | $d_1$: 0 | $d_1$: 0 | $d_1$: 0 | $d_1$: 0, $d_8$: $-$small |
| $6K | $d_1$: $-$1K gain | $d_1$: $-$1K | $d_1$: $-$1K | vacancy cost | $d_1$: $-$1K, $d_8$: $-$mod |
| $6K + 5yr | $d_1$: $-$1K, $d_5$: +stab | $d_1$: $-$1K, $d_5$: + | $d_1$: $-$1K, $d_5$: + | vacancy cost | $d_1$: $-$1K, $d_5$: + |
| $7K | $d_1$: $-$2K, $d_3$: $-\beta$ | $d_1$: vacancy | $d_1$: vacancy | vacancy cost | $d_1$: vac, $d_8$: $-$large |
| $7K + buyout | $d_1$: $-$2K + buyout | vacancy | vacancy | vacancy + buyout | $d_8$: $-$very large |

The critical insight: the landlord's BF for charging $7K includes a fairness boundary penalty $\beta_{\text{fairness}}$ on $d_3$ (capturing gentrification-created value) and a legitimacy cost on $d_8$ (reputational risk in a gentrification-sensitive city). These penalties do not appear in the $d_1$-only analysis.

**Maria's BF for each strategy pair (selected cells):**

- **Accept $7K**: $d_1$: $-$2K/month margin loss; $d_3$: $-\beta_{\text{fairness}}$ (accepting exploitation); $d_4$: $-$moderate (forced operational changes); $d_7$: $-$moderate (identity compromise)
- **Accept $6K with guarantee**: $d_1$: $-$1K/month (manageable); $d_3$: small (increase is within fair range); $d_5$: + (long-term stability builds trust); $d_7$: 0 (no identity compromise)
- **Negotiate + campaign**: $d_1$: uncertain; $d_4$: + (exercising autonomy); $d_6$: + (community engagement); $d_7$: + (acting on values); $d_8$: $-$small (adversarial)

### Computing the BGE

**Step 1: Landlord's best response to each of Maria's strategies.**

- If Maria accepts any offer: Landlord's BF is minimized at $6K + 5yr guarantee (good $d_1$ return, trust benefit from stability, avoids fairness boundary of $7K)
- If Maria accepts $\leq$6K: Landlord must offer $\leq$6K; best response is $6K
- If Maria accepts $\leq$6K with guarantee: Landlord's best response is $6K + 5yr
- If Maria rejects all increases: Landlord's best response is $5K (avoid vacancy cost)
- If Maria negotiates: Landlord's best response is $6K + 5yr (avoids campaign costs on $d_8$)

**Step 2: Maria's best response to each of the landlord's strategies.**

- If landlord charges $5K: Maria accepts (status quo is optimal)
- If landlord charges $6K: Maria accepts (manageable, no boundaries crossed)
- If landlord charges $6K + 5yr: Maria accepts with guarantee (best BF -- manageable cost + long-term stability)
- If landlord charges $7K: Maria negotiates + campaigns (high BF for accepting; lower BF for fighting)
- If landlord charges $7K + buyout: Maria negotiates (high BF for both accepting and buyout)

**Step 3: Find fixed points.**

The best-response correspondence has a fixed point at:
- **Landlord: $6K + 5-year guarantee**
- **Maria: Accept $\leq$6K with guarantee**

At this profile:
- Landlord's BF: $d_1$ gain of $12K/year; $d_5$ gain from stability; no fairness boundary crossed; moderate legitimacy
- Maria's BF: $d_1$ cost manageable; $d_3$ within fair range; $d_5$ gain from certainty; $d_7$ no identity compromise

This is the **Bond Geodesic Equilibrium** of the lease negotiation.

### Checking the contraction condition

The landlord's $\alpha$ (self-sensitivity): High. The landlord's costs are primarily determined by the rent level and vacancy risk -- properties of the landlord's own strategy.

The landlord's $\kappa$ (cross-sensitivity): Moderate. The landlord's costs depend on Maria's response (vacancy vs. tenancy), but the number of possible responses is limited.

Maria's $\alpha$: High. Maria's costs are determined by her own financial position, identity, and community relationships.

Maria's $\kappa$: Moderate. Maria's costs depend on the landlord's offer, but her values and community are largely independent of the landlord's specific number.

Since $\alpha_i > \kappa_i$ for both players (each agent's situation is dominated by their own manifold structure rather than by the other's strategy), the contraction condition (Lemma 26) is satisfied. The BGE is unique. Iterated best response converges geometrically to the $6K + guarantee equilibrium.

### Comparison with $d_1$-Only Nash

| | Nash ($d_1$ only) | BGE (full manifold) |
|---|---|---|
| Landlord's strategy | Charge $7K | Charge $6K + 5yr guarantee |
| Maria's strategy | Pay or leave | Accept $6K with guarantee |
| Landlord's $d_1$ payoff | +$2K/month | +$1K/month |
| Landlord's full-manifold BF | High ($d_3$, $d_5$, $d_8$ costs) | Low (no boundaries crossed) |
| Maria's $d_1$ payoff | $-$2K/month | $-$1K/month |
| Maria's full-manifold BF | Very high ($d_3$, $d_4$, $d_7$ costs) | Low (manageable, identity preserved) |
| Stability | Unstable (Maria may leave) | Stable (5-year lock-in) |
| Pareto comparison | Pareto-dominated on full manifold | Pareto improvement over Nash |

The BGE is strictly Pareto superior to the Nash outcome on the full manifold. Both players have lower total behavioral friction. The landlord sacrifices $1K/month in $d_1$ but gains stability ($d_5$), community preservation ($d_6$), and regulatory goodwill ($d_8$). Maria absorbs a $1K/month increase but gains certainty ($d_9$) and preserves identity ($d_7$), fairness ($d_3$), and community ($d_6$).

This is not a coincidence. It is a structural feature of the BGE: by optimizing on the full manifold, agents find paths that create value on evaluative dimensions ($d_3$, $d_5$, $d_6$, $d_7$) that the scalar projection cannot see. The evaluative dimensions are not conserved (Attribute Conservation theorem), so *both* parties can gain on them simultaneously. The BGE exploits this positive-sum structure; the Nash equilibrium, limited to $d_1$, misses it entirely.

## The BGE as a Research Program

### What BGE Explains That Nash Cannot

The BGE framework resolves a collection of "anomalies" that game theory has catalogued but not unified:

1. **Ultimatum game rejections** (Example 31): Predicted by $d_3$ activation. Rejection rate varies with fairness salience, as the framework requires.

2. **Trust game cooperation**: Predicted by $d_5$ activation. Cooperation is the Bond geodesic when the trust dimension's edge weights make defection more costly on the full manifold than on the $d_1$ projection.

3. **Public goods contribution** (Example 33): Predicted by $d_6$ and $d_7$ activation. Contribution levels and their decay pattern are predicted by the relative weights of social-impact and identity dimensions.

4. **Gift exchange in labor markets**: Workers who receive above-market wages reciprocate with above-minimum effort. Nash ($d_1$ only) predicts minimum effort regardless of wage. BGE predicts reciprocity through $d_3$ (fairness) and $d_5$ (trust).

5. **Third-party punishment**: Observers who are not directly affected by an unfair transaction will pay money to punish the offender. Nash on $d_1$ predicts no punishment (it is costly with no monetary return). BGE predicts punishment through $d_3$ (fairness norm enforcement) and $d_8$ (legitimacy maintenance).

In each case, the BGE prediction follows from the manifold structure: identify the active dimensions, compute the edge weights, solve for the equilibrium. The prediction is *derived*, not fitted. The framework says: tell me the active dimensions and their weights, and I will tell you the equilibrium.

### What BGE Does Not Claim

Intellectual honesty requires stating the framework's limitations:

1. **BGE does not solve the measurement problem.** The framework requires the covariance matrix $\Sigma$ and boundary penalties $\beta_k$ as inputs. These must be estimated from data -- behavioral experiments, cultural observations, neuroimaging. The framework tells you what to measure and how to use the measurements, but it does not provide the measurements themselves.

2. **BGE is not automatically efficient.** The Prisoner's Dilemma on the manifold can still produce suboptimal outcomes. BGE inherits the efficiency failures of Nash for the same structural reason: individual rationality does not guarantee collective optimality. The improvement is that more dimensions of cost are internalized, shifting more games toward cooperation -- but the fundamental tension between individual and collective rationality persists.

3. **BGE assumes agents pathfind on their perceived manifold.** If an agent misperceives the manifold -- if their heuristic is inadmissible, or their $\Sigma$ is miscalibrated -- the BGE of the perceived game may differ from the BGE of the true game. The framework distinguishes between these (the perceived-manifold BGE and the true-manifold BGE) but does not claim that agents always perceive correctly.

## The Relationship to General Relativity

The analogy between BGE and general relativity is structural, not metaphorical. It is worth making precise:

| General Relativity | Geometric Economics |
|---|---|
| Spacetime manifold $(M, g)$ | Decision manifold $(E, \Sigma, \beta)$ |
| Geodesic (free-fall path) | Bond geodesic (minimum-friction path) |
| Flat spacetime (Minkowski) | Flat manifold ($d_1$ only, $\Sigma = \sigma_1^2 \mathbf{e}_1\mathbf{e}_1^T$) |
| Newtonian gravity (weak-field limit) | Nash equilibrium ($d_1$ projection) |
| Einstein field equations | BGE condition (agents minimize BF) |
| Curvature | Moral boundary penalties, dimensional interactions |
| Special relativity as limiting case | Classical game theory as limiting case |

Nash equilibrium is to BGE as Newtonian mechanics is to general relativity: a special case valid in the "flat" limit (when the decision manifold collapses to a single dimension with no curvature from boundary penalties). The special case is not wrong; it is incomplete. It works when the field is weak (when moral dimensions are inactive) and fails when the field is strong (when moral dimensions dominate).

This is not an assertion of metaphysical unity between physics and economics. It is a structural observation: the same mathematical apparatus -- manifolds, metrics, geodesics, field equations -- describes both domains. Whether this convergence is deep or accidental is a question the framework does not answer. What it demonstrates is that the mathematics works: it unifies classical and behavioral economics, explains anomalies that have resisted scalar analysis, and generates falsifiable predictions.

---

## Technical Appendix

### Nash's Existence Theorem (Applied to $\Gamma^+$)

**[Established Mathematics.]** Nash (1950) proved that every finite game has at least one mixed-strategy Nash equilibrium, using Kakutani's fixed-point theorem. The augmented game $\Gamma^+$ is finite (finite agents, finite strategy sets), so Nash's theorem applies directly.

The proof: Each agent's mixed strategy is a probability distribution over $S_i$, forming a simplex $\Delta(S_i)$. The product $\prod_i \Delta(S_i)$ is compact and convex. The best-response correspondence $\text{BR}: \prod_i \Delta(S_i) \rightrightarrows \prod_i \Delta(S_i)$ is upper-hemicontinuous with non-empty convex values (by linearity of expected payoff in own strategy). By Kakutani's theorem, $\text{BR}$ has a fixed point -- a mixed-strategy Nash equilibrium of $\Gamma^+$, which is a mixed BGE by Theorem 21(1).

### Banach's Fixed-Point Theorem (Applied to Contraction Lemma)

**[Established Mathematics.]** Banach's contraction mapping theorem states that if $T: X \to X$ is a contraction ($\|T(x) - T(y)\| \leq L\|x - y\|$ with $L < 1$) on a complete metric space $(X, d)$, then $T$ has a unique fixed point. Applied to Lemma 26: the best-response mapping is a contraction when $\alpha_i > \kappa_i$ for all agents, so the BGE is unique.

The convergence rate is geometric: after $k$ iterations, $\|s^{(k)} - s^*\| \leq L^k \|s^{(0)} - s^*\|$. For a two-player game with $L = 0.5$, ten iterations reduce the error by a factor of $1024$. This makes iterated best response a practical algorithm for BGE computation.

### The Augmented Game Payoff Structure

**[Conditional Theorem.]** The payoff function $u_i(\gamma_i, \gamma_{-i}) = -\text{BF}_i(\gamma_i \mid \gamma_{-i})$ in the augmented game has the following structure:

$$u_i = -\sum_{e \in \gamma_i} \left[\Delta\mathbf{a}(e)^T \Sigma_i^{-1} \Delta\mathbf{a}(e) + \sum_k \beta_{k,i} \cdot \mathbf{1}[e \text{ crosses boundary } k]\right]$$

where $\Sigma_i$ is agent $i$'s covariance matrix (encoding $i$'s relative weighting of dimensions) and $\beta_{k,i}$ is $i$'s boundary penalty for constraint $k$. Note that different agents may have different $\Sigma_i$ and $\beta_{k,i}$ -- reflecting different cultures, values, and experiences. The augmented game payoff captures this heterogeneity naturally.

In the Maria-landlord example: $\Sigma_{\text{Maria}}$ weights $d_3$ (fairness) and $d_7$ (identity) heavily; $\Sigma_{\text{REIT}}$ weights $d_1$ (monetary return) and $d_8$ (regulatory compliance) heavily. The BGE reflects both agents' manifold structures simultaneously.

### Behavioral Friction Decomposition

For pedagogical clarity, the total behavioral friction can be decomposed:

$$\text{BF}_i = \underbrace{\text{BF}_i^{d_1}}_{\text{monetary cost}} + \underbrace{\text{BF}_i^{d_2 \ldots d_9}}_{\text{moral-social cost}} + \underbrace{\sum_k \beta_{k,i} \cdot \mathbf{1}[\text{boundary}]}_{\text{boundary penalties}}$$

Nash equilibrium sets the second and third terms to zero, optimizing $\text{BF}_i^{d_1}$ alone. BGE optimizes the sum. The difference between Nash and BGE outcomes is determined by the magnitude of the moral-social costs and boundary penalties relative to the monetary cost.

When these are small ($\text{BF}^{d_2 \ldots d_9} \approx 0$, $\beta_k \approx 0$): BGE $\approx$ Nash. This is the case in anonymous commodity markets.

When these are large: BGE $\neq$ Nash. This is the case in face-to-face bargaining, labor markets, medical markets, and any context where moral and social dimensions are active.

The empirical question is not "is BGE right or is Nash right?" It is: "in this specific market, how large are the non-monetary behavioral friction terms?" The answer determines which equilibrium concept is the better predictor.

### Connection to the Framework

The Bond Geodesic Equilibrium completes the multi-agent story:

- **Chapter 5** solved single-agent pathfinding: $f(n) = g(n) + h(n)$ on the decision manifold.
- **Chapter 6** proved that scalar utility is irrecoverably lossy: the full manifold cannot be compressed to $\mathbb{R}$ without information destruction.
- **This chapter** answers: what is the equilibrium when multiple agents pathfind simultaneously?
- **Chapter 8** will ask: what symmetries does the equilibrium respect? (gauge invariance)
- **Chapter 9** will derive: what conservation laws follow from those symmetries? (Noether's theorem for economics)

The BGE is the game-theoretic completion of the geometric economics program. Nash equilibrium -- the foundation of modern economics -- is the $d_1$-only contraction of BGE, exactly as scalar utility is the rank-0 contraction of the economic tensor (Chapter 6). The same mathematical operation (contraction/projection) that explains why scalar ethics loses information also explains why scalar economics loses information. The framework is unified, and the BGE is its central construction.

---

## Notes on Sources

Nash equilibrium is from Nash (1950), "Equilibrium Points in N-Person Games," *Proceedings of the National Academy of Sciences*. The existence theorem is from Nash (1951), "Non-Cooperative Games," *Annals of Mathematics*. Kakutani's fixed-point theorem is from Kakutani (1941), "A Generalization of Brouwer's Fixed Point Theorem," *Duke Mathematical Journal*.

The ultimatum game literature begins with Guth, Schmittberger, and Schwarze (1982), "An Experimental Analysis of Ultimatum Bargaining," *Journal of Economic Behavior and Organization*. The cross-cultural evidence is from Henrich et al. (2001, 2005). The framing effect in the Prisoner's Dilemma ("Wall Street Game" vs. "Community Game") is from Liberman, Samuels, and Ross (2004), "The Name of the Game," *Personality and Social Psychology Bulletin*.

The public goods literature is surveyed in Ledyard (1995), "Public Goods: A Survey of Experimental Research," in *The Handbook of Experimental Economics*. Third-party punishment is documented in Fehr and Fischbacher (2004), "Third-Party Punishment and Social Norms," *Evolution and Human Behavior*.

The Fehr-Schmidt model of inequality aversion (Fehr and Schmidt, 1999, "A Theory of Fairness, Competition, and Cooperation," *Quarterly Journal of Economics*) and the Bolton-Ockenfels ERC model (Bolton and Ockenfels, 2000, "ERC: A Theory of Equity, Reciprocity, and Competition," *American Economic Review*) are the most prominent attempts to modify the utility function to capture fairness preferences. The BGE framework subsumes these models: they correspond to specific augmented games where only $d_1$ and $d_3$ are active. The framework generalizes by activating all nine dimensions and providing a unified mechanism (geodesic optimization on the manifold) rather than ad hoc utility modifications.

The Bond Geodesic Equilibrium -- its definition, the augmented game construction, the BGE-Nash relationship theorem, the existence proof via Nash's theorem, the contraction lemma, the welfare results, and the applications to the three canonical games -- is the original contribution of Bond (2026b), *Geometric Ethics*, Chapter 20, here developed in full for the economic context. The interpretation of Nash equilibrium as a scalar projection of a richer geometric object is, to my knowledge, new.

Banach's contraction mapping theorem is from Banach (1922), "Sur les Operations dans les Ensembles Abstraits et leur Application aux Equations Integrales," *Fundamenta Mathematicae*. The application to game-theoretic best-response dynamics follows Moulin (1984), "Dominance Solvability and Cournot Stability," *Mathematical Social Sciences*, generalized to the augmented game setting.
