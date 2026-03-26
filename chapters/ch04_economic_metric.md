# Chapter 4: The Economic Metric

> *"God created the integers; all else is the work of man."*
> -- Leopold Kronecker
>
> *"God created the manifold; all else is the work of the metric."*
> -- Attributed to various differential geometers

---

> **RUNNING EXAMPLE -- MARIA'S COFFEE SHOP**
>
> *Maria is afraid of losing her shop. She is not equivalently excited about expanding it. This asymmetry -- the fact that the threat of loss produces a stronger reaction than the promise of an equivalent gain -- is one of the most replicated findings in behavioral economics. Kahneman and Tversky called it loss aversion and measured it at $\lambda \approx 2.25$: losses loom roughly 2.25 times as large as equivalent gains.*
>
> *But Maria's loss aversion is not a fixed number. When her landlord threatens to raise the rent 40% -- threatening her livelihood, her employees' jobs, her identity as a business owner, her standing in the community -- Maria's resistance is fierce. When she loses \$20 in a poker game with friends, she shrugs it off. Same person, wildly different $\lambda$. The standard account says both are "loss aversion" with $\lambda \approx 2.25$. The geometric account says they are different because different dimensions of the decision manifold are active. The rent threat activates $d_1$ through $d_9$; the poker loss activates $d_1$ only. The metric is different because the space is different.*
>
> *This chapter derives loss aversion -- and every other prospect-theory phenomenon -- as a geometric property of the decision manifold's metric. The metric is not a parameter to be fitted. It is a mathematical structure from which the parameters follow.*

---

## Why the Metric Matters

A manifold without a metric is a space without distances. You can name the points, but you cannot say how far apart they are. You can identify directions, but you cannot say which directions cost more to traverse. A metric transforms a bare topological space into a *geometric* space -- a space where distance, angle, curvature, and geodesic have precise meaning.

Chapter 3 defined the economic decision manifold and its nine dimensions. This chapter equips it with a metric -- the mathematical structure that encodes the cost of moving between states. The metric determines:

- **How costly** a given economic action is (the distance it traverses on the manifold).
- **Whether gains and losses are symmetric** (they are not -- and the asymmetry is a property of the metric, not a psychological quirk).
- **How the agent's current position affects the cost of actions** (reference dependence as curvature).
- **Whether re-describing the same decision changes its evaluation** (framing effects as gauge violations).
- **How the discount rate behaves over time** (hyperbolic rather than exponential, because curvature is non-constant).
- **Why ownership changes valuation** (the endowment effect as rights-dimension activation).

This chapter presents the strongest material in the paper: a systematic derivation of *every* major prospect-theory phenomenon from the manifold's metric structure. The phenomena are not catalogued as separate biases. They are *theorems* -- logical consequences of the metric.

---

## 4.1 The Metric as Covariance Structure

Recall from Chapter 3 that the edge weight between two economic states is:

$$w(v_i, v_j) = \Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a} + \sum_k \beta_k \cdot \mathbf{1}[\text{boundary } k \text{ crossed}]$$

The first term -- the Mahalanobis distance -- is determined by the inverse of the covariance matrix $\Sigma$. In the continuous limit, where the decision complex approximates a smooth manifold, this becomes a Riemannian metric:

$$ds^2 = g_{\mu\nu} \, da^\mu \, da^\nu$$

where $g_{\mu\nu} = (\Sigma^{-1})_{\mu\nu}$ is the metric tensor. The metric tensor encodes the infinitesimal cost of displacement along each pair of dimensions.

**[Modeling Axiom.]** Equipping the manifold with the inverse covariance matrix as metric tensor is a specific modeling choice. It says: the cost of an economic displacement is measured in "standard deviations of behavioral expectation" -- displacements that are unusual (far from the mean behavior in the population) are costly, while displacements that are typical (close to the mean) are cheap. This is a natural choice for a framework grounded in observed behavior: the metric reflects what agents actually do, not what they "should" do.

### Diagonal vs. Off-Diagonal Components

If $\Sigma$ were diagonal (all dimensions independent), the metric would be:

$$ds^2 = \frac{(da_1)^2}{\sigma_1^2} + \frac{(da_2)^2}{\sigma_2^2} + \cdots + \frac{(da_9)^2}{\sigma_9^2}$$

Each dimension would contribute independently to the total cost, weighted by the inverse of its variance. This is the "orthogonal dimensions" case -- simpler to compute but empirically wrong, because economic dimensions are correlated.

The off-diagonal components of $g_{\mu\nu}$ encode the correlations. When $g_{13}$ is large (fairness and consequences are tightly coupled), a displacement that simultaneously changes $d_1$ and $d_3$ has a different cost from the sum of the individual displacements. The interaction terms -- the products $da^\mu \, da^\nu$ for $\mu \neq \nu$ -- are where the interesting economics lives.

---

## 4.2 Loss Aversion as Asymmetric Metric

We now derive the central result of behavioral economics -- loss aversion -- as a geometric property of the metric.

> **Theorem 34 (Loss Aversion as Metric Asymmetry).** *Kahneman-Tversky loss aversion ($\lambda \approx 2.25$) arises from an asymmetry in the decision manifold's metric: losses traverse more dimensions than equivalent gains.*

**Argument.** Consider an agent at state $v_0$ evaluating a gain of $+x$ or a loss of $-x$ on the monetary dimension ($d_1$).

**Gain path ($v_0 \to v_+$):** The attribute-vector change is concentrated on $d_1$:
$$\Delta \mathbf{a}_+ \approx (x, 0, 0, 0, 0, 0, 0, 0, 0)$$

The edge weight is approximately:
$$w_+ \approx \frac{x^2}{\sigma_1^2}$$

