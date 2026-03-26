# Geometric Economics: Decision Manifolds, Equilibria, and the Geometry of Markets

**Andrew H. Bond**
Senior Member, IEEE
Department of Computer Engineering
San Jose State University
andrew.bond@sjsu.edu

Spring 2026

---

## Preface

Every economics textbook begins with a simplification: reduce the agent to a utility maximizer, reduce the outcome to a number, find the number that is biggest. This simplification has been extraordinarily productive. It built the edifice of modern economics — general equilibrium, welfare theorems, mechanism design, auction theory — and its practitioners have earned more than their share of Nobel prizes.

This book argues that the simplification is also the source of economics' most persistent failures. Not because humans are irrational — the behavioral economists have made that case convincingly — but because the space on which economic decisions are made has *geometric structure* that scalar utility cannot represent. When we compress a nine-dimensional decision into a single number, we lose precisely the information that determines actual behavior: which values trade off against which, where the moral boundaries lie, how trust and fairness interact with price, and why the same monetary gamble produces different choices depending on whether it is framed as a loss or a gain.

The mathematical name for this structure is *geometry*. Not the geometry of triangles but the geometry of curved spaces, tensor fields, and symmetry groups — the same mathematics that describes how matter curves spacetime, how electromagnetic fields transform under change of coordinates, and how conservation laws emerge from symmetry. This book applies that mathematics to economic decision-making and demonstrates that it resolves, from first principles, puzzles that have resisted scalar analysis for decades.

The central construction is the **Bond Geodesic Equilibrium** (BGE), a generalization of Nash equilibrium to the full decision manifold. We prove that Nash equilibrium is the scalar projection of BGE — the special case obtained by collapsing all dimensions except monetary payoff. The projection is lossy: the Scalar Irrecoverability Theorem (Chapter 6) proves that the information destroyed by this collapse is mathematically irrecoverable. Homo economicus is not wrong. It is a shadow on the wall of a nine-dimensional cave.

The framework is empirically grounded. The companion library `eris-econ` (published on PyPI) implements the full pipeline — decision manifold, A* pathfinding, BGE computation — and validates against published experimental data from game theory and prospect theory across multiple cultures. The results: 16 of 16 behavioral predictions correct at 2.70% mean absolute error, including cross-cultural variation in ultimatum game offers explained by metric differences rather than "cultural preferences."

This is the fourth book in the Geometric Series. *Geometric Methods in Computational Modeling* (Bond, 2026a) provides the mathematical toolkit. *Geometric Ethics* (Bond, 2026b) develops the moral manifold. *Geometric Reasoning* (Bond, 2026c) generalizes from ethics to all reasoning, establishing the search-geometry connection, the heuristic field formalism, and the failure taxonomy. The present book instantiates that general framework on the economic decision manifold.

I thank my colleagues in the SJSU Department of Computer Engineering, the researchers whose experimental data make the empirical validation possible — especially Fraser, Nettle, Ruggeri, and their collaborators — and the computational resources provided by the Atlas workstation and San Jose State University.

Andrew H. Bond
San Jose, California
March 2026

---

## Core Objects at a Glance

| Object | What It Is | Where Developed |
|--------|-----------|-----------------|
| **Economic decision complex** $\mathcal{E}$ | 9-dimensional weighted simplicial complex of economic states and transitions | Ch. 3 |
| **Decision manifold metric** | Mahalanobis distance + boundary penalties: $d(s,t) = \sqrt{(s-t)^T \Sigma^{-1} (s-t)} + \sum_k \beta_k \cdot \mathbb{1}[\text{boundary}_k]$ | Ch. 4 |
| **Price heuristic** $h(x)$ | The price signal as scalar field guiding economic search; admissible = efficient market | Ch. 5 |
| **Economic tensor** | Obligations as vectors, interests as covectors, GDP as a specific contraction | Ch. 6 |
| **Bond Geodesic Equilibrium** (BGE) | Multi-agent equilibrium on the full manifold; Nash is the d₁-only projection | Ch. 7 |
| **Economic gauge group** | $\mathbb{R}^+ \times S_n$ (scaling × relabeling); invariance under unit changes | Ch. 8 |
| **Value conservation** | Noether's theorem applied to economic BIP; value ≠ created by relabeling | Ch. 9 |
| **Scalar Irrecoverability** | No continuous $\phi: \mathbb{R}^9 \to \mathbb{R}$ is injective; GDP destroys 8 dimensions | Ch. 6 |

