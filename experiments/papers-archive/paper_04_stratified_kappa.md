# A Measured Boundary Penalty, and Why the Fourfold Pattern is Not a Rotation

*Structural paper. Draft 2026-09-13. Supersedes the group-theoretic reading in
`paper_03_fourfold_symmetry.md` and reports a measured boundary penalty for the
pathfinding framework of `geometric-methods` Chapter 6. Every number here comes from a sealed
registration or a committed script, and the exploratory work is marked as such
throughout.*

---

## Abstract

Risk attitude in two-outcome gambles is usually described by where a gamble sits
on two axes, how far it leans toward gains or losses and how likely its larger
outcome is. A recent line of work read the fourfold pattern of risk attitudes as
a symmetry on that plane, a rotation mixing the two axes, with a chirality that
tells clockwise from counter-clockwise. We show the chirality is an artifact of
the coordinate, and that the plane it is defined on is not a plane.

The gain and loss axis reaches its endpoints exactly on gambles that have no loss
branch, or no gain branch. Those are not places on a continuum. They are a
different kind of gamble, and on them the coordinate collapses, so the product
that was read as a chirality becomes a relabelling of the probability axis. A
probability effect among gambles that cannot lose therefore presents as a
rotation when it is pooled with everything else.

Measuring the three regions separately, on ninety six thousand individual choices
and again on three hundred and eighty three thousand, the chirality is absent
where it would have to live and the term that distinguishes the two axes is large
and negative. The two regions do not join smoothly. Risk sensitivity diverges as
a gamble becomes barely mixed and reverses discontinuously when the last opposite
branch is removed.

The discontinuity is not a new phenomenon. Volume 1 of this series already builds
pathfinding on decision manifolds around a cost with a smooth part and a
discontinuous part, and already tabulates a penalty for crossings in which a
dimension goes from positive to zero. A loss branch vanishing is exactly such a
crossing. That volume assigns an infinite penalty to the sacred case, meaning the
path is forbidden. Risk sensitivity is not sacred, so here the penalty is finite
and we measure it. These are the first values of a boundary penalty in this
programme that come from data rather than from stipulation.

What we add to that framework is a warning about how its spaces are given
coordinates. A dimension built as a balance between two magnitudes that cannot be
negative saturates exactly where one of them is absent, which is exactly where the
framework places a boundary. So the coordinate degenerates at the boundary it is
meant to help detect, and a smooth model fitted across it does not merely miss the
penalty. It reports structure that is not there.

We also report that the disagreement between two published estimates, which five
preregistrations were written to resolve, was never demonstrated. The coordinate
is a property of the gamble rather than of the trial, and once the uncertainty is
computed on that basis the two intervals overlap and neither excludes zero. A
corpus of many subjects on few gambles is a small corpus for this question.

---

## 1. Introduction

The fourfold pattern is one of the most replicated regularities in the study of
choice. People tend to avoid risk for likely gains and unlikely losses, and to
seek it for unlikely gains and likely losses. Four statements, one shape.

A natural move is to ask whether the four are one thing. Write each gamble as a
point on two axes, a domain axis running from pure loss to pure gain and a
probability axis running from unlikely to likely, and the fourfold pattern
becomes a sign that flips as you cross either axis. That is the signature of a
group acting on a plane, and it invites a stronger reading still, that the plane
carries a rotation and the pattern is a rotation-covariant quantity.

Our own earlier work made that move and then tested it. The test failed in a way
that took five preregistrations to understand, and the understanding is worth
more than the original claim. This paper reports it.

The short version is that the coordinate degenerates at its own endpoints, and
the endpoints are where the phenomenon lives. Everything follows from that.

We report a preregistered result, then the exploratory analyses that explain it,
then a methodological finding about uncertainty that changes what any of the
earlier numbers could have shown, and then the one result here that is not about
gambles at all. We disclose two claims of our own that did not survive, one
hypothesis of ours that was refuted, and one test we ran that turned out not to
be estimable.

---

## 2. The model and the coordinate

A participant chooses between two gambles. We model the probability of taking the
riskier of the two as a logistic function of two differences, the difference in
expected value and the difference in outcome spread, with the second weighted by
a quantity that depends on where the riskier gamble sits.

    logit P(take the riskier) = b_EV * dEV + kappa(d, q) * dSD

`dEV` and `dSD` are the riskier option minus the safer one, so `dSD` is positive
by construction. `kappa` is the object of interest. It is the modifier on risk
sensitivity and it is where any structure has to be.

The two coordinates come from `d4_rotation.py` and are used here unchanged. For a
gamble with outcomes weighted by their probabilities, write `pos` for the
probability-weighted positive part and `neg` for the negative part.

    d = (pos - neg) / (pos + neg)
    q = 2 * p_salient - 1

