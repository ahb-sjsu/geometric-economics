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

## Dimension discovery from choices, steps 1–2 (`discover_dims.py`, `discover_dims.json`)

The candidate dimensions are the right singular vectors of the GDT metric U. U is k = 32, λ = 1e-5,
refit on all training pairs; its directions agree with the registered metric's at |cos| = 1.00. Each
candidate goes through the admission screens of moral-spectrum-analyzer's discovery roadmap that need
no second corpus:

- stability: the median over 20 bootstrap refits of the best |cos| (bar 0.70);
- non-redundancy: the direction's score on all 27,982 action texts against the nine xbse axes
  (max |r| < 0.35);
- importance: the rise in dev loss when the direction is projected out of the metric.

| Direction | Singular value | Dev loss if removed | Stability | Max \|r\| with xbse | R² from nine axes |
|---|---|---|---|---|---|
| 0 | 11.9 | +0.0315 | 0.93 | 0.25 (physical harm) | 0.13 |
| 1 | 9.9 | +0.0108 | 0.80 | 0.59 (privacy, −) | 0.44 |
| 2 | 9.5 | +0.0029 | 0.71 | 0.18 | 0.08 |
| 3–31 | 8.9–2.7 | ≤ 0.0018 | 0.30–0.59 | ≤ 0.31 | ≤ 0.12 |

Subspace stability (mean cos² of principal angles, median over resamples) is 0.65 for the top 4, 0.65
for the top 8, 0.68 for the top 16 and 0.73 for all 32.

- **Three directions are stable, and only two of them are also non-redundant: 0 and 2.** Past the
  third, the 32-dimensional metric is a rotating fit, not structure.
- **Direction 0 carries most of what the metric learned.** Removing it costs 0.032 nats per annotation,
  more than GDT's whole advantage over a linear scalar. Its extremes are cruelty to or estrangement from
  close family ("cutting my sick grandma out of my life", "despising my mentally handicap sister") at
  one end, and mundane acts ("asking for a refund", "changing laundry", "being polite") at the other.
  A plausible name is *moral gravity*, how serious the act is, as distinct from which value it touches.
  The nine axes explain 13% of it.
- **Direction 1 is mostly the xbse privacy and autonomy axes** (R² 0.44). It sets omitted care duties
  to family against offensive jokes and exposure.
- **Direction 2 looks like topic** (disability against weddings and family secrets) more than morality,
  and it carries little (0.003).

The names come from eight exemplars per end and are hypotheses. Before direction 0 is called a new
dimension it needs two checks:

1. whether it is moral-spectrum-analyzer's general-valence channel (its pc0 / G), which the roadmap
   already calls a moral-relevance detector;
2. cross-corpus replication (step 3).

### Direction 0 is not general valence (`check_valence.py`, `check_valence.json`)

General valence was checked in both of moral-spectrum-analyzer's forms:

- G, the trained channel `general_valence_joint`, at all three seeds (all passed their gates);
- pc0, the first principal component of the nine axis scores.

| | r with G (s0 / s1 / s2) | r with pc0 | R² nine axes | R² nine axes + G |
|---|---|---|---|---|
| Direction 0 | 0.26 / 0.18 / 0.19 | −0.25 | 0.130 | 0.144 |
| Direction 1 | 0.08 / 0.16 / 0.17 | −0.28 | 0.440 | 0.441 |
| Direction 2 | −0.09 / −0.08 / −0.06 | 0.09 | 0.084 | 0.091 |

86% of direction 0 lies outside everything moral-spectrum-analyzer measures.

### Not a family topic axis, and not pure gravity (`check_topic.py`, `probe_dir0.py`)

- A kinship-word indicator explains 7% of direction 0 (r = −0.27).
- Among actions that mention no kin, the spread is unchanged (SD 0.056 against 0.056 overall).
- The ordering holds without kin. At the low end are "killing my friend's tarantula", "cutting an
  autistic friend out of my life" and "potentially causing a girl to fail university". At the high
  end are "buying curtains" and "asking for a refund".

Median percentile on direction 0 by keyword group (0 = the low end):

| Group | n | Median | IQR |
|---|---|---|---|
| violence | 201 | 0.25 | 0.08–0.57 |
| kin | 6,122 | 0.33 | 0.15–0.55 |
| friends and partners | 10,026 | 0.41 | 0.20–0.63 |
| lying and cheating | 477 | 0.44 | 0.25–0.70 |
| theft, fraud, scams | 141 | 0.50 | 0.21–0.74 |
| strangers, customers, coworkers | 1,065 | 0.57 | 0.34–0.78 |

Violence sits low, as a gravity reading predicts. Impersonal wrongs (theft, fraud) sit mid-range and
acts toward strangers sit high, as a relational-stakes reading predicts. The best description these
data support is *harm to people the actor is close to, scaled by severity*. The keyword groups are
crude; the theft group includes "stealing my buddy's girl". A clean test needs independent ratings of
severity and of relational closeness on a sample of actions, then a regression of direction 0 on both.

Together with `../../strata2/DEVELOPMENT.md` and `../../menus/DEVELOPMENT.md`: in none of the three
domains does the data prefer a Euclidean distance from a reference point over its nearest
non-geometric rival. What the data do reward is curvature, and in menus a scale set by the menu.
