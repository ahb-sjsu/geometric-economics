# Ethics application: the correlation-attitude study, for SJSU's IRB

**Status: a draft by Claude, written 2026-11-08 at the owner's request ("draft the ethics application"). Not
submitted.** The owner accepted the choices listed below on the same day. The owner fills in the marked fields and
submits the application in IRB Mentor, SJSU's online system. The answers follow the order of the questions in SJSU's blank IRB Mentor application, a PDF on
the IRB's forms page (read 2026-11-08). The live form may differ in places.

The study is the pilot and the main study of `../DESIGN.md` and `../PILOT.md`, sealed on 2026-11-07 under the signed
tag `prereg-correlation-v1`. One application covers both phases. Every number below comes from those documents, from
the page's code in `../instrument/`, or from the SJSU, Prolific, DataPipe and GitHub pages named where they are used.

## Before submitting

### What only the owner can fill in

Each place is marked `[OWNER: ...]`.

1. **The PI's title and department, qualifications, and CITI certificate.** SJSU's submission checklist requires
   human-subjects training through CITI completed in the last five years.
2. **The start date.** It cannot be retroactive. SJSU puts exempt review at about one week, not counting revisions
   (its "review types" page, read 2026-11-08). After approval the approved consent goes into the page and the study
   is sealed again (below), and the accounts are set up (`../instrument/README.md`, "Deploying"). The date should
   leave time for both.
3. **Funding.** Whether the study is funded, and by what. PILOT.md estimates about $7,700 for both phases, at the cap
   of 240 with 30% flagged and everyone included. The maximum enrollment requested below is a worst case and would
   cost more: roughly $16,000 if every place were used and paid in full, at PILOT.md's costs per person.
4. **Financial conflicts of interest.**
5. **Contact details.** These are the address participants write to, the page where the donation receipts will be
   published, and the line for questions about participants' rights.
   - SJSU's IRB contact page (read 2026-11-08) lists Alena Filip, Human Protections Analyst, Alena.Filip@sjsu.edu,
     (408) 924-2479.
   - The consent templates in SJSU's Informed Consent Handbook give irb@sjsu.edu at the same number.
   - Which of the two SJSU wants on a consent notice is not stated on the pages read. The IRB office can say.
6. **The storage account (choice C1).** Whether DataPipe can connect to an SJSU Google account is not known
   (`../instrument/README.md`, "Hosting"). Check before submitting, since the data plan rests on it.
7. **The computer on which the PI handles the files that contain Prolific IDs (choice C2).**

### Choices made in this draft

Claude made these choices in drafting. The owner accepted all seven on 2026-11-08 ("go with your choices"). The text
below uses each one where marked.

- **C1. The data go into the PI's SJSU Google Drive, not a personal account.**
  - `../instrument/README.md` says "the owner's Google Drive".
  - SJSU's Data Management Handbook quotes CSU policy: "Employees must not store or transmit protected University
    data using services hosted by third parties which do not have a contract in place with the campus or its
    Auxiliaries, such as personal cloud accounts."
  - The session files hold Prolific IDs. SJSU's form lists "unique ID numbers not created for the study" as direct
    identifiers.
  - DataPipe also has no contract with SJSU. The draft says so, and the board may ask for more.
- **C2. Prolific IDs never reach the analysis workstation or the AI assistant.**
  - The PI alone runs the steps that read the IDs, on the computer named in item 7:
    - `export_pilot.py review`, for payments;
    - the export;
    - in the pilot, `split_pilot.py`, which replaces the IDs with codes. In the main study the export does that
      itself.
  - Only the coded files go further.
  - The steps in `../instrument/README.md` stay the same, apart from who runs these.
  - SJSU's handbook advises institutional devices for Level 2 data, the level of the Prolific IDs.
- **C3. Files with Prolific IDs are deleted three years after the main study ends.** That is the CSU minimum for
  research records. SJSU's handbook allows identifiers needed only to track participants to go sooner. The coded data
  are kept.