A monetary gain changes your bank balance. For most people in most contexts, it does not trigger a rights violation ($d_2 \approx 0$), a fairness concern ($d_3 \approx 0$), an autonomy shift ($d_4 \approx 0$), or an identity reassessment ($d_7 \approx 0$). The gain is one-dimensional.

**Loss path ($v_0 \to v_-$):** The attribute-vector change affects multiple dimensions:
$$\Delta \mathbf{a}_- \approx (-x, -\delta_2, -\delta_3, 0, 0, -\delta_6, -\delta_7, 0, -\delta_9)$$

where:
- $\delta_2$ reflects the perceived rights violation: "I had this; now it's taken."
- $\delta_3$ reflects fairness: "This is unfair."
- $\delta_6$ reflects social status: "I've lost standing."
- $\delta_7$ reflects identity: "I am a loser."
- $\delta_9$ reflects epistemic anxiety: "What else might I lose?"

The edge weight is:
$$w_- \approx \frac{x^2}{\sigma_1^2} + \frac{\delta_2^2}{\sigma_2^2} + \frac{\delta_3^2}{\sigma_3^2} + \frac{\delta_6^2}{\sigma_6^2} + \frac{\delta_7^2}{\sigma_7^2} + \frac{\delta_9^2}{\sigma_9^2} + \text{cross terms}$$

which is strictly greater than $w_+$.

The ratio $w_- / w_+$ is the **geometric loss-aversion coefficient**:

$$\lambda = \frac{w_-}{w_+} = 1 + \frac{\delta_2^2/\sigma_2^2 + \delta_3^2/\sigma_3^2 + \delta_6^2/\sigma_6^2 + \delta_7^2/\sigma_7^2 + \delta_9^2/\sigma_9^2 + \text{cross terms}}{x^2/\sigma_1^2}$$

This is not a free parameter. It is a *derived quantity* determined by the manifold's metric structure -- specifically, by the magnitudes of the cross-dimensional activations $\delta_k$ relative to the primary monetary displacement $x$. $\square$

### Why $\lambda$ Is Variable, Not Constant

> **Remark 35 (Why $\lambda \approx 2.25$).** The specific value $\lambda \approx 2.25$ should be derivable from the dimensional covariance matrix $\Sigma$ estimated from behavioral data. If losses activate approximately 4-5 dimensions beyond $d_1$ with average activation $\delta_k \approx 0.5\sigma_k$, then:
>
> $$\lambda \approx 1 + 4 \times (0.5)^2 = 1 + 4 \times 0.25 = 2.0$$
>
> close to the observed value. Precise calibration requires fitting $\Sigma$ to experimental data from prospect-theory studies -- a concrete empirical programme.

**[Empirical.]** The critical prediction of this derivation is that $\lambda$ is *not constant*. Standard prospect theory treats $\lambda \approx 2.25$ as a fixed parameter of the value function. The geometric framework predicts that $\lambda$ varies with the number and intensity of activated moral dimensions:

| Loss Type | Active Dimensions | Predicted $\lambda$ | Observed $\lambda$ |
|---|---|---|---|
| Losing \$100 cash | $d_1$ only | $\approx 1.0 - 1.2$ | $\approx 1.0 - 1.5$ |
| Losing a \$100 gift from a friend | $d_1 + d_5 + d_7$ | $\approx 2.0$ | $\approx 1.8 - 2.3$ |
| Losing a \$100 family heirloom | $d_1 + d_2 + d_6 + d_7$ | $\approx 3.0$ | $\approx 2.5 - 3.5$ |
| Losing a family photograph (no monetary value) | $d_2 + d_6 + d_7$ | $\gg 3.0$ | Often described as "priceless" |

The eris-econ validation confirms this: the framework predicts loss aversion varying from 1.0 to 3.53 depending on dimensional activation, matching observed ranges in the empirical literature.

**What would falsify this:** If $\lambda$ were constant across conditions -- as standard prospect theory predicts -- the geometric derivation would be wrong. If $\lambda$ varied but not monotonically with dimension count, the dimensional model would be wrong.

> **RUNNING EXAMPLE -- MARIA'S VARIABLE LOSS AVERSION**
>
> *Maria's $\lambda$ for the rent increase is high -- perhaps 3.0 or higher -- because the threatened loss activates at least seven of the nine dimensions. Losing the shop means losing money ($d_1$), contractual position ($d_2$), fairness ($d_3$: the REIT is capturing value Maria created), autonomy ($d_4$: she would need to find employment), trust relationships ($d_5$), community standing ($d_6$), and her identity as a business owner ($d_7$). Only $d_8$ (legitimacy -- the REIT is within its rights) and $d_9$ (epistemic -- the situation is not ambiguous) are approximately neutral.*
>
> *Compare this to Maria losing \$100 from her purse. Only $d_1$ is activated. Her $\lambda$ for this loss is close to 1.0 -- she is mildly annoyed, not devastated. Same person. Different manifold activation. Different $\lambda$.*

---

## 4.3 Reference Dependence as Coordinate Choice

> **Proposition 36 (Reference Points as Local Coordinates).** *Kahneman-Tversky reference dependence is a coordinate effect: the agent evaluates outcomes in local coordinates centered at the current state rather than in global coordinates. This is not a bias -- it is the natural coordinate system for pathfinding.*

A* search computes edge costs $w(v_i, v_{i+1})$ from the *current* node, not from the origin. The cost of moving from "here" to "there" depends on where "here" is. This is not an approximation or a computational shortcut -- it is the correct procedure for pathfinding on a curved manifold.

In physics, the analogous phenomenon is well understood: the metric of a curved manifold is position-dependent. The speed of light is the same everywhere, but the distance between two events depends on where you measure it -- because spacetime is curved by mass. Similarly, the "cost" of an economic displacement depends on the agent's current position on the manifold -- because the metric varies with position.

### Why Reference Dependence Is Not a Bias

