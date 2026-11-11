# Sequential risk tasks: does a random loss change the next decision from the same starting state?

**Status: DRAFT design, 2026-11-10. No data downloaded or opened. Nothing sealed.** Choices are
Claude's and open to the owner.

## 1. Why this arena

Chess fixed the state exactly and had no money. Poker had money, but the player's stack is part of
the state and is made by the player's own play, which biased every comparison against a baseline
(`../poker/DEVELOPMENT.md`). The property poker lacked is a history containing events the chooser
did not cause. A search on 2026-11-10 (`../DESIGN.md`, Section 12) found it in the Basel-Berlin Risk
Study.

## 2. Data

Frey, Pedroni, Mata, Rieskamp and Hertwig, "Risk preference shares the psychometric structure of
major psychological traits", Science Advances 3(10) e1701381, 2017. OSF project `rce7g`, CC BY 4.0.
1,507 participants in Basel and Berlin, 109 of them retested after six months. Trial-level files for
the Balloon Analogue Risk Task, the Columbia Card Task, decisions from experience and lotteries.
Counts from the Psych-101 index: about 1.69 million balloon-task choices and 676,000 card-task
choices. One task drawn at random was paid, from a bonus of 15 Swiss francs or 10 euros.

Everything in this paragraph is from the paper's public pages, the OSF description and file listing,
and the Psych-101 index, as reported by the search. No file was opened.

**The authors ask to be contacted before new projects, to avoid overlap.** The data are openly
licensed, so this is a courtesy and not a condition. A draft note for the owner to send is in
`NOTE-TO-AUTHORS-DRAFT.md`. Nothing is downloaded until the owner has decided whether to send it.

## 3. The comparison, and what must be checked first

In the balloon task a participant inflates a balloon pump by pump, earning with each pump, and may
stop and bank the amount. Each balloon has a capacity. A pump beyond it bursts the balloon and the
amount for that balloon is lost. Every balloon starts from the same state.

**The event that is not the chooser's doing is the capacity.** Whether a balloon bursts depends on
the capacity and on how far the participant pumped, so a burst is partly the participant's doing.
The capacity is not.

Three things about the files decide what can be done. Section 3a records what the published
supplement settles and what it leaves.

1. **Is the capacity of each balloon recorded, including for balloons that were banked?** If so, the
   clean comparison is available: the next balloon's pumps as a function of the previous balloon's
   capacity, which is as good as randomly assigned.
2. **Was the sequence of capacities drawn afresh for each participant, or fixed for all?** With one
   fixed sequence, the previous capacity is tied to the trial number and cannot be separated from
   it. With a few fixed sequences, the comparison is between sequences.
3. **Is each pump recorded, or only the total per balloon?** Only totals are needed for the
   comparison across balloons.

If the capacity is not recorded, what remains is the comparison of the balloon after a burst with
the balloon after a banked one, among balloons where the participant pumped at least as far. That
comparison conditions on the participant's own play and inherits a milder form of the poker
problem. It would be reported as such and not registered.

## 3a. What the published supplement says (read 2026-11-10, no data file opened)

Source: the paper's Supplementary Materials PDF (`1701381_SM.pdf`, from the Europe PMC file service
for PMC5627985), section "Methods and DVs of behavioral tasks".

- 30 balloons, 1 point per pump, a burst loses the points for that balloon.
- **The 30 capacities are one fixed set, "presented in randomized order"**: 1, 13, 18, 22, 28, 30,
  33, 37, 47, 49, 50, 55, 56, 58, 61, 67, 70, 72, 73, 78, 79, 81, 91, 95, 98, 100, 106, 110, 115, 128.
  Their mean is 64.03, which agrees with the supplement's "on average, balloons exploded after 64
  pumps".
- The supplement does not say whether the order was randomised separately for each participant.
  That is the natural reading, and it is my reading, not a stated fact.
- The card task has 84 rounds that differ in the number of loss cards, the gain and the loss, and a
  loss card ends the round. So its rounds do not start from one common state, and the supplement
  does not say how card positions were set. It stays undesigned.

**What this changes.**

1. **Question 2 is mostly answered, in the favourable direction.** A random order of a fixed set
   means the capacity of the previous balloon is assigned by the draw. Whether the order was drawn
   per participant is the one thing still to confirm, from the files or from the authors.
