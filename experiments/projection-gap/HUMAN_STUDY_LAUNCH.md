# Human projection-gap study — launch plan (what's ready, what needs you)

The LLM panel is a **model organism**; humans are the confirmatory gate for Pillar 2 of Geometric
Decision Theory. Everything an AI agent can prepare is done; the remaining gates are institutional,
ethical, and financial — they must be yours.

## What is READY (built + verified)

- **Instrument:** the gamified "Dear Ethicist" web app (`human_pilot/index.html` + `pilot.js` +
  `letters.json`) — 13 letters (7 real, 2 placebo, 4 dose), between-subjects (one pole per contrast),
  attention check, incentive framing, random-lottery bonus. LLM-dry-run validated (16,848 responses).
- **Pre-registration: FROZEN** — `prereg-v2.lock.json`, combined sha256 **ca84eb4c…** (lock file hash
  533f8962). The sign predictions are locked *before* any human data:
  A1.1/A1.2/A2.1/A3.1/B1.1/B2.1 = **+1**, B1L.1 = **−1**; placebos null; dose **monotone** (v2's
  fixed-temperature redesign). This is AsPredicted/OSF-ready text.
- **Analysis pipeline:** `analyze_human.py` — between-subjects two-proportion z per contrast, BH-FDR
  across the 7, sign-match to prereg-v2, placebo correction, cross-domain, dose monotonicity, pre-
  registered attention-check exclusion. Runs from `human_pilot/` (`python analyze_human.py --data
  pilot.jsonl`).

## Power analysis (from the LLM dry-run effect sizes)

Between-subjects; each subject sees one pole per contrast → N subjects ≈ 2 × (n per pole). Powered at
80%, Bonferroni α=0.05/7 across the 7 real contrasts:

| target | n/pole | **N subjects** | approx cost (Prolific) |
|---|--:|--:|--:|
| 4 strongest real contrasts | 175 | **350** | ~$1,300–1,800 |
| 5 strongest (matches the LLM's 5/7) | 561 | **~1,120** | ~$4,300–5,700 |
| all 7 | 3,177 | ~6,400 | impractical |

**Recommended launch: N ≈ 400–500** (powers the 4 strongest robustly; ~$1,500–2,500 at ~$1.5–2 ×
1.33 Prolific fee for an ~8–10 min task). Two contrasts (A2.1 identity, B2.1 societal) are **near-null
in the LLMs** (gaps +0.04 / −0.05) — they may not reach significance, exactly as in the LLM 5/7. **Do
not** power for all 7; power for the 4–5 and report the rest honestly.

## The GATES that require YOU (an AI agent cannot do these)

1. **IRB / ethics approval** — human-subjects research needs your institution's IRB (or an exempt
   determination for anonymous, minimal-risk economic-choice vignettes). This is the hard gate.
2. **Public pre-registration** — post the frozen `prereg-v2` predictions + `analyze_human.py` plan to
   **OSF or AsPredicted** *before* collecting data. (The hash is already frozen locally; you just
   publish it.)
3. **Recruitment platform + funding** — a **Prolific** (recommended) or MTurk account with ~$2,000
   loaded; host the web app (any static host — GitHub Pages / Netlify) writing responses to a backend
   (the pilot already targets a Google Sheets / JSONL sink).
4. **Consent + debrief** — a consent page (minimal-risk, anonymous, right-to-withdraw) and a debrief;
   templates are standard and IRB will want to see them.

## Go-live checklist (in order)

1. IRB submission (or exemption) — the long pole; start here.
2. Comprehension pilot **N≈50** (already flagged in the protocol) — confirms the letters read clearly
   and the attention check works, before the powered run.
3. Publish `prereg-v2` + analysis plan to OSF/AsPredicted; record the timestamp/URL.
4. Deploy the web app + backend; smoke-test end-to-end (one self-response → lands in the sink →
   `analyze_human.py` parses it).
5. Launch on Prolific, N≈500, balanced pole assignment, attention-check screening.
6. Run `analyze_human.py --data <collected>.jsonl` → the pre-registered verdict.

## Honest caveats

- **Human effect sizes are unknown.** The LLM dry-run is the only prior; humans may be **stronger**
  (the LLM magnitudes were ~5× under the model's, so the study could be cheaper) or weaker. The
  comprehension pilot + a sequential look would refine N.
- **B2.1 was slightly *negative* in the LLMs** — a potential falsifier to watch; the pre-registration
  scores it honestly either way.
- This confirms Pillar 2 in **humans**; it does not by itself make the broader theory "proven" — that
  needs the human result *plus* replication and a novel confirmed prediction.

*Status: launch-ready. Blocking gates are IRB + platform + funding — yours. I can draft the OSF/AsPredicted
text, the consent/debrief pages, and the deployment scripts on request.*