where `p_salient` is the probability of the outcome with the larger absolute
value. So `d` runs from minus one to plus one across the domain axis and `q` runs
from minus one to plus one across the probability axis.

The six symmetry-adapted quadratic terms on that plane are a constant, an
isotropic term `d^2 + q^2`, the product `d * q`, the two linear terms `d` and `q`,
and the axis-distinguishing term `d^2 - q^2`. Under the symmetry group of a
square, `d * q` is the component a ninety degree rotation sends to its own
negative, which is why it has been read as a chirality.

**The whole paper turns on one observation about `d`.** It equals plus one
exactly when `neg` is zero, and `neg` is zero exactly when the gamble has no loss
branch. It equals minus one exactly when the gamble has no gain branch. The
endpoints of `d` are not a region of a continuum. They are a categorical property
of the stimulus.

---

## 3. Data

`peterson2021using` from Psych-101, which is the choices13k stimulus family
recorded at the level of the individual choice rather than as a rate over a
median of sixteen subjects. 13,735 participants and 1,097,375 recorded key
presses.

Three parsers were written before one was correct, and the corpus is what the
third one says it is. The first captured the first press on each problem and
discarded the four that follow, losing ninety one percent of the corpus without
reporting it. The second replaced silence with accounting, and the accounting
immediately put 45.8 percent of presses in a bucket named "no declared menu",
because many options are lotteries of three to ten branches written as a comma
list. The third accounts for every press token in a named bucket and asserts that
the buckets sum to the corpus.

| bucket | presses | share |
|---|---|---|
| first press, decision from description | 96,237 | 8.77 |
| repeat press, decision from experience | 384,948 | 35.08 |
| ambiguous, no stated probability | 210,965 | 19.22 |
| multi-branch, outside the two-outcome coordinate | 405,225 | 36.93 |
| no declared menu | 0 | 0.00 |
| press key not on menu | 0 | 0.00 |

Multi-branch lotteries are excluded rather than approximated. The coordinate is a
two-outcome function and extending it to a ten-branch lottery would mean writing
a new coordinate and calling it the old one.

The analysed corpus is **95,748 first-choice description trials over 5,672
strictly two-outcome problems from 13,735 participants**. A second arm of
**382,992 decisions from experience** on the same stimuli and the same people is
used for replication in Section 7.

Every row is oriented by risk rather than by the order the transcript happened to
declare the two options, and the builder refuses to write a corpus in which that
fails. An earlier version of this analysis was void for exactly that error, and
Section 15 reports it.

---

## 4. The preregistered result

`prereg-d4stability-v2`, sealed and signed before any fit, asked whether the
chirality holds still inside one corpus. The corpus was split into four folds by
outcome scale and the spread of the chirality across folds compared against
random partitions of the same fold sizes. The statistic is Cochran's Q, which
divides each fold's deviation by its own standard error, because folds split by
scale differ in precision where random folds do not.

The test has a measured size of 0.020 against a nominal 0.05 and a power near
0.95 to detect a spread large enough to explain the disagreement it was built to
explain.

| fold | stakes | trials | chirality | se |
|---|---|---|---|---|
| 0 | smallest | 23,003 | +0.2279 | 0.0369 |
| 1 | | 23,608 | −0.2609 | 0.0615 |
| 2 | | 24,197 | −0.4216 | 0.0730 |
| 3 | largest | 24,940 | −0.5003 | 0.1361 |
| whole corpus | | 95,748 | +0.2506 | 0.0233 |

Q is 103.0 against a random-split null mean of 9.93, permutation p of 0.0005, and
a range of 0.728. All three registered predictions passed.

**The chirality is not a stable quantity.** Splitting one corpus by stake size
moves it by more than the whole distance between the two published estimates this
line was trying to reconcile.

That is the registered finding. The rest of this paper is exploratory and
explains it.

---

## 5. Where the chirality comes from

The coordinate is exactly invariant under multiplying both outcomes of a gamble
by a positive constant, which the row builder checks on every row at two scale
factors, 191,496 checks with no violations. So a chirality that moves with stake
size is moving with something the coordinate cannot represent.

The obvious candidate is that risk sensitivity genuinely depends on stakes.
Adding a scale term and a scale interaction says otherwise. Absolute scale does
belong in `kappa` as a main effect, worth 31.8 log-likelihood units on two
degrees of freedom, but the interaction of scale with the chirality is
`+0.0002 plus or minus 0.0293`. **Scale is not what moves the chirality.**

The real answer is that the endpoints of `d` are a different kind of gamble.
Checked on all 95,748 rows with no exceptions.

