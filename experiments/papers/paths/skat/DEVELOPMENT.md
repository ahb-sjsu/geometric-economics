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

## Next

1. A simulation with no memory through `analyze_bids.py` and through the registered poker code,
   to measure the bias in each.
2. An estimator for Skat that uses only lags at which the player sat in another seat, or pools
   cells across a player's whole record.
3. Position within the series, which the design listed and this pass did not use.
