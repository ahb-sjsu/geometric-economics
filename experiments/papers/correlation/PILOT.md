# Pilot: measuring what the rehearsal assumed, and nothing the claim uses

**Status: DRAFT, 2026-11-03.** Not sealed and not run. It needs people, ethics approval and money,
which are the owner's to arrange. The analysis code is written and passes its self-test. The power table
is rehearsal version 5, all 22 cells (see "The power table" and REHEARSAL.md). The table's own checks
call for two rule changes before the seal. The instrument is not built, because it depends on
the platform.

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
| Risk attitude at the ideal | `κ` exactly 1 (GEO1) or exactly 2 (GEO2) | the population median `κ` from `hier.py`; the lottery-choice rate at the ideal as a model-free cross-check | R, S calibration |
| Choice noise | median abs logit over block R, per person, log-normal around 1.5 (sd 0.35 on the log scale) | agreement between a block R choice and its repeat | R, PR |
| Weight on the charity | `sqrt(P22/P11)` from U(0.25, 1), so everyone trades the two off | the share who never trade toward the charity (`P` of rank one); the share who always do | R, PW |
| Metric correlation | `P12/sqrt(P11 P22)` from U(−0.6, 0.6) | GEO fitted per person; reported only | R, S calibration |
| Lapses | U(0, 0.06) per person; every fitted model fixes 4% | attention-check failures | A |
| Side bias | N(0, 0.3) on the logit | each person's left-choice rate; reported only | all readable |
| A sure-thing rule | not simulated | the share who always take the sure amount at the ideal, and what they do when it is far worse than the lottery | S calibration, PS |
| Session length | about 35 minutes (DESIGN.md) | measured | timestamps |

PR, PW and PS are trials only the pilot has (below).

**Three of these move power most.**
- `κ`, which takes the claim from 94–98% to 30–34% between its two rehearsed values. No value between
  them has been simulated.
- The share of people whose `P` is near rank one, who weigh only their own points. GEO gives them no
  correlation attitude and no background dependence. Every model predicts them alike, so they dilute
  every comparison. In dictator games about a third of people give nothing (Engel 2011; from memory,
  to check). The rehearsal had no such people.
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

**Inclusion rule, the main study's too.** DESIGN.md had none.
- Finished the session.
- Passed the comprehension quiz within two attempts.
- Chose the dominated option in at most 2 of the 8 attention checks. The reference simulation (below)
  reports how often the rehearsal's simulated people would fail this. It should be near zero, so that
  the rule removes inattention, not noise.
  - **It is not near zero under GEO** (2026-11-03, simulated people only). The rule excludes about 10% of
    simulated people under GEO1, GEO2 and EARLY, 18% to 20% at the noisiest rows (target 1.0) and 5% to
    7% at the least noisy. Under RDU, CAG, ADD and IA it excludes 1% to 2% (reference, 400 simulated
    pilots per truth).
  - **It also selects on the metric.** Under GEO1 it excludes 26% of people whose metric correlation is
    below −0.2, 4% of those between −0.2 and 0.2, and under 1% of those above 0.2. A negative
    correlation makes the dominated option, 10 points worse on both attributes, close in value to the
    better one. No simulated metric ranks it higher, so these are noisy choices, not reversed
    preferences.
  - As written, then, the rule would tilt the sample toward one sign of the metric correlation, which
    shapes the correlation attitude GEO predicts. This is an open decision (below).

**Comprehension quiz,** before block R. Four questions: what self points become, what charity points
become, how a lottery is resolved, and how many trials are paid. Someone who fails twice leaves with
the base payment, unless the ethics review sets otherwise.

**The instrument is the main study's, unchanged.**
- `stimuli.py` version 4, all 140 trials, the charity choice and the payment rule: one trial paid, a
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
- For the population `κ`, version 3's 95% intervals at 120 people had median width 0.19 under `κ = 1`
  and 0.32 under `κ = 2` (`results/summary_v3.json`). Scaled by √3, 40 people would give about 0.33
  and 0.55. That is an extrapolation, which the pilot rehearsal checks. One simulated pilot of 40 under
  GEO1 gave 0.80 to 1.16, a width of 0.35 (the self-test, 2026-11-03). The table's `κ` rows are 0.25
  apart, so 40 people place the study within a row or two.
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
  cautious choice (open decision, below).
- **Specificity holds.** The five specificity cells passed in no study at any n.
- **The rank-one check misses.** With 40% of people of rank one, power at n = 120 was 58% at `κ = 1`
  and 4% at `κ = 1.5`, against the 86% and 34% that `n(1 − s)` predicts. So `s` becomes a dimension of
  the table before the seal, as the rule above requires. The direction was predicted before the run (REHEARSAL.md): the margin applies
  to the mean over everyone, which the rank-one people pull toward zero.
