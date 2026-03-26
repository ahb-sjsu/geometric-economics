# Chapter 1: The Scalar Economy

> *"Not everything that can be counted counts, and not everything that counts can be counted."*
> — William Bruce Cameron (often attributed to Einstein)

---

> **RUNNING EXAMPLE — MARIA'S COFFEE SHOP**
>
> *Maria Esperanza owns a small coffee shop on Valencia Street in San Francisco's Mission District. The neighborhood is gentrifying. Her landlord, who owns the building through a real estate investment trust, has raised the rent 40%. The REIT's analysis is simple: comparable properties in the area command higher rents; the market rate has moved; the increase maximizes the building's yield.*
>
> *This analysis lives on a one-dimensional manifold: dollars. It cannot see that Maria employs four people from the neighborhood who will lose their jobs. It cannot see that the coffee shop is the informal community meeting point where immigrant families get help with paperwork. It cannot see that Maria's supplier, a small-batch roaster in Oakland, depends on her steady orders. It cannot see that the REIT's own long-term value depends on the neighborhood vitality that businesses like Maria's create.*
>
> *The landlord's spreadsheet captures one dimension of a nine-dimensional reality. This book develops the mathematics for the other eight.*

---

## The Shape of the Problem

Something has gone wrong with how we measure economic life — not the substance, but the *form*.

For most of its history, economics has operated with a tacit assumption: that economic evaluation, at the moment of decision, reduces to a single number. Utility theory makes this explicit: assign a real-valued utility to each outcome, choose the outcome with the highest utility. Cost-benefit analysis makes it operational: monetize all costs and benefits, sum them, and compare the totals. GDP makes it national: add up all market transactions in an economy and call the sum "economic output."

The output is always a number. A ranking. A line.

This book argues that the assumption is wrong. Not because economic decisions are *vague* or *irrational* or *too complex to model*, but because they have *geometric structure* that a single number cannot represent. Economic evaluation is not a point on a line. It is a location in a space — a space with dimensions, distances, directions, curvature, and boundaries. When we flatten this structure into a scalar, we lose information. And the information we lose is precisely the information that matters most in the decisions that matter most: which values are at stake, where the moral boundaries lie, how trust and fairness interact with price, and why the same monetary gamble produces different choices depending on how it is described.

The mathematical name for this structure is *geometry*. Not the geometry of triangles and circles, but the far richer geometry of manifolds, tensors, metrics, and fiber bundles — the mathematics that describes how matter curves spacetime, how electromagnetic fields transform under change of coordinates, and how conservation laws emerge from symmetry. **Geometric Economics** argues that economic reality has exactly this character.

## Three Failures of the Scalar

The limitations of scalar economic evaluation are not merely theoretical. They manifest in three domains where the stakes are highest.

### Failure 1: GDP

Gross Domestic Product is the most influential scalar in the history of economics. It measures the total market value of all final goods and services produced in a country in a given period. Governments rise and fall on its trajectory. Central banks calibrate monetary policy to its growth rate. International institutions rank nations by it.

And it is, by the standards of this book, a *contraction*: a mathematical operation that takes a multi-dimensional object and collapses it to a scalar, destroying all directional information in the process.

**[Empirical.]** What does GDP destroy? Consider two economies with identical GDP:

- Economy A has high material output ($d_1$), severe inequality ($d_3$), eroding trust ($d_5$), environmental degradation ($d_6$), and declining institutional legitimacy ($d_8$).
- Economy B has moderate material output ($d_1$), strong fairness norms ($d_3$), high social trust ($d_5$), sustainable resource use ($d_6$), and robust institutions ($d_8$).

GDP cannot distinguish them. The scalar has destroyed eight dimensions of information. The Stiglitz-Sen-Fitoussi Commission (2009) documented this failure exhaustively and recommended "multiple indicators." The geometric framework provides the mathematical alternative that the commission lacked: the *economic tensor*, of which GDP is a specific contraction — and the Scalar Irrecoverability Theorem (Chapter 6) proves that what the contraction destroys is mathematically irrecoverable from the scalar alone.

### Failure 2: Utility Maximization

**[Modeling Axiom.]** The utility function $u: X \to \mathbb{R}$ maps the set of possible outcomes $X$ to the real line. A rational agent chooses the $x \in X$ that maximizes $u(x)$. This is the foundation of rational choice theory, and it has a deep problem: the codomain is one-dimensional.

A student choosing between job offers weighs salary ($d_1$), autonomy ($d_4$), social impact ($d_6$), and alignment with identity ($d_7$). A patient choosing between treatments weighs survival probability ($d_1$), quality of life ($d_3$), family impact ($d_6$), and autonomy over end-of-life decisions ($d_4$). A voter choosing between candidates weighs economic policy ($d_1$), rights ($d_2$), fairness ($d_3$), and institutional legitimacy ($d_8$).

