# prereg-menus-v1. Does the menu set the scale of evaluation?

**Status: SEALED 2026-10-31** (`prereg-menus-v1.sha256`, signed tag `prereg-menus-v1`). No choice in
the test data had been read when it was sealed; Section 9 lists exactly what was seen.

## 1. The question

In binary choice an additive value and a menu-relative geometric cost cannot be told apart, because
the reference cancels (`../strata2/DEVELOPMENT.md`). With more options shown they can. On a
development dataset (Molter et al. 2022, `DEVELOPMENT.md`), three rounds found:

- a menu-relative reference with Euclidean distance does not produce context effects and fits worse
  than additive value;
- what the data want is a menu-dependent *scale*: each attribute's gap divided by the menu's range on
  that attribute raised to an exponent ρ;
- fit per participant, ρ has median 0.526 (interquartile range 0.381–0.746). It is partial: between
  absolute coding (ρ = 0) and full scale invariance (ρ = 1);
- this model beats additive value by 0.062 nats per trial and divisive normalisation by 0.060, and
  reproduces the attraction and compromise effects at their observed size.

This registration asks whether that law, **with ρ frozen at Molter's value**, predicts choices in a
different task with different people. In mathematical-physics terms, it tests the universality of a
scale exponent.

## 2. Test data, held back unread

Gluth, Spektor and Rieskamp 2018, *eLife* 7:e39659, OSF `8r4fh`, all four experiments. On every
trial, two all-or-nothing gambles HV and LV can be chosen. Magnitude is CHF 2–12, probability 1/8–7/8,
shown as colour and orientation. On distractor trials a third gamble D is shown but cannot be chosen.
The response deadline is 1.5 s (6 s for one group of Experiment 2).

| File | sha256 |
|---|---|
| exp1_data.zip | `310daf2920b8b074cec93872dd9940282eec9a7a3fcd7c12ee198e2e498d6e1c` |
| exp2_data.zip | `bae1c637a15f0388c8ab1a60c1a6ce0b1579ffb887127f350dc46ac63e6aa489` |
| exp3_data.zip | `96f74cb7b7855ead703924b214f2898ef3f9dbe778c4289b70b3e2adde35d0ba` |
| exp4_data.zip | `cbfe406e324845885968e54f46184e8a4e284a00a241eca3eec7ae6d3a171bd4` |

Parsing (`gluth_rows.py`) writes covariates and outcomes to separate files, and every row is assigned
to a named bucket:

| Experiment | Participants | Rows | Training (block 0) | Non-choice (codes 9, 10) | Kept |
|---|---|---|---|---|---|
| 1 | 31 | 15,232 | 2,460 | 701 | 12,071 |
| 2 | 49 | 23,120 | 2,932 | 623 | 19,565 |
| 3 | 23 | 11,112 | 1,636 | 395 | 9,081 |
| 4 | 44 | 16,416 | 3,216 | 799 | 12,401 |

That is 147 participants, matching the paper's 31, 49, 23 and 44, and 53,118 kept choices, of which
26,459 are on distractor trials. Kept rows include presses on D (code 2). These are not scored, because
D cannot be chosen; their number is reported.

Chau et al. 2014 (Dryad `10.5061/dryad.040h9t7`) was intended as a second test set, but Dryad refuses
scripted downloads (HTTP 401 and 403). It is not part of this registration.

## 3. Models (`menus_models.py`)

An option's coordinates are x = (W(p), (m/20)^α), where W is linear in log-odds (γ, δ). Every option
shown enters the menu statistics; only available options can be chosen. Choice is a softmax of minus
the cost over the available options.

| Model | Cost | Free parameters |
|---|---|---|
| ADD | a_p (r_p − x_p) + a_m (r_m − x_m), with r the attribute-wise best shown | 5 |
| **RNG** | the same, each gap divided by (menu range)^ρ\*, **ρ\* = 0.5256 frozen** | 5 |
| RNG1 | the same with ρ = 1 (full range normalisation) | 5 |
| DN | divisive normalisation: V = x_p x_m, cost −β V / (σ + ΣV over shown) | 6 |
| RNGfree | RNG with ρ free in (0, 1.5); fit only for H4 | 6 |

## 4. Protocol (`fit_menus.py`)

For each participant:

1. fit each model on that participant's **binary trials** (no D);
2. score the HV-or-LV choices on that participant's **distractor trials** by log-loss per choice;
3. for H4 only, fit RNGfree on all of that participant's trials.

Participants are weighted equally. Intervals are 2,000 bootstrap draws over participants. The margin
is 1% of ADD's mean calibration gain over chance: 0.01 × (ln 2 − mean binary-trial loss of ADD).

