# prereg-chess-memory-v1. How far back does history reach in a chess player's choice of move?

**Status: SEALED 2026-11-11.** Drafted by Claude on 2026-11-10. The owner gave the word to seal on
2026-11-11 ("seal when ready and proceed"). Every choice below is Claude's. At the seal the held-out
month was on Atlas, checksummed and unopened. The hashes are in `prereg-chess-memory-v1.sha256`.

## 1. Question

`geometric-methods` Chapter 6 makes a decision a least-cost path from the present state to a goal.
As written, that depends on the present state and on nothing before it
(`../lean/DecisionPaths.lean`, `best_continuation_history_free`). If instead each cost reads a
reference that moves with the past, history matters through that reference and nothing else
(`ranking_depends_on_state_and_reference`), and a reference that reads back m steps cannot tell
apart two histories that share their last m steps.

Chess gives the state exactly. This study measures, for one player at one position, how the chance of
choosing a different move depends on how many final half-moves two of that player's games share.

## 2. What development found

July and August 2026, every rated standard game, `DEVELOPMENT.md`. With pairs of games at least 24
hours apart and the player's own moves in the same order in both games:

| Shared final half-moves k | July D(k) | August D(k) |
|---|---|---|
| 0 | +0.0363 | +0.0360 |
| 2 | +0.0123 | +0.0129 |
| 4 | +0.0084 | +0.0069 |
| 6 or more | +0.0044 | +0.0000 |

D(k) is the rate of changing move between two games sharing their last k half-moves, minus the rate
between two games with identical move orders.

## 3. Data

**Held out: October 2026**, `lichess_db_standard_rated_2026-10.pgn.zst` from
`database.lichess.org`, CC0, sha256 `043906ebfade1bfeb7c00087590fac505370936c028525e4722e2dbd4986ae86`
as published by Lichess. Downloaded to Atlas on 2026-11-10 and not decompressed. No project has read
it. September 2026 is left untouched as a reserve.

**Not held out:** June 2026 (an incomplete file), July and August 2026 (development here, and
evaluation months of gate G7a of `geometric-evaluation-theory`).

**Players overlap between months.** A player's habits in October are not independent of July. The
test is therefore a replication on new games, not on new people, and is described that way.

## 4. Procedure, fixed

1. **Targets.** `results/targets.tsv` as it stands: 6,039 move orders reaching the positions that had
   two usable orders in the 4% July sample. It is not rebuilt from October.
2. **Mining.** `mine_targets.py` over every game of October. Program accounts are dropped. Games
   with a time control whose estimated length is under 30 seconds are dropped at analysis.
3. **Pairs.** For each player, position and speed category, every pair of that player's games, at
   most 40 games per cell chosen by the seeded generator in `analyze_memory.py`. Pairs less than 24
   hours apart are dropped. Pairs where the player's own moves came in a different order are
   dropped. k is the number of final half-moves the two orders share, with 6 or more pooled.
4. **Statistic.** D(k) as in Section 2, one value per player (the mean over that player's
   positions), averaged over players who have at least one identical-order pair and one pair at k.
   Intervals are 95% percentile intervals from 2,000 resamples of players.

The code is `mine_paths.py`, `mine_targets.py`, `analyze_paths.py` (for the speed categories) and
`analyze_memory.py` at the sealed commit, called as `analyze_memory.py ROWS OUT 24`.

5. **Second pass, for H5 and for the curves by time spent.** `mine_movetime.py` over every game of
   October. It is the registered miner with one more column, the mover's clock after the chosen
   move. The time spent on a move is the clock before it, minus the clock after it, plus the
   increment, in whole seconds. `analyze_pull_time.py ROWS OUT` then gives the pull defined in
   `DEVELOPMENT.md`, pass 7, for moves of zero seconds and for moves of two seconds or more. Moves
   of one second are left out. H1 to H4 use the first pass only.

## 5. Predictions

Each stands alone.

- **H1. History matters with the position fixed.** D(0) has an interval above +0.02.
- **H2. It matters beyond the last move.** D(2) has an interval above +0.005.
- **H3. The last move carries most of it.** D(0) − D(2), over players who have pairs of both kinds,
  has an interval above +0.015.
- **H4. The values replicate.** D(0) lies in +0.031 to +0.041, D(2) in +0.008 to +0.017, and D(4) in
  +0.003 to +0.013. Each band is the mean of the two development months plus or minus 0.005, which
  is several times the difference between those months.

- **H5. A move played in no time is drawn to the opponent's earlier move, and a slower move to the
  last one.** Added 2026-11-11 from passes 7 and 8 of development. In each of bullet, blitz and
  rapid, the pull among zero-second moves has an interval below zero, and the pull among moves of
  two seconds or more has an interval above zero. H5 passes if both hold at all three speeds. On
  August the six values were −0.074, −0.074 and −0.086, and +0.071, +0.067 and +0.062. H5 rests on
  one development month. It is graded by `grade_pull.py` and is not part of H1 to H4.

**What each failure would mean.**

- H5 fails: the direction found in August does not replicate, and the reading that a zero-second
  move was chosen before the opponent's last move loses its support.
- H1 fails with an interval inside ±0.01: the development result does not replicate, and Definition
  6.2 as written stands in this arena.
- H2 fails while H1 passes: a reference equal to the previous position is enough.
- H3 fails: the effect is not concentrated in the last move.

