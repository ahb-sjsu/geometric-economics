# Poker: development record

**Development on three sites: Absolute Poker, Full Tilt Poker and Ongame Network.** Nothing here is
a registered test. PokerStars, iPoker and PartyPoker are held out and no action from them has been
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

## Reading, against what was written in DESIGN.md before any action was read

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