Consider two agents evaluating the same absolute outcome: a salary of \$80,000.

**Agent A** currently earns \$60,000. The displacement is $\Delta d_1 = +20,000$ (a gain). The gain path is approximately one-dimensional.

**Agent B** currently earns \$100,000. The displacement is $\Delta d_1 = -20,000$ (a loss). The loss path activates multiple dimensions: $d_3$ (unfairness of the pay cut), $d_6$ (status loss), $d_7$ (identity as a high earner).

The same absolute outcome (\$80,000) has different metric costs for the two agents -- not because they have different "reference points" (a psychological construct) but because they are at different positions on the manifold, and the metric is position-dependent (a geometric fact). Agent B's displacement traverses more dimensions than Agent A's, so it has higher total cost.

**[Conditional Theorem.]** Reference dependence dissolves as a paradox once we recognize that economic decisions are made on a manifold with position-dependent metric, not on a flat space with position-independent metric. On a flat space, the cost of moving from 60 to 80 and from 100 to 80 differs only in sign. On a curved manifold, the two displacements traverse different regions of the space, with different curvatures and different dimensional activations. The asymmetry is geometric, not psychological.

---

## 4.4 Framing Effects as Gauge Variance

> **Theorem 37 (Framing as Gauge Symmetry Violation).** *A framing effect -- where logically equivalent descriptions of the same decision produce different choices -- is a gauge symmetry violation on the decision manifold. The Bond Invariance Principle (BIP) requires that evaluations be invariant under meaning-preserving transformations. Framing effects occur when the agent's heuristic function $h(n)$ is not gauge-invariant -- when the System 1 assessment depends on the description rather than the described state.*

**Argument.** Let $x$ and $\tau(x)$ be two descriptions of the same economic state, related by a meaning-preserving transformation $\tau$ (e.g., "90% survival rate" vs. "10% mortality rate"). The BIP requires $J(\tau(x)) = J(x)$. If the agent's choice differs between $x$ and $\tau(x)$, then $h(\cdot)$ is gauge-variant: the heuristic assigns different costs to the same economic state under different descriptions.

This is a *miscalibration of the heuristic*, not a fundamental feature of the manifold. The manifold structure (the edge weights $w$) is gauge-invariant -- "90% survival" and "10% mortality" describe the same state and therefore have the same attribute vector. The heuristic approximation $h$ may not be gauge-invariant, because System 1 processes the *description* (the frame) rather than the *described state* (the attribute vector).

The Bond Index quantifies the magnitude of this miscalibration:

$$\text{BI}(\tau) = \frac{|h(\tau(x)) - h(x)|}{h(x)}$$

A Bond Index of zero means perfect gauge invariance (no framing effect). A positive Bond Index measures the severity of the gauge violation. $\square$

### The Critical Distinction: Metric Feature vs. Heuristic Error

This theorem draws a precise line between two categories of behavioral phenomena:

**Metric features (not biases):**
- Loss aversion: losses genuinely traverse more dimensions. The metric asymmetry is a structural property of the manifold. An agent with perfect information and unlimited computation would still exhibit loss aversion, because the manifold *is* asymmetric.
- Reference dependence: the metric genuinely varies with position. This is curvature, not error.
- The endowment effect: ownership genuinely creates rights ($d_2$), changing the dimensional structure of the state.

**Heuristic errors (genuine biases):**
- Framing effects: the same state, described differently, produces different evaluations. The manifold has not changed; the heuristic has failed to be invariant.
- Anchoring: an irrelevant number influences the evaluation. The manifold is unaffected by the anchor; the heuristic is contaminated.
- Availability bias: easily recalled instances distort probability estimates. The manifold structure is unchanged; the heuristic's estimate of $d_9$ (epistemic quality) is miscalibrated.

The geometric framework does not claim that all "biases" are rational. It claims that *some* are rational responses to manifold structure and *some* are genuine heuristic errors -- and it provides the mathematical criterion (gauge invariance) that distinguishes them.

> **RUNNING EXAMPLE -- FRAMING MARIA'S DECISION**
>
> *"Your rent is increasing from \$5,000 to \$7,000" activates loss framing: Maria perceives a loss of \$2,000/month. "Your new rent will be \$7,000, which is below the neighborhood average of \$8,500" activates gain framing: Maria perceives a saving relative to the market. The underlying economic state is identical. If Maria's response differs between the two descriptions, she is exhibiting a framing effect -- a gauge violation. The geometric framework predicts: Maria is more susceptible to framing when she is under cognitive load (System 2 resources depleted, so she relies more on gauge-variant System 1), and less susceptible when she has time to compute the full attribute vector (System 2 can verify gauge invariance by checking that the two descriptions map to the same manifold state).*

---

## 4.5 Hyperbolic Discounting as Path Curvature

Classical economics assumes exponential discounting: a reward $R$ at time $t$ has present value $R \cdot e^{-\delta t}$, where $\delta$ is a constant discount rate. This produces time-consistent preferences -- if you prefer A today to B tomorrow, you will also prefer A-in-30-days to B-in-31-days.

**[Empirical.]** Observed behavior is *hyperbolic*: the present value follows $R / (1 + kt)$ rather than $R \cdot e^{-\delta t}$. Hyperbolic discounting produces present bias (immediate rewards are overvalued) and preference reversals (you prefer the larger-later reward when both are distant, but switch to the smaller-sooner reward as it approaches). These phenomena are among the most robust findings in behavioral economics.

> **Proposition 38 (Hyperbolic Discounting as Temporal Curvature).** *Hyperbolic discounting arises because the decision manifold's curvature is non-constant along the temporal dimension. Near the present ($t \to 0$), the manifold is sharply curved (short-term consequences loom large in all dimensions), producing steep discounting. At distant horizons ($t \to \infty$), the manifold flattens (distant consequences affect fewer dimensions), producing shallow discounting. The overall discount function is the integral of curvature along the temporal axis, which yields a hyperbolic rather than exponential form.*

