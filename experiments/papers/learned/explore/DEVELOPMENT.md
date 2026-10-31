# Part III exploration: is distance from a reference the right curvature? Development record

**This is development on the spent prereg-learned-v1 data** (Scruples Dilemmas: which of two actions
is less ethical, with 5 annotations per pair). It uses the same splits and the same held-out rule
(dev and test pairs sharing an action with train are dropped) as the registration. It addresses the
registration's own caveat: H2 showed that curvature beats a linear scalar, not that *distance from a
reference* is the right curvature.

## Models (`explore_learned.py`)

| Model | Cost of an action e |
|---|---|
| LIN | w · e (logit = b + w·(e0 − e1)) |
| GDT | ‖U (e − r)‖₂, the registered form |
| GDTq | (Σ_i \|U (e − r)\|_i^q)^(1/q), q free in (0.5, 4.5) |
| SQD | ‖U (e − r)‖₂², squared distance: a convex quadratic utility with the reference folded into its linear term |
| QUAD | w·e + Σ_j s_j (u_j·e)²: a low-rank quadratic with free-sign curvature and no reference |

Ranks are k ∈ {16, 32, 64} for the encoders and k = 9 (full) for xbse. The penalty λ ∈ {0, 1e-5,
1e-4} is chosen on dev, with two restarts. Coordinates come from three sources:

- **LaBSE** and **BGE-M3**, the registered and replication encoders;
- **xbse**: the nine graded moral axes (physical harm, fairness, autonomy, privacy,
  societal/environmental, care, legitimacy, epistemic quality, identity attack). Each is its own
  fine-tuned BGE-M3 encoder plus a valence axis. All nine passed their gates (`xbse_scores.meta.json`).
  Scores are standardised on train.

## Result (`explore_learned.json`, test log-loss per annotation)

| Coordinates | LIN | GDT | GDTq | SQD | QUAD |
|---|---|---|---|---|---|
| LaBSE | 0.6549 | **0.6410** | 0.7069 | 0.6433 | 0.6638 |
| BGE-M3 | 0.6283 | 0.6196 | 0.6280 | **0.6175** | 0.6468 |
| xbse (9 axes) | 0.6770 | 0.6731 | 0.6723 | 0.6738 | **0.6700** |

| Comparison, paired bootstrap over test pairs | LaBSE | BGE-M3 | xbse |
|---|---|---|---|
| GDT − LIN | −0.0140 [−0.0189, −0.0093] | −0.0087 [−0.0131, −0.0041] | −0.0040 [−0.0061, −0.0019] |
| GDT − SQD | −0.0023 [−0.0058, +0.0013] | +0.0021 [−0.0012, +0.0055] | −0.0008 [−0.0013, −0.0002] |
| GDT − QUAD | −0.0228 [−0.0310, −0.0142] | −0.0272 [−0.0365, −0.0187] | +0.0030 [+0.0011, +0.0049] |
| GDTq − GDT | +0.0659 [+0.0547, +0.0781] | +0.0083 [+0.0037, +0.0132] | −0.0008 [−0.0017, +0.0002] |

## Reading

1. **Curvature beats a linear scalar everywhere.** This replicates H2 in all three coordinate systems.
2. **Distance from a reference cannot be told apart from a convex quadratic utility.** In both
   encoders, GDT and SQD are within ±0.002 with intervals spanning zero. In the moral-axis space GDT
   is ahead by 0.0008, which is significant but small. The registered geometric form is not shown to
   be the right curvature; it is one of two forms the data cannot separate.
3. **The free Minkowski exponent is not usable in high dimension.** In the encoders, GDTq drives q
   below 1 (0.6 to 0.9), reaches much lower training loss, and generalises badly. In the 9-d moral-axis
   space, q runs to the top bound (4.47, close to the max-norm, where the worst axis dominates) for a
   gain of 0.0008. Neither is evidence about the true norm.
4. **The nine moral axes carry much less than the raw encoders** (LIN 0.677 against 0.628 to 0.655).
   They still beat Part III's text-codebook axes (0.6875). In their space a free-sign quadratic with no
   reference is best. Some axes are evaluated convexly, some concavely, and that differs from distance
   to a single ideal point.

Together with `../../strata2/DEVELOPMENT.md` and `../../menus/DEVELOPMENT.md`: in none of the three
domains does the data prefer a Euclidean distance from a reference point over its nearest
non-geometric rival. What the data do reward is curvature, and in menus a scale set by the menu.