In each case, the agent must somehow compress a multi-dimensional evaluation into a single ranking. The utility function *assumes* this compression is possible without loss. The geometric framework *proves* it is not (Theorem 14).

The behavioral economics program — Kahneman's prospect theory, Thaler's nudges, Ariely's predictable irrationality — has documented the consequences of this compression. Loss aversion, framing effects, anchoring, the endowment effect — these are not cognitive biases. They are the *artifacts of dimensional collapse*: phenomena that appear anomalous on the scalar projection but are natural, predictable features of the full manifold. Chapter 4 demonstrates this in detail, showing that loss aversion is not a constant ($\lambda \approx 2.25$) but a variable that ranges from 1.0 to 3.53 depending on how many dimensions of the decision manifold are active.

### Failure 3: Cost-Benefit Analysis

Cost-benefit analysis is the workhorse of policy evaluation. Its virtue is that it provides a common currency in which all costs and benefits can be expressed and compared. Its vice is that the conversion to a common currency loses exactly the information that makes policy decisions difficult.

Should we build the highway through the wetland? Cost-benefit analysis sums the transportation savings, subtracts the environmental damage (monetized at some exchange rate), and reports a number. But the hard question is not what the number is — it is whether the exchange rate is legitimate. Can ecological value be converted to transportation value *at any rate*? The claim that it can is a substantive moral commitment, not a mathematical necessity. Different exchange rates — in the geometric vocabulary, different *metrics* — yield different answers. And the choice of metric is doing the real moral work, hidden behind the apparent objectivity of the calculation.

**[Modeling Axiom.]** A geometric approach would make the metric explicit. It would represent transportation value and ecological value as *dimensions* of a value space, and the metric tensor $g_{\mu\nu}$ would encode the structure of permissible trade-offs. If the two values are incommensurable — if no legitimate exchange rate exists — then the metric is *degenerate* along the relevant subspace: the off-diagonal components are undefined. The framework represents this as a structural feature of the economic landscape, not as a failure of analysis.

## What Geometry Provides

The word "geometry" comes from the Greek γεωμετρία — literally, "earth measurement." But modern geometry has traveled far from surveying. It is the mathematics of *structure*: how spaces are shaped, how quantities transform, how objects relate across changes of perspective.

What does this geometry provide for economics?

**Directions, not just magnitudes.** An economic change is not merely large or small. It *points somewhere* — toward greater fairness, toward less autonomy, toward more trust. A scalar captures the magnitude; a vector captures the magnitude *and* the direction. When we say "this policy increases welfare," the geometric question is: in which direction? At whose expense? Along which dimensions?

**A metric for comparison.** To say that two values are "incommensurable" is not to say that comparison is impossible. It is to make a precise structural claim about the metric tensor: the inner product between the two value-directions is undefined, or the metric is degenerate along the relevant subspace. To say that values *can* be traded off at some rate is to specify a non-degenerate metric with particular off-diagonal components. Different economic theories correspond to different metrics — and the choice of metric, typically hidden in scalar frameworks, becomes explicit and debatable.

**Boundaries and phase transitions.** Economic life is not uniformly smooth. There are thresholds where small changes produce large jumps: the difference between being employed and unemployed, between solvent and bankrupt, between legal and illegal. Scalar functions, if continuous, cannot represent such discontinuities. Geometric economics uses *stratified spaces* — spaces composed of smooth regions joined along boundaries where the rules change — to represent the patchwork structure of economic reality.

**Conservation laws.** Emmy Noether's theorem establishes that every continuous symmetry of a physical system corresponds to a conserved quantity. Applied to economics: the requirement that economic evaluation be invariant under re-description (the same transaction, described in different currencies, must receive the same evaluation) implies a conservation law for economic value. Value cannot be created or destroyed by relabeling. It can be generated (by production) or consumed (by use), but it must be accounted for consistently across all representations.

**Computability.** Geometric objects can be represented in computers, geometric operations can be implemented in algorithms, and geometric equations can be solved numerically. The companion library `eris-econ` demonstrates this: it implements the full decision manifold, A* pathfinding, and Bond Geodesic Equilibrium computation, and validates against published experimental data.

## What This Book Is Not

Intellectual honesty requires stating what we do not claim.

**This is not a claim about the metaphysics of value.** We do not assert that economic dimensions exist in some Platonic realm, or that the decision manifold is a fundamental constituent of reality. Our claim is *structural*: that geometric representation captures more of the structure of economic phenomena than scalar representation, loses less information, and enables analysis that scalar frameworks cannot support.

