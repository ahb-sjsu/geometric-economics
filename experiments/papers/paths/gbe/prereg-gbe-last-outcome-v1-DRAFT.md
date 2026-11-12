# prereg-gbe-last-outcome-v1. What the last gamble does to the next choice, and whether the points held carry it

**Status: DRAFT, not sealed.** Drafted by Claude on 2026-11-11 from the development half alone
(`DEVELOPMENT.md`, passes 1 to 7). Every bar below is Claude's proposal and open to the owner.
The held-out half has not been opened. Sealing needs the owner's word and the items of Section 10.

## 1. Question

Chess and poker supported the claim that the last step changes a choice beyond the present
position. The Great Brain Experiment is the first arena here in which the order of trials was
set by chance, so the last outcome is close to assigned. Development gave an answer with two
parts, and both go to the held-out half.

- Pooled, a player gambles about one point of a hundred less after a won gamble than after a
  lost one, and that difference goes away once the points held are matched.
- Inside that null there is structure. The sign turns with the kind of trial just played, and
  the size of a loss moves the next choice more than the size of a win.

## 2. What development found

23,589 participants, 799,142 choices that follow a taken gamble.

| Quantity | Development value |
|---|---|
| After a win minus after a loss, matched on kind and position | −0.0105 (−0.0130 to −0.0080) |
| The same with the points held matched | +0.0030 (+0.0004 to +0.0053) |
| The same with the player's share of gambles matched too | −0.0023 (−0.0049 to −0.0002) |
| After a gain trial, points held matched | −0.0139 (−0.0174 to −0.0104) |
| After a loss trial, points held matched | +0.0207 (+0.0164 to +0.0244) |
| Slope on the size of a lost gamble, points held matched, per hundred points | +0.0192 (+0.0099 to +0.0285) |
| Loss slope minus win slope, points held matched | +0.0197 (+0.0066 to +0.0325) |
| Next-trial check, pooled, three matchings | +0.0017, +0.0018, +0.0001 |

The splits by kind and the slopes were looked for after the first result. They are hypotheses
and this registration is their first test.

## 3. Data

Rutledge, "Risky decision and happiness task: The Great Brain Experiment smartphone app", Dryad,
doi 10.5061/dryad.prr4xgxkk. Archive sha256
`456859176aece7ac40dc2303aec210490a90bb5d395f713ddf75ffb91fb82168`.

**Held out:** the 23,478 participants whose identifier hashes to 8 through f under the rule of
`DESIGN.md` Section 4, fixed before the download. All of a participant's plays go with the
participant.

**What has been read of them.** The count of participants, written by `split_gbe.py`, which reads
the identifier field and no other. Nothing else. The file has been unreadable since the split.

## 4. Procedure, fixed

