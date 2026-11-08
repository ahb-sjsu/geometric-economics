# The instrument

The web page that runs one participant through the correlation-attitude study (`../DESIGN.md`, `../PILOT.md`). Built
2026-11-06. It is a static page with no server of its own: plain HTML, CSS and JavaScript, no libraries, nothing
loaded from elsewhere. It saves through DataPipe's API into storage the owner controls. Sealed on 2026-11-07 under
the signed tag `prereg-correlation-v1` (`../prereg-correlation-v1.sha256`), all but `config.js` and this README.

## Files

| File | What it is |
|---|---|
| `index.html`, `style.css` | the page and its look. Every bar spans 0 to 100 at the same width on every trial, so the top of each scale, the ideal, is the same on every screen |
| `stimuli.js` | written by `../build_instrument.py` from `stimuli.py`: each trial's id and its two options, the parts that `presentation(seed)` shuffles, and the stimulus hash. No roles, blocks or cells |
| `order.js` | a participant's order, exactly as `stimuli.presentation(seed)` gives it: numpy's SeedSequence, its PCG64 generator and `Generator.permutation`, written out |
| `text.js` | every word the participant reads, so the wording can change without touching the logic. The consent text is a draft for the ethics review |
| `task.js` | the session: consent, charity, rules, quiz, trials, debrief, the paid choice, saving, resuming |
| `config.js` | the deployment's settings: mode, DataPipe experiment, Prolific completion codes, receipts address, contacts. Not sealed. Until every field is filled the page records nothing and asks the participant to return the study |
| `MANIFEST.json` | written by `../build_instrument.py`: the sha256 of every file the browser loads except `config.js`, and a build hash over them, which every saved record carries |

The scripts beside the analysis code:

| Script | What it does |
|---|---|
| `../build_instrument.py` | writes `stimuli.js` and `MANIFEST.json`; `--check` fails if either is stale |
| `../export_pilot.py` | `review`: the saved files into a list for approving submissions, the bonus list for Prolific and the totals owed to each charity. `export`: the export that `split_pilot.py` reads |
| `../main_analysis.py` | the main study's export and its analysis (`../MAIN.md`) |
| `../instrument_roundtrip.py` | the round trip of PILOT.md, sequence step 3 (below) |
| `../instrument_screens.py` | a picture of every screen, for the ethics application |

The three scripts that run a browser need Playwright with Chromium, so they run on Atlas, not on the laptop.

## A session

1. A link without a Prolific ID, or a window under 1000 by 620 pixels, stops at a message. Nothing is recorded.
2. **Consent.** Declining ends the session and records nothing. Agreeing starts the record: a random order seed
   below 2³¹, the order it gives, and the start time.
3. **How it works, then the charity** (five, in alphabetical order, each with one line on what it does), **then the
   rules**, with one sure and one coin-flip example.
4. **The quiz:** four questions (`text.js`, `TEXT.quiz`). A wrong answer brings the rules again and a second try.
   Two wrong tries end the session with the base payment (completion code `quiz_failed`).
5. **The trials** in the participant's order: Option A on the left is option 0. Each option is a card with one
   outcome ("For sure") or two ("Coin flip": Heads and Tails, 1 in 2 each), each outcome a bar and a number for
   "You" and for the charity. The choose buttons come on two frames after the cards are drawn; the response time
   runs from then to the click. A 300 ms blank screen separates trials.
6. **The pilot's debrief:** belief that the donation will be made (1 to 5), which choices are paid, difficulty (1 to
   5), and how they chose (optional text). The main study has none.
7. **The paid choice:** one of the trials shown, drawn uniformly with the browser's cryptographic random numbers, and
   a fair coin if the option chosen in it is a coin flip. The draw is stored before it is shown, so a reload shows
   the same one. The bonus and the donation are 5 cents a point.
8. **The return to Prolific,** only after the last save has arrived. If it keeps failing the participant can try
   again, or finish anyway and write to the researcher.

Times: `t_start` at consent, `t_main_end` at the 140th choice, `t_end` when the paid choice is shown. The pilot's
gate on session length reads `t_main_end − t_start`, so it includes the rules and the quiz, as the rehearsal's
simulated export assumed (four minutes).

