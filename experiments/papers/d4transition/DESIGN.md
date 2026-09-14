# Transition study design. Measuring a boundary penalty as an edge property

*Design, 2026-09-13. Not registered and not run. Written so it can be registered
without further design decisions.*

---

## 1. What this measures, and why nothing already collected can

`geometric-methods` Chapter 6, Definition 6.1, gives the edge weight of the
decision complex as

    w(a -> b) = d_M(a, b) + sum over k of beta_k * 1[boundary k crossed going a to b]

**A boundary penalty is a property of an edge.** An edge is a change of state. The
chapter notes at that definition that boundary penalties need not be symmetric,
since crossing in one direction may be penalised where the reverse crossing is
not, and gives selling stolen goods against buying them as the example.

`paper_04` measured a discontinuity of `0.8737 plus or minus 0.2056` where a loss
branch is eliminated and `1.3390 plus or minus 0.2459` where a gain branch is. It
could not measure an edge. Its stimuli are static gambles presented one at a time,
so those two numbers are **two different boundaries compared across two different
populations of gamble**, not one boundary taken in two directions. Whether the
asymmetry Chapter 6 anticipates exists is untested, and no reanalysis of that
corpus can test it.

This design tests it.

---

## 2. The identification result, which is the reason the design works

Present the same ordered pair of states in both directions to the same
participant. Because the Mahalanobis term is symmetric,

    w(a -> b) - w(b -> a) = sum over k of beta_k * ( 1[crossed going a to b] - 1[crossed going b to a] )

**The difference of the two directions cancels the metric exactly.** Whatever the
precision matrix is, however badly it is estimated, and whatever the smooth
structure of the space, it contributes the same amount to both directions and
subtracts out. What remains is the directional part of the boundary penalty and
nothing else.

This is the whole reason to run a paired bidirectional design rather than measure
the two directions on separate stimuli. It removes the need to estimate a metric
at all, and it removes every confound that acts symmetrically on the pair.

**It does not remove confounds that act asymmetrically.** Status quo bias,
endowment effects and loss aversion over the transition itself are all
asymmetric, and would produce a direction difference on pairs that cross no
boundary at all. Section 5 is how that is handled, and it is the part of the
design that decides whether the study is worth running.

---

## 3. Arm A, outcome boundaries

The boundary is the presence of a loss branch, which is the crossing `paper_04`
measured statically.

Participants hold a position with a described outcome distribution. On each trial
they are offered a switch to a different position, at a stated price, and accept
or decline. Price is titrated to an indifference point.

Four state types, all two-outcome and all with equal expected value by
construction.

| label | description | stratum |
|---|---|---|
| `G` | outcomes all non-negative | no loss branch |
| `M` | one positive and one negative outcome | mixed |
| `G'` | a second state with all outcomes non-negative | no loss branch |
| `M'` | a second mixed state | mixed |

Three pair types, each presented in both directions.

| pair | crossing | expected direction difference |
|---|---|---|
| **`G` against `M`** | acquires or sheds a loss branch | the boundary penalty |
| **`G` against `G'`** | none, both unmixed | **control** |
| **`M` against `M'`** | none, both mixed | **control** |

**The two control pairs are the instrument, not a nicety.** They measure the
direction difference that exists when no boundary is crossed. The estimand is the
excess of the crossing pair's direction difference over the controls', and a
design without them measures status quo bias and calls it a boundary penalty.

---

## 4. Arm B, permission boundaries

The motivating case is an agent whose authorisation is elevated, after which
actions previously refused become available. In the language of Definition 6.1
that is not a move within the complex. **It is a change in which edges exist.**
Elevation makes edges with `beta = infinite` traversable.

That is a different object from Arm A and it is worth measuring separately
because the framework treats it the same way and it may not behave the same way.

Participants hold a board of actions, each with a stated payoff, each marked open
or closed to them. They may take the best action that is open. A trial offers a
move to another board, in one direction on one trial and the other direction on a
matched trial, so the Section 2 cancellation applies.

**The control is the part that had to be worked out, and it is what makes the arm
measure anything.** It cannot be a permission change that changes no permissions,
which is not a thing. It is **the same value gain delivered without the permitted
set changing**. With `a < b` two payoffs and `v` the gain under test,