- **C4. The consent notice says the coded choices may be shared in a public archive.**
  - Without that sentence the sealed protocol keeps per-person rows private ("Per-person rows stay private unless the
    consent covers sharing them", PILOT.md, "Data and provenance").
  - They could then never be shared, since participants cannot be asked again.
  - "May" keeps the decision open.
- **C5. Stopping early is unpaid, except after a technical problem.**
  - Someone who stops partway and returns the study on Prolific is not paid, as is usual there.
  - Someone stopped by a technical problem who writes to the PI on Prolific is paid the base payment.
  - The alternative is to pay everyone who stops in proportion to the choices made.
  - SJSU's form asks for either rule to be disclosed on the consent document, and the notice discloses it.
- **C6. Participants can withdraw their data until the study closes on Prolific,** by a message to the PI. After that
  the coded data stay in the registered analysis.
- **C7. The AI assistance is disclosed under "Other issues".** The form does not ask about it.

### What approval means for the sealed study

- **The consent text changes.**
  - The consent screen's wording is in `../instrument/text.js`, which the seal `prereg-correlation-v1` covers.
  - SJSU's forms page requires the consent shown online not to deviate from the stamped notice, and to link to a
    stamped copy that participants can print or download.
  - The sealed draft also lacks three things SJSU's templates and handbook ask for: a statement of purpose, what
    someone who stops early is paid, and how long identifying data are kept.
  - So `text.js` changes after approval, to show the approved notice word for word with the link.
- **A changed `text.js` needs a new round trip and a new seal.** It changes the page's build hash, so the round trip
  (`../instrument_roundtrip.py`, on Atlas) runs again. Then a new seal is made with the owner's OK, before the pilot.
  PILOT.md foresaw this: "A change to anything sealed, such as the consent text after the ethics review, needs a new
  seal."
- **The board may ask for changes to how the page behaves.** Two are possible here: letting participants skip the
  pilot's closing questions, and clearing the browser's copy of the session at the end. Both are in `task.js` and
  would go into the same new seal.
- **`config.js` is not sealed.** It gets the contact details, the protocol number and the receipts address, and
  `consent_draft: false`.

### Attachments to upload

IRB Mentor takes files, not links (SJSU's checklist).

| File | Where it goes in the form |
|---|---|
| `consent_notice_pilot.docx`, `consent_notice_main.docx` | Consent Document Attachment(s). Bottom margins of one inch, for the stamp |
| `recruitment.docx` | Recruitment Materials Attachment(s) |
| `instrument_screens.pdf` | Study Instruments Attachments |
| `DESIGN.docx`, `PILOT.docx` | Other Study Attachments: the registered design and pilot protocol |

The repository keeps the sources of these files, not the files, since it tracks no Word or PDF files. They are built
as follows.

- **Each Word file** comes from the Markdown file of the same name, in this folder or, for `DESIGN.md` and `PILOT.md`,
  one folder up: `pandoc NAME.md --reference-doc=REF.docx -o NAME.docx`. `REF.docx` is pandoc's default reference
  document (`pandoc -o REF.docx --print-default-data-file reference.docx`) with the page set to Letter and all four
  margins to one inch. The default document sets no margins.
- **`instrument_screens.pdf`** comes from `screens.html` and a folder `screens/` of screenshots beside it.
  `python ../instrument_screens.py screens` takes the screenshots, in the pilot's mode, and `python make_pdf.py`,
  run in the same folder, prints the page in headless Chromium. Both need Playwright and run on Atlas.

---

## The application, question by question

### Admin

- **Is this a multi-institutional, collaborative study?** No.
- **Department:** `[OWNER: department]`
- **PI type:** Faculty.
- **Review type requested:** Exempt, category 3(i)(B) of 45 CFR 46.104(d). The reasons are under "Other issues".

### Study personnel

**PI:** Andrew H. Bond, San José State University, `[OWNER: title, department]`. Training certificate:
`[OWNER: upload the CITI certificate]`.

**Qualifications.**
> The PI leads a research programme on geometric models of value and choice, and this study tests one of its models
> with people. `[OWNER: relevant training, and any earlier human-subjects research.]` The design, the analysis and the
> sample-size rule were registered before any data collection. The study's web page and its analysis were tested on
> simulated participants beforehand (attached: the design and the pilot protocol).

**Study activities carried out by this investigator.**
> All of them: the design, the study's web page, recruitment on Prolific, consent (on the web page), data collection,
> payments and donations, data management, and analysis.

**External study personnel.** None.

### Study timing and funding

**Anticipated start date.** `[OWNER: a date that leaves time for review and for the steps after approval]`

**Is the study currently funded?** `[OWNER]`

**Are you applying for funding?** `[OWNER]` Potential funding sources: `[OWNER]`

### Other institutions

**Names and roles of participating institutions.**
> None. Participants are recruited and paid through Prolific, a commercial platform for recruiting research
> participants. Prolific does not take part in the research. It does not see the study's responses, which go from
> the study's web page to the PI's storage.

### Study location

**Where will the study be conducted?** Online.
> Everything takes place on the study's web page, in the participant's own browser, at a time the participant
> chooses while the study is open on Prolific. There is no external site.

### Study design

**Study purpose.**
> Many choices affect both the chooser and someone else, and their results are often uncertain. Economists and
> psychologists describe how people value such options with mathematical models. This study tests one such model,
> developed in the PI's research, against its main rivals.
>
> The model says that a person judges each possible outcome by how far it falls short of the best possible outcome
> on both counts at once: their own earnings and a charity's donation. Only then does the person weigh the outcomes
> by their chances. Two predictions follow that the usual models do not make in this form.
>
> - **Correlation attitude.** Take two coin flips that give the same chances of each amount to the participant and to
>   the charity, but pair the amounts differently. In one, both amounts are high together or low together. In the
>   other, one is high when the other is low. The model predicts a definite preference between them, whose size
>   depends on how the person trades off their own earnings against the charity's.
> - **Background dependence.** How much risk a person accepts over their own earnings changes with how much the
>   charity receives.
>
> The research questions are these.
> - H1 to H3: does the model predict each person's choices better than three rivals? The model and its rivals are
>   calibrated on the person's choices without risk and on simple coin flips. Each then predicts the person's other
>   choices. The claim needs H1, H2 and H3 together.
> - H4: do the model's predictions track the differences between people better than its two strongest rivals'
>   predictions do?
> - Secondary: do people show aversion to inequality between themselves and the charity, a rival explanation the
>   study can tell apart?
>
> The hypotheses, the analysis and the rule that sets the main study's size were registered in a public repository
> before any data were collected. The pilot measures quantities the design needs and tests no hypothesis.

**Study background.**
> How people value options with several attributes under risk has a long theoretical history. Richard (1975) and
> Epstein and Tanny (1980) defined correlation aversion: preferring a gamble that spreads good and bad outcomes
> across attributes over one that pairs them. Keeney and Raiffa (1976) set out when risk attitude over one attribute
> can depend on the level of another. Measured correlation attitudes vary by domain. People are averse over income at
> different times (Andersen et al., 2018; Rohde and Yu, 2024). Over longevity and wealth they are averse for gains and
> seeking for losses (Attema et al., 2019). Donors are averse across two aid outcomes (Gangadharan et al., 2019).
>
> When choices affect another person, people's own risk taking shifts with the other's payoff (Linde and Sonnemans,
> 2012; Schwerter, 2024), and risk can serve as an excuse to give less to a charity (Exley, 2016). The closest
> study, Berg and Rietz (2026), ties each lottery's outcome for the subject to a matched person's payoff. No study
> we found offers coin flips over pairs of (own earnings, charity donation) in which the pairing of the outcomes is
> flipped while each attribute's chances stay fixed. None measures risk attitude over one's own money as the
> charity's amount changes. This design does both, and links both effects to each person's trade-offs without risk
> through one model, tested against named rivals.
>
> References (checked against the publisher, RePEc or a university repository on 2026-11-08; Epstein and Tanny, and
> Keeney and Raiffa, as in DESIGN.md's prior-art list, read 2026-11-03)
> - Andersen, S., Harrison, G. W., Lau, M. I. and Rutström, E. E. (2018). Multiattribute utility theory, intertemporal
>   utility, and correlation aversion. *International Economic Review* 59(2):537–555, doi:10.1111/iere.12279.
> - Attema, A. E., L'Haridon, O. and van de Kuilen, G. (2019). Measuring multivariate risk preferences in the health
>   domain. *Journal of Health Economics* 64:15–24, doi:10.1016/j.jhealeco.2018.12.004.
> - Berg, J. and Rietz, T. (2026). Do unto others: a theory and experimental test of interpersonal preference factors
>   in decision making under uncertainty. *Journal of Risk and Uncertainty*, doi:10.1007/s11166-026-09495-9.
> - Epstein, L. G. and Tanny, S. M. (1980). Increasing generalized correlation: a definition and some economic
>   consequences. *Canadian Journal of Economics* 13(1):16–34.
> - Exley, C. L. (2016). Excusing selfishness in charitable giving: the role of risk. *Review of Economic Studies*
>   83(2):587–628, doi:10.1093/restud/rdv051.
> - Gangadharan, L., Harrison, G. W. and Leroux, A. D. (2019). Are risks over multiple attributes traded off? A case
>   study of aid. *Journal of Economic Behavior and Organization* 164:166–198, doi:10.1016/j.jebo.2019.05.025.
> - Keeney, R. L. and Raiffa, H. (1976). *Decisions with Multiple Objectives.* Wiley.
> - Linde, J. and Sonnemans, J. (2012). Social comparison and risky choices. *Journal of Risk and Uncertainty*
>   44(1):45–72, doi:10.1007/s11166-011-9135-z.
> - Richard, S. F. (1975). Multivariate risk aversion, utility independence and separable utility functions.
>   *Management Science* 22(1):12–21, doi:10.1287/mnsc.22.1.12.
> - Rohde, K. I. M. and Yu, X. (2024). Intertemporal correlation aversion: a model-free measurement. *Management
>   Science* 70(6):3493–3509, doi:10.1287/mnsc.2023.4863.
> - Schwerter, F. (2024). Social reference points and risk taking. *Management Science* 70(1):616–632,
>   doi:10.1287/mnsc.2023.4698.

**Research design.**
> An experiment in which each participant makes every choice: 140 choices in one online session, 160 in the pilot, in
> an order shuffled for each person. It runs in two registered phases.
> - A pilot of 120 counted participants measures quantities the design needs, such as how noisy people's choices
>   are, how many people ignore the charity, and how long the session takes. It tests no hypothesis.
> - A rule registered in advance then sets the main study's size: 120, 160, 200 or 240 counted participants.
>
> The procedures are the same in both phases, apart from 20 extra choices and four closing questions in the pilot.

**Data collection methods.**
> A web page built for the study, which participants open from Prolific. It records each choice and how long it
> took, the charity chosen, the answers to a four-question quiz on the payment rules, and, in the pilot only, four
> closing questions (see "Data instruments").

**Data analysis methods.**
> All analyses were registered before data collection, and the code was tested on simulated participants first.
> - **Fitting.** For each participant, the PI's model and three rivals are fitted to the calibration choices: the
>   choices without risk, and the coin flips over one amount while the other is at its maximum of 100 points. Each
>   fit uses maximum likelihood, with a prior estimated from the sample. Each fitted model then predicts the
>   participant's other choices without refitting.
> - **H1 to H3** compare the models' prediction error on those choices (log-loss), with 95% intervals clustered by
>   participant. Each passes when the PI's model is better by a registered margin of 0.005 per choice.
> - **H4** compares, across participants, rank correlations between each model's predicted and observed
>   preferences, with a bootstrap interval.
> - **Model-free checks.** Do choices between the paired coin flips depart from even odds? Does risk taking over
>   one's own earnings change with the charity's amount?
> - **A hierarchical Bayesian model** estimates the population value of the model's risk parameter.
> - **A secondary test** scores inequality aversion on 20 choices built for it.
> - **The pilot** computes summary quantities and quality checks, and reads the main study's size from a table of
>   simulated studies computed in advance.

**Does this study meet the definition of a clinical trial?** No.

### Subject population

**Type of subjects.**
> Adults, 18 or older, who are members of Prolific, an online platform where people sign up to take part in research
> for pay. They must live in the United States, be fluent in English, and take part on a desktop or laptop computer.
> Prolific's own filters select them. Anyone who took part in the pilot cannot take part in the main study.

**Rationale for subject selection.**
> - **Payment.** The study needs adults who can be paid real money and can direct real donations. Prolific pays
>   participants and their bonuses itself.
> - **Attention.** Participants must read the payment rules closely.
>   - Douglas, Ewell and Brauer (2023, *PLOS ONE* 18(3):e0279720) found Prolific's and CloudResearch's participants
>     more likely than MTurk's, Qualtrics' and SONA's to pass attention checks.
>   - Peer and colleagues (2022, *Behavior Research Methods* 54:1643–1662) found that, without filters, only Prolific
>     gave high data quality on every measure. Three of their five authors worked at Prolific.
> - **Country.** The United States goes with the PI's institution, payment in dollars, and US charities whose
>   donation receipts can be published.
> - **Device.** A desktop or laptop gives everyone the same kind of screen and input, since response times are
>   recorded.

**Number of subjects.**
> - **Pilot.** Recruitment continues until 120 participants meet the inclusion rule. Those who fail the quiz, stop
>   early or miss more than two attention checks add to the number who take part. At the limits of the pilot's
>   registered quality bars, about 210 would take part: 80% pass the quiz within two tries, 85% of those finish, and
>   85% of finishers meet the attention rule. We request approval for up to 250 in the pilot.
> - **Main study.** The main study counts n participants who meet the inclusion rule and are not flagged as
>   ignoring the charity. n is 120, 160, 200 or 240, set from the pilot by a rule registered in advance. The flagged
>   are paid in full but not counted.
>   - At n = 240, if 40% are flagged, and at the quality limits above, about 690 would take part.
>   - We request approval for up to 700 in the main study, so at most 950 in all. If more are needed, the PI will
>     submit a modification.
> - **How the sizes were chosen.** The sizes come from a power analysis by simulation. At n = 120 the registered
>   claim passed in 94% to 98% of simulated studies when the model is right and its cost behaves like distance. It
>   passed in none of the simulated studies under four rival models (the registered design and pilot protocol,
>   attached). The pilot sets the main study's size because the power depends on quantities that only real
>   participants can show.

**Inclusion and exclusion criteria.**
> - **Inclusion,** applied by Prolific's filters: 18 or older (all Prolific members), living in the United States,
>   fluent in English, on a desktop or laptop computer. The page also asks for a browser window at least 1000 by 620
>   pixels, and waits until the window is large enough.
> - **Exclusion.** Pilot participants are excluded from the main study, by Prolific's filter and again in the
>   analysis. There is no other screening. There is no criterion on race, ethnicity or gender, nor on age beyond
>   being 18 or older.
> - **Who is counted, as distinct from who is paid.** The analysis counts those who:
>   - pass the quiz within two tries;
>   - finish;
>   - choose the worse option in at most 2 of the 8 attention checks;
>   - in the main study, are not flagged as ignoring the charity. Someone is flagged who nearly always kept their own
>     points in the choices where giving some up would have given the charity two or three times as many.
>
>   Everyone who finishes is paid in full. The data of those not counted are kept and reported apart.

**Selection criteria.**
> None beyond the above. Prolific shows the study to eligible members, who take places first come, first served,
> until the target is reached.

**Subjects' ages.** 18 years or older.

**Vulnerable populations.** None of the above.
> No vulnerable group is targeted or expected beyond its share of the general adult population on Prolific.

**Prior associations with the research team.** No.
> Prolific members are unknown to the PI, who sees only their Prolific IDs.

**Potential interpersonal conflicts of interest.** No.

### Recruitment

**Recruitment and enrollment procedures.**
> - **The listing.** The PI posts the study on Prolific with the listing text attached. Prolific shows it to members
>   who meet the filters, and they choose whether to start.
> - **The link.** Starting the study opens its web page, with the member's Prolific ID in the link. The page first
>   shows the consent notice.
> - **No direct contact.** The PI does not contact anyone directly.
> - **The order of the phases.** The pilot runs first. The main study is posted after the pilot's analysis, with
>   pilot participants excluded.

**Recruitment materials.**
> The Prolific study listing, one for the pilot and one for the main study (attached). It gives the title, the PI's
> name, affiliation and contact, what participants will do, the time and the payment. It is posted only on Prolific,
> which also shows the payment, the estimated time and the devices allowed.

### Consent

**Type of consent document.** Consent notice.
> There are two notices, one for the pilot and one for the main study. They differ only in the time, the number of
> choices, the base payment and the pilot's closing questions. Documentation of consent (a signature) is not
> collected, as SJSU's handbook allows for exempt online studies.

**Who will obtain consent and answer participants' questions?**
> The consent notice is the study page's first screen. The PI, Andrew H. Bond, answers questions through Prolific's
> messages or by email.

**How, when and where will consent be obtained?**
> Online, on the study's web page, before anything is recorded.
> - The participant reads the notice and clicks "I agree, and I am 18 or older" or "I do not agree".
> - Declining ends the session, and nothing is recorded.
> - The page shows the approved notice word for word, with a link to the stamped copy that participants can print or
>   download.
> - No signature is collected. The session record keeps the time of agreement.

**Language(s).** English.

**Legally authorized representatives.** No.

### Assent

Not applicable. Only adults take part.

### Study procedures

**Does the study involve accessing secondary data only?** No.

**Procedures, in order.** The main study is the same without step 9.
> 1. On Prolific, the participant reads the listing and starts the study. The study's web page opens.
> 2. If the link lacks a Prolific ID, the page asks the participant to start from Prolific. If the window is
>    smaller than 1000 by 620 pixels, the page asks for a larger one, and continues once it is large enough.
>    Nothing is recorded at this step.
> 3. **Consent notice.** The participant agrees or declines. Declining ends the study, and nothing is recorded.
> 4. **How the study works:** one screen.
> 5. **The charity.** The participant chooses one of five charities, each with one line on what it does. Its
>    donation, if any, comes from the paid choice.
> 6. **The rules,** with an example of a sure option and of a coin-flip option, and how a paid choice turns into a
>    bonus and a donation.
> 7. **Four multiple-choice questions on the rules.**
>    - A wrong answer brings the rules again and a second try.
>    - Two wrong tries end the study, and the participant is paid the base payment.
> 8. **The choices,** one at a time, in an order shuffled for each participant: 160 in the pilot, 140 in the main
>    study.
>    - Each is between two options shown as cards, with bars and numbers for "You" and the charity, on scales from 0
>      to 100 points.
>    - An option is either sure or a coin flip with two outcomes, each with a 1 in 2 chance.
>    - A blank screen of 0.3 seconds separates two choices. Progress is saved every 20 choices, and a reload resumes
>      the same session.
> 9. **Pilot only: four closing questions.**
>    - How sure are you that the donation will be made? (1 to 5)
>    - Which choices are paid? (multiple choice)
>    - How hard were the choices? (1 to 5)
>    - How did you make your choices? (optional, free text)
> 10. **The paid choice.**
>     - The computer draws one of the participant's choices at random. If the option chosen in it is a coin flip,
>       the computer flips a fair coin.
>     - The screen shows the result: the bonus to the participant and the donation to the charity, at 5 cents a
>       point.
> 11. **The return to Prolific,** once the last save has arrived.
>
> After the session the participant does nothing more. The PI approves submissions and pays the bonuses on Prolific.
> The PI also makes the donations and publishes the receipts.

**Content of the intervention.**
> Behavioral. Participants choose between options that give points to themselves and to a charity they picked. Some
> options are sure, and some depend on a coin flip. One choice per participant is paid for real at 5 cents a point.
> The participant's points become a bonus, and the charity's points a donation to that charity. Every option is
> shown in full, and nothing is hidden or false.
>
> The choices fall into a few kinds:
> - choices without risk, which measure how each person trades their own points against the charity's;
> - coin flips over one of the two amounts at a time;
> - pairs of coin flips that differ only in how the two amounts are paired across outcomes;
> - 8 attention checks, in which one option is 40 points worse for both the participant and the charity;
> - 20 choices in which the participant's and the charity's amounts cross, built to detect inequality aversion;
> - in the pilot only, 20 more: some earlier choices repeated with the sides swapped, and a few with wider trade-offs
>   or larger rewards for risk.

**Cognitive, psychological or usability tests on a computer.**
> The choice task above is the only computer task. The quiz checks that the participant understands the payment
> rules. Screenshots of every screen are attached.

**Who will conduct the procedures, and where and when?**
> The PI, Andrew H. Bond. Online, at a time each participant chooses while the study is open on Prolific. Four
> outside services are involved:
> - **Prolific:** recruitment and payment.
> - **GitHub Pages:** hosts the study's web page. It is a static page with no server of its own, and its code is
>   public.
> - **DataPipe** (pipe.jspsych.org): a free service run by the developers of jsPsych. It passes each saved file from
>   the participant's browser to the PI's storage.
> - **Google Drive,** on the PI's SJSU account (choice C1): storage.

**Frequency and duration.**
> One session, with no follow-up. It takes about 42 minutes in the pilot (160 choices and four closing questions)
> and about 35 minutes in the main study (140 choices). The times include the consent, the rules and the quiz.

**Alternatives for those who choose not to take part.**
> Not taking part. Prolific members choose freely among many studies.

**Classroom setting.** No.

**Deception or incomplete disclosure.** No.
> - **Every payment is real.** The paid choice's points are paid as a bonus and donated to the charity, and the
>   receipts for the donations are published.
> - **The purpose is stated in general terms.** The consent notice says the study compares models of how people
>   value such choices. It does not state the specific predictions, so as not to steer the choices.
> - **The notices say that a few choices check attention,** and the pilot's that a few appear twice, but not which.

**Costs to participants.** No.

**Incentives or compensation.** Yes.
> - **Base payment.** $8.40 in the pilot and $7.00 in the main study, paid through Prolific. That is $12 an hour for
>   the expected time, Prolific's recommended rate; its minimum is $8 an hour (Prolific's help page on IRB
>   applications, read 2026-11-08). If the median session runs longer than expected, the base payment is raised to
>   keep $12 an hour.
> - **Bonus.** One choice drawn at random pays the participant's points at 5 cents a point, up to $5.00. Over the
>   pilot's choices it averages about $3.70 to $3.90, depending on how the person chooses (PILOT.md). It is paid
>   through Prolific after the study.
> - **Donation.** The same choice's charity points, at 5 cents a point and up to $5.00, go to the charity the
>   participant chose. It averages about $1.70 to $2.00. This is not compensation to the participant.
> - **Partial compensation and attention checks.**
>   - Someone who fails the quiz twice is paid the base payment.
>   - Attention checks never change anyone's payment, and everyone who finishes is paid in full.
>   - Someone who stops partway and returns the study on Prolific is not paid. Someone stopped by a technical problem
>     who writes to the PI on Prolific is paid the base payment (choice C5).
>   - The consent notice says all of this.

**Will you collect identifying information to award the compensation?** No.
> Payment goes through Prolific under the participant's Prolific ID. Prolific holds participants' payment details.
> The PI collects no names, addresses or other identifiers.

### Data instruments and recording devices

**Information to be gathered, and the means of collecting it.**
> The study's web page records the following and saves it as the participant goes:
> - the Prolific ID, and Prolific's study and session identifiers, which arrive in the link;
> - a random session code, and the random seed that sets the order of the choices;
> - the time of agreement, of the 140th choice, and of the draw of the paid choice;
> - the charity chosen and the quiz answers;
> - for each choice, which option was chosen and how long the choice took;
> - in the pilot, the answers to the four closing questions;
> - the paid choice, the coin, the bonus and the donation;
> - the size of the browser window at the start;
> - how many times the page was reloaded, and how many times it was hidden during the choices (the participant
>   switched to another tab or minimized the window);
> - any failed saves, and a code identifying the version of the page.
>
> It does not record names, contact details, IP addresses, demographics, or anything about the device beyond the
> window size. No previously collected data are used.

**Study instrument types.**
> Survey/Questionnaire: the quiz on the rules, and the pilot's four closing questions. Other: a computer-based choice
> task.
>
> The other instrument is the study's web page, which presents the choices and records them as above. Screenshots of
> every screen are attached.

**Study instruments attachments.** `instrument_screens.pdf`

**Recording devices.** No recording devices will be used.
> No audio, video, photographs or physiological measures. The page records clicks and times only.

### Medical devices

No.

### Subject identifiers

**Will investigators know, have access to, or collect any direct identifying information?** Yes.
> - The Prolific ID, and Prolific's session identifier. SJSU's form counts these as "unique ID numbers not created
>   for the study".
> - They are pseudonymous. Prolific holds the link to a person's identity, and the PI cannot see it. In Prolific's
>   words, "Researchers identify participants using their unique Prolific ID rather than their names or other direct
>   identifiers" (help page on IRB applications, read 2026-11-08).

**Will investigators know, collect, or have access to indirect identifying information?** No.
> The data hold no demographics, location or employer. The charity chosen, the choices and the response times could
> not identify a person, even combined.

### Data management plan

**What kind of direct identifying information will be known or collected?**
> The Prolific ID and Prolific's session identifier.

**What is the intended use of the identifying information?**
> - to approve each submission and pay each bonus on Prolific;
> - to count a person's first session only, if they open the study twice;
> - to keep pilot participants out of the main study;
> - to delete a participant's data on request;
> - to answer messages.

**Level 1 or 2 data elements?** Yes.
> - Level 2: the Prolific ID and session identifier, and every file that links them to responses. That means the
>   saved session files, Prolific's list of the study's participants, the bonus list, the pilot's full export and
>   the key files below. SJSU's Data Management Handbook places identifiable personal information at Level 2. It
>   also says that unlabeled information defaults to Level 2.
> - No Level 1 data are collected.

**Format.** Digital only.

**Where will files with direct identifying information be stored?** Choices C1 and C2.
> - **During the study.** Each saved session file goes through DataPipe into a folder in the PI's SJSU Google Drive.
> - **After each phase.** The PI downloads the files, with Prolific's list of participant IDs, to a private folder
>   on `[OWNER: the computer, e.g., an SJSU-issued laptop]`. There the PI prepares the payments and runs the export
>   and, in the pilot, the split.
> - **The export,** followed in the pilot by the split, writes coded files without Prolific IDs and one key file
>   that links the codes to Prolific IDs.
>   - The session files, the participant list, the bonus list, the pilot's full export and the key file stay in the
>     two private folders.
>   - Only the coded files are copied to the analysis workstation.
> - **The participant's browser** keeps a copy of that participant's own session, which the page uses to resume
>   after a reload. It stays there until the participant clears the browser's data.

**Security features for each location.**
> - **The SJSU Google Drive folder** is reached through SJSU's single sign-on `[OWNER: and multi-factor
>   authentication, if SJSU's accounts use it]`. It is not shared with anyone.
> - **The computer** is password protected `[OWNER: and its disk encrypted]`.
> - **DataPipe's experiment is deleted once its files are downloaded.** That removes DataPipe's log for it.
>   DataPipe's privacy page says the log can hold the names of files that failed to save, and the study's file names
>   contain the Prolific ID.
> - **No secrets in the page.** The page's code holds no passwords, and no keys to the storage.
> - **Stray files are left out.** Anyone who reads the page's code could send files to the study's folder. The
>   export leaves out files from anyone not on Prolific's list of the study's participants.

**De-identification: method, timing, and who is responsible.**
> - **The method** is coding (pseudonymization).
>   - The export keeps only the fields the analysis needs. It drops Prolific's session identifier, the window size,
>     and the counts of reloads and hidden pages.
>   - Each Prolific ID is replaced with a study code: p001, p002 and so on in the pilot, by the split that follows
>     the export; m0001 and so on in the main study, numbered by start time, by the export itself.
> - **When.** The PI runs these steps after each phase's data collection and payments. In the main study the PI
>   also runs the export during recruitment, to count who qualifies.
> - **Who.** The PI is responsible.

**Where is the key to the code stored, and how is it protected?**
> - **The key files** are `id_map.json` for the pilot and `main_id_map.json` for the main study. They are kept in the
>   private folders, apart from the coded data. They are never published or copied to the analysis workstation.
> - **The pilot's key has one more use:** keeping pilot participants out of the main study's data.
> - **No consent forms are signed,** so none is stored.

**International travel with identifying information.** `[OWNER: none planned]`

**Which team members will have access to identifying information?**
> Only the PI.

**Will access to identifying information be granted to individuals, institutions or vendors outside the research
team, or without a contract with SJSU?** Yes.
> 1. **Prolific** knows who its members are, and holds their payment details. It sees the study's listing, its link,
>    who started and finished, and the completion code. It does not see the responses. In its words, "Prolific
>    cannot see or store the responses participants submit directly to your external study tool" (help page on IRB
>    applications, read 2026-11-08).
>    - Rationale: it recruits and pays.
>    - Access is under Prolific's terms with its members and with researchers.
> 2. **DataPipe** receives each saved file, including the Prolific ID, and passes it to the PI's storage.
>    - Its privacy page (last updated 16 September 2026, read 2026-11-08) says it "keeps no copy afterwards" in
>      normal operation. The exceptions are a temporary encrypted copy during transfer, and files held for up to 14
>      days while the storage cannot accept them.
>    - It also says DataPipe's own code "never reads, stores, or forwards a participant's IP address or browser user
>      agent". Requests pass through Google Cloud, whose own request logs are kept for 30 days. DataPipe runs on
>      Google Cloud in the United States.
>    - Rationale: a static web page has no server of its own to save to, and DataPipe is a free service built for
>      studies like this one.
> 3. **Google** stores the files in the PI's SJSU Google Drive. This is SJSU-licensed storage, reached through SJSU's
>    single sign-on (choice C1).
> 4. **GitHub** hosts the page and receives no study data. GitHub's documentation says a Pages visitor's "IP address
>    is logged and stored for security purposes". The PI cannot see those logs.
>
> **Steps to ensure proper handling.**
> - Each service receives only what it needs to do its job.
> - Prolific IDs never reach the analysis workstation.
> - The DataPipe experiment is deleted once its files are downloaded.

**Will any information that could identify participants be reported?** No.

**Mechanisms to maintain confidentiality in reporting.**
> Study codes in place of Prolific IDs, and statistics over participants. Any estimate for a single participant is
> reported under a code.

**Limits to confidentiality.** Yes.
> - **Prolific** knows who took part.
> - **The outside services** pass and store the files under their own policies, as described above.
> - **Each participant's browser** keeps a copy of their own session until they clear it.
> - **The pilot's optional written answer** holds whatever a participant types. It is kept private and never shared.
>
> The consent notices describe the first three. The pilot's notice also says that written answers are never shared.

**Will data or findings be shared with external institutions from which subjects were recruited?** Not applicable.

**Will identifying information be retained or shared for future research?** No.
> 1. None is retained for future research.
> 2. None is shared with other investigators or repositories.
> 3. Participants will not be contacted again.
> 4. Until the study closes on Prolific, a participant can ask for their data to be deleted by a message to the PI
>    (choice C6). After that the coded data stay in the registered analysis.
>
> Separately, the coded choices, without Prolific IDs or written answers, may be shared in a public research archive
> (choice C4). The consent notice says so.

**Intended audience and reporting.**
> Researchers in economics, psychology and decision science, through journal articles, preprints and conference
> presentations. The registered design, the analysis code and aggregate results are public in the PI's GitHub
> repository.

**How long will identifying information and keys be kept?** Choice C3.
> The files that contain Prolific IDs are kept until three years after the main study ends, the CSU minimum for
> research records, and then deleted. They are the session files, Prolific's participant lists, the bonus lists, the
> pilot's full export and the key files. The coded data contain no Prolific IDs and are kept.

**How will identifying information be destroyed?**
> - **Google Drive:** permanent deletion, the trash included.
> - **The PI's computer:** a secure-deletion tool, as SJSU's data handbook advises for digital files.
> - **DataPipe:** each experiment is deleted once its files are downloaded.

**Who will conduct the destruction?** The PI.

### Risks and benefits

**Are there anticipated risks?** Yes, all minimal.

**Risks, with likelihood and seriousness.**
> 1. **Boredom or fatigue** from 35 to 42 minutes of similar choices. Likely for some participants, mild and
>    temporary.
> 2. **Mild discomfort** in choosing between one's own money and a charity's donation. Unlikely to be more than
>    mild. No choice touches a sensitive matter.
> 3. **Loss of confidentiality.** Unlikely, given the protections in the data management plan, and of low
>    seriousness. The data hold no names or contact details. The responses would not harm a participant if
>    disclosed: choices among point amounts, a charity and response times.
>
> There is no physical, legal or financial risk. Participants cannot lose money, and the bonus is never negative.

**Procedures to protect against or minimize each risk.**
> - **Stopping and resuming.** Participants can stop at any time. A reload resumes where they left off, so a break
>   costs nothing.
> - **Understanding the rules.** The rules are explained with examples and checked by a quiz, so no one plays
>   without understanding how they are paid.
> - **A fair draw.** The paid choice is drawn by the browser's cryptographic random number generator and shown to
>   the participant.
> - **Data protection,** as in the data management plan.

**Treatment for study-related injuries.** Not applicable. The study has no physical procedures.

**Potential group harm.** No.

**Potential benefits.** Yes.
> - **Participants** receive no direct benefit beyond the payment.
> - **Indirectly,** the results test competing models of how people value uncertain outcomes for themselves and for
>   others. Those outcomes bear on charitable giving and on decisions that affect other people.
> - **The charities** receive real donations from the paid choices.

### Financial conflicts of interest

**Do you or any investigator have a financial interest related to this research?** `[OWNER]`

### Other study attachments

> - The registered design (`DESIGN.docx`) and the pilot protocol (`PILOT.docx`), sealed on 2026-11-07 in the PI's
>   public GitHub repository, `ahb-sjsu/geometric-economics`, under the signed tag `prereg-correlation-v1`.
> - The references are in the "Study background" answer.

### Other issues

**1. The exemption requested: category 3(i)(B) of 45 CFR 46.104(d).** The criteria are as SJSU's Table of
Exemption Categories states them.
> - **A benign behavioral intervention.** Participants choose between options that give points, worth real money, to
>   themselves and to a charity. The regulation's own examples include "having the subjects play an online game"
>   and "having them decide how to allocate a nominal amount of received cash between themselves and someone else".
>   The amounts here are nominal: at most $5.00 to the participant and $5.00 to the charity, on top of the base
>   payment.
> - **Brief in duration.** One session of about 35 minutes in the main study and 42 in the pilot, with no follow-up.
>   Whether that counts as brief is the board's decision. If the board finds that the study does not qualify, the
>   PI asks for expedited review with a waiver of documentation of consent.
> - **Harmless, painless, not physically invasive,** not likely to have a significant adverse lasting impact, and
>   nothing a participant should find offensive or embarrassing. The choices are between point amounts for oneself
>   and a well-known charity of one's choosing.
> - **Adults who agree in advance,** on the consent screen. The information is collected through data entry
>   (clicks).
> - **Criterion (B).** Disclosure of a participant's responses would not place them at risk of criminal or civil
>   liability, or damage their financial standing, employability, educational advancement or reputation.
> - **No deception** (category 3(iii)).

**2. Two phases under one protocol.**
> - The pilot measures what the design needs and tests no hypothesis. A rule registered in advance then sets the
>   main study's size.
> - The procedures are the same in both, apart from the pilot's 20 extra choices and four closing questions.
> - The pilot's registered rules may call for more calibration choices of a kind it already has. If they do, or if
>   anything else in the procedures changes, the PI submits a modification before the main study.

**3. Real donations.**
> - **How they are made.** After each phase the PI makes one payment to each charity. Each payment is the total of
>   that charity's points over all paid choices, at 5 cents a point.
> - **The receipts** are published at `[OWNER: receipts address]` and carry no participant information.
> - **The five charities** were checked on 2026-11-06 against the IRS's Publication 78 list and automatic revocation
>   list. All five are public charities, and none has been revoked.
>
> | Charity | EIN |
> |---|---|
> | American Red Cross | 53-0196605 |
> | Doctors Without Borders USA | 13-3433452 |
> | Feeding America | 36-3673599 |
> | St. Jude Children's Research Hospital | 62-0646012 |
> | World Wildlife Fund | 52-1693387 |

**4. The registered design and the consent text.**
> - **Fixed before any data.** The design, the analysis code and the web page were fixed in a public repository
>   under a signed tag (2026-11-07).
> - **The approved notice replaces the draft.** It will replace the draft consent text on the page word for word,
>   with a link to the stamped copy, and the change will be recorded under a new signed version before recruitment
>   starts.

**5. AI assistance (choice C7).**
> - **Its role.** The PI used an AI assistant, Claude, made by Anthropic, to help write the study's web page, its
>   analysis code and a first draft of this application.
> - **No identifying information reaches it.** The assistant is not a member of the research team. The PI alone
>   handles the files that contain Prolific IDs, and only coded data are used with the assistant's help (choice C2).
