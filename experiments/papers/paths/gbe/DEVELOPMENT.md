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
whether the player gambled. Mixed trials only. The runs are trials of the method on small
samples.

**`radar_fit.py`, 15,000 trials, three folds done of five and part of the fourth** (read
2026-11-11 23:40 UTC, still running). Area under the ROC curve on participants not used for the
search.

| Columns | Formula found | Formula | Logistic regression | Boosted trees |
|---|---|---|---|---|
| Offer, fold 0 | `(ev_gap hypot ev_gap) / ev_gap` | 0.671 | 0.702 | 0.694 |
| Offer and person, fold 0 | `(ev_gap / lose) - g_rate_prev` | 0.800 | 0.814 | 0.822 |
| Offer, person and path, fold 0 | `(ev_gap / lose) - g_rate_prev` | 0.800 | 0.819 | 0.837 |
| Offer, fold 1 | `tanh(spread geometric ev_gap)` | 0.662 | 0.695 | 0.695 |
| Offer and person, fold 1 | `(ev_gap / lose) - g_rate_prev` | 0.777 | 0.780 | 0.798 |
| Offer, person and path, fold 1 | `(ev_gap / lose) - g_rate_prev` | 0.777 | 0.788 | 0.812 |
| Offer and person, fold 2 | `(ev_gap / lose) - g_rate_prev` | 0.805 | 0.807 | 0.815 |
| Offer, person and path, fold 2 | `(ev_gap / lose) - g_rate_prev` | 0.805 | 0.808 | 0.823 |
| Offer and person, fold 3 | `(ev_gap / lose) - g_rate_prev` | 0.807 | 0.797 | 0.810 |

On offer columns alone, folds 2 and 3 returned `sigmoid(lose geometric ev_gap)` and
`tanh(lose hypot lose)`, a different formula on every fold, none as good as the standard models.

- **With the player's own rate on offer, the search returned the same formula on every fold so
  far (four).**
  On a mixed trial the safe value is zero, so `ev_gap / lose` is half of one plus the ratio of
  the win to the loss. The formula says a player gambles when the win is large enough beside the
  loss, with a bar set by that player's habit. That is the standard account of loss aversion,
  recovered from the table with no hint. It is within 0.003 to 0.022 of the two standard models.
- **With the path columns on offer the search returned the same formula and used none of them**,
  on all three folds where that run is done.
  The boosted trees gained 0.008 to 0.016 from the path columns, so there is something there
  that one threshold on a short formula does not reach.
- The first formula on offer columns alone is the sign of `ev_gap` and no more.

**`radar_path.py`, 40,001 trials from 2,726 participants, five folds.** Only the trials that a
model of offer and person leaves open (its probability between 0.3 and 0.7), 17,392 test trials
over the folds, about half of them gambles. `base` is that model's log odds. Two scores were
tried. The second, the area under the ROC curve, was added to Theory Radar on the owner's word on
2026-11-11 after the first failed (theory-radar branch `feature/auc-objective-mahalanobis`,
commit db41b48). Mean area under the curve on participants not used for the search:

| | Area under the curve |
|---|---|
| Offer and person model alone (`base`) | 0.642 |
| Theory Radar formula, scored by F1 | 0.592 |
| Theory Radar formula, scored by area under the curve | 0.654 |
| Logistic regression on `base` and the seven path columns | 0.666 |
| Boosted trees on the same | 0.678 |

- **The path columns add 0.023 to 0.036 on the open trials**, by the two standard models.
- **Scored by F1, the formulas did worse than using no path column**, on every fold, and a
  different formula came back on most folds. With half the choices being gambles, saying yes every
  time scores 0.675 and the formulas found scored 0.679. F1 is the wrong score for a small shift
  in a rate.
- **Scored by area under the curve, four folds of five returned the same formula,
  `(base - prev_out) max base`,** and the fifth returned `(base - cum_total) + base`. Columns are
  on a common scale here, so the first reads: start from the player's usual odds and raise them
  when the last trial paid less than average, by the size of the shortfall, and leave them alone
  when it paid more. The formula gains 0.011, about a third to a half of what the standard models
  gain.
- So the search, given the right score, found a short and stable form, and it is one-sided: a
  poor last payoff raises gambling and a good one does nothing. That asymmetry was not looked
  for. It is a hypothesis for the held-out half. It also sits beside pass 6, where the points
  held account for most of the effect of the last outcome. The last payoff and the points held
  move together and these runs do not separate them.