| state | open | payoffs (A, B, C) | best open |
|---|---|---|---|
| `L0` | A, B | `a`, `b`, `b+v` | `b` |
| `L1` | A, B | `a`, `b+v`, `b+v` | `b+v` |
| `H1` | A, B, C | `a`, `b`, `b+v` | `b+v` |
| `H2` | A, B, C | `a`, `b`, `b+2v` | `b+2v` |

| pair | gains `v` by |
|---|---|
| `CROSS`, `L0` to `H1` | **opening C.** not one number on the board changes |
| `CTRL_LO`, `L0` to `L1` | raising `B`. `C` stays closed at the same number |
| `CTRL_HI`, `H1` to `H2` | raising `C`. nothing opens or closes |

**All three are worth exactly `v`, and only the first changes what is open.**

**A closed action is shown, not hidden.** If `C` were absent from `L0`, reaching
`H1` would look like a new option arriving, which is what `CTRL_LO` already does,
and there would be no boundary on the screen to cross. Part of what this measures
may then be a response to being refused rather than to the permission. That is
the construct. A participant who never saw the boundary would be the confound.

**Payoffs are certain, deliberately.** An earlier version of this section gave the
actions uncertain payoffs so that a permission would carry option value, and
reasoned from there that a rational agent pays for elevation and requires nothing
to give up a permission it never uses. That reasoning is sound and the design was
not, because valuing an option is harder than valuing a bonus, so a difference
between the crossing pair and the controls could have been a difference in
arithmetic rather than in permissions. With certain payoffs every pair is the same
sum and only the route differs. The elevation is never nominal either: the checker
requires the newly opened action to be the one the participant would actually
take, which is the opposite of the control this section once proposed.

**The prediction that separates this from Arm A** is that a permission boundary
should be more strongly asymmetric than an outcome boundary. What is measured is
the excess for the crossing pair over the mean of the two controls, the same
estimand as Arm A, so the two arms can be compared. They are compared
**standardised**, each divided by its own between-family spread, because Arm A
prices in multiples of a gamble's spread and Arm B in multiples of a permission's
gain and the raw numbers are not commensurable.

---

## 5. What the controls protect against, stated as the thing most likely to sink this

**The obvious confound is that people dislike switching.** If a participant
requires compensation to move in either direction, every pair shows a direction
difference and the crossing pair shows one too. A study that reported that as
`beta` would be measuring the endowment effect with extra steps.

The design handles it by subtraction and the registration must make the
subtraction primary.

    estimand = ( direction difference on the crossing pair )
             - ( mean direction difference on the two control pairs )

**The falsifier is that the controls are not zero and the crossing pair does not
exceed them.** If both come out equal, the correct report is that this design
measured a switching cost and found no boundary-specific component, and that
Chapter 6's asymmetry is not detectable by this route.

A second confound is that `G` and `M` differ in variance as well as in stratum. It
is handled by construction, matching the pairs on outcome standard deviation as
well as expected value, so the states differ in whether a loss branch exists and
as little else as can be arranged. Where matching is impossible the residual
difference is recorded as a covariate and reported, not absorbed.

---

## 6. Stimulus construction, and the coordinate rule this programme now has

States are constructed directly in outcome space as triples of a high outcome, a
probability and a low outcome. **They are not constructed by placing points in a
normalised-difference coordinate.**

`paper_04` Section 11 gives the reason. A coordinate built as a balance between
two non-negative magnitudes saturates exactly where one is absent, which is
exactly the boundary this study is about, so a design laid out in that coordinate
would place its crossing pairs at a point where the coordinate has rank one and
cannot distinguish the quantities being manipulated.

Matching requirements per pair, all verified in code before any data is
collected.

1. Equal expected value to within a declared tolerance.
2. Equal outcome standard deviation to within a declared tolerance.
3. For crossing pairs, exactly one of the two states has a negative outcome.
4. For control pairs, both states are on the same side.
5. No state has both outcomes equal, and no state has both outcomes zero.

---

## 7. Measurement

Indifference price by **multiple price list**, not by staircase and not by a
single accept or decline. `PILOT.md` Section 2 records why this changed. A
staircase needs about a dozen trials per cell, and a participant seeing three
families faces eighteen cells, which is more than two hundred trials before any
redundancy. A price list gives the same indifference point in one screen of
eleven rows.

