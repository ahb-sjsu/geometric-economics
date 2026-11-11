# A game built to collect the data: design note

**Status: proposal, 2026-11-11. Nothing built. No participant has been approached.** The owner
asked whether an online game could collect the data the thesis needs. Drafted by Claude. Every
choice below is Claude's and open to the owner. Collecting data from people needs ethics approval,
which is the owner's to seek.

## 1. Why build one

Every arena so far uses records made for another purpose. Each can test only the weakest
implication of the thesis, that the last step matters beyond the present state, and each has the
same weakness. The path a person took was their own doing or the table's, so it cannot be set.
Chess fixes the state by waiting for the same position to recur. Skat has a random deal. Poker and
taxi have neither.

A game we run can do what none of them can.

- **Assign the path at random.** Two players are brought to the same state by different routes
  that the server chose. Any difference in what they do next is caused by the route.
- **Put the strata there on purpose.** The thesis says choices move on a space made of pieces
  with boundaries between them. In found data a boundary has to be guessed. In a game it is a
  rule we wrote, so its position is known and the test is whether behaviour changes there.
- **Hold out by design.** Players, maps and weeks can be set aside before anyone plays.
- **Compare models.** The data can be shaped so that a stratified model and the standard ones
  (expected utility, prospect theory with a moving reference point) give different predictions
  for the same choice.

## 2. The game, in one paragraph

A trading game on a map. The player runs a caravan between towns, buys goods where they are
cheap and sells where they are dear. Each turn the player picks the next town. Routes differ in
length, toll, risk of loss and what can be traded at the end. A run lasts about ten minutes. This
is pathfinding in the literal sense, and every choice is an economic one. The state is small and
fully recorded: the town, the money, the cargo, the turn.

## 3. What the server controls

- **Matched arrivals.** Events on the road (a windfall, a robbery, a toll) come in scripted pairs.
  One player gains 40 and then loses 40. Another loses 40 and then gains 40. A third has neither.
  All three reach the same town on the same turn with the same money and cargo and face the same
  menu of routes. Players are assigned to scripts at random.
- **Boundaries.** Some rules change the kind of situation and not only its size. Debt (below zero
  the player pays interest and loses access to some routes). A licence tier (above a level of
  wealth new markets open). A border (goods are taxed on crossing). Each is a candidate stratum
  boundary with a known place.
- **Matched displacement.** The same change in money can be delivered within a region or across a
  boundary. If crossing costs the player more than the money explains, that is the signature the
  thesis predicts and a smooth utility does not.

## 4. The tests it would support, in the order they should be registered

1. **History beyond state, with assigned paths.** The matched arrivals of Section 3. This repeats
   the chess and poker question with the cause settled.
2. **A boundary costs more than its distance.** Choices near debt, a tier or a border against
   choices equally far in money from no boundary.
3. **Model comparison on held-out players.** A stratified least-cost model against expected
   utility and against prospect theory with an adaptive reference point, each fit on development
   players and scored on players it has not seen. This is the test the thesis has not had.

Test 3 is the one that could support the thesis itself. Tests 1 and 2 are needed first because 3
is uninterpretable if they fail.

## 5. What could go wrong

- **Play money.** People take risks with points that they would not take with pay. The run's
  final wealth should convert to a bonus, as in the correlation study.
- **Play is not work.** A player may seek excitement and not profit. Instructions and a
  comprehension check help. A public leaderboard would make it worse and is left out.
- **The player learns the scripts.** Paired events must be hidden among unpaired ones, and a
  player should meet each script once.
- **The designer's hand.** We choose where the boundaries are, so finding that behaviour changes
  at a rule we announced does not show that people's own evaluations are stratified. It shows
  they respond to the rule. The stronger version hides the boundary's place and asks whether a
  model can find it from choices. Both versions should be planned.
- **Sample size.** The poker effect was about one decision in a hundred. A game effect of that
  size would need tens of thousands of matched decisions. A pilot has to measure the size first.
- **Demand effects and bots.** Paid panels bring inattentive players and scripts. The correlation
  study's checks apply.

## 6. Two ways to get players

- **A paid panel (Prolific).** A few hundred to a few thousand people, known consent, known cost,
  quick. Fits tests 1 and 2. The repository already has a browser instrument, a payout script and
  an ethics application for the correlation study, and much of that carries over.
- **A public game.** Free to play, open to anyone, far more data over months, and the only way
  to see long histories of one person. It needs a game people want to play, hosting, a privacy
  notice, an age gate, and an ethics protocol for open enrolment. It is a much larger build.

**Recommendation.** Start with the panel version. Build the smallest game that delivers the
matched arrivals and one boundary, pilot it on a few dozen people to measure effect size and
noise, then register. Keep the public version as a later step that reuses the same engine.

## 7. What it needs from the owner

- A word to go ahead with a prototype (static page, no data collection, playable by the owner).
- A decision on pay per player and the cap, as for the correlation study.
- An ethics application or an amendment to the pending one. Claude can draft it. The owner
  submits.
- Hosting. The correlation instrument's arrangement can be reused if the owner agrees.

## 8. What can be done before any of that

- A simulator of the game with artificial players of each model class, to check that the three
  tests can tell the models apart at a feasible sample size. This uses no people and can start
  now on Atlas.
- The game rules as a specification, with the scripts and the split fixed in writing before a
  line of the page is written.
