# Chapter 13: Trade as Geodesic Exchange

> *"If a foreign country can supply us with a commodity cheaper than we ourselves can make it, better buy it of them with some part of the produce of our own industry."*
> — Adam Smith, *The Wealth of Nations* (1776)

*Part V: Applications*

---

> **RUNNING EXAMPLE — MARIA'S COFFEE SHOP**
>
> *Maria Esperanza sources her coffee beans from a small cooperative in Huila, Colombia. The cheapest option would be commodity beans from a large Brazilian plantation at $12/lb — the $d_1$-optimal geodesic. But Maria pays $25/lb for single-origin Colombian beans through her Oakland roaster Elena, who has a direct relationship with the cooperative. On the full manifold, the Colombian path traverses lower-cost regions: fair wages ($d_3$), transparent supply chain ($d_5$, $d_9$), community development in Huila ($d_6$), and alignment with Maria's identity ($d_7$). The $d_1$ premium of $13/lb buys a geodesic that is shorter on the full manifold than the "cheaper" commodity path.*
>
> *International trade is not about finding the cheapest goods. It is about finding the shortest path on the multi-national decision manifold — and the cheapest path on $d_1$ is rarely the shortest on all nine dimensions.*

---

## 13.1 Comparative Advantage as Curvature

**[Modeling Axiom.]** David Ricardo's principle of comparative advantage states that even when one country is more efficient at producing *everything*, both countries benefit from trade if they specialize in goods where their relative efficiency advantage is greatest. The standard proof uses opportunity cost — the scalar version.

The geometric reinterpretation: comparative advantage is a statement about *curvature*. Country A has low curvature along the textile-production axis of the decision manifold — moving from "no textiles" to "many textiles" costs little in terms of displaced resources and social disruption. Country B has low curvature along the semiconductor axis. Each country's geodesic — the optimal production path — follows the low-curvature direction.

When both countries produce everything domestically, each is forced to traverse high-curvature regions of their manifold (A producing semiconductors, B producing textiles). Trade allows each to follow their low-curvature geodesic and exchange the results. The gains from trade are the reduction in total geodesic length: the sum of the two specialized geodesics is shorter than the sum of the two autarky geodesics.

This reinterpretation reveals something hidden in the classical formulation: the curvature that determines comparative advantage is not fixed. It can be changed by investment in infrastructure, education, institutions, and technology. A country that invests in semiconductor R&D is *flattening* its manifold along the semiconductor axis — reducing the curvature, making production cheaper, and shifting its comparative advantage. Industrial policy, in the geometric framework, is *deliberate curvature reduction* on specific production axes.

The East Asian development model — Japan, then South Korea, then Taiwan, then China — can be read as a sequence of deliberate curvature reductions: each country invested heavily in specific production capabilities (textiles, then electronics, then semiconductors, then advanced manufacturing), reducing curvature on those axes until their comparative advantage shifted. The policy succeeded not because it "picked winners" in the traditional sense but because the investment reduced curvature — made production cheaper and less disruptive — on strategically chosen axes.

**On the full manifold**, comparative advantage has dimensions beyond $d_1$. A country may have low curvature on $d_1$ for electronics production (cheap labor) but high curvature on $d_4$ (coercive labor practices) and $d_3$ (unfair wage distribution). The $d_1$-only geodesic says "produce electronics." The full-manifold geodesic may say "produce electronics *with fair labor standards*" — a longer $d_1$ path but a shorter total path.

### Formalizing Comparative Advantage as Curvature

**[Conditional Theorem.]** The classical Ricardian model can be re-derived as a curvature statement.

**Theorem 13.1 (Ricardian Comparative Advantage as Curvature).** *Let country A's production manifold have sectional curvature $K_A(d_1, d_{\text{textile}})$ in the textile-production plane and $K_A(d_1, d_{\text{semi}})$ in the semiconductor plane. Let country B's production manifold have corresponding curvatures $K_B$. Country A has comparative advantage in textiles if and only if:*

$$\frac{K_A(d_1, d_{\text{textile}})}{K_A(d_1, d_{\text{semi}})} < \frac{K_B(d_1, d_{\text{textile}})}{K_B(d_1, d_{\text{semi}})}$$

