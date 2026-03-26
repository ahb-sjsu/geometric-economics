# Appendix A: Mathematical Prerequisites

This appendix collects the mathematical definitions and results used throughout the book. It is self-contained for readers unfamiliar with differential geometry, game theory, or the specific constructions of the geometric framework; those with background in these areas may skip directly to the chapters. Full proofs and extended treatments can be found in *Geometric Methods in Computational Modeling* (Bond, 2026a) and *Geometric Reasoning* (Bond, 2026c).

---

## A.1 Smooth Manifolds and Riemannian Geometry

**Definition A.1 (Topological Manifold).** A *topological manifold* of dimension $n$ is a Hausdorff, second-countable topological space $M$ such that every point $p \in M$ has a neighborhood homeomorphic to an open subset of $\mathbb{R}^n$.

**Definition A.2 (Smooth Manifold).** A *smooth manifold* is a topological manifold equipped with a maximal smooth atlas --- a collection of charts $\{(U_\alpha, \varphi_\alpha)\}$ covering $M$ such that all transition maps $\varphi_\beta \circ \varphi_\alpha^{-1}$ are $C^\infty$.

*Economic interpretation*: The economic decision manifold is a 9-dimensional space. Each "chart" corresponds to a particular accounting system, unit convention, or cultural framework for describing economic states. Transition maps are the conversions between these descriptions (e.g., currency conversion). The smoothness requirement says that small changes in one description produce small changes in any other. (See Chapter 3.)

**Definition A.3 (Riemannian Metric).** A *Riemannian metric* on a smooth manifold $M$ is a smooth assignment of a positive-definite inner product $g_p: T_pM \times T_pM \to \mathbb{R}$ to each tangent space $T_pM$. In local coordinates, $g = g_{ij} \, dx^i \otimes dx^j$.

**Definition A.4 (Geodesic).** A curve $\gamma: [0,1] \to M$ is a *geodesic* if it satisfies

$$\frac{d^2 \gamma^k}{dt^2} + \Gamma^k_{ij} \frac{d\gamma^i}{dt} \frac{d\gamma^j}{dt} = 0$$

where $\Gamma^k_{ij}$ are the Christoffel symbols of the Levi-Civita connection.

**Definition A.5 (Geodesic Distance).** The geodesic distance between $p, q \in M$ is

$$d(p, q) = \inf_\gamma \int_0^1 \sqrt{g_{\gamma(t)}(\dot{\gamma}(t), \dot{\gamma}(t))} \, dt$$

where the infimum is over all smooth curves from $p$ to $q$.

*Economic interpretation*: Geodesics are the "optimal paths" on the decision manifold --- the paths of least total cost when all nine dimensions are accounted for. The Bond geodesic (Chapter 7) is the discrete analogue on the economic decision complex.

**Definition A.6 (Sectional Curvature).** The sectional curvature at a point $p$ in the plane spanned by tangent vectors $u, v \in T_pM$ is

$$K(u,v) = \frac{R(u,v,v,u)}{g(u,u)g(v,v) - g(u,v)^2}$$

where $R$ is the Riemann curvature tensor. Curvature measures how rapidly nearby geodesics diverge or converge. In a flat space ($K = 0$), parallel geodesics remain parallel. In positive curvature ($K > 0$), they converge. In negative curvature ($K < 0$), they diverge.

*Economic interpretation*: Curvature determines how sensitive economic outcomes are to small perturbations. Divergent curvature (Chapter 11) is the mathematical mechanism of financial contagion: small perturbations produce arbitrarily large changes in the geodesic.

---

## A.2 The Mahalanobis Distance

**Definition A.7 (Mahalanobis Distance).** Given a positive-definite covariance matrix $\Sigma \in \mathbb{R}^{n \times n}$, the *Mahalanobis distance* between vectors $x, y \in \mathbb{R}^n$ is

$$d_M(x, y) = \sqrt{(x - y)^T \Sigma^{-1} (x - y)}$$

**Properties:**
- When $\Sigma = I$ (identity), the Mahalanobis distance reduces to Euclidean distance.
- The Mahalanobis distance is invariant under linear transformations that preserve $\Sigma$: if $y = Ax$ and $\Sigma_y = A\Sigma_x A^T$, then $d_M(y_1, y_2; \Sigma_y) = d_M(x_1, x_2; \Sigma_x)$.
- The Mahalanobis distance accounts for correlations between dimensions: if $d_1$ and $d_3$ are highly correlated ($\sigma_{13}$ is large), a change that affects both in the expected direction has lower Mahalanobis distance than a change affecting them independently.

