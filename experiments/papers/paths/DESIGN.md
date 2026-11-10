# Decisions as paths on a stratified space: a new start

**Status: DRAFT, 2026-11-09. Nothing sealed, no data file opened, no code written.**
The owner asked on 2026-11-09 to start over: dimensions discovered and not tuned by hand, and the
long-term idea that an economic decision is pathfinding on a stratified manifold, as in the
programme's other domains. The owner chose to begin with sequential public data. Every other choice
below is Claude's and is open to the owner.

## 1. Why a new start, and what is not carried over

The tests archived on 2026-11-02 and reported in `../tcss-part2/manuscript/` were run on single choices
between two described lotteries over money. Such a choice has no path, no boundary to cross and one
attribute per outcome. A theory of paths on a stratified space predicts nothing there that a utility
function cannot also produce.

Nothing is carried over from Part I: not the nine coordinates, the fitted variances, the
cost-dependent temperature, or the expected-value-and-spread encoding.

## 2. The framework this stands on

This line adds no new formalism. It tests statements the programme already makes.

- **`geometric-methods`, Chapter 6.** Definition 6.1 gives the decision complex, a graph whose edge
  weight is a Mahalanobis term plus a sum of boundary penalties, one for each boundary the edge
  crosses. Definition 6.2 makes the decision the least-cost path to a goal set. Section 6.1.2 states
  that a path crossing a boundary incurs a cost no smooth distance predicts.
- **`geometric-ethics`, Chapter 8.** Definitions 8.1 to 8.3, stratification and the Whitney
  conditions.
- **`../../../stratification-thesis.md`.** The decision form of the thesis and Prediction W. Its
  warning applies here in full: any space can be cut into pieces after the fact, so a stratum counts
  only if it predicts held-out behaviour.
- **`moral-spectrum-analyzer/docs/DISCOVERY_ROADMAP.md`.** How a direction becomes a dimension:
  stability under resampling, replication in a second corpus, non-redundancy, and a single candidate
  designated before unblinding.
- **`../d4transition/`** (sealed 2026-09-14, no data). The identification result that a direction
  difference cancels the symmetric metric term and leaves the boundary penalties.

## 3. What the idea predicts that a static utility does not

A static utility assigns each option a value from its own description. Three consequences of
Chapter 6 fall outside that class.

- **P-edge. A boundary costs something in the present choice.** Among moves that a static evaluation
  rates as equal, those whose edge crosses a boundary are chosen at a different rate, by an amount
  that is a constant of the boundary and not of the position. This is Definition 6.1 read directly.
- **P-path. Whether history matters, given the state, is an open question inside the framework, and
  the first draft of this file had it wrong.** Corrected 2026-11-09. The first draft said that two
  people in the same state who arrived by different edges choose differently, "with the sign of the
  boundary penalties on those edges". Definition 6.2 does not say that. A least-cost path from the
  current state to the goal depends on the current state and the goal, and on nothing before. The
  strict reading therefore predicts **no** effect of history once the state is fixed. History can
  enter in two ways, and each is an addition to Chapter 6 that has to be stated. Either the goal or
  reference point moves with what has happened, as in Part I's public-goods encoding and in the
  reference-point account of Deal or No Deal. Or the search is bounded and the agent continues a
  plan made earlier (Section 6.5). The two differ in what they predict: a moving reference gives an
  effect that depends on how far the state was displaced and fades with time, and a reused plan gives
  an effect that depends on which continuation the earlier moves were preparing. A test of history
  with the state held fixed is therefore a diagnosis of which version holds, with no result that
  counts as a confirmation in advance.
- **P-jump. Behaviour is flat, then jumps.** Along a smooth change of the state, choice probability
  changes little, then changes abruptly where the least-cost path switches stratum. A smooth model
  with the same number of parameters fits the jump worse.
- **P-local. Dimension is local.** A metric fit within a stratum has lower rank than one fit across
  strata, and a piecewise metric predicts held-out choices better than one global metric of the same
  total number of parameters.

None of these is new as an observation. Path dependence in game-show choices, present bias at the
boundary of "now", and loss aversion at zero are published. The claim to test is narrower: that one
model, with discovered coordinates and boundary penalties as its only non-smooth part, predicts
held-out choices better than the best published account of each setting at equal capacity. A
prior-art check is running and its result is to be added as Section 9 before any claim of novelty.

