# Dear Ethicist — projection-gap human pilot

A self-contained, deployable web pilot for the human projection-gap study
(`../HUMAN_STUDY_PROTOCOL.md`), styled on the Dear Ethicist advice-column game but standalone (it does
not touch the deployed game). It presents economic-decision letters whose **monetary payoffs are
identical across the two poles** and only a non-monetary coordinate (social impact / identity /
epistemic status) changes — so every scalar theory is forced to predict equal choice rates and the
frozen metric (`prereg-v2`) predicts a signed gap.

## Files

| File | Role |
|---|---|
| `letters.json` | the stimulus set — 7 real contrasts, 2 placebos, 4 dose levels, 32 encoding-invariance reframings, 1 attention check; aligned to `prereg-v2` contrast ids |
| `index.html` + `pilot.js` | the web app: consent → demographics → **between-subjects** randomized letters (one pole/contrast) → attention check → JSONL export (+ optional Sheets POST) |
| `analyze_human.py` | between-subjects analysis (Δ = P(A\|hi) − P(A\|lo), two-proportion z, BH-FDR, placebo correction, cross-domain, dose monotonicity); simulation self-test |

## Run it

```bash
# locally
python -m http.server 8000        # then open http://localhost:8000/
# analysis (simulated pilot)
python analyze_human.py            # self-test
python analyze_human.py --data pilot.jsonl   # real data (concatenated JSONL records)
```

Deploy: drop the folder on GitHub Pages (as the existing Dear Ethicist game is). To log to a sheet,
set `CONFIG.SHEETS_ENDPOINT` in `pilot.js` to a Google Apps Script Web-App URL (see
`erisml-lib/.../dear-ethicist-sheets-setup.md`); otherwise each subject downloads their JSONL.

## Design (as pre-registered)

- **Between-subjects on the pole**: each subject sees one pole per contrast → no within-pair demand.
  Δ is a group difference. Randomized order; attention check; coarse demographics only.
- **Data schema** matches the panel's: rows `{subject, contrast, pole, kind, domain, coord, sign_pred,
  choice, rt}` → `analyze_human.py` reads them directly, and they map to `analyze.py`'s fields.
- **Predictions** are `prereg-v2` (frozen, hashed) — sign is primary; monotone dose is the sharp
  secondary; placebos null is the falsifier.

## Before the confirmatory run (not yet wired — pre-registration gates these)

1. **Real-money incentive hook** — random-decision selection + Prolific bonus (the protocol requires
   incentivized choice for the economics claim). Currently the pilot is choice-only.
2. **More encoding-invariance reframings** per coordinate (≥3 each; some contrasts have 1 lo-pole
   variant — add matched ones), and log the reframing index so sign-stability can be tested per Thm 5.
3. **Add the identity (d7) coordinate** to the Dear Ethicist DEME dimension set if merging into the
   deployed game.
4. **OSF / AsPredicted registration** + the repo `sha256` analysis-plan lock, before collecting a
   single confirmatory datum. Run the ~N=50 pilot first (comprehension, attention-pass, RT, direction)
   — pilot data must **not** touch the predictions.

*Validated: `analyze_human.py` recovers a planted between-subjects effect (H1=1.00, cross-domain) and
is null under no effect (H1=0.14). The stimulus set and analysis are runnable now; the incentive hook
and registration are the remaining gates to a real run.*
