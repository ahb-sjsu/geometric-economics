# The seam at |d| = 1, characterised. The fourfold chirality is an artifact of the coordinate's endpoints

**Exploratory, 2026-09-13. Changes no registered verdict.** `prereg-d4stability-v2`
is sealed and its result stands. This explains it.

---

## The short version

`d = +1` is not a place in the coordinate. **It is the set of gambles with no
loss branch at all**, and `d = -1` is the set with no gain branch. Checked on
every one of the 95,748 rows, with no exceptions:

| | rows | equivalence | holds |
|---|---|---|---|
| `d = +1` | 35,617 | the risky option has **no loss branch** | **True** |
| `d = -1` | 4,146 | the risky option has **no gain branch** | **True** |
| `\|d\| < 1` | 55,985 | the risky option is **mixed** | **True** |

At those endpoints the product `d·q` degenerates. With `d = +1` it *is* `q`, and
with `d = -1` it *is* `-q`. **A chirality coefficient fitted across the whole
corpus therefore cannot distinguish a genuine `d·q` interaction from "kappa
depends on `q` with opposite sign in gains and losses".** Those are the same
column.

And when the regimes are separated, that is exactly what it turns out to be.

| | `d·q` |
|---|---|
| pooled across all regimes | **+0.2506 ± 0.042** |
| **inside mixed gambles, where `d·q` is a real product** | **−0.0303 ± 0.0728** |

The chirality is **zero in the interior**. The pooled `+0.25` is assembled from
the two unmixed regimes, where the column is algebraically `±q`:

| regime | q-slope | contribution to a pooled `d·q` |
|---|---|---|
| `gain_only`, `d·q = +q` | +0.3372 | **+0.337** |
| `loss_only`, `d·q = −q` | −0.1430 | **+0.143** |
| pooled estimate | | **+0.2506**, between them |

## What the fourfold pattern actually is

Kahneman and Tversky's fourfold pattern is risk aversion for likely gains, risk
seeking for unlikely gains, and the reverse for losses. Written in this
coordinate that is precisely **"kappa has a q-slope of one sign in the pure-gain
regime and the other sign in the pure-loss regime"**, which is the two rows of
the table above.

The gain half of that pattern is reproduced here decisively and the loss half is
not determined at all, which a later section sets out. **What is not supported in
either half is the further claim that it is a `d·q` chirality**, a
rotation-covariant structure on a plane. At the only places the pattern lives,
`d·q` is not a product of two varying quantities, it is a relabelling of `q`. The
D₄ language adds a group-theoretic reading the data cannot carry, because the
coordinate is degenerate exactly where the phenomenon is.

**The original record's conclusion was right and its evidence was wrong.**
`RESULTS_d4_rotation.md` says the fourfold `d·q` is a corner phenomenon. It is.
But the `+0.003` interior estimate it rested on was masked by pooling seventeen
corner rows, and the correct interior estimate is `−0.0303 ± 0.0728`, which
reaches the same conclusion by measurement rather than by accident.

## The seam is real and it is large

Estimating kappa freely in strata of `1 − |d|`, approaching the boundary from
inside the mixed gambles. No functional form imposed, one free coefficient per
stratum, a single shared `bEV`.

**Gain side** (`bEV = +0.5971`):

| stratum, `1 − \|d\|` | n | kappa | se |
|---|---|---|---|
| 0.005 – 0.020 | 552 | **+0.7207** | 0.2040 |
| 0.020 – 0.050 | 1,266 | +0.6658 | 0.1437 |
| 0.050 – 0.100 | 1,736 | +0.3598 | 0.1330 |
| 0.100 – 0.200 | 3,584 | −0.1011 | 0.0824 |
| 0.200 – 0.400 | 7,602 | −0.2744 | 0.0492 |
| 0.400 – 1.010 | 22,342 | −0.1872 | 0.0188 |
| **`d = +1` exactly** | **35,617** | **−0.1529** | 0.0262 |

**jump at the boundary −0.8737 ± 0.2056, 4.2 standard errors.**

**Loss side** (`bEV = +0.5951`):

| stratum, `1 − \|d\|` | n | kappa | se |
|---|---|---|---|
| 0.050 – 0.100 | 431 | **−0.8219** | 0.2354 |
| 0.100 – 0.200 | 1,016 | −0.9186 | 0.1806 |
| 0.200 – 0.400 | 2,279 | −0.5924 | 0.1336 |
| 0.400 – 1.010 | 14,046 | +0.2515 | 0.0303 |
| **`d = −1` exactly** | **4,146** | **+0.5171** | 0.0710 |

