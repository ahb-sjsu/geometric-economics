# Dataset inventory — validating the geometric decision theory

Two validation jobs: **A** = fit-and-transfer the shared metric (individual-level, cross-domain,
out-of-sample — the reviewer's demand); **B** = projection-gap (a non-monetary coordinate varied at
fixed money/lottery). Reachability below is **probed by `fetch.py`, not asserted**.

## Reachability (probed 2026-07-04)

| id | validates | access | conf | reachable | notes |
|---|:--:|---|:--:|:--:|---|
| **gps** — Global Preferences Survey | A | registration | high | login-gated | best cross-domain same-subject data; needs manual registration |
| **cpc18** — Choice Prediction Competition | A | verify | low | 404 on guessed repo | gold-standard risky-choice benchmark; data repo needs manual confirmation |
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

1. **GPS** (job A, cross-domain same-subject) and **CPC** (job A, risky-choice benchmark) — the two
   that turn the TCSS paper from "16 aggregate targets" into "held-out individual prediction under a
   common likelihood." Both need a manual access step (GPS registration; CPC repo confirmation).
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
