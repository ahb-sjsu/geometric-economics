# Poker: does what just happened matter beyond the state of the hand?

**Status: DRAFT design, 2026-11-10. Development assignment fixed below before any action was read
by a program. Nothing sealed.** Choices are Claude's and open to the owner.

## 1. The question carried over from chess

Chess development (`../chess/DEVELOPMENT.md`) found that a player's move depends on the opponent's
last move beyond the position it produces, with a smaller remainder from earlier moves that does not
clearly shrink. Definition 6.2 of `geometric-methods` Chapter 6, read as written, allows neither
(`../lean/`). The claim to carry across arenas is the narrow one that survived:

> With the present state held fixed, the most recent step changes the choice, and it carries more of
> the effect than the steps before it.

Poker is the first arena here where the stake is money.

## 2. Data and the split, fixed now

HandHQ logs in the PHH collection, version 2 (`poker-hand-histories-v2.zip`, md5 `0918a30f…`, on
Atlas). No-limit hold'em, six sites, 1 to 23 July 2009, 21,349,121 hands with complete header lines,
276,628 player labels that persist across tables and days (`results/labels.json`).

| Role | Sites (folder prefix) | Hands counted from header lines |
|---|---|---|
| **Development** | Absolute Poker (ABS), Full Tilt Poker (FTP), Ongame Network (ONG) | 1,270,658 + 1,299,362 + 1,647,399 |
| **Held out, three separate replications** | PokerStars (PS), iPoker Network (IPN), PartyPoker (PTY) | 8,042,259, 5,996,745, 3,092,698 |

The counts are from `results/labels.json`. An earlier note in `../DESIGN.md` gave the PokerStars and
PartyPoker figures the other way round, as a web summary of the record had them. The folder counts
here are the ones to trust.

Held-out sites are other sites, so by construction other tables and, unless one person held accounts
at two sites, other people. That is stronger than the chess design, where the held-out month has the
same players.

**What has been read of the held-out sites.** Header lines of every hand, for the label count. And
the first four hands of one PokerStars file at the $0.25 big blind, read by eye on 2026-11-10 to
learn the format, before this split existed. No statistic of any action has been computed on any
site.

## 3. What is observed and what is not

Each hand gives the blinds, every player's stack at the start, every action with its amount, the
board, and a label for each player and table. A player's cards appear only if shown at showdown.

**The hidden cards do not bias this design.** Cards are dealt at random and are independent of
anything that happened in earlier hands. A comparison of one player's choices after different recent
events therefore compares the same distribution of cards. What cannot be done is to condition on the
cards, and nothing below does.

**Time of day is blank.** Order comes from the hand number within a table.

## 4. The state, the choice and the history

- **Choice.** A player's first decision before the flop when it is a real decision: fold, call or
  raise. Two indicators: entered the pot voluntarily (call or raise), and raised. A big blind who
  checks an unraised pot has made no choice and is left out.
- **State, held fixed by stratifying.** Seat relative to the blinds, number of players dealt in,
  whether a raise came before the player's turn, the player's stack in big blinds (in bins), the
  big blind level, and the site.
- **History.** The result of the player's previous hands at the same table, each measured as the
  change in the player's starting stack from one hand to the next, in big blinds. Using the stack
  change avoids reconstructing pots from actions. A hand after which the player's stack was topped up
  or the player left the table has no measurable result and breaks the chain.
- **Recent events compared.** A large loss (the stack fell by at least 10 big blinds), a large win
  (rose by at least 10), or neither. Thresholds are fixed here. Other thresholds are reported, not
  searched.

## 5. Quantities

Within a player and a state stratum, the rate of entering the pot after a given event j hands back,
minus the rate when the last four hands held no large win or loss, with the more recent hands also
free of large events so that one event is isolated at one lag. This gives two curves, one for losses
and one for wins, over lags 1 to 4. Averaged over players who have both kinds of hand in a stratum,
with intervals from resampling players. The same for the rate of raising.

**What the chess result predicts here, written before any poker action is read.**

1. The lag-1 point differs from zero for at least one of the two events.
2. The lag-1 point is larger in size than the lag-2 point, over the same players.
3. No prediction is made about the sign. Published work on online poker reports looser play after
   large losses (Smith, Levere and Kurtzman 2009, Management Science; to be verified before sealing),
   so a positive sign after a loss would repeat a known result and is not counted as support for
   anything new.

**A confound to design against, known in advance.** After a large win the stack is larger, and stack
size changes correct play. Stratifying on the stack removes the mechanical part. After a large loss
some players top up to the table maximum, which resets the stack and is excluded by the chain rule
above. What remains uncontrolled is that the other players at the table have also just seen the
event and may play differently against that player.

## 6. Order of work

1. `mine_hands.py`: one row per player per hand for the development sites only. It reads actions
   only up to the flop. A guard refuses any path belonging to a held-out site.
2. Development on the three small sites. Every analysis tried is recorded in `DEVELOPMENT.md`.
3. A grader with bars from development, self-tested on the development sites.
4. Prior art: play after wins and losses in online poker, and any within-player lag analysis.
5. The owner's word, then the seal, then the three held-out sites, each graded separately.
