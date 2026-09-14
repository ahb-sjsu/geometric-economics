# prereg-d4transition-v1 — Is a Boundary Penalty Directional?

**Status:** v1, **DRAFT**. Not sealed, not signed, not run. **It cannot be sealed
until the pilot supplies the scale**, and Section 11 is the only section that
waits on it.

**Author:** Andrew H. Bond, San José State University.

**Relation to the programme.** `geometric-methods` Chapter 6, Definition 6.1,
gives the edge weight of the decision complex as a smooth Mahalanobis term plus a
sum of boundary penalties times an indicator that a boundary was crossed. The
chapter notes at that definition that boundary penalties need not be symmetric,
since crossing one way may be penalised where the reverse is not. **That asymmetry
has never been measured.** Section 6.5's moral heuristic takes the penalties as
inputs and they have been stipulated throughout.

`paper_04` supplied the first measured values, `0.8737 plus or minus 0.2056` where
a loss branch is eliminated and `1.3390 plus or minus 0.2459` where a gain branch
is. **Those are not an asymmetry.** They come from static gambles presented one at
a time, so they are two different boundaries compared across two different
populations of gamble, not one boundary taken in two directions. No reanalysis of
that corpus can do better.

This measures the edge.

> **What has been done before this draft.** The stimulus set, the instrument, the
> analysis, the invariance suite, the grader and the pilot protocol are written
> and self-tested. **No human data exists.** Every number quoted below from a
> simulation is labelled as such and none of it sets a bar.

---

## 1. The question

Does crossing a boundary in one direction cost more than crossing it back?

## 2. The identification result, which is why the design works

Present the same ordered pair of states in both directions to the same
participant. The Mahalanobis term is symmetric, so

    w(a -> b) - w(b -> a) = sum over k of beta_k times
                            ( 1[crossed going a to b] - 1[crossed going b to a] )

**The difference of the two directions cancels the metric exactly.** No precision
matrix has to be estimated, and every confound acting symmetrically on the pair
subtracts out with it.

It does **not** remove confounds that act asymmetrically, and the main one is that
people dislike switching. Section 4 is how that is handled and it is the part of
the design that decides whether the study is worth running.

## 3. Participants and assignment

Fixed after the pilot, from its variance components, and **Section 11 is where
those numbers go**. The pilot's own design is 60 participants on 30 families,
three families each, six participants per family.

The confirmatory sample is drawn fresh. **The pilot's participants are not
pooled** and its families may be reused, since a scale is a property of the
stimuli rather than of the people.

## 4. The design, and what the controls are for

Each family holds four states with **exactly** equal expected value and
**exactly** equal outcome spread, differing only in the probability of the high
outcome. Three pairs are drawn from it, all with the same probability separation.

| pair | crossing |
|---|---|
| `CROSS`, `G1` against `M1` | acquires or sheds a loss branch |
| `CTRL_G`, `G2` against `G1` | none, both unmixed |
| `CTRL_M`, `M1` against `M2` | none, both mixed |

**The controls are the instrument, not a nicety.** A participant who requires
compensation to move in either direction produces a direction difference on every
pair, crossing or not. A study reporting that as a boundary penalty would be
measuring the endowment effect with extra steps. So the estimand is

    excess = direction difference on CROSS
           - mean of the direction differences on CTRL_G and CTRL_M

and the registration makes the subtraction primary.

## 5. Stimuli

`build_stimuli.py`, 160 families on 35 distinct shapes, every match verified on
the **delivered rounded values** rather than on the unrounded ones. Worst expected
value mismatch after rounding `0.0090` and worst spread mismatch `0.0074`, against
tolerances of `0.02`.

States are constructed in outcome space and **never by placing points in a
normalised-difference coordinate**. `paper_04` Section 11 gives the reason. Such a
coordinate has rank one exactly at the boundary this study is about.

No state sits within `0.10` in log ratio of `|H| = |L|`, which is the second seam
`paper_04` Section 9 found, where the salience coordinate jumps.

The checker is run against five deliberately broken families and rejects each.

## 6. Instrument

This section states Arm A's instrument. Arm B's is Section 8.1 and uses the same
builder, the same schedule and the same checks.

A multiple price list of eleven rows per cell, at
`-3.0, -2.1, -1.5, -0.9, -0.45, 0, +0.45, +0.9, +1.5, +2.1, +3.0` times the
family's spread. Prices are in units of the family's own spread because absolute
prices would make families at different stake scales incomparable.

**The range was chosen by measuring both failure modes**, in
`price_range_sweep.py`, read at one and a half times the assumed noise. The
provisional range of plus or minus one censored the crossing pair's forward cell
and attenuated the scale by 26 percent. Tripling the span over the same eleven
rows costs nothing in participant time.

