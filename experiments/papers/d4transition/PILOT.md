# Pilot protocol. Measuring one number and refusing to measure anything else

*Protocol, 2026-09-13. Not registered and not run. To be sealed before collection.*

---

## 1. The one thing this measures

Every bar in `grade_transition.py` is a multiple of the between-family standard
deviation of the excess. The multipliers are already fixed. **The scale is not
known and this pilot exists to measure it.**

That is the whole purpose. The pilot tests no hypothesis, reports no estimate of
the boundary penalty, and its output is three variance components and nothing
else.

**The discipline is structural rather than intentional.** `pilot_analysis.py` will
compute the per-family excess, because a variance decomposition needs it, and
will emit only the variance components. It will not write the mean excess to its
output, to the console, or to any file. A protocol that relies on the analyst not
looking is not a protocol.

---

## 2. Why a price list and not a staircase

The design document said staircase. On working out the trial load that is wrong.

A staircase needs about a dozen trials per cell to converge, and a participant
seeing three families faces eighteen cells, which is more than two hundred trials
before any redundancy. A multiple price list gives the same indifference point in
one screen.

**Each cell is one price list of eleven rows.** The participant marks accept or
decline at each price. The switch point is the indifference price. Eleven rows,
eighteen cells, one hundred and ninety eight binary responses per participant,
which is about twenty five minutes.

The staircase's starting-point bias is handled by the list being presented whole,
so there is no adaptive path and no order within a cell to bias.

---

## 3. Prices, in units of the state's own spread

Prices are set as fractions of the standard deviation of the states in the family,
which is the same for all four states by construction. **Absolute prices would
make a family with a stake scale of five and one with a scale of eighty
incomparable**, and the between-family variance would then be mostly a variance in
units.

The eleven rows of every list are

    -3.0, -2.1, -1.5, -0.9, -0.45, 0, +0.45, +0.9, +1.5, +2.1, +3.0

times the family's spread. A negative price is a payment to the participant for
making the switch, a positive price is a charge. The list is presented in a fixed
ascending order and the direction of the effect is therefore known in advance,
which is what V1 checks.

**This range was chosen by measuring, not by widening until it looked safe.**
`price_range_sweep.py` puts six candidates against a planted truth and reports
both failure modes, since they pull in opposite directions. Too narrow and the
tails of the crossing cell fall off the end and the components are attenuated.
Too coarse and every price is read to the nearest wide interval and the
components are inflated by quantisation.

| candidate | rows | worst cell at an edge | family bias |
|---|---|---|---|
| the provisional plus or minus one | 11 | 0.382 | **−41.5 percent** |
| plus or minus two | 11 | 0.081 | −13.6 percent |
| **plus or minus three, adopted** | **11** | **0.011** | **−6.9 percent** |
| plus or minus three, hybrid | 17 | 0.011 | −5.4 percent |
| plus or minus four, hybrid | 17 | 0.000 | −3.1 percent |

read at **one and a half times the assumed noise**, because the real noise is
unknown until this pilot measures it and a range chosen with no margin is a range
that fails on contact with data.

**Tripling the span over the same eleven rows costs nothing.** It is still 198
rows per participant. The quantisation penalty that made widening look expensive
does not bite, because the rows scale with the span, and the coarser grid costs
about three percent of bias where the censoring it removes was costing
twenty six. The denser seventeen-row grids buy under two further points for a
fifty five percent longer session and were rejected.

The per-cell check of Section 7 remains the guard. If the pilot's own data trips
it, the range widens again.

The recorded indifference price is the midpoint of the interval containing the
single switch from accept to decline.

**A list with no switch is recorded at the appropriate endpoint and flagged.** A
list with more than one switch is non-monotone, which is the analogue of a
staircase failing to converge, and is counted against the V3 budget.

---

## 4. Assignment

| quantity | value |
|---|---|
| families in the pilot | 30, drawn from the 160 to span shapes and scales |
| participants | 60 |
| families per participant | 3 |
| observations per family | 6 participants |
| cells per participant | 3 families times 3 pairs times 2 directions, 18 |
| rows per participant | 198 |

Thirty families gives twenty nine degrees of freedom on the between-family
component, so the standard deviation is estimated to about thirteen percent
relative precision. **That is adequate for a scale and it is stated so it is not
mistaken for precision about an effect.**