- In the logistic regression of fold 0 the largest path weights were the points from the last
  trial (−0.27), the running total (−0.18), the points two trials back (−0.16) and the last
  surprise (+0.13), per standard deviation.

**With Mahalanobis columns, five folds** (`results/radar_path_mixed_auc_maha.json`). The owner
also proposed Mahalanobis distance. Theory Radar now has six such columns: the distance of a
trial from the centre of the gambles and from the centre of the safe choices, in the pooled
covariance and in each class's own, and the linear and quadratic discriminants built from them.
Mean area under the curve on participants not used for the search:

| | Area under the curve |
|---|---|
| Offer and person model alone (`base`) | 0.642 |
| Linear discriminant column alone (`maha_lin`) | 0.666 |
| Quadratic discriminant column alone (`maha_quad`) | 0.665 |
| Distance from either centre alone, four columns | 0.516 to 0.549 |
| Theory Radar formula with these columns on offer | 0.668 |
| Logistic regression on `base` and the seven path columns | 0.666 |
| Boosted trees on the same | 0.678 |

- **All five folds returned the same formula, `(prev_out max maha_lin) min maha_quad`**, with the
  first two terms in either order.
- **The linear discriminant alone equals the logistic regression on every fold**, to the third
  decimal, as it should, since the two are close to the same model. The formula is level with
  both (0.002 above on average, from −0.001 to +0.006 by fold).
- So these columns let a formula match the linear model. The boosted trees stay 0.010 above the
  formula on average. The columns do not by themselves say what the form is, because each
  one is a weighted mix of all eight columns. The short form without them,
  `(base - prev_out) max base` at 0.654, says more and scores less.

## Pass 6. Matching on the running total

`analyze_matched.py`, `results/dev_matched.json`. No mean is removed. Trials are put in cells and
the rate of gambling after a won gamble is compared with the rate after a lost one inside each
cell, all participants pooled.

| Cells | Last gamble won | Next gamble won, must be zero |
|---|---|---|
| Kind of trial, position in the play | −0.0105 (−0.0130 to −0.0080) | +0.0017 (−0.0002 to +0.0037) |
| and the points so far in the play, in bins of 25 | +0.0030 (+0.0004 to +0.0053) | +0.0018 (−0.0002 to +0.0038) |
| and the player's share of gambles on the rest of the play, five bins | −0.0023 (−0.0049 to −0.0002) | +0.0001 (−0.0016 to +0.0021) |

The intervals are from the rerun that added the splits below. Its resamples were not the same
ones as the first run's, so the ends moved in the fourth decimal. The estimates are unchanged.

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

**Apart by kind of trial** (same file, last trial as reference only). "Won" in a gain trial means
the gamble paid points where losing it paid zero. In a loss trial it means the gamble cost
nothing where losing it cost points.

| | Kind and position | and points so far | and the player's share |
|---|---|---|---|
| Last gamble was in a gain trial | −0.0282 (−0.0316 to −0.0248) | −0.0139 (−0.0174 to −0.0104) | −0.0173 (−0.0205 to −0.0140) |
| Last gamble was in a mixed trial | −0.0095 (−0.0136 to −0.0054) | +0.0004 (−0.0038 to +0.0047) | −0.0031 (−0.0070 to +0.0012) |
| Last gamble was in a loss trial | +0.0124 (+0.0083 to +0.0166) | +0.0207 (+0.0164 to +0.0244) | +0.0144 (+0.0102 to +0.0181) |
| Present trial is a gain trial | +0.0034 (+0.0002 to +0.0070) | −0.0059 (−0.0093 to −0.0023) | −0.0105 (−0.0136 to −0.0070) |
| Present trial is a mixed trial | −0.0309 (−0.0354 to −0.0268) | −0.0054 (−0.0097 to −0.0011) | −0.0104 (−0.0145 to −0.0062) |
| Present trial is a loss trial | −0.0096 (−0.0140 to −0.0059) | +0.0181 (+0.0138 to +0.0217) | +0.0118 (+0.0076 to +0.0152) |

- **The pooled figure near zero is two opposite effects.** With the points held matched, a won
  gamble in a gain trial is followed by less gambling (−0.014 to −0.017) and a won gamble in a
  loss trial by more (+0.014 to +0.021). After a mixed trial nothing is left. Both of the first
  two survive the match on the player's share.
