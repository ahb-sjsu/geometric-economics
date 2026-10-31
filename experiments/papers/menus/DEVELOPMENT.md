# menus: geometry where binary choice cannot see it. Development record

**This is development, not a test.** Binary choice cannot separate a menu-relative geometric cost from
an additive value, because with two options under an additive cost the reference cancels
(`../strata2/DEVELOPMENT.md`). With three or more options it does not cancel. Here the menu models are
developed on one dataset. A second is held back unread for a sealed test.

## Data

- **Development: Molter et al. 2022** (*PLoS Comp Biol* 18(7): e1010283). Data from GitHub
  `moltaire/gda-context` at commit `66a42557`, using the authors' cleaned `results/0-clean_data/trials.csv`
  (their exclusions). There are 40 participants × 225 trials = 9,000 choices. Each trial offers three
  all-or-nothing gambles (probability p of winning m). A and B were set near indifference for each
  participant. C is either an asymmetrically dominated decoy (attraction trials), an extreme that makes
  the target the middle option (compromise trials), or a filler.
- **Held back, not read: Chau et al. 2014** (Dryad `10.5061/dryad.040h9t7`, CC0, `behav_*.mat`) and
  **Gluth et al. 2018** (OSF `8r4fh`, four experiments, each with a Data component). In most of these
  trials the third option is shown but cannot be chosen. Only file names have been listed.

## Models (`explore_molter.py`)

An option is mapped to coordinates (W(p), (m/20)^α), where W is linear in log-odds. The cost is measured
against the menu reference r, the best value on each attribute across the three options. Choice is a
softmax of the negative cost.

| Model | Cost | Context effect possible? |
|---|---|---|
| ADD | a_p (r_p − x_p) + a_m (r_m − x_m) | no: the reference cancels |
| L2 | √(a_p² (r_p − x_p)² + a_m² (r_m − x_m)²), the GDT menu geometry | yes, through the reference |
| Lq | Minkowski exponent q free | yes |
| ADD-rng | ADD with each gap divided by the menu's range on that attribute | yes, through the scale |
| L2-rng | L2 on range-scaled gaps | yes |

The models are fit pooled over participants and scored by 5-fold cross-validation over participants.
The interval is a bootstrap over participants.

## Result (`explore_molter.json`)

| Model | CV log-loss per trial | minus ADD | Predicted relative share of target, attraction / compromise | Predicted P(C) |
|---|---|---|---|---|
| ADD | 1.052 | | 0.48 / 0.50 | 0.32 |
| L2 | 1.074 | +0.022 | 0.48 / 0.55 | 0.31 |
| Lq (q = 0.65) | 1.040 | −0.012 [−0.027, +0.002] | 0.49 / 0.42 | 0.33 |
| **ADD-rng** | **0.961** | **−0.091 [−0.138, −0.044]** | 0.69 / 0.51 | 0.25 |
| L2-rng | 1.001 | −0.051 [−0.096, −0.006] | 0.67 / 0.56 | 0.28 |
| *observed* | | | *0.571 / 0.536* | *0.217* |

## Reading

1. **A menu-relative reference with Euclidean distance does not produce the attraction effect.** A
   dominated decoy is worse than its target on both attributes, so it never moves the attribute-wise
   best, and L2 predicts no effect (0.48). It also fits worse than the additive model.
2. **A menu-dependent scale does.** Measuring each attribute's gaps in units of the menu's range on that
   attribute (range normalisation, as in Soltani, De Martino and Camerer 2012) is the best model by a
   wide margin. It predicts the attraction effect and the low choice share of the decoy. It overshoots
   the effect (0.69 against 0.57).
3. **In geometric terms, the menu sets the metric, not the reference point.** That is the efficient-coding
   reading of Observation Theory's consumer: the code adapts to the spread of what is on offer.
4. **Caveats.** The fits are pooled, although A and B were calibrated to indifference participant by
   participant. With α fitted near 0, the magnitude coordinate is effectively log m. There is one dataset.

## Round 2: how much scaling, by what statistic, against which competitor (`explore_molter2.py`)

New models:

- **RNGρ** divides gaps by range^ρ, with ρ free in (0, 1.5). ρ = 0 is ADD and ρ = 1 is round 1's ADD-rng.
- **SD** divides by the menu's standard deviation.
- **L2ρ** is Euclidean on range^ρ-scaled gaps.
- **DN** is divisive normalisation (Louie, Khaw and Glimcher 2013), the standard context model in
  neuroeconomics.

