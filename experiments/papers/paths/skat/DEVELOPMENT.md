# Skat: development record

Development archive only (`dev/skatgame-games-2016-05-2026.bz2` on Atlas). The held-out archive
is unreadable and unopened. Nothing here is a registered test. Every choice is Claude's.

## Pass 0, 2026-11-11. What the records hold

`count_basic.py`, `results/count_basic.json`. 2,620,004 games, all parsed. See `DESIGN.md`,
Section 3.

## Pass 1, 2026-11-11. Rows, seats and the deal

`mine_games.py` wrote one row per game. Logins are keyed digests and the four program names are
kept as names.

- **The seat reading holds.** In all 2,620,004 games every card a seat played was among the ten
  cards read as that seat's, or in the skat for the declarer. Not one game failed.
- **Nearly every game is one person against two programs.** 2,612,909 games have exactly two
  program seats. 6,860 have one, 219 have none and 16 have three (`results/repeats_dev.json`). So
  this archive is people playing the server's programs, and not people playing each other. The
  design note did not know this.
- **No deal is replayed.** No game has the same three hands as an earlier game of its series,
  in any seat order (`check_repeats.py`).
- **The deal looks fair by the last outcome.** The mean number of jacks in middlehand's cards is
  1.254 after a lost declared game, 1.249 after a won one and 1.252 after a game not declared, for
  people. A fair deal gives 1.25. The standard error at the smallest of these counts is about
  0.004.

## Pass 2, 2026-11-11. First rates by history, and a flaw the programs exposed

`analyze_bids.py`, `results/bids_dev.json`. 867,108 middlehand decisions by 3,072 people, of
which 295,435 by the ten busiest. People bid on 58.4% of them.

**People, within player and hand cell.**

| Comparison | Difference in rate of bidding | Players |
|---|---|---|
| After a won declared game, against after a game not declared | +0.022 (+0.002 to +0.041) | 819 |
| After a lost declared game, against after a game not declared | −0.003 (−0.024 to +0.019) | 706 |
| After a loss against after a win | −0.017 (−0.042 to +0.009) | 631 |
| One declared game in the last three, 1 back against 2 back | +0.007 (−0.015 to +0.030) | 574 |
| The same, 2 back against 3 back | +0.008 (−0.015 to +0.030) | 567 |

Dropping the ten busiest people changes no entry by more than 0.001. Nothing here is resolved
except the first row, and the first row has a plain other reading. A
player in a session of free bidding declares more and bids more, so that row can be produced by
the session and not by the win.

**The programs did not return zero under the comparison by lag.** With the series as the unit,
the difference between 2 back and 3 back was +0.033 for `kermit`, +0.055 for `zoot`, +0.035 for
`theCount` and +0.009 for `xskat`, and all four intervals exclude zero. The 1 back against 2 back
differences were near zero for all four.

**The raw rates say the programs do not respond.** Without cells, the rate of bidding by how far
back the one declared game lay:

| | 1 back | 2 back | 3 back |
|---|---|---|---|
| `xskat`, after a win | 0.606 | 0.605 | 0.604 |
| `kermit`, after a win | 0.531 | 0.526 | 0.542 |
| `zoot`, after a win | 0.627 | 0.636 | 0.628 |
| `theCount`, after a win | 0.562 | 0.557 | 0.556 |
| people, after a win | 0.546 | 0.541 | 0.539 |
| people, after a loss | 0.607 | 0.611 | 0.607 |

**Reading, which is an inference and has not been shown by simulation.** A middlehand decision
with the declared game three back means the same player was middlehand in that earlier game, bid,
and won the auction. That earlier bid is itself one of the decisions in the same series and often
the same cell. Selecting on it inside a short sequence pushes the rate in the selected group down,
which is the bias Miller and Sanjurjo (2018) described for streaks in finite sequences. It fits
the sign, and it fits the fact that only the comparison involving 3 back is affected, since one
and two games back the player sat in another seat. With the series as the unit the sequences are
short and the bias is large. With the player as the unit they are longer and it is smaller, but
it is not zero, and its size for people has not been measured.

**What follows.**

- The comparison by lag as built cannot be registered. It needs either an estimator that does not
  select within short sequences, or a correction measured by passing memoryless simulated players
  through the same code.
- The control worked as intended. It caught a flaw in the estimator that the people's numbers
  alone would not have shown.
- The same question now hangs over the poker contrast, which has the same shape. A note has been
  added to the poker results file. The poker verdicts stand as graded.
- For people, the raw rates after a win fall slightly with distance (0.546, 0.541, 0.539) and
  after a loss are flat. Nothing is claimed from them.

## Pass 3, 2026-11-12. The bias measured, and an estimator that does not have it for people

