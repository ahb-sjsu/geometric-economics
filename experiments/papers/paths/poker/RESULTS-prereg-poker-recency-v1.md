# Result of prereg-poker-recency-v1

**Run 2026-11-11 on Atlas, from a fresh clone at the signed tag `prereg-poker-recency-v1`
(commit `38a51f5`).** Runner `run_sealed.sh`. Graded once. Nothing was changed after the seal.

## Order of events

1. Bundle hashes verified against `prereg-poker-recency-v1.sha256`. Archive md5 matched (V1 not
   triggered).
2. Rehearsal. The development sites were mined and analysed again with the cloned code. The output
   was identical byte for byte to the committed `results/recency_dev_coarse.json` (08:44 UTC).
3. Only then were PokerStars and PartyPoker mined, analysed and graded. Files
   `results/sealed_recency_PS.json`, `results/sealed_graded_PS.json` and the same for PTY.

## Verdicts

| | PokerStars | PartyPoker |
|---|---|---|
| Hands mined | 8,042,259 | 3,092,698 |
| Players in the first contrast | 39,272 | 10,732 |
| **H1** raising dips in the hand straight after a large pot | **pass** | **pass** |
| Lag 1 minus lag 2 | −0.0101 (−0.0132 to −0.0071) | −0.0058 (−0.0115 to −0.0005) |
| **H2** the dip lasts one hand | **pass** | **pass** |
| Lag 2 minus lag 3 | +0.0017 (−0.0014 to +0.0048) | −0.0021 (−0.0079 to +0.0034) |
| **H3** the size lies in −0.022 to −0.005 | **pass** | **pass** |
| **H4** below zero after a win and after a loss | **pass** | **pass** |
| After a large win | −0.0106 (−0.0141 to −0.0070) | −0.0102 (−0.0168 to −0.0035) |
| After a large loss | −0.0003 (−0.0057 to +0.0049) | −0.0032 (−0.0122 to +0.0055) |
| Lag 3 minus lag 4, no bar | 0.0000 (−0.0030 to +0.0031) | +0.0042 (−0.0015 to +0.0099) |

Intervals are 95%, from 2,000 resamples of players. No void condition was triggered. Both sites
are far above the 3,000 players of V2.

**By the registration's rule the claim counts as replicated,** since H1 passes on both sites. On
two sites that were not used in development, a player raised about 0.006 to 0.010 less often in the
one hand after a large pot than in the hand after that, and from the second hand on consecutive
hands did not differ.

## What has to be said beside the verdicts

- **PartyPoker passes H1 and H3 narrowly.** Its interval ends at −0.0005, and its estimate of
  −0.0058 is just inside H3's upper edge of −0.005. Its effect is about half the development
  estimate of −0.012. PokerStars, the larger site, is close to the development value.
- **H4 passes on point estimates, as registered, and the loss side is weak.** After a large loss
  the estimate on PokerStars is −0.0003 with an interval centred on zero. The dip is clear after a
  win on both sites and is not shown after a loss on either. The registration's reading of an H4
  pass, that the dip does not depend on the result of the pot, is **not supported by these
  numbers**, even though the bar as written was met. The plainer description is a dip after
  winning a large pot.
- **H2's band was widened before the seal** from ±0.01 to ±0.015. Both sites would also have passed
  the narrower band.
- **The miner set aside 256,459 PokerStars records** that failed its validity rule (a missing or
  malformed line, or blinds and stacks that do not match the number of players), beside the
  8,042,259 it used. That is 3.1% of the site's 8,298,718 records. The registered count of
  8,042,259, made from header lines before the seal, equals the number the run used.
  On the development sites the rule set aside 507 of 4.2 million, and on PartyPoker none. Why
  PokerStars has more has not been looked into. None of them has an unknown stack.
- **Not claimed,** as registered. The result does not say why. It does not show a reference point.
  The two prior papers on poker were not read in full, so whether this comparison is new is open.

## Reported without a bar (Section 6 of the registration)

Run 2026-11-11 with the code at the sealed tag, after the verdicts. Files
`results/sealed_s6_*.json`.

**The first contrast for raising under the other three specifications.** Lag 1 minus lag 2 after a
large pot of either result.

| Specification | PokerStars | PartyPoker |
|---|---|---|
| Registered: coarse stack bins | −0.0101 (−0.0132 to −0.0071) | −0.0058 (−0.0115 to −0.0005) |
| Stack bins 10 big blinds wide | −0.0057 (−0.0102 to −0.0014) | −0.0075 (−0.0152 to +0.0004) |
| Coarse bins, table in the cell | −0.0096 (−0.0137 to −0.0057) | −0.0101 (−0.0170 to −0.0030) |
| Narrow bins, table in the cell | −0.0041 (−0.0107 to +0.0024) | −0.0088 (−0.0204 to +0.0025) |

All eight estimates are below zero. Five of the eight intervals exclude zero. The three that
include it are the specifications that keep the fewest players.

**Lag 2 minus lag 3 under the strictest specification** is −0.0068 (−0.0133 to +0.0004) on
PokerStars and −0.0093 (−0.0203 to +0.0022) on PartyPoker. Under the other specifications it is
within 0.005 of zero on both sites. So "the dip lasts one hand" holds in three specifications and
is less clear in the fourth, where both sites lean the same way.

**Entering the pot.** Nothing consistent, as on development. Under the registered specification
the lag 1 minus lag 2 difference is +0.0010 (−0.0036 to +0.0053) on PokerStars and +0.0089
(+0.0015 to +0.0164) on PartyPoker. The PartyPoker value does not hold with narrow stack bins.

