# prereg-poker-recency-v1. Does a player raise less in the hand straight after a large pot?

**Status: DRAFT, 2026-11-10. Not sealed.** Drafted by Claude. Every choice below is Claude's and
open to the owner. Sealing needs the owner's explicit word after reading the bundle list in
Section 9. No action from a held-out site has been read by a program.

## 1. Question

Chess development found that a player's move depends on the opponent's last move beyond the
position it produces (`../chess/DEVELOPMENT.md`). The claim carried to poker is that, with the
present state held fixed, the most recent step changes the choice and earlier steps add little.
Poker is the first arena here with money at stake.

## 2. What development found

Three sites (Absolute Poker, Full Tilt Poker, Ongame Network), 4,217,419 hands, `DEVELOPMENT.md`.

- A comparison of hands after a large pot with hands after four quiet hands could not be trusted. Its
  sign for losses changed with the width of the stack bins, because the stack is part of the state
  and is made by the player's own recent play. No such comparison is registered here.
- A comparison that uses no quiet-hand baseline held in four specifications. Among decisions with
  exactly one large pot in the player's last four hands, the rate of raising one hand after the pot
  is 0.010 to 0.014 below the rate two hands after it, within player and state. From the second
  hand on, consecutive hands do not differ.

## 3. Data

HandHQ logs in the PHH collection, version 2, md5 `0918a30f97bda0129897b7e0f1ec895a`, no-limit
hold'em, 1 to 23 July 2009.

**Held out, each graded as a separate replication:** PokerStars (8,042,259 hands by header count),
iPoker Network (5,996,745) and PartyPoker (3,092,698). They are other sites than the development
sites, so other tables and, unless one person held accounts at two sites, other people.

**What has been read of them.** Header lines of every hand, for the count of player labels. And the
first four hands of one PokerStars file, read by eye on 2026-11-10 to learn the format before the
split existed. No statistic of any action.

## 4. Procedure, fixed

1. **Mining.** `mine_hands.py ARCHIVE OUT --sites SITE --allow-heldout`, one held-out site at a
   time. The first decision before the flop for each player in each hand, read up to the first
   board card and no further.
2. **Results of hands.** The change in a player's starting stack from one hand to the next hand
   dealt at the same table, in big blinds. A rise that lands on a whole multiple of 10 big blinds
   between 20 and 250 is treated as a possible top-up and breaks the chain. A large pot is a change
   of 10 big blinds or more in either direction. Hands are ordered within a table by the integer
   groups in the site's hand label.
3. **Decisions used.** Those with four measured results behind them at the table, exactly one of
   which was a large pot. A big blind who checks an unraised pot has made no decision.
4. **Statistic.** Within a cell (player, site, big blind, seat, number of players, whether a raise
   came before, stack bin of 0–40, 40–80, 80–120, 120–200 or over 200 big blinds), the rate of
   raising at lag j minus the rate at lag j + 1. A player's value is the mean over cells weighted by
   the smaller of the two counts. The reported number is the mean over players with a 95% interval
   from 2,000 resamples of players.

Called as `analyze_recency.py HANDS OUT 10 0 SITE`, then `grade_recency.py`.

**Why the coarse stack bins are the registered ones.** Both sides of every comparison have just been
through a large pot of the same kind, so the bias that sank the baseline comparison does not arise,
and the four specifications agreed on development. The coarse bins keep twice as many players as the
strictest specification, and PartyPoker is smaller than the development set. The choice is made for
precision and is stated as such.

## 5. Predictions, for each held-out site separately

- **H1. Raising dips in the hand straight after a large pot.** The lag 1 minus lag 2 difference,
  after a large pot of either result, has an interval below zero.
- **H2. The dip lasts one hand.** The lag 2 minus lag 3 difference has an interval inside −0.01 to
  +0.01.
- **H3. The size replicates.** The lag 1 minus lag 2 difference lies in −0.022 to −0.005.
- **H4. The dip follows wins and losses alike.** The lag 1 minus lag 2 difference is below zero after
  a large win and after a large loss, taken separately. Point estimates only, since the loss side
  had half the players on development and two of four intervals there included zero.

**What each failure would mean.**

- H1 fails on a site: the development result does not carry to that site.
- H2 fails with H1 passing: the effect reaches further back than one hand.
- H4 fails: the dip depends on the result of the pot and is not a response to having played one.

**Overall.** The claim counts as replicated if H1 passes on all three sites. Two of three is reported
as partial and is not called a replication.

## 6. Reported without a bar

- The same contrasts with stack bins 10 big blinds wide, with the table added to the cell, and both.
- The contrasts for entering the pot, which showed nothing consistent on development.
- Lag 3 minus lag 4.
- The contrasts by big blind level.
- The comparison with quiet hands, in the form used in pass 1 of development, labelled as biased.

## 7. Not claimed

A pass says that on these sites in July 2009 a player raised a little less in the one hand after a
large pot. It does not say why. A player may be distracted, the other players may treat that player
differently for a hand, or the software may delay the player's turn. It does not show a reference
point, and it says nothing about what a win or a loss does to risk taking, which published work
addresses at a threshold a hundred times larger (Smith, Levere and Kurtzman 2009; Eil and Lien 2014).

## 8. Void conditions

- **V1.** The archive's md5 differs from Section 3.
- **V2.** Fewer than 3,000 players contribute to the first contrast on a site. Development had 17,974.
- **V3.** More than 2% of a site's hands cannot be ordered because their labels hold no digits.

## 9. Bundle to seal

This file without DRAFT in its name, `mine_hands.py`, `analyze_lags.py` (for the shared constants and
rules), `analyze_recency.py`, `grade_recency.py`, `DESIGN.md`, `DEVELOPMENT.md`, and the four
development result files `results/recency_dev_*.json`. Then a hash file, a signed commit, a signed
tag `prereg-poker-recency-v1` pushed to the public repository, and only then the mining of the
held-out sites.

## 10. Before sealing

- `grade_recency.py` on the development result with the registered specification, by site, as its
  self-test. It must return H1 to H4 as passes on the pooled development sites.
- The full texts of the two prior papers, for whether either compares one hand after with two.
- Whether the hand labels order play within a table on the held-out sites. It is assumed. A check
  that needs no action: within a table, players' starting stacks should change little between
  consecutive labels far more often than between labels taken at random.
- The owner's view on H3's band, which is the weakest part of this draft.