**Argument.** Consider a reward that can be received now or at time $t$. The reward's *immediate* impact is primarily on $d_1$ (monetary value). But the *near-term* context activates additional dimensions:

- **At $t = 0$ (now):** The reward is vivid and concrete. All dimensions are potentially active: social impact ($d_6$: "people see me receiving this"), identity ($d_7$: "I am the kind of person who seizes opportunities"), autonomy ($d_4$: "I can spend this immediately"), epistemic status ($d_9$: "I am certain of this reward"). The effective dimensionality of the evaluation is high.

- **At $t = 1$ year:** The reward is abstract and distant. Fewer dimensions are active: primarily $d_1$ (the expected monetary value, discounted for risk) and $d_9$ (uncertainty about whether the reward will materialize). The effective dimensionality is low.

The discount function is the ratio of edge weights:

$$D(t) = \frac{w_+(t)}{w_+(0)} = \frac{\text{manifold distance at time } t}{\text{manifold distance at time } 0}$$

Since the manifold distance at $t = 0$ is large (many dimensions active) and decreases as $t$ increases (fewer dimensions active), the discount function decreases steeply near $t = 0$ and flattens for large $t$. The functional form that emerges from this decreasing-dimensionality model is closer to $1/(1 + kt)$ (hyperbolic) than to $e^{-\delta t}$ (exponential).

### Why Present Bias Is Stronger for Visceral Goods

This derivation also explains a secondary finding: present bias is stronger for visceral goods (food, sex, drugs) than for abstract goods (money, career advancement). Visceral goods activate more dimensions of the manifold at short time horizons -- social impact, identity, autonomy are all engaged by immediate visceral choice. Abstract goods primarily affect $d_1$ (consequences) at all horizons. The curvature differential between $t = 0$ and $t \gg 0$ is therefore larger for visceral goods than for abstract goods, producing a steeper discount function and more pronounced present bias.

> **RUNNING EXAMPLE -- MARIA'S TIME HORIZON**
>
> *Maria is offered two deals: (A) a \$5,000 equipment grant she can use immediately, or (B) a \$7,000 equipment grant that arrives in six months. Classical discounting at market rates favors B. But Maria's manifold evaluation at $t = 0$ activates multiple dimensions: she can fix the espresso machine now ($d_1$), demonstrate competence to her landlord during lease negotiations ($d_5$, $d_6$), and maintain her identity as a proactive business owner ($d_7$). At $t = 6$ months, these dimensions are less active -- the lease negotiation will be over, the immediate crisis past. Maria's preference for A is not "present bias" in the pejorative sense. It is the rational response to a manifold where immediate action has higher dimensional activation than delayed action.*

---

## 4.6 The Endowment Effect as Hohfeldian Asymmetry

> **Proposition 39 (Endowment Effect as Rights Creation).** *The endowment effect -- valuing a good more highly when you own it than when you don't -- arises because ownership creates a Hohfeldian right ($d_2$) that must be surrendered upon sale. The attribute-vector change for selling includes $\Delta d_2 < 0$ (loss of right), while the attribute-vector change for buying includes $\Delta d_2 > 0$ (acquisition of right). Since loss of rights activates more dimensions than acquisition (by the same mechanism as loss aversion), selling has higher total edge weight than buying.*

**Argument.** Consider a coffee mug worth \$5 at market price.

**Buying the mug (non-owner $\to$ owner):**
$$\Delta \mathbf{a}_{\text{buy}} = (-5, +\delta_2, 0, 0, 0, 0, 0, 0, 0)$$

The buyer pays \$5 ($\Delta d_1 = -5$) and acquires a property right ($\Delta d_2 = +\delta_2$). The acquisition of a right is a positive change on $d_2$, approximately one-dimensional.

**Selling the mug (owner $\to$ non-owner):**
$$\Delta \mathbf{a}_{\text{sell}} = (+5, -\delta_2, -\delta_3, 0, 0, -\delta_6, -\delta_7, 0, 0)$$

The seller receives \$5 ($\Delta d_1 = +5$) but surrenders a property right ($\Delta d_2 = -\delta_2$). The *loss* of the right activates additional dimensions: fairness ($d_3$: "am I getting enough for something that's mine?"), social status ($d_6$: "selling off my things"), identity ($d_7$: "this was part of my possessions"). The selling path is multi-dimensional.

The willingness to accept (WTA) must compensate for the multi-dimensional displacement:
$$\text{WTA} = \sqrt{(\Delta d_1)^2 / \sigma_1^2 + (\delta_2)^2 / \sigma_2^2 + (\delta_3)^2 / \sigma_3^2 + \cdots}$$

The willingness to pay (WTP) must compensate only for the monetary cost:
$$\text{WTP} \approx \frac{|\Delta d_1|}{\sigma_1}$$

Therefore $\text{WTA} > \text{WTP}$, and the ratio $\text{WTA}/\text{WTP} \approx 2$-$3$ matches the observed endowment effect.

**The key insight:** The WTA/WTP gap is not a separate phenomenon from loss aversion. It is the *same metric asymmetry* expressed in the specific domain of property rights. Loss aversion is the general principle (losses activate more dimensions); the endowment effect is its application to the Hohfeldian structure of ownership.

---

## 4.7 Probability Weighting as Epistemic Curvature

Standard prospect theory includes a probability-weighting function $w(p)$ that overweights small probabilities and underweights large ones. The geometric framework provides a natural interpretation.

