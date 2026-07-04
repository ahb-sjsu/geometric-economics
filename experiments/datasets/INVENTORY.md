# Dataset inventory — validating the geometric decision theory

Two validation jobs: **A** = fit-and-transfer the shared metric (individual-level, cross-domain,
out-of-sample — the reviewer's demand); **B** = projection-gap (a non-monetary coordinate varied at
fixed money/lottery). Reachability below is **probed by `fetch.py`, not asserted**.

## Reachability (probed 2026-07-04)

| id | validates | access | conf | reachable | notes |
|---|:--:|---|:--:|:--:|---|
| **cpc18** — Choice Prediction Competition 2018 | A | **open (CC-BY)** | high | **yes** | **CONFIRMED**: Zenodo [10.5281/zenodo.2571510](https://zenodo.org/records/2571510), `all CPC18 raw data.csv` (65 MB, 694,500 individual choices), train/test split. Fetch via the TCSS Zenodo downloader. |
| **choices13k** — large-scale risky choice | A | open | high | yes | Peterson et al. (Science 2021), ~13k problems, [github.com/jcpeterson/choices13k](https://github.com/jcpeterson/choices13k). Second lottery-leg benchmark. |
| **gps** — Global Preferences Survey | A | registration | high | login-gated | best cross-domain same-subject data; needs manual registration |
| **bruhin2010** — Risk and Rationality | A | supplement | med | yes | per-subject CPT params; common-protocol competitor |
| **manylabs2** — Many Labs 2 | A/B | open (OSF) | med | yes | individual framing manipulations at scale |
| **ruggeri2020** — KT 19-country replication | A | open (OSF) | med | yes | already a TCSS target; re-analyze individual-level |
| **moralmachine** — Moral Machine | B | open (large) | med | yes | d6/d7 at massive scale |
| **socialchem** — Social-Chemistry-101 | B | open | high | yes | already used (CHSH seeding); d6/d8 |
| **ethics** — ETHICS | B | open | high | yes | d7 encoding source |
| **halevy2007** — Ambiguity (Ellsberg) | B | supplement | low | yes (landing) | existing human d9 projection-gap |

> A `reachable=yes` with an HTML content-type is usually a **landing/registration page**, not the
> data file — real availability is confirmed per dataset, not from the HTTP status alone.

## Priorities

1. **CPC18** (job A, risky-choice benchmark) — **open, CC-BY, confirmed, 694,500 individual choices
   with a train/test split**, directly fetchable via the TCSS Zenodo downloader. This is the fastest
   path to turning the TCSS paper from "16 aggregate targets" into "held-out individual prediction
   under a common likelihood" — the single biggest credibility jump. **Start here.** (choices13k is a
   second open lottery-leg benchmark.) **GPS** adds the cross-domain same-subject dimension but needs
   manual registration.
2. **halevy2007 / ambiguity** and any **framing-of-games** data — existing **human projection-gaps**
   (d9, d7/d8) that pre-validate the LLM result on real people. See `../historical-ledger/`.
3. **socialchem / ethics / moralmachine** — open now, for **encoding** the non-monetary coordinates
   and rater-auditing them (addresses the encoding-dependence critique).

## Usage

```bash
python fetch.py                          # probe all URLs, honest reachability report
python fetch.py --download ethics socialchem   # git-clone / download the open ones
```

`fetch.py` only reports what it can actually reach; registration-gated sources surface as a
login/redirect, which is the truth. Manual-access datasets (GPS, CPC, journal supplements) are flagged
`registration` / `verify` / `supplement` and need a human step.
