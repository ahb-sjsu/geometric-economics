# Pilot: measuring what the rehearsal assumed, and nothing the claim uses

**Status: DRAFT, 2026-11-03.** Not sealed and not run. It needs people, ethics approval and money,
which are the owner's to arrange. The analysis code is written and passes its self-test. Rehearsal version 5
(22 cells) found that the rules needed changing. The five rule decisions it left open were taken on
2026-11-03, before any data, by Claude at the owner's instruction to proceed; the owner may overrule any of
them at the seal ("Decisions taken, 2026-11-03", below). The table they need is rehearsal version 6, complete
on 2026-11-04 (79 cells, REHEARSAL.md). The pilot rehearsal ran four times. Its first two runs each failed a bar
and changed the rule, and the fourth passed every bar as restated before it ran (sequence step 4). On
2026-11-04 the owner accepted the decisions and chose to count only the people the self-only flag does not
catch in the main tests. How cautious the rule may be is still open. The instrument is not built, because it
depends on the platform.

## What it is for

The rehearsal's power rests on person-level ranges that were chosen, not measured (`rehearsal.py`,
`draw`). The pilot measures them in real people and checks the instrument.

- **It puts the study in one row of a power table.** The table is computed and sealed before the pilot
  runs. The pilot only says which row applies, and the main study's sample size follows from the row
  by a sealed rule. This is the order the transition study settled on (`../d4transition/PILOT.md`).
  Freezing first means nothing the pilot measures can reach the margin, a model, the claim or the
  sample size except through a rule written in advance.
- **It checks the instrument.** Two-attribute lotteries, a charity that really receives money, and 140
  choices have not yet been put in front of anyone.
- **It checks that the stimuli are aimed right.** Block R and the calibration lotteries must straddle
  people's indifference points, or the calibration set cannot measure `P` and `κ`.

**The pilot can end the study.** At n = 120 the claim passed in 94% to 98% of simulated studies if
cost behaves like distance (`κ = 1`), and in 30% to 34% if it behaves like squared distance (`κ = 2`)
(rehearsal versions 3 and 4). Nothing yet says where people are. If the pilot puts the population `κ`
near 2, no n in the table reaches adequate power, and a null would not be informative (DESIGN.md, the
population `κ`). Forty people can show that before 240 are paid.

**It tests no hypothesis.** It never reads a choice that H1 to H4, MF1, MF2 or SH1 to SH3 use. Its
estimates are design inputs, not findings about preferences.

## What the rehearsal assumed, and what the pilot reads instead

| Quantity | Rehearsal (`rehearsal.py`) | Pilot statistic | Trials |
|---|---|---|---|
| Risk attitude at the ideal | `κ` exactly 1 (GEO1) or exactly 2 (GEO2); version 6, 0.5 to 2 | the lottery-choice rate at the ideal, read against simulated pilots (the rule); the population median `κ` from `hier.py`, reported | R, S calibration |
| Choice noise | median abs logit over block R, per person, log-normal around 1.5 (sd 0.35 on the log scale) | agreement between a block R choice and its repeat | R, PR |
| Weight on the charity | `sqrt(P22/P11)` from U(0.25, 1), so everyone trades the two off | the share who never trade toward the charity (`P` of rank one); the share who always do | R, PW |
| Metric correlation | `P12/sqrt(P11 P22)` from U(−0.6, 0.6) | GEO fitted per person; reported only | R, S calibration |
| Lapses | U(0, 0.06) per person; every fitted model fixes 4% | attention-check failures | A |
| Side bias | N(0, 0.3) on the logit | each person's left-choice rate; reported only | all readable |
| A sure-thing rule | not simulated | the share who always take the sure amount at the ideal, and what they do when it is far worse than the lottery | S calibration, PS |
| Session length | about 35 minutes (DESIGN.md) | measured | timestamps |

PR, PW and PS are trials only the pilot has (below).

**Three of these move power most.**
- `κ`. At n = 120 and noise target 1.5 the claim passed in 96% of simulated studies at `κ = 1`, 74% at
  1.25 and 40% at 1.5, and not monotonically above that (The power table).
- The share of people whose `P` is near rank one, who weigh only their own points. GEO gives them no
  correlation attitude and no background dependence. Every model predicts them alike, so they dilute
  every comparison. In dictator games 36% of people give nothing, and about half as many when the
  recipient is deserving, as a charity is: just under a fifth (Engel 2011, pp. 589 and 594). Giving
  nothing at one point for one is an upper bound on ignoring the charity, and block R's high-ratio pairs
  give the charity two or three points per point given up. Before version 5 the rehearsal had no such
  people.
- Choice noise, which scales how detectable every effect is.

## What it must not do

The discipline is built in, as in the transition study. A protocol that relies on the analyst not
looking is not a protocol.

- **Read a test or secondary choice.** The instrument's export is split at collection into a readable
  file (calibration, check and pilot-only trials) and a sealed file (block S off the ideal, X, XC and
  SC). Response times on sealed trials go with them, since the time a hard choice takes says something
  about the preference. `pilot_analysis.py` refuses any input that carries a sealed trial, and says why.
- **Be pooled with the main sample.** Pilot participants are barred from the main study.
- **Move the margin, the models, the claim or the trial roles.** They are sealed before it runs.
- **Choose the row by judgement.** The rule below chooses it.

## Participants and instrument

