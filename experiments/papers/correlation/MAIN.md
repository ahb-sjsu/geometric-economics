# The main study: who counts, the fits and the tests

**Status: written 2026-11-07, not sealed.** The owner asked for it on 2026-11-07 ("write the main study runner and seal
it with step 10"). It is sealed at sequence step 10 (PILOT.md), under the signed tag `prereg-correlation-v1-main`, with
the n the pilot chooses, before anyone is recruited to the main study. It has read no data: neither the pilot nor the
main study has run.

## What it is for

DESIGN.md ("Analysis") registers the tests, and `rehearsal.py` computes them on simulated people. Until now nothing read
the main study's saved files into them. `main_analysis.py` does, and changes none of them.
- **`export`** turns the files the instrument saved in the main study's mode into one record per participant.
- **`grade`** decides who counts, fits the models as the rehearsal did, and runs `rehearsal.evaluate` and
  `rehearsal.tests` themselves.

`seal_main.py` writes and checks the seal of step 10. Neither file changes anything sealed on 2026-11-07, so the
design's seal stays intact (`python seal_correlation.py`).

## Running it

**Step 10, after the pilot is split and analysed (step 9), with the owner's OK.**
1. Change this file's status line to say it is sealed.
2. `python seal_main.py --write --estimates EST`, where `EST` holds the pilot's `pilot_estimates.json`. With the owner's
   OK to publish the estimates (PILOT.md, "Data and provenance"), add `--publish-estimates`.
3. `python seal_main.py` must print `SEAL INTACT`.
4. Commit `prereg-correlation-v1-main.sha256`, `results/sample_size.json` (and `results/pilot_estimates.json` if
   published) and this file. Tag the commit `prereg-correlation-v1-main` with a signed annotated tag, and push both.

**The main study.**
1. Set `mode: "main"` in `instrument/config.js`, make a new DataPipe experiment for it, and exclude the pilot's
   participants on Prolific (`instrument/README.md`).
2. While recruiting, download the files and run
   `python main_analysis.py export RAW --prolific IDS.txt --pilot-ids PILOT_SPLIT/id_map.json --out MAIN --source human`.
   `MAIN/export_record.json` gives `qualify`, the number who meet the inclusion rule so far. Recruitment stops when it
   reaches n.
3. Approve, pay and donate as after the pilot, with `export_pilot.py review RAW --prolific IDS.txt --out REVIEW --mode
   main` (`instrument/README.md`, "After the study").
4. Export once more, then run `python main_analysis.py grade MAIN/main_data.json --out RESULTS`, in an environment
   with jax and NumPyro for `hier.py`. It writes `RESULTS/main_results.json`.

Only `export_record.json` and `main_results.json` may enter the public repository. `main_data.json`, `main_people.json`,
`main_problems.json` and `main_id_map.json` hold per-person rows, and `main_id_map.json` holds Prolific IDs.

## Who counts

DESIGN.md's inclusion rule, applied through the sealed code's own functions:
- **The first session counts.** A participant's first session counts, whatever its status, as `export_pilot.py`
  counts it. Files from anyone not on Prolific's list of the study's participants are left out.
- **The inclusion rule** (DESIGN.md, Inclusion):
  - finished the session;
  - passed the quiz within two tries;
  - chose the dominated option in at most 2 of the 8 attention checks (`pilot_analysis.person`);
  - is not flagged as self only (`rehearsal.flagged`: the self-favouring option in at least 15 of block R's 20 pairs
    at ratios 2 and 3).
- **The tests count the first n who meet it, in order of start time.** Start time is `t_start`, the moment of consent.
  This is the order the rehearsal counted in: it recruited until there were n unflagged people and tested the first n.
- **Pilot participants are left out,** whoever they are, since the pilot bars them (PILOT.md). The pilot's private
  `id_map.json` names them, and a human export without it is refused.
- **Reported apart.** Flagged people, and anyone who qualifies after the first n, enter no registered test. Flagged
  people are paid, and their MF1 and MF2 statistics are reported with an interval. Later qualifiers are counted.

## The fits

They are `rehearsal.main`'s, unchanged.
1. Every model (GEO, EARLY, RDU, CAG, IA) is fitted to each person's calibration trials with fixed weak priors.
2. An empirical-Bayes prior is taken from the first fits of the first 60 people included (choice 1, below). It is
   each parameter's median, with a spread of 1.4826 times its MAD, at least 0.25 (`models.eb_prior`).
3. Every model is fitted again for each person counted, from their first fit, under that prior.
4. The second fits predict the test trials and the crossing set, with no refit.

The population `κ` is `hier.py`'s.

## What it reports

`main_results.json`, in the order DESIGN.md gives:
- **The model-free checks first.** MF1 (block X's rate of the correlated option against even odds) and MF2 (risk
  attitude over one attribute as the other leaves its ideal, the matched lotteries only).
- **The claim.** H1, H2 and H3 are GEO's held-out log-loss against EARLY, RDU and CAG. Each passes when the upper end of
  its 95% interval over people lies below −0.005. The claim is their conjunction. Each H is reported on its own, with
  its pass at every margin the rehearsal recorded.
- **H4,** the comparative test across people.
- **The population `κ`:** the posterior median and 95% interval, and whether the interval excludes 1 and 2.
- **The secondary claim,** SH1 and SH2 together, with SH1r and both forms of SH3 reported only.
- **DESIGN.md's readings,** quoted where their condition holds. One is that both model-free checks are null. The other
  two are a null on the claim with `κ`'s interval excluding 1, or excluding 2.
- The counts at each step of the inclusion rule, the prior's people, the mean log-loss of every model after each pass,
  the median session length, the share of choices faster than a second, the rate of left choices and the charities
  chosen.

## Choices made in writing it (Claude's, 2026-11-07)

The sealed documents leave six things open. Claude chose each before any data, as follows. The owner may change any of
them before step 10, and step 10 seals them.
1. **The empirical-Bayes prior comes from the first 60 people included, flagged or not.** `rehearsal.main` took it
   from the first 60 people it recruited, whoever the flag later caught. The table's power over unflagged people and its
   false-positive rates were computed that way. A prior from unflagged people only was never rehearsed.
2. **The first n who qualify count, in order of start time.** Anyone who qualifies later is paid and counted, and
   enters no test. Any order that the choices cannot affect would be as fair; this one is the rehearsal's.
3. **The population `κ` is fitted to the n people counted.** `rehearsal.main` fitted it to the first 120 recruited,
   flagged or not. DESIGN.md says flagged people enter no registered test, and `pilot_analysis.py` fits it to the
   people its own flag does not catch. Rehearsal version 3's coverage figures came from cells with nobody of rank one. There the flag catches
   only a few people, and the two groups nearly coincide.
4. **The random streams are fixed.**
   - Each person's fits take their random second start from their own stream: `[20261102, 20, k]` for the k-th person
     in the export.
   - `hier.py` runs with seed 0.
   - H4's bootstrap is `rehearsal.tests`'s own, seeded by n.
5. **Human data are graded only under the seal of step 10.**
   - n comes from that seal, never from the command line.
   - The seal must name this `main_analysis.py`.
   - The seal and the design's seal must be intact.
   - The export must have left the pilot's participants out.
   - `hier.py` must run.
6. **Reported apart means** the flagged people's model-free statistics and the number who qualified after the first n.
   Per-person rows go to a private file.

## The guards

`grade` refuses, exit 2, naming its reason:
- human data without the seal of step 10 (`missing`);
- human data at an n given by hand (`n`), or a seal recording an n outside 120 to 240;
- a seal that names another `main_analysis.py` (`runner`);
- a broken seal of step 10 or of the design, or one that names another design seal (`seal`);
- human data exported without the pilot's id map (`pilot`);
- another stimulus hash (`hash`);
- an undeclared source (`provenance`);
- a field the export does not write (`field`);
- a pilot-only trial, or a finished session without all 140 trials (`format`);
- fewer people qualifying than n (`short`).

`export` refuses a human export without the pilot's id map (`pilot`). It also refuses any session that fails one of
`export_pilot.py`'s checks: hashes, order, quiz, payment, mode (`problems`). With `--exclude-problems` it leaves those
sessions out and counts them.

## The self-test

`python main_analysis.py self-test DIR [--hier]` simulates a main study at n = 120 under `κ = 1`, noise target 1.5 and
a rank-one share of 0.3 (cell `G100T15S30`). Each person goes through saved session files in the page's format, written
from the fields of the round trip's main-mode records. Planted among the first 60:
- a quiz failed twice;
- a quiz passed at the second try;
- a session stopped after 70 choices;
- three attention checks failed;
- a first session stopped and a second one finished;
- a pilot participant;
- someone not on Prolific's list;
- a stray file;
- an earlier checkpoint of a session that later finished.

It checks the following, and writes `main_selftest.json` with the hashes of the code it ran:
- every exported choice is the simulated one;
- the planted cases are left out as planted;
- no Prolific ID is outside the id map;
- the people counted and the prior's people are those the simulation itself says, and every registered number equals
  `rehearsal.tests` computed again from the simulated choices;
- two controls make a check fail: choices read the other way round, and the flag ignored;
- every guard above refuses for its own reason;
- human data under an intact seal of step 10 are graded at its n.

*Result, 2026-11-07 (Atlas, with `hier.py`; `results/main_selftest.json`): 26 of 26 checks pass, in 517 seconds.*
- **Counts.** 184 people were exported, each choice the simulated one. 179 were included and 56 flagged. 120 were
  counted, and 16 of the prior's 60 were flagged.
- **The numbers.** Every registered number equals `rehearsal.tests` computed again from the simulated choices, exactly.
- **The simulated study's verdict.** It passes the claim: the upper ends of H1, H2 and H3 are −0.035, −0.026 and
  −0.039. `hier.py` puts the population `κ` at 0.95, with a 95% interval of 0.85 to 1.05, for a true `κ` of 1, with no
  divergence.
- **The controls each make their check fail.**
  - Choices read the other way round change every registered number. That runner could count only 93 people, so it
    was compared at 93.
  - With the flag ignored, 40 of the 120 counted are flagged people.
- **The guards.** Each refuses for its own reason.

**On the page's own files.** The instrument's round trip (2026-11-06) clicked two main-mode sessions through the real
page in a headless browser. `export` takes both, with all 140 trials each exactly as saved, finished and included.

## The rehearsal

`python main_analysis.py rehearse TRUTH 10 OUT.json --seed K` runs simulated main studies of n = 120 through the saved
files, `export` and `grade`, without `hier.py`. `summarise` scores the runs against the bars below. There are 20 studies
per truth, two runs of 10 with seeds 0 and 1. It shows that the runner, end to end, passes the claim as often as the
rehearsal says it should. It is not a power estimate: the sealed table is.

**Expected, written 2026-11-07 before any run.**
- **`G100T15S30`.** The sealed table's power over unflagged people at n = 120 is 0.96, 1.00 and 0.90 at rank-one
  shares of 0, 0.2 and 0.4 (`results/power_table_v6b.json`). So the claim should pass in about 95% of studies, and the
  secondary claim in none.
- **EARLY, RDU, CAG and ADD.** In rehearsal version 4, at n = 120 and margin 0.005, the claim passed in 0 of 50 studies
  under each, and the secondary claim in none.
- **IA.** The claim passed in none, and the secondary claim in all 50.

**The bars, set before the runs** (`main_analysis.py`, `summarise`):
- the claim passes in at least 16 of 20 under `G100T15S30`, and in at most 1 of 20 under each of the five truths
  without the metric;
- the secondary claim passes in at least 18 of 20 under IA, and in at most 1 of 20 under every other truth;
- every run used the same code.

*Result, 2026-11-07 (Atlas, 120 simulated studies in 488 seconds; `results/main_rehearsal.json`): every bar passes.*
Passes in 20 studies of each truth:

| Truth | Claim | H1 | H2 | H3 | Secondary claim |
|---|---|---|---|---|---|
| `G100T15S30` | 19 | 19 | 20 | 19 | 0 |
| EARLY | 0 | 0 | 5 | 0 | 0 |
| RDU | 0 | 20 | 0 | 1 | 0 |
| CAG | 0 | 20 | 20 | 0 | 0 |
| ADD | 0 | 0 | 7 | 0 | 0 |
| IA | 0 | 0 | 16 | 0 | 20 |

- **The pattern is DESIGN.md's account of why the claim needs all three.**
  - Under CAG, H1 and H2 passed in every study and H3 in none.
  - Under RDU, H1 passed in every study and H2 in none.
  - Under EARLY, ADD and IA, H2 alone passed in some.
- **The flag.** Under `G100T15S30` it caught 28% of the people included.
- **The records.** Each run's record is in `results/main_rehearsal_runs/`.

## The seal of step 10

PILOT.md's step 10 records the row and n by the sealed rule under a signed tag, with the hash of
`pilot_estimates.json`. `seal_main.py` writes that record, `prereg-correlation-v1-main.sha256`. Its format is the
design seal's, and it seals this analysis with the n:
- this file, `main_analysis.py`, `results/main_selftest.json`, `results/main_rehearsal.json` and
  `results/sample_size.json`, with `results/pilot_estimates.json` if the owner publishes it;
- n, the rule's decision, or the owner's when the rule chooses none, and the hash of `pilot_estimates.json`;
- the design seal's combined hash.

It writes nothing unless:
- the design's seal is intact;
- `pilot_analysis.size` accepts the estimates against the sealed table;
- the self-test passed on the code as it is;
- the rehearsal passed its bars on the same analysis code.

`main_analysis.py grade` reads the record before it grades human data.

*Dry run, 2026-11-07 (Atlas, in a throwaway copy of this folder, nothing in the repository).* A simulated pilot stood
in for the real one. It was analysed against the sealed reference and table, then relabelled as human.
- **Before the relabelling.** `--write` refused while the estimates were missing, and refused them while they were
  marked simulated. Both refusals came from `pilot_analysis.size`'s own guards.
- **The owner's branch.** Relabelled as human, the estimates led the rule to choose no n. The rule stops for some pilots
  even at `κ = 1`, as the pilot rehearsal showed (PILOT.md, sequence step 4). `--write` refused until it was given the
  owner's 240 and the owner's words. It then wrote the record, and the check read `SEAL INTACT`.
- **The rule's branch.** A second simulated pilot, for which the rule chose n = 160, was sealed at 160. `--owner-n` was
  then refused.
- **Grading.** A simulated main study of 336 people, relabelled as human, was graded through the command line at the
  record's n of 240, with `hier.py`, in 806 seconds.
- **The controls.**
  - One byte added to `main_analysis.py` broke the seal, and `grade` refused (`runner`).
  - One byte added to `MAIN.md` broke it too (`seal`).
  - One byte added to `DESIGN.md` broke the design's seal: `grade` refused (`seal`), and `--write` refused.
  - With the record removed, `grade` refused (`missing`).
  - Restored, both seals read intact.