## What is saved, and how

The whole session record is saved at each checkpoint as a new file, `<Prolific ID>_<session>_<n>.json`: after
consent, after the charity, after each quiz try, every 20 trials and at the 140th, and at the end. A session that
stops early leaves its last checkpoint, which the pilot's gates need (who passed the quiz, who finished). The record
is also kept in the browser's storage, so a reload resumes the same session.

A record holds the Prolific ID, study and session parameters, the order seed and order, the charity, each quiz try's
answers, every trial's id, position, choice and response time, the debrief, the paid choice, the times, and the
number of reloads, of times the tab was hidden during the trials, and of saves that failed. `export_pilot.py`
keeps only what the export format asks for (`split_pilot.py`).

Saving uses DataPipe's API (`POST https://pipe.jspsych.org/api/data/` with `experimentID`, `filename` and `data`;
read 2026-11-06). DataPipe answers 201 when the file is stored and 202 when it has queued it to store later; both
count as saved. It answers 400 with `FILE_EXISTS` when a file of that name is already stored, which the page also
counts as saved, since only an earlier try of the same file can have that name. Network failures and 5xx answers are
tried again after 1, 2, 4, 8 and 16 seconds.

## Hosting: Claude's choice, 2026-11-06

On 2026-11-06 the owner asked for the instrument to be built without naming a host. This is Claude's choice, and the
owner may change it. The page itself does not depend on it: only `config.js` names the storage, and
any service that takes DataPipe's request would do.

- **The page: GitHub Pages, from a public repository that holds only this folder's files,** copied from the sealed
  tag. A page's code is visible to anyone who opens it, so nothing is lost by publishing it. A separate repository
  keeps a curious participant away from DESIGN.md and its hypotheses. The page asks search engines not to index it.
- **The data: DataPipe, into the owner's Google Drive.** DataPipe sends each file straight to storage the researcher
  controls, and its privacy page (read 2026-11-06, last updated 2026-09-16) says it keeps no copy in normal
  operation. It runs on Google Cloud in the United States and is operated by jsPsych's developers, for free.
  - It answers every save with a status, so the page can retry, and can hold the participant until the last save has
    arrived, as Prolific advises.
  - **It stops writing to OSF after 2026-11-16,** because OSF is closing its projects feature. Its storage
    providers are now Google Drive, Dataverse and Zenodo. Google Drive is the simplest of the three.
  - It holds no independent security certification and is not HIPAA compliant, by its own account. The study collects
    no health information.
  - Whether SJSU's Google accounts allow DataPipe to add files is not known. The ethics application names the
    storage, and the owner may pick another provider or account.
- **Not chosen.** A JATOS server, such as the free MindProbe, is built for studies like this one, but it is one more
  service holding the data until it is downloaded. A server on Atlas would put a home machine on the open internet
  for the length of the study.

## Deploying (owner, after the seal and the ethics approval)

1. **DataPipe.** Make an account at pipe.jspsych.org, connect the storage (Google Drive), and create one experiment
   for the pilot. Turn on data validation (JSON) and set the session limit well above the number of files expected:
   about 15 checkpoints per participant. Copy the experiment's id.