**This is not a new economic theory.** We do not propose "geometric consequentialism" or "manifold monetarism" as competitors to existing schools. Rather, the framework provides a common mathematical language in which existing theories can be stated with unprecedented precision. Neoclassical economics is a specific metric (diagonal, $d_1$-only). Behavioral economics is the study of heuristic corruption on the decision manifold. Institutional economics is the study of boundary constraints. The framework does not adjudicate between these theories; it makes their commitments explicit.

**This is not a rejection of mathematical economics.** On the contrary, it is an argument for *more* mathematics — specifically, the mathematics of geometry, which provides tools that the current apparatus of optimization theory and general equilibrium lacks.

## The Suspicious Coincidence

In 2025, while developing a framework for verifying that AI systems treat morally equivalent inputs equivalently, I noticed something strange. The mathematics I was using to describe moral reasoning — manifolds, metrics, gauge invariance, conservation laws — was identical to the mathematics of field theory in physics. Not merely analogous. *Identical.*

The conservation law for harm had the same form as the conservation law for charge. The stratification of moral space had the same structure as the stratification of phase spaces. The discrete transitions between Hohfeldian jural states mapped precisely onto the $D_4$ dihedral group — the same symmetry group that describes the symmetries of a square.

When I applied the same framework to economic decisions, the correspondences continued. The utility function was a specific contraction of a tensor. Nash equilibrium was the scalar projection of a richer geometric object. Prospect theory's "anomalies" — loss aversion, framing effects, the endowment effect — were natural geometric properties of a curved decision manifold with a Finsler metric.

I do not claim that this convergence reveals a deep metaphysical unity between physics and economics. Perhaps it does; perhaps it does not. What I claim is more modest and more useful: that the mathematical structures developed by physicists to describe nature are *also* the right structures for describing economic decision-making. The same patterns of transformation, conservation, and symmetry that organize the physical world also organize the economic world — or at least, modeling them as doing so yields a framework of extraordinary explanatory and predictive power.

## The Arc of the Book

**Part I: The Problem** motivates geometric economics. This chapter has argued that scalar reduction is the structural source of economics' most persistent failures. Chapter 2 traces proto-geometric insights through the history of economic thought — from Adam Smith's gradient flows to Amartya Sen's irreducibly plural capabilities — showing that the geometry was always latent in the tradition.

**Part II: The Framework** builds the apparatus. Chapter 3 defines the economic decision manifold. Chapter 4 equips it with a metric and derives prospect-theoretic phenomena as geometric properties. Chapter 5 develops the price signal as a heuristic field. Chapter 6 constructs the full economic tensor and proves the Scalar Irrecoverability Theorem.

**Part III: Dynamics and Symmetry** adds motion and conservation. Chapter 7 defines the Bond Geodesic Equilibrium and proves it subsumes Nash. Chapter 8 develops gauge invariance for economics — the principle that economic evaluations must not depend on the unit system. Chapter 9 derives conservation laws.

**Part IV: Failure Modes** catalogs what goes wrong. Chapter 10 maps the four geometric pathologies (heuristic corruption, objective hijacking, local minima, gauge breaking) onto market failures. Chapter 11 interprets financial crises as curvature singularities. Chapter 12 reframes inequality as metric distortion.

**Part V: Applications** demonstrates the framework's reach. Chapter 13 reinterprets trade theory. Chapter 14 reframes regulation. Chapter 15 connects climate economics to manifold curvature.

**Part VI: Horizons** (Chapter 16) surveys open questions and the prospects for geometric economics as a research program.

## A Note on Ambition

This book makes an ambitious claim: that the right mathematical language for economic decision-making is the language of modern geometry — manifolds, tensors, metrics, connections, gauge theory. This will strike some economists as overreach. Economics is a domain of practical trade-offs, institutional complexity, and irreducible uncertainty. How could it be captured by the same mathematics that describes general relativity?

The answer is that we are not claiming to *capture* economics. We are claiming to provide a *structural vocabulary* that makes economic reasoning more precise, more transparent, and more computable — without pretending to replace judgment with calculation. The vocabulary captures structure; institutional wisdom, democratic deliberation, and market dynamics fill in content. A map of a city captures the geometry of streets and landmarks; it does not capture the experience of walking through them. But the map is useful — sometimes indispensable — precisely because it captures structure that experience alone does not make explicit.

The economic map has been one-dimensional for too long. This book draws the other eight dimensions.

---

## Worked Example: Maria's Rent Increase

Let us formalize the opening scenario. Maria's landlord has raised the rent by 40%, from $5,000/month to $7,000/month. On the scalar projection ($d_1$ only), this is a simple calculation: $7,000 < revenue, so Maria can pay; $7,000 > revenue, so she closes.