**jump at the boundary +1.3390 ± 0.2459, 5.4 standard errors.**

The shape is the same on both sides and it is not a smooth approach. Kappa
**diverges** as the gamble becomes barely mixed, reaching `+0.72` on the gain
side and `−0.92` on the loss side, and then **reverses sign discontinuously** at
the point where the last trace of the opposite branch disappears.

A gamble offering a one percent chance of losing something behaves nothing like
the same gamble with that branch removed. That is loss aversion at its sharpest,
and it is a discontinuity in the stimulus space, not in the psychology: the two
gambles are nearly identical in expectation and utterly different in kind.

## Removing the seam does not rescue the quadratic

The natural next hope is that the six-term model is fine within regimes and the
seam is the whole problem. It is not.

| free surface over | cells | weighted `R²` of the quadratic | largest residual |
|---|---|---|---|
| all rows | 22 | 0.361 | 6.39 se |
| **mixed gambles only** | 24 | **0.306** | 5.62 se |

Restricting to mixed gambles makes the quadratic fit **worse**, not better. There
is more wrong with the six-term form than the seam.

## The coefficients are not parameters, demonstrated

The same six terms, projected from the free surface, on two subsets of one
corpus:

| term | all rows | mixed only |
|---|---|---|
| `d·q` | **+0.2155** | **−0.2052** |
| `d` | **−0.2625** | **+0.2525** |
| `d²−q²` | **+0.1118** | **−0.6789** |

**Every one flips sign.** These are projection coefficients of a surface the
basis fits badly, and they move with whatever stimuli are in the sample. That is
the whole explanation of `prereg-d4stability-v2`'s verdict, of the
CPC18-to-choices13k disagreement, and of the `+0.003` that started this.

## What the structure is, regime by regime

Separating regimes buys **195.8 log-likelihood units on 6 extra parameters**,
against a chi-square on 6 degrees of freedom whose 0.001 critical value is 22.5.

**Inside mixed gambles** the six terms are all identified and only two matter:

| term | coefficient | se | |
|---|---|---|---|
| `d²−q²` | **−0.6943** | 0.0873 | **−8.0 se, dominant** |
| `q` | +0.1714 | 0.0571 | +3.0 se |
| `const` | −0.0683 | 0.0243 | −2.8 se |
| `d²+q²` | +0.0464 | 0.0395 | +1.2 se |
| `d` | +0.0548 | 0.0535 | +1.0 se |
| **`d·q`** | **−0.0303** | 0.0728 | **−0.4 se** |

The interior is dominated by `d²−q²`, the term that distinguishes the two axes,
and the chirality is absent. That is the opposite of the published picture, in
which the chirality dominated and `d²−q²` was a rotation-breaking nuisance.

**Inside the unmixed regimes** `d` is constant, so only `{1, q, q²}` is
identified. Kappa estimated freely in q, no form imposed:

| `gain_only` | mean q | kappa | | `loss_only` | mean q | kappa |
|---|---|---|---|---|---|---|
| n 3,914 | −0.980 | **−0.5557** | | n 565 | −0.980 | **+0.8251** |
| n 9,549 | −0.849 | −0.3843 | | n 932 | −0.859 | +0.6715 |
| n 4,342 | −0.600 | −0.0263 | | n 976 | −0.548 | +0.5274 |
| n 10,658 | −0.276 | −0.1135 | | n 802 | −0.083 | +0.1455 |
| n 7,154 | +0.593 | **+0.1878** | | n 871 | +0.613 | +0.4535 |

Kappa rises with q among gambles that cannot lose. **That is half the fourfold
pattern, stated without any group theory**, and it is the whole of what a pooled
`d·q` was measuring. The loss column looks like the mirror image, falling from
`+0.83` to `+0.15` before turning up again, but it rests on 4,146 rows and its
fitted slope is `−0.1430 ± 0.1196`. Treat that column as suggestive and read the
section on it below before quoting it.

## Replication on the experience arm, six independent lines

The description arm is 95,748 trials. The corpus also holds **382,992 decisions
from experience**, presses two through five on the same problem after outcome
feedback, from the same participants on the same stimuli. `experience_arm.py`
runs the identical regime-separated model there and on each press index
separately.

