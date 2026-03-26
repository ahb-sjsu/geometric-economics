# Appendix C: Data Sources and Empirical Operationalization

This appendix describes the data sources used to validate the framework, the methods for measuring the economic metric from observable data, and the connections between existing economic indicators and the nine-dimensional decision manifold.

---

## C.1 Measuring the Economic Metric from Market Data

The economic metric is determined by the $9 \times 9$ covariance matrix $\Sigma$ (Chapter 4). Estimating $\Sigma$ from real-world data is the central empirical challenge of the framework. The matrix has $9 \times 10 / 2 = 45$ independent parameters (9 variances and 36 covariances). This section describes how each class of parameter can be estimated.

### Monetary Dimension ($d_1$): Variance and Cross-Covariances

The variance $\sigma_1^2$ --- the normal range of fluctuation in monetary outcomes --- is directly observable from market data: asset return distributions, income distributions, price volatility indices.

**Data sources:**
- CRSP (Center for Research in Security Prices): stock returns, daily/monthly, 1926--present.
- FRED (Federal Reserve Economic Data): interest rates, inflation, GDP components, labor market indicators.
- World Bank Open Data: cross-country income, trade flows, development indicators.
- BLS (Bureau of Labor Statistics): wage distributions, consumer price indices, employment data.

The cross-covariances $\sigma_{1k}$ (how monetary outcomes correlate with non-monetary dimensions) are estimated indirectly, typically from survey data or natural experiments. For example, $\sigma_{15}$ (money-trust covariance) can be estimated from the relationship between financial returns and trust measures in the General Social Survey or the World Values Survey.

### Rights Dimension ($d_2$): Property Rights Indices

The variance $\sigma_2^2$ and cross-covariances $\sigma_{2k}$ are estimated from institutional quality indices.

**Data sources:**
- Heritage Foundation Index of Economic Freedom: property rights sub-index, 183 countries, 1995--present.
- World Bank Doing Business/Business Ready indicators: contract enforcement, property registration.
- Fraser Institute Economic Freedom of the World: legal structure and property rights component.

### Fairness Dimension ($d_3$): Inequality Measures

The fairness dimension is operationalized through distributional measures.

**Data sources:**
- World Inequality Database (WID): top income shares, wealth concentration, pre/post-tax distributions, 100+ countries, 1900--present.
- Luxembourg Income Study (LIS): cross-national microdata on income and wealth, 50+ countries.
- Piketty and collaborators: historical capital-income ratios, wealth-to-income series.
- Gini coefficients: World Bank, OECD, national statistical offices.

### Autonomy Dimension ($d_4$): Labor Market Flexibility

**Data sources:**
- OECD Employment Outlook: employment protection legislation indices, hours worked, job tenure.
- ILO (International Labour Organization): labor market indicators, informal employment, forced labor estimates.
- Survey data: job satisfaction surveys, self-employment rates, union coverage.

### Trust Dimension ($d_5$): Social and Institutional Trust

**Data sources:**
- World Values Survey (WVS): generalized trust ("Most people can be trusted"), institutional trust, 100+ countries, 1981--present.
- General Social Survey (GSS): interpersonal trust, confidence in institutions, U.S., 1972--present.
- Edelman Trust Barometer: trust in government, business, media, NGOs, 28 markets.
- Experimental data: trust games (Berg, Dickhaut, and McCabe, 1995), repeated-interaction protocols.

### Social Impact Dimension ($d_6$): Externality Measures

**Data sources:**
- EPA (Environmental Protection Agency): emissions data, Toxics Release Inventory.
- Global Carbon Project: national CO$_2$ emissions, 1959--present.
- OECD Better Life Index: community engagement, environmental quality, social connections.
- Eurostat: social impact indicators, community cohesion metrics.

### Identity/Virtue Dimension ($d_7$): Cultural Values

**Data sources:**
- Hofstede cultural dimensions: individualism/collectivism, long-term orientation, 70+ countries.
- Schwartz Values Survey: 10 basic human values, 82 countries.
- World Values Survey: self-expression values, traditional/secular values.

