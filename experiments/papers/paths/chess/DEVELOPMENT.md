# Chess: does the move order matter once the position is fixed? Development record

**Development on July 2026 of the Lichess open database.** Nothing here is a registered test. July
and August 2026 are development months. A later month, not yet downloaded, is held out.

The question and its reading are in `../DESIGN.md`, Sections 3 and 7b. In short: Definition 6.2 as
written predicts no effect of history once the state is fixed (`../lean/`,
`best_continuation_history_free`). An effect would mean the definition needs a reference point that
moves with the past, or a plan carried forward.

## Pass 1. A 4% sample of games, compared between groups of players

`mine_paths.py`, then `analyze_paths.py`. Run 2026-11-10 on Atlas, one core.

- 89,288,421 games read, 3,570,216 sampled by a keyed hash of the game address, 38,168,877 decision
  rows after 6 to 16 half-moves. 45,886 sampled games were too short, 16,372 involved a program
  account and 3,654 had no usable time control.
- A cell is one position at one rating band (400 points wide) and speed category. A path class is
  one ordering of the mover's own moves together with one ordering of the opponent's. Classes with
  at least 150 players enter. The statistic for a pair of classes is the total variation distance
  between their next-move distributions, minus its mean under 200 random relabellings.

| Comparison | Pairs | Positions | Excess distance, weighted mean | 95% interval | Pairs with p < 0.05 |
|---|---|---|---|---|---|
| Own moves in a different order | 319 | 110 | 0.085 | 0.071 to 0.100 | 66% |
| Opponent's moves in a different order | 449 | 112 | 0.049 | 0.035 to 0.062 | 44% |
| Opponent's earlier moves in a different order, last move the same | 163 | 67 | 0.006 | 0.001 to 0.013 | 15% |

Intervals resample positions. All pairs come from the first five or six moves of the game, because
only very common opening positions have two orders with 150 sampled players each. Blitz and bullet
supply almost all of them.

**Reading.** Most of the dependence on move order goes away as the comparison is tightened. With the
position, the mover's own order and the last move all fixed, the average excess is under one
percentage point. It is not zero: 15% of pairs reach p < 0.05 where 5% would by chance, and a few
positions show an excess near 0.10.

**Why this pass cannot settle it.** The groups compared are different people. A player whose own
moves were the same in two orders still chose each of them against a different reply. In the largest
case, a White player reaches the same position by `e4 Nf3 d4` against `c5 e6 cxd4` and against
`e6 c5 cxd4`. The second group played `Nf3` against the French move `e6`, which most players do not,
so the two groups differ in who they are before they differ in history. The remaining excess can be
that difference alone.

## Pass 2. Every game, compared within the player

`make_targets.py`, `mine_targets.py`, `analyze_within.py`, run by `run_within.sh`. Started 2026-11-10
05:31 UTC on Atlas, screen session `paths-chess-within`.

- `make_targets.py` lists every move order seen in the sample for the positions that entered pass 1:
  6,039 orders.
- `mine_targets.py` reads every game of the month and keeps those that follow a listed order, by
  matching the text of the first moves. No sampling.
- `analyze_within.py` takes each player who met one position in two or more games and every pair of
  those games. The outcome is whether the player chose a different next move in the two games. The
  baseline is that rate when the two move orders were identical. The quantity is the rate when the
  orders differed, minus the baseline, for players who have pairs of both kinds at one position.

A test on the first 300,000 games ran in 77 seconds and gave differences of about +0.02 for both
opponent-order classes and +0.06 for own-order, each with an interval that includes zero at that
size. The full month has about 300 times as many games.

**What would count as what, written before the full result.**

- A difference for the third class (opponent's earlier order, last move the same) whose interval
  lies within 0.01 of zero: the strict reading holds at the precision available, and the models for
  the other arenas need no history beyond the state.
- A positive difference clear of zero: history matters with the position, the player and the last
  move fixed. Whether it is a moving reference or a carried plan is then the next question.
- Still not excluded by this design: the opponent differs between the two games, and a player may
  respond to who the opponent is. Opponent rating is recorded and not yet controlled.

## Result of pass 2

To be added.