**The interface does not force a single switch point.** The share of non-monotone
lists is the instrument's own convergence diagnostic and V3 below is computed from
it. An interface enforcing monotonicity would destroy the measurement it supports.

`session_builder.py` builds the schedule and checks every constraint the protocol
states, rejecting seven deliberately broken schedules in Arm A and eight in Arm
B, the extra one being a dominated price row, which cannot arise where a pair
carries no value. Four of those checks were added with Arm B and apply to both
arms: prices must be the value difference plus multiples of the unit, the
stimulus must deliver the value difference the rows assume, the two directions of
a pair must be worth opposite amounts, and no row may be dominated. `roundtrip_check.py` runs both arms and
confirms that every cell each instrument delivers is read by the analysis, 1,080
delivered and 1,080 read in each.

## 7. The estimand

The mean over families of the per-family excess, with its interval from
**resampling families**.

**The clustering unit is the family and not the pair or the trial.** The three
pairs of a family share states. `paper_04` Section 8 is why this matters, where a
trial-level interval on a stimulus-level coefficient was too narrow by four and a
half times and turned an estimate containing zero into a confident one.

## 8. Arm B, permission boundaries

The auth-elevation case. In Definition 6.1's terms an elevation is not a move
within the complex, it is a change in **which edges exist**, making edges of
infinite penalty traversable.

**Its control is the part that had to be worked out and it is what makes the arm
measure anything.** Arm A's controls hold value fixed and differ only in whether a
loss branch exists. The analogue is not a permission change that changes no
permissions, which is not a thing. It is **the same value gain delivered without
the permitted set changing**.

A participant takes the best action they are permitted to take. With `a < b` two
permitted payoffs and `v` the gain under test,

| state | permits | payoffs | best |
|---|---|---|---|
| `L0` | A, B | `a`, `b` | `b` |
| `L1` | A, B | `a`, `b+v` | `b+v` |
| `H1` | A, B, C | `a`, `b`, `b+v` | `b+v` |
| `H2` | A, B, C | `a`, `b`, `b+2v` | `b+2v` |

| pair | gains `v` by |
|---|---|
| `CROSS`, `L0` to `H1` | **gaining a permission** |
| `CTRL_LO`, `L0` to `L1` | improving an action already permitted |
| `CTRL_HI`, `H1` to `H2` | improving an action already permitted |

**All three are worth exactly `v` and only the first changes the permitted set.**

**Payoffs are certain rather than risky, deliberately.** An earlier sketch gave
the actions uncertain payoffs so a permission would carry option value. Valuing an
option is harder than valuing a bonus, so a difference between the crossing pair
and the controls could have been a difference in arithmetic rather than in
permissions. With certain payoffs every pair is the same sum and only the route
differs.

**A closed action is shown, not hidden.** Every state displays every action with
its payoff and marks which of them the participant may take. If `C` were simply
absent from `L0`, then reaching `H1` would look like a new option arriving, which
is what `CTRL_LO` already does when `B` improves, and there would be no boundary
on the screen to cross. With the closed rows visible the contrast is exact.

| pair | what changes |
|---|---|
| `CROSS` | `C` opens. **Not one number on the board changes.** |
| `CTRL_LO` | `B` rises by `v`. `C` stays closed at the same number. |
| `CTRL_HI` | `C` rises by `v`. Nothing opens or closes. |

The cost of showing a closed action is that part of what is measured may be a
response to being refused rather than to the permission itself. That is the
construct. What would be a confound is a participant who never saw the boundary.

`build_stimuli_armb.py` produces 60 families and rejects nine deliberately broken
ones, including a state permitting an action with no payoff, which made an earlier
version of the checker crash rather than reject. **A checker that raises where it
should reject tells you nothing about the stimulus.**

The elevation must not be nominal, so the checker requires the newly permitted
action to be the one the participant would actually take.

### 8.1 The instrument, and the one price rule

`session_builder.py --arm B --write --html` emits 60 self-contained sessions into
`task_armb/`, on the same schedule as Arm A: 30 families, 3 per participant, 18
cells, direction separation at least five, counterbalanced deterministically.
`task_template_armb.html` presents each state as a board of actions with their
payoffs, marks each open or closed, states the best the participant may take, and
asks a price list. One builder serves both arms and the schedule checks are shared.

**Where the rows sit is one rule in both arms.**

    price row = (value difference) + (multiple) x (unit)