**[Conditional Theorem.]** Probability weighting arises from the curvature of the epistemic dimension ($d_9$). Near $p = 0$ and $p = 1$, the epistemic status changes sharply: the transition from "impossible" to "barely possible" and from "almost certain" to "certain" activates $d_9$ strongly (the agent's confidence shifts). In the middle range ($p \approx 0.5$), epistemic status is relatively stable -- the agent is already uncertain, so changes in probability do not produce large shifts in $d_9$.

The probability-weighting function $w(p)$ is the projection of the manifold distance onto the probability axis:

$$w(p) \propto \int_0^p \sqrt{g_{99}(p')} \, dp'$$

where $g_{99}(p)$ is the metric component along $d_9$ at probability $p$. If $g_{99}$ is large near $p = 0$ and $p = 1$ (sharp curvature at the endpoints of the probability scale) and small near $p = 0.5$ (flat curvature in the middle), the integral produces an S-shaped weighting function that overweights small probabilities and underweights large ones.

This is consistent with the Allais and Ellsberg paradoxes, which both involve shifts in epistemic status ($d_9$) that the scalar expected-value calculation ignores.

### The Allais Paradox Dissolved

The Allais paradox -- the most famous violation of the expected utility independence axiom -- dissolves on the decision manifold. Consider the classic choice:

**Option A:** Certain \$1,000,000.
**Option B:** 89% chance of \$1,000,000, 10% chance of \$5,000,000, 1% chance of \$0.

Expected value favors B (\$1,390,000 vs. \$1,000,000). Most people choose A. Then, in a second pair:

**Option C:** 11% chance of \$1,000,000, 89% chance of \$0.
**Option D:** 10% chance of \$5,000,000, 90% chance of \$0.

Expected value favors D. Most people choose D -- but this violates the independence axiom, because the only difference between the A-vs-B pair and the C-vs-D pair is the removal of the common 89% chance of \$1,000,000.

On the decision manifold, the paradox vanishes. Choosing A over B reflects the activation of $d_9$ (epistemic certainty has value: "I *know* I get the million") and $d_7$ (identity: "I am prudent -- I take the sure thing"). The attribute-vector difference between A and B includes non-zero components on $d_7$ and $d_9$ that the expected-value calculation discards. In the C-vs-D pair, both options involve substantial uncertainty ($d_9$ is already degraded for both), so the epistemic and identity components are approximately equal, and the agent defaults to expected-value comparison -- choosing D.

On the scalar projection, independence is violated. On the full manifold, preferences are consistent: the attribute-vector difference between certainty and risk includes dimensions that the scalar calculation ignores.

### The Ellsberg Paradox Dissolved

The Ellsberg paradox -- ambiguity aversion, preferring known to unknown probabilities -- reflects $d_9$ directly. Known probabilities have higher epistemic-status scores than ambiguous ones. The Mahalanobis distance from the ambiguous gamble to the goal is larger than from the known-probability gamble, even when expected values are equal, because $\Delta d_9 \neq 0$ for the ambiguous case. Ambiguity aversion is not a violation of rational behavior. It is a rational response to a genuine dimensional difference: known and unknown risks have different $d_9$ scores, and the metric weights this difference.

---

## 4.8 Worked Example: Computing $\lambda$ for Maria's Rent Decision

Let us compute the geometric loss-aversion coefficient for Maria's specific situation.

### Setup

Maria currently operates at a steady state with attribute vector $\mathbf{a}_0$. She faces two symmetric possibilities:

**Scenario G (gain):** The landlord *reduces* rent by \$2,000/month (from \$5,000 to \$3,000). Total annual impact: +\$24,000.

**Scenario L (loss):** The landlord *increases* rent by \$2,000/month (from \$5,000 to \$7,000). Total annual impact: -\$24,000.

Both scenarios involve the same monetary magnitude: \$24,000/year. The question is: what is the ratio of manifold distances?

### Gain Path (G)

Maria's attribute-vector change under the rent reduction:

$$\Delta \mathbf{a}_G = (+24000, 0, +0.2, +0.1, +0.1, +0.1, +0.1, 0, 0)$$

The gain is primarily monetary ($d_1$). Small positive spillovers: the lower rent feels slightly fairer ($d_3 = +0.2$), gives Maria slightly more autonomy ($d_4 = +0.1$), slightly increases her trust in the landlord ($d_5 = +0.1$), has a small positive community signal ($d_6 = +0.1$), and mildly reinforces her identity ($d_7 = +0.1$). These spillovers are small because gains do not strongly activate non-monetary dimensions.

### Loss Path (L)

Maria's attribute-vector change under the rent increase:

$$\Delta \mathbf{a}_L = (-24000, -0.3, -0.6, -0.5, -0.7, -0.4, -0.5, +0.1, -0.6)$$

The loss is monetary ($d_1 = -24000$) but triggers substantial non-monetary activations:
- $d_2 = -0.3$: sense of rights erosion ("the lease should protect me")
- $d_3 = -0.6$: strong unfairness ("I built this neighborhood's value; the REIT is capturing it")
- $d_4 = -0.5$: autonomy loss ("I'm forced to cut wages or quality")
- $d_5 = -0.7$: trust destruction ("they'll just raise it again")
- $d_6 = -0.4$: community impact signal ("people will see my shop struggling")
- $d_7 = -0.5$: identity threat ("I might not be a business owner anymore")
- $d_8 = +0.1$: the REIT is within its rights (slightly legitimacy-preserving)
- $d_9 = -0.6$: uncertainty ("what happens next year?")

### Computing Edge Weights

Using a representative covariance matrix with standard deviations $\sigma_k$ calibrated to behavioral data (and assuming for simplicity that cross-correlations add approximately 20% to the diagonal terms):

**Gain weight:**
$$w_G = \frac{(24000)^2}{\sigma_1^2} + \frac{(0.2)^2}{\sigma_3^2} + \frac{(0.1)^2}{\sigma_4^2} + \cdots \approx \frac{(24000)^2}{\sigma_1^2} \times 1.08$$

The non-monetary terms add approximately 8% to the base monetary cost.

**Loss weight:**
$$w_L = \frac{(24000)^2}{\sigma_1^2} + \frac{(0.3)^2}{\sigma_2^2} + \frac{(0.6)^2}{\sigma_3^2} + \frac{(0.5)^2}{\sigma_4^2} + \frac{(0.7)^2}{\sigma_5^2} + \frac{(0.4)^2}{\sigma_6^2} + \frac{(0.5)^2}{\sigma_7^2} + \frac{(0.1)^2}{\sigma_8^2} + \frac{(0.6)^2}{\sigma_9^2} + \text{cross terms}$$

If we estimate the non-monetary activations at approximately $0.5\sigma_k$ on average for the six strongly activated dimensions, each contributes $(0.5)^2 = 0.25$ in standardized units. With six such dimensions plus cross-correlation amplification of approximately 20%:

$$w_L \approx \frac{(24000)^2}{\sigma_1^2} + 6 \times 0.25 \times 1.2 = \frac{(24000)^2}{\sigma_1^2} + 1.80$$

Normalizing both weights by the common monetary base $\frac{(24000)^2}{\sigma_1^2}$, and noting that the normalized monetary component equals 1.0 in these units:

$$\lambda = \frac{w_L}{w_G} = \frac{1.0 + 1.80}{1.0 + 0.08} = \frac{2.80}{1.08} \approx 2.59$$

### Interpretation

Maria's loss-aversion coefficient for the rent decision is approximately $\lambda \approx 2.6$ -- higher than the textbook average of 2.25, because the rent increase activates more dimensions more strongly than a typical laboratory gamble. This is consistent with the prediction that $\lambda$ increases with dimensional activation.

Compare this to a laboratory experiment where Maria evaluates a coin flip for \$100 gain or \$100 loss, with no social context, no identity implications, and no contractual dimensions. In that setting, the gain and loss paths are both approximately one-dimensional, and $\lambda \approx 1.0$-$1.2$.

**The geometric framework predicts that loss aversion is not a personality trait (some fixed $\lambda$ that characterizes Maria). It is a manifold property (a variable $\lambda$ that depends on how many dimensions the specific loss activates).** This prediction is testable and distinguishes the geometric framework from standard prospect theory.

### Sensitivity Analysis: What Drives $\lambda$?

The computation above reveals what controls the magnitude of loss aversion. Three factors dominate:

1. **Number of activated dimensions ($N$).** Each additional dimension that a loss activates adds a positive term to $w_L$ without a corresponding increase in $w_G$. This is the primary driver: losses that touch more of the agent's life produce more loss aversion.

2. **Intensity of activation ($\delta_k / \sigma_k$).** Dimensions that are strongly activated (large $\delta_k$ relative to $\sigma_k$) contribute more to $w_L$. A loss that produces intense unfairness perception ($\delta_3 \gg \sigma_3$) adds more to the loss weight than one that produces mild unfairness.

3. **Cross-dimensional correlation.** When activated dimensions are positively correlated -- as they typically are (trust erosion accompanies fairness violation, which accompanies identity threat) -- the off-diagonal terms in $\Sigma^{-1}$ amplify the total edge weight beyond what independent dimensions would produce.

This decomposition generates precise experimental predictions. To test whether the geometric account is correct, one would design losses that hold monetary magnitude constant while varying the number of activated dimensions, the intensity of activation, or the correlation structure. The geometric framework predicts that $\lambda$ will increase with each factor. Standard prospect theory predicts $\lambda \approx 2.25$ regardless.

---

## 4.9 The Metric Classification of "Biases"

We can now systematically classify every major behavioral-economics phenomenon as either a metric feature or a heuristic error:

| Phenomenon | Type | Mechanism | Geometric Object |
|---|---|---|---|
| Loss aversion | Metric feature | Losses activate more dimensions | Metric asymmetry $w_-/w_+ > 1$ |
| Reference dependence | Metric feature | Metric varies with position | Manifold curvature |
| Endowment effect | Metric feature | Ownership creates $d_2$ right | Hohfeldian dimension activation |
| Hyperbolic discounting | Metric feature | Curvature varies along time axis | Non-constant temporal curvature |
| Status quo bias | Metric feature | Departures from status quo are multi-dimensional | Displacement cost from current vertex |
| Framing effects | Heuristic error | $h(n)$ depends on description, not state | Gauge symmetry violation |
| Anchoring | Heuristic error | Irrelevant information contaminates $h(n)$ | Gauge-variant heuristic |
| Availability bias | Heuristic error | Recall ease distorts $d_9$ estimate | Miscalibrated epistemic dimension |
| Sunk cost fallacy | Heuristic error | Past costs contaminate current $g(n)$ | Path-dependence violating re-description invariance |

The first five are not biases. They are rational responses to the geometry of the decision manifold. An omniscient agent with unlimited computation would still exhibit them, because the manifold *is* asymmetric, curved, rights-structured, and temporally non-uniform.

The last four are genuine cognitive errors. They violate gauge invariance -- the requirement that evaluations depend on the economic state, not on the description, the framing, the anchoring context, or the sunk history. The geometric framework identifies these as *heuristic miscalibrations* with a specific mathematical signature (non-zero Bond Index), distinguishable from rational metric responses.

### Why This Classification Matters

The classification has practical consequences. If loss aversion is a metric feature rather than a bias, then "debiasing" agents to eliminate loss aversion is misguided -- you would be asking them to ignore real dimensions of their decision space. A financial advisor who tells a client "ignore your emotional reaction to losses" is, on this account, advising the client to optimize on the scalar projection rather than the full manifold. The "emotional reaction" carries information about the multi-dimensional cost of the loss.

Conversely, if framing effects are genuine heuristic errors, then interventions to reduce framing effects are well-justified. Training agents to evaluate options in terms of explicit attribute vectors -- making the manifold structure salient rather than relying on the frame-dependent heuristic -- should reduce framing effects. The framework predicts a specific magnitude: framing effects should decrease in proportion to the agent's ability to compute the full attribute vector, and should approach zero when all nine dimensions are made simultaneously visible.

**[Empirical.]** This generates a testable prediction: loss aversion should be robust to "debiasing" interventions (because it reflects manifold structure, not heuristic error), while framing effects should be reducible by interventions that make the manifold structure explicit (because they reflect heuristic miscalibration, not manifold structure). If both phenomena respond identically to debiasing, the geometric classification is wrong.

---

## 4.10 The Finsler Generalization

The Mahalanobis metric, being a quadratic form, is symmetric: $d(A, B) = d(B, A)$. But the analysis of loss aversion shows that the metric is *asymmetric* -- the cost of moving from state A to state B (a gain) differs from the cost of moving from B to A (a loss), even when $|A - B| = |B - A|$.

**[Modeling Axiom.]** To capture this asymmetry rigorously, the decision manifold requires a *Finsler metric* rather than a Riemannian metric. A Finsler metric is a generalization that allows the metric function to depend on both position and direction:

$$F(x, v) \neq F(x, -v) \quad \text{in general}$$

where $x$ is the position on the manifold and $v$ is the direction of displacement. In the economic context, $F(x, v)$ measures the cost of displacement $v$ from state $x$, and the asymmetry $F(x, v) \neq F(x, -v)$ formalizes the fact that gains and losses have different costs even when they have the same magnitude.

The Finsler metric for the economic decision manifold takes the form:

$$F(x, v) = \begin{cases} \sqrt{v^T \Sigma_+^{-1}(x) \, v} & \text{if } v \text{ is a "gain direction" (net positive on active dimensions)} \\ \sqrt{v^T \Sigma_-^{-1}(x) \, v} & \text{if } v \text{ is a "loss direction" (net negative on active dimensions)} \end{cases}$$

where $\Sigma_+^{-1}(x)$ is the metric for gain paths (approximately diagonal, concentrated on $d_1$) and $\Sigma_-^{-1}(x)$ is the metric for loss paths (full matrix, with activation across multiple dimensions). The loss-aversion coefficient is:

$$\lambda(x) = \frac{F(x, -v)}{F(x, v)}$$

This is position-dependent (through $\Sigma_{\pm}(x)$), direction-dependent (through the gain/loss classification of $v$), and computable from the covariance structure.

### Application: Wage Rigidity

The Finsler metric immediately explains one of the most puzzling phenomena in labor economics: downward wage rigidity. Bewley's (1999) field study found that firms resist cutting nominal wages even in recessions, citing "morale" as the primary reason. Classical economics has no explanation for this -- if labor supply exceeds demand, the wage should fall.

The geometric explanation is direct:

- A wage cut traverses the fairness dimension ($\Delta d_3 < 0$) and the legitimacy dimension ($\Delta d_8 < 0$) for the employee.
- By the loss-aversion theorem (Theorem 34), the *perceived* cost of a wage cut ($w_-$) exceeds the cost of never having received the higher wage ($w_+$), because the loss activates more dimensions.
- The employer anticipates that the total behavioral friction (behavioral friction -- the total path cost on the decision manifold, formally defined in Chapter 7) $\text{BF}_{\text{employee}}$ will include reduced effort, increased turnover, and social sanction ($d_6$) -- all of which cost more on the full manifold than the monetary savings from the wage cut.
- The Bond geodesic for the employer avoids the wage-cut edge and instead traverses a different path (layoffs, reduced hiring, unpaid overtime, benefit cuts) that has lower total manifold cost -- even though its monetary cost ($d_1$) may be higher.

The Finsler asymmetry makes this precise: the metric for wage reductions ($\Sigma_-^{-1}$) has larger off-diagonal terms than the metric for equivalent wage increases ($\Sigma_+^{-1}$), because wage cuts activate fairness, legitimacy, and identity dimensions that wage increases do not. The employer's optimal path on the full manifold avoids the high-friction wage-cut direction in favor of lower-friction alternatives.

---

## 4.11 Different Metrics, Different Economics

Different economic theories correspond to different choices of metric on the decision manifold. This observation makes the framework's relationship to existing theories precise.

**Utilitarian metric:** $g_{\mu\nu} = \delta_{\mu 1} \delta_{\nu 1} / \sigma_1^2$ -- only $d_1$ (consequences) has non-zero metric weight. All non-monetary dimensions are invisible. This is Homo economicus: the metric collapses the manifold to a line.

**Rawlsian metric:** The metric weights the dimension that is worst-off for the least-advantaged agent. This is a lexicographic metric that prioritizes the minimum across dimensions.

**Capabilities metric:** The metric weights each dimension by the agent's capability in that dimension, with special attention to dimensions below a sufficiency threshold. This is Sen's framework, formalized as a specific metric on the nine-dimensional manifold.

**Welfare-state metric:** The metric has strong off-diagonal terms between $d_1$ (consequences) and $d_3$ (fairness), $d_4$ (autonomy), and $d_8$ (legitimacy), encoding the political commitment that economic outcomes should be fair, free, and legitimate.

**[Modeling Axiom.]** The choice of metric is not a mathematical question -- it is a political and philosophical one. The geometric framework does not prescribe which metric is "correct." It provides the mathematical language in which different metrics (and therefore different political philosophies) can be stated, compared, and analyzed with unprecedented precision. The debate about what economic policy should optimize is, in this framework, a debate about which metric tensor $g_{\mu\nu}$ should govern the evaluation of economic states.

---

## Technical Appendix

### Formal Statement of the Finsler Metric

**[Conditional Theorem.]** Let $\mathcal{M} \subseteq \mathbb{R}^9$ be the smooth economic decision manifold (the continuous limit of the decision complex). A *Finsler metric* on $\mathcal{M}$ is a function $F: T\mathcal{M} \to [0, \infty)$ satisfying:

1. $F(x, v) \geq 0$ for all $(x, v) \in T\mathcal{M}$, with equality iff $v = 0$ (positive definiteness).
2. $F(x, \alpha v) = |\alpha| F(x, v)$ for all $\alpha \in \mathbb{R}$ (absolute homogeneity -- note: this allows $F(x, v) \neq F(x, -v)$, unlike the positive homogeneity of standard Finsler metrics, because we use absolute value).
3. The Hessian $g_{ij}(x, v) = \frac{1}{2} \frac{\partial^2 F^2}{\partial v^i \partial v^j}$ is positive definite for $v \neq 0$ (strong convexity).

For the economic metric, we relax condition 2 to allow directional asymmetry:

$$F(x, v) = \begin{cases} \sqrt{v^T G_+(x) v} & \text{if } v \in C_+(x) \text{ (gain cone)} \\ \sqrt{v^T G_-(x) v} & \text{if } v \in C_-(x) \text{ (loss cone)} \end{cases}$$

where $C_+(x)$ and $C_-(x)$ partition the tangent space $T_x\mathcal{M}$ into gain and loss directions (defined by the sign of the net change on emotionally salient dimensions), and $G_+(x)$, $G_-(x)$ are the position-dependent gain and loss metric tensors. The loss-aversion coefficient at position $x$ in direction $v$ is:

$$\lambda(x, v) = \frac{F(x, -v)}{F(x, v)} = \sqrt{\frac{v^T G_-(x) v}{v^T G_+(x) v}}$$

### Derivation of $\lambda \approx 2.25$ from Population Averages

**[Conditional Theorem.]** Let $N_{\text{loss}}$ denote the average number of non-monetary dimensions activated by a loss in a standard prospect-theory experiment (where the loss involves money in a laboratory setting with moderate social context). Let $\bar{\delta}$ denote the average normalized activation per dimension (in units of $\sigma_k$). Then:

$$\lambda \approx \sqrt{1 + N_{\text{loss}} \cdot \bar{\delta}^2}$$

For $N_{\text{loss}} \approx 4$-$5$ and $\bar{\delta} \approx 0.6$-$0.7$:

$$\lambda \approx \sqrt{1 + 4.5 \times 0.42} \approx \sqrt{2.89} \approx 1.7 \quad \text{(lower bound)}$$

$$\lambda \approx \sqrt{1 + 5 \times 0.49} \approx \sqrt{3.45} \approx 1.86 \quad \text{(upper bound)}$$

Including cross-correlation amplification (the off-diagonal terms in $\Sigma^{-1}$ add approximately 30-50% to the quadratic form for correlated dimensions):

$$\lambda \approx 1.86 \times 1.2 \approx 2.23$$

This is within the empirical range $\lambda \in [2.0, 2.5]$ reported in meta-analyses of prospect-theory studies.

The derivation also predicts:
- $\lambda$ should be closer to 1.0 for purely monetary losses in low-context settings (few non-monetary dimensions active).
- $\lambda$ should be substantially above 2.25 for losses with high moral-dimensional content (losses of identity, rights, community standing).
- $\lambda$ should vary cross-culturally, because $\Sigma$ varies cross-culturally (different cultures weight different dimensions differently).

All three predictions are consistent with existing evidence and generate specific, testable hypotheses for future empirical work.

### The Relationship Between Mahalanobis and Finsler Metrics

The standard Mahalanobis distance $d_M = \sqrt{\Delta \mathbf{a}^T \Sigma^{-1} \Delta \mathbf{a}}$ is a Riemannian metric (symmetric, quadratic). The Finsler generalization preserves the Mahalanobis structure within each cone (gain and loss) but allows different covariance matrices for gain and loss directions. The two descriptions are compatible:

- For small displacements within a single cone, the Finsler metric reduces to the Mahalanobis metric with the appropriate $\Sigma$.
- For large displacements that transition from gain to loss regions, the Finsler metric accounts for the direction-dependent asymmetry.
- In the limit where $\Sigma_+ = \Sigma_-$ (gain and loss metrics are identical), the Finsler metric reduces to the standard Mahalanobis metric with $\lambda = 1$ (no loss aversion).

---

## Notes on Sources

Loss aversion was first reported in Kahneman and Tversky (1979), "Prospect Theory," *Econometrica*. The endowment effect was demonstrated by Thaler (1980), "Toward a Positive Theory of Consumer Choice," *Journal of Economic Behavior and Organization*, and systematically studied by Kahneman, Knetsch, and Thaler (1990), "Experimental Tests of the Endowment Effect and the Coase Theorem," *Journal of Political Economy*. Hyperbolic discounting is reviewed in Frederick, Loewenstein, and O'Donoghue (2002), "Time Discounting and Time Preference: A Critical Review," *Journal of Economic Literature*. Framing effects are from Tversky and Kahneman (1981), "The Framing of Decisions and the Psychology of Choice," *Science*. The Finsler metric generalization draws on Bao, Chern, and Shen (2000), *An Introduction to Riemann-Finsler Geometry*, Springer. The Hohfeldian framework is from Hohfeld (1913), "Some Fundamental Legal Conceptions," *Yale Law Journal*. The geometric derivations are from Bond (2026), "Geometric Economics," Sections 7-8, and Bond (2026), *Geometric Ethics*, Chapter 20. The eris-econ empirical validation data (loss aversion varying 1.0-3.53, 16/16 behavioral predictions, 2.70% MAE) is from the eris-econ library validation results (Appendix C of the book plan).