*Economic interpretation*: The Mahalanobis distance is the natural metric on the economic decision manifold (Chapter 4). The covariance matrix $\Sigma$ encodes how the nine economic dimensions interact: which tradeoffs are easy (correlated dimensions) and which are costly (independent or anti-correlated dimensions). Different economic cultures correspond to different $\Sigma$ matrices, producing different metrics on the same underlying manifold.

---

## A.3 A* Search

**Definition A.8 (A* Search).** Given a weighted graph $(V, E, w)$ with start vertex $v_0$ and goal set $G \subseteq V$, and a heuristic function $h: V \to \mathbb{R}_{\geq 0}$, the A* algorithm finds the minimum-cost path from $v_0$ to $G$ by maintaining the evaluation function

$$f(v) = g(v) + h(v)$$

where $g(v)$ is the actual cost of the best known path from $v_0$ to $v$, and $h(v)$ is the heuristic estimate of the cost from $v$ to the nearest goal vertex.

**Theorem A.1 (Optimality of A*).** If $h$ is *admissible* --- $h(v) \leq h^*(v)$ for all $v$, where $h^*(v)$ is the true minimum cost from $v$ to $G$ --- and *consistent* --- $h(v) \leq w(v, v') + h(v')$ for all edges $(v, v')$ --- then A* returns an optimal path.

*Economic interpretation*: Economic decision-making is A* search on the decision complex (Chapter 5). The $g(v)$ component is System 2 deliberation --- the accumulated, verified cost of the path so far. The $h(v)$ component is System 1 heuristic estimation --- the fast, approximate estimate of how much further cost remains. Prices are the economic heuristic field: an admissible price heuristic corresponds to an efficient market. Market failures are failures of heuristic admissibility. (See Chapter 5.)

---

## A.4 Simplicial Complexes

**Definition A.9 (Simplicial Complex).** A *simplicial complex* $K$ is a collection of simplices (vertices, edges, triangles, tetrahedra, ...) closed under taking faces. A $k$-simplex is the convex hull of $k+1$ affinely independent points.

**Definition A.10 (Weighted Simplicial Complex).** A *weighted simplicial complex* is a simplicial complex equipped with a weight function $w: K_1 \to \mathbb{R}_{> 0}$ on its 1-simplices (edges).

*Economic interpretation*: The economic decision complex $\mathcal{E}$ (Chapter 3) is a weighted simplicial complex whose vertices are economic states (points in $\mathbb{R}^9$), whose edges are feasible economic actions, and whose edge weights are the Mahalanobis distance plus boundary penalties. Higher-dimensional simplices encode multi-step economic plans.

---

## A.5 Noether's Theorem

**Theorem A.2 (Noether's Theorem, 1918).** If the action functional $S[\gamma] = \int L(\gamma, \dot{\gamma}, t) \, dt$ is invariant under a continuous one-parameter group of transformations $\gamma \mapsto \gamma_\varepsilon$, then there exists a conserved quantity $Q$ along the equations of motion:

$$\frac{dQ}{dt} = 0$$

The conserved quantity is

$$Q = \frac{\partial L}{\partial \dot{\gamma}^i} \xi^i$$

where $\xi^i = \frac{d\gamma^i_\varepsilon}{d\varepsilon}\big|_{\varepsilon=0}$ is the generator of the symmetry.

**Correspondence (symmetry $\to$ conservation):**

| Symmetry | Conservation Law |
|----------|-----------------|
| Time translation invariance | Energy conservation |
| Spatial translation invariance | Momentum conservation |
| Rotational invariance | Angular momentum conservation |
| Gauge invariance ($U(1)$) | Charge conservation |

*Economic interpretation*: Chapter 9 applies Noether's theorem to the economic gauge group $\mathcal{G} = \mathbb{R}^+ \times S_n$. The continuous scaling symmetry $\mathbb{R}^+$ produces a conservation law for economic value: value cannot be created by relabeling (changing currency, units, or numeraire). The discrete component $S_n$ produces selection rules rather than continuous conservation laws.

---

## A.6 Game Theory Basics

**Definition A.11 (Normal-Form Game).** A *normal-form game* is a triple $\Gamma = (N, \{S_i\}_{i \in N}, \{u_i\}_{i \in N})$ where $N$ is a finite set of players, $S_i$ is player $i$'s strategy set, and $u_i: \prod_{j \in N} S_j \to \mathbb{R}$ is player $i$'s payoff function.

**Definition A.12 (Nash Equilibrium).** A strategy profile $s^* = (s_1^*, \ldots, s_n^*)$ is a *Nash equilibrium* if no player can improve their payoff by unilateral deviation:

$$u_i(s_i^*, s_{-i}^*) \geq u_i(s_i, s_{-i}^*) \quad \forall \, s_i \in S_i, \; \forall \, i \in N$$

**Theorem A.3 (Nash, 1950).** Every finite game has at least one mixed-strategy Nash equilibrium.

*Economic interpretation*: The Bond Geodesic Equilibrium (Chapter 7) is Nash equilibrium of the augmented game $\Gamma^+$, where payoffs are the negative of behavioral friction on the full manifold. Classical Nash equilibrium is the scalar projection --- the special case where only $d_1$ (monetary payoff) is active. The BGE-Nash theorem (Theorem 21) establishes this relationship precisely.

---

## A.7 The Scalar Irrecoverability Theorem

**Theorem A.4 (Scalar Irrecoverability).** Let $n > 1$. No continuous function $\phi: \mathbb{R}^n \to \mathbb{R}$ is injective.

*Proof.* By the rank-nullity theorem, $\ker(D\phi_p)$ has dimension $\geq n - 1$ at every regular point $p$. Thus $\phi$ identifies distinct points in $\mathbb{R}^n$ that differ only along the kernel directions. The collapse is irrecoverable: no continuous function $\psi: \mathbb{R} \to \mathbb{R}^n$ satisfies $\psi \circ \phi = \text{id}$, because such a $\psi$ would imply injectivity of $\phi$. $\square$

**Corollary A.5 (GDP Irrecoverability).** GDP is a continuous function $\phi: \mathbb{R}^9 \to \mathbb{R}$ on the economic state space. By Theorem A.4, GDP identifies distinct economic states that differ on at least 8 of 9 dimensions. No post-hoc adjustment, weighting, or correction can recover the information that GDP discards.

*Economic interpretation*: This is the mathematical foundation of the book's critique of scalar economics. Utility functions, cost-benefit analyses, and single-index welfare measures all fall under the scope of the theorem. Chapter 6 develops the full implications.

---

## A.8 Finsler Metrics and Asymmetric Distance

**Definition A.13 (Finsler Metric).** A *Finsler metric* on a manifold $M$ is a smooth function $F: TM \to \mathbb{R}_{\geq 0}$ that is positively homogeneous of degree 1 in each fiber ($F(x, \lambda v) = \lambda F(x, v)$ for $\lambda > 0$) and strictly convex in $v$. Unlike a Riemannian metric, a Finsler metric need not satisfy $F(x, v) = F(x, -v)$.

*Economic interpretation*: Loss aversion makes the economic metric asymmetric: the cost of moving from state $A$ to state $B$ (a gain) differs from the cost of moving from $B$ to $A$ (a loss of the same magnitude). This asymmetry is naturally modeled by a Finsler metric (Chapter 4). The loss aversion coefficient $\lambda$ --- which varies between 1.0 and 3.53 with dimensional activation in the eris-econ validation --- quantifies the degree of asymmetry.

---

## A.9 Gauge Theory Fundamentals

**Definition A.14 (Gauge Group).** A *gauge group* $G$ is a group of transformations that change the mathematical description of a system without changing its physical (or economic) content.

**Definition A.15 (Gauge Invariance).** A functional $J$ is *gauge-invariant* if $J(\tau(x)) = J(x)$ for all gauge transformations $\tau \in G$.

**Definition A.16 (Gauge Violation).** A *gauge violation* is a measurable failure of invariance: $J(\tau(x)) \neq J(x)$ for some $\tau \in G$.

*Economic interpretation*: The economic gauge group is $\mathcal{G} = \mathbb{R}^+ \times S_n$ (scaling and relabeling). Gauge invariance means that economic decisions should not depend on the units used to describe them. Money illusion, sunk cost fallacy, and denomination effects are gauge violations --- failures of invariance under meaning-preserving re-description. (See Chapter 8.)