Arm A matches expected value across a pair, so its value difference is zero and
its rows straddle zero. Arm B's pairs are all worth `v`, so the forward rows sit
either side of `+v` and the backward rows either side of `-v`. **The value
difference cancels out of the estimand**, since the excess is a difference of
direction differences over three pairs that carry the same `v`, so this decides
only where rows are spent.

**The rows are not symmetric, and the reason is a mistake worth recording.** The
first version capped the multiples at plus and minus one, so forward prices ran
from zero to `2v`. A forward row below zero is dominated, because it pays the
participant to take the better state. **A forward row above `v` is the opposite
of dominated. It is the measurement.** Paying more than the money is worth is
exactly what a premium on a permission looks like, and the cap put a ceiling on
the premium the instrument could see. The round trip found it as 14 percent of
one cell hitting an edge. `price_range_armb.py` now sweeps the direction effect
alongside the noise, because the direction effect is the estimand and its size
cannot be assumed while choosing the range. The adopted rows run from zero to
`2.5v` going forward and mirror going back.

### 8.2 A failure that hits no edge

Choosing Arm B's rows turned up a defect in the pilot analysis that applies to
Arm A equally. When the grid step where the switch lands is wide compared with
the spread of prices, the switch falls in the same interval whatever the family
effect was, **the scale comes out low, and nothing hits an edge.** Censoring
announces itself and this does not. It matters because every bar in the
confirmatory study is a multiple of that scale, so an attenuated scale makes the
study easier to pass.

`pilot_analysis.py` now measures the step where switches actually land and
refuses a scale below the resolution the data can support. The constant is
measured rather than chosen: holding the rows fixed and varying only the planted
spread, recovery stays within six percent while the step is up to about two and a
half spreads wide and then collapses, to minus 35 percent at 3.8 and minus 60
percent at 5.0, with nothing censored at any of them. The bar is set at two. A
self-test plants a spread below it and confirms the check fires while every other
check passes.

The same exercise found that the pooled price-slope diagnostic was reading
**minus 3.8** on Arm B data where every participant responded to price correctly.
Arm B's forward and backward lists occupy disjoint ranges, so pooling raw prices
compared two ranges rather than measuring a slope. The price is now centred
within its cell before pooling, which leaves Arm A's value unchanged at 48.8 and
takes Arm B's to plus 45.9.

Invariant **I7** was added for the class of defect behind both: rename the
control pairs to the other arm's names and change nothing else, and the estimate
must be bit identical with no family lost. A fourth broken pipeline in `I0`
writes Arm A's control names into its own source, is correct on Arm A, and loses
all 60 families on Arm B without raising.

**What is still missing for Arm B is people.** Ethics approval, recruitment and
the decision to run are the owner's, as for Arm A. P3 remains NOT TESTED until
Arm B data exists, and the grader reports it as such rather than as a failure,
which was a defect found while writing this document and fixed.

**Arm B runs through Arm A's analysis unchanged.** The pair names are read from
the data rather than hardcoded, since a hardcoded lookup would have missed every
Arm B record and discarded the cell silently. What is enforced is structural,
exactly three pair types with exactly one crossing pair, and `check_both_arms.py`
confirms both arms recover all 30 families and that the rule rejects two pair
types, four pair types, and a set with no crossing pair.

## 9. Predictions

Bars live in `analysis/grade_transition.py` and nowhere else. The multipliers are
**already committed**, before any data.

- **P1, a boundary penalty exists.** The excess exceeds `2.5` times the pilot's
  between-family standard deviation.
- **P2, it is directional.** The excess is positive, meaning acquiring a loss
  branch costs more than shedding it, and beyond two of its own standard errors.
  The sign convention is declared in the grader so it cannot be chosen later.
- **P3, permissions differ from outcomes.** Arm B's excess exceeds Arm A's by
  `1.0` pilot sigmas. **Not testable unless Section 8 is resolved.**

Reported separately. **No composite verdict.**

## 10. Void conditions

Not predictions. A run failing any of these reports nothing.

| | condition |
|---|---|
| V1 | price must move choice in the **expected** direction, slope z at least 3.0 |
| V2 | the invariance suite passes **and its self-test passed** |
| V3 | at most 15 percent of price lists non-monotone |
| V4 | delivered stimuli still satisfy their matching tolerances |
| V5 | the two controls differ by no more than 3 pilot sigmas |
| V6 | at least 40 families on at least 20 shapes |
| V7 | no single family moves the estimate by more than a quarter of itself |

**V1 is the cheapest and would have caught the defect that voided
`prereg-d4stability-v1` in one second.** V2 is deliberately two-part, because a
suite that passes but whose self-test never ran licenses nothing. **V5 is the one
most likely to fire and is the design's own throat.** If the two control pairs
disagree, their mean is not a single quantity and the subtraction in Section 4 is
unjustified.