The thirty families are chosen to span the shape grid rather than at random, so
the scale is not estimated from one corner of the design. The selection rule is
fixed in code before collection and recorded.

---

## 5. Randomisation and separation

Direction order is randomised within participant and counterbalanced across
participants, so no order effect can align with a direction.

**The two directions of a pair are separated by at least four intervening cells**,
so the second is not answered by recalling the first.

Pair type order is randomised within family.

Family order is randomised within participant.

---

## 6. What the pilot outputs

A variance decomposition of the per-family excess into

    sigma_family        variation between families
    sigma_participant   variation between participants
    sigma_residual      everything else

and the implied standard deviation of a per-family excess at a stated number of
participants per family, which is the quantity the confirmatory bootstrap will
see.

**Reporting the decomposition rather than the raw spread is what makes the pilot
transferable.** The raw spread of per-family excess depends on how many
participants contributed to each family, so a pilot at six per family and a
confirmatory study at twelve would not share a scale. The decomposition lets the
scale be computed for whatever the confirmatory design turns out to be.

`pilot_scale_arm_<A|B>.json` records the three components, the implied scale, the design
they were measured under, and nothing else.

---

## 7. What would make the pilot itself a failure

Checked before any confirmatory study is designed. These are not predictions and
failing them means the instrument is fixed and the pilot repeated, not that a
result is reported.

- **The price slope.** Acceptance must fall as the charge rises, pooled across all
  cells, at a z of at least 3.0. This is V1 of the grader, checked here first
  because there is no point sizing a study around an instrument that does not
  respond to its own manipulation.
- **Non-monotone lists above twenty five percent.** The task is then too hard or
  the price range is wrong, and the range is adjusted and the pilot repeated.
- **A between-family component at or below zero.** The design then has no
  between-family variation to speak of at this sample, and the confirmatory study
  needs more families rather than more participants.
- **Floor or ceiling, checked per cell and not pooled.** If more than fifteen
  percent of lists in ANY cell type switch at the first or last row, the price
  range does not bracket indifference there and must be widened.

  **The pooled version of this check does not work, and building the analysis
  found out why.** Four of the six cells are controls, which sit near the middle
  of the price range by construction, so they dilute the statistic. In a
  self-test the pooled share was 3.7 percent, comfortably inside any budget,
  while the crossing pair's forward cell was censored 22 percent of the time and
  the between-family standard deviation came out at 0.228 against a planted
  0.300. **A pooled share of four percent concealed a twenty four percent
  attenuation of the very number the pilot exists to measure.**

  The crossing pair's forward cell is the one that carries the excess and it is
  therefore the one whose tails leave the range first. `pilot_analysis.py`
  reports the share for every cell type and the check applies to the worst.

---

## 7b. The failure that hits no edge

Section 7 lists failures that announce themselves. There is one that does not.

When the grid step where a switch lands is wide compared with the spread of
prices, the switch falls in the same interval whatever the family effect was, the
shared covariance that estimates the between-family variance collapses, and **the
scale comes out low with nothing censored.** It is the dangerous direction,
because every bar in the confirmatory study is a multiple of this scale, so an
attenuated scale makes the study easier to pass.

`pilot_analysis.py` measures the width of the interval each switch actually lands
in, takes the median, and reports it as `grid_step_median` with the
`resolution_floor` it implies. The check `resolution_ok` fails when the measured
spread is below that floor, and a pilot that fails it is not usable.

**The constant is measured, not chosen.** Holding the rows fixed and varying only
the planted spread, the recovered between-family standard deviation stays within
six percent of the truth while the step is up to about two and a half spreads
wide, then collapses to minus 35 percent at 3.8 and minus 60 percent at 5.0, with
nothing hitting an edge at any of them. The bar is set at two, inside the measured
knee. Self-test 7 plants a spread below the floor and confirms the check fires
while every other check passes.

This was found while choosing Arm B's price rows and applies to Arm A the same
way, which is why it lives in the analysis and not in an arm.

## 8. What the pilot must not do

**It must not compute or report the mean excess.** That is the estimand, and a
pilot that reports it has tested the hypothesis on data that will not be part of
the confirmatory sample and has spent the registration's credibility for nothing.

