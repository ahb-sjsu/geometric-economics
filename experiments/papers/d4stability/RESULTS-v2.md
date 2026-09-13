# prereg-d4stability-v2 — run record. The chirality is not stable, because the model is wrong

**Run 2026-09-13 on Atlas.** peterson2021using, 95,748 first-press description
trials over 5,672 strictly two-outcome problems from 13,735 participants. Seal
verified on both machines before the fit. Bundle combined sha256
`b1887b5d2d82aba92f75b507bebaff50bdb6582f75f44402579baec24273dbb6`, signed tag
`prereg-d4stability-v2` on commit `2bd3040`.

**This run is valid.** Gradient infinity norm `8.6e-10` against a registered
tolerance of `1e-5`, every fold converged, `bEV = +0.5882` so F5 passes, and
every pipeline invariant passes including the I0 self-test, so F6 passes.

---

## Verdicts

| | Prediction | Verdict | | |
|---|---|---|---|---|
| W1 | Composition sensitivity, permutation `p < 0.05` on Q | **PASS** | `p` = **0.0005** | Q = 103.0 |
| W2 | Range at least the between-corpus gap `0.5654` | **PASS** | range = **0.7282** | |
| W3 | Fold estimates not all of one sign | **PASS** | one positive, three negative | |

## What was measured

| fold | stakes | problems | trials | `c2` | se |
|---|---|---|---|---|---|
| 0 | smallest | 1,394 | 23,003 | **+0.2279** | 0.0369 |
| 1 | | 1,391 | 23,608 | −0.2609 | 0.0615 |
| 2 | | 1,440 | 24,197 | −0.4216 | 0.0730 |
| 3 | largest | 1,447 | 24,940 | **−0.5003** | 0.1361 |
| **whole corpus** | | **5,672** | **95,748** | **+0.2506** | 0.0233 |

The random-split null on Q has mean `9.93` and a 95th percentile of `25.83`. The
observed Q is `103.0`. **The four scale folds disagree with each other far beyond
anything a random partition of the same sizes produces.**

## What this settles, and it is not what it looks like

**The interior chirality is not a stable quantity.** Split one corpus by stake
size and it runs from `+0.23` to `−0.50`, a range of `0.728` that **exceeds the
entire CPC18-to-choices13k gap of `0.565`**. The design had power near 0.95 to
detect a spread large enough to explain that gap and it found a larger one.

So the between-corpus disagreement needs no explanation beyond stimulus
composition. It is what this quantity does routinely. **That closes the question
this line has been chasing since `prereg-d4gate-v1`.**

But the reason is sharper than "unstable", and three exploratory analyses run
after the seal say what it is.

## Why it moves, which is the part that matters

### The coordinate cannot see stake size, so this should not have happened

`(d, q)` is exactly invariant under positive scaling of both outcomes, checked
191,496 times in the sealed row builder. A chirality that runs monotonically with
stake size is moving with a variable the coordinate provably cannot represent.
That is misspecification, not instability.

### But the chirality does not actually interact with scale

Adding `scale` and `(d·q) × scale` to kappa, in `refine_structure.py`:

| term | coefficient | se |
|---|---|---|
| `scale` | **−0.0671** | 0.0157 |
| `(d·q) × scale` | **+0.0002** | 0.0293 |
| `d·q` base | +0.2595 | 0.0481 |

**The interaction is zero to four decimal places.** Absolute scale does belong in
kappa as a main effect, worth 31.8 log-likelihood units on 2 degrees of freedom,
but the chirality itself does not depend on stakes. So scale is not what moves
`c2` across the folds.

### The model is wrong, and that is what moves it

`refine_structure.py` estimates kappa **freely, one coefficient per cell of the
(d, q) plane, with no functional form imposed**. 22 cells of 25 survive at 400
trials each. Projecting that free surface onto the six symmetry terms:

| term | free surface | parametric |
|---|---|---|
| `const` | −0.0509 | −0.0518 |
| `d²+q²` | +0.0992 | +0.0875 |
| **`d·q`** | **+0.2155** | +0.2506 |
| `d` | **−0.2625** | −0.1716 |
| `q` | −0.0024 | +0.0161 |
| `d²−q²` | **+0.1118** | −0.0150 |

**The quadratic form explains a weighted `R² = 0.361` of the free surface, and
the largest cell residual is 6.39 standard errors.** Nearly two thirds of the
structure is something the six terms cannot represent.

That is the whole explanation. **Fit a badly misspecified model to subsamples
with different stimulus composition and the coefficients move, because each
subsample projects the same non-quadratic surface onto a different quadratic.**
The fold heterogeneity, and the CPC18-to-choices13k disagreement, are the same
artifact seen twice.

### What the free surface actually looks like

The strongest feature is a discontinuity at `|d| = 1`, the boundary between mixed
gambles and gambles with no loss branch at all:

| cell | mean `d` | mean `q` | n | kappa |
|---|---|---|---|---|
| 15 | **+0.962** | −0.980 | 508 | **+0.7397** |
| 20 | **+1.000** | −0.936 | 8,587 | **−0.5535** |

Two cells adjacent in the coordinate, `d` differing by 0.038, and kappa differing
by **1.29**. A quadratic cannot do that and no smooth function of `(d, q)` can.
Whatever is happening at the pure-gain and pure-loss boundary is not continuous
in this coordinate.

## What the chirality is, after all this