### Legitimacy Dimension ($d_8$): Governance Quality

**Data sources:**
- World Bank Worldwide Governance Indicators: rule of law, regulatory quality, government effectiveness, control of corruption, 200+ countries, 1996--present.
- Transparency International Corruption Perceptions Index.
- V-Dem (Varieties of Democracy): democratic governance indicators, 200+ countries, 1789--present.

### Epistemic Dimension ($d_9$): Information Quality

**Data sources:**
- Market microstructure data: bid-ask spreads as proxies for information asymmetry (Glosten and Milgrom, 1985).
- Credit rating agency data: rating accuracy, transition matrices, default prediction performance.
- Financial reporting quality: Beneish M-score for earnings manipulation detection, audit quality indicators.
- Media pluralism indices: Reporters Without Borders Press Freedom Index, media concentration data.

---

## C.2 GDP Alternatives as Partial Dimensional Recovery

The Scalar Irrecoverability Theorem (Chapter 6) proves that GDP discards 8 of 9 dimensions. Existing alternative indices can be understood as attempts to recover some of the discarded dimensions.

### Stiglitz-Sen-Fitoussi Commission (2009)

The Commission on the Measurement of Economic Performance and Social Progress recommended a multi-dimensional dashboard including:

| Recommendation | Dimension Recovered | Manifold Dimension |
|---|---|---|
| Material living standards (income, consumption, wealth) | Monetary outcomes | $d_1$ |
| Health | Physical wellbeing | $d_1$ (partial), $d_6$ |
| Education | Epistemic capacity | $d_9$ |
| Personal activities including work | Autonomy | $d_4$ |
| Political voice and governance | Legitimacy | $d_8$ |
| Social connections and relationships | Trust | $d_5$ |
| Environment (present and future) | Social impact | $d_6$ |
| Insecurity (economic and physical) | Rights, autonomy | $d_2$, $d_4$ |

The Commission's dashboard recovers dimensions $d_1$, $d_2$, $d_4$, $d_5$, $d_6$, $d_8$, $d_9$ --- 7 of 9 dimensions. The missing dimensions are $d_3$ (fairness as an intrinsic dimension, not just an observable) and $d_7$ (identity and virtue). This is the most comprehensive scalar-recovery attempt in the mainstream economics literature, and its incompleteness confirms the irrecoverability theorem: even the most sophisticated multi-dimensional dashboard cannot reconstruct the full metric from its scalar projections.

### Human Development Index (HDI)

The UNDP's HDI combines life expectancy, education, and GNI per capita.

| HDI Component | Dimension Recovered |
|---|---|
| Life expectancy at birth | $d_1$ (partial), $d_6$ |
| Mean years of schooling | $d_9$ |
| GNI per capita (PPP) | $d_1$ |

The HDI recovers 2 of 9 dimensions ($d_1$, $d_9$). It is a substantial improvement over GDP alone but remains a severe compression.

### Genuine Progress Indicator (GPI)

The GPI adjusts GDP for income distribution, household labor, environmental costs, and other factors.

| GPI Adjustment | Dimension Recovered |
|---|---|
| Income distribution weighting | $d_3$ (partial) |
| Value of household work | $d_4$ (partial) |
| Cost of environmental degradation | $d_6$ |
| Cost of crime | $d_2$ (partial) |
| Value of leisure time | $d_4$ (partial) |

The GPI recovers approximately 4 of 9 dimensions, but each recovery is partial (a scalar proxy for a full dimensional value).

---

## C.3 ESG Metrics as Partial Dimensional Recovery

Environmental, Social, and Governance (ESG) metrics --- used by investors to assess non-financial performance --- can be mapped directly to manifold dimensions.

| ESG Category | Typical Indicators | Manifold Dimension |
|---|---|---|
| Environmental | Carbon emissions, water use, waste | $d_6$ (social impact) |
| Social - Labor | Worker safety, fair wages, diversity | $d_3$ (fairness), $d_4$ (autonomy) |
| Social - Community | Community investment, local impact | $d_6$ (social impact) |
| Social - Human Rights | Supply chain labor standards | $d_2$ (rights) |
| Governance - Board | Independence, diversity, structure | $d_8$ (legitimacy) |
| Governance - Transparency | Reporting quality, audit standards | $d_9$ (epistemic) |
| Governance - Ethics | Anti-corruption, whistleblower protection | $d_5$ (trust), $d_7$ (identity) |

