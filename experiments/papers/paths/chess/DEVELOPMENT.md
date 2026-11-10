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

## Pass 2 restated as one curve: how far back does history reach?

Added 2026-11-10 while pass 2 was mining, before any full result. `analyze_memory.py`, run by
`run_memory.sh` on the same rows.

The three classes of pass 1 were chosen by hand. `../lean/` now gives a reason for one ordering of
them. If edge weights read a reference that moves with the past, history matters only through that
reference, and a reference that reads back m steps cannot tell apart two games that share their last
m half-moves. So for each pair of one player's games at one position, let k be the number of final
half-moves the two orders share, and let D(k) be the rate at which the player changes move in such
pairs minus the rate when the whole order was identical.

| Curve | What holds |
|---|---|
| D(k) = 0 for every k | Definition 6.2 as written. No history beyond the state |
| D(0) > 0 and D(k) = 0 from k = 1 | The reference is the previous position |
| D(k) reaches 0 at k = m | A reference with memory m |
| D(k) does not fall with k | Not a reference of bounded memory. A plan, or a difference between opponents |

The curve is reported twice: over pairs where the player's own moves came in the same order, and
over all pairs.

**Reading rule, written before the result.** D(k) counts as zero when its 95% interval lies inside
−0.01 to +0.01. The estimate of memory is the smallest k from which every D with a usable interval
counts as zero. If no such k exists within the first five half-moves, the bounded-memory reading
fails on this evidence.

**Limits known in advance.** Positions come from the first six moves of the game, where play is
memorised. With the player's own order held the same, k is always even, so the curve has points at
0, 2 and 4 only. The opponent differs between the two games of a pair, and opponent rating is not
yet controlled. A script test on the first 400,000 mined rows ran correctly. Its numbers are from 1%
of the month and are not a result.

**Timing.** Pass 2 reads about 9,000 games a second on its one core, so July takes near three hours
and August follows. Both curves are queued behind them (screen session `paths-chess-memory`).

## Pass 3, planned: does a boundary cost something in the present choice?

Written 2026-11-10 before any such analysis. This is the direct test of Definition 6.1
(`../lean/`, `boundary_edge_costs_its_penalty`): of two moves at equal distance, the one that crosses
a boundary costs that boundary's penalty more, so it should be chosen less, by an amount that belongs
to the boundary and not to the position.

**A pilot that needs no engine time.** About 6% of Lichess games carry the site's own engine
evaluation after every move. `mine_targets.py` now keeps that number where present. On the first
400,000 games of August, 21,676 of 179,272 mined decisions carried one (12%). August's full pass
will therefore give evaluations for most moves that are played at all often in the target positions.

- **Static value of a move:** the median evaluation after it, over the games that carry one, from
  the mover's side. A move needs at least 20 evaluated games.
- **Equal moves:** two moves at one position whose static values differ by at most 0.10 pawns.
- **Edge classes, from the rules and the move's notation alone:** capture, pawn move, castling, king
  move that gives up castling, other piece move. The last is the class that crosses nothing.
- **Quantity:** for each pair of equal moves of different classes, the log odds that players choose
  the boundary-crossing move, within rating band and speed. Pooled over positions per class, with an
  interval from resampling positions, and a measure of how much it varies between positions.
- **Reading, fixed now.** Definition 6.1 with non-negative penalties predicts log odds below zero
  for every crossing class, about the same at every position. Log odds above zero for a class mean
  that boundary attracts and does not cost, which the definition as written does not allow. Wide
  variation between positions means the offset is not a constant of the boundary.

**Why this is only a pilot.** The target positions are opening positions, where the popularity of a
move reflects memorised theory more than a choice made at the board. Evaluations from the site are
shallow. A proper test needs positions from the middle of the game and engine analysis of every
legal alternative, which is an NRP job and is not yet planned in detail. The pilot is run to learn
the size and sign to expect.

## Result of the pass 3 pilot (August 2026)

