# Existing games, distribution and data collection: survey

**Status: survey, 2026-11-11.** From nine web searches by Claude on that day. Most statements
below come from search summaries and store listings, not from playing the games or reading the
papers and policies in full. Each is marked where that matters. Nothing has been built.

## 1. Games close to the proposal

The proposal is a daily game in which the player goes deeper for more reward and may bank or go
on (`DESIGN.md`, and the owner's exchange of 2026-11-11).

| Game | What it is | Overlap |
|---|---|---|
| Daily Dungeon (a Discord bot, `top.gg` listing) | One seeded dungeon a day for everyone. Every fifth floor the player chooses to descend for a bigger score or retire and bank it. Streak and leaderboard. | Closest found. Same daily seed and the same bank or go on choice. Lives inside Discord. |
| Cruel Dungeon (Product Hunt listing) | Daily roguelike, same dungeon for every player, first run ranked. | Daily shared seed. No bank or go on choice in the listing. |
| Daily Dungeon (`dailydungeon.net`) | A daily browser puzzle after the manner of Wordle. | Daily format only. A different game from the bot of the same name. |
| Delve: Dungeon Flip (itch.io) | Push your luck, one card at a time. | The mechanic, with no daily seed in the listing. |
| Mining and digging phone games (Pocket Mine, Dig Out and others) | Dig deeper for more. | Theme. None of the listings states a bank or go on choice. |
| Board games of the kind (Deep Sea Adventure, Diamant) | Tabletop push your luck with a dive or a mine. | The search found no digital version. Not confirmed either way. |

**Reading.** The mechanic and the daily format each exist, and one Discord bot combines them. No
web or phone game was found that does both, and none that assigns histories for research. So the
idea is not new as a game and we should not say it is. What would be ours is the hidden scripted
history and the fixed state. The game should have its own theme, name and rules and should copy
none of these. The dive theme is free. The name "Daily Dungeon" is taken twice.

## 2. Games built to collect behavioural data

- **The Great Brain Experiment** (University College London, a phone app from 2013). It included a
  gambling task for points. Rutledge's group reports 18,420 players in a study of momentary
  happiness and 25,189 in a study of risk taking by age (Current Biology). This is the nearest
  precedent, a risk task at scale delivered as a phone game by academics. The papers were not read.
- **Its data are public.** A Dryad record, "Risky decision and happiness task: The Great Brain
  Experiment smartphone app" (doi 10.5061/dryad.prr4xgxkk), is described as 47,067 adult
  participants from March 2013 to October 2015. Each player made a sequence of risky choices with
  outcomes shown. **This is a candidate dataset for the present line**, with money-like stakes,
  many people and trial order. The Dryad page (read through a summariser) gives 91,058 completed
  plays, about 2.7 million choices and 1.1 million happiness ratings, in one 88 MB archive of
  Matlab arrays with a README and the authors' script. Read in the owner's browser later the same
  day: the page marks the data public domain (CC0), and the README says each play's 30 trials were
  drawn at random and shown in a random order. So the history a player met was assigned by chance.
  See `../gbe/DESIGN.md`. Nothing was downloaded. If it is taken up, the split into development and held
  out has to be fixed before the archive is opened, as for the other arenas.
- **Sea Hero Quest.** A navigation game used for research on spatial ability, on phones, described
  by its makers as the largest navigation study.
- **Borderlands Science and Project Discovery.** Science tasks placed inside existing commercial
  games (Borderlands 3, EVE Online). Players there do analysis. They are not the subjects.
- **Skill Lab, Neureka.** Named in a 2026 review of such games (arXiv 2604.24321), which says that
  rigorous and ethically sound design is uncommon among them. Not read beyond the summary.
- **The Balloon Analogue Risk Task.** The standard laboratory task of this shape (pump for more,
  lose all if it bursts). The search returned nothing on it. It is named here from memory, and its
  literature has to be read before any claim that our measure is new.

**Reading.** Academic groups have delivered risk tasks as phone games to tens of thousands of
volunteers and published from them. That answers whether it can work. What they did not do, as
far as these searches show, is assign the path to a fixed state.

## 3. Distribution

| Channel | Cost and gate | Fit |
|---|---|---|
| **Web page, installable to the home screen** | No store, no review, one link. Hosting of static files is free or near it. | Best first step. Works on phones and laptops, updates at once, and a link is what a class, a panel or a forum post needs. |
| **Paid panel (Prolific) pointed at the web page** | Pay per participant. | Best for the registered test. One peer-reviewed comparison found Prolific the only platform with high data quality without filters. Prolific published its own account of that study. |
| **Volunteer research sites (LabInTheWild, TestMyBrain)** | Free, by arrangement with the site. Players get feedback on their own results. | Worth asking. Their own authors report good data quality and a wider range of ages and countries than paid panels. Whether they take outside studies was not checked. |
| **itch.io, Reddit and similar** | Free. | Reach among people who like games. No evidence found on data quality from these. |
| **Google Play** | 25 dollars once. A personal account made after November 2023 must run a closed test with 12 testers for 14 days before each new app is published. Organisation accounts are exempt. The 12 testers and 14 days were confirmed on Google's own help page (answer 14151465) on 2026-11-11. The fee and the exemption are from third-party guides. | Possible later. The web page can be wrapped as an app. |
| **Apple App Store** | 99 dollars a year. A waiver exists for accredited educational institutions and nonprofits as legal entities, not for individuals, and only for free apps (Apple's support page, through a summary). | Possible later, and slowest. Apple's guideline 5.1.3 on health research apps requires consent and approval by an independent ethics board. Whether Apple would treat a decision game as such research was not established. |

**Recommendation.** Web first. A single static page that installs to the home screen reaches every
device, needs no store's permission, and is what the correlation study already uses. Stores come
only if the game proves people want it, and then as a wrapper round the same page. A store adds
weeks of review, age rating forms, a privacy label and a second and third copy of every release.

## 4. Getting the data to Atlas

**Not directly.** The correlation study's instrument README already rejects a server on Atlas
because it "would put a home machine on the open internet". That holds more strongly for a public
game. Atlas is also one machine in one house. If it is off or the line is down, plays are lost.

**What to do.**

1. The game is a static page on a host such as GitHub Pages.
2. Each finished run is sent as one small record to a collector that only accepts writes. For a
   panel study the present arrangement (DataPipe into storage the owner controls) is enough. For a
   public game with many players a small hosted endpoint in front of object storage is the usual
   form. Which service is the owner's choice and has a cost that was not priced here.
3. Atlas pulls the new records on a schedule, over an outbound connection, verifies them and
   stores them under `/archive`. Nothing on the internet connects in to Atlas.
4. The held-out split is applied by the puller before any analysis code can read the files, by a
   rule fixed in advance (for example by a keyed digest of the player's random identifier).

**What a record holds.** A random identifier made in the browser, the day's seed, the script
assigned, every choice with its time, and the build version. No name, email, location or device
identifier. That keeps the privacy notice short and the ethics application simple.

**What must not be skipped.** Assignment of scripts has to happen on the server side or be
derived from the identifier by a keyed rule, so a player cannot choose or predict it. A static
page alone cannot keep a key secret, so a public version needs the small endpoint of step 2 to
hand out assignments. A panel version can assign from the panel's participant identifier.

## 5. What this changes in the plan

- Check the Great Brain Experiment data on Dryad before building anything. If it carries each
  person's risky choices in order, it is a ready test of history beyond state in a risk task at
  scale, and it would also give the effect size a pilot is meant to measure.
- Read the Balloon Analogue Risk Task literature on sequential effects.
- Then the simulator, then a prototype page, as in `DESIGN.md`.

## Sources

- https://top.gg/bot/1522949916434104360
- https://www.producthunt.com/products/cruel-dungeon
- https://www.gamingonlinux.com/2024/10/daily-dungeon-gives-you-a-fresh-dungeon-puzzle-every-day-inspired-by-wordle
- https://zer0w0n.itch.io/delve
- https://datadryad.org/dataset/doi:10.5061/dryad.prr4xgxkk
- https://rutledge-lab.squarespace.com/happinessequation
- https://rutledge-lab.squarespace.com/risk-taking-across-lifetime
- https://arxiv.org/pdf/2604.24321
- https://seaheroquest.com/citizen-science
- https://www.doi.org/10.1038/S41587-020-0694-X
- https://prolific.com/blog/data-quality-of-platforms-and-panels-for-online-behavioral-research
- https://wildlab.cs.washington.edu/Project_LabintheWild.html
- https://developer.apple.com/support/fee-waiver
- https://ontest.app/blog/google-play-12-testers-14-days-requirement-explained
- https://conductatlas.com/platform/apple/apple-app-store-review-guidelines/health-and-medical-app-requirements/
