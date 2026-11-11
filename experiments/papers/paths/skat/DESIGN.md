# Skat: does the last game change a bid on a freshly dealt hand?

**Status: design, 2026-11-11. Development archive opened for counting only. No registration
drafted. The held-out archive is unreadable on Atlas and has not been opened.** Drafted by Claude.
Every choice below is Claude's and open to the owner. A seal needs the owner's explicit word.

## 1. Why this arena

Chess fixed the state by finding the same position twice. Poker compared hands at matched stacks.
In both, the state a player faces is partly the player's own doing, so a difference by history
can always be read as a difference in state that the analysis missed.

In Skat the hand is dealt at random before each game. What a player holds does not depend on
anything that happened before. So if the rate of bidding on a fresh hand differs with the result
of the game before, the difference is caused by the history and not by the hand. No other arena
in this line has that property.

The archive also holds its own control. About two thirds of all seats are held by four programs
(Section 3). The same test run on a program should return zero if the program's bid reads only
its cards. That the programs keep no memory of earlier games is assumed here and has not been
checked against their code.

## 2. What it does not add

This is again the weak statement that the last step matters beyond the present state. A reference
point that adapts after a win or a loss predicts it as well as a stratified manifold does. A pass
would be a cleaner version of the poker result. It would not separate the thesis from reference
dependence.

## 3. What the development archive holds

`count_basic.py` over `dev/skatgame-games-2016-05-2026.bz2`, run 2026-11-11
(`results/count_basic.json`).

- 2,620,004 games, all of which parse. They run from 2016 to 2026 at roughly 210,000 to 350,000 a
  year.
- Each record gives the time, a series number, three logins in seat order, three ratings, the
  full deal, every bid, the discard, every card and the result.
- The seat order is the bidding order. The first ten cards of the deal are forehand's, the next
  ten middlehand's, the next ten rearhand's and the last two the skat. This was read from three
  records and is to be confirmed by the miner on all of them (each card a player plays must come
  from that player's ten cards or the skat).
- Middlehand speaks first. In 1,539,866 games middlehand bid and in 1,071,180 passed. The other
  8,958 end before any bid.
- 5,180 distinct logins, 548 with 100 games or more. The twenty busiest hold 79% of all seats.
  The four busiest names are programs (`xskat`, `kermit`, `zoot`, `theCount`), each also present
  with a `:2` suffix, which marks a second connection of the same login. That these four are
  programs is taken from their names and from the server's description, and no other login has
  been classified. In 1,772,379 games at least one login carries a suffix.
- Found in development, pass 1: nearly every game is one person against two programs, so the
  people here are playing the server's programs and not each other. See `DEVELOPMENT.md`.
- Logins are not written to any committed file. The miner writes keyed digests, as in chess.

## 4. The decision and the comparison

**Decision.** Middlehand's first action, to bid 18 or to pass. It is taken before any other
player has acted in the game, so it reads only the player's ten cards and whatever the player
carries from earlier games. Each player is middlehand in one game of three.

**History.** The result of the previous game in the same series for that player. A loss as
declarer, a win as declarer, or a game spent defending. Two games belong to one chain if they
share the series number, hold the same three logins and follow one another in the record.

**Comparison, as in poker.** Within a player, the rate of bidding when the event was one game
back against the rate when it was two games back with an uneventful game between. Because the
seat rotates, the first comparison to work out in development is which lags are available for a
middlehand decision and how many decisions each has.

**Hand strength.** Not needed for an unbiased comparison, since the deal is random. It is used to
narrow the interval. Cells by number of jacks and by the count of aces and tens, to be fixed in
development.

**Control.** The same comparison on the four programs.

## 5. Things that could produce a false result

- **Who stays.** A player who leaves after a loss is not seen at lag one. The comparison is within
  player and conditions on the player being present at both lags, as the poker one did.
- **The deal is not random.** To be checked by the distribution of jacks in middlehand's cards
  against the hypergeometric one, overall and after each kind of previous result.
- **Shared logins and unlisted programs.** A login with a suffix, or one with a very large number
  of games, may be a program. Development has to fix a rule for who counts as a person before any
  rate by history is computed.
- **Scoring formats.** A series may be played to a fixed number of games with a running score, so a
  player behind late in a series may bid more for a reason that is strategy and not memory. The
  position within the series is in the record and is to enter the cells.

## 6. Order of work

1. Miner, one row per game per seat, development archive only. Confirms the seat order.
2. The rule for programs and for chains. Counts of decisions by lag.
3. The randomness check.
4. Only then the first rate by history, on development.
5. A registration draft with bars set from development, and a rehearsal. The held-out archive
   stays unreadable until a seal on the owner's word.