**Participants.** 40 who meet the inclusion rule, from the population and platform the main study
will use. Recruitment continues until 40 qualify. The number who did not is recorded, because it sets
the main study's recruitment.

**Inclusion rule, the main study's too.** DESIGN.md had none. The main study also leaves out people flagged
as self only (DESIGN.md, Inclusion; the owner's decision of 2026-11-04). The pilot keeps them, since it
estimates their share.
- Finished the session.
- Passed the comprehension quiz within two attempts.
- Chose the dominated option in at most 2 of the 8 attention checks. The reference simulation (below)
  reports how often the rehearsal's simulated people would fail this. It should be near zero, so that
  the rule removes inattention, not noise.
  - **With stimulus version 4's checks it was not near zero under GEO** (2026-11-03, simulated people
    only). The rule excluded about 10% of simulated people under GEO1, GEO2 and EARLY, 18% to 20% at the
    noisiest rows (target 1.0) and 5% to 7% at the least noisy. Under RDU, CAG, ADD and IA it excluded 1%
    to 2% (reference, 400 simulated pilots per truth).
  - **It also selected on the metric.** Under GEO1 it excluded 26% of people whose metric correlation is
    below −0.2, 4% of those between −0.2 and 0.2, and under 1% of those above 0.2. A negative
    correlation makes the dominated option, 10 points worse on both attributes, close in value to the
    better one. No simulated metric ranks it higher, so these were noisy choices, not reversed
    preferences.
  - **Stimulus version 5 moves the checks** (decided 2026-11-03, below). The dominated option is now 40
    points worse on both attributes, at charity shortfalls of 50 to 60. Six candidate sets were scored
    first on 2,000 simulated people per truth and row. Pairs near the ideal did worse under `κ = 2`, whose
    cost is flat there.
  - **In the version 6 reference the selection is gone** (400 simulated pilots per truth and row). The rule
    excludes at most 0.45% of simulated people on average under any truth or row. Of people whose metric
    correlation is below −0.2 it excludes at most 1.3%, at the noisiest rows, and 0.3% under GEO1, against
    26% before. The checks enter no other simulated choice, so the move changes no number in the power table:
    two quick cells run on Atlas with the old and the new code gave identical claim records. Rerun on NRP,
    the version 5 cells moved by a study or two of 50, which floating point differing between machines
    accounts for (REHEARSAL.md).

**Comprehension quiz,** before block R. Four questions: what self points become, what charity points
become, how a lottery is resolved, and how many trials are paid. Someone who fails twice leaves with
the base payment, unless the ethics review sets otherwise.

**The instrument is the main study's, unchanged.**
- `stimuli.py` version 5, all 140 trials, the charity choice and the payment rule: one trial paid, a
  coin flip for lotteries, donations with published receipts.
- Block R first, then everything else interleaved, as DESIGN.md says. The order is shuffled afresh for
  each participant from a recorded seed, and `stimuli.py`'s `order` is one such shuffle. A single order
  would put the same trials late for everyone, so fatigue would line up with trial content.
- The export records, per trial, the stimulus id, the side chosen and the response time, and per
  participant the order seed, the charity, quiz attempts, start and end times and the debrief. It names
  the stimulus set and its hash, and declares `"source": "human"`.

**Pilot-only trials, after trial 140.** Twenty, about 5 minutes. Any of them can be the paid trial, so
they carry the same incentive.
- **PR, 8 repeats.** Two block R pairs from each tradeoff ratio, shown again with the sides swapped.
  Agreement with the first answer measures choice noise without a model.
- **PW, 8 wide-ratio pairs,** at block R's locations. Block R offers from 0.5 to 3 charity points per
  self point given up. Four pairs offer 6 (5 self points against 30 for the charity) and four offer a
  quarter (20 against 5). They tell someone who weighs the charity a little from someone who ignores
  it, and someone who weighs their own points a little from someone who ignores them.
- **PS, 4 lotteries at the ideal whose sure amount is 12 to 15 points worse than the lottery's expected
  value,** two per attribute. For any `κ` up to 4, expected cost favours the lottery in each. Someone
  who still takes the sure amount follows a rule that no `κ` describes.
- **Debrief.** Belief that the donation will be made (1 to 5), the payment rule (one multiple-choice
  question), difficulty (1 to 5), and how they chose (free text).

**Length.** About 42 minutes: DESIGN.md's 35 for the main trials, plus the extra trials and the
debrief.

**Why 40.**
- From 40 people a share near 0.3 is known to about ±0.14 (95%), and a rate near 0.1 to 0.15, such as
  the exclusion rate, to about ±0.1.
- For `κ`, the lottery-choice rate of about 30 unflagged people varies between simulated pilots by about
  ±0.012 (20th to 80th percentile), against steps of 0.015 to 0.02 between rows 0.25 apart (Reading the
  pilot). So 40 people place the study within a row or two, and the pilot rehearsal checks that the 80%
  limit covers as it should (sequence step 4).
- The cost is a third of the main study's at its smallest size, plus about 7 minutes per person.

## The power table, computed before the pilot

Rehearsal version 5 runs the main claim (H1, H2 and H3 at margin 0.005) on the version 4 stimuli, with
50 studies per cell at n = 60, 120, 160, 200 and 240.

- **GEO, 15 cells.** A population `κ` of 1, 1.25, 1.5, 1.75 or 2, crossed with choice noise of 1.0,
  1.5 or 2.0 (the median abs logit over block R). Every simulated person has the cell's `κ` and trades
  the two attributes off, as in GEO1 and GEO2. Those two are the cells (1, 1.5) and (2, 1.5), rerun out
  to 240.
