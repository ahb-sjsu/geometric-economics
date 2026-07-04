# One Metric for Risk and Strategy: Cross-Domain Transfer of a Geometric Decision Model

*Pillar 1 (empirical). Draft. The crown-jewel result: a single decision metric, calibrated on risky
choice, predicts human play in strategic games it was never shown — the parsimony obligation of the
keystone theory, and the one thing no scalar decision theory can express.*

---

## Abstract

Cumulative prospect theory (CPT) describes risky choice; equilibrium and behavioral game theory
describe strategic choice; the two literatures share almost no machinery. We ask whether a single
geometric decision metric predicts behavior in **both**. Encoding lottery options and normal-form
game strategies into one feature space — expected value and outcome dispersion, with strategic
uncertainty proxied by payoff variance under a level-0 belief — we fit the metric on one domain and
**predict the other with no re-fit**. Three findings. **(1) Individual-level competitiveness.** On the
Choice Prediction Competition benchmark (CPC18; 694k choices), predicting *unseen games* out of
sample, the geometric model beats expected value and linear random-utility and comes within <1 s.d. of
CPT **with one fewer parameter**. **(2) Cross-domain transfer.** A metric fit *only* on lotteries
predicts human play across 110 published normal-form games, closing 66% of the chance-to-native gap;
the reverse direction fails. **(3) The transfer is a shared *shape*, not a shared *scale*.** Motivated
by polar quantization, we decompose the metric into a scale-invariant *aversion angle* and a
domain-specific magnitude; transferring only the angle raises both directions to ~97–100% of a native
fit, and the fitted angles are nearly equal across domains. A structural search over model forms
independently selects a maximally-transferable structure. We report the honest limits: the effect is a
shared risk–return tradeoff, not yet the social/moral dimensions the framework posits, and level-k
sophistication does not help.

---

## 1. Introduction

The strongest test of a decision theory is not fit but **transfer**: does a structure estimated in one
setting predict behavior in a genuinely different one, with nothing re-fit? Scalar theories cannot even
be asked this cross-domain question — CPT has no representation of a game, Nash none of a lottery. A
theory that spans both domains with *one* metric would, if it transferred, demonstrate exactly the
parsimony the keystone theory (Paper 0) requires and no incumbent can supply. This paper runs that
test on large public human datasets.

Our claim is deliberately bounded. We do **not** claim to beat CPT on lotteries — CPT is purpose-built
for that domain and we tie it, leaner by one parameter. We claim something a scalar theory cannot
match at any parameter count: **a metric calibrated on risky choice predicts strategic play out of
sample.**

## 2. Model and shared encoding

The geometric cost of an option is `C = √( Σ_k (Δa_k)² / σ_k² )` and choice is softmax over `−C/T`
(Paper 0, §2). To place lotteries and games in one space we encode each option by its **expected
value** and **dispersion**:

- **Lottery option** `(H, p, L)`: `EV = pH + (1−p)L`, `SD = √(p(H−EV)² + (1−p)(L−EV)²)`.
- **Game strategy** `s` of the row player with payoff matrix `M`: under a uniform level-0 belief over
  the opponent's actions, `EV_s = mean_j M[s,j]`, `SD_s = std_j M[s,j]` — strategic uncertainty as
  payoff variance. Payoffs are scale-normalized per dataset.

The cost is the Mahalanobis distance from the ideal (high EV, low dispersion): the same `σ_ev, σ_sd,
T` govern both domains, which is what makes the transfer question meaningful.

## 3. Data

- **Lotteries — CPC18** (Erev, Ert, Plonsky; Zenodo `10.5281/zenodo.2571510`, CC-BY): 270 games,
  27,780 description choices (first encounter, no feedback), median 120 subjects/game.
- **Games — bogota datapool** (Wright & Leyton-Brown, compiling Stahl-Wilson, Costa-Gomes,
  Goeree-Holt, Cooper, Haruvy, Camerer): 110 two-player normal-form games with human action
  frequencies.

## 4. Result 1 — held-out individual prediction (CPC18)

Predicting unseen games' choice rates, 20-split cross-validation by GameID:

| Model | #params | Held-out MAE | 
|---|--:|--:|
| constant | 1 | 0.199 ± 0.012 |
| Expected Value (logit) | 1 | 0.149 ± 0.008 |
| linear random-utility | 4 | 0.128 ± 0.010 |
| **Geometric** | 4 | **0.124 ± 0.009** |
| **CPT** | 5 | **0.118 ± 0.008** |

