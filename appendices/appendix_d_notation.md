# Appendix D: Notation and Conventions

Consistent with the Geometric Series. Where domain-specific notation extends the parent conventions, the extension is marked with (GE).

---

## Manifolds and Spaces

| Symbol | Meaning | Introduced |
|---|---|---|
| $\mathcal{E}$ | Economic decision complex (weighted simplicial complex) | Ch. 3 |
| $d_1, \ldots, d_9$ | Nine economic dimensions (consequences through epistemic) | Ch. 3 |
| $\Sigma$ | $9 \times 9$ covariance matrix encoding dimension interactions | Ch. 4 |
| $T_pM$ | Tangent space at $p \in M$ | App. A |
| $\mathbb{R}^9$ | Economic state space (attribute space) | Ch. 3 |

## Dimensions (GE)

| Symbol | Name | Type | Introduced |
|---|---|---|---|
| $d_1$ | Consequences (monetary payoff) | Transferable | Ch. 3 |
| $d_2$ | Rights (property, contract) | Transferable | Ch. 3 |
| $d_3$ | Fairness (distributive justice) | Transferable | Ch. 3 |
| $d_4$ | Autonomy (freedom of action) | Transferable | Ch. 3 |
| $d_5$ | Trust (relational, institutional) | Evaluative | Ch. 3 |
| $d_6$ | Social impact (externalities, community) | Evaluative | Ch. 3 |
| $d_7$ | Identity / Virtue (self-conception) | Evaluative | Ch. 3 |
| $d_8$ | Legitimacy (institutional, regulatory) | Evaluative | Ch. 3 |
| $d_9$ | Epistemic (information quality) | Evaluative | Ch. 3 |

## Metrics and Distances

| Symbol | Meaning | Introduced |
|---|---|---|
| $g_{\mu\nu}$ | Metric tensor on the economic manifold; $g_{\mu\nu} = (\Sigma^{-1})_{\mu\nu}$ | Ch. 4 |
| $d_M(x, y)$ | Mahalanobis distance: $\sqrt{(x-y)^T \Sigma^{-1} (x-y)}$ | Ch. 4 |
| $w(v_i, v_j)$ | Edge weight: $\Delta\mathbf{a}^T \Sigma^{-1} \Delta\mathbf{a} + \sum_k \beta_k \cdot \mathbb{1}[\text{boundary}]$ | Ch. 4 |
| $\beta_k$ | Boundary penalty for constraint $k$ | Ch. 4 |
| $K(u,v)$ | Sectional curvature at $p$ in the plane spanned by $u, v$ | Ch. 11 |

## Pathfinding and Search

| Symbol | Meaning | Introduced |
|---|---|---|
| $\gamma^*$ | Bond geodesic (minimum-cost path on $\mathcal{E}$) | Ch. 7 |
| $h(x)$ | Price heuristic (scalar field on $\mathcal{E}$) | Ch. 5 |
| $g(x)$ | Accumulated path cost (System 2 computation) | Ch. 5 |
| $f(x) = g(x) + h(x)$ | A* evaluation function | Ch. 5 |
| $\text{BF}$ | Behavioral friction (total path cost on the manifold) | Ch. 7 |
| $G$ | Goal region (subset of vertices in $\mathcal{E}$) | Ch. 5 |

## Game Theory and Equilibrium (GE)

| Symbol | Meaning | Introduced |
|---|---|---|
| $\Gamma$ | Multi-agent BGE game | Ch. 7 |
| $\Gamma^+$ | Augmented game (Nash formulation of BGE) | Ch. 7 |
| $N$ | Set of players | Ch. 7 |
| $S_i$ | Agent $i$'s strategy set (paths in $\mathcal{E}_i$) | Ch. 7 |
| $u_i$ | Agent $i$'s payoff: $u_i = -\text{BF}_i$ | Ch. 7 |
| $\sigma_i^*$ | Agent $i$'s mixed BGE strategy (distribution over paths) | Ch. 7 |
| $\gamma_{-i}$ | Other agents' strategy profile | Ch. 7 |
| $\alpha_i$ | Self-separation parameter for agent $i$ | Ch. 7 |
| $\kappa_i$ | Cross-sensitivity parameter for agent $i$ | Ch. 7 |
| $L$ | Lipschitz constant: $L = \max_i (\kappa_i / \alpha_i)$ | Ch. 7 |
| BGE | Bond Geodesic Equilibrium | Ch. 7 |

## Symmetry and Gauge Theory (GE)

| Symbol | Meaning | Introduced |
|---|---|---|
| $\mathcal{G} = \mathbb{R}^+ \times S_n$ | Economic gauge group (scaling $\times$ relabeling) | Ch. 8 |
| $\mathbb{R}^+$ | Multiplicative group of positive reals (scaling) | Ch. 8 |
| $S_n$ | Symmetric group on $n$ elements (numeraire relabeling) | Ch. 8 |
| $\sigma_\lambda$ | Scaling transformation: $d_1 \mapsto \lambda \cdot d_1$ | Ch. 8 |
| $\rho_\pi$ | Relabeling transformation (numeraire permutation) | Ch. 8 |
| BIP | Bond Invariance Principle | Ch. 8 |
| $V_{ij}$ | Gauge violation tensor (GE) | Ch. 8 |

## Economic Tensors

| Symbol | Meaning | Introduced |
|---|---|---|
| $\mathbf{a} \in \mathbb{R}^9$ | Attribute vector (point on the manifold) | Ch. 3 |
| $\Delta\mathbf{a}$ | Attribute displacement (tangent vector) | Ch. 4 |
| $T^{\mu}{}_{\nu}$ | Economic tensor (obligations as vectors, interests as covectors) | Ch. 6 |
| $\text{tr}(T)$ | GDP: contraction of the economic tensor | Ch. 6 |

## Crisis Geometry (GE)

| Symbol | Meaning | Introduced |
|---|---|---|
| $\det(\Sigma)$ | Determinant of covariance matrix; $\to 0$ at singularity | Ch. 11 |
| $\det(g_{\mu\nu})$ | Determinant of metric tensor; $\to \infty$ at singularity | Ch. 11 |
| $\lambda$ | Loss aversion coefficient (varies 1.0--3.53) | Ch. 4 |

## Conventions

- **Bold lowercase** ($\mathbf{a}$, $\mathbf{v}$): vectors in $\mathbb{R}^n$
- **Bold uppercase** ($\mathbf{\Sigma}$): matrices
- **Calligraphic** ($\mathcal{E}$, $\mathcal{G}$): complexes, groups, and abstract spaces
- **Blackboard bold** ($\mathbb{R}$, $\mathbb{R}^+$): standard mathematical spaces
- **Greek lowercase** ($\gamma$, $\sigma$, $\lambda$): curves, strategies, parameters
- **Subscript indices** ($g_{\mu\nu}$, $\sigma_{jk}$): tensor and matrix components
- **Superscript indices** ($\gamma^k$, $T^{\mu}{}_{\nu}$): contravariant components
- Einstein summation convention is used throughout unless otherwise noted
- All logarithms are natural ($\ln$) unless specified as $\log_2$ or $\log_{10}$
- Statistical significance: * $p < 0.05$, ** $p < 0.01$, *** $p < 0.001$
- Currency values are in U.S. dollars unless otherwise specified
- "Scalar projection" always refers to the map $\pi_{d_1}: \mathbb{R}^9 \to \mathbb{R}$ that extracts the $d_1$ (monetary) component
