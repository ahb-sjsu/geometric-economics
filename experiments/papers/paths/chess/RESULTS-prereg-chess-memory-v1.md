# Result of prereg-chess-memory-v1

**Run 2026-11-11 on Atlas, from a fresh clone at the signed tag `prereg-chess-memory-v1`
(commit `f287c83`).** Runner `run_sealed.sh`. Graded once. Nothing was changed after the seal.

## Order of events

1. Bundle hashes verified against `prereg-chess-memory-v1.sha256`. The October file's sha256
   matched (V1 not triggered).
2. Rehearsal of the H5 chain. August was mined again with the cloned `mine_movetime.py` and
   analysed. The output was identical byte for byte to the committed
   `results/pull_time_2026-08.json` (10:56 UTC). The H1 to H4 chain had been rehearsed the same way
   on commit `0bedf33`, and step 1 confirms its files are those that were sealed.
3. Only then was October decompressed, for the first time by any project. 95,395,628 games,
   42,602,020 rows in each mining pass. Files `results/sealed_*.json`.

## Verdicts

D(k) is the rate at which a player chose a different move in two games that reached the same
position by orders sharing their last k half-moves, minus that rate for identical orders. Own
moves in the same order, pairs at least 24 hours apart. Intervals are 95%, from 2,000 resamples of
players.

| Prediction | Bar | October | Verdict |
|---|---|---|---|
| **H1** history matters with the position fixed | D(0) interval above +0.02 | +0.0371 (+0.0363 to +0.0380), 442,555 players | **pass** |
| **H2** it matters beyond the last move | D(2) interval above +0.005 | +0.0126 (+0.0116 to +0.0136), 284,058 players | **pass** |
| **H3** the last move carries most of it | D(0) − D(2) interval above +0.015 | +0.0235 (+0.0223 to +0.0247), 252,956 players | **pass** |
| **H4** the values replicate | D(0) in +0.031 to +0.041, D(2) in +0.008 to +0.017, D(4) in +0.003 to +0.013 | +0.0371, +0.0126, +0.0064 | **pass** |
| **H5** a move played in no time is drawn to the earlier move, a slower one to the last | at bullet, blitz and rapid, zero-second pull below zero and slower pull above zero | table below | **pass** |

The rate of changing the move between identical orders was 0.279. No void condition was triggered:
442,555 players contribute to D(0) against a floor of 50,000, and 101,760 to D(4) against 5,000.

**H5, the pull in king steps.**

| Speed | Zero-second moves | Moves of two seconds or more | Slower minus zero, same players |
|---|---|---|---|
| Bullet | −0.073 (−0.076 to −0.071), 107,044 players | +0.076 (+0.068 to +0.084), 42,628 | +0.153 (+0.141 to +0.166) |
| Blitz | −0.075 (−0.079 to −0.072), 77,173 | +0.067 (+0.063 to +0.071), 186,688 | +0.142 (+0.133 to +0.152) |
| Rapid | −0.071 (−0.084 to −0.057), 6,775 | +0.060 (+0.055 to +0.065), 125,974 | +0.142 (+0.116 to +0.168) |

The smallest set has 6,775 players against V3's floor of 1,000.

**Against development.** August gave D(0) +0.0360, D(2) +0.0129 and D(4) +0.0069. October gives
+0.0371, +0.0126 and +0.0064. For H5 the six October values are each within 0.016 of August's.

## What has to be said beside the verdicts

- **Players overlap with the development months.** The registration said so. This is a replication
  on new games, not on new people.
- **Part of D(0) is early choice.** The curve on moves that took two seconds or more, reported
  below, puts D(0) at +0.0326 against +0.0371 over all moves. About an eighth of the registered
  effect of the last move goes when zero-second moves are removed.
- **On slower moves alone H2 would not quite have cleared its bar.** D(2) there is +0.0070 with an
  interval from +0.0049, against a bar of +0.005. The bar applies to the registered curve, which
  passed. The slower moves are the cleaner measure of history at a fixed position, so the
  statement "it matters beyond the last move" is firm for all moves and marginal for slow ones.
- **H5 takes a zero-second move to be one entered in advance.** The rows do not say so.
- **Not claimed,** as registered. The result does not show a moving reference as against a carried
  plan. It covers common opening positions on one site. It says nothing about money.

## Reported without a bar (Section 6 of the registration)

**D(2) − D(4) and D at five or more half-moves.** D(2) − D(4) over the same players is +0.0022
(+0.0001 to +0.0042). D with five or more shared half-moves is +0.0106 (+0.0046 to +0.0164), on
12,276 players. On development the same quantity was not distinguishable from zero. Here it is, and
it is not smaller than D(4). The effect does not clearly fade between two half-moves and five.

**Opponents rated within 50 points in the two games of a pair.** D(0) +0.0374 (+0.0364 to +0.0385),
D(2) +0.0133 (+0.0121 to +0.0146), D(4) +0.0070 (+0.0046 to +0.0092). The curve is unchanged, so a
player adapting to a stronger or weaker opponent does not produce it.