| | rows | equivalence |
|---|---|---|
| `d` equals plus one | 35,617 | the gamble has no loss branch |
| `d` equals minus one | 4,146 | the gamble has no gain branch |
| `d` strictly inside | 55,985 | the gamble is mixed |

On those two sets `d` is constant, so the product `d * q` is not a product. Where
`d` is plus one the column is `q`. Where `d` is minus one the column is minus `q`.
**A chirality fitted across the whole corpus cannot be told apart from a
probability effect carrying opposite signs in the two domains, because they are
the same column.**

Fitting the three regions separately settles which it is.

| | chirality |
|---|---|
| pooled across all regions | +0.2506 plus or minus 0.0423 |
| inside mixed gambles, where the product is a product | **−0.0303 plus or minus 0.0728** |

The pooled value is assembled from the two degenerate regions.

| region | slope in `q` | contribution to a pooled chirality |
|---|---|---|
| no loss branch, column is `q` | +0.3372 | +0.337 |
| no gain branch, column is minus `q` | −0.1430 | +0.143 |
| pooled estimate | | +0.2506, between them |

Gambles with no loss branch outnumber those with no gain branch nine to one, so
**the pooled chirality is essentially the probability slope among gambles that
cannot lose**.

---

## 6. The seam

The two regions do not join smoothly onto the interior. Estimating `kappa` freely
in strata approaching the boundary from inside the mixed gambles, with no
functional form imposed and one free coefficient per stratum.

| distance from the boundary | gain side | loss side |
|---|---|---|
| 0.005 to 0.020 | +0.7207 | |
| 0.020 to 0.050 | +0.6658 | |
| 0.050 to 0.100 | +0.3598 | −0.8219 |
| 0.100 to 0.200 | −0.1011 | −0.9186 |
| 0.200 to 0.400 | −0.2744 | −0.5924 |
| 0.400 to 1.010 | −0.1872 | +0.2515 |
| **at the boundary** | **−0.1529** | **+0.5171** |

Risk sensitivity **diverges** as a gamble becomes barely mixed, reaching `+0.72`
on the gain side and `−0.92` on the loss side, and then **reverses sign
discontinuously** when the last trace of the opposite branch is removed. The jump
is `−0.8737 plus or minus 0.2056` on the gain side, 4.2 standard errors, and
`+1.3390 plus or minus 0.2459` on the loss side, 5.4 standard errors.

A gamble offering a one percent chance of losing something behaves nothing like
the same gamble with that branch deleted. The two are nearly identical in
expectation and different in kind.

---

## 7. What the interior contains, and whether it replicates

Separating the regions buys 195.8 log-likelihood units on six extra parameters in
the description arm and 398.0 in the experience arm. Inside the mixed gambles all
six terms are identified and two matter.

| term | coefficient | se | standard errors |
|---|---|---|---|
| `d^2 - q^2` | **−0.6943** | 0.0873 | −8.0 |
| `q` | +0.1714 | 0.0571 | +3.0 |
| constant | −0.0683 | 0.0243 | −2.8 |
| `d^2 + q^2` | +0.0464 | 0.0395 | +1.2 |
| `d` | +0.0548 | 0.0535 | +1.0 |
| **`d * q`** | **−0.0303** | 0.0728 | **−0.4** |

The interior is dominated by the term that tells the two axes apart, and the
chirality is absent. That is the reverse of the published picture, in which the
chirality dominated and the axis-distinguishing term was a rotation-breaking
nuisance.

**This replicates on twenty one independent lines.** The description arm, the
full experience arm, each of four experience press indices separately, twelve
random halves of the participant pool, two alternative risk measures and a probit
link.

| line | chirality inside mixed | `d^2 - q^2` inside mixed |
|---|---|---|
| description, 95,748 | −0.030 plus or minus 0.073 | −0.694 plus or minus 0.087 |
| experience, 382,992 | −0.053 plus or minus 0.037 | −0.407 plus or minus 0.044 |
| experience press 2 | −0.060 | −0.460 |
| experience press 3 | −0.057 | −0.382 |
| experience press 4 | −0.054 | −0.409 |
| experience press 5 | −0.040 | −0.378 |
| twelve participant halves | mean −0.029, range −0.097 to +0.040 | mean −0.637, range −0.728 to −0.546 |
| variance as the risk measure | −0.041 plus or minus 0.070 | −0.813 plus or minus 0.093 |
| semi-deviation as the risk measure | −0.178 plus or minus 0.054 | −0.536 plus or minus 0.078 |
| probit link | −0.019 | −0.396 |

The chirality is never more than 0.8 standard errors from zero on any line except
semi-deviation, where it is negative, and it never approaches the `+0.25` the
pooled model reports. The axis-distinguishing term is strongly negative on all
twenty one.