**Removed after the grader's self-test, 2026-11-10.** The first draft also predicted that D falls from
two half-moves to four, and that D at six or more is zero within ±0.01. On the development months the
fall from two to four, taken over the same players, was +0.0000 in July and +0.0022 in August, and
the interval at six or more is about ±0.006 wide, which cannot separate zero from the value at four.
Both statements came from comparing averages over different players (`DEVELOPMENT.md`, "The
grader's self-test"). Neither is predicted here. Both quantities are reported without a bar.

## 6. Reported without a bar

- D(2) − D(4) over players who have both, and D at six or more half-moves.
- The same curve with opponents rated within 50 points of each other in the two games of a pair
  (`analyze_memory.py ROWS OUT 24 50`).
- The curve over all pairs, including those where the player's own order differed, at each k from 0
  to 5.
- The curve by speed category and by rating band.
- The curve with pairs restricted to different opponents, which October's rows allow and the
  development months' do not.
- The curve on moves of two seconds or more and the curve on zero-second moves
  (`analyze_memory_time.py`). On August, D(0) among moves of two seconds or more was +0.032 against
  +0.036 over all moves (`DEVELOPMENT.md`, pass 9).
- The pull at classical speed, and the difference in pull between the two kinds of move within
  the same players.

## 7. Not claimed

A pass says that in common opening positions on one site a player's move depends on the recent
order of moves, with a memory of a few half-moves. It does not show that the cause is a moving
reference and not a carried plan or a response to the opponent's identity. Pass 8 of development
found that a move played in zero seconds behaves as if chosen before the opponent's last move. For
such a move the position was not fixed at the time of choosing, so D(0) over all moves includes
some early choice along with memory. Pass 9 puts that share at about a tenth on August, and the
curve on slower moves is reported beside the registered one. It says nothing about
positions later in the game, about other games, or about economic choice. Whether the same depth
appears in Deal or No Deal and in poker is the subject of later registrations.

## 8. Void conditions

- **V1.** The October file's sha256 differs from Section 3.
- **V2.** Fewer than 50,000 players contribute to D(0), or fewer than 5,000 to D(4). The development
  months had about 413,000 and 96,000.
- **V3, for H5 only.** Fewer than 1,000 players in either set of moves at any of the three speeds.
  August's smallest set had 6,502.

## 9. Bundle to seal

This file, `mine_paths.py`, `mine_targets.py`, `analyze_paths.py`, `analyze_memory.py`,
`grade_memory.py`, `results/targets.tsv`, `DEVELOPMENT.md`, the development results
`results/memory_reg_2026-07.json`, `results/memory_reg_2026-08.json` and
`results/pull_time_2026-08.json`, and for H5 and the curves by time spent `mine_movetime.py`,
`analyze_pull.py`, `analyze_pull_time.py`, `analyze_memory_time.py` and `grade_pull.py`.
`seal_chess.py` lists them and writes the hash file. Then a signed commit, a signed tag
`prereg-chess-memory-v1` pushed to the public repository, and only then the run.

## 10. Before sealing

- `grade_memory.py` is written and was run on both development months (2026-11-10). After the
  removals above it must return H1 to H4 as passes on both. Rerun it to confirm.
- Run the full chain on a development month from a fresh clone of the sealed commit on Atlas.
- Decide whether H4's bands are too generous or too tight. They are the weakest part of this draft.
- Prior art: a test of history with the position held fixed was not found in the check of
  2026-11-09. Repeat the search for work on move-order effects before sealing.

**Progress on this list, 2026-11-11.**

- Prior art, search repeated. Still no study found that holds the position fixed and tests whether
  the order of the moves that reached it changes the next move. The nearest work found is on other
  questions: Salant, Spenkuch and Almog use Lichess games to show that a player's opening experience
  in standard chess carries into Chess960, and Lappo, Rosenberg and Feldman (Proc. R. Soc. B 2023)
  study how the popularity of opening moves spreads among masters. Both were read as search
  summaries only, not in full. A web search is not proof of absence.
- Rehearsal from a fresh clone. `run_rehearsal.sh` clones the public repository on Atlas, mines
  August 2026 with the cloned code and the committed targets, runs the registered analysis and the
  grader, and compares both outputs byte for byte with the committed files. Started 2026-11-11 on
  commit `0bedf33`. Its outcome is recorded below when it ends. A rehearsal on the sealed commit
  itself is still owed if any bundled file changes before the seal.
- **Rehearsal outcome, 2026-11-11.** The run on commit `0bedf33` started at 02:17 UTC, finished
  mining August at 04:29 and ended at 04:46. The analysis output is identical byte for byte to the
  committed `results/memory_reg_2026-08.json`, and the grader's output is identical to the committed
  `results/graded_dev_2026-08.json`. The registered chain therefore reproduces its development
  result from the public repository alone, given the month's file and the key for player digests.
  No bundled file has changed since that commit. `mine_movetime.py`, added later for a development
  pass, is a separate file and leaves the registered miner untouched.

**Settled at the seal, 2026-11-11.**

- **H4's bands are unchanged.** The owner was told they were the weakest part and did not comment.
- **H5 was added on the day of the seal,** from two development passes run that day. Its files are
  new and no file of the H1 to H4 chain was changed, so the rehearsal above still covers that
  chain. `grade_pull.py` returns a pass on the August development file
  (`results/graded_pull_dev_2026-08.json`).
- **Still owed after the seal and before October is opened:** a rerun of the H5 chain on August
  from a fresh clone at the sealed tag, compared with the committed
  `results/pull_time_2026-08.json`. The sealed run does this first and stops if it differs.