**Checked in Lean, 2026-11-10** (`lean/`, nine theorems, no `sorry`, standard axioms only). Under
Definitions 6.1 and 6.2 two histories that end in the same state have the same best continuations
(`best_continuation_history_free`), a weight that reads the previous state breaks this
(`history_can_matter_if_weight_reads_the_past`), the two directions of a pair differ by boundary
penalties alone when the distance term is symmetric (`direction_difference`), and a boundary-crossing
move costs its penalty more than a move at equal distance that crosses none
(`boundary_edge_costs_its_penalty`). These are consequences of the definitions and say nothing about
behaviour. `lean/README.md` lists what was not formalised.

**The first quantity to carry across domains: the depth of memory.** Added 2026-11-10. The Lean
check was extended the same day. With a reference that moves with the past, history matters only
through the reference (`ranking_depends_on_state_and_reference`), and a reference that reads back m
steps cannot tell apart two histories that share their last m steps. The depth m is then one number
that each arena can measure in its own data, with the state held fixed:

| Arena | Two histories that share their last k steps | What is compared |
|---|---|---|
| Chess | the same position reached by move orders with the same last k half-moves | the next move |
| Deal or No Deal | the same remaining prizes and current offer, with the same last k earlier offers | deal or no deal |
| Poker | the same public state of the hand, with the same last k hands' results for the player | fold, call or raise |

Definition 6.2 as written says m = 0 everywhere. The claim to register, once chess has given a
value, is that m is the same small number in the other arenas. A different m in each arena, or no
finite m, is a failure of the common account and is reported as one. This is narrower than P-path
as first drafted and it can fail.

## 4. Rules for this line, each from a failure in the last one

1. **The strongest incumbent at equal capacity is in the comparison from the first fit.** Last time
   the linear scalar stood in for it and the tie with a squared distance was found afterward.
2. **One corpus is held back unseen for each sealed test,** named before development starts
   (Section 6). Development corpora are spent when touched.
3. **Coordinates are discovered.** A model reads a generic description of the state, not summaries
   chosen by the researcher. A discovered direction is named only after the roadmap's screens.
4. **A stratum must predict.** Strata are proposed from the structure of the task before choices are
   read, or found on development data and confirmed on held-out data.
5. **Flexible models are judged only on held-out data,** with a margin set by rehearsal on simulated
   choices from the incumbent, so that noise cannot pass.
6. **Seal before scoring,** public tag before the run, as for the October registrations.

## 5. Data found on 2026-11-09

Found by reading papers, archive pages, readme files and file listings. No data file was opened.
Every set has at least one published analysis, so none is unanalysed. None reports income.

### Sequential decisions

| Set | Decision | Size | Where | Not yet verified |
|---|---|---|---|---|
| **DOND-AU.** de Roos and Sarafidis 2010, J. Appl. Econometrics 25(6):987–1027 | Each round, take the bank's offer or open more cases. Remaining prizes known | 399 contestants, one row per round, 2004–2005, prizes to A$2,000,000 on special shows | JAE Data Archive `deal-data.zip`. Columns include the contestant's own guess of the offer and an audience poll | licence (a mirror is reported CC BY 4.0) |
| **DOND-NL/DE/US.** Post, van den Assem, Baltussen and Thaler 2008, AER 98(1):38–71 | same | 151 contestants | DataverseNL doi:10.34894/TXJK6K (CC BY 4.0), openICPSR 113232 | covariates, top prize |
| **DOND-LAB.** Baltussen, van den Assem and van Dolder 2016, REStat 98(2):318–332 | The same game played by experimental participants at limited stakes | not read | Harvard Dataverse doi:10.7910/DVN/27523 | everything beyond existence |
| **WHEEL.** Klein Teeselink, van Dolder, van den Assem and Dana 2024, Games Econ. Behav. | The Price Is Right wheel: stop or spin again, earlier scores known | 10,071 showdowns, 1979–2021 | Mendeley Data doi:10.17632/xw45438phj.1 (CC BY 4.0) | file contents. Source is a fan-edited site |
| **WWTBAM.** Hartley, Lanot and Walker 2014, J. Appl. Econometrics 29(6):861–879 | Answer or walk away, with the amount at risk known | 515 contestants | JAE Data Archive `wwtbam-data.zip` | columns. The chance of knowing the answer is unobserved |
| Psych-101 sequential tasks (Columbia Card Task and others) | to be listed | to be listed | copy on Atlas | the list. A folder-name listing was started 2026-11-09 |