**It survives, and it is smaller than the parametric fit says.** The free surface
projects onto `d·q` at `+0.2155` without the term ever being imposed, so a chiral
component is a property of the data and not of the basis. But it sits inside a
surface the basis describes badly, so the number attached to it is a projection
coefficient rather than a parameter of anything.

## A claim I made and have to withdraw

After the first corrected fit I said that two of the three symmetry-breaking
terms, `q` and `d²−q²`, were absent, on the strength of their being small and not
significant. **Tested properly against a negligibility band, nothing of the kind
is established.**

The band is `|c| < 0.048`, one third of the smaller of the two CPC18 published
values, anchored outside this corpus because the point estimates had already been
seen. An equivalence test asks whether the whole confidence interval lies inside
the band:

| term | coefficient | 95% CI | verdict |
|---|---|---|---|
| `q` | +0.0161 | [−0.0601, +0.0923] | **not shown absent** |
| `d²−q²` | −0.0150 | [−0.1031, +0.0730] | **not shown absent** |
| `d²+q²` | +0.0875 | [+0.0420, +0.1329] | not shown absent |
| `d·q` | +0.2506 | [+0.1676, +0.3336] | not shown absent |
| `d` | −0.1716 | [−0.2351, −0.1082] | not shown absent |

Every interval is wider than the band. The corpus does not have the precision to
establish that any term is negligible, so "these terms vanish" was an
absence-of-evidence claim and is withdrawn. Given that the free surface projects
`d²−q²` at `+0.1118` rather than `−0.0150`, it was probably also wrong.

## The multi-branch hypothesis, tested and refuted

I proposed that choices13k's opposite sign came from collapsing multi-branch
lotteries into three columns, since 1,095 of its 2,380 rows have `LotNumB > 1`
while peterson excludes them. `c13k_two_outcome.py` refits v3's corpus on subsets:

| subset | n | chirality |
|---|---|---|
| all rows, reproducing v3 exactly | 2,380 | −0.1216 |
| two-outcome only | 1,285 | −0.0659 |
| multi-branch only | 1,095 | −0.1560 |
| two-outcome and unambiguous | 1,039 | −0.2314 |

**Refuted.** Restricting to the clean subset leaves the sign negative and moves
it nowhere near `+0.25`, and the subsets disagree with each other in no
consistent direction. The explanation is the misspecification above, which
predicts exactly this kind of incoherent subset-to-subset movement.

## What this does to the lineage

| | Outcome | What it established |
|---|---|---|
| `prereg-d4gate-v1` | VOID | a coordinate reimplemented instead of imported |
| `prereg-d4interior-v2` | VOID under its own F3 | an optimizer that did not converge |
| `prereg-d4interior-v3` | V1 FAIL, V2 FAIL | the CPC18 chirality does not replicate |
| `prereg-d4stability-v1` | VOID | a design oriented against its own outcome |
| `prereg-d4stability-v2` | **W1, W2, W3 all PASS** | the chirality is not stable, and the six-term model is why |

**The interior question is closed and the answer is that it was the wrong
question.** There is no stable interior chirality to find, because kappa is not a
quadratic in `(d, q)` and the chirality is a projection coefficient of a model
that captures a third of the structure.

**The designed grid in `experiments/papers/d4design/` should not be run as
specified.** It was built to place stimuli at chosen intermediate angles so a
quadratic kappa could be estimated cleanly. Estimating a misspecified model
cleanly is not progress. If the grid is run it should target the free surface,
and in particular the discontinuity at `|d| = 1`, which is where the structure
actually is.

## What to do next

1. **Characterise the free surface properly.** 22 cells at 400 trials is coarse
   and the corpus supports finer. The discontinuity at `|d| = 1` is the feature
   to chase and it is present in 8,587 trials in one cell alone.
2. **Find a coordinate in which the surface is smooth**, or accept that the
   pure-gain and pure-loss boundary is a genuine seam and model the two regions
   separately. A discontinuity of 1.29 in kappa across `Δd = 0.038` is either a
   real seam or a sign that `d` is the wrong variable near its endpoints.
3. **The experience arm is still untouched.** 384,948 decisions from experience
   on the same stimuli and the same people, a within-corpus contrast with no
   population confound. The free surface can be estimated there too and compared.
4. **Do not report any of the six coefficients as parameters** until a form is
   found that fits the surface. They are projections and they move with whatever
   stimuli happen to be in the sample, which is precisely what this run measured.

---

## Followed up and resolved, same day

`SEAM.md` characterises the `|d| = 1` seam and answers the question this record
left open. In short: `|d| = 1` is not a location in the coordinate but exactly
the set of gambles with no loss branch or no gain branch, verified on all 95,748
rows, and there `d·q` degenerates algebraically into `±q`. Separating regimes,
the pooled chirality of `+0.2506 ± 0.0423` becomes **`−0.0303 ± 0.0728` inside
mixed gambles**, replicated across six independent lines including the
382,992-decision experience arm, never more than 0.8 standard errors from zero.

The interior term is `d²−q²` at `−0.6943 ± 0.0873`. Regime separation buys 195.8
log-likelihood units on 6 parameters in the description arm and 398.0 in the
experience arm.

**The recommendations in the section above are superseded in one respect.** Item 2
suggests finding a coordinate in which the surface is smooth. The seam is not a
coordinate defect to be smoothed away, it is a real categorical boundary between
mixed and unmixed gambles, and the right response is to model the regimes
separately rather than to look for a chart that hides the join.
