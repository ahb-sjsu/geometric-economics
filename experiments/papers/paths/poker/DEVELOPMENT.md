# Poker: development record

**Development on three sites: Absolute Poker, Full Tilt Poker and Ongame Network.** Nothing here is
a registered test. PokerStars and PartyPoker are held out (iPoker was dropped on 2026-11-11, see the
registration, Section 3) and no action from them has been
read by a program (`DESIGN.md`, Section 2).

## Pass 1. A large win or loss, one to four hands back

`mine_hands.py`, then `analyze_lags.py`. Run 2026-11-10 on Atlas. Files `results/lags_dev.json` and,
for the record of a fault, `results/lags_dev_without_ongame.json`.

**Mined.** 4,240 files, 4,217,419 hands, 21,244,573 player-hand rows, 507 hands skipped as
unreadable.

**A fault found and fixed before the result was read.** The first run of the analysis used
13,644,244 rows. The hand number was parsed as an integer, and Ongame writes it as text such as
`R5-1704660-533`, so every Ongame row was dropped without a message. The order key is now the tuple
of integer groups in the label, and the output counts rows without a usable hand number (zero). The
numbers below are from the corrected run. The earlier output is kept under a name that says what it
lacked. Its curves agree with the corrected ones to within 0.004 at every point.

**Used.** 7,096 tables, 16,783,124 decisions with four measured results behind them. 392,507
decisions had two large events in the last four hands and are left out. 189,409 rises were treated as
possible top-ups and broke a chain.

**Entering the pot.** The rate in the baseline (four quiet hands) is 0.349 in the compared cells.
Each entry is the rate after one isolated event, minus the baseline, within player and state.
Intervals resample players.

| Hands back | After a loss of 10 big blinds or more | 95% interval | After a win of 10 or more | 95% interval |
|---|---|---|---|---|
| 1 | +0.0224 | +0.0173 to +0.0273 | −0.0204 | −0.0249 to −0.0160 |
| 2 | +0.0185 | +0.0136 to +0.0231 | −0.0152 | −0.0195 to −0.0107 |
| 3 | +0.0111 | +0.0061 to +0.0163 | −0.0131 | −0.0175 to −0.0087 |
| 4 | +0.0077 | +0.0026 to +0.0128 | −0.0101 | −0.0142 to −0.0057 |

**Raising.** Baseline 0.169.

| Hands back | After a loss | 95% interval | After a win | 95% interval |
|---|---|---|---|---|
| 1 | +0.0069 | +0.0033 to +0.0106 | −0.0310 | −0.0341 to −0.0278 |
| 2 | +0.0106 | +0.0069 to +0.0143 | −0.0171 | −0.0201 to −0.0140 |
| 3 | +0.0075 | +0.0037 to +0.0110 | −0.0105 | −0.0137 to −0.0074 |
| 4 | +0.0045 | +0.0007 to +0.0080 | −0.0113 | −0.0141 to −0.0083 |

**One hand back against two, over the same players.**

| | Entering | Raising |
|---|---|---|
| After a loss, lag 1 minus lag 2 | −0.0022 (−0.0089 to +0.0041), 23,359 players | −0.0091 (−0.0140 to −0.0040) |
| After a win, lag 1 minus lag 2 | −0.0111 (−0.0172 to −0.0050), 26,052 players | −0.0169 (−0.0210 to −0.0129) |

## Reading of pass 1, against what was written in DESIGN.md before any action was read

*Superseded in part by pass 2 below, 2026-11-10. Point 1 for losses and the loss column of the
tables above did not survive finer control of the stack.*

1. **The most recent hand changes the choice with the state held fixed.** Yes, for both events.
   Players enter 2.2 points more pots after a large loss and 2.0 points fewer after a large win, on a
   base of 35 in 100.
2. **The most recent hand carries more than the one before.** After a win, yes: the effect one hand
   back is larger than two hands back by 0.011 for entering and 0.017 for raising, over the same
   players. After a loss, no: the two are equal for entering, and for raising the effect two hands
   back is the larger.