### Choices whose outcomes pay the decider and another person

| Set | Decision | Size | Where |
|---|---|---|---|
| **FOF.** Kalist 2004, J. Statistics Education 12(3), Friend or Foe | Each of two partners secretly splits or takes a jointly earned pot | 227 games, 454 contestants, $200 to $16,400 | JSE data page, also R `Ecdat::FriendFoe` |
| **DIVIDED.** van Dolder, van den Assem, Camerer and Thaler 2015, AER P&P 105(5):402–407 | Three strangers must agree who takes which unequal share | not read | UK Data Service doi:10.5255/UKDA-SN-852884 (CC BY 4.0) |

Golden Balls (van den Assem, van Dolder and Thaler 2012) has no public deposit. It would have to be
requested from the authors.

### Choices with two attributes per option

| Set | Decision | Size | Where | Not yet verified |
|---|---|---|---|---|
| **ITC.** Pongratz and Schoemann 2026, Scientific Data 13:323 | Smaller sooner against larger later, amounts and delays stated | 1,172,644 trials, 11,852 people, 100 studies | OSF `mxucn` | licence (two statements disagree), whether delayed sooner options occur |

**Spent and not to be used:** CPC15, CPC18, choices13k, Wulff et al. 2018, Ruggeri et al., Plonsky
2018, the five strata corpora, Molter 2022, Gluth 2018, Scruples.

## 6. First study: Deal or No Deal

**Why this one.** The decision is literally a path. The state is the set of prizes still in play, and
each opened case removes one, so the distribution over remaining prizes moves to a face of the
simplex it lived on. The stratification is given by the game and not chosen by the researcher. Three
independent data sets of the same game exist, which gives a development set and held-out sets without
splitting one sample.

**Assignment, fixed now.**

- **Development: DOND-NL/DE/US** (151 contestants). It is the most analysed, so the least is lost by
  spending it.
- **Held out for the sealed test: DOND-AU** (399 contestants). Its parser writes states and choices
  to separate files, and no choice is read until the seal. The rehearsal uses the states only.
- **Held out for a second sealed test of transfer across stakes: DOND-LAB.** Same rule.

**The state, described generically.** The sorted vector of remaining prizes, each divided by the
largest prize on the board at the start, the current offer in the same unit, the previous offers, and
the round. No expected value, spread or other summary is computed by hand. A model is free to learn
them.

**Models, all fit on the development set.**

- **PT-path.** The path-dependent prospect theory of Post et al. 2008, with its reference point
  adjusting slowly to earlier offers, as specified in that paper. This is the incumbent.
- **Static.** Expected utility and prospect theory over the remaining prizes with no history.
- **Flexible.** A regularised model of the generic state with the same number of free parameters as
  the geometric model, so that a win cannot be a win of capacity.
- **Geo-global.** One learned metric on the generic state, cost of "deal" against cost of "no deal".
- **Geo-strata.** The same with a boundary penalty on each edge that crosses a boundary named below,
  and a metric allowed to differ by stratum.

**Boundaries proposed before any choice is read,** from the rules of the game alone.

- The largest remaining prize is eliminated.
- The offer falls below the previous offer.
- The offer falls below the best offer so far.
- The last prize above a round number of the contestant's currency is eliminated (to be fixed per
  edition from the prize board, before choices are read).

Development may drop boundaries. It may not add one after choices on the held-out sets are read.

**Predictions to be registered, in outline.** On DOND-AU, with everything frozen:

- H1 (P-path). Geo-strata beats Static.
- H2. Geo-strata beats PT-path. This is the comparison that matters.
- H3 (P-jump). Geo-strata beats Geo-global and beats Flexible.
- H4 (P-path, model-free). Among pairs of contestant-rounds matched on the generic state, the one whose
  last edge crossed a named boundary takes the offer at a different rate, with the sign fixed on the
  development set.