`analyze_edges.py`, run 2026-11-10 on August's rows, the only ones that carry evaluations.
`results/edges_pilot_2026-08.json`. 232 positions had at least two moves with 20 evaluated games and
50 plays each. Each row compares a class of move with engine-equal moves of class `piece`, the class
that crosses nothing.

| Class | Positions | Pairs | Mean log odds of choosing it | 95% interval | Spread between positions (SD) | Positions below zero |
|---|---|---|---|---|---|---|
| Pawn move | 217 | 2,118 | −0.21 | −0.35 to −0.08 | 1.09 | 60% |
| Capture | 39 | 87 | +0.89 | +0.31 to +1.45 | 1.87 | 21% |
| Castling | 13 | 20 | +2.28 | +1.38 to +3.19 | 1.77 | 0% |
| King move | 3 | | too few | | | |
| Check: piece against piece | 196 | 1,285 | +0.16 | −0.03 to +0.36 | 1.37 | 43% |

**Reading, by the rule fixed above.**

- **Captures and castling are chosen more than equal quiet moves, not less.** A capture is chosen
  about 2.4 times as often and castling about ten times as often. Definition 6.1 with non-negative
  penalties does not allow a boundary that attracts. On this pilot the reading "a move that cannot
  be undone carries a penalty" is contradicted for both.
- **Pawn moves are chosen a little less,** by a factor of about 0.8. The check row shows the pooling
  has noise of the same size (+0.16 where it should be zero), so this is not established.
- **The offset is not a constant of the class.** The spread between positions is five times the mean
  for pawn moves and twice the mean for captures.

**What this does and does not say.** It says that irreversibility under the rules of chess is not a
boundary in the sense of Chapter 6. That was this design's guess (`../DESIGN.md`, Section 7b) and
not a statement of the programme, whose boundaries are things like a right given up or a sacred
value crossed. The pilot is on opening positions, where recapturing and castling are standard, and
the evaluations are shallow. It is a pilot against one operational reading, and it went against that
reading. A test of boundary penalties in chess would first need a reason, independent of the data,
to call something a boundary there. None is offered here.

## Result of pass 2 (development, July and August 2026)

Every game of each month was read. July gave 39,609,722 decisions at the target positions and
5,893,068 player-position cells with two or more games. August gave 40,938,630 and 6,069,628.
Files: `results/within_2026-0{7,8}.json`, `results/memory_2026-0{7,8}.json`.

**The memory curve, player's own moves in the same order in both games.** D(k) is the rate at which
a player changes move between two games sharing their last k half-moves, minus the rate between two
games with identical move orders. Intervals resample players.