*That is, the ratio of curvatures is lower for A in textiles than for B. This is equivalent to the standard condition that A's opportunity cost of textiles (in terms of semiconductors) is lower than B's.*

*Proof sketch.* The geodesic length from "no production" to "$n$ units produced" is proportional to $\int_0^n \sqrt{K(d_1, d_j)} \, dq$, where $q$ is the quantity produced. The opportunity cost of producing one more unit of textiles (in terms of semiconductors foregone) is the ratio of geodesic costs: $K_A(d_1, d_{\text{textile}}) / K_A(d_1, d_{\text{semi}})$. The standard Ricardian condition says A should produce the good where its opportunity cost ratio is lowest. The curvature formulation is a geometric restatement of the same condition. $\square$

The curvature formulation reveals something the classical formulation hides: comparative advantage can exist *on different dimensions*. A country may have comparative advantage on $d_1$ in one product and comparative advantage on $d_3$ (fairness) in another. The full-manifold gains from trade depend on the metric $\Sigma$ — on how much each trading partner weights each dimension. A country with strong labor protections ($d_3$, $d_4$) may have comparative advantage in producing goods whose consumers weight those dimensions heavily, even if its $d_1$ production costs are higher.

This is the geometric explanation for why "Made in Germany" and "Swiss-made" command premiums far exceeding any plausible quality difference. These labels signal low curvature on $d_3$ (fair labor), $d_8$ (regulatory compliance), and $d_9$ (quality assurance) — dimensions that consumers weight when the full manifold is active. The premium is not irrational. It is the market price of the evaluative-dimension surplus embedded in the product's geodesic.

### The Heckscher-Ohlin Model, Geometrized

The Heckscher-Ohlin theorem — that countries export goods intensive in their abundant factor — is a curvature statement about factor endowments. A country abundant in labor has low curvature in the labor-intensive production plane: adding more labor to production is a small perturbation, traversing a nearly flat region of the manifold. A country scarce in labor has high curvature: adding labor requires crossing steep regions (immigration barriers on $d_8$, wage competition on $d_3$, social tensions on $d_6$).

The geometric reformulation adds depth: factor abundance is not just about physical endowment ($d_1$) but about institutional capacity. A country may be "abundant" in labor on $d_1$ (many workers) but "scarce" on $d_4$ (labor autonomy — workers lack bargaining power) and $d_3$ (fairness — wages do not reflect productivity). The full-manifold comparative advantage depends on all dimensions of the factor endowment, not just the physical quantity.

## 13.2 Trade Restrictions as Artificial Boundaries

Tariffs, quotas, and trade barriers are artificial boundaries on the multi-national decision manifold. They force the geodesic to detour around forbidden regions — raising the total path cost.

**[Conditional Theorem.]** The welfare cost of a trade restriction is the difference between the unrestricted geodesic and the restricted geodesic:

$$\text{Cost}_{\text{restriction}} = \text{BF}(\gamma_{\text{restricted}}) - \text{BF}(\gamma_{\text{unrestricted}})$$

On $d_1$ alone, this is the standard deadweight loss triangle from trade theory. On the full manifold, the cost may be larger or smaller depending on which dimensions the restriction protects.

A tariff that protects domestic workers ($d_3$, $d_4$) from competition with coerced foreign labor may *reduce* total manifold cost even though it *increases* $d_1$ cost. The standard trade argument — that all restrictions reduce welfare — holds only on the scalar projection. On the full manifold, some boundaries are welfare-improving because they prevent the geodesic from traversing morally prohibited regions ($\beta_k = \infty$).

### The Infant Industry Argument, Geometrized

The infant industry argument — that a new domestic industry may need temporary protection to develop competitive capability — is a curvature-smoothing argument. A new industry starts with high curvature on $d_1$ (high initial costs), $d_9$ (high epistemic uncertainty about production methods), and $d_5$ (no established trust relationships with customers). Exposure to unrestricted international competition at this stage means competing against established foreign producers who have already flattened their curvature through experience.

Temporary protection (a tariff, a subsidy) provides a boundary that shields the infant industry from the low-curvature foreign geodesic while it reduces its own curvature through learning-by-doing. The protection should be removed when the domestic curvature has fallen to competitive levels — that is, when the domestic geodesic is approximately as short as the foreign one.