- H5 (transfer, second seal). The model frozen on television data predicts DOND-LAB after one scale
  is refit.

Bars, margins and the matching rule come from the rehearsal.

**What is already known and limits the test.** Post et al. report that contestants take more risk
after both unlucky and lucky eliminations. H1 is therefore expected and is not evidence for the
geometric form. H2 and H3 carry the weight.

**The main risk is size.** 399 contestants give perhaps two to three thousand round decisions, most
of them early rounds where almost nobody deals. The rehearsal must report power for H2 and H3 under
PT-path as the truth and under Geo-strata as the truth. **Rule written now:** if power for H2 is below
0.8 at the effect found on the development set, the study is not sealed as a confirmatory test of H2,
and DOND becomes a development setting for the next study.

## 7. Second study, if the first is worth sealing or not: intertemporal choice

The ITC database has a hundred studies and over a million trials, so power is not the constraint, and
each option has two attributes. It has no paths. It tests P-jump and P-local.

- Boundary proposed from the task: the sooner option is paid now. Quasi-hyperbolic discounting is this
  boundary with a fixed form, so it is the incumbent to beat, with hyperbolic discounting and the
  attribute-comparison models (ITCH, the tradeoff model, DRIFT).
- Held out by study: the studies are assigned to development or held-out by a hash of the study
  identifier, before any file is opened.
- Whether the database's authors already compared these models on the pooled data is part of the
  prior-art check.

## 7b. Third arena, proposed by the owner on 2026-11-09: chess

**Why it fits.** A chess game is a path on a graph in the literal sense of Definition 6.1. The space
is stratified by its own rules: a capture or a pawn move cannot be undone, and each capture moves the
game to a position with fewer pieces. Material has a conventional price (pawn 1, knight and bishop 3,
rook 5, queen 9), so it plays the part money plays elsewhere, and every sacrifice is a trade of that
coordinate against others. An engine gives each position a value that does not depend on how it was
reached, which is the static benchmark the other arenas lack. Time controls from one minute to thirty
vary how much a player can compute while the rules stay fixed.

**Why it is not a substitute for the economic studies.** The stake is a game result and rating
points, not money, and the player faces an opponent. A result here bears on the general thesis that
decisions are paths on a stratified space. It says nothing by itself about economic choice.

**Data.** The Lichess open database of rated games, with ratings, time control and per-move clocks.
Three months are already on Atlas at `/archive/ahb-sjsu/lichess` (June, July and August 2026, 28 to
30 GB each), fetched on 2026-09-20 for gate G7a of `geometric-evaluation-theory`. That gate used June
as its shakedown month and July and August as evaluation months, for a different quantity (the
smallest evaluation difference a player resolves, by time control). For this line all three count
as development months. **A later month is the held-out month, to be downloaded and not opened.**
The licence and the share of games carrying engine evaluations are in the prior-art check.

**The test that needs no model: transpositions.** The same position is often reached by different
move orders. The strict reading of Definition 6.2 predicts the same distribution of next moves
whatever the order (Section 3, P-path as corrected). With tens of millions of games a month the
matching can be exact on position, side to move, rating band, time control and clock remaining.

- **What is already known.** Models that predict human moves do better when given the preceding
  moves: Maia takes the last twelve half-moves and gains about three points of accuracy, and a 2026
  preprint reports five from twenty moves of history (Section 9). Those figures pool all positions and
  all reasons. The prior-art check found no published test with the position held fixed.
- **Three comparisons, in order of how much they exclude.**
  1. Same position, the mover's own moves in a different order. An effect here can be repertoire.
  2. Same position, the mover's own moves in the same order, the opponent's moves in a different
     order. The mover did not choose the difference. An effect can still be attention to the
     opponent's last move.
  3. As 2, with the opponent's last move also the same, so that only the order of the opponent's
     earlier moves differs. An effect here is history with the position, the mover's own play and
     the last move all fixed.
- **Statistic.** For each position and pair of path classes, the distance between the two
  distributions of next moves, against the same distance between random halves of one path class.
  Within rating band and time control. Bars and margin come from development months.
