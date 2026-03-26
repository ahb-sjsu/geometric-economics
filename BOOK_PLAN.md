# Geometric Economics: Decision Manifolds, Equilibria, and the Geometry of Markets
## Book Plan — Andrew H. Bond

**Target**: ~80,000-100,000 words (16 chapters + appendices)
**Empirical basis**: eris-econ library (BGE, game theory, prospect theory), cross-cultural data (Fraser & Nettle, Ruggeri, Henrich et al.)
**Existing material**: Ch20 of Geometric Ethics (~7K words), eris-econ validation results, SERIES_OUTLINES.md

---

## Running Example: Maria's Coffee Shop

Maria owns a small coffee shop in a gentrifying neighborhood. Every business decision she makes — pricing, hiring, sourcing, expanding — lives on a 9-dimensional decision manifold. Classical economics says she should maximize profit (d₁). But she also cares about fair wages (d₃), her employees' autonomy (d₄), community trust (d₅), neighborhood impact (d₆), her identity as an ethical business owner (d₇), and compliance with regulations (d₈). Her decisions are geodesics on this manifold, not points on a profit curve.

---

## Part I: The Problem (Ch. 1-2)

### Ch. 1: The Scalar Economy (~6,000 words) — TO WRITE
- GDP as a specific contraction of the economic tensor
- Utility maximization and its paradoxes
- The Stiglitz-Sen-Fitoussi critique, geometrized
- Running example: Maria's profit-maximizing landlord raises rent 40%

### Ch. 2: Historical Precursors (~6,000 words) — TO WRITE
- Adam Smith's invisible hand as gradient flow
- Walras's general equilibrium as fixed point on a manifold
- Arrow-Debreu as topological existence proof
- Sen's capabilities as manifold coordinates
- Kahneman & Tversky as heuristic corruption cataloguers

## Part II: The Framework (Ch. 3-6)

### Ch. 3: The Economic Decision Manifold (~6,000 words) — PARTIAL (from Ch20)
- 9-dimensional space: consequences, rights, fairness, autonomy, trust, social impact, virtue/identity, legitimacy, epistemic
- Transferable (d₁-d₄) vs. evaluative (d₅-d₉) dimensions
- The Economic Decision Complex (Definition 20.1-20.2 from Ch20)

### Ch. 4: The Economic Metric (~6,000 words) — PARTIAL (from Ch20)
- Mahalanobis distance + boundary penalties
- Covariance matrix Σ encodes dimension interactions
- Different economics = different metrics (utilitarian, capabilities, welfare)
- Loss aversion as Finsler metric asymmetry

### Ch. 5: The Price Signal as Heuristic Field (~6,000 words) — TO WRITE
- Prices estimate cost of state transitions
- Admissible price heuristic = efficient market hypothesis
- Market failures as heuristic corruption
- Running example: Maria's coffee supplier raises prices — which heuristic does she follow?

### Ch. 6: Economic Tensors (~5,000 words) — PARTIAL (from Ch20)
- Obligations as vectors, interests as covectors
- Satisfaction as contraction
- GDP as contraction of the full economic tensor
- Scalar Irrecoverability for economics (Theorem 20.2)

## Part III: Dynamics and Symmetry (Ch. 7-9)

### Ch. 7: The Bond Geodesic Equilibrium (~7,000 words) — MOSTLY DONE (from Ch20)
- Central construction: BGE definition
- BGE-Nash relationship (Theorem 20.3)
- Existence of mixed BGE (Theorem 20.4)
- Contraction lemma for uniqueness (Lemma 20.1)
- Iterated best-response A* algorithm

### Ch. 8: Market Symmetries and Gauge Invariance (~6,000 words) — TO WRITE
- Economic BIP: invariance under currency relabeling, unit scaling
- Money illusion as gauge violation
- Sunk cost fallacy as path-dependence violating re-description invariance

### Ch. 9: Conservation Laws (~5,000 words) — TO WRITE
- Noether's theorem → economic BIP → conservation of value
- Value cannot be created by relabeling, only by real transformation
- Attribute conservation in bilateral exchange (Theorem 20.6 from Ch20)

## Part IV: Failure Modes (Ch. 10-12)

### Ch. 10: Market Failures as Geometric Pathologies (~6,000 words) — TO WRITE
- Heuristic corruption: externalities, information asymmetry
- Objective hijacking: regulatory capture, short-termism
- Local minima: bubbles, poverty traps
- Gauge breaking: money illusion, nominal/real confusion

### Ch. 11: Financial Crises as Curvature Singularities (~5,000 words) — TO WRITE
- 2008 as manifold singularity
- Metric degeneration, curvature divergence
- Recovery as smoothing the singularity

### Ch. 12: Inequality as Metric Distortion (~5,000 words) — TO WRITE
- Different agents experience different metrics
- A dollar worth more to the poor = different curvature
- Inequality is metric divergence, not just a number

## Part V: Applications (Ch. 13-15)

### Ch. 13: Trade as Geodesic Exchange (~5,000 words) — TO WRITE
- Comparative advantage as curvature statement
- Trade restrictions as artificial boundaries

### Ch. 14: Regulation as Boundary Enforcement (~5,000 words) — TO WRITE
- Environmental regulation = forbidden manifold regions
- Financial regulation = curvature constraints

### Ch. 15: The Discount Rate as Geodesic Curvature (~5,000 words) — TO WRITE
- Stern-Nordhaus debate as manifold curvature disagreement

## Part VI: Horizons

### Ch. 16: Open Questions (~4,000 words) — TO WRITE
- Measuring the economic metric empirically
- Economic No Escape Theorem
- Mechanism design on the manifold

## Appendices
- A: Mathematical Prerequisites (inherit from GR)
- B: The eris-econ Library (code reference)
- C: Empirical Validation Data

## Data Available
- eris-econ validation: 16/16 behavioral predictions, 2.70% MAE
- Loss aversion: varies 1.0-3.53 with dimensional activation
- KT17: 13/17 prospect theory problems correct
- Cross-cultural: Machiguenga, Tsimane, US, Lamalera
- Fraser & Nettle: 106 + 528 subjects, out-of-sample validation