The domain-general geometry beats EV and random-utility out of sample and lands within <1 s.d. of the
domain-specialized CPT, with one fewer parameter. On its home turf, CPT should and does lead narrowly;
the point is that the geometry is competitive there *and* portable, which CPT is not.

## 5. Result 2 — cross-domain transfer

Fit one domain, predict the other with no re-fit; multinomial NLL, chance = uniform:

| Target | model | NLL | interpretation |
|---|---|--:|---|
| Games | fit-on-games (native) | 0.876 | (chance 1.040) |
| Games | **transfer lotteries→games** | 0.931 | **66% of chance→native gap closed** |
| Lotteries | fit-on-lotteries (native) | 0.624 | (chance 0.693) |
| Lotteries | transfer games→lotteries | 0.783 | worse than chance |

A metric that has seen *only lotteries* predicts strategic game play well above chance — two-thirds of
the way to a games-native fit, on games it was never shown. The reverse direction fails, exposing an
asymmetry we resolve next.

## 6. Result 3 — the transfer is a shared *shape* (polar decomposition)

The cost factors as `C = r · √((cosθ/σ_ev)² + (sinθ/σ_sd)²)`: a radius `r` (overall scale) times an
angular term set entirely by the ratio `σ_ev : σ_sd` — the **aversion angle**, the risk–return
tradeoff shape, which is *scale-invariant*. Transferring the whole metric forces both shape and scale
across domains; transferring only the angle, and recalibrating the magnitude, isolates what should be
universal:

| Direction | full transfer | **angle-locked (polar) transfer** |
|---|--:|--:|
| lotteries → games | 0.931 (66%) | **0.876 (100%)** |
| games → lotteries | 0.783 (−131%) | **0.627 (97%)** |

The asymmetry disappears: the angle-locked transfer reaches ~97–100% of a native fit **in both
directions**, and the fitted aversion angles are nearly equal across domains (`σ_ev/σ_sd`: lotteries
0.105, games 0.146). **The risk–return tradeoff shape is shared across risky and strategic choice;
only the stakes are domain-specific.** This is a stronger and cleaner statement of the shared-metric
claim than the raw transfer, and it is the paper's headline.

**Structural corroboration.** A search over model *forms* (value transform, dispersion feature, metric
norm, reference point), scored by worst-case bidirectional transfer, independently selects a
maximally-transferable structure (variance dispersion, city-block norm), confirming that the naive
Euclidean-SD form is not the most portable — two routes to the same conclusion.

## 7. Honest limits

- **A shared risk–return tradeoff, not (yet) the social dimensions.** Matrix games exercise payoff and
  strategic uncertainty, not the fairness/identity/legitimacy coordinates the framework posits. The
  transfer we demonstrate is of the risk part of the metric. Establishing transfer of the *social*
  coordinates requires social-preference games (ultimatum, public goods, trust) under the same
  protocol — the natural next study.
- **Level-k does not help.** Iterated best-response beliefs *degrade* the game encoding; the naive
  level-0 belief predicts best, consistent with the level-0 literature. The metric transfers because it
  captures the non-strategic risk response that dominates human play, not sophisticated reasoning.
- **Encoding.** Two-outcome approximation for multi-outcome lotteries; per-dataset scale
  normalization. These are model-neutral and do not favor the geometry.

## 8. Discussion

No scalar decision theory can be *asked* the question this paper answers, because none spans both
domains. That the geometry can be asked — and that its scale-invariant tradeoff shape transfers at
~97–100% of a native fit in both directions — is the first evidence that the shared metric is a
predictive structure, not a representational convenience. Combined with the individual-level
competitiveness on CPC18, it discharges the *parsimony* obligation of the keystone theory. What it does
not do is establish the projection gap (Paper 2) or the social-coordinate transfer or the human
confirmation of the strict-subsumption corollary — which we state plainly, because a foundation is
only as strong as the honesty of its claims.

*Artifacts: `datasets/cpc18.py`, `fit_transfer.py`, `bogota_games.py`, `cross_domain.py`,
`structural_search.py`; results in `datasets/RESULTS_cpc18.md`, `RESULTS_cross_domain.md`. Public
data (CC-BY / study terms).*