The geometric framework adds a criterion for when protection is justified that the classical framework lacks: the protection is welfare-improving on the full manifold only when the domestic industry will eventually develop not just $d_1$ competitiveness (low monetary cost) but also evaluative competitiveness — local employment ($d_6$), domestic knowledge development ($d_9$), institutional capacity ($d_8$). Protection that develops only $d_1$ competitiveness at the cost of evaluative dimensions (e.g., protecting an industry that relies on exploitative labor practices) may pass the scalar test and fail the manifold test.

### Trade and the Conservation Laws

The conservation laws of Chapter 9 constrain the structure of international trade. In a bilateral trade between countries A and B:

- **Transferable dimensions are conserved**: Country A's monetary surplus ($d_1$) is country B's deficit. The trade balance is the accounting identity. Country A's intellectual property rights ($d_2$) transferred in a licensing deal are rights that A surrenders.

- **Evaluative dimensions are not conserved**: Trade between countries can simultaneously build trust ($d_5$ for both), strengthen institutions ($d_8$ for both), and reveal information ($d_9$ for both). This is the evaluative surplus of trade — the value created by the relationship itself, beyond the exchange of goods.

The framework explains why trade relationships are more durable and more valuable than arms-length transactions: the evaluative surplus from repeated trade accumulates over time. The EU's economic integration created massive evaluative surplus — institutional trust, regulatory harmonization, cultural exchange — that would not appear in any $d_1$-only accounting. Britain's exit from the EU destroyed evaluative value on $d_5$ (trust between UK and EU institutions), $d_8$ (shared regulatory legitimacy), and $d_6$ (cross-border community connections) — losses that are invisible to GDP but real on the full manifold.

## 13.3 Fair Trade as Full-Manifold Optimization

**[Empirical.]** The fair-trade movement is, in geometric terms, an explicit shift from $d_1$-optimal to full-manifold-optimal trade. Fair-trade certification ensures that the supply chain geodesic respects minimum values on $d_3$ (fair wages), $d_4$ (worker autonomy), $d_6$ (community development), and $d_8$ (regulatory compliance).

The willingness-to-pay premium for fair-trade goods ($1.40–$3.50 per pound for coffee, depending on study) is the market's estimate of the evaluative-dimension surplus created by the full-manifold geodesic. The framework predicts that the premium varies with the buyer's covariance matrix $\Sigma$ — buyers who weight evaluative dimensions heavily pay higher premiums, as the empirical data confirms.

### The Fair-Trade Premium as Manifold Distance

The fair-trade premium has a precise geometric interpretation. Let $\gamma_{\text{commodity}}$ be the $d_1$-optimal supply chain path and $\gamma_{\text{fair}}$ be the fair-trade path. The premium $\pi$ is:

$$\pi = \text{BF}_{d_1}(\gamma_{\text{fair}}) - \text{BF}_{d_1}(\gamma_{\text{commodity}})$$

This is the additional $d_1$ cost of the fair-trade geodesic. The fair-trade geodesic is chosen when:

$$\text{BF}_{\text{full}}(\gamma_{\text{fair}}) < \text{BF}_{\text{full}}(\gamma_{\text{commodity}})$$

That is, when the total cost on the full manifold is lower for the fair-trade path despite its higher $d_1$ cost. The difference $\text{BF}_{\text{full}}(\gamma_{\text{commodity}}) - \text{BF}_{\text{full}}(\gamma_{\text{fair}})$ is the evaluative surplus of fair trade — the value created on $d_3$, $d_5$, $d_6$, and $d_7$ by choosing the longer $d_1$ path.

The framework predicts that the fair-trade premium should be highest for goods where the evaluative dimensions are most active. Coffee (visible labor conditions, personal relationship with roaster, identity-expressive purchase) should command a higher premium than, say, copper wire (anonymous commodity, no identity component, no visible labor dimension). The empirical evidence confirms this prediction: fair-trade premiums are highest for consumer-facing goods with identity and trust dimensions active.

## 13.4 Global Value Chains as Manifold Paths