3. **No claim on the sign.** Looser after a loss and tighter after a win is the direction reported
   in published work on online poker. It repeats a known result.

**The same shape as chess, and the same caution.** In both arenas the last step has an effect with
the state fixed, and something smaller is still there four steps back. In poker every point at lag 4
is clear of zero. As in chess, the column means fall with distance, and the comparison over the same
players is what shows whether that fall is real: after a win it is, after a loss it is not.

## Pass 2. The checks, and what did not survive them

Run 2026-11-10. Two controls, alone and together. Stack bins 10 big blinds wide in place of bins 40
wide (`lags_dev_bin10.json`), and the table added to the cell so that a player is compared only with
the same player at the same table (`lags_dev_coarse_table.json`, `lags_dev_bin10_table.json`). Per
site with narrow bins: `lags_dev_bin10_{ABS,FTP,ONG}.json`.

**Difference from the baseline, one hand after the event.**

| Specification | Enter, after loss | Enter, after win | Raise, after loss | Raise, after win |
|---|---|---|---|---|
| Coarse bins (pass 1) | +0.022 | −0.020 | +0.007 | −0.031 |
| Narrow bins | −0.002 | −0.041 | −0.013 | −0.038 |
| Coarse bins, same table | +0.013 | −0.024 | +0.002 | −0.033 |
| Narrow bins, same table | −0.022 | −0.055 | −0.026 | −0.043 |

**The finding of pass 1 that players enter more pots after a large loss is withdrawn.** It is +0.022
with coarse bins, zero with narrow bins and −0.022 with narrow bins at the same table. A result
whose sign depends on the width of a bin is not a result.

**Why the comparison with a baseline cannot be trusted in either form.** The stack is part of the
state, and the stack is itself made by the player's recent play. With coarse bins, a player after a
loss is shallower than the same player in the baseline, inside one bin, and shallow stacks are played
differently. With narrow bins the baseline at a given stack is made of the times the player drifted
to that stack through many small pots, which are stretches of active play, while the event hands
arrived there in one step. With narrow bins every curve goes negative and the loss curve grows with
distance (−0.022, −0.025, −0.031, −0.036 at the same table), which no account of behaviour predicts
and a biased baseline does. The three sites agree with one another under narrow bins, so this is a
property of the method and not of one site.

**After a large win the sign is the same in all four specifications.** Players enter fewer pots and
raise less. The size ranges from −0.020 to −0.055, so only the direction is supported, and the
direction is the one already published (Section "Prior work").

**One comparison does not use the baseline, and it holds in every specification.** One hand after
the event against two hands after the same kind of event, over the same players. Both sides have
just been through a large pot and sit at about the same stack.

| Specification | Raise, after loss | Raise, after win | Enter, after loss | Enter, after win |
|---|---|---|---|---|
| Coarse bins | −0.009 (−0.014 to −0.004) | −0.017 (−0.021 to −0.013) | −0.002 (−0.009 to +0.004) | −0.011 (−0.017 to −0.005) |
| Narrow bins | −0.007 (−0.014 to −0.001) | −0.014 (−0.019 to −0.009) | +0.004 (−0.005 to +0.012) | −0.004 (−0.012 to +0.004) |
| Coarse bins, same table | −0.010 (−0.015 to −0.004) | −0.017 (−0.021 to −0.012) | −0.001 (−0.009 to +0.006) | −0.010 (−0.016 to −0.003) |
| Narrow bins, same table | −0.011 (−0.019 to −0.004) | −0.009 (−0.015 to −0.003) | +0.006 (−0.004 to +0.016) | −0.000 (−0.009 to +0.008) |

**What development supports, then.** In the hand straight after a large pot, won or lost, a player
raises less often than one hand later, by about one point after a loss and one to two after a win,
on a base near 0.19. The eight intervals for raising all exclude zero. For entering the pot there is
no such effect after a loss, and after a win it appears only with coarse bins.

**For the claim carried from chess.** The most recent step changes the choice beyond the state, here
for raising. It does so whichever way the pot went, so it is a response to having just played a
large pot and not to its result. That is a narrower statement than the one pass 1 seemed to give.