Prices are set as fractions of the family's own spread rather than in absolute
units, because a family at a stake scale of five and one at eighty would
otherwise be incomparable and the between-family variance would be mostly a
variance in units.

A list with more than one switch is non-monotone and is the analogue of a
staircase failing to converge. It counts against the V3 budget of Section 10.

Direction order is randomised within participant and counterbalanced across
participants, so an order effect cannot align with a direction.

The two directions of a pair are separated by at least four intervening cells, so
that the second is not answered by recalling the first.

---

## 8. Predictions

To be written into a grader before any data is collected, with every threshold in
that file and nowhere else.

- **P1, a boundary penalty exists.** The crossing pair's direction difference
  exceeds the control mean by more than a bar set from the pilot's own noise.
- **P2, it is asymmetric.** The crossing pair's direction difference is non-zero
  in a declared direction, which is the question `paper_04` could not reach.
**P3 was here and has been removed.** It required Arm B's excess to exceed Arm
A's, each standardised by its own between-family spread. Arm B is built end to
end and is **not registered in v1**, because collecting it needs its own pilot and
roughly doubles the sample, and that decision has not been taken. The grader does
not score Arm B. Its numbers, if supplied, are reported unregistered and ungraded.

Reported separately. **No composite verdict.**

---

## 9. Power, and the counting rule this programme learned the hard way

**The effective sample is the number of distinct stimulus pairs, not the number of
trials.** `paper_04` Section 8 found that CPC18's 26,467 trials are 137 distinct
gambles at about 102 subjects each, and that resampling gambles inflated a
standard error by four and a half times and turned a confident estimate into an
interval containing zero. Section 13 found that a four times larger arm added no
precision because it fell on the same 251 gambles.

So the design is sized in pairs first.

**Stage one, a pilot**, specified in full in `PILOT.md`. 60 participants, 30
families, 3 families each. Its only purpose is to estimate the variance
components of the per-family excess, and it emits a variance decomposition and
nothing else. **It does not compute the mean excess**, which is the estimand, and
the analysis script is written so that it cannot. No hypothesis is tested and no
bar is set from it beyond the noise scale.

**Stage two** sizes the confirmatory study for a declared effect, expressed as a
multiple of the pilot's between-pair standard deviation rather than in absolute
units, because a bar in absolute units measures its own tolerance.

Both stages resample **families**, not pairs and not trials, for every interval.
The three pairs of a family share states and are not independent. Held-out splits,
if any, split by family. `build_stimuli.py` reports 160 families on 35 distinct
shapes, and the shape count is the conservative effective sample.

---

## 10. Void conditions

Written into the grader as conditions, not as things to notice.

- **V1.** Price must move choice in the expected direction. If paying more makes
  acceptance more likely, the instrument is inverted and the run is void. This is
  the analogue of the sign check that `prereg-d4stability-v1` lacked and that
  would have caught its defect in one second.
- **V2.** The pipeline invariance suite must pass, including a self-test that it
  rejects a deliberately mislabelled direction. A gate never shown to reject
  anything is decoration.
- **V3.** Staircases that fail to converge by their declared stopping rule are
  excluded by a rule fixed in advance, and the excluded count is reported.
- **V4.** Matching tolerances in Section 6 must hold on every delivered pair.

---

## 11. What this design cannot settle

**It measures a penalty for one boundary in one domain.** Chapter 6's table has six
boundary types and this addresses the structure of one of them.

**Arm B is an analogue and not the medical case.** A laboratory permission is not
a clinical authorisation and the stakes are not comparable. If the asymmetry
appears here it is evidence that the structure is real, not that its magnitude
transfers.

**It cannot separate a boundary penalty from a boundary-shaped preference.** If
people treat the acquisition of loss exposure as categorically different from its
magnitude, this design will measure that, and whether to call it a penalty in the
edge weight or a feature of the utility is a modelling choice the data does not
force.

**It says nothing about search.** Chapter 6's object is a path. This measures one
edge.

---

## 12. Order of work

1. Construct the pairs and verify every matching requirement in code.
2. Write the invariance suite and its self-test. Run it.
3. Write the grader with the void conditions of Section 10.
4. Run the pilot. Estimate the between-pair noise. Nothing else.
5. Set the bars from the pilot noise, seal, sign, register.
6. Run the confirmatory study.
7. Grade with the sealed grader, and report the controls beside every estimate.
