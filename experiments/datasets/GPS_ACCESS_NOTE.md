# GPS data access — status, diagnosis, and request email

Status of the Move-2 confirmation (`prereg-coupling-v1`): **blocked on data access.** The scorer
(`gps_coupling.py`) is built and ready; it runs the moment the GPS `.dta` files are in place under
`raw_gps/`. What follows is the access trail so this isn't re-diagnosed later.

## What we have vs. need

- **Have:** the Harvard Dataverse replication package (doi:10.7910/DVN/HH8DV4) — but it ships **only the
  Stata do-files**, not the data. The do-files confirm the variable names
  (`patience risktaking posrecip negrecip altruism trust`, plus `country`/`isocode`) and that
  `Country.dta` / `Individual.dta` live in a `Data/` folder.
- **Need:** `Country.dta` (76 rows — enough for the country-level proxy test) and/or `Individual.dta`
  (~80k rows — the fuller test). These are copyright-gated and are **not** redistributed by any mirror
  (the community repo github.com/scerioli/Global-Preferences-Survey explicitly excludes them).

## The blocker (diagnosed 2026-07-05)

The sole legitimate source is down at the TLS layer:

- `https://gps.iza.org/downloads` → 302 redirect to `https://gps.econ.uni-bonn.de/`.
- `https://gps.econ.uni-bonn.de/` → TLS handshake fails: the server accepts the TCP connection then
  closes it without returning a certificate. `openssl s_client` = "unexpected eof while reading,"
  0 bytes read; browsers show `PR_END_OF_FILE_ERROR`. Reproduces from multiple networks → server-side.
- `https://www.briq-institute.org/...` → certificate **expired** (briq merged into IZA, Jan 2024).

Nothing client-side fixes this; the data host is offline/misconfigured. Retry later, or email a contact.

## Contact (important)

- `briq@iza.org` **bounces** for external senders — it is an internal distribution group
  (`550 5.7.133 SenderNotAuthenticatedForGroup`). Do **not** use it.
- Correct contact (GPS contact page, gps.econ.uni-bonn.de/contact):
  **Prof. Dr. Armin Falk — armin.falk@uni-bonn.de**. Optional cc: **thomas.dohmen@uni-bonn.de**
  (co-runs the GPS at Bonn). Fallback if no reply in ~1 week: **enke@fas.harvard.edu** (Benjamin Enke).
- Send from a **university address** (andrew.bond@sjsu.edu) — DMARC passes and it reads as legitimate.

## Draft email (ready to send)

> **To:** armin.falk@uni-bonn.de   **Cc:** thomas.dohmen@uni-bonn.de
> **Subject:** GPS data request — download site (gps.econ.uni-bonn.de) currently failing TLS handshake
>
> Dear Prof. Falk,
>
> I am writing to request access to the Global Preferences Survey dataset (Falk, Becker, Dohmen, Enke,
> Huffman & Sunde, 2018), and to report an apparent outage on the download site.
>
> I first tried the group address listed after the briq–IZA merger (briq@iza.org), but it rejects
> external senders, so I am contacting you directly as the GPS contact listed at
> gps.econ.uni-bonn.de.
>
> The downloads page is currently unreachable for me: https://gps.iza.org/downloads redirects to
> https://gps.econ.uni-bonn.de/, which then fails during the TLS handshake — the server accepts the
> connection but closes it without returning a certificate (browser error PR_END_OF_FILE_ERROR;
> openssl s_client reports "unexpected eof while reading," 0 bytes read). It reproduces from more than
> one network, so it appears to be server-side rather than local. Because the site is down I cannot
> complete the standard data-request form.
>
> Could you either let me know when the site is expected to be back, or advise on an alternative way to
> obtain the country-level and individual-level .dta files? I already have the replication do-files
> from the Harvard Dataverse (doi:10.7910/DVN/HH8DV4); only the data files themselves are missing.
>
> Intended use: an academic, non-commercial study on whether risk and social preference measures share
> low-dimensional latent structure. I will cite Falk et al. (2018, QJE) and Falk et al. (2016) as
> required and will not redistribute the data.
>
> Affiliation: Andrew H. Bond, Department of Computer Engineering, San José State University
> (andrew.bond@sjsu.edu).
>
> Thank you very much for maintaining this resource, and for any guidance you can offer.
>
> Best regards,
> Andrew H. Bond

## When the data arrives

Unzip anywhere under `experiments/datasets/raw_gps/` (any `.dta` with the six preference columns is
found automatically) and run:

    python gps_coupling.py

It reports the 6×6 Spearman matrix, tests **P1** (risk↔social sign) and **P2** (rank-1 vs rank-2),
and scores them against the frozen hash — honestly, whichever way it comes out. Note Falk et al.'s own
two-bundle finding (risk+patience; altruism+posrecip+trust) makes a P1/P2 **falsification** a live
outcome; that is still a real, reportable result (and would push the structure toward the rank-2 the
Ruggeri leg already favored).