## Key Results at a Glance

| Finding | Source |
|---------|--------|
| Nash equilibrium is the scalar projection of BGE (Theorem 21) | eris-econ |
| Loss aversion varies 1.0–3.53 with dimensional activation (contradicts constant λ) | eris-econ |
| 16/16 behavioral predictions correct at 2.70% MAE | eris-econ validation |
| Kahneman & Tversky 17 problems: 13/17 predicted (76%) | eris-econ |
| Cross-cultural ultimatum offers explained by metric variation | Henrich et al. data |
| Public goods: 4.3% out-of-sample prediction error | Fraser & Nettle |
| Endowment ratio: 1.66 (consistent with experimental WTA/WTP) | eris-econ |

## How to Read This Book

- **The theoretical path**: Chapters 1–9. From the scalar failure through the full geometric framework.
- **The empirical path**: Chapters 3, 4, 7, and the worked examples throughout. For readers who want data and predictions.
- **The applied path**: Chapters 1, 7, 10, 13–15. From motivation through equilibrium to applications.
- **The fast path**: Chapters 1, 6, 7, 10. The scalar failure, irrecoverability, BGE, and market failures. The core argument in four chapters.

Each chapter opens with a running example — Maria, who owns a small coffee shop in a gentrifying neighborhood — that grounds the abstract framework in the decisions of a real business owner navigating a multi-dimensional economic landscape.

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

## Table of Contents

### Part I: The Problem
1. The Scalar Economy
2. Historical Precursors — Geometry Before Geometry

### Part II: The Framework
3. The Economic Decision Manifold
4. The Economic Metric
5. The Price Signal as Heuristic Field
6. Economic Tensors and Scalar Irrecoverability

### Part III: Dynamics and Symmetry
7. The Bond Geodesic Equilibrium
8. Market Symmetries and Gauge Invariance
9. Conservation Laws for Economics

### Part IV: Failure Modes
10. Market Failures as Geometric Pathologies
11. Financial Crises as Curvature Singularities
12. Inequality as Metric Distortion

### Part V: Applications
13. Trade as Geodesic Exchange
14. Regulation as Boundary Enforcement
15. The Discount Rate as Geodesic Curvature

### Part VI: Horizons
16. Open Questions

### Appendices
A. Mathematical Prerequisites
B. The eris-econ Library
C. Empirical Validation Data

---

## Notation

| Symbol | Meaning |
|--------|---------|
| $\mathcal{E}$ | Economic decision complex |
| $d_1, \ldots, d_9$ | Nine economic dimensions (consequences through epistemic) |
| $\Sigma$ | 9×9 covariance matrix encoding dimension interactions |
| $\beta_k$ | Boundary penalty for constraint $k$ |
| $\gamma^*$ | Bond geodesic (optimal path on the decision manifold) |
| $h(x)$ | Price heuristic (scalar field on $\mathcal{E}$) |
| $f(x) = g(x) + h(x)$ | A* evaluation function ($g$ = System 2, $h$ = System 1) |
| $\text{BF}$ | Behavioral friction (total edge-weight cost of a path) |
| $\Gamma^+$ | Augmented game (multi-agent decision problem on $\mathcal{E}$) |
| $\alpha_i, \kappa_i$ | Self-separation and cross-sensitivity for agent $i$ |
| $\lambda$ | Loss aversion coefficient (varies with dimensionality in our framework) |
| BGE | Bond Geodesic Equilibrium |
| BIP | Bond Invariance Principle |
