# prereg-chess-memory-v1. How far back does history reach in a chess player's choice of move?

**Status: DRAFT, 2026-11-10. Not sealed.** Drafted by Claude. Every choice below is Claude's and
open to the owner. Sealing needs the owner's explicit word after reading the bundle list in
Section 9. The held-out month is on Atlas, checksummed and unopened.

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

## 5. Predictions

Each stands alone.

- **H1. History matters with the position fixed.** D(0) has an interval above +0.02.
- **H2. It matters beyond the last move.** D(2) has an interval above +0.005.
- **H3. The last move carries most of it.** D(0) − D(2), over players who have pairs of both kinds,
  has an interval above +0.015.
- **H4. The values replicate.** D(0) lies in +0.031 to +0.041, D(2) in +0.008 to +0.017, and D(4) in
  +0.003 to +0.013. Each band is the mean of the two development months plus or minus 0.005, which
  is several times the difference between those months.

**What each failure would mean.**

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

## 7. Not claimed

A pass says that in common opening positions on one site a player's move depends on the recent
order of moves, with a memory of a few half-moves. It does not show that the cause is a moving
reference and not a carried plan or a response to the opponent's identity. It says nothing about
positions later in the game, about other games, or about economic choice. Whether the same depth
appears in Deal or No Deal and in poker is the subject of later registrations.

## 8. Void conditions

- **V1.** The October file's sha256 differs from Section 3.
- **V2.** Fewer than 50,000 players contribute to D(0), or fewer than 5,000 to D(4). The development
  months had about 413,000 and 96,000.

## 9. Bundle to seal

This file without DRAFT in its name, `mine_paths.py`, `mine_targets.py`, `analyze_paths.py`,
`analyze_memory.py`, `results/targets.tsv` (to be fetched from Atlas and committed),
`DEVELOPMENT.md`, and a grader `grade_memory.py` holding the bars of Section 5, which is not yet
written. Then a hash file, a signed commit, a signed tag `prereg-chess-memory-v1` pushed to the
public repository, and only then the run.

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