1. `analyze_matched.py HELDOUT OUT` and `analyze_matched.py HELDOUT OUT_LEAD lead`, unchanged.
   Rows are choices whose reference trial was a taken gamble. Inside a cell the rate of gambling
   after a won reference gamble minus the rate after a lost one, cells weighted by
   n_won · n_lost / (n_won + n_lost), participants pooled. Cells are M0 (kind of present trial,
   position in five bins), M1 (and points so far in the play in bins of 25) and M2 (and the
   player's share of gambles on the rest of the play in five bins). Intervals from 1,000
   resamples of participants.
2. `analyze_onesided.py HELDOUT OUT`, unchanged. Slopes of the present choice on the half spread
   of the reference gamble, apart for won and lost, with a constant per cell and per outcome.
   Cells C1 are kind of present trial, kind of reference trial, position, the player's share and
   the points so far in bins of 25.
3. The reference is the last trial (lag 1) for the predictions and the next trial (lead 1) for
   the checks.

## 5. Predictions

- **H1. Gambling dips after a win.** Lag 1, M0, interval below zero.
- **H2. The size replicates.** Lag 1, M0, point estimate in −0.018 to −0.004.
- **H3. The points held carry the pooled dip.** Lag 1, M1 and M2, both intervals inside −0.008
  to +0.008.
- **H4. The sign turns with the kind of trial just played.** With the points held matched (M1),
  the interval after a gain trial is below zero and the interval after a loss trial is above
  zero. Reported for M2 as well, where the same is expected.
- **H5. A larger loss on the last gamble is followed by more gambling.** C1, lag 1, slope for
  lost gambles, interval above zero.
- **H6. The loss slope is larger than the win slope.** C1, lag 1, loss slope minus win slope,
  interval above zero. On development this was three of its own standard errors from zero. If
  the true value equals the development value the chance of passing is about 0.85, and less if
  development overstated it.

**Checks, each with its own bar.** A prediction counts only if its check holds.

- **K1, for H1 to H3.** Lead 1, pooled, M0, M1 and M2: each point estimate within ±0.004.
- **K2, for H4.** Lead 1 after a gain trial and after a loss trial, M1: each point estimate
  within ±0.005.
- **K3, for H5.** Lead 1 slope for lost gambles, C1: point estimate within ±0.010.
- H6 has no check. A selection common to won and lost gambles cancels in it.

**What each failure would mean.**

- H1 fails: the development dip does not carry to other people in the same app.
- H3 fails with H1 passing: the last outcome acts beyond the points held, pooled, and pass 6 of
  development was wrong about why.
- H4 fails with H3 passing: the points held carry the whole effect and the split by kind was a
  product of looking.
- H5 or H6 fails: the one-sided form that Theory Radar found on development does not hold up.
- A check fails: the comparison it guards is not trusted on this half, whatever its value.

**Overall.** The first part of Section 1 counts as replicated if H1, H3 and K1 pass. The second
part counts as replicated if H4 with K2 and H6 pass. Anything less is reported as it falls and
is not called a replication.

## 6. Reported without a bar

- Whether the slope after a won gamble is zero or negative, with each of the two checks of
  pass 7. Development could not decide it.
- The difference between the next-trial slopes for won and lost gambles.
- All splits by kind of the present trial, and after a mixed trial.
- Lag 2.
- The same quantities on each participant's first play alone.
- The within-play comparison of pass 3 and the fits of pass 4, labelled with their failed checks.
- The frozen Theory Radar formula `(base - prev_out) max base` against the model of offer and
  person alone, by area under the curve, if the script of Section 10 exists at the seal.

## 7. Not claimed

A pass says that in this app, played for points by unpaid volunteers, the choices follow the
pattern above. It does not say the pattern holds for money. It does not separate the points held
in a play from a player's wealth, which is not recorded. The spinner is not a fair coin (50.5% of
gambles are won, more on later plays), so the last outcome is close to assigned by chance and not
exactly so. The checks are the guard against that and they are not proof.

## 8. Void conditions

- **V1.** The held-out file does not hold 23,478 participants.
- **V2.** Fewer than 600,000 choices follow a taken gamble. Development had 799,142.
- **V3.** Any of the three scripts is changed after the seal.

## 9. Bundle to seal

This file, `DESIGN.md`, `DEVELOPMENT.md`, `split_gbe.py`, `analyze_last.py` (for the shared
constants), `analyze_matched.py`, `analyze_onesided.py`, a grading script, and the development
result files `results/dev_matched.json`, `results/dev_matched_lead.json`,
`results/dev_onesided.json` and `results/dev_onesided_first.json`. Then a signed commit and a
signed tag pushed to the public repository, and only then the held-out file is made readable.

## 10. Before sealing

- A grading script that reads the three result files and returns each prediction and check as
  pass or fail, and its self-test on the development files. On development it must return every
  prediction and check of Section 5 as a pass, since the bars were set there.
- A seal script that lists the bundle and writes the hash file, as for chess and poker.
- The published papers on these data read for any analysis of the previous outcome. Two web
  searches found none. Two searches do not show there is none.
- The owner's view on the bars, above all the bands of H2 and H3 and the limits of K1 to K3,
  which are set by eye at roughly twice the development values.
- Whether to add the frozen Theory Radar formula as a prediction. It needs a script that fits
  the model of offer and person on development and scores the formula on the held-out half.
- The owner's word.