- **The rank-one share, 2 cells.** The sample-size rule treats a share `s` of people who weigh only
  their own points as shrinking the sample to n(1 − s), because every model predicts them alike. Two
  cells test that, with `s` = 0.4 at `κ` = 1 and 1.5 and noise 1.5. If either misses by more than two
  standard errors, `s` becomes a dimension of the table before the seal.
- **Specificity, 5 cells.** EARLY, RDU, CAG, ADD and IA at noise 2.0 with lapses from U(0, 0.15). Tight
  intervals and the most misspecified lapse make this the row likeliest to give a false positive. The
  claim must pass in at most 1 of 50 studies at every n, the record version 3 had at margin 0 (one CAG
  study). If it passes more often, the design is not sealed as it stands, and the owner decides what
  changes.
- **Cost.** 22 one-CPU jobs on NRP. Version 3 took 23 to 214 minutes per truth at 200 people.

**Result (complete 2026-11-03).** The numbers are in REHEARSAL.md and `results/power_table_v5.json`.
- **Power falls fast with `κ` and with noise.** At n = 120 and target 1.5 the claim passed in 96% of
  studies at `κ = 1`, 74% at 1.25, 40% at 1.5, 30% at 1.75 and 40% at 2. At target 1.0 it passed in
  under 40% for every `κ` above 1.
- **It is not monotone in `κ`.** It is lowest around 1.5 to 1.75, and recovers at 2 for less noisy
  choosers: 66%, 38% and 72% at target 2.0 and n = 120. Rounding `κ` up is therefore not always the
  cautious choice ("Decisions taken", 3).
- **Specificity holds.** The five specificity cells passed in no study at any n.
- **The rank-one check misses.** With 40% of people of rank one, power at n = 120 was 58% at `κ = 1`
  and 4% at `κ = 1.5`, against the 86% and 34% that `n(1 − s)` predicts. So `s` becomes a dimension of
  the table before the seal, as the rule above requires. The direction was predicted before the run (REHEARSAL.md): the margin applies
  to the mean over everyone, which the rank-one people pull toward zero.
- Cells took 43 to 132 minutes each.

**Version 6 (complete 2026-11-04).** The decisions of 2026-11-03 need more of the table: 50 studies per
cell at n = 60, 120, 160, 200 and 240 (REHEARSAL.md, `results/power_table_v6.json`).
- The 22 version 5 cells, rerun. They reproduce version 5 to within a study or so of 50 (REHEARSAL.md).
- Rows at `κ` = 0.5 and 0.75, at the three noise targets: 6 cells.
- The share of rank-one people at 0.2, 0.4 and 0.6, at every row that reached 0.80 by n = 240 with nobody
  of rank one (`κ` = 1 at every target, 1.25 at targets 1.5 and 2.0, and 2 at target 2.0) and at the new
  rows: 35 cells.
- Every study scores the main claim twice: over every simulated person, as DESIGN.md registers it, and
  over the people the main study's self-only flag does not catch, recruited until there are n of them.
- A noisier row, target 0.7, at every `κ`, with shares at `κ` up to 1: 16 cells, added after the second
  pilot rehearsal found pilots noisier than every row (sequence step 4). 79 cells in all.

**Result.**
- **The rows below 1 have more power than `κ = 1`:** at target 1.0 and n = 120, 100%, 98% and 84% at `κ` of
  0.5, 0.75 and 1.
- **Who H1 to H3 count matters as soon as people ignore the charity.** At `κ = 1`, target 1.5 and n = 120,
  the claim over everyone passed in 96%, 88%, 58% and 10% of studies at shares of 0, 0.2, 0.4 and 0.6.
  Over unflagged people it passed in 96%, 100%, 90% and 96%. With nobody of rank one the two agree.
- **Specificity holds in both populations:** none of the five non-GEO cells passed in any study.
- **The version 5 cells moved by at most two studies of 50** when rerun (REHEARSAL.md).

## Reading the pilot

**Each model-free statistic is read against simulated pilots.** `pilot_analysis.py reference`
simulates pilots of 40 included people from the rehearsal's truths through the same 160 trials, recruiting
until 40 pass the inclusion rule, and computes each statistic the same way. The real value is read against that distribution, never against a number
chosen by hand, so the reference absorbs the statistic's own bias and spread.