**Feedback does not change the structure.** The four press indices are four
successive decisions on the same gamble with accumulating outcome information and
they are flat in every column.

**Regime separation predicts out of sample.** Splitting by gamble rather than by
trial, because trials on one gamble share a coordinate, and scoring on held-out
gambles across twenty splits.

| model | held-out log-likelihood per trial | splits won |
|---|---|---|
| expected value alone | −0.654463 | |
| pooled six-term | −0.651589 | 20 of 20 over expected value |
| region-separated | −0.649791 | 20 of 20 over pooled |

---

## 8. The uncertainty was wrong, and it changes what was ever shown

The coordinate is a property of the gamble, not of the trial. A hundred people
answering the same gamble do not supply a hundred independent observations about
how risk sensitivity varies with that gamble's coordinate. **The effective sample
for a coefficient on the plane is the number of distinct gambles.**

CPC18, the corpus that produced the published estimate this line was written to
replicate, has 26,467 first-trial rows and 270 games. Its mixed subset is 13,927
trials over **137 gambles**, about 102 subjects each. Resampling gambles with
replacement, four hundred draws, refitting each time.

| corpus | mixed trials | gambles | chirality | trial-level se | **gamble-clustered se** | 95 percent interval |
|---|---|---|---|---|---|---|
| CPC18, all lotteries | 13,927 | 137 | +0.9679 | 0.0946 | **0.3179** | +0.241 to +1.484 |
| CPC18, two-outcome | 7,923 | **81** | +0.7538 | 0.1241 | **0.5614** | **−0.897 to +1.380** |
| peterson | 55,985 | 3,314 | −0.0293 | 0.0306 | 0.0538 | **−0.140 to +0.071** |

The clustered standard error is 4.5 times the trial-level one on the clean CPC18
subset and 1.8 times on peterson, which is the ratio of cluster sizes.

**On like-for-like two-outcome data the intervals overlap and neither excludes
zero.** The apparent ten standard error difference between the two corpora is an
artifact of counting 102 subjects on one gamble as 102 independent facts about
that gamble.

The consequence for the original estimate is direct. CPC18's published interior
chirality rests on roughly 137 mixed gambles and its honest clustered uncertainty
is of order three tenths to six tenths. **It was never shown to differ from
zero.** Five preregistrations asked whether a second corpus reproduced it and none
asked whether the first corpus had established it.

**A corpus of many subjects on few gambles is a small corpus for this question.**
Counted by gambles rather than by trials, the corpus used here is twenty four
times the corpus that produced the original claim, despite appearing three times
smaller by row count.

---

## 9. What the structure is

The domain of risk sensitivity is not a plane with a group acting on it. It is a
partition into three pieces of two different dimensions, with the behaviour
discontinuous across the join.

| piece | what it is | dimension | free variable | what `kappa` does |
|---|---|---|---|---|
| mixed gambles | a gain branch and a loss branch | two | `d` and `q` | dominated by `d^2 - q^2` at −0.69, no chirality |
| no loss branch | 35,617 trials | one | `q` alone | rises with `q`, slope +0.30 to +0.34 |
| no gain branch | 4,146 trials | one | `q` alone | not determined |

On the two one-dimensional pieces the domain coordinate carries no information,
so the only structure available is a probability effect. The rise of risk
sensitivity with probability salience among gambles that cannot lose is the
solid, replicated half of the fourfold pattern and is the whole of what the
pooled chirality was measuring. The mirror-image slope among gambles that cannot
win is **not established here**, and Section 11 says why.

Two further limits belong with this description.

**Even inside the two-dimensional piece the quadratic form is inadequate.**
Estimating `kappa` freely over cells of the plane and projecting that free surface
onto the six terms, the quadratic explains a weighted 0.361 of it across all rows
and **0.306 inside mixed gambles alone**. Restricting to the interior makes the
fit worse. The largest cell residual is 5.6 standard errors. So `d^2 - q^2` is
itself a projection of a surface the basis does not describe, and should be
reported as the leading term rather than as a parameter.

**The coefficients are not parameters, and that is demonstrable.** The same six
terms projected from the free surface on two subsets of one corpus, all rows
against mixed gambles only, give `+0.2155` against `−0.2052` for the chirality,
`−0.2625` against `+0.2525` for the domain term, and `+0.1118` against `−0.6789`
for the axis term. Every one changes sign.

### The stratification, evaluated rather than gestured at

An earlier draft called this "stratified in the weak sense" and declined to say
more. That was not good enough. The work below separates what is a theorem from
what is measurable and tests only the second.

