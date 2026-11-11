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

## Still to be reported

Section 6 of the registration lists five things to report without a bar (narrower stack bins, the
table in the cell, entering the pot, big blind levels, the biased quiet-hand comparison). They have
not been run yet.
