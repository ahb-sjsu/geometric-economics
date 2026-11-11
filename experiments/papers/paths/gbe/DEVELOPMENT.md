# Great Brain Experiment: development record

Development half only (`split/dev.pkl` on Atlas, sha256 `5e622ed3…9d37e`). The held-out half and
the original archive are unreadable on Atlas. Nothing here is a registered test. Every choice is
Claude's.

## Fetch and split, 2026-11-11

The owner gave the word to download ("yes download as you recommend"). Dryad refused a scripted
download from Atlas (its interface asks for an account token and the public link returned 403), so
the archive was downloaded once through the owner's browser, moved to Atlas and deleted from the
laptop. Its sha256, `456859176aece7ac40dc2303aec210490a90bb5d395f713ddf75ffb91fb82168`, matches the
value Dryad records for the file.

Before any data was read, the authors' script and the PDF of field tables were extracted and read.
The archive stores a sequential participant number `id`, so the rule of `DESIGN.md` Section 4 was
applied to it by `split_gbe.py`. Development 23,589 participants, held out 23,478. The depression
subset went 951 and 907. The held-out file and the original archive were then set unreadable and
the unsplit copy deleted.

## Pass 1. The first comparison, and its check failing

`analyze_last.py`, `results/dev_last.json`. 23,589 participants, 45,652 plays, 1,369,560 trials.

Within a participant, the rate of gambling after a won gamble minus the rate after a lost one.

| Reference trial | Difference |
|---|---|
| The trial before (lag 1) | −0.0131 (−0.0160 to −0.0103) |
| Two trials before (lag 2) | −0.0037 (−0.0065 to −0.0009) |
| The trial after (lead 1), which must be zero | −0.0044 (−0.0071 to −0.0017) |

**The check did not return zero.** A choice cannot depend on a spin that has not happened. So this
estimator is biased by something of about a third of the size of the effect.

## Pass 2. The cause

`diag_check.py`, `results/dev_diag.json`.

- **The spinner is not a fair coin held fixed.** 50.53% of 825,511 taken gambles were won, which is
  about ten standard errors above one half. The share won is 50.2% on a participant's first play,
  50.7% on the second, 50.6% on the third and 51.2% on the fourth and later.
- The field tables say the player spins the spinner and record the direction and duration of the
  spin. Why the share won rises with practice is not known. It could be that players learn
  something about the spin, or that people who win more keep playing. Neither has been tested.
- **Pooled over all trials with no per-participant step, the checks are near zero** (lead 1
  +0.0016, lead 2 +0.0003) and lag 1 is −0.0104. So the bias is in comparing across one person's
  plays, where the chance of winning and the taste for gambling both drift.

The design note's statement that the last outcome is a coin flip needs this beside it. Within one
play it is close to one. Across a person's plays it is not.

## Pass 3. The comparison within a play

`analyze_within_play.py`, `results/dev_within_play.json`. Each play is its own block and only
contrasts inside a play are used.

| Reference trial | Difference |
|---|---|
| Lag 1 | −0.0107 (−0.0133 to −0.0084) |
| Lag 2 | −0.0039 (−0.0060 to −0.0018) |
| Lead 1, must be zero | +0.0021 (+0.0001 to +0.0041) |
| Lead 2, must be zero | −0.0005 (−0.0026 to +0.0015) |

The checks are now a fifth of the effect or less and of mixed sign. Lead 1 still just excludes
zero, so a small bias of unknown source remains and the registered test should carry the checks
with their own bars.

**Reading.** After winning a gamble a player gambles about one percentage point less on the next
trial than after losing one. Two trials on, the difference is about a third as large. That is the
same shape as chess and poker: the last step matters most and earlier ones less.

**By kind of trial, lag 1, within play.**

| | Difference |
|---|---|
| After a gamble in a gain trial (won a gain against got nothing) | −0.0248 (−0.0284 to −0.0214) |
| After a gamble in a mixed trial | −0.0086 (−0.0128 to −0.0043) |
| After a gamble in a loss trial (lost nothing against took the loss) | +0.0078 (+0.0036 to +0.0119) |
| Present trial is a gain trial | −0.0023 (−0.0058 to +0.0011) |
| Present trial is a mixed trial | −0.0266 (−0.0307 to −0.0224) |
| Present trial is a loss trial | −0.0069 (−0.0106 to −0.0030) |

Two things stand out and neither was predicted beforehand.

- The sign turns with the kind of gamble just played. After a gain trial, the better outcome
  lowers the next rate of gambling. After a loss trial, the better outcome raises it. Put by what
  happened to the points: a gamble that changed the total (a gain won, a loss taken) is followed
  by less gambling than one that left it where it was.
- The effect falls mostly on mixed trials, where a gain is weighed against a loss. On gain
  trials it is not distinguishable from zero.

These are development findings on half the data. They were looked for after the first result and
would need the held-out half to stand.

## What is not yet done

- The running total differs after a win and after a loss. No analysis here holds it fixed.
- The poker result was a dip after winning. This is a dip after winning too. Whether the two are
  the same thing is not shown.
- The source of the remaining lead 1 value.
- The published papers on these data have not been read for sequential effects on choice.