**All pairs, including those where the player's own order differed.** D at k of 0 to 5 is +0.0418,
+0.0422, +0.0130, +0.0182, +0.0066 and +0.0099. As on development, a difference in the player's own
move (odd k) counts a little more than a difference in the opponent's one half-move nearer.

**By time spent on the move.**

| | All moves | Two seconds or more | Zero seconds |
|---|---|---|---|
| Rate of changing the move, identical orders | 0.279 | 0.385 | 0.138 |
| D(0) | +0.0371 | +0.0326 (+0.0310 to +0.0342) | +0.0507 (+0.0494 to +0.0521) |
| D(2) | +0.0126 | +0.0070 (+0.0049 to +0.0094) | +0.0125 (+0.0112 to +0.0140) |
| D(4) | +0.0064 | +0.0038 (−0.0014 to +0.0090) | +0.0089 (+0.0065 to +0.0113) |
| D(0) − D(2), same players | +0.0235 | +0.0253 (+0.0224 to +0.0282) | +0.0373 (+0.0354 to +0.0392) |

**The pull at classical speed.** Among moves of two seconds or more it is +0.110 (+0.082 to
+0.137), on 4,193 players. Zero-second moves are too few to report (39 players).

**By speed, by rating band and against different opponents, written after the result.** The
sealed code could restrict by speed but not by rating or opponent. `analyze_memory_split.py` and
`run_split.sh` were written on 2026-11-11 after H1 to H5 were graded. They import the registered
functions unchanged and apply one filter to every class of pair, the baseline included. The four
rating bands were chosen then, before any curve by band was computed. A band is the mover's rating
in that game (`results/sealed_split_*.json`).

| Subset | Players at D(0) | D(0) | D(2) | D(4) | D(5 or more) |
|---|---|---|---|---|---|
| Pairs against different opponents | 441,031 | +0.0372 (+0.0364 to +0.0380) | +0.0126 (+0.0116 to +0.0136) | +0.0065 (+0.0047 to +0.0084) | +0.0104 (+0.0045 to +0.0161) |
| Bullet | 135,531 | +0.0477 (+0.0464 to +0.0492) | +0.0171 (+0.0155 to +0.0185) | +0.0083 (+0.0055 to +0.0110) | +0.0120 (+0.0032 to +0.0209) |
| Blitz | 235,495 | +0.0339 (+0.0328 to +0.0350) | +0.0109 (+0.0096 to +0.0123) | +0.0061 (+0.0037 to +0.0087) | +0.0136 (+0.0055 to +0.0218) |
| Rapid | 97,860 | +0.0280 (+0.0260 to +0.0299) | +0.0079 (+0.0052 to +0.0108) | +0.0017 (−0.0041 to +0.0074) | +0.0004 (−0.0169 to +0.0185) |
| Classical | 2,206 | +0.0284 (+0.0143 to +0.0425) | −0.0185 (−0.0372 to +0.0015) | −0.0008 (−0.0381 to +0.0370) | +0.0385 (−0.0347 to +0.1229) |
| Rated under 1400 | 139,613 | +0.0318 (+0.0302 to +0.0334) | +0.0104 (+0.0081 to +0.0127) | +0.0034 (−0.0021 to +0.0084) | +0.0130 (−0.0037 to +0.0297) |
| Rated 1400 to 1799 | 179,166 | +0.0394 (+0.0381 to +0.0407) | +0.0134 (+0.0118 to +0.0151) | +0.0067 (+0.0034 to +0.0098) | +0.0107 (+0.0007 to +0.0208) |
| Rated 1800 to 2199 | 118,960 | +0.0388 (+0.0374 to +0.0402) | +0.0143 (+0.0128 to +0.0160) | +0.0099 (+0.0072 to +0.0125) | +0.0149 (+0.0060 to +0.0245) |
| Rated 2200 and over | 25,760 | +0.0395 (+0.0366 to +0.0423) | +0.0100 (+0.0071 to +0.0129) | +0.0072 (+0.0025 to +0.0117) | +0.0091 (−0.0069 to +0.0249) |

- **Different opponents.** The curve is the registered one to the third decimal. Rematches against
  one opponent do not produce it.
- **Speed.** D(0) falls from bullet to blitz to rapid. Pass 9 of development found that moves made
  in no time raise D(0), and bullet has the most of them, so this ordering is at least partly that
  mixture and is not evidence that faster play has a longer memory. In rapid D(4) is not
  distinguishable from zero. Classical has too few players to read beyond D(0).
- **Rating.** D(0) is present in every band and is somewhat lower under 1400 than above. D(2) is
  present in every band. The effect is not confined to weak or to strong players.
- **D(5 or more)** is above zero in bullet, blitz, the two middle bands and the different-opponent
  subset, and unresolved elsewhere. The reach beyond four half-moves reported above is not the
  product of one subset.