- Cells took 43 to 132 minutes each.

## Reading the pilot

**Each model-free statistic is read against simulated pilots.** `pilot_analysis.py reference`
simulates pilots of 40 included people from the rehearsal's truths through the same 160 trials, recruiting
until 40 pass the inclusion rule, and computes each statistic the same way. The real value is read against that distribution, never against a number
chosen by hand, so the reference absorbs the statistic's own bias and spread.

**The row.** Each quantity enters at its pessimistic 80% limit, so that over the pilot's sampling
error the main study has at least the tabulated power with probability about 0.8. That is the logic of
sizing from an upper confidence limit of a pilot's variance (Browne 1995; from memory, to check).
- **`κ`.** The smallest tabulated `κ` at or above the 80th percentile of the posterior for the
  population median `κ`, from `hier.py` on the 64 calibration trials (DESIGN.md's secondary
  analysis). Above 2 there is no row, and the study is not powered for this population.
  - Version 3 found these intervals possibly narrow under `κ = 2` (they covered the truth in 7 of 10
    studies). The pilot rehearsal tests the rule itself at 40 people.
  - The fit leaves out the people flagged as self only (below), as the agreement does. The table's rows
    contain no such people.
  - If even the 80th percentile is below 1, the `κ = 1` row is used and the estimates say so. Power below
    `κ = 1` was not simulated. A population that takes risks over shortfalls, the pattern prospect theory
    reports for losses, would sit there. Whether to extend the table below 1 is an open decision.
  - Rounding up is cautious only if power falls as `κ` rises. In version 5 it does not: power is lowest
    around 1.5 to 1.75 (The power table, result). The rule needs changing before the seal (open
    decisions).
- **Noise.** The least noisy row whose simulated median agreement on the repeats, at the chosen `κ`,
  does not exceed the 20th percentile of the pilot's agreement (bootstrap over people). The pilot's
  agreement leaves out the people flagged as self only, whom the table's rows do not contain. If the
  pilot is noisier than every row, the table is extended by the same code before n is set.
- **The rank-one share `s`.** A person is flagged as self only if they chose the self-favouring option in
  at least 18 of the 24 high-ratio riskless pairs: block R's 20 pairs at ratios 2 and 3, and the four
  ratio-6 pairs. People who trade the two off mostly give on these pairs. The one-sided 80% upper Wilson
  limit `q` of the flagged share is converted with the row's simulated flag rates,
  `s = (q − fpr) / (tpr − fpr)`, clipped to [0, 1].
  - In the reference (10,000 included simulated people of each kind per row), the rule flags 61% to 97%
    of rank-one people, fewest at `κ = 2` and the noisiest target. It flags 0.6% to 2.0% of people who
    trade off.
  - *Revised 2026-11-03, before any data.* The first rule required at least 38 of the 40 block R pairs and
    all four ratio-6 pairs. It flagged 1% to 43% of simulated rank-one people, depending on the row.
    Someone who ignores the charity still chooses noisily between amounts 5 to 15 of their own points
    apart.
  - The rates come from the rehearsal's model of a rank-one person (REHEARSAL.md, version 5). If real ones
    are more consistent, the correction overstates `s`, which errs toward a larger sample.

**The sample size.**
- For n of 120, 160, 200 and 240, read the row's power at n(1 − s) people, interpolating linearly
  between tabulated values.
- n is the smallest with power of at least 0.80. It never goes below 120, the size at which the
  population `κ` and the crossing set were rehearsed.
- If none reaches 0.80, the study is not powered for the population the pilot found. The owner decides
  between running at 240, with the power stated in the registration, and stopping.
- Recruitment continues until n people meet the inclusion rule.

**Reported, not used for the row.** GEO's per-person ratio and metric correlation, the side bias, the
share who always trade toward the charity, and the lottery-choice rate at the ideal, each against its
reference under the version 4 assumptions. If the lottery rate points to a `κ` row two or more steps
from `hier.py`'s, the report says so before n is fixed. The rule still uses `hier.py`'s row.

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

1. **Owner decisions** (below).
2. **Prior art.** DESIGN.md's list and the two references below are read before anything is sealed.
3. **Build** (next section). A round trip sends the instrument's output through the split and the
   analysis, and checks that every cell lands where it should and nowhere else. An optional
   language-model pass over the wording (DESIGN.md, stage 2) fits here. It is not evidence about
   people.