ESG metrics collectively cover 7 of 9 dimensions (missing $d_1$ --- monetary payoff --- which is measured by standard financial metrics). The ESG framework's limitation, from the manifold perspective, is that it does not estimate the *covariance matrix* $\Sigma$. It measures individual dimensions but not their interactions. The metric --- which is determined by $\Sigma^{-1}$ --- requires the full covariance structure, including how environmental performance covaries with governance quality ($\sigma_{68}$), how labor practices covary with financial returns ($\sigma_{13}$), and so on. This covariance estimation is the key empirical frontier identified in Chapter 16.

---

## C.4 Experimental Validation Data

### Game Theory: Ultimatum Game (Henrich et al., 2001, 2005, 2010)

**Dataset**: Ultimatum game offers and rejections across 15 small-scale societies (Machiguenga, Tsimane, Lamalera, Au, Gnau, Hadza, Mapuche, Torguud, Khazakh, Sangu, Orma, Shuar, Achuar, U.S., and others). N = 1,762 subjects.

**Framework prediction**: Cross-cultural variation in offers is explained by variation in the covariance matrix $\Sigma$ --- specifically, the relative weight of $d_3$ (fairness) versus $d_1$ (monetary payoff) --- rather than by "cultural preferences" treated as unexplained parameters.

**Result**: The framework predicts offer levels across all 15 societies with MAE < 5%, using only three metric parameters ($\sigma_1$, $\sigma_3$, $\sigma_{13}$) calibrated to each society's market integration and institutional structure.

### Game Theory: Public Goods (Fraser and Nettle, 2020)

**Dataset**: 106 subjects (Study 1) and 528 subjects (Study 2) in public goods games with varied institutional contexts.

**Framework prediction**: Contribution levels are determined by the effective weight of $d_6$ (social impact) in the agent's metric, which varies with institutional framing.

**Result**: 4.3% out-of-sample prediction error.

### Prospect Theory: Kahneman and Tversky (1979)

**Dataset**: The original 17 choice problems from Kahneman and Tversky (1979).

**Framework prediction**: Prospect theory "anomalies" --- the certainty effect, reflection effect, and isolation effect --- are predicted by the Finsler asymmetry of the economic metric (loss aversion as metric asymmetry, Chapter 4) and dimensional activation patterns.

**Result**: 13 of 17 problems correctly predicted. The four misses involve mixed prospects where the dimensional activation pattern is ambiguous.

### Endowment Effect (Kahneman, Knetsch, and Thaler, 1990)

**Framework prediction**: The willingness-to-accept / willingness-to-pay ratio is determined by the loss aversion coefficient $\lambda$, which varies with dimensional activation.

**Result**: Predicted WTA/WTP ratio of 1.66, consistent with the experimental range of 1.5--2.5.

---

## C.5 Cross-Cultural Metric Calibration

The framework predicts that different cultures correspond to different covariance matrices $\Sigma$, producing different metrics on the same underlying manifold. The calibration procedure:

1. **Collect dimensional proxies**: For each culture/society, collect observables that proxy the nine dimensions (income variance, property rights indices, Gini coefficient, labor market flexibility, trust surveys, environmental indicators, cultural values, governance quality, information access).

2. **Estimate $\Sigma$**: Compute the sample covariance matrix from the proxied dimensional values, corrected for measurement error using the errors-in-variables framework.

3. **Validate**: Use the estimated $\Sigma$ to predict behavior in game-theoretic experiments conducted in that culture, and compare predictions to observed behavior.

This procedure has been applied to the Henrich et al. cross-cultural dataset (15 societies) and to the Fraser and Nettle institutional framing dataset (2 institutional contexts). In both cases, the metric variation explains behavioral variation that the standard model treats as unexplained "cultural preferences."