- Put another way, in both kinds the player gambles less after a gamble that moved the points,
  up in a gain trial or down in a loss trial, than after one that returned zero. That reading
  was made after seeing the table.
- **These splits have no check of their own yet.** The next-trial check was run pooled only. It
  is being run by kind (`dev_matched_lead.json`), and until it is in the rows above stand
  unchecked.
- So the second bullet of this pass needs narrowing. Matching on the points held removes the
  pooled effect. It does not remove the effect after gain trials or after loss trials, which
  have opposite signs and cancel.

## Pass 7. Is the effect one-sided, with the points held matched

`analyze_onesided.py`, `results/dev_onesided.json`, 799,142 trials after a taken gamble. Pass 5
found the form `(base - prev_out) max base`: a poor last payoff raises gambling and a good one
does nothing. This pass asks whether that holds inside cells matched as in pass 6. Let s be half
the distance between the two outcomes of the last gamble, in hundreds of points (0.50 on
average). A won gamble paid s more than its mean and a lost one s less. The table gives the
change in the rate of gambling per hundred points of s, apart for won and lost, with a constant
for each cell and for won against lost. The same fit with the next gamble as reference is the
check. The outcome of the next gamble cannot act on the present choice, so that slope shows only
which players take wide gambles.

Cells without the points held (kind of present trial, kind of reference trial, position, the
player's share):

| | Last gamble | Next gamble | Last minus next |
|---|---|---|---|
| Won, per hundred points | −0.0112 (−0.0202 to −0.0024) | +0.0152 (+0.0061 to +0.0245) | −0.0264 (−0.0391 to −0.0138) |
| Lost, per hundred points | +0.0230 (+0.0139 to +0.0321) | +0.0030 (−0.0057 to +0.0123) | +0.0200 (+0.0075 to +0.0328) |

With the points held matched too, in bins of 25:

| | Last gamble | Next gamble | Last minus next |
|---|---|---|---|
| Won, per hundred points | −0.0004 (−0.0100 to +0.0085) | +0.0144 (+0.0051 to +0.0232) | −0.0148 (−0.0278 to −0.0026) |
| Lost, per hundred points | +0.0192 (+0.0099 to +0.0285) | +0.0001 (−0.0089 to +0.0097) | +0.0192 (+0.0063 to +0.0322) |

- **A larger bad surprise is followed by more gambling, and matching on the points held does not
  remove it.** The slope is +0.019 to +0.023 per hundred points in all four versions and every
  interval excludes zero. For the average gamble that is about one point of a hundred in the rate
  of gambling, the size of the pooled effect of pass 3.
- **For a good surprise the answer depends on the check.** With the points held matched the slope
  after a won gamble is zero (−0.0004), which is the one-sided form of pass 5. But the check is
  not flat for won gambles. A wider gamble won on the next trial goes with more gambling now
  (+0.014), and a wider gamble lost on the next trial does not (+0.000). Subtract the check and
  the won slope is −0.015, a two-sided effect.
- **The check itself is not understood.** If the next-trial slope showed only who takes wide
  gambles, it would be the same for won and lost, since the outcome is chance. It is not. This is
  the same unexplained next-trial value as in passes 3, 4 and 6, here with a shape. Until it is
  explained, neither the one-sided nor the two-sided reading of the won slope is established.
- The caveat of pass 6 holds here too. Two players at the same total after a wide loss and
  after a narrow loss came from different totals.

Set beside pass 6: on the points held matched, the average difference between after a win and
after a loss is near zero pooled, and yet the size of a loss still moves the next choice. So the
points held do not carry everything the last step does in these data. That is a development
reading and goes to the held-out half as a hypothesis.

## What is not yet done

- Pass 6 matches on the running total within a play. It does not separate the points held from
  the wealth of the player outside the game, which is not recorded.
- The next-trial check for the splits by kind in pass 6 is running.
- The first Theory Radar run (`radar_fit.py`) is unfinished, in its fourth fold of five.
- Why a wide gamble won on the next trial goes with more gambling now, and a wide one lost does
  not (pass 7).
- The poker result was a dip after winning. This is a dip after winning too. Whether the two are
  the same thing is not shown.
- The source of the remaining lead 1 value.
- The published papers on these data have not been read for sequential effects on choice. Two
  web searches on 2026-11-11 turned up no analysis of the previous outcome on these data. They
  found Rutledge et al. 2016 on age and risk and Bedder et al. 2023 on time of day. Two searches
  do not show there is none.