4. **Pilot rehearsal** on NRP: simulated pilots of 40 through the whole chain. It must show that
   - under `κ` of 1, 1.5 and 2 the rule picks the true row or the one above in at least 90% of pilots;
   - the upper limit for `s` covers a planted share of 0.3 in about 80% of pilots;
   - the analysis refuses a file carrying a sealed trial, by its own guard;
   - a simulated input writes only `rehearsal_pilot_estimates.json`, and the sample-size rule refuses it
     by the provenance guard;
   - a deliberately broken split that leaks test choices fails the round trip, since a gate never shown
     to reject anything is decoration.
5. **Power table:** rehearsal version 5 on NRP.
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
| `stimuli.py`: `pilot_extras`, `presentation`, `digest` | the 20 pilot-only trials (ids 140 to 159, role "pilot", their own random stream; `build()` unchanged, checked against `stimuli_v4.json`); one participant's order from their seed; the hash the export must declare |
| `split_pilot.py` | the export into `readable.json`, `sealed.json`, `id_map.json` and `split_record.json`. Its docstring defines the export format the instrument must write |
| `pilot_analysis.py` | `reference`, `analyse`, `size`, `self-test` and `rehearse` (the pilot rehearsal), with the guards above |
| `rehearsal.py` | version 5 cells with `κ`, noise target, rank-one share and lapse ceiling as parameters (REHEARSAL.md); `simulate` runs the same people through the pilot-only trials |
| `power_table.py` | the table from the version 5 runs, with the rank-one and specificity checks |
| `hier.py` | now also reports the posterior's 80th percentile |
| the instrument | not built: it depends on the platform. It must write the export that `split_pilot.py` documents |

**Self-test** (`pilot_analysis.py self-test`, on Atlas). 17 of 17 checks pass, both with `κ` stubbed and
with `hier.py`. Each refusal is checked to name its own reason.
- The size rule refuses:
  - a missing file;
  - a simulated file put where it looks, for provenance;
  - a `κ` not from `hier.py`;
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
  2,208 misplaced trials, the 48 test trials of each of 46 simulated people. The analysis's own guard
  refuses it too.

**The pilot rehearsal** (sequence step 4) is built and smoke-tested, not run.
- **Smoke test.** Two simulated pilots under `κ = 1`, noise 1.5 and a planted rank-one share of 0.3
  took 283 s on one Atlas CPU, with a peak of 0.65 GiB.
  - Their upper limits for `s` were 0.45 and 0.36, both covering the planted 0.3.
  - Their `κ` rows were 1.25 and 1.
  - Both picked the noise row 1.0, one noisier than the truth (see the open decision on the noise rule).
- **Cost.** At about 2.5 minutes per pilot, 100 pilots per truth take about 4 hours. The run belongs on
  NRP, about 10 pilots per job.

**The reference** (`results/pilot_reference_v5.json`): 400 simulated pilots per truth, and the self-only
flag rates from 10,000 included simulated people of each kind per row. It took 423 s on one Atlas CPU.

## Open decisions (owner)

- Population, platform, who runs it, and the ethics route.
- The charity list and the point rate. The pilot must use the main study's.
- The cap on n. The table runs to 240.
- Whether the crossing set stays (DESIGN.md).
- The attention-check part of the inclusion rule, which under GEO selects on the metric correlation
  (Participants). The options:
  - keep the checks only as an instrument gate, read against the reference;
  - exclude only near-random responding, say the dominated option in 5 or more of 8;
  - redesign the pairs so that every rehearsed metric ranks them clearly. This needs a new stimulus
    version and a rerun.
- Whether to extend the table below `κ = 1` (Reading the pilot).
- The `κ` rule, now that power is not monotone in `κ`. One option: use the lowest power among the rows
  the posterior's central 80% interval spans, instead of the row above its 80th percentile.
- The rank-one share as a table dimension, which the rank-one check now requires: which shares, and at
  which rows.
- The noise rule.
  - As written, it moves to the next noisier row whenever the pilot's 20th percentile of agreement falls
    below the true row's median. If the bootstrap spread matches the sampling spread, that happens about
    80% of the time by construction.
  - The rows are far apart. In the reference, the median agreement is 0.64, 0.70 and 0.75, and a single
    pilot's agreement falls within about ±0.02 of it (20th to 80th percentile).
  - So the rule usually costs a full row of power. Interpolating the table between noise rows at the
    pilot's 20th percentile would keep the caution without the jump.
- Sealing.

## References to check

- Engel (2011), the dictator-game meta-analysis, for the share who give nothing.
- Browne (1995), on sizing a study from an upper confidence limit of a pilot's variance.
