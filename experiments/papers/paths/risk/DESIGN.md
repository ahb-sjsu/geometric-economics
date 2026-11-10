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

Three things about the files decide what can be done, in this order. None is known yet.

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

## 4. Quantities, if the capacity is recorded

Within a participant, the number of pumps on balloon t as a function of the capacity of balloon
t − 1, of t − 2, and so on, each divided into low (below the participant's own median pump count,
so that a burst was likely) and high. The curve over lags is the analogue of the chess and poker
curves.

**What the earlier arenas predict here, written before any file is opened.**

1. A low capacity one balloon back lowers the pumps on the next balloon.
2. The effect one balloon back is larger than the effect two balloons back, over the same
   participants.
3. Whether anything is left three or four balloons back is open. Chess left a remainder and poker
   left none.

That people pump less after a burst is well known for this task. Point 1 would repeat it with a
cleaner comparison and is not claimed as new. Points 2 and 3 are the ones that carry the question.

## 5. Held-out set, to be fixed before any choice is read

Development on one site and the sealed test on the other. Which is which is decided by the first
character of the sha256 of the string `basel-berlin` (0 to 7: develop on Basel), computed and
recorded before download, so that the choice is not made after seeing sizes or quality. The retest
wave is a second held-out set for the same participants six months later.

## 6. The card task

Reported by the search as a second sequential task with random draws. Whether its feedback was
random or scripted is not confirmed, and many versions of that task fix the position of the loss
card. It is not designed here until the documentation has been read.

## 7. Order of work

1. The owner decides on the note to the authors.
2. Read the task documentation and the file dictionary. Answer the three questions of Section 3.
3. Fix the split by the rule of Section 5. Download.
4. Parser with states and outcomes in separate files. Development on one site.
5. Grader, draft registration, the owner's word, seal, the other site.