## 5. Predictions (`grade_menus.py`)

| | Prediction | Pass if |
|---|---|---|
| H1 | Range scaling at Molter's exponent beats additive value on distractor trials | RNG − ADD, upper 95% bound < −margin |
| H2 | It beats divisive normalisation | RNG − DN, upper bound < −margin |
| H3 | It beats full range normalisation | RNG − RNG1, upper bound < −margin |
| H4 | Universality: the exponent transfers | median per-participant ρ (RNGfree) in Molter's IQR [0.381, 0.746], and its 95% interval inside (0.10, 0.90) |
| H5 | Square-root-to-Weber crossover | **NOT ASSESSABLE, declared now.** Menu ranges span a factor of 5–6 (5th to 95th percentile, `gluth_stimuli.json`); a crossover needs an order of magnitude. |

**Void** if more than 10% of the per-participant fits fail to converge.

Each prediction stands alone. No combination is a headline.

## 6. What a result would mean

- **H1 passes.** The menu's range sets the scale of evaluation, with an exponent learned in another
  task, on other people, under a 1.5 s deadline.
- **H1 fails.** A dominated, unchoosable option does not move choice through range scaling in this
  task. That agrees with Cao and Tsetsos 2022, who found the reported distractor effects in these data
  vanish once covariation is controlled.
- **H4 fails while H1 passes.** Range scaling holds but its exponent is task-specific, so universality
  fails.

## 7. Rehearsal

Choices are simulated on the real Gluth stimuli from each truth (ADD, RNG, RNG1, DN), with
per-participant weights jittered. The chain and grader are run end to end. Required outcomes:

| Truth | Required |
|---|---|
| ADD | H1 FAIL, H4 FAIL |
| RNG | H1, H2, H3 and H4 PASS |
| RNG1 | H3 FAIL |
| DN | H2 FAIL |

Results are in `rehearsal/`.

**Round 1** passed all four truths. **Round 2** clipped the exponentiated weights at e^±20 in
`menus_models.py`; divisive normalisation had produced inf × 0 = NaN for large weights. It also passed
all four, and it is the code sealed here.

| Truth | RNG − ADD [95%] | RNG − DN | median free ρ [95%] | Verdicts H1–H4 | Required |
|---|---|---|---|---|---|
| ADD | +0.0148 [+0.0119, +0.0177] | +0.0076 | 0.03 [0.00, 0.05] | F F P F | H1 F, H4 F ✓ |
| RNG | −0.0143 [−0.0175, −0.0112] | −0.0195 | 0.558 [0.505, 0.584] | P P P P | all P ✓ |
| RNG1 | −0.0411 [−0.0445, −0.0378] | −1.94 | 1.02 [1.00, 1.06] | P P F F | H3 F ✓ |
| DN | +0.0171 [+0.0118, +0.0231] | +0.0450 | 0.06 [0.03, 0.10] | F F P F | H2 F ✓ |

Margins were 0.0008–0.0028. Under the RNG truth the effect is about ten times the margin. ρ is
recovered within 0.03 of its true 0.526, slightly high. One fit in 735 failed to converge under the
ADD and DN truths, far below the 10% void bar. The simulated effect size depends on the rehearsal's
assumed weights (`SIM_THETA` in `fit_menus.py`), so the power shown is for that size of effect.

**Note on `gluth_stimuli.json`.** Its "groups" field tabulates the `between` column, which turned out
to be a timing value, not a group label. Nothing uses it.

## 8. Development record

`DEVELOPMENT.md`, `explore_molter*.py`, `explore_molter*.json`. The development data are Molter et
al. 2022 from GitHub `moltaire/gda-context` at commit `66a425571b8165c3cb1f87e06956f8a56ad866fc`,
cleaned trials sha256 `4c74e4778d49122bc350a8692f8d89f74b9520544e45a0fcb5d1472539dbedd9`.

## 9. What was seen in the test data before sealing

- File names, the column header, and the comment header of one file. The comment header holds personal
  fields (age, sex, major); none are copied anywhere.
- The **sets** of distinct values of block, trial_type, positions and the response code in one file
  (no counts).
- Which response codes occur at all on trials with and without D, per block, in Experiments 1 and 4
  (presence only).
- To establish the response coding, Experiment 4's share of rows where the reward equalled HV's, LV's
  or D's drawn outcome, and the share of zero rewards, separately for each response code. This showed
  code 0 = HV and code 1 = LV. It does not give how often each code was pressed.
- Rows per block per participant, and trial-type sets per block (structure only).
- The accounting buckets in Section 2, and the stimulus statistics in `gluth_stimuli.json`.

No choice frequency, choice share, or model fit on Gluth's choices has been computed.