**The domain is Whitney stratified, and that is a theorem rather than a finding.**
The stimulus space is the set of triples of a high outcome, a probability and a
low outcome. The three regions are cut out by sign conditions, no loss branch
when the low outcome is non-negative, no gain branch when the high outcome is
non-positive, and mixed otherwise. That is a hyperplane arrangement, hence
semialgebraic, and every semialgebraic set admits a Whitney stratification. For an
arrangement the strata are open subsets of affine subspaces, so their tangent
spaces are constant and both Whitney conditions hold at once. **Measuring this
empirically would be a category error.** It is true by construction and carries no
information about people.

**The coordinate map degenerates, and that is measurable.** The map from a gamble
to its two coordinates has a Jacobian of rank two on the mixed region and rank one
on both unmixed regions, because the domain coordinate is constant there. Checked
by finite differences at four hundred random points in each region, giving rank
two at four hundred of four hundred mixed points and rank one at four hundred of
four hundred in each unmixed region. That is the precise content of the phrase
"the coordinate degenerates".

**The domain coordinate is continuous and not differentiable across the
frontier.** Its one-sided derivative with respect to the low outcome is
`2(1-p)/(pH)` from the mixed side and exactly zero from the other. Numerical
differencing reproduces the analytic value to six decimal places at four test
points. The coordinate has a corner at the frontier, not a smooth join.

**The frontier condition fails for the graph of risk sensitivity, so Whitney A and
B are inapplicable to it.** Whitney regularity is a condition on a pair of strata
in which the closure of the larger contains the smaller. For the graph of a
behavioural function that containment is an empirical question. Estimating risk
sensitivity freely in strata approaching the boundary gives a limit from inside of
`+0.7091` against a value on the edge of `-0.1530`, a difference of
`-0.8621 plus or minus 0.1614`, **5.3 standard errors**. The closure of the graph
over the mixed region does not contain the graph over the edge.

**The correct statement is therefore not that Whitney regularity is unverified. It
is that the pair is not a stratified set at all**, because the condition A and B
presuppose does not hold. They are undefined here rather than untested.

**And the one direction of Whitney A we attempted is not estimable.** Had the
frontier condition held, A would require the slope of risk sensitivity in the
probability direction just inside the boundary to converge to its slope on the
edge. The innermost stratum holds 768 rows and returns a slope of
`-3.0986 plus or minus 2.9959`. A test whose standard error is three cannot
reject anything, and calling that consistent would repeat the
absence-of-evidence error this paper criticises elsewhere. **It is not
determined.**

### A second seam, found by asking where else the coordinate degenerates

The probability coordinate is defined through whichever outcome has the larger
absolute value. Where the two absolute values are equal the definition switches
and the coordinate jumps to its own negative. **That is a second discontinuity,
strictly inside the region this paper has otherwise treated as ordinary
interior.**

It is real and it is large. Across the switch the probability coordinate moves by
about `0.87` to `0.98` on average, and 3,401 analysed rows lie within twelve
percent of it.

We tested whether risk sensitivity jumps there too. Estimating freely in bands of
the log ratio of the two absolute outcomes, the jump is
`-0.1003 plus or minus 0.3216`, **0.3 standard errors**. No jump is detected.

**The honest reading is bounded rather than negative.** The band immediately above
the switch holds 326 rows and the comparison has a standard error of `0.32`. That
rules out a jump of the size seen at the first seam, `0.86`, and does not rule out
one half that size. **The second seam is benign for risk sensitivity as far as we
can tell, and we cannot tell very far.**

---

## 10. A measured boundary penalty, in the framework that predicted one

The seam this paper reports is not a new phenomenon. It is an instance of one
that Volume 1 of this series already defines, and the contribution here is a
measurement rather than a mechanism.

**What the framework already says.** `geometric-methods` Chapter 6 builds
pathfinding on decision manifolds, and Definition 6.1 gives the edge weight of the
decision complex as a smooth part and a discontinuous part,

    w(a -> b) = Mahalanobis distance from a to b
              + sum over k of beta_k times an indicator that boundary k is crossed

Section 6.1.2, "The Boundary Discontinuity Problem", states the difficulty
squarely. The decision spaces have discontinuous cost functions, a path crossing a
boundary incurs an additional cost that no smooth distance function can predict,
and Section 6.1.3 concludes that even a perfectly calibrated smooth heuristic
remains inadmissible in their presence. Section 6.4.3 tabulates the boundary
types with their penalties, and one row of that table is the boundary this paper
measures.

| boundary | condition | penalty |
|---|---|---|
| sacred value | any dimension goes from positive to zero | infinite |