- **Reading, written before any row is analysed.** No effect in comparison 3 at the registered margin
  supports the strict reading, and the models of Sections 6 and 7 then need no history beyond the
  state. An effect in 3 means the framework needs a moving reference or a reused plan, and the two are
  told apart by whether the effect grows with the clock time since the differing moves (reference
  fading) or with whether the earlier order prepared the chosen continuation (plan).

**Status 2026-11-10.** `chess/mine_paths.py` writes one row per decision after 6 to 16 half-moves for
a 4% hash sample of games: position key, the moves so far in order, the move chosen, keyed digests of
game and player, ratings, time control and clock. A test on the first 60,000 games of July 2026 gave
25,797 rows in 3.5 seconds. The full July pass was started on Atlas on 2026-11-10 03:57 UTC, screen
session `paths-chess-07`, one core at lowest priority, output
`/archive/experiments/paths/chess/rows/paths_2026-07.tsv.gz`. The June file on Atlas is an incomplete
download and cannot be read. July and August are the development months.

**The test of P-edge and of discovered coordinates.** For positions where the engine rates two moves as equal within
a margin, which one do people play? The engine difference is zero by construction, so what remains is
what people price and the engine does not. Candidate directions come from a generic description of the
move (squares, piece, material change, a learned position embedding), screened as in the roadmap. Two
hypotheses to check against prior art before they are claimed: moves that give up material are
under-played against engine-equal moves that keep it, and so are moves that retreat.

**The test of local dimension.** Material configuration gives the strata. Fit the metric on those
discovered directions within a stratum and across strata, and compare held out, as in P-local.

**The incumbent here is a neural network.** Maia predicts human moves by rating band far better than
any small model will. The comparison is therefore not total accuracy. It is whether, with Maia's
prediction as the baseline, the edge class of the previous move and the boundary terms still add
held-out information, and with the registered sign.