| arm | n | `mixed:d·q` | `mixed:d²−q²` | `gain_only:q` | pooled `d·q` |
|---|---|---|---|---|---|
| description | 95,748 | −0.030 ± 0.073 | −0.694 ± 0.087 | +0.337 ± 0.042 | +0.251 |
| experience, all | 382,992 | −0.053 ± 0.037 | −0.407 ± 0.044 | +0.297 ± 0.021 | +0.165 |
| experience, press 2 | 95,748 | −0.060 ± 0.074 | −0.460 ± 0.088 | +0.310 ± 0.043 | +0.173 |
| experience, press 3 | 95,748 | −0.057 ± 0.074 | −0.382 ± 0.088 | +0.297 ± 0.043 | +0.176 |
| experience, press 4 | 95,748 | −0.054 ± 0.075 | −0.409 ± 0.088 | +0.285 ± 0.043 | +0.150 |
| experience, press 5 | 95,748 | −0.040 ± 0.075 | −0.378 ± 0.088 | +0.297 ± 0.043 | +0.163 |

**The chirality inside mixed gambles is never more than 0.8 standard errors from
zero in any of six lines**, while the pooled value is positive in all six. The
interior term `d²−q²` is strongly negative in all six. The pure-gain q-slope is
between `+0.28` and `+0.34` in all six, at 7 to 14 standard errors.

Regime separation buys 398.0 log-likelihood units on 6 parameters in the full
experience arm, and 93 to 113 in each press index alone.

**Feedback does not change the structure.** The press-index rows are four
successive decisions on the same problem with accumulating outcome information,
and they are flat in every column. Whatever the coordinate is doing, it is doing
it the same way before and after people learn what the gamble pays.

## One half of the fourfold story is not established

The clean reading, that kappa's q-slope is positive in gains and negative in
losses, rests on two numbers of very unequal quality.

| regime | description | experience | rows |
|---|---|---|---|
| `gain_only:q` | +0.3372 ± 0.0422 | +0.2973 ± 0.0213 | 35,617 / 142,468 |
| `loss_only:q` | −0.1430 ± 0.1196 | +0.0138 ± 0.0632 | 4,146 / 16,584 |

**The gain side is solid and the loss side is not determined.** Its two estimates
differ in sign, both are within one standard error of zero, and the regime holds
4,146 description rows against 35,617. With `gain_only` outnumbering `loss_only`
nine to one, the pooled chirality is **essentially the pure-gain regime's
probability slope, on its own**.

So the honest statement is narrower than the fourfold pattern. What this corpus
establishes is that **kappa rises with probability salience among gambles that
cannot lose**, and that this single fact accounts for the whole of the apparent
`d·q` chirality. Whether the mirror-image slope exists among gambles that cannot
win is not answered here, and this corpus does not contain enough pure-loss
gambles to answer it.

## The cross-corpus test, which failed, and what the failure taught

The seam account makes a sharp prediction: if the pooled chirality is an
accounting artifact of regime mixing, corpora should differ in the pooled value
because they differ in regime composition, and should agree at about zero inside
mixed gambles.

**Both halves of that prediction failed, and the second failure was the useful
one.** `cross_corpus_regimes.py` fits five corpora, including CPC18 at the
individual trial level for the first time, taking first-trial rows from
`cpc18_raw.csv` where no feedback has been given.

| corpus | n | gain-only share | pooled `d·q` | `d·q` inside mixed |
|---|---|---|---|---|
| CPC18 trial 1, all lotteries | 26,467 | 0.40 | +0.5041 | **+0.9679** |
| CPC18 trial 1, two-outcome | 14,614 | 0.38 | +0.3164 | **+0.7538** |
| choices13k aggregate, all | 2,346 | 0.37 | +0.3178 | +0.0337 |
| choices13k aggregate, two-outcome | 1,282 | 0.37 | +0.4366 | +0.1223 |
| peterson description | 95,748 | 0.37 | +0.2506 | −0.0293 |

**The regime shares are nearly identical**, 0.37 to 0.40, so composition has
almost no variation with which to explain anything. And the spread of the mixed
chirality across corpora, `0.997`, is four times the spread of the pooled one,
`0.254`. On its face that says the interior chirality really does differ between
corpora, by about ten trial-level standard errors, which would overturn
everything above.

## The standard errors were wrong, in this line and before it

CPC18's 26,467 first-trial rows come from **270 games**, and its mixed subset is
13,927 trials over **137 distinct problems**, about 102 subjects apiece. The
coordinate `(d, q)` is a property of the problem, not of the trial. Ninety-eight
people answering the same gamble do not supply ninety-eight independent
observations about how kappa varies with that gamble's coordinate. **The
effective sample for a `(d, q)` coefficient is the number of problems.**

