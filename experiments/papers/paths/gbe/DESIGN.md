# The Great Brain Experiment: risky choices with the order assigned by chance

**Status: design, 2026-11-11. Nothing downloaded. The archive has not been opened.** Found during
the survey for a purpose-built game (`../game/SURVEY.md`). Drafted by Claude. Every choice below
is Claude's and open to the owner. Download and any seal need the owner's word.

## 1. What it is

Rutledge, "Risky decision and happiness task: The Great Brain Experiment smartphone app", Dryad,
doi 10.5061/dryad.prr4xgxkk, published 2021 and updated 2023. The Dryad page and the README
preview were read in the owner's browser on 2026-11-11. The page marks the data as public domain
(CC0).

- 47,067 adults, anonymous and unpaid, from March 2013 to October 2015.
- 91,058 completed plays, about 2.7 million choices and 1.1 million happiness ratings.
- A play is 30 trials. Each trial offers a safe amount against a gamble with two outcomes. 11
  trials have gains only, 11 losses only and 8 are mixed. The stakes are points.
- **For each play the trials were drawn at random from a fixed list and shown in a random
  order.** Versions 1 and 2 drew from 150 possible trials, versions 3 to 5 from 120.
- Dates are removed. Days are counted from a person's first play. Time of day is given.
- One archive of 87.52 MB holding Matlab structure arrays, a script that reproduces published
  results, and a PDF with tables of every field. Those tables have not been read, so the exact
  field names, and whether the gamble's outcome is stored for each trial, are not yet known.

## 2. Why it matters here

It is the first arena found in which the path was assigned by chance and not by the player.

- **The offer is independent of the past.** Trial order is random, so what a player is offered on
  trial t does not depend on what happened on trials before it.
- **The last outcome is a coin flip.** Given that a player took the gamble on trial t − 1, whether
  it paid was decided by the app. So among decisions that follow a taken gamble, those after a win
  and those after a loss differ only by chance.

A difference in the rate of gambling on trial t between those two groups, on the same offer, is
therefore caused by the last outcome. No matching on state is needed and no estimator that
selects on a pattern inside a finite sequence, which is what went wrong in Skat
(`../skat/DEVELOPMENT.md`) and may touch poker. The comparison conditions only on an earlier
choice and then uses a random event.

That the gamble's two outcomes were equally likely is from memory of the published papers and is
not stated in the README preview. It has to be confirmed from the field tables and from the data.

## 3. What it does not give

- **Points, not money.** The players were unpaid.
- **It is again the weak statement.** An effect of the last outcome on the next choice is
  predicted by a moving reference point as much as by a stratified space. What this arena adds is
  the cause, not the theory.
- **Total points so far differ.** A player who just won has more points than one who just lost.
  So the present state, if it includes the running total, is not the same in the two groups. Two
  ways to deal with it, both to be worked out in development: compare at lag two with the last
  outcome held fixed (won then lost against lost then won, which end at the same total when the
  amounts match), or use plays in which no running total was shown, if the field tables say such
  plays exist.
- **Prior work.** The group's own papers model happiness as a function of recent outcomes
  (Rutledge and others, PNAS 2014). One search found no paper on the effect of the last outcome on
  the next choice in these data. That search was shallow and the papers were not read, so no claim
  of being first can be made.

## 4. The split, fixed here before the archive is downloaded

A participant is development or held out by a rule that reads only the participant's identifier.

- Take the participant's identifier as the archive stores it, as text. If the archive has no
  identifier field, take the participant's position in the array, counted from 1, as text.
- Compute SHA-256 of the text `gbe-split-2026-11-11:` followed by that identifier.
- If the first hexadecimal character is 0 to 7 the participant is **development**. If it is 8 to
  f the participant is **held out**.
- All of a participant's plays go with the participant.
- The script that applies the rule reads the identifier field and no other, writes the two parts
  as separate files, and the held-out file is made unreadable at once.

About half of 47,067 people on each side. If the first pass shows the effect needs more
development data than that, the rule is not changed. The estimate is simply less precise.

## 5. Order of work, once the owner gives the word to download

1. Fetch the archive to Atlas, record its sha256, do not open it.
2. Read the PDF of field tables only.
3. Write and run the split script. Held-out part unreadable.
4. Development: confirm the random order and the coin flip from the data, then the first rate of
   gambling after a win against after a loss, by trial type.
5. A registration draft with bars from development, a rehearsal, and a seal on the owner's word.

## 6. What it would do for the game

It would give the size of the effect of the last outcome in a risk task played on a phone by
volunteers. That is the number the game's pilot was meant to measure, and it sets how many
players the game would need.