**A loss branch vanishing is exactly that condition.** The probability-weighted
negative part of a gamble goes from positive to zero, and the gamble changes kind.
The framework assigns an infinite penalty to such crossings for sacred dimensions,
meaning the edge is removed and no path may use it.

**What this paper supplies is the penalty, measured, in a domain where it is
finite.** Risk sensitivity is not a sacred dimension and the crossing is not
forbidden, so the penalty is large rather than infinite.

| crossing | measured discontinuity in risk sensitivity |
|---|---|
| the loss branch is eliminated | `0.8737 plus or minus 0.2056`, 4.2 standard errors |
| the gain branch is eliminated | `1.3390 plus or minus 0.2459`, 5.4 standard errors |

These are the first values of a boundary penalty in this programme that come from
data rather than from stipulation. Chapter 6's moral heuristic, `h_M(n)` as the
sum over boundaries of `beta_k` times the probability of crossing boundary `k`,
takes the penalties as inputs. They have been posited throughout. One is now
measured.

**Two cautions about that comparison.** The measured quantities are
discontinuities in the risk-sensitivity modifier, not in the edge weight of a
nine-dimensional complex, so they are penalties in the sense of the same
structure and not in the same units. And Chapter 6 notes at Definition 6.1 that
boundary penalties need not be symmetric, since crossing in one direction may be
penalised where the reverse is not. **We cannot test that here.** Our stimuli are
static gambles rather than transitions, so the two rows above are two different
boundaries and not one boundary taken in two directions.

## 11. What this adds to the boundary problem, and it is not good news

Section 6.1.2 says a smooth heuristic cannot predict a boundary penalty. This
paper reports a sharper failure, one that the chapter does not anticipate and
that bears on how the complex is coordinatised in the first place.

**If a stratum is parameterised by a normalised difference, the coordinate itself
degenerates at the boundary, and a smooth model fitted across it does not merely
miss the penalty. It manufactures structure that is not there.**

**Proposition.** Let `a` and `b` be non-negative and not both zero, and let
`d = (a - b) / (a + b)`. Then `d` equals plus one exactly when `b` is zero and
minus one exactly when `a` is zero. On the set where `b` is zero the gradient of
`d` vanishes, so any chart containing `d` drops rank there. And on that same set,
for any other coordinate `x`, the product `d * x` is identically `x`. **The two
columns are the same column.** A model fitted across both regions therefore lets
the coefficient on `d * x` absorb whatever `x` effect exists on the degenerate
set.

Verified here rather than asserted. The Jacobian of the coordinate map has rank
two on the mixed region and rank one on both unmixed regions, at four hundred of
four hundred random points in each.

**That is the whole story of this paper in one sentence.** A probability effect
living on gambles that cannot lose was read as a rotation-covariant chirality on a
plane, because on that set the product of the two coordinates is a relabelling of
one of them.

**The consequence for Chapter 6 is a chart-selection rule, not a correction.**
Definition 6.1 embeds the complex in a nine-dimensional space and takes the metric
from a precision matrix. Nothing in that construction requires any coordinate to
be a normalised difference. But the moment a dimension is built as a balance
between two non-negative magnitudes, benefit against harm, consonance against
dissonance, one claim against a competing claim, that dimension saturates exactly
where one magnitude is absent, which is exactly where Section 6.4.3 places a
boundary. **The chart degenerates precisely at the boundary the chart is supposed
to help detect.**

The rule that follows is short. Wherever a bounded balance coordinate is
introduced, ask what its endpoints mean. If they mean absence rather than
extremity, they are a stratum boundary in the sense of Section 6.4.3, the chart
must not be assumed to extend across them, and interaction terms built on that
coordinate are unidentified on the far side.

We audited the other volumes for this pattern and it has not spread to them in
code. A search of the ethics, aesthetics, law, cognition, reasoning and
observation repositories found no normalised-difference coordinate in use. This is
a guard for future work rather than a retraction of existing work.

**A second kind of information loss.** Section 6.4.2 motivates behavioural
friction by the Scalar Irrecoverability Theorem of Chapter 1, that scalar utility
at a single state discards all but one dimension. The degeneracy above is a
different loss and worth naming separately. It is not a projection from many
dimensions to one at a point. It is a chart whose rank falls on a subset, so an
open region of stimulus space is collapsed onto an edge of the coordinate square
and the coefficients fitted there describe the edge rather than the region.

## 12. What this says about paths and goals

Chapter 6 already contains the pathfinding consequences, and we restate only what
our measurements bear on.

**The crossing cost is not small, and it is now known for one boundary.** Section
6.5 defines the moral heuristic as a sum of penalties weighted by the probability
of crossing each boundary, and proves an admissibility condition for it. That
condition is stated in terms of the penalties. Supplying a measured penalty makes
the condition checkable for one boundary in one domain instead of assumed.