**The same games with memory removed.** `null_perm.py`. Every game in which middlehand bid or
passed is put in a cell (middlehand's login, jacks held, bin of aces plus tens). Inside a cell
the way the game went (the first action, who declared, the result) is shuffled among the games.
Deals, seats and the order of games stay. After the shuffle a bid depends on the hand cell and
on nothing before it, every player's rate in every cell is unchanged, and a game middlehand
declares is still one in which middlehand bid. Ten shuffles through the unchanged
`analyze_bids.py` (`results/null_summary_per_player.txt`).

| 2 back against 3 back | Real | Mean of ten shuffles | Spread of the shuffles (sd) |
|---|---|---|---|
| `xskat` | +0.009 | +0.011 | 0.003 |
| `kermit` | +0.033 | +0.029 | 0.009 |
| `zoot` | +0.055 | +0.029 | 0.010 |
| `theCount` | +0.035 | +0.033 | 0.004 |
| people | +0.008 | +0.012 | 0.008 |

- **The reading of pass 2 is shown.** Players with no memory give the differences the programs
  gave. The interval excluded zero in 38 of 40 shuffled runs for the programs. The estimator
  makes this difference and the programs did not respond to their past.
- `zoot` is 2.7 spreads above its shuffles. That is not followed up. One of four at that
  distance is not strong, and the shuffle is not a full model of a program.
- 1 back against 2 back is unbiased, as expected, since the player sat in another seat at both.
  The ten shuffles average −0.002 for people and within ±0.002 of zero for each program.
- **For people the first estimator is also too noisy to use.** With no effect in the data its
  value for 1 back against 2 back still ranged from −0.020 to +0.021 over ten shuffles.

**Cells pooled over players.** `analyze_bids_pooled.py`, `results/bids_pooled_dev.json`. The
same cells and the same two sides. Cells are weighted by n_a · n_b / (n_a + n_b) and pooled, so
a player counts by the number of usable decisions and not as one vote. Intervals from 2,000
resamples of players. Six shuffles through it (`results/null_summary_pooled.txt`).

| People | Real | Mean of six shuffles | Spread (sd) |
|---|---|---|---|
| After a lost declared game, against after a game not declared | +0.0208 (+0.0088 to +0.0328) | +0.0005 | 0.0013 |
| After a won declared game, against after a game not declared | +0.0196 (+0.0117 to +0.0283) | −0.0003 | 0.0006 |
| After a loss against after a win | −0.0046 (−0.0166 to +0.0072) | +0.0007 | 0.0017 |
| One declared game in the last three, 1 back against 2 back | +0.0041 (−0.0016 to +0.0101) | +0.0012 | 0.0017 |
| The same, 2 back against 3 back | −0.0014 (−0.0054 to +0.0021) | −0.0001 | 0.0019 |
| 1 back against 2 back, the game was won | +0.0071 (+0.0002 to +0.0142) | +0.0013 | 0.0020 |
| 1 back against 2 back, the game was lost | −0.0096 (−0.0204 to +0.0018) | +0.0002 | 0.0049 |

- **For people this estimator shows no bias.** All seven shuffled means are within 0.0013 of zero.
  The intervals are about a quarter as wide as before (0.012 against 0.045 for the lag rows).
- **For the programs the bias is still there** (2 back against 3 back, +0.008 to +0.029 on the
  shuffles), because their unit is the series and a series is short. The programs' real values
  sit on their shuffles here too.
- **After declaring a game a person bids more on the next one, by two points of a hundred, and
  it does not matter whether the game was won or lost.** This is far outside the shuffles. It is
  not evidence that the last game acts on the next bid. A player in a session of free bidding
  declares more and bids more, and the shuffle does not hold a session fixed.
- **The comparison built to cancel the session, 1 back against 2 back, shows nothing resolved.**
  +0.004, with an interval that includes zero. After a won game it is +0.007 and the interval
  just excludes zero. Without the ten busiest people it is +0.009 (+0.003 to +0.015) overall
  and +0.013 (+0.005 to +0.020) after a win, against shuffles of +0.001 and +0.000.
- If that holds it is a rise in bidding in the game straight after a won one, lasting one game.
  Poker gave a dip in raising straight after a large pot, so the direction is the opposite, and
  here it appears clearly only when ten people are left out. It is a development reading on a
  comparison chosen after seeing the table.

**What the shuffle does not test.** It breaks the tie between a player and that player's result
in games where the player sat in another seat, since the result moves with middlehand's cell.
The comparisons are within player, so this should not matter, but it has not been shown. And a
shuffle within a player's whole record removes sessions along with memory.

## Next

1. Decide whether Skat goes to a registration. The pooled estimator is fit to register for
   people. The one effect that cancels the session is small (+0.004 to +0.009) and unsettled, so
   a registration would be a test of a weak development signal. The owner's call.
2. Who the ten busiest people are in kind, people or programs, from their bidding against the
   four known programs. The lag result turns on them.
3. Position within the series, which the design listed and no pass has used.
4. The poker check asked for in pass 2 was done by simulation
   (`../poker/RESULTS-prereg-poker-recency-v1.md`).