## Pass 3. The surviving contrast, estimated directly

`analyze_recency.py`, run 2026-11-10. It uses only decisions with exactly one large pot in the
player's last four hands and compares, within a cell, the rate at one lag with the rate at the next.
No quiet-hand baseline enters. 2,790,778 decisions. Files `results/recency_dev_*.json`.

**Raising, after a large pot of either kind.** Rate one hand after: 0.15 to 0.17.

| Specification | Lag 1 − lag 2 | Lag 2 − lag 3 | Lag 3 − lag 4 | Players |
|---|---|---|---|---|
| Coarse bins | −0.012 (−0.017 to −0.007) | −0.002 (−0.006 to +0.003) | −0.002 (−0.007 to +0.002) | 17,974 |
| Narrow bins | −0.014 (−0.020 to −0.007) | −0.002 (−0.009 to +0.004) | +0.000 (−0.006 to +0.007) | 11,784 |
| Coarse bins, same table | −0.010 (−0.016 to −0.005) | −0.002 (−0.008 to +0.004) | −0.003 (−0.008 to +0.003) | 14,950 |
| Narrow bins, same table | −0.013 (−0.021 to −0.005) | −0.001 (−0.008 to +0.008) | −0.009 (−0.017 to −0.001) | 8,856 |

**The dip lasts one hand.** In the hand straight after a large pot a player raises about 1.2 points
less often than in the hand after that, which is about 8% of the rate. From the second hand on,
consecutive hands do not differ, in eleven of the twelve later intervals.

Split by the result of the pot, the first difference is −0.016, −0.015, −0.013 and −0.014 after a
win (all four intervals exclude zero) and −0.006, −0.011, −0.009 and −0.024 after a loss (two of four
exclude zero, and the players are half as many).

**Entering the pot shows no consistent first difference.** After a pot of either kind it is +0.004,
+0.000, +0.010 and +0.004, with one interval of four excluding zero.

**What this adds to pass 2.** The contrast is not only robust, it has a shape: one hand, then
nothing. In the language of `../DESIGN.md`, the depth of memory for raising is one step.

## Prior work, read 2026-11-10 from abstracts and summaries

- Smith, Levere and Kurtzman, "Poker player behavior after big wins and big losses", Management
  Science 55(9):1547–1555, 2009. Experienced online players play less cautiously after a big loss.
  A win or loss of $1,000 in one hand was the event and the next 12 hands the window. Looseness was
  measured by voluntary entry and aggression by an aggression factor.
- Eil and Lien, "Staying ahead and getting even: risk attitudes of experienced poker players", Games
  and Economic Behavior 87:50–69, 2014. Players take more risk while losing within a session, and
  gains make many of them more conservative.

Looser after losses and tighter after wins is therefore known. The first half did not survive the
checks here at a threshold of 10 big blinds. That is not a contradiction of the published result,
which used a threshold of $1,000 and a different comparison. Neither paper, as far as the abstracts
show, compares one hand after with two hands after. That is unverified against the full texts.

## Not excluded

- **The stack within a bin.** After a large win the stack is larger. Bins are 40 big blinds wide in
  the middle of the range, so a stack that grew by 10 can stay in its bin and still be deeper than
  in the baseline. Deeper stacks change correct play. This bears on the win curve and not on the
  loss curve, where a fall of 10 leaves the stack shallower. A rerun with narrow bins is the check.
- **Top-ups read as wins.** A rise that lands on a multiple of 10 big blinds is dropped. A top-up to
  any other amount is counted as a win.
- **The others at the table.** They saw the same hand and may play differently against the player
  who just won or lost.
- **Order of hands.** Hands are ordered by the number the site gave them. That this is the order of
  play within a table is assumed and was not checked against anything.
- **Any of it as a registered result.** Three held-out sites remain unread.

## Next

1. Narrow stack bins, and the same curves by site, to see whether the three development sites agree.
2. Prior art on play after wins and losses, read properly, before anything is called new.
3. A grader with bars from these numbers, then the owner's word on sealing the test for the three
   held-out sites.