On the full manifold, the decision is richer:

| Dimension | Status quo ($5,000 rent) | After increase ($7,000 rent) |
|-----------|--------------------------|-------------------------------|
| $d_1$: Consequences | Profitable, small margin | Break-even or loss |
| $d_2$: Rights | Lease respected | Lease terms exploited |
| $d_3$: Fairness | Rent proportional to value | Rent captures gentrification premium Maria created |
| $d_4$: Autonomy | Business decisions free | Forced to cut wages, hours, or quality |
| $d_5$: Trust | Stable landlord-tenant relationship | Relationship adversarial |
| $d_6$: Social impact | Community hub maintained | Four jobs lost, community space lost |
| $d_7$: Identity | Maria as ethical employer | Maria forced into choices she opposes |
| $d_8$: Legitimacy | Market-rate rent | REIT extracting community-created value |
| $d_9$: Epistemic | Maria knows her costs | Uncertainty about future increases |

The Mahalanobis distance between the status quo and the post-increase state is not 40% (the scalar) but a much larger displacement on the full manifold, because multiple dimensions shift simultaneously and the covariance matrix $\Sigma$ amplifies displacements along dimensions that co-vary (fairness and trust are correlated; when one drops, the other drops further).

The landlord's analysis, operating on $d_1$ alone, sees a rent increase of $2,000/month. The geometric analysis, operating on the full manifold, sees a displacement that crosses moral boundaries ($d_3$, $d_7$), degrades trust ($d_5$), destroys social capital ($d_6$), and creates existential uncertainty ($d_9$). The boundary penalties $\beta_k$ for the crossed thresholds dominate the Mahalanobis distance. The "rational" $d_1$ decision — raise rent to market — is revealed as a suboptimal path on the full manifold.

This is not a rejection of the landlord's right to charge market rent. It is a demonstration that the *market rate* itself is a scalar projection of a richer economic reality, and that decisions made on the projection can be strictly dominated by decisions made on the full manifold — dominated in the Pareto sense, where both landlord and community are better off under a path that respects the full geometry.

---

## Technical Appendix

**The Scalar Irrecoverability Theorem (Preview).** **[Conditional Theorem.]** Let $X \subseteq \mathbb{R}^n$ be a connected open set with $n \geq 2$. No continuous function $\phi: X \to \mathbb{R}$ is injective. Therefore, any scalar summary of a multi-dimensional economic state necessarily maps distinct states to the same number, and no post-hoc procedure can recover the lost distinction.

*Proof sketch.* By Brouwer's invariance of domain, $\mathbb{R}^n$ and $\mathbb{R}^1$ are not homeomorphic for $n \geq 2$. If $\phi$ were a continuous injection from the compact set $\overline{X}$ into $\mathbb{R}$, it would be a homeomorphism onto its image — embedding an $n$-dimensional space into $\mathbb{R}^1$. This contradicts invariance of domain. The full proof is given in Chapter 6.

**Dimensional Count (Justification).** **[Modeling Axiom.]** The claim that economic decisions involve nine dimensions is a modeling axiom, not a mathematical necessity. The specific dimensionality is inherited from the moral manifold developed in *Geometric Ethics* (Bond, 2026b, Chapter 5), where it is derived from a $3 \times 3$ decomposition of moral space (three normative modes × three scopes). The adaptation to economics replaces moral-specific labels with economic-specific ones while preserving the mathematical structure. The dimensionality is empirically testable: factor analysis of behavioral economic data should recover approximately nine independent factors. The eris-econ validation (Appendix C) provides preliminary evidence.

---

## Notes on Sources

The critique of GDP as a welfare measure is developed in Stiglitz, Sen, and Fitoussi (2009), *Mismeasuring Our Lives*. Raworth (2017), *Doughnut Economics*, provides the most accessible recent critique from within the economics profession. The Scalar Irrecoverability Theorem is a mathematical formalization of their qualitative arguments.

The behavioral economics canon includes Kahneman and Tversky (1979), "Prospect Theory: An Analysis of Decision Under Risk," *Econometrica*; Thaler (1980), "Toward a Positive Theory of Consumer Choice," *Journal of Economic Behavior and Organization*; and Ariely (2008), *Predictably Irrational*. We treat these as empirical data, not as theoretical commitments.

The geometric framework inherits from Bond (2026a), *Geometric Methods in Computational Modeling*; Bond (2026b), *Geometric Ethics*; and Bond (2026c), *Geometric Reasoning: From Search to Manifolds*. The specific application to economics was first presented as Chapter 20 of *Geometric Ethics* and is developed here in full.
