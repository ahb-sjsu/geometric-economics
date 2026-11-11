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

## Pass 4. Holding the running total fixed

`analyze_total.py`, `results/dev_total.json`. 799,061 trials from 23,571 participants. Least
squares within a play of the present choice on whether the last gamble was won, with other
columns added. The second row is the same fit with the next trial as reference, which must give
zero.

| Columns beside the last outcome | Last gamble won | Next gamble won, must be zero |
|---|---|---|
| None | −0.0107 (−0.0132 to −0.0083) | +0.0021 (+0.0001 to +0.0041) |
| Offer, kind of trial, position in the play | −0.0113 (−0.0137 to −0.0090) | +0.0015 (−0.0005 to +0.0033) |
| Total | +0.0010 (−0.0015 to +0.0035) | −0.0091 (−0.0111 to −0.0071) |
| Total, offer, kind | −0.0063 (−0.0086 to −0.0039) | −0.0035 (−0.0054 to −0.0016) |
| Total, offer, kind, position | −0.0074 (−0.0097 to −0.0050) | −0.0026 (−0.0046 to −0.0008) |

- **The effect is not explained by the offer or by where the trial sits in the play.** With
  those held fixed it is −0.0113 and the check passes.
- **This method cannot hold the total fixed.** Every fit that includes the total fails the check,
  by as much as −0.0091. A likely cause, not tested: the mean of the total over a play includes
  the trials after a future win, so removing that mean ties the total to outcomes that have not
  happened yet. The rows with the total are therefore not evidence either way.
- In every fit a higher total goes with less gambling, about one to three points in a hundred per
  standard deviation of the total within a play (122 points). That coefficient carries the same
  bias and is not a result.

Whether the last outcome acts beyond what it does to the total stays open. A comparison that
does not remove a mean within the play is needed, for example matching trials on the total
across plays.

## Pass 5. Theory Radar

The owner proposed using his Theory Radar (`theory-radar` 0.4.0, commit 2155a62) to look for a
more basic form behind these patterns. It searches short formulas over the columns of a table
for the one whose threshold best separates a yes from a no, scored by F1. The yes or no here is
whether the player gambled. Mixed trials only. Both runs are trials of the method on small
samples and neither is finished.

**`radar_fit.py`, 15,000 trials, two folds done of five.** Area under the ROC curve on
participants not used for the search.

| Columns | Formula found | Formula | Logistic regression | Boosted trees |
|---|---|---|---|---|
| Offer, fold 0 | `(ev_gap hypot ev_gap) / ev_gap` | 0.671 | 0.702 | 0.694 |
| Offer and person, fold 0 | `(ev_gap / lose) - g_rate_prev` | 0.800 | 0.814 | 0.822 |
| Offer, person and path, fold 0 | `(ev_gap / lose) - g_rate_prev` | 0.800 | 0.819 | 0.837 |
| Offer, fold 1 | `tanh(spread geometric ev_gap)` | 0.662 | 0.695 | 0.695 |
| Offer and person, fold 1 | `(ev_gap / lose) - g_rate_prev` | 0.777 | 0.780 | 0.798 |

- **With the player's own rate on offer, the search returned the same formula on both folds.**
  On a mixed trial the safe value is zero, so `ev_gap / lose` is half of one plus the ratio of
  the win to the loss. The formula says a player gambles when the win is large enough beside the
  loss, with a bar set by that player's habit. That is the standard account of loss aversion,
  recovered from the table with no hint. It is within 0.003 to 0.022 of the two standard models.
- **With the path columns on offer the search returned the same formula and used none of them.**
  The boosted trees gained 0.016 from the path columns on fold 0, so there is something there
  that one threshold on a short formula does not reach.
- The first formula on offer columns alone is the sign of `ev_gap` and no more.

**`radar_path.py`, 40,000 trials, one fold done of five.** Only the trials that a model of offer
and person leaves open (its probability between 0.3 and 0.7), about a third of all trials. On
3,590 such test trials the area under the curve was 0.642 for the offer and person model alone,
0.667 with a logistic regression that adds the path columns, 0.670 with boosted trees, and 0.612
for the formula Theory Radar found, `(prev_lat max cum_total) * base`.

- **The path columns add about 0.025 on the open trials**, by the two standard models.
- **Theory Radar's formula did worse than using no path column at all.** On these trials about
  half the choices are gambles, and F1 at that rate is nearly as high for saying yes every time
  (0.656) as for the formula found (0.667). F1 is the wrong score for a small shift in a rate. A
  search scored by area under the curve or by log loss would be the fair trial of the idea, and
  that is a change to Theory Radar and not to this analysis.
- In the logistic regression the largest path weights were the points from the last trial
  (−0.27), the running total (−0.18), the points two trials back (−0.16) and the last surprise
  (+0.13), in units of one standard deviation. More points just received, less gambling. One
  fold, no intervals.

## Pass 6. Matching on the running total

`analyze_matched.py`, `results/dev_matched.json`. No mean is removed. Trials are put in cells and
the rate of gambling after a won gamble is compared with the rate after a lost one inside each
cell, all participants pooled.

| Cells | Last gamble won | Next gamble won, must be zero |
|---|---|---|
| Kind of trial, position in the play | −0.0105 (−0.0130 to −0.0080) | +0.0017 (−0.0003 to +0.0038) |
| and the points so far in the play, in bins of 25 | +0.0030 (+0.0004 to +0.0056) | +0.0018 (−0.0002 to +0.0039) |
| and the player's share of gambles on the rest of the play, five bins | −0.0023 (−0.0047 to −0.0001) | +0.0001 (−0.0017 to +0.0020) |

- **All three checks pass**, which the method of pass 4 could not manage with the total in the fit.
- **Once two trials are matched on the points held, most of the effect of the last outcome is
  gone.** It falls from −0.0105 to between +0.0030 and −0.0023, with the sign depending on
  whether the kind of player is matched too. On this evidence the dip after a win is mostly the
  player holding more points, and not the win as an event.
- What is left is at most about a quarter of the first figure and its sign is not settled. Two
  players at the same total after a win and after a loss came from different totals, so they are
  not the same kind of player, and the third row only partly repairs that.

This bears on the claim the campaign set out to test. Chess and poker supported "the last step
matters beyond the present position". Here the present position, the points held, appears to
carry most of what the last step seemed to do. That is a development finding on half the data
and it was not predicted.

## What is not yet done

- Pass 6 matches on the running total within a play. It does not separate the points held from
  the wealth of the player outside the game, which is not recorded.
- The splits by kind of trial in pass 3 have not been redone with the total matched.
- Both Theory Radar runs are unfinished, and a search scored by something other than F1 has not
  been tried.
- The poker result was a dip after winning. This is a dip after winning too. Whether the two are
  the same thing is not shown.
- The source of the remaining lead 1 value.
- The published papers on these data have not been read for sequential effects on choice.