**A heuristic smooth across this frontier underestimates by about the full range
of the quantity it is estimating.** Risk sensitivity ranges over roughly one unit
across the whole plane, and the discontinuity at the frontier is `0.87` and
`1.34`. Section 6.1.2's claim that no smooth distance function can predict the
penalty is, in this domain, not a small correction.

**Our measurements say nothing about search.** We observe choices between two
gambles, not trajectories through a complex. Everything in this section is what a
measured boundary penalty implies for the machinery of Chapter 6, offered so the
two can be checked against each other, and none of it is a test of that machinery.

**The one thing we would want next is a transition.** Chapter 6's boundary
penalties are properties of edges, and an edge is a change of state. A design in
which the same participant faces a gamble before and after a branch is added or
removed would measure the penalty as the chapter defines it, directionally, and
would settle whether the asymmetry between our two frontiers is a property of the
boundaries or of the two populations of gambles that sit on either side of them.

## 13. Three gaps, closed

The first draft of this paper named three gaps. Closing them changed two of its
conclusions and confirmed a third.

**The loss stratum is thin, and it is thinner than trial counts suggest.** It
holds 4,146 trials over 251 distinct gambles, and the experience arm's 16,584
further trials fall on 239 of the same gambles. The effective sample for a
coordinate coefficient is the number of gambles, so **the second arm adds nothing
here**, and this is the one place in the paper where a four times larger dataset
buys no precision at all. Resampling the gambles, the probability slope is
`−0.3609` with interval `−0.5034` to `−0.2368`. It is determined, it mirrors the
gain side, and Section 9 is corrected accordingly.

**The low agreement between the quadratic and the free surface is real structure,
not cell noise.** A weighted agreement of `0.307` could mean the quadratic misses
most of the structure or merely that the cells are noisily estimated. The way to
tell is to simulate from the fitted quadratic, re-run the entire free-surface
estimate on the simulated choices, and see what agreement the quadratic scores
against itself. **If the quadratic were true it would score `0.930`**, mean of
twelve simulations with a standard deviation of `0.004`. The observed `0.307`
falls short by `0.623`, which is more than a hundred simulation standard
deviations. The misspecification is real and it is large.

**Separability is rejected, and the risk-sensitivity conclusions survive it.** The
model assumes the expected-value coefficient does not depend on position. Allowing
it to vary over the plane wins on **20 of 20 held-out splits by gamble**, with a
margin of `+0.001401 plus or minus 0.000132`, and the expected-value coefficient
turns out to depend strongly on the axis-distinguishing term, at
`−0.4289 plus or minus 0.0662`. So the assumption is false and the paper should
not have made it silently.

What matters is whether that contaminates the risk-sensitivity surface, and it
does not.

| term | assuming separability | allowing both to vary |
|---|---|---|
| `d * q` | −0.0293 | −0.0290 |
| `d^2 - q^2` | −0.6370 | −0.6020 |
| `d` | +0.3265 | +0.3160 |
| `q` | +0.2072 | +0.1948 |

Every conclusion in Sections 5 through 9 is unchanged. **A rejected assumption
that moves nothing is worth reporting precisely because the reflex is to assume it
moved something.**

## 14. Relation to the prior claims

**The original corner reading was right and its evidence was not.**
`RESULTS_d4_rotation.md` concluded that the fourfold product is a corner
phenomenon, resting on an interior estimate near zero. That estimate was pooled
over seventeen corner rows that dominated the likelihood, and dropping them moves
it to `+0.44`. The conclusion survives and the route to it does not. The correct
interior estimate is `−0.0303 plus or minus 0.0728`, and the reason the product
is a corner phenomenon is that at the corners it is not a product.

**The Klein four-group reading in `paper_03_fourfold_symmetry.md` should be
withdrawn.** The pattern lives exactly where the coordinate degenerates, and there
the group-theoretic content is empty. The rejection of the larger dihedral group
is unaffected, since it rests on a corner decomposition in which the
rotation-breaking component is significant at a chi-square of 75.4, but that
decomposition's chiral component is a probability effect in disguise.

**The axis-distinguishing term was there all along.** The earlier record reports
it at `+0.34` as the dominant rotation-breaking quantity. That was right in
substance, opposite in sign because it was pooled across the seam, and mislabelled
as a nuisance. It is the interior term.

---

## 15. Negatives, withdrawals and errors

Reported here rather than in a file nobody opens.