**It must not be pooled with the confirmatory data.** The confirmatory study
collects fresh participants. The pilot families may be reused, since the scale is
a property of the stimuli, but the observations are not.

**It must not be used to choose the multipliers.** Those are already fixed in
`grade_transition.py` and committed. If the measured scale makes the study
infeasible at any reasonable sample, the correct response is to say so and stop,
not to lower the bar.

---

## 9. Sequence

1. Fix the thirty-family selection rule in code. Run it. Record the families.
2. Seal this protocol and the selection.
3. Collect.
4. Run `pilot_analysis.py`. It emits `pilot_scale_arm_<A|B>.json`, named for the
   arm the responses declare, and nothing else.
5. Check Section 7. If any fails, fix the instrument and repeat from step 3.
6. Seal the arm's scale file.
7. Size the confirmatory study from the sealed scale and the fixed multipliers.
8. Register the confirmatory study. Only then collect it.

---

## 10. What this protocol cannot fix

**A price list measures a stated willingness to accept, not a decision.** If the
boundary penalty is a property of acting rather than of pricing, this instrument
will not see it, and no sample size repairs that.

**Three families per participant is few.** The participant component will be
estimated from sixty people each contributing three families, which is enough for
a variance component and not enough to say anything about individual differences.
Nothing in the confirmatory design should rest on the participant component.

**The scale is measured on these stimuli.** If the confirmatory study introduces
families outside the shape grid used here, the scale does not transfer to them
and the protocol must be repeated for the new range.

---

## 10b. Arm B

Arm B uses this protocol unchanged. The same 30 families, 60 participants, 3
families each, 18 cells, the same separation and counterbalancing, and the same
analysis. Two things differ and both are in Section 8.1 of the registration: a
cell shows a board of permitted and closed actions rather than a gamble, and the
price rows sit either side of the family's gain rather than either side of zero.

    python session_builder.py --arm B --write --html
    python roundtrip_check.py

**Arm B is not registered in v1**, so this pilot is Arm A's. Arm B's instrument
exists and running it would need its own pilot, because the scale is per arm and
the arms do not share a price unit: Arm A's rows are multiples of the gamble
spread, Arm B's are multiples of the gain. That is enforced rather than intended.
A response file declares its arm, `pilot_analysis.py` names its output for that
arm, and `grade_transition.py` refuses a scale whose arm does not match.

**What this pilot is for has narrowed.** Section 11 of the registration is sealed
and did not need it: the bar and the estimate share units, so the scale cancels
out of the power calculation. The pilot measures the RATIO `r` of participant and
residual variance to family variance, which says which row of the registered
table the study is in, and it runs the instrument checks below. It cannot move a
bar or the sample size. Both are sealed before it runs.

## 11. Running it

The instrument is built and its output is proven to be what the analysis reads.

    python build_stimuli.py                             # arm A, 160 families
    python build_stimuli_armb.py                        # arm B, 60 families
    python session_builder.py --arm A --write --html    # 60 sessions, all checks
    python session_builder.py --arm B --write --html    # 60 sessions, all checks
    python roundtrip_check.py                           # both arms into the analysis

`session_builder.py` emits `task/p000.html` through `task/p059.html` for arm A
and `task_armb/p000.html` through `task_armb/p059.html` for arm B. Each is
self-contained at about sixteen kilobytes, needs no server, and opens by double
clicking. The participant answers eighteen price lists and saves a JSON file at
the end, eleven rows per list in arm A and twelve in arm B.

**The interface does not force a single switch point**, and that is deliberate.
The share of non-monotone lists is the instrument's own convergence diagnostic and
the grader's V3 budget is computed from it. An interface that enforced
monotonicity would destroy the measurement it is supposed to support.

Collect the saved files, concatenate their `records` into one document with
`"source": "human"`, and run

    python pilot_analysis.py responses.json

which writes `pilot_scale_arm_<A|B>.json` only if the source is human, and
`rehearsal_scale_arm_<A|B>.json` otherwise. `grade_transition.py` refuses any
scale not marked human, any scale reporting `usable` false, any scale whose arm
does not match, and a pre-split `pilot_scale.json` outright rather than reading
it as either arm.

**What remains is entirely people.** Ethics approval, consent, recruitment,
payment and the decision to run at all are the owner's, and nothing in this
directory should be taken as a judgement that the study is ready to put in front
of participants.