**Compute.** Engine labelling goes to NRP, not Atlas (owner's rule of 2026-09-20), after the NRP
preflight checklist. Streaming passes over the source files run on Atlas at low priority.

**Claude's recommendation, not decided by the owner:** run the transposition test first of all three
arenas. It needs no model, the development data are already on Atlas, and its sample is large enough
that a null would be informative. Deal or No Deal remains the first economic study.

## 8. Order of work

1. Prior-art check (running). Add Section 9.
2. Finish the Psych-101 listing, by folder name only.
3. Read the Post et al. and de Roos and Sarafidis papers for the model specifications and the game
   rules of each edition. Papers only.
4. Write the parser for the development set, with choices and state in separate files, and the
   rehearsal on simulated choices from PT-path, Static and Geo-strata.
5. Develop on DOND-NL/DE/US. Record every model tried.
6. Rehearse on the AU stimuli with simulated choices. Apply the rule in Section 6.
7. Ask the owner for the seal.

## 9. Prior art, checked 2026-11-09

A web check of about sixty searches, reading abstracts and some full texts. Absence below means not
found in that check. It is not proof of absence. Entries marked (u) were seen only in a search
snippet or secondary source.

**What already exists, and must be credited.**

- **Ideal points and learned metrics.** Probabilistic unfolding places people and options in a latent
  space and lets distance drive choice (Coombs; Kamakura and Srivastava 1986, Marketing Science
  5:199–218; DeSarbo, De Soete and Jedidi 1989). Xu and Davenport (NeurIPS 2020) learn an ideal point
  and a Mahalanobis metric jointly from paired comparisons. Shubatt and Yang (arXiv:2401.17578) make
  choice probability depend on a value difference divided by a distance between options, across
  multiattribute, risky and intertemporal choice, with the distance specified and not learned.
  Distance from a learned ideal point is therefore not new as a form.
- **Deal or No Deal.** Expected utility, rank-dependent utility and prospect theory have all been
  fitted. Post et al. 2008 give the main account of path dependence, a reference point that lags the
  offers. Andersen et al. 2008 report probability weighting without loss aversion, and de Roos and
  Sarafidis 2010 do not confirm an endowment effect.
- **Discontinuities joined across domains.** Andreoni and Sprenger (2010 working paper) model a
  discontinuity at certainty by analogy with the one at the present. Halevy 2008 and Chakraborty,
  Halevy and Saito 2020 link the certainty effect and diminishing impatience formally.
  Cerreia-Vioglio, Dillenberger and Ortoleva join the endowment effect, loss aversion and the
  certainty effect under cautious utility.
- **Decisions as planning.** Tree search with pruning (Huys et al. 2012) and resource-rational
  planning (Callaway et al. 2022), on laboratory planning tasks. Karlström and Persson
  (arXiv:2603.01785) pose a least-action account on Fisher–Rao geometry with a term for path
  dependence.
- **Direction asymmetry as a measured quantity.** The gap between willingness to accept and to pay
  (Knetsch 1989; Kahneman, Knetsch and Thaler 1990), contested by Plott and Zeiler 2005 and 2007.
- **Chess.** Maia (McIlroy-Young et al., KDD 2020) matches 46 to 53% of human moves by rating band,
  with the last twelve half-moves as input and no clock. Later models reach about 55% (u for venue).
  Anderson, Kleinberg and Mullainathan 2016 on error against an engine benchmark, Russek et al. 2025
  on thinking time, Anderson and Green 2018 on personal-best ratings as reference points (u).
- **The Lichess database** is CC0, carries per-move clocks since April 2017, and about 6% of games
  carry engine evaluations (from the site).

**Not found.**

1. A latent space learned from risky or intertemporal choices, with distance to an ideal point.
2. Any held-out comparison of models on Deal or No Deal data.
3. One formalism treating present bias, certainty, zero price, the loss kink and sacred values as
   boundary crossings. The first two are already joined.
4. A stratified-space model of individual choice. Stratified sets appear in general-equilibrium
   theory only.
5. The direction difference used to cancel a symmetric distance and isolate a boundary cost.
6. Any comparison of discounting models on the pooled intertemporal choice database. Its authors fit
   none.
7. A test of history in human chess with the position held fixed, or an engine-matched study showing
   that people under-play sacrifices, retreats or irreversible moves.

**What this changes.** Item 2 makes the Deal or No Deal study useful even if the geometric model
loses, since no one has scored the published models out of sample. Item 6 does the same for the
intertemporal database. Items 1 and 3 narrow what may be called new: the form is known, and the claim
is the discovery of the space from choices and the single treatment of boundaries.

## 12. Data better suited to the economic question, searched 2026-11-10

The owner asked for a search for data that fit the economics work better than chess (no money) and
poker (money, but the stack is part of the state and is made by the player's own play). The brief
put one property above the rest: a history containing shocks the person did not cause, so that the
same state is reached by different luck. Found from landing pages, dataset cards and file listings.
No data file was opened. Items marked (u) were not confirmed on a primary page.

**Shortlist.**

| Rank | Source | Why it fits | Main weakness |
|---|---|---|---|
| 1 | **Basel-Berlin Risk Study** (Frey et al. 2017, Science Advances). OSF `rce7g`, CC BY 4.0. 1,507 people, 109 retested after six months. Trial-level balloon task (about 1.69 million choices) and Columbia Card Task (about 676,000), also in Psych-101 | The state is exact. Balloon bursts and card draws are random draws. Basel against Berlin, or the retest wave, gives a held-out set | One task drawn at random is paid, from a small bonus. The authors ask to be contacted before new projects. Whether card-task feedback was random or scripted is (u) |
| 2 | **Pooled indefinitely repeated prisoner's dilemma.** Fudenberg and Karreskog Rehbinder 2024, AEJ Micro, replication package doi:10.3886/E182668V1, 161 sessions. Dal Bó and Fréchette 2011 single study on openICPSR 112401 | The state is exact: the payoff matrix and continuation probability are fixed per session. Match length and rematching are random, and a new partner's first move is not the chooser's doing. Incentivised | Access, licence and file list (u), the archive page blocked the fetch |
| 3 | **Polymarket on-chain fills.** Hugging Face `moose-code/polymarket-onchain-v1`, CC BY 4.0, 1.17 billion fills, 2.6 million wallets, 2020 to 2026, 127 GB | The only large real-money field source that is openly downloadable. Resolutions are not a small trader's doing | A wallet is not a person. A wallet's position and balance are its own doing, which is the poker problem again. No order book |
| 4 | **Decisions from experience** (Wulff et al. 2018). Zenodo 1491449, CC BY-SA 4.0, 28 publications, about 1.12 million sampling choices | Samples are random draws | Few final choices per person. Incentives vary by study (u) |

**Already touched in this programme.** CPC18 was on the search's list. Its first-trial choices were
used in Part II. Its later trials, where a person meets the same gamble repeatedly with feedback
from random draws, were not used, but the corpus is not untouched. The description part of the Wulff
collection was a test corpus of `prereg-psych101-v1`. Its sampling part was set aside there and not
analysed.

**Checked and set aside.** The bwin and Transparency Project gambling sets hold per-person totals or
daily aggregates with no bet-level options or odds, and need a terms-of-use form naming an ethics
board. Betfair historical data shows no bettor identifier. Prosper's bid data was withdrawn. Manifold
is play money. The Dal Bó and Fréchette 2018 meta-data has no public location that could be found.

**What each of the top two would test.** In the balloon task a burst is a random event. Among
occasions where a person attempted a given pump, whether the balloon burst at that pump was decided
by the draw and not by the person. The next balloon then starts from the same state, and the
question is whether the person pumps less after a burst one balloon back, two back, and so on. In
the repeated prisoner's dilemma each new match starts from the same state with a stranger, and the
question is whether the first move depends on what the previous stranger did, one match back, two
back, and so on. In both the event is not the chooser's doing, which is what the poker comparison
lacked.

## 11. Bridge, parked 2026-11-10

Proposed by the owner from a pasted list of sources. One item was checked and the rest are unverified.

- **Richard Pavlicek's database** is 10,485,760 random deals, each solved double-dummy by computer
  (`rpbridge.net/8j29.htm`). It holds no human bidding or play and cannot be used.
- **Complete Bridge Database** (Axinte, about 384,000 boards from championships since 1953, with
  bidding and play), **Bridgetoernooi** (over 200,000 deals on request) and the **`pbn-files`**
  repository are described as records of human play. Their licences, formats and contents are not
  checked.

**What bridge offers that the other arenas do not.** In duplicate play the same deal is bid and
played at many tables, so one state is decided by many players without any matching. All four hands
are on record, unlike poker. The bidding can only go up, and the scoring has known jumps at game and
slam.

**Why it waits.** Bids are signals under partnership agreements, so a bid is not one person's choice
among options in the sense the other arenas allow. The stake is ranking, not money. A double-dummy
solver sees all four hands, so it is not the benchmark for a player who sees two. And the usable
sources are small and of uncertain licence beside a chess month of ninety million games.

## 10. Poker, looked at 2026-11-09

The Kaggle set `hosseinah1/poker-game-dataset` holds two files, `poker-hand-training.csv` and
`poker-hand-testing.csv`. By its file names and one indirect description it is the hand-classification
set from the UCI repository: five cards and the name of the hand they make. It records no bets, no
money and no decisions, so it cannot be used here. The page itself could not be read.

A usable poker source turned up in the same search and is not yet examined: the PHH collection
(`uoftcprg/phh-dataset`, MIT licence, Zenodo doi:10.5281/zenodo.10796885), which includes 21.6 million
no-limit hold'em hands from six online sites in July 2009 at stakes from 25NL to 1000NL, and the
10,000 hands played by the Pluribus program against professionals. Whether opponents' cards are shown
only at showdown, and whether the stakes were real money, are not stated on its front page.

**Looked at again 2026-11-10, at the owner's request** (repository front page, the Zenodo record and
the paper's abstract page, no data file opened). The archive is one 20.3 GB zip under CC BY 4.0
(Zenodo v3, doi:10.5281/zenodo.17136841; Kim, "Recording and Describing Poker Hands", IEEE Conference
on Games 2024).

| Part | Size | Human decisions | Use here |
|---|---|---|---|
| HandHQ logs | 21,605,687 no-limit hold'em hands, 1 to 23 July 2009, six sites, 25NL to 1000NL | yes | the main candidate |
| Pluribus | 10,000 hands, the program against professionals | yes, few players | all cards may be on record, to verify |
| Computer Poker Competition 2009–2017 | about 620 million hands | no, programs only | none |
| 2023 WSOP final table | 83 hands | yes | too few |

**Why poker fits.** A hand is a path through four betting rounds that the rules separate, with
irreversible edges (a fold, an all-in), and the stake is money. Of the arenas here it is the only
one that is sequential, monetary and large at once.

**To verify from the documentation before any use, in this order.**

1. Whether HandHQ player identities are consistent across hands. The record calls the logs
   anonymised. If each hand has fresh labels, nothing within a player or across a session can be
   tested.
2. Whether a player's cards are recorded only when shown. If so, the state is known only for hands
   that reached showdown, which selects on the outcome of the very decisions under study. Tests would
   then have to condition on public information alone.
3. Whether the HandHQ tables were real-money tables. The stake labels suggest so. The record does not
   say it.
4. What is already published on these or similar logs, for instance on play after large wins and
   losses.

**Format read 2026-11-10** from the first four hands of one sample file in the repository
(`data/handhq/PS-…_25NLH_OBFU/0.25/`), for the schema only. The owner also sent Zenodo record
13997158, which is version 2 of the same collection: 1.9 GB, CC BY 4.0, the human-play parts without
the 620 million program hands that version 3 added. Version 2 is the one to download.

- Each hand records blinds, every player's starting stack, every action with its amount, the board
  cards, the site, the date, a hand number, a table label and one label per player.
- **Cards are hidden unless shown.** Every deal is written `????`. A hand appears only where a player
  showed it at showdown, and a player who mucked stays `????`. Question 2 is answered: the full
  state is known only for shown hands, so any test must condition on public information, or treat
  the showdown subset as selected.
- **Player and table labels are 22-character strings** of the kind a hash gives. Whether one player
  keeps one label across hands could not be told from four hands. Question 1 is still open, and it
  is checkable by counting repeated labels without reading any action.
- **Amounts are in dollars** (blinds $0.10 and $0.25 at the 25NL table). Real money is likely and is
  still not stated anywhere read.
- **Time of day is blank** (`00:00:00`). Order within a day would have to come from the hand number.

**Question 1 answered 2026-11-10: the player labels are stable.** `poker/count_labels.py` read the
`players`, `table`, `day` and `venue` lines of every HandHQ hand in the version 2 archive
(md5 `0918a30f…`, as the Zenodo record lists) and nothing else. Result in
`poker/results/labels.json`.

- 21,349,121 hands with all three header lines, in 27 site-and-stake folders. The record states
  21,605,687. The difference of about 1% is hands lacking one of the three lines and is not examined.
- 276,628 distinct labels. Hands per label: 7 at the 10th percentile, 60 at the median, 640 at the
  90th, 7,407 at the 99th. Only 4,891 labels appear in a single hand.
- 136,609 labels appear on two or more days and 9,628 on ten or more. 146,066 appear at two or more
  tables, and 56,635 in two or more site-and-stake folders.
- 95% of all seats played belong to labels with at least 100 hands.

A label is therefore a player followed across tables, days and stake levels. Comparisons within a
player, and of a player's play after earlier hands, are possible. Questions 2 to 4 stand as before:
cards are hidden unless shown, real money is likely and unstated, and prior work is unchecked.

**The IRC Poker Database, sent by the owner 2026-11-10** (`poker.cs.ualberta.ca/irc_poker_database.html`,
page read, archive not downloaded). More than 10 million hands logged by Michael Maurer's observer
program on IRC poker channels from 1995 to 2001, hosted by the University of Alberta's Computer Poker
Research Group as one archive, `IRCdata.tgz`. The page calls the games "free-money games" that
predate real-money sites, with higher channels that required a qualifying bankroll. The page does
not describe the file format, the variants and limits, how players are identified, whether cards
are shown only at showdown, or any licence beyond a copyright notice. All of those are to be read
from the archive's own documentation.

**How the two poker sources could fit together, if the checks pass.** IRC is play money over six
years. HandHQ is dollars over 23 days. Developing on the first and sealing a test on the second would
ask whether a model built where nothing was at stake predicts play for money, which is a harder and
more useful test than a split of one source. It depends on question 1 for both: without stable player
labels neither supports anything across hands.