**A preregistration of ours was void.** `prereg-d4stability-v1` built its design
matrix by differencing the two options in the order the transcript declared them
while building its outcome as "took the riskier option". Those disagree on the
74.8 percent of rows where the second option is riskier. Reorienting improved the
fit by 2,675 log-likelihood units and flipped the headline estimate from `−0.1775`
to `+0.2506`. Every check the registration carried passed, because each tested a
component and the defect was in a relationship between two components. It was
caught by a stray fit returning a negative coefficient on expected value, which
says people choose against expected value and is a symptom rather than a finding.
The replacement carries a sign check as a void condition and an invariance suite
that is itself tested against the known defect.

**A claim of ours was withdrawn.** After the first corrected fit we reported that
two of the three symmetry-breaking terms were absent. Tested against a
negligibility band of 0.048, anchored on published CPC18 values because our own
point estimates had already been seen, **nothing was shown absent**. Every
interval is wider than the band. That was an absence-of-evidence claim.

**A hypothesis of ours was refuted.** We proposed that the second corpus took the
opposite sign because it collapses multi-branch lotteries into three columns.
Refitting on subsets gives `−0.1216` for all rows, `−0.0659` for two-outcome only,
`−0.1560` for multi-branch only and `−0.2314` for two-outcome and unambiguous. The
sign stays negative and the subsets disagree in no consistent direction.

**A test of ours was mis-sized and replaced before sealing.** The first version of
the registered statistic used the plain standard deviation of the fold estimates
and had a size of 0.110 against a nominal 0.05, because folds split by scale
differ in precision where random folds do not. It was replaced by the studentised
form, whose size is 0.020.

**The loss half of the fourfold pattern IS established, and an earlier draft of
this paper said otherwise.** That draft quoted `−0.1430 plus or minus 0.1196`, a
coefficient conditional on a quadratic probability term being in the same model,
and read its overlap with zero as the linear slope being undetermined. Those are
different quantities. Fitted as a slope, with uncertainty from resampling the 251
distinct pure-loss gambles, the probability slope is
**`−0.3609`, 95 percent interval `−0.5034` to `−0.2368`**, excluding zero. The
detection limit at that sample is about `0.20` and the slope is `0.36`.

So the probability slope is `+0.3372` among gambles that cannot lose and
`−0.3609` among gambles that cannot win. **Mirror images, both determined.** That
is the fourfold pattern, and this corpus supports both halves of it.

The stratum remains the thinnest part of the corpus. It holds 4,146 trials over
**251 distinct gambles**, and the experience arm's 16,584 further trials fall on
**239 of those same gambles**, so they add trials and not information about a
coordinate coefficient. A gap of this kind cannot be closed by more subjects.

**The designed grid we built should not be run as specified.** It was constructed
to place stimuli at chosen intermediate angles so a quadratic could be estimated
cleanly. Estimating a misspecified model cleanly is not progress.

---

## 16. Conclusion

A coordinate whose endpoint coincides with a categorical change in the stimulus
will manufacture structure there. The gain and loss axis used throughout this
line reaches its endpoints exactly on gambles with no loss branch and gambles
with no gain branch, and on those sets the product of the two coordinates is not
a product. A probability effect among gambles that cannot lose therefore presents
as a rotation-covariant chirality whenever it is pooled with the interior, and
that is where the chirality came from.

Inside the genuinely two-dimensional region the chirality is absent on twenty one
independent lines and the leading term is the one that tells the two axes apart.
The two regions do not join smoothly. Risk sensitivity diverges as a gamble
becomes barely mixed and reverses when the last opposite branch is removed.

The fourfold pattern is not four independent facts, and it is also not a rotation.
Its solid half is that risk sensitivity rises with probability salience among
gambles that cannot lose. That is one fact, and it is worth more than a group.

---

## Reproduce

All scripts in `d4stability/analysis/` unless noted. Run on Atlas, never on a
laptop, with BLAS pinned to one thread per worker.

    stability_rows_v2.py       build the corpus, orientation guard asserted
    pipeline_invariants.py     the invariance gate, including its self-test
    d4stab_fit_v2.py           the registered confirmatory fit
    d4stab_grade_v2.py         the grader, which holds every bar
    seam_covariates.py         rebuild the option parameters, assert alignment
    seam_analysis.py           the seam, the regions, the free surface
    experience_arm.py          the 382,992 decisions from experience
    refine_structure.py        the free surface and the equivalence tests
    cross_corpus_regimes.py    five corpora, CPC18 at the trial level
    cluster_bootstrap.py       gamble-clustered uncertainty
    robustness.py              held out, model form, participant halves
    c13k_two_outcome.py        the multi-branch hypothesis
    stratification_theory.py   rank, regularity, frontier, second seam
    close_gaps.py              loss stratum, surface calibration, separability

Registrations and run records are in `d4stability/`, with the full account of the
seam in `d4stability/SEAM.md`.
