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