**After a win and after a loss, across specifications.** After a win the estimate for raising is
below zero in all eight cells. After a loss it is below zero in all eight as well, from −0.0003 to
−0.0112, and every one of those intervals includes zero.

**The comparison with quiet hands, labelled biased in the registration.** Raising after a large pot
against raising after four quiet hands, stack bins 10 big blinds wide.

| Hands since the pot | PokerStars, after a win | PartyPoker, after a win | PokerStars, after a loss | PartyPoker, after a loss |
|---|---|---|---|---|
| 1 | −0.0342 | −0.0344 | −0.0055 | −0.0069 |
| 2 | −0.0212 | −0.0215 | +0.0036 | −0.0020 |
| 3 | −0.0172 | −0.0171 | −0.0034 | −0.0016 |
| 4 | −0.0147 | −0.0149 | −0.0021 | −0.0039 |

The two sites agree to the third decimal after a win. This comparison mixes the effect of the pot
with the effect of the larger stack a win leaves, which is why it was not registered. It is shown
because the drop from the first hand to the second, −0.013 on both sites after a win, is the
quantity the registered contrast isolates.

**By big blind level, written after the result.** The sealed code had no option for it.
`analyze_recency_bb.py` and `run_bb.sh` were written on 2026-11-11 after H1 to H4 were graded.
They call the registered analysis unchanged on the hands within one range of big blind. The three
ranges were chosen from the counts of rows by big blind on the two sites, before any contrast by
level was computed. Raising, lag 1 minus lag 2, either kind of pot (`results/sealed_bb_*.json`).

| Big blind | PokerStars | players | PartyPoker | players |
|---|---|---|---|---|
| under 1 dollar | −0.0097 (−0.0132 to −0.0062) | 30,044 | −0.0051 (−0.0121 to +0.0016) | 7,860 |
| 1 to under 5 dollars | −0.0106 (−0.0177 to −0.0039) | 8,493 | −0.0056 (−0.0178 to +0.0069) | 2,045 |
| 5 dollars and over | −0.0123 (−0.0258 to +0.0010) | 2,369 | −0.0027 (−0.0158 to +0.0099) | 1,647 |

All six estimates are below zero. Two of the six intervals exclude zero, both on PokerStars. The
estimate does not shrink as the stakes rise on PokerStars, and no trend can be read on PartyPoker
at these widths. So the data give no sign that the dip belongs only to small-stakes play, and they
cannot show that it holds at high stakes either. After a win alone the six estimates run from
−0.0056 to −0.0166 and are all below zero. After a loss they run from −0.0092 to +0.0099 with every
interval including zero.

**The check raised on 2026-11-11 by the Skat development, now run.** A comparison of this shape,
run on short sequences, gave non-zero differences for card-playing programs whose raw rates were
flat (`../skat/DEVELOPMENT.md`). The registered poker contrast selects on a large pot in the
previous hands, and a hand in which a player raised is more likely to become a large pot, so a
bias of the same kind could enter here. The check passes simulated players with no memory through
the registered code unchanged (`null_sim.py`, `run_null.sh`, `null_raw.py`). Each simulated player
is one measured PokerStars player's counts of actions (143,815 players, 46.8 million hands). Every
action is drawn independently of the past, and the change in stack is drawn from the measured
changes for that action, so raising leads to large pots as often as in the data. The seat moves
round the table each hand. Two simulated sets, about 5.29 million decisions and 45,000 players in
each first contrast.

| Raising, after any large pot | PokerStars, sealed | Simulated, set 1 | Simulated, set 2 |
|---|---|---|---|
| Lag 1 minus lag 2 | −0.0101 (−0.0132 to −0.0071) | +0.0003 (−0.0027 to +0.0033) | +0.0017 (−0.0012 to +0.0046) |
| Lag 2 minus lag 3 | +0.0017 (−0.0014 to +0.0048) | +0.0001 (−0.0028 to +0.0029) | −0.0031 (−0.0061 to −0.0001) |
| Lag 3 minus lag 4 | 0.0000 (−0.0030 to +0.0031) | +0.0011 (−0.0018 to +0.0040) | −0.0011 (−0.0039 to +0.0018) |
| Lag 1 minus lag 2 after a large win | −0.0106 (−0.0141 to −0.0070) | −0.0007 (−0.0042 to +0.0031) | −0.0023 (−0.0060 to +0.0014) |

- **Players with no memory do not produce the sealed dip.** Both simulated values of the first
  contrast are near zero and of the other sign, and their intervals end far above −0.0101.
- The simulation bounds a bias of this kind at about three thousandths either way, the width of
  its intervals. The PokerStars estimate is three times that. The PartyPoker estimate of −0.0058
  is not, so on PartyPoker this check does not settle whether a bias of that size is present.
- Of the 36 simulated intervals (two sets, raising and entering, three kinds of pot, three pairs
  of lags) two exclude zero, both just, which is what chance gives.
- A first version kept every simulated player in one seat. The registered analysis compares
  within a seat, so that put consecutive hands in the same cell, which real play never does. It
  returned about −0.005 at every pair of lags with flat raw rates
  (`results/null_fixedseat_recency_1.json`). It shows the estimator can be biased when a cell
  holds consecutive hands. It is not a measure of the bias in the data.
- What the simulation leaves out: tables with several players, play that depends on the seat,
  and a style that drifts between stays at a table. None of these has been tested.

The verdicts above stand as graded and are not changed by this check.