Modern global value chains are not simple bilateral trades but multi-step paths through the international decision manifold. A smartphone traverses: mining in Congo ($d_3$, $d_4$ risks), refining in China ($d_6$ environmental costs), assembly in Vietnam ($d_1$ labor cost), design in California ($d_7$ innovation identity), sale in Europe ($d_8$ regulatory compliance).

Each step is an edge on the decision complex. The total behavioral friction of the path is the sum of edge weights across all dimensions and all steps. The $d_1$-optimal path minimizes monetary cost; the full-manifold geodesic minimizes total behavioral friction.

**[Empirical.]** The growing corporate emphasis on "supply chain transparency" and "ESG compliance" is a market recognition that $d_1$-optimal supply chains are not geodesics on the full manifold. Companies that optimize only $d_1$ expose themselves to boundary penalties when exploitative practices ($d_3$, $d_4$ violations) are revealed — the Rana Plaza factory collapse, the Foxconn suicides, conflict minerals in electronics. These are not PR crises; they are boundary crossings on the true manifold that were invisible on the $d_1$ projection.

### Supply Chain Vulnerability as Manifold Fragility

The $d_1$-optimal global value chain is the shortest path on the monetary projection. But the shortest path on a projection can be *fragile* — vulnerable to perturbations that the projection does not represent.

Consider the semiconductor supply chain before 2020. The $d_1$-optimal path concentrated production in a small number of fabrication plants in Taiwan and South Korea. On $d_1$, this was efficient: the lowest unit cost. On $d_9$ (epistemic security — robustness against disruption), the concentration was catastrophically risky: a single earthquake, pandemic, or geopolitical event could halt production for the global industry.

The COVID-19 pandemic and the subsequent chip shortage demonstrated the cost. The $d_1$-optimal geodesic — concentrate production for minimum unit cost — was not the full-manifold geodesic. The full-manifold geodesic would have included geographic diversification ($d_9$: reducing epistemic risk), domestic capacity ($d_4$: preserving national autonomy), and supply chain relationships ($d_5$: maintaining trust with multiple suppliers rather than depending on one).

The geometric prediction: supply chain resilience is a multi-dimensional optimization problem, not a cost-minimization problem. The optimal supply chain on the full manifold is more expensive on $d_1$ but shorter on $d_4$, $d_5$, and $d_9$. The trend toward "friend-shoring" and "near-shoring" is the market discovering the full-manifold geodesic after decades of following the $d_1$ projection.

## 13.5 Trade Wars as Manifold Competition

**[Modeling Axiom.]** When two countries impose tariffs on each other's goods, they are not merely raising prices. They are competing to shape the other country's decision manifold — to raise the curvature of the other's production paths and lower the curvature of their own.

A tariff on Chinese goods in the United States raises the curvature of the "buy Chinese" path for American consumers: the monetary cost ($d_1$) increases, making the domestic path relatively shorter. China's retaliatory tariff raises the curvature of the "sell to America" path for Chinese producers. Each country is trying to make its own geodesic shorter by making the other's geodesic longer.

On $d_1$ alone, tariff wars are negative-sum: both countries' consumers pay higher prices, and both countries' producers lose market access. The total $d_1$ cost is the standard deadweight loss.

On the full manifold, the analysis is more complex. If China's exports were produced under conditions that cross $d_3$ (fairness) and $d_4$ (autonomy) boundaries — forced labor, suppressed wages, environmental dumping — then the tariff is a boundary enforcement mechanism that prevents the American consumer's geodesic from traversing morally prohibited regions. The tariff raises the $d_1$ cost of the boundary-crossing path, routing the consumer's geodesic toward domestic or third-country alternatives that respect the boundaries.

The framework does not automatically endorse free trade or protectionism. It says: *compute the geodesic on the full manifold.* If free trade is the shortest path on all nine dimensions, free trade is optimal. If free trade requires traversing boundary-crossing regions (coerced labor, environmental destruction, institutional corruption), then some form of boundary enforcement — tariffs, sanctions, or trade agreements with labor and environmental provisions — may produce a shorter total geodesic despite its higher $d_1$ cost.

## 13.6 Currency as Gauge Transformation in Trade