| Shared final half-moves | July D | July 95% interval | August D | August 95% interval | Players (July) |
|---|---|---|---|---|---|
| 0 (opponent's last move differs) | +0.0376 | +0.0368 to +0.0385 | +0.0373 | +0.0365 to +0.0382 | 436,372 |
| 2 | +0.0129 | +0.0119 to +0.0140 | +0.0130 | +0.0120 to +0.0140 | 280,820 |
| 4 | +0.0091 | +0.0074 to +0.0109 | +0.0070 | +0.0052 to +0.0087 | 101,741 |
| 6 or more | +0.0072 | +0.0015 to +0.0129 | +0.0032 | −0.0022 to +0.0084 | 12,162 |

The baseline rate of changing move between identical orders is 0.21 to 0.28. Over all pairs,
including those where the player's own order differed, D is +0.043 at k = 0 and +0.043 to +0.045 at
k = 1 in both months, then +0.014, +0.018 to +0.021, +0.007 to +0.009 and +0.007 to +0.010.

**Reading by the rule written above.**

- **Definition 6.2 as written fails here.** The same player in the same position changes move 3.8
  percentage points more often when the opponent's last move differed. The interval is nowhere near
  the ±0.01 band. Player identity cannot explain it, since each player is compared with themselves.
- **A reference equal to the previous position fails too.** With the last move the same and only
  earlier moves different, D is +0.013, outside the band in both months.
- **The curve falls with distance.** +0.038, +0.013, +0.008, +0.005. The two months agree to the
  third decimal at k = 0 and k = 2.
- **Whether it reaches zero is not settled.** By the rule, August gives a memory of four half-moves
  and July gives none inside the window, because July's interval at k = 4 ends at +0.0109. The rule
  was written with a band of ±0.01 and the curve sits right at it.

**What is not excluded.** These numbers are from the first six moves of the game. The opponent
differs between the two games of a pair, and a player may respond to who the opponent is. And pairs
with identical orders may more often be rematches minutes apart, in which a player repeats a line.
That would lower the baseline and lift every D(k) by the same amount. It cannot produce the fall
from k = 0 to k = 2, which is a difference between two points measured against similar baselines.
It could produce the floor near +0.007. The next table tests it.

## Control: pairs of games at least 24 hours apart

`analyze_memory.py` with a third argument of 24, run 2026-11-10. Every pair, including the
identical-order baseline, uses two games at least a day apart. Files
`results/memory_gap24_2026-0{7,8}.json`. Own moves in the same order.

| Shared final half-moves | July D | July 95% interval | August D | August 95% interval |
|---|---|---|---|---|
| 0 | +0.0363 | +0.0354 to +0.0371 | +0.0360 | +0.0352 to +0.0369 |
| 2 | +0.0123 | +0.0112 to +0.0133 | +0.0129 | +0.0119 to +0.0140 |
| 4 | +0.0084 | +0.0066 to +0.0102 | +0.0069 | +0.0050 to +0.0086 |
| 6 or more | +0.0044 | −0.0013 to +0.0103 | +0.0000 | −0.0053 to +0.0056 |

The control removes about a ninth of the pairs and changes no point by more than 0.003. Rematches
within a session do not explain the curve or its floor.

## Control: opponents of similar rating

`analyze_memory.py ROWS OUT 24 50`, run 2026-11-10. Pairs a day apart whose two opponents were rated
within 50 points of each other. Files `results/memory_gap24_opp50_2026-0{7,8}.json`.

| Shared final half-moves | July D | July 95% interval | August D | August 95% interval |
|---|---|---|---|---|
| 0 | +0.0375 | +0.0365 to +0.0385 | +0.0369 | +0.0359 to +0.0380 |
| 2 | +0.0123 | +0.0110 to +0.0135 | +0.0132 | +0.0121 to +0.0145 |
| 4 | +0.0070 | +0.0046 to +0.0093 | +0.0065 | +0.0042 to +0.0087 |
| 6 or more | +0.0013 | −0.0062 to +0.0089 | +0.0011 | −0.0060 to +0.0087 |

A quarter of the players drop out and the curve does not move. A player adjusting to a stronger or
weaker opponent does not explain it. With this control both months meet the rule at four half-moves
and at six or more, so the memory is four half-moves by the rule, with a remainder at four that is
above zero and under 0.01. A response to who the opponent is, beyond rating, is still not excluded,
since the development rows do not carry the opponent's identity.

## The grader's self-test, and a correction to the reading above

`grade_memory.py` on both development months, 2026-11-10. `analyze_memory.py` was first extended to
compute the fall between two points of the curve over the players who have both points. Files
`results/memory_reg_2026-0{7,8}.json`, `results/graded_dev_2026-0{7,8}.json`.

| | July | August |
|---|---|---|
| D(0) − D(2), same players | +0.0223 (0.0211 to 0.0235), 236,738 players | +0.0232 (0.0220 to 0.0244), 243,010 |
| D(2) − D(4), same players | +0.0000 (−0.0021 to +0.0024), 83,351 players | +0.0022 (+0.0001 to +0.0044), 86,446 |

As first drafted the grader returned five passes on August and failed July on H3 and H5.

**Correction.** The sections above say the curve "falls with distance" through +0.013 at two
half-moves and +0.007 to +0.009 at four. Those are averages over different sets of players. Among
the players who have pairs at both distances, the effect at two and at four is the same in July and
differs by 0.002 in August. The fall from two to four in the tables is mostly a change in who is
being averaged. What the data support is narrower.

- A large effect of the opponent's last move, +0.036, falling by +0.022 to +0.023 once the last two
  half-moves are shared. This is the same in both months and within the same players.
- A remainder near +0.01 that does not clearly shrink between two and four half-moves.
- At six or more, an interval about ±0.006 wide around a value near zero. That is too wide to say
  whether the remainder has gone.

A remainder that does not shrink with distance is not what a fading reference predicts. It is what
one would see if players hold prepared lines filed under the order of moves that names an opening,
or respond to the kind of opponent that a move order reveals. Neither is a property of how decisions
are made in general. The earlier sentence that the memory is "about four to six half-moves" is
withdrawn. The supported statement is that the last move matters beyond the position it produces,
and that something smaller persists for at least four half-moves in opening positions.

**Consequence for the registration.** The second half of H3 and the whole of H5 rested on the
uncorrected reading. They are removed from the draft and reported without a bar.

## Whose move differed: the curve over all pairs

The last half-move before a decision is the opponent's, so in the curve over all pairs an even k
means the nearest differing move was the opponent's and an odd k means it was the player's own.
With pairs a day apart (July, August):

| Nearest differing move | k | D, July | D, August |
|---|---|---|---|
| Opponent's last move | 0 | +0.0411 | +0.0406 |
| Player's own last move | 1 | +0.0416 | +0.0429 |
| Opponent's move before that | 2 | +0.0128 | +0.0133 |
| Player's own move before that | 3 | +0.0166 | +0.0189 |
| Opponent's, three moves back | 4 | +0.0083 | +0.0071 |
| Five or more half-moves back | 5+ | +0.0091 | +0.0038 |

Counted in whole moves, the effect is about +0.04 one move back, +0.013 to +0.019 two moves back and
under +0.01 three moves back. At each distance a difference in the player's own move matters a
little more than a difference in the opponent's, although it lies one half-move further away. That
is what a plan would add on top of a reference, and it is small beside the common part.

## What pass 2 establishes, and what it does not

**Established on two development months, within player, with and without the time control.** In
common opening positions a player's next move depends on how the position was reached. The
dependence is largest when the opponent's last move differed (+0.036 on a baseline of 0.28) and
about a third of that when only moves two half-moves back or earlier differed (+0.012). Beyond that
the averages are lower, but see the correction in the self-test section: within the same players the
effect at four half-moves is not smaller than at two.

**For the framework.** Definition 6.2 as written, with no history beyond the state, does not
describe these choices. Nor does a reference equal to the previous position. The size is small:
history shifts about one choice in thirty at its largest.

*Corrected 2026-11-10.* This paragraph first went on to say that a reference fading with distance
fits the shape, with a memory of about four to six half-moves. The grader's self-test (above) showed
that the fall from two half-moves to four is not there within the same players. The shape is a large
effect of the last move and a small remainder that does not clearly shrink, which a fading reference
does not predict.

**Not established.**

- That this is a reference and not a carried plan. Both give a curve that falls with distance. They
  differ in what the changed move is, which has not been looked at.
- That it is not a response to the opponent. A different move order by the opponent is some evidence
  about who the opponent is, and the player may adapt to that. Opponent identity was not recorded
  and opponent rating was not controlled.
- Anything outside the first six moves of the game, where lines are memorised under names that
  depend on the order of moves.
- Any of it as a registered result. These are development months. The registered test is on a month
  not yet downloaded.

**Next, in order.** Record the opponent's digest and control for opponent rating. Classify what the
changed move is, to tell a reference from a plan. Then write the registration for a fresh month:
the four points of the curve, with the values above as the predictions and the two months' spread as
the margin.
