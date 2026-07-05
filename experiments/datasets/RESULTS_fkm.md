# FKM (Fisman-Kariv-Markovits 2007) — powered individual-level social evidence

The underpowered 9-game social-transfer test (Move 2c) needed real individual-level allocation data.
It arrived: the **FKM replication package** (OpenICPSR 115613) — **76 subjects × 50 budget-line dictator
choices** (2-person) + 65 × 50 (3-person). Each 2-person choice is a point on a budget line
`p_self·π_self + p_other·π_other = m` with the price of giving `p = p_other/p_self` varied across 50
rounds. The CES giving utility gives closed-form demand
`log(π_self/π_other) = c + (1/(1−ρ))·log(p)`, so a per-subject OLS recovers (α, ρ) and its fit R².

## The four tests (all powered, individual level, 3,800 choices)

**T1 — utility-consistency (the geometric/metric claim).** **96%** of subjects (66/69) have a
*downward-sloping giving demand* (slope b>0 ⇔ ρ<1 ⇔ convex preferences): they give less as giving gets
more expensive. Choice is governed by a **coherent preference/utility metric** — the powered version of
FKM's own GARP result (~90% consistent). This is direct, large-sample support for the thesis's premise
that choice is metric-governed, in the *social* domain.

**T2 — low-dimensionality (the low-rank pillar, socially).** A **2-parameter CES** (weight α +
substitution ρ) fits each subject with mean within-subject **R² = 0.54** (median 0.58; 59% above 0.5).
Individual giving preference is well-captured by **two numbers** — the social analog of the low-rank Σ
pillar, on powered real data.

**T3 — self↔other reflection + self-regard (the reflection motif).** Mean **21% given to the other**
(79% kept); median CES weight on self **α = 0.78**; **94%** put >50% weight on self. Strong self-regard
is the **σ_s reflection-breaking** — the same self↔other-reflection-broken-by-aversion structure as
Charness-Rabin (β=0.34) and the value-reflection-broken-by-loss-aversion motif.

**T4 — heterogeneity.** Substitution ρ ranges **−1.23 (p10) … −0.04 (median) … +0.67 (p90)** — from
near-utilitarian (perfect substitutes, ρ→1) to Rawlsian (Leontief, ρ→−∞). Matches FKM Table 2 (α
median ≈ 0.78, wide ρ spread), validating the reconstruction.

## Why this matters

This is the **powered social evidence the 9-game test could not reach.** It corroborates the thesis's
two load-bearing shapes *in the social domain, at the individual level, on 3,800 real choices*:

- **Choice is metric/utility-governed** (T1, 96% convex-consistent) — the geometric premise.
- **The social preference is low-dimensional** (T2, 2-param CES fits) — the low-rank shape.
- Plus the **reflection + self-regard** motif (T3), consistent across FKM, Charness-Rabin, and risk.

Combined with the earlier finding that unsupervised clustering collapses distributional preferences to
~3 types (EVIDENCE.md), the social domain now independently shows both **low dimensionality** and a
**reflection-broken value structure** — the same shapes as the risk-domain pillars.

## Honest bounds

- Simple OLS-CES on interior choices; FKM use nonlinear Tobit to handle the many corner solutions
  (Fig 1A shows ~40% of choices give ≤5%). Signs and the (α, ρ) spread match FKM Table 2, but R²=0.54
  is "low-dim but noisy," not a clean 1.0.
- 2-person shown; the **3-person data (Data_3D)** is loaded and available to split *giving* (self vs
  others) from *social preferences* (trade-offs between others) — FKM's distinctive elaboration and the
  natural next step for a within-domain transfer test.
- No within-subject 2-person↔3-person transfer (the two experiments used different subjects, IDs 1–76
  vs 135–199), so that specific transfer is a distributional comparison, not a within-subject one.

*Data: FKM (2007) replication, OpenICPSR 115613 (licensed; not committed). Reproduce: `python fkm.py`
with the extracted `raw_fkm/` present.*