**The rule.** Each quantity enters at its pessimistic 80% limit, so that over the pilot's sampling
error the main study has at least the tabulated power with probability about 0.8. For one quantity this is
Browne's result (1995): sizing a t-test from a one-sided 100(1 − γ)% upper limit of the pilot's standard
deviation reached the planned power in at least 100(1 − γ)% of simulated trials. Secondary sources
attribute the 80% level to him; the full text was not seen. With several quantities, each at its own
limit, the probability is not simply 0.8, and Browne does not cover it. The pilot rehearsal measures it
(sequence step 4). Perugini, Gallucci and Costantini (2014) apply the same idea to an effect size
("safeguard power"). The form below is version 6's, decided on 2026-11-03 ("Decisions taken").
- **`κ`.** `κ` enters as draws from its confidence distribution, not as one row.
  - The statistic is the lottery-choice rate at the ideal (the 24 calibration lotteries), over the
    pilot's people not flagged as self only, whom the table's rows do not contain. The reference has the
    same rate from 400 simulated pilots at each row. At each `κ` row, G is the share of those simulated
    pilots whose rate is at or below the pilot's, mixed between the two noise rows as power is. Higher `κ`
    means fewer lotteries taken, so G rises with `κ`, and the draws are its inverse at 500 evenly spaced
    levels (`kappa_belt`). The draw at level 0.8 is an 80% upper limit for `κ` by construction, with the
    statistic's own bias and spread in it, as for every other statistic here.
  - The rate falls steadily with `κ`: 0.54, 0.52, 0.50, 0.48, 0.46, 0.45 and 0.43 from 0.5 to 2 at target
    1.5. It hardly moves with noise, and a single pilot's spread (about ±0.012 between the 20th and 80th
    percentiles) is smaller than the step between rows, so it places `κ` to about a row.
  - Each draw takes the lower power of the two tabulated rows around it. A draw above 2 takes power 0,
    since nothing above 2 was simulated; one below 0.5 takes the lowest row.
  - n is chosen so that the 20th percentile of power over the draws reaches 0.80 (The sample size). When
    power falls as `κ` rises, this reads power at the 80% upper limit, as version 5's rule did; the
    self-test checks that. Version 5 found that power does not always fall: it is lowest around 1.5 to
    1.75 and recovers at 2 for less noisy choosers. Rounding a limit near 1.9 up to the 2 row would then
    claim more power than the 1.75 row has.
  - **Revised 2026-11-03, after the first pilot rehearsal** (sequence step 4). The draws first came from
    `hier.py`'s posterior for the population median `κ`. Its 80th percentile was at or above the true `κ`
    in only 45%, 38% and 50% of simulated pilots at `κ` = 1, 1.5 and 2, against the bar of 70% (83% at
    0.75). The posterior sat 0.1 to 0.2 below the truth, also in 25 pilots with nobody of rank one, and
    the posterior of the population mean did no better. Why is not known. `hier.py`'s `κ` is still
    reported, as DESIGN.md's secondary analysis, but the rule no longer reads it.
- **Noise.** At each `κ` row, the 20th percentile of the pilot's agreement on the repeats (bootstrap over
  people) is placed between the two noise rows whose simulated median agreement brackets it, and power
  is read linearly between them. At or above the least noisy row, that row is used, with no
  extrapolation. The pilot's agreement leaves out the people flagged as self only, whom the table's rows
  do not contain. If the pilot is noisier than every row, the table is extended by the same code before n
  is set.
  - Version 5's rule took the least noisy row at or below that percentile. The rows are far apart (median
    agreement 0.64, 0.70 and 0.75 at `κ = 1`, against a single pilot's 20th to 80th percentile of about
    ±0.02), so it dropped a full row of power about 80% of the time.
- **The rank-one share `s`.** A person is flagged as self only if they chose the self-favouring option in
  at least 18 of the 24 high-ratio riskless pairs: block R's 20 pairs at ratios 2 and 3, and the four
  ratio-6 pairs. People who trade the two off mostly give on these pairs. The one-sided 80% upper Wilson
  limit `q` of the flagged share is converted at each `κ` row with that row's simulated flag rates, taken
  at the same point between the noise rows as power, `s = (q − fpr) / (tpr − fpr)`, clipped to [0, 1].
  - In the version 6 reference (10,000 included simulated people of each kind per row), the rule flags 48%
    to 99% of rank-one people, fewest at `κ = 2` and the noisiest target. It flags 0.5% to 1.9% of people
    who trade off. Version 5's reference gave 61% to 97%. Its attention checks also excluded the noisiest
    rank-one people, the ones the flag misses.
  - The main study's flag, 15 or more of block R's 20 pairs, flags 52% to 99.5% of rank-one people and 1.2%
    to 4.2% of the others. It catches more of both than the pilot's rule, since the four ratio-6 pairs
    offer only 5 of one's own points, and rank-one people choose noisily there.
  - *Revised 2026-11-03, before any data.* The first rule required at least 38 of the 40 block R pairs and
    all four ratio-6 pairs. It flagged 1% to 43% of simulated rank-one people, depending on the row.
    Someone who ignores the charity still chooses noisily between amounts 5 to 15 of their own points
    apart.
  - The rates come from the rehearsal's model of a rank-one person (REHEARSAL.md, version 5). If real ones
    are more consistent, the correction overstates `s`, which errs toward a larger sample.

**The sample size.**
- For each n of 120, 160, 200 and 240, power at each `κ` row is read at the pilot's noise (above) and at
  that row's upper limit for `s`, linearly between the tabulated shares of 0, 0.2, 0.4 and 0.6.
  - The table has shares only at rows that reached 0.80 by n = 240 with nobody of rank one, and at the
    rows below 1. Elsewhere a share above 0 counts as power 0, and so does a share above 0.6. Both err
    toward stopping.
  - Version 5 read the row's power at n(1 − s) people instead. Its rank-one check showed that this
    overstates power badly (The power table, result).
- Over the draws of `κ`, as above, the 20th percentile of that power.
- n is the smallest with that percentile at least 0.80. It never goes below 120, the size at which the
  population `κ` and the crossing set were rehearsed.
- If none reaches 0.80, the study is not powered for the population the pilot found. The owner decides
  between running at 240, with the power stated in the registration, and stopping.