2. **Prolific.** Create the study: adults in the United States, fluent in English, desktop or laptop; the study URL
   with Prolific's URL parameters (`PROLIFIC_PID`, `STUDY_ID`, `SESSION_ID`); two completion codes, one for finishing
   and one for a quiz failed twice, both paid the base payment. The completion URL is
   `https://app.prolific.com/submissions/complete?cc=<code>` (Prolific's documentation, read 2026-11-06).
3. **config.js.** Fill in the experiment id, the two codes, the receipts address and the contacts, and set
   `consent_draft` to false once the board's approved consent is in `text.js`.
4. **The page.** Copy this folder, with the filled `config.js`, to the public repository, and turn on GitHub Pages.
   Check the deployed files against `MANIFEST.json`.
5. **A test session** from Prolific's preview, before launch, to see a file arrive in the storage. Turn on DataPipe's
   "accept new data" only then.

## After the study (owner)

1. Download every file from the storage into a private folder, and save Prolific's list of the study's participant
   IDs, every status included, one per line.
2. `python export_pilot.py review RAW --prolific IDS.txt --out REVIEW`. `review.csv` gives each participant's status
   for approving submissions; `problems.json` lists any session that fails a check.
3. Pay the bonuses with `REVIEW/bonuses.csv`, one `<participant ID>,<dollars>` line per bonus. Prolific's help page
   describes the bulk bonus list as submission IDs and amounts, and its API accepts participant IDs too (read
   2026-11-06). If the web form refuses participant IDs, Prolific's submission list gives each one's submission ID.
4. Make the donations, one payment per charity, from `REVIEW/donations.json`, and keep the receipts.
5. Write `PAID.json` beside the bonus file as paid: `{"bonuses_csv": "bonuses.csv", "donations": {"<charity>":
   {"dollars": "...", "date": "...", "receipt": "..."}}}`.
6. `python export_pilot.py export RAW --prolific IDS.txt --paid PAID.json --out EXPORT.json --source human`, then
   `split_pilot.py` and `pilot_analysis.py analyse`, as PILOT.md says. None of these files enters the public
   repository.

A participant's first session counts, whatever its status. A second session in another browser has seen the trials,
so its choices are not counted. If only the second one finished, the bonus is paid from it, and the export lists the
participant as not finished.

**In the main study** (`mode: "main"` in `config.js`, after the seal of PILOT.md's step 10), steps 1 to 4 are the same,
with `--mode main` on `review`. `PAID.json` is not needed, since only the pilot's export reads it. In place of step 6,
run `python main_analysis.py export RAW --prolific IDS.txt --pilot-ids PILOT_SPLIT/id_map.json --out MAIN --source
human`, then `main_analysis.py grade` (`../MAIN.md`). The main study has no split and no sealed file. Its export's
record says how many people qualify so far, which is when recruitment can stop.

## Known limits

- **The draw runs in the participant's browser.** Someone who edits the page could change their record.
  `export_pilot.py` recomputes every payment from the recorded choice and coin and refuses a record that does not
  match, but it cannot tell a forged choice from a real one. The most a forged record can gain is the difference
  between two bonuses, at most $5.
- **The quiz's answers are in the page's code,** as every web page's are.
- **A second browser starts a second session.** The browser's storage resumes a reload, not a new device. The export
  counts the first session.
- **The consent text is a draft.** The board's approved text replaces it, and a change to anything sealed means a new
  seal.

## The charities' status, checked 2026-11-06

PILOT.md ("The open items", 4) says each charity's tax-exempt status is checked when the instrument is built. The IRS's
Tax Exempt Organization Search refused automated access, so the check used the IRS's own bulk files behind it,
downloaded on 2026-11-06 (`apps.irs.gov/pub/epostcard`): the Publication 78 list of organizations eligible for
deductible contributions (file of 2026-10-13) and the automatic revocation list (2026-11-06).

| Charity | Legal name in Publication 78 | EIN | Code | Revoked |
|---|---|---|---|---|
| American Red Cross | American National Red Cross, Washington DC | 53-0196605 | PC | no |
| Doctors Without Borders USA | Medecins Sans Frontieres USA Inc., New York NY | 13-3433452 | PC | no |
| Feeding America | Feeding America, Chicago IL | 36-3673599 | PC | no |
| St. Jude Children's Research Hospital | St. Jude Childrens Research Hospital Inc., Memphis TN | 62-0646012 | PC | no |
| World Wildlife Fund | World Wildlife Fund Inc., Washington DC | 52-1693387 | PC | no |

PC is the IRS's code for a public charity, to which contributions are deductible up to 50% of income (60% for cash),
by its Publication 78 data dictionary. St. Jude's fundraising and awareness organization is ALSAC, listed as American
Lebanese Syrian Assoc Char Inc., Memphis TN, EIN 35-1044585, also PC and not revoked. If the donation goes through
ALSAC, its receipt may carry that name.