There are two protocols:

- **pooled**, as in round 1;
- **personal**, with one parameter set per participant and 5-fold cross-validation over that
  participant's trials.

The personal protocol matters here because A and B were calibrated to indifference participant by
participant.

| Model | pooled CV | minus ADD | personal CV | minus ADD |
|---|---|---|---|---|
| ADD | 1.039 | | 0.698 | |
| RNG (ρ = 1) | 0.952 | −0.087 [−0.136, −0.044] | 0.766 | +0.068 [+0.028, +0.110] |
| **RNGρ** | **0.938** | −0.101 [−0.129, −0.074] | **0.636** | **−0.062 [−0.083, −0.042]** |
| SD | 0.958 | −0.081 [−0.129, −0.036] | 0.767 | +0.068 [+0.026, +0.112] |
| L2ρ | 0.992 | −0.047 [−0.095, −0.003] | 0.731 | +0.033 [+0.005, +0.059] |
| DN | 1.039 | −0.000 [−0.025, +0.023] | 0.696 | −0.002 [−0.015, +0.009] |

Personal fits:

- RNGρ beats DN by 0.060 [0.039, 0.082] and beats L2ρ by 0.095 [0.078, 0.113].
- ρ has median 0.55 and interquartile range 0.39–0.75 across participants. Pooled, it is 0.84.
- Cross-validated, RNGρ predicts relative target shares of 0.572 for attraction (observed 0.571) and
  0.530 for compromise (observed 0.536). Its predicted P(C) is 0.230, against 0.217 observed.

**Reading.**

- Full range normalisation's pooled win was an artefact of pooling heterogeneous participants. Per
  participant it loses to additive value.
- What survives is partial scaling, with an exponent between 0 (absolute coding) and 1 (full scale
  invariance), plus person-specific weights. It reproduces both context effects at their observed size.
- Divisive normalisation does no better than additive value on these menus.
- Euclidean combination loses under every protocol.

**A physics reading of ρ (interpretation, not a result).** ρ = 1 is the scale-symmetric point (Weber).
ρ = ½ is the square-root law of noise-limited discrimination (DeVries-Rose in vision). In the author's
GE-P-2026-007 notation, ρ plays the part of the conservation coefficient κ, and an exponent whose
interval excludes 0 and 1 is that registration's outcome (b), "anchored but leaky". Round 3 tests the
two claims mathematical physics makes about such an exponent:

- **universality:** the same exponent for probability and amount;
- **crossover:** from ½ to 1 as the menu widens, with a single scale R₀.

## Round 3: universality and crossover (`explore_molter3.py`, personal protocol)

The models are:

- **RHO2**, with separate exponents ρ_p and ρ_m;
- **CROSS**, which divides gaps by √(R (R₀ + R)). Its exponents are fixed: ½ for ranges below R₀ and 1
  above. Its only free parameters are one R₀ per attribute, so it has as many as RHO2.

Results:

| Comparison (per-participant CV, minus) | Difference |
|---|---|
| RNGρ minus ADD | −0.066 [−0.089, −0.046] (round 2 reproduces on new folds) |
| RHO2 minus RNGρ | +0.0015 [−0.012, +0.018] |
| CROSS minus RNGρ | −0.0002 [−0.009, +0.006] |
| CROSS minus RHO2 | −0.0017 [−0.018, +0.009] |

- **Universality.** The prediction does not need attribute-specific exponents. From the per-participant
  fits on all trials, the median ρ_p is 0.49 and the median ρ_m is 0.66. The difference is −0.09
  [−0.19, −0.003], marginal. The exponents correlate across people (Spearman 0.53), so each person
  carries a common scaling tendency.
- **Crossover.** The law with no free exponent predicts as well as a free exponent, but R₀ is not
  identified. Its per-participant estimates run from about 0.1 to 10⁶: the interquartile range is
  0.135 to 9.4 × 10⁵ for probability and 0.002 to 25 for amount. Molter's menus do not vary their
  ranges enough to place a crossover, so this dataset can neither confirm nor refute it.
- **Design consequence.** A test of the crossover needs menus whose ranges vary over an order of
  magnitude or more. That should guide how the held-back Gluth data are used.