- Recruitment continues until n people meet the inclusion rule.
- **H1 to H3 count only the people the main study's self-only flag does not catch** (the owner's decision
  of 2026-11-04; DESIGN.md, Inclusion). The rule reads the table's power over those people
  (`power_unflagged`), and n counts them, so about n/(1 − f) are recruited when a share f is flagged.

**Reported, not used for the rule.** GEO's per-person ratio and metric correlation, the side bias, the
share who always trade toward the charity, the lottery-choice rate over everyone included, and `hier.py`'s
population median `κ`, each against its reference under the version 4 assumptions. If the row nearest
`hier.py`'s posterior median is two or more steps from the row the lottery rate points to, the report says
so before n is fixed. The rule still uses the lottery rate.

## When the pilot fails, and when the stimuli change

**Instrument gates.** These are judgements of feasibility, not tests. A failure means the instrument
is fixed and the pilot repeated with new people.
- At least 85% of those who pass the quiz finish.
- At least 80% pass the quiz within two attempts.
- At most 15% of finishers fail the inclusion rule.
- At least 75% rate the donation's reality at 4 or 5 of 5. Doubt about the donation lowers the
  charity's weight in a way the analysis cannot tell from preference.
- At most 10% of readable choices take under a second.
- The median time for the 140 main trials is at most 45 minutes. If it is longer, the crossing set is
  the first cut (owner's decision).
- Every bonus and every donation goes through as described.

**Targeting rules.** These change the stimuli, not the people. Each fires when its share is above the
97.5th percentile of its reference under every version 4 truth (the largest of the seven) and is at
least 6 of the 40. The first condition says the population differs from what the rehearsal assumed. The second says enough
people are affected to matter.
- **Self side.** People who never trade toward the charity in block R but do in at least 2 of the 4
  ratio-6 pairs. Block R gains a cell of ratio-6 pairs.
- **Charity side.** People who always trade toward the charity in block R but keep their own points in
  at least 2 of the 4 quarter-ratio pairs. Block R gains a cell of quarter-ratio pairs.
- **Risk.** People who take the sure amount in all 12 calibration lotteries of an attribute but take a
  PS lottery. That attribute's calibration gains lotteries with larger premiums.

Such a change adds only calibration trials of a kind the pilot already ran, so it needs no second
pilot. It does need a new stimulus version, a rerun of the rehearsal at every truth, a new table and a
new seal, all before the main study.

## Data and provenance

- **The raw export never enters the public repository.** It holds platform identifiers, which the split
  replaces with p001 to p040.
- **`split_pilot.py` writes the readable and the sealed file,** and records the sha256 of each in the
  pilot record (`split_record.json`). It also writes `id_map.json`, the only output with platform
  identifiers. It stays private, and it is what bars pilot participants from the main study.
- **The sealed file is opened only after the main study is graded.** Anything read from it then is
  reported as an unregistered sample of 40.
- **`pilot_analysis.py` writes `pilot_estimates.json` only when the input declares
  `"source": "human"`,** and `rehearsal_pilot_estimates.json` otherwise. It refuses an undeclared source
  and a stimulus hash that does not match `stimuli.py`.
- **The sample-size rule refuses estimates not marked human, and estimates that report a failed gate.**
  Its self-test puts a simulated file exactly where the rule looks and checks that the refusal names
  provenance, not a missing file. A refusal for the wrong reason proves nothing (the transition study
  again).
- **`pilot_estimates.json` carries aggregates only.** With the owner's OK it is published with the code.
  Per-person rows stay private unless the consent covers sharing them.

## Sequence

1. **Owner decisions** (below). The five rule decisions version 5 left open were taken on 2026-11-03 and
   accepted by the owner on 2026-11-04, with the population for H1 to H3 ("Decisions taken"). The owner's
   remaining decisions are under "Open decisions".
2. **Prior art.** DESIGN.md's list and the two references below are read before anything is sealed.
   Done 2026-11-03. The nearest study found, Berg and Rietz (2026), varies the link between one's own
   payoff and a peer's; none found pairs one's own payoff with a charity's, or varies the other's level
   (DESIGN.md, "Prior art").
3. **Build** (next section). A round trip sends the instrument's output through the split and the
   analysis, and checks that every cell lands where it should and nowhere else. An optional
   language-model pass over the wording (DESIGN.md, stage 2) fits here. It is not evidence about
   people.
4. **Pilot rehearsal:** simulated pilots of 40 through the whole chain, 100 per truth. The truths are
   `κ` of 0.75, 1 and 1.5 at noise target 1.5 and `κ = 2` at 2.0, each with a planted rank-one share of
   0.3. The bars below were set on 2026-11-03, before it ran (`pilot_analysis.py summarise`). It must
   show that
   - the 80% upper limit the rule reads for `κ` is at or above the true `κ`, the pilot's 20th percentile
     of agreement is at or below the truth's simulated median, and the upper limit for `s` is at or above
     the planted share, each in at least 70% of pilots. Each is nominally 80%; 70 allows for sampling
     error over 100 pilots;
   - of the pilots whose rule chooses an n, at least 80% choose one at which the truth's power is at
     least 0.80. Under a truth no n reaches, that means the rule must stop;
   - the analysis refuses a file carrying a sealed trial, by its own guard;
   - a simulated input writes only `rehearsal_pilot_estimates.json`, and the sample-size rule refuses it
     by the provenance guard;
   - a deliberately broken split that leaks test choices fails the round trip, since a gate never shown
     to reject anything is decoration.

   If a bar fails, the rule is revised and the pilot rehearsal run again before the seal. Version 5's
   first bar, that the rule picks the true row or the one above in at least 90% of pilots, belonged to the
   row rule and is replaced.

   *The second bar was restated on 2026-11-04, after the third run and before the fourth:* at most 20% of
   all pilots may choose an n at which the truth's power is below 0.80. In its first form, a share of the
   pilots that choose an n, any choice under a truth that no n reaches counts as a total failure, however
   rarely the rule makes it. The first form is still reported.

   **First run, 2026-11-03** (seeds 0 to 9, 100 pilots per truth, `κ` from `hier.py`). The `κ` bar failed:
   the limit covered the true `κ` in 83%, 45%, 38% and 50% of pilots at `κ` = 0.75, 1, 1.5 and 2. The
   agreement bar passed (85%, 77%, 77% and 81%), and so did the share bar (78%, 75%, 71% and 91%). The rule
   was revised ("Reading the pilot", `κ`) and run again on new seeds, against the same bars.

   **Second run** (seeds 10 to 19, `κ` from the lottery rate). The `κ` bar passed: 78%, 73%, 80% and 80%.
   The agreement bar passed: 86%, 74%, 85% and 82%. The share bar failed at `κ = 0.75`: 60% as scored.
   - In 17 of those 100 pilots the agreement fell below every noise row. The rule then has no noise position,
     computes no share limit and stops, asking for the table to be extended. The scoring counted those
     pilots as misses.
   - Among the 83 pilots with a limit, 72% covered. The limit's exact coverage there, from the binomial, is
     78.5%. Across both runs, pilots below every noise row were 0% to 17% per truth.
   - The cause is a gap in the table, not the share rule: target 1.0 was the noisiest row. Version 6 gained
     a target-0.7 row at every `κ`, with shares at `κ` up to 1 (16 cells, REHEARSAL.md), and the rehearsal
     ran a third time on new seeds, against the same bars.

   **Third run** (seeds 20 to 29, the lottery-rate `κ` and the target-0.7 rows). Every coverage bar passed:
   `κ` 79%, 72%, 77% and 80%; agreement 74%, 75%, 80% and 80%; share 82%, 82%, 90% and 92%. One pilot in
   400 fell below every noise row.
   - **The power bar, read with the table.** Where the truth was powered, every pilot that chose an n chose
     one with the power under the unflagged population; under the registered one, 8 of 9 at `κ = 1`. Under
     `κ = 1.5`, which no n reaches, 2 of 100 pilots chose n = 160 counting unflagged people, and 98
     stopped. The bar's first form counts that as a failure, and it was restated (above).
   - **A joint form of the rule** drew the three quantities together instead of putting each at its own
     80% limit. It stopped only a few points less often, and under the registered population at `κ = 1`
     only 7 of the 10 pilots that chose an n had the power. It was not adopted (`choose_n_joint`).

   **Fourth run** (seeds 30 to 39, the same rule, the restated bar). Every coverage bar passed: `κ` 75%,
   76%, 74% and 81%; agreement 80%, 76%, 84% and 88%; share 87%, 87%, 91% and 88%.
   - The restated power bar passed under every truth in both populations: at most 5% of all pilots chose
     an n without the power.
   - The first form failed three times. Twice it was one or two pilots under a truth no n reaches. The
     third is real: under the registered population at `κ = 1`, 5 of the 11 pilots that chose an n chose
     120 where the truth needs 160 (6 of 20 over runs 3 and 4). Pilots that clear a threshold most pilots
     miss have optimistic estimates.
   - Under the unflagged population, every chosen n at a powered truth had the power, in both runs.
   - **The cost of caution is large.** Where some n up to 240 has the power, the rule stopped in 79% and
     89% of pilots under the registered population (`κ` of 0.75 and 1), and in 29%, 68% and 100% under the
     unflagged one (`κ` of 0.75, 1, and 2 at target 2.0, which needs n = 200).
   - Each run is scored with its own code and reference against the final table in
     `results/pilot_rehearsal_v6_run1.json` to `_run4.json`. The simulated pilots themselves stay on Atlas
     (`/archive/experiments/correlation/pilot_reh_v6*`). Each quantity enters at its
     own 80% limit, so together they ask for more than 80% assurance. Ways to lower it are the owner's to
     weigh (Open decisions).
5. **Power table:** rehearsal version 6 on NRP (version 5 before the decisions of 2026-11-03).
6. **Seal** DESIGN.md (with the inclusion and sample-size rules), this protocol, the code and the table
   under a signed tag. Owner's OK.
7. **Ethics approval.**
8. **Collect** the pilot.
9. **Split, then analyse.** A failed gate sends the study back to step 8 with new people after the fix.
   A fired targeting rule sends it back to step 5 with the new stimuli, and to a new seal.
10. **Row and n** by the sealed rule, recorded under a signed tag with the hash of
    `pilot_estimates.json`.
11. **Main study.**

## What the pilot cannot settle

- **Whether GEO is right.** By design.
- **`κ` under another model.** The population `κ` means something only if GEO is right. Under RDU and
  CAG, version 3 read it as 1.64 and 1.86. A population that weighs outcomes pessimistically therefore
  lands in a high row, and asks for a large sample or ends the study. That errs safely, since under
  those truths the claim should fail at any n.
- **Transfer.** The estimates hold for the platform, population, point rate and charity list they were
  measured with. Change any of them and the pilot runs again.
- **The fixed 4% lapse.** If the included people lapse more than the rehearsal assumed, every fitted
  model is misspecified in the same way. The specificity cells run lapses up to 15% to check that this
  does not produce a pass.
- **The extra trials come last.** Fatigue makes the repeats a little noisier than block R itself, which
  errs toward a larger sample.

## Built (2026-11-03)

| File | What it does |
|---|---|
| `stimuli.py`: `pilot_extras`, `presentation`, `digest` | the 20 pilot-only trials (ids 140 to 159, role "pilot", their own random stream); one participant's order from their seed; the hash the export must declare. Version 5 (2026-11-03) moves the attention checks and nothing else: every other trial, and the order, is version 4's |
| `split_pilot.py` | the export into `readable.json`, `sealed.json`, `id_map.json` and `split_record.json`. Its docstring defines the export format the instrument must write |
| `pilot_analysis.py` | `reference`, `analyse`, `size`, `self-test`, `rehearse` (the pilot rehearsal) and `summarise` (its bars), with the guards above. `kappa_belt` turns the lottery rate into draws of `κ`; the rule itself is `choose_n`, which `summarise` applies to simulated pilots because `size` refuses simulated estimates |
| `rehearsal.py` | version 5 and 6 cells with `κ`, noise target, rank-one share and lapse ceiling as parameters (REHEARSAL.md); version 6 adds the main study's self-only flag and scores the claim over unflagged people too; `simulate` runs the same people through the pilot-only trials |
| `power_table.py` | the table from the version 6 runs, both populations, with the rank-one, specificity and version 5 reproduction checks |
| `hier.py` | also reports the posterior's draws of the population median `κ`, which the first pilot rehearsal's rule read. The rule now reads `kappa_belt`, and `hier.py`'s `κ` is reported |
| `submit_nrp.py` | the NRP driver, for rehearsal cells and for the pilot rehearsal (`--pilot-ref`, `--pilot-table`) |
| the instrument | not built: it depends on the platform. It must write the export that `split_pilot.py` documents |

**Self-test** (`pilot_analysis.py self-test`, on Atlas). 21 of 21 checks pass (2026-11-03, with the revised
`κ` rule; the 20 before it also passed with `hier.py` fitting `κ`). Each refusal is checked to name its own
reason. The four new checks:
- the `κ` rule gives version 5's n when power falls with `κ` (160 against 160, a made-up table);
- where power rises again at `κ = 2`, it stops, where rounding up would have chosen 160;
- power at a share of 0.3 lies between the 0.2 and 0.4 cells;
- at the `κ = 1` row's median lottery rate, `κ`'s confidence distribution has median 1.000 (80th
  percentile 1.187).
- The size rule refuses:
  - a missing file;
  - a simulated file put where it looks, for provenance;
  - `κ` draws not from the sealed belt;
  - a failed gate;
  - a fired targeting rule;
  - another table.
- The analysis refuses:
  - a readable file carrying a block S test trial;
  - an extra field;
  - an undeclared source;
  - another stimulus hash;
  - a reference built on other stimuli.
- The round trip puts every trial where its role says.
- A deliberately broken split that also routes the test trials to the readable file fails the round trip:
  1,920 misplaced trials, the 48 test trials of each of 40 simulated people (46 with version 4's attention
  checks, which excluded 6). The analysis's own guard refuses it too.

**The pilot rehearsal** (sequence step 4) ran three times. The first run fitted `hier.py` in every pilot
and ran on NRP, about 2.2 minutes per pilot. The later runs skip it, since the rule no longer reads it, and
took about 2 seconds per pilot on Atlas.
- **Smoke test** (version 5's rules). Two simulated pilots under `κ = 1`, noise 1.5 and a planted
  rank-one share of 0.3 took 283 s on one Atlas CPU, with a peak of 0.65 GiB.
  - Their upper limits for `s` were 0.45 and 0.36, both covering the planted 0.3.
  - Their `κ` rows were 1.25 and 1.
  - Both picked the noise row 1.0, one noisier than the truth. That jump is why the noise rule now
    interpolates ("Decisions taken").
- **Cost.** At about 2.5 minutes per pilot, 100 pilots per truth take about 4 hours. The run belongs on
  NRP, about 10 pilots per job.
- **Two faults on 2026-11-03, both fixed before any result was read.**
  - `reference` reused the name of its output path for a loop variable, so it wrote to file descriptor 0
    and failed with "bad file descriptor". The self-test caught it.
  - The first four pilot-rehearsal Jobs failed at once with "argument list too long". The command, which
    carries the code, passed Linux's 128 KiB limit on a single argument once `pilot_analysis.py` joined
    it. The drivers were stopped before any retry and the four failed Jobs deleted. The files now ride
    gzipped (72 KB), and `submit_nrp.py` refuses a command over 120,000 bytes.

**The reference** (`results/pilot_reference_v6.json`, on stimulus version 5): 400 simulated pilots per truth
and per row, now 28 rows, with exclusion by metric correlation and every pilot's lottery rate, which the `κ`
rule reads; and the flag rates of both self-only rules from 10,000 included simulated people of each kind
per row. It took about 10 minutes on one Atlas CPU, with a peak of 0.10 GiB. Each version reproduced the
one before it exactly and added to it: the first pilot-rehearsal run read `pilot_reference_v6_run1.json`
(21 rows) and the second `pilot_reference_v6_run2.json` (with the lottery rates). Version 5's reference
(`results/pilot_reference_v5.json`, 423 s) is kept as the record of the old attention checks.

## Decisions taken, 2026-11-03

Version 5 left five rule decisions open for the owner. On 2026-11-03 the owner asked Claude to proceed
with the next steps, and Claude took the five as below, before any data. Each was Claude's choice, with its
reason. On 2026-11-04 the owner accepted them, with the changes the pilot rehearsal forced (the `κ` statistic,
the target-0.7 row, the restated power bar): "go with your recommendations".

1. **The attention checks moved** (stimulus version 5; Participants, inclusion rule). As they were, they
   excluded people by the sign of the metric correlation under GEO. The alternatives listed were to keep
   the checks only as an instrument gate, which leaves inattentive people in the sample, or to exclude
   only at 5 or more dominated choices of 8. That still removes about a third of anyone choosing at random
   between options close in value (36%), so it would still select on the metric. Moving the checks
   removes the selection at its cause, and changes no simulated choice the claim reads.
2. **Rows at `κ` = 0.5 and 0.75.** Neither GEO's fit nor `hier.py` places `κ` below 0.5, so the two rows
   cover the model's whole range below 1. Before, such a population was read from the `κ = 1` row, with
   power there assumed, not simulated. A population that takes risks over shortfalls, as prospect theory reports for losses, would
   sit there.
3. **The `κ` rule reads the whole distribution of `κ`** (Reading the pilot). It equals version 5's rule
   wherever power falls with `κ`, and stays cautious where it does not. The alternative listed, the lowest
   power among the rows the central 80% interval spans, ignores how much of the distribution sits at each
   row, and it is more pessimistic than the 80% logic asks for. *Revised the same day, after the first
   pilot rehearsal:* the distribution is now the lottery-rate confidence distribution, not `hier.py`'s
   posterior, which sat too low at pilot size.
4. **The rank-one share is a dimension of the table,** at 0.2, 0.4 and 0.6, at every row that reached
   0.80 by n = 240 with nobody of rank one, and at the rows below 1. Version 5's own rule required the
   dimension once its check missed. Rows short of 0.80 at a share of 0 do not reach it with rank-one
   people added, so they need no share cells, and the rule reads them as power 0. The share of 0.6 is
   a margin. Engel's meta-study suggests that just under a fifth give a charity nothing at one point for
   one (above), but a pilot of 40 is noisy, and its upper limit enters converted by the flag's rates.
5. **The noise rule interpolates** between rows (Reading the pilot). It keeps the 20th percentile's
   caution without version 5's jump of a full row, which happened about 80% of the time.

**Which people H1 to H3 count: decided by the owner on 2026-11-04.** DESIGN.md had registered them over
everyone included.
- A person flagged as self only by the main study's rule (block R: the self-favouring option in at least
  15 of the 20 pairs at ratios 2 and 3) has a metric of rank one or close to it. Every model predicts
  such a person alike, so they dilute the margin and carry no evidence. DESIGN.md itself says they should
  show neither effect ("Who shows it").
- Restricting H1 to H3 to unflagged people, recruited until there are n of them, keeps the margin's
  meaning and most of the power that rank-one people cost. The price is paying the flagged people too.
- Version 6 scores the claim both ways in every simulated study, so the choice was made with the
  numbers. Claude recommended the restriction, and the owner adopted it ("go with your recommendations").
  DESIGN.md's inclusion rule now leaves flagged people out of the main study, and `pilot_analysis.py`
  reads the unflagged power. In the pilot rehearsal's third and fourth runs, every n the rule chose at a
  powered truth had the power under this population; under the registered one, 5 of the 11 chosen in
  the fourth run did not, at `κ = 1` (sequence step 4).

## Open decisions (owner)

- Population, platform, who runs it, and the ethics route.
- The charity list and the point rate. The pilot must use the main study's.
- The cap on n. The table runs to 240.
- Whether the crossing set stays (DESIGN.md).
- How cautious the sample-size rule is. With 40 people and each of three quantities at its own 80% limit,
  it stopped in a third to all of the simulated pilots whose truth some n up to 240 could power (sequence
  step 4). A larger pilot narrows the limits, a cap above 240 needs new table columns, and a lower
  assurance accepts more underpowered studies. Each costs money or certainty.
- Sealing.

## References (read 2026-11-03)

- Engel, C. (2011). Dictator games: a meta study. *Experimental Economics* 14(4):583–610,
  doi:10.1007/s10683-011-9283-7. Read in full: 36.11% of 20,813 reconstructed dictators give nothing
  (p. 589); with a deserving recipient, such as a charity, "only half as many dictators keep everything"
  and more than 20% give everything (p. 594, Fig. 4).
- Browne, R. H. (1995). On the use of a pilot sample for sample size determination. *Statistics in
  Medicine* 14(17):1933–1940, doi:10.1002/sim.4780141709. Abstract only. Kieser and Wassmer (1996),
  *Biometrical Journal* 38:941–949, analyse it.
- Perugini, M., Gallucci, M. and Costantini, G. (2014). Safeguard power as a protection against imprecise
  power estimates. *Perspectives on Psychological Science* 9(3):319–332, doi:10.1177/1745691614528519.
- DESIGN.md's prior-art list, read the same day, is in DESIGN.md.