**[Modeling Axiom.]** International trade introduces a gauge complication absent from domestic exchange: goods are priced in different currencies, and the exchange rate between currencies is itself a market-determined variable subject to speculation, manipulation, and misalignment.

In the geometric framework, a currency denomination is a *gauge choice* — a labeling convention that should not affect the evaluation of the underlying economic state. The same good, priced at $100 in the US and €92 in Europe, is the same good. The evaluation of whether to buy it should be invariant under the currency transformation. When it is not — when agents make different trade decisions depending on the denomination — we have a gauge violation.

Exchange rate misalignment is a systematic gauge violation that distorts the entire trade manifold. An undervalued currency makes a country's exports appear cheaper on $d_1$ than they actually are — the price heuristic is biased by the gauge. An overvalued currency has the opposite effect. The standard policy debate about "currency manipulation" is, in geometric terms, a debate about deliberate gauge violations: a country that artificially suppresses its exchange rate is distorting the price heuristic on the trade manifold, routing geodesics through its economy that would otherwise pass through other countries.

### Trade Agreements as Manifold Harmonization

**[Empirical.]** Trade agreements — from bilateral tariff reductions to comprehensive frameworks like the EU single market — are attempts to harmonize the decision manifolds of participating countries. Harmonization involves:

1. **Boundary alignment**: Agreeing on common regulatory boundaries ($d_8$), so that the regulatory constraints are the same across the manifold. Without alignment, a good that crosses from one country to another may traverse a boundary in the destination country that does not exist in the origin country.

2. **Metric convergence**: Aligning the covariance matrices $\Sigma$ across countries, so that the cost of economic transitions is comparable. Mutual recognition of professional qualifications, common product standards, and harmonized labor protections all serve to make the manifolds of participating countries more similar.

3. **Gauge fixing**: Agreeing on common units and measurement standards, so that the price heuristic is comparable across countries. The euro is the most dramatic example: a common currency eliminates the currency gauge entirely within the eurozone, removing an entire class of gauge violations from intra-eurozone trade.

The EU single market is, in this framework, the most ambitious manifold harmonization project in history. Its success — the world's largest single market by GDP — and its difficulties (the eurozone crisis, Brexit, disputes over regulatory harmonization) can both be understood geometrically. The success comes from the reduction in boundary penalties and gauge violations between member states. The difficulties come from the fact that manifold harmonization requires convergence of $\Sigma$ — the covariance matrices that encode each country's values, institutions, and economic structure. Countries with very different $\Sigma$ (e.g., Germany and Greece, with very different weights on $d_8$ institutional legitimacy and $d_3$ fairness norms) find harmonization costly, because convergence requires changing the relative importance of dimensions — which is a cultural and political transformation, not just a regulatory one.

## 13.7 The Geometry of Trade Imbalances

**[Modeling Axiom.]** A persistent trade imbalance — one country systematically exporting more than it imports — is a statement about the relative curvatures of the two countries' manifolds. The exporting country has lower curvature in the production of traded goods: its geodesics to production states are shorter, so it produces more cheaply and exports the surplus. The importing country has lower curvature in the consumption dimension (or in the production of non-traded services): its geodesics favor consumption of imported goods over domestic production.

On $d_1$ alone, a trade deficit is a monetary flow: the importing country sends money to the exporting country in exchange for goods. By the conservation laws of Chapter 9, the $d_1$ flow is balanced by a corresponding flow of financial assets (the exporting country accumulates claims on the importing country). This is the standard balance-of-payments accounting.

On the full manifold, the picture is richer. The trade relationship may generate evaluative surplus ($d_5$, $d_6$, $d_9$) that benefits both parties. But a persistent imbalance may also reflect a structural asymmetry: the importing country's $d_4$ (autonomy) is constrained by dependence on foreign production. Its $d_9$ (epistemic security) is degraded by the loss of domestic productive capacity. Its $d_6$ (community impact) may decline as manufacturing jobs disappear.