2. **Question 1 matters less than it did.** A burst reveals the capacity, since the balloon burst at
   that pump. The lowest capacities burst for nearly everyone. A participant who pumps at all bursts
   the capacity-1 balloon, and I expect few to stop before 13, though that is a guess until the
   files are read. So the position of the lowest-capacity balloons in each participant's sequence
   can be read from the pump counts even if no capacity is recorded. For banked balloons the
   capacity is one of the values not yet seen, and is not known singly.
3. **A new mechanical bias, and its remedy.** The order is a draw without replacement, so the
   capacity of balloon t is slightly negatively related to the capacity of balloon t − 1 (correlation
   −1/29). The observed pumps on balloon t are cut off by its own capacity. After a low-capacity
   balloon the next one is therefore slightly larger on average and cuts off slightly less, which
   would raise observed pumps with no change in the participant. The remedy is an outcome that the
   cut-off cannot move, namely whether the participant pumped at least m times, counted only on
   balloons that did not burst before m. A balloon that burst before m is dropped, and the dropping
   depends only on that balloon's own capacity. A permutation of each participant's order gives the
   reference distribution.
4. **A burst with nothing lost.** The capacity-1 balloon bursts at the first pump with at most one
   point at stake. Its position is random and its burst is no one's doing. Comparing the balloon
   after it with the balloon after the capacity-13 or capacity-18 balloon separates the event of a
   burst from the size of the loss. This was not in the design before the supplement was read.
5. **Question 3.** The Psych-101 index count of about 1.69 million balloon-task choices over
   1,507 participants and 109 retests is about 35 per balloon, which fits one record per pump. That
   is an inference from a count, not a reading of the files.

## 4. Quantities

Revised 2026-11-10 after the supplement was read and before any data file was opened. The first
draft split the previous capacity at the participant's own median pump count. With a fixed set of
capacities the split can be on the capacity itself, which does not depend on the participant's
play.

Within a participant, the outcome on balloon t (pumped at least m, for a small set of m fixed in
development) as a function of the capacity of balloon t − 1, of t − 2, and so on, with the
capacity classed as low (the six lowest, 1 to 30, where a burst is likely) or not. Where a banked
balloon's capacity is not recorded, low is read from a burst at 30 pumps or fewer, and the
comparison is restricted as Section 3 says. The curve over lags is the analogue of the chess and
poker curves.

**What the earlier arenas predict here, written before any file is opened.**

1. A low capacity one balloon back lowers the pumps on the next balloon.
2. The effect one balloon back is larger than the effect two balloons back, over the same
   participants.
3. Whether anything is left three or four balloons back is open. Chess left a remainder and poker
   left none.

That people pump less after a burst is well known for this task. Point 1 would repeat it with a
cleaner comparison and is not claimed as new. Points 2 and 3 are the ones that carry the question.
Whether the burst with nothing lost (Section 3a, point 4) moves the next balloon is a fourth
question with no prediction from the earlier arenas, and is reported as exploratory.

## 5. Held-out set, to be fixed before any choice is read

Development on one site and the sealed test on the other. Which is which is decided by the first
character of the sha256 of the string `basel-berlin` (0 to 7: develop on Basel), computed and
recorded before download, so that the choice is not made after seeing sizes or quality. The retest
wave is a second held-out set for the same participants six months later.

**Computed 2026-11-10, before any download.** The sha256 of `basel-berlin` (12 bytes, no newline) is
`b4ddc5038c200368e52797c926e4afa624a50abfbe742c0a3752d1dbe58dd2fd`. The first character is `b`,
which is outside 0 to 7. **Development is Berlin. Basel is held out.** The retest wave is held out
at both sites.

## 6. The card task

Reported by the search as a second sequential task with random draws. Whether its feedback was
random or scripted is not confirmed, and many versions of that task fix the position of the loss
card. It is not designed here until the documentation has been read.

## 7. Order of work

1. The owner decides on the note to the authors.
2. Read the file dictionary. Confirm that the order was randomised per participant and whether
   the capacity or the order is recorded (Section 3a). The task documentation has been read.
3. Fix the split by the rule of Section 5. Download.
4. Parser with states and outcomes in separate files. Development on one site.
5. Grader, draft registration, the owner's word, seal, the other site.