The grader is run against a clean result and nine broken ones and voids on each.
It is also checked that the predictions can fail, that a run with no penalty fires
F1, and that a penalty in the wrong direction is reported as such.

## 11. Power and size

**PENDING THE PILOT.** This section is the only thing standing between this draft
and a seal.

Every bar in Section 9 is a multiple of the between-family standard deviation of
the excess. **The multipliers are fixed and committed. The scale is not known.**
The pilot measures it and nothing else, emitting a variance decomposition from
which the scale at any number of participants per family follows.

**The pilot must not be used to choose the multipliers.** They are already
committed. If the measured scale makes the study infeasible at any reasonable
sample, the correct response is to say so and stop, not to lower a bar.

**A scale from simulated responses cannot be used.** `pilot_analysis.py` requires
responses to declare their source and writes a simulated run to a different
filename, and the grader refuses any scale not marked human. A rehearsal on
simulated data confirms the chain runs and its numbers set nothing.

## 12. Falsifiers

- **F1, the one that costs something.** If P1 fails, this design found no
  boundary-specific component beyond what the controls explain. The correct report
  is that it measured a switching cost and nothing more, and that Chapter 6's
  asymmetry is not detectable by this route. **That is to be reported as plainly
  as a positive.**
- **F2.** P1 passing while P2 fails is a penalty in the unexpected direction. It
  is a finding about the sign and must be reported as one, not folded into P1.
- **F3.** Any void condition fires and the run reports nothing.
- **F4, against ourselves.** This measures one boundary of the six Chapter 6
  tabulates, in one domain, with one instrument.

## 13. What this cannot settle

**A price list measures a stated willingness to accept, not a decision.** If the
penalty is a property of acting rather than of pricing, this instrument will not
see it and no sample size repairs that.

**It cannot separate a boundary penalty from a boundary-shaped preference.** If
people treat the acquisition of loss exposure as categorically different from its
magnitude, this design measures that, and whether to call it a penalty in the edge
weight or a feature of the utility is a modelling choice the data does not force.

**It measures one edge, not a path.** Chapter 6's object is a trajectory through a
complex. This is one crossing.

**The scale transfers only to these stimuli.** Families outside the shape grid the
pilot used are outside what it measured.

## 14. Freezing procedure

1. Resolve Section 8. Build Arm B, or seal with P1 and P2 and remove P3.
2. Run the pilot under `PILOT.md`. Check its own failure conditions.
3. Seal `pilot_scale.json`.
4. Fill Section 11 from the sealed scale and the committed multipliers.
5. Finalise this document, **then** hash the bundle.
6. Commit, sign the tag `prereg-d4transition-v1`, push.
7. Only then collect the confirmatory sample.
8. Grade with the sealed grader and **report the controls beside every estimate**.

## 15. Errors in this lineage, carried forward

From `prereg-d4stability-v2` Section 15, with the new ones added.

1. A coordinate reimplemented rather than imported. Fixed by importing.
2. A power simulation drawing one choice per row where the target was a rate.
3. Generative coefficients transcribed, five of six wrong. Fixed by reading them
   at run time.
4. A derivative-free optimizer on a convex problem.
5. A convergence threshold that measured itself.
6. A parser that dropped 91 percent of a corpus silently.
7. A second parser whose largest bucket was "not understood".
8. A test statistic whose size was 0.110 against a nominal 0.05.
9. **A design matrix oriented against its own outcome**, which voided
   `prereg-d4stability-v1`. Every component check passed and the defect was in a
   relationship between two components. V1 and the invariance suite exist because
   of it.
10. **A gate whose threshold measured its own noise**, inside the machinery built
    to prevent item 9.
11. **New here. A pooled diagnostic that hid the thing it was for.** A floor and
    ceiling share of 3.7 percent across six cell types concealed 22 percent
    censoring on the one cell carrying the estimand, and a 24 percent attenuation
    of the scale. Fixed by checking per cell and applying the bar to the worst.
12. **New here. A refusal for the wrong reason.** A rehearsal reported that the
    grader rejected a simulated scale. It had rejected a missing file. Fixed by
    placing the file where the consumer looks and confirming the refusal names
    provenance.
13. **New here. An untested prediction reported as a failure.** The grader scored
    P3 as FAIL when Arm B was absent. Fixed by reporting NOT TESTED, found while
    writing Section 8 of this document.

The generalisation holds and has been sharpened twice. **Every one of these was
caught by machinery rather than by care, except item 9, which was caught by
luck.** Items 11, 12 and 13 were caught by writing down what a check was for and
noticing it did not do that.
