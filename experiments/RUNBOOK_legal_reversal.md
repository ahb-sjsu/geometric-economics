# RUNBOOK — geometric pathology → appellate reversal (executable construction)

The experiment for [[prereg-legal-reversal-v1]], ordered so the **freeze precedes any
outcome-label analysis** ([[FREEZE_PROTOCOL]]). Each stage lists the real effort and the current
blocker, from the 2026-07 CourtListener reconnaissance. This is the *construction*; the confirmatory
run is gated on the starred items.

## Stage 0 — reconnaissance (DONE)
- CourtListener v4: detail/text endpoints need a **free API token** (401 unauth); open search = metadata
  + citation graph only. Full text via token or **free bulk download**.
- `posture`/`procedural_history`/`syllabus` are **~0% populated** → **no structured disposition/grounds
  field.** Label + grounds are text-derived. (docketNumber 100%, citation 80%, judge 80%.)
- Consequence: the reversal-grounds label is a **constructed NLP+graph artifact**, not a lookup.

## Stage 1 — finalize scope + FREEZE  ★ (gates everything below)
1. Fill every `TODO_` in `legal_reversal_scope.json`: court set (prefer random panel assignment for the
   IV), year cuts `t0<t1`, `S` weights, min test n; pin the ErisML extractor version.
2. Run [[FREEZE_PROTOCOL]]: `sha256sum` sidecar → signed tag `prereg-legal-reversal-v1` → `ots stamp`
   → push. **No outcome-label work before this tag exists.**

## Stage 2 — corpus (open, reproducible)  ★ needs free CL token / bulk
`cl_fetch.py` (to write): pull full opinions for the fixed court/window from CL bulk (or token API),
redact per `label.leakage_redaction`. Store text + citation edges + docket + panel. **Effort: moderate;
blocker: token/bulk download (~GBs).**

## Stage 3 — construct the label (the hard part)  ★ NLP+graph project
`build_labels.py` (to write), per `label.construction_pipeline`:
link each decision to its reviewing appellate opinion (citation graph + `sibling_ids` + docket) → NLP-
parse that opinion's holding for reverse/vacate vs affirm → extract the ground → map to a deontic gate.
**Then Westlaw KeyCite-validate ≥300 sampled labels (manual); require ≥90% agreement or re-freeze v2.**
**Effort: large; this stage has its own measurable error and is not optional.**

## Stage 4 — features  ★ needs ErisML LLM extraction at scale
`compile_features.py` (to write): run the **ErisML compiler** (pinned version) on each redacted opinion
→ `MoralTensorV3` (GDT coordinates) + deontic gates + Gini/worst-off. Fit the rank-`k` manifold on the
**train split only**; compute `S` = off-manifold residual + curvature + gate-failures.
**Effort: large + compute; blocker: LLM-extraction backend (API keys/GPU). The mock extractor produces
fake geometry and MUST NOT be used for the result.** Report inter-extractor stability on a sample.

## Stage 5 — analysis (frozen thresholds)
`analyze.py` (to write): temporal split; evaluate the five confirmatory rows **once** on the sealed test
years; Priest–Klein selection control (random-assignment IV or Heckman two-stage); legal-BERT baseline
for H2; Holm correction. Emit the scorecard against the frozen thresholds.

## Stage 6 — interpret (committed)
`H1∧H2∧H3` → Tier A. `H1, ¬H2` → Tier B (reported as re-description). `¬H1` → graveyard. `¬P0` → void.
Primary target = gate-aligned reversals; all-grounds = secondary.

---

## Honest status (why the confirmatory run is not "just run now")

The confirmatory result cannot be produced in a single session without either **violating the
pre-registration** (Stage 1 must precede Stages 3–5) or **fabricating** (skipping the token corpus, the
label-construction project, or the scale LLM compile). None of those is acceptable. The rigorous path is
the ordered runbook above: **finalize + freeze first**, then execute Stages 2–5 as the real, multi-week
project they are. What is genuinely done and real: the design, the substrate (ErisML = GDT encoder), the
gate-aligned mechanism, the pre-committed gate, the freeze discipline, and the reconnaissance that sizes
every remaining stage. The decisive unknown remains **H2** — whether the moral-tensor geometry beats
legal-BERT — and it is set exactly where the difficulty belongs.