`cluster_bootstrap.py` resamples problems with replacement, 400 draws, refitting
each time:

| corpus | mixed trials | **problems** | `d·q` | trial-level se | **clustered se** | 95% CI | |
|---|---|---|---|---|---|---|---|
| CPC18, all lotteries | 13,927 | **137** | +0.9679 | 0.0946 | **0.3179** | [+0.241, +1.484] | excludes 0 |
| CPC18, two-outcome | 7,923 | **81** | +0.7538 | 0.1241 | **0.5614** | **[−0.897, +1.380]** | **includes 0** |
| peterson | 55,985 | **3,314** | −0.0293 | 0.0306 | 0.0538 | **[−0.140, +0.071]** | **includes 0** |

The clustered standard error is **4.5 times** the trial-level one on CPC18's
clean subset and 1.8 times on peterson, exactly as the ratio of cluster sizes
predicts.

**On like-for-like two-outcome data with honest uncertainty the intervals
overlap.** CPC18 at `[−0.897, +1.380]` and peterson at `[−0.140, +0.071]` are not
in conflict, and neither excludes zero. The ten standard error corpus difference
was an artifact of counting 102 subjects on one gamble as 102 independent facts
about that gamble's coordinate.

The one row that still excludes zero, CPC18 with all lotteries, rests on the
multi-branch approximation that reads a ten-branch lottery through three columns.
That is the approximation this line has documented as unsound, so it is the
weakest row in the table and not the one to build on.

## What this means for the number that started everything

CPC18's interior chirality of `+0.4438` is the estimate the whole lineage has
been trying to replicate, across five registrations. **It rests on roughly 137
mixed problems, and its honest problem-clustered uncertainty is on the order of
`±0.3` to `±0.6`.**

`prereg-d4interior-v3` asked whether choices13k reproduced it, and judged that
against a bar of `0.1043` derived from choices13k's own null. **It never asked
whether `+0.4438` was itself distinguishable from zero.** With clustered
uncertainty on clean data, it is not.

So the disagreement that launched `prereg-d4gate-v1`, `prereg-d4interior-v2`,
`prereg-d4interior-v3`, `prereg-d4stability-v1` and `prereg-d4stability-v2` was
between two numbers whose intervals always overlapped. The registrations were
correctly executed and asked a question that the uncertainty could not support.

## Consequences

1. **Do not report `d·q` as an interior structure.** Inside mixed gambles it is
   `−0.0303 ± 0.0728`. The pooled value is an artifact of a degenerate column.
2. **Do not read the D₄ or V₄ framing onto the fourfold pattern.** The pattern
   lives exactly where the coordinate degenerates, and at those points the
   group-theoretic content is empty.
3. **Report `d²−q²` as the interior term**, at `−0.6943 ± 0.0873`, with the
   caveat that the quadratic explains only `R² = 0.306` of the free surface
   there, so even this is a projection.
4. **The designed grid should not be run as specified.** It was built to place
   stimuli at chosen intermediate angles so a quadratic kappa could be estimated
   cleanly. The interior question it was to settle is answered, and the answer is
   that there is nothing there.
5. **`d` is the wrong variable near its endpoints.** It is continuous in value
   and categorical in meaning, and any model smooth in `d` is wrong across the
   seam. Regime separation, or a mixedness indicator, is the minimum fix.
6. **Cluster every standard error by problem.** Trial-level intervals on a
   coefficient of `(d, q)` are wrong by the square root of the subjects per
   problem, which is about ten on CPC18 and four on peterson. Every published
   interval on a kappa coefficient in this programme is too narrow, and the
   CPC18-derived ones are too narrow by a factor that changes conclusions.
7. **A corpus of many subjects on few problems is a small corpus** for this
   question. CPC18's 26,467 first-trial rows are 137 mixed problems. More
   subjects on the same gambles buy precision about those gambles' choice rates
   and nothing about how kappa varies across the plane.

## Reproduce

    python seam_covariates.py     # rebuild (H, p, L), assert alignment with the seal
    python seam_analysis.py       # Q1 to Q5
    python refine_structure.py    # the free surface and the equivalence tests
    python experience_arm.py      # the 382,992 decisions from experience
    python cross_corpus_regimes.py  # five corpora, CPC18 at the trial level
    python cluster_bootstrap.py     # problem-clustered uncertainty