The "China shock" literature (Autor, Dorn, and Hanson, 2013) documented exactly this pattern: regions of the United States that were most exposed to Chinese import competition experienced not just $d_1$ losses (lower wages, higher unemployment) but cascading losses across evaluative dimensions — increased social dysfunction ($d_6$), loss of community identity ($d_7$), degraded institutional trust ($d_5$, $d_8$), and epistemic decline ($d_9$: reduced educational investment). The $d_1$-only trade model predicted that displaced workers would move to new sectors. The full-manifold model predicts that the displacement crosses multiple boundaries simultaneously, making adjustment far more costly than the scalar projection suggests.

---

## Worked Example: Maria's Bean Sourcing Decision

Maria evaluates three supply chain options:

**Option A: Commodity (Brazil, $12/lb)**
- $d_1$: -$960/month (80 lbs × $12)
- $d_3$: -0.6 (underpaid workers, exploitative conditions)
- $d_5$: -0.3 (anonymous broker, no relationship)
- $d_6$: -0.4 (plantation monoculture, community disruption)
- $d_7$: -0.7 (violates Maria's identity as ethical sourcer)
- Total BF: $960/\sigma_1^2 + 0.6^2/\sigma_3^2 + 0.3^2/\sigma_5^2 + 0.4^2/\sigma_6^2 + 0.7^2/\sigma_7^2$ ≈ **high**

**Option B: Fair-trade (Colombia via Elena, $25/lb)**
- $d_1$: -$2,000/month
- $d_3$: +0.5 (fair wages, cooperative structure)
- $d_5$: +0.4 (trusted relationship with Elena)
- $d_6$: +0.6 (community development fund)
- $d_7$: +0.8 (identity-consistent sourcing)
- Total BF: $2,000/\sigma_1^2 - (0.5^2 + 0.4^2 + 0.6^2 + 0.8^2)/\sigma_k^2$ ≈ **moderate**

**Option C: Direct-trade (Colombia, no intermediary, $18/lb)**
- $d_1$: -$1,440/month
- $d_3$: +0.3 (fair but unverified)
- $d_5$: -0.2 (no trusted intermediary)
- $d_9$: -0.4 (quality uncertainty)
- Total BF: moderate but uncertain

The $d_1$-only ranking: A > C > B. The full-manifold ranking: B > C > A. Maria chooses B — the most expensive option monetarily, the cheapest on the full manifold. This is not irrational. It is optimal on the correct manifold.

### The Conservation Laws in Maria's Trade

Applying the conservation framework (Chapter 9) to Maria's sourcing decision:

**Option B (Elena, fair-trade):** The $2,000 monetary transfer is conserved — Maria pays, Elena receives. But the evaluative surplus is substantial: trust (+0.4 each), community (+0.6 each), identity (+0.8 Maria, +0.5 Elena). Total evaluative value created per transaction: approximately 2.3 units.

**Option A (commodity):** The $960 monetary transfer is conserved. The evaluative surplus is approximately zero — no trust, no community, no identity affirmation. The $1,040/month Maria saves on $d_1$ comes at the cost of 2.3 units of evaluative value per transaction.

The conservation law reveals the hidden structure: Maria's "willingness to pay more" for fair-trade beans is not a consumption preference on $d_1$. It is the purchase of evaluative surplus that cannot be obtained at any price through the commodity channel. The premium is the monetary cost of accessing a different region of the manifold — a region where evaluative value can be created.

## The Geometry of Trade Agreements: A Deeper Analysis

### Bilateral vs. Multilateral Trade

**[Modeling Axiom.]** The geometry of bilateral trade differs fundamentally from multilateral trade. In bilateral trade, two agents optimize on their respective manifolds, finding a BGE that balances both agents' behavioral friction. In multilateral trade, $n$ agents optimize simultaneously, and the equilibrium is a multi-dimensional fixed point.

The critical difference: bilateral trade can only exploit the curvature differentials between two countries. Multilateral trade can exploit *circular* curvature differentials — comparative advantage chains where Country A trades with B, B trades with C, and C trades with A, with each leg following a low-curvature geodesic that no bilateral combination can achieve.

The gains from multilateral trade exceed the sum of bilateral gains precisely because of this circularity. The geometric framework makes this precise: the multi-agent BGE on a trade manifold with $n$ countries finds geodesics that exploit the full curvature structure of the manifold, including curvature gradients that are invisible in any bilateral projection.

This is the geometric argument for multilateral trade organizations (WTO, EU single market): they enable the economy to find geodesics on the full $n$-country manifold, rather than being restricted to the bilateral projections. The gains from the multilateral geodesic over the best set of bilateral geodesics are the "geometric surplus" of multilateral trade — a surplus that arises from the curvature structure of the full manifold and cannot be computed from any set of bilateral comparisons.

### Rules of Origin as Geodesic Constraints

**[Empirical.]** Rules of origin in trade agreements specify what fraction of a good's value must be produced within the agreement's territory to qualify for preferential tariff rates. In the geometric framework, these are constraints on the geodesic's path: the supply chain trajectory must pass through specific regions of the production manifold.

The USMCA's automotive rules of origin, for example, require that 75% of a vehicle's value be produced in North America, with specific wage thresholds for labor content. These are boundary penalties on the production geodesic: a supply chain that routes through low-wage Asian manufacturing incurs a tariff penalty that a North American supply chain avoids.

The geometric analysis reveals that rules of origin create two competing effects. They *protect* evaluative dimensions ($d_3$: fair wages, $d_4$: labor autonomy, $d_6$: domestic community impact) by preventing the geodesic from routing through regions where these dimensions are violated. But they also *distort* the $d_1$ geodesic by forcing production through higher-cost regions. The net effect on total manifold cost depends on the covariance matrix $\Sigma$ — on how much each dimension matters.

For goods where the evaluative dimensions are strongly weighted (consumer products with visible supply chains, goods requiring skilled labor, products with significant community employment impact), rules of origin may reduce total manifold cost even while increasing $d_1$ cost. For anonymous commodity goods where only $d_1$ matters, rules of origin are pure deadweight loss. The framework provides the criterion: compute the full-manifold cost of the constrained geodesic versus the unconstrained geodesic, and assess whether the evaluative gains justify the monetary cost.

## The Political Economy of Trade, Geometrized

### Distributional Effects of Trade

**[Empirical.]** The Stolper-Samuelson theorem predicts that trade liberalization benefits the abundant factor and harms the scarce factor. In a labor-abundant developing country opening to trade, wages rise; in a capital-abundant developed country opening to trade with a labor-abundant partner, wages fall (or grow more slowly) while returns to capital increase.

The geometric framework extends this prediction to the full manifold. The workers displaced by trade competition do not only suffer $d_1$ losses (lower wages or unemployment). They experience cascading losses:

- $d_4$ (autonomy): loss of occupation eliminates the daily exercise of skill and judgment
- $d_5$ (trust): the implicit social contract — "work hard and you will prosper" — is violated
- $d_6$ (community): factory towns lose their economic anchor and social infrastructure
- $d_7$ (identity): "steelworker," "autoworker," "miner" are identities, not just job descriptions
- $d_9$ (epistemic): uncertainty about future employment, retraining options, and economic prospects

The policy implication: trade adjustment assistance that provides only $d_1$ compensation (cash payments, retraining subsidies) addresses one dimension of a five-dimensional loss. The empirical evidence on the effectiveness of Trade Adjustment Assistance (TAA) in the United States confirms this prediction: TAA recipients who receive cash and retraining show limited improvement relative to non-recipients, because the cash does not restore autonomy, identity, community, or trust. Effective adjustment requires multi-dimensional intervention — a prediction that follows directly from the manifold structure and that would not be generated by a $d_1$-only analysis.

### Trade and Power Asymmetry

**[Modeling Axiom.]** Trade between partners of unequal economic power is not just an exchange on the manifold; it is an interaction where the more powerful partner can shape the other's manifold. A large importing nation can set terms of trade that force the exporting nation's geodesic through regions that the exporting nation would not voluntarily traverse.

Consider trade between a large retail corporation and a small-country supplier. The corporation can demand: low prices ($d_1$ extraction from the supplier), rapid fulfillment timelines ($d_4$ constraint on the supplier's autonomy), exclusive dealing ($d_5$ trust asymmetry), and compliance with the corporation's proprietary standards ($d_8$ legitimacy defined by the powerful party). Each demand reshapes the supplier's manifold — raising the curvature on specific dimensions and constraining the available geodesics.

This is not free trade in the classical sense — where both parties freely choose their geodesics and find mutual gains. It is *constrained trade*, where one party defines the boundaries on both manifolds. The conservation law still holds on the transferable dimensions: the monetary transfer is zero-sum. But the evaluative surplus that would arise from genuinely voluntary exchange — mutual trust, relationship-building, identity affirmation — is suppressed by the power asymmetry. The dominant party captures $d_1$ surplus while preventing the creation of $d_5$–$d_9$ surplus that would empower the subordinate party.

The framework generates a prediction: trade relationships characterized by power asymmetry should generate less evaluative surplus than relationships between equal partners. This is testable by comparing the trust, community, and identity outcomes of supply chain relationships between small suppliers and large buyers versus relationships between equal-sized firms.

---

## Technical Appendix

**Definition 13.1 (Geodesic Gains from Trade).** The *geodesic gains from trade* between countries A and B are:

$$G = \left[\text{BF}(\gamma_A^{\text{autarky}}) + \text{BF}(\gamma_B^{\text{autarky}})\right] - \left[\text{BF}(\gamma_A^{\text{trade}}) + \text{BF}(\gamma_B^{\text{trade}})\right]$$

$G > 0$ whenever trade allows both countries to follow lower-curvature geodesics. On the scalar projection ($d_1$ only), $G$ reduces to the standard Ricardian gains from trade.

**Proposition 13.1 (Trade Restrictions May Be Optimal).** **[Conditional Theorem.]** A trade restriction that raises $d_1$ cost but prevents boundary crossing on $d_k$ ($k > 1$) reduces total manifold cost whenever $\beta_k > \Delta d_1 / \sigma_1^2$. The restriction is welfare-improving on the full manifold even though it is welfare-reducing on the scalar projection.

**Proposition 13.2 (Evaluative Surplus of Trade Relationships).** **[Conditional Theorem.]** In a repeated bilateral trade relationship between agents A and B, the cumulative evaluative surplus after $n$ transactions is:

$$V_{\text{eval}}(n) = \sum_{t=1}^{n} \sum_{k=5}^{9} \left[\Delta d_k^{(t)}(A) + \Delta d_k^{(t)}(B)\right]$$

This quantity is typically concave in $n$ (initial transactions build trust rapidly; subsequent transactions add trust at a diminishing rate) and can be permanently reduced to zero by a single betrayal (Theorem 9.3 from Chapter 9). The evaluative surplus provides a geometric measure of the "value of the trade relationship" that is invisible to $d_1$ accounting.

**Proposition 13.3 (The Anti-Comparative-Advantage Trap).** **[Conditional Theorem.]** A country whose comparative advantage on $d_1$ requires boundary crossing on $d_3$ or $d_4$ (e.g., comparative advantage in cheap labor that relies on coercive labor practices) faces a geometric trap: the $d_1$ geodesic that trade theory recommends is not a geodesic on the full manifold. If the country follows the $d_1$ recommendation and specializes in boundary-crossing production, it becomes locked into a production path that is optimal on the scalar projection but suboptimal on the full manifold — and the lock-in deepens over time as the production infrastructure, skill distribution, and institutional structure adapt to the boundary-crossing path. Escape from this trap requires a coordinated shift across multiple dimensions, analogous to escaping a poverty-trap basin (Chapter 10).

---

## References

Ricardo, D. (1817). *On the Principles of Political Economy and Taxation.*
Smith, A. (1776). *An Inquiry into the Nature and Causes of the Wealth of Nations.*
Stiglitz, J. E. (2002). *Globalization and Its Discontents.* Norton.
Autor, D. H., Dorn, D., and Hanson, G. H. (2013). "The China Syndrome: Local Labor Market Effects of Import Competition in the United States." *American Economic Review*, 103(6), 2121–2168.
Banerjee, A. V., and Duflo, E. (2011). *Poor Economics.* PublicAffairs.
Heckscher, E. (1919). "The Effect of Foreign Trade on the Distribution of Income." *Ekonomisk Tidskrift*, 21, 497–512.
Ohlin, B. (1933). *Interregional and International Trade.* Harvard University Press.
Krugman, P. (1980). "Scale Economies, Product Differentiation, and the Pattern of Trade." *American Economic Review*, 70(5), 950–959.
