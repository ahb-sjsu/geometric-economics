# Pre-registration: geometric pathology predicts appellate reversal (`prereg-legal-reversal-v1`)

*Frozen before any modeling on the outcome-linked corpus. The legal leg of the Geometric Decision
Theory (GDT) program; cross-references the `geometric-law` book (Ch. 10, "Legal Failures as Geometric
Pathologies"). This is a deliberate **Tier-A attempt**: a prediction that is novel, uses a non-circular
ground-truth label (later reversal), is uniquely geometric (must beat a strong flat-text baseline), and
is about real human high-stakes decisions.*

*Companion frozen predictions: [[prereg-sigma-v1]] (low-rank Σ), [[prereg-coupling-v1]] (cross-domain
angle coupling). Same freeze discipline: sha256 below; no line changes without breaking the hash.*

---

## 0. Why this is the Tier-A candidate (and the honest gate)

The GDT program's held-out results to date largely **re-describe** known regularities (Tier B). A
Tier-A result requires a prediction that is (i) novel, (ii) large, (iii) uniquely geometric — a scalar
/ flat-feature model cannot produce it — and (iv) confirmed on human behavior. Appellate **reversal**
supplies the rare non-circular ground-truth label GDT's "failure = geometric pathology" thesis needs.

**The gate, pre-committed:** the study is a Tier-A success **only if H1 AND H2 AND H3 all pass**
(reversal is predicted, the geometric score beats the flat-text baseline, and reversal has the
predicted geometric *structure*). If H1 passes but H2 fails (geometry merely matches BERT), we will
report the result as **Tier B (re-description), not Tier A** — stated now, so it cannot be reframed
post hoc.

## 1. Core hypothesis

> Original judicial opinions whose compiled geometry is **pathological** — far from the low-rank
> decision manifold, high local curvature — are **reversed on appeal at a higher rate** than
> geometrically central opinions, and this geometric signal predicts reversal **beyond** what a strong
> flat-text legal-language baseline predicts.

## 2. Unit, population, corpus

- **Unit of analysis:** a single first-instance or intermediate-appellate decision that was
  subsequently subject to appellate review.
- **Corpus (open, reproducible — required):** Caselaw Access Project (Harvard LIL, ~7M cases, open as
  of 2024) and/or CourtListener / Free Law Project bulk data (citation network + disposition metadata).
  **No bulk extraction from Westlaw** (subscriber ToS; *Thomson Reuters v. ROSS*, D. Del. 2025). Westlaw
  is used **only** to (a) validate labels via KeyCite on a random sample (individual, manual queries)
  and (b) reference the Key Number taxonomy for coordinate design — never as the training corpus.
- **Jurisdiction/window (pre-committed to avoid cherry-picking):** one jurisdiction with high appellate
  coverage and machine-readable disposition (primary: U.S. federal courts of appeals reviewing district
  decisions; the exact court set and year range are fixed in `legal_reversal_scope.json`, committed with
  this file, before label linkage).

## 3. Label: reversal (non-circular, external)

- **y = 1** if the decision received **negative appellate treatment reversing/vacating** it in its
  direct history; **y = 0** if **affirmed**. Derived from the open citation/disposition graph (a later
  appellate case in the direct line disposing "reversed"/"vacated" vs "affirmed").
- **Label validation:** on a random n≥300 sample, the open-derived label is checked against **Westlaw
  KeyCite** (manual). Pre-committed acceptance: ≥90% agreement; below that, the labeling protocol is
  revised and re-frozen as v2 before any modeling.
- **Leakage control (mandatory):** strip editorially-added treatment flags / headnotes / synopsis and
  any later-appended history from the case text before compilation (CAP/Westlaw sometimes prepend red-
  flag markers). The model sees only the court's own opinion text. Reversal itself is inherently
  external (the opinion cannot contain its own future reversal), which is the label's virtue.

## 4. The geometric quantity (pre-committed operationalization)

Each opinion is compiled to a **dense moral tensor** `T_case` by the **ErisML compiler**
(`MoralTensorV3`, rank-2 `(k,n)` = moral-dimension × stakeholder, plus four Kantian deontic gates and
Gini/worst-off aggregates). Crucially, the `k` axis is the set of moral dimensions
(`rights_respect, fairness_equity, autonomy_consent, privacy_protection, legitimacy_trust,
epistemic_quality, virtue_care, …`) — **essentially the GDT decision-manifold coordinates**, so the
compiler acts as a concrete GDT encoder and the pathology score lives in the same space as the rest of
the program. (The visual `aesthetics-compiler` is the wrong tool and is not used.) On the **training
split only**:

1. Fit a rank-`k` low-rank model (Tucker/PCA) to the training-case tensors; `k` chosen by a
   pre-committed elbow rule (first `k` where marginal explained variance < 1%), fixed before test use.
2. **Pathology score** `S(case)` = a fixed convex combination (weights frozen in the scope file) of:
   - **off-manifold residual**: `‖T_case − Π_k T_case‖` (reconstruction error under the rank-`k` fit);
   - **local curvature / geodesic deviation** as defined in *Geometric Methods* (Bond 2026a);
   - **number of failed deontic gates** (universalizability, mere_means, valid_consent,
     legitimate_authority) — categorical normative pathology.
`S` is computed identically on train/val/test; test cases are never used to fit the manifold.

**Label alignment (primary target).** The compiler encodes *moral* structure; reversal tracks *legal*
error, and the two align on rights/procedure grounds but not on precedential/statutory ones. The
**primary** label is therefore reversal on **gate-aligned grounds** (jurisdiction/standing →
legitimate_authority; due process/waiver → valid_consent; equal protection → universalizability;
dignity → mere_means); **all-grounds** reversal is a secondary target, expected weaker. This is
pre-committed so a hit on gate-aligned reversal with a null on all-grounds is the *anticipated* honest
shape, not a post-hoc rescue.

## 5. Hypotheses, thresholds, falsifiers (all pre-committed)

| ID | Claim | Pass threshold | Falsifier |
|---|---|---|---|
| **H1** | `S` predicts reversal | odds ratio per SD of `S` ≥ 1.25, `p<0.001`, after §6 selection control | OR ≤ 1.10 or n.s. |
| **H2** | uniquely geometric | adding `S` to a strong flat-text baseline (legal-BERT on the same redacted text) improves held-out AUC by **ΔAUC ≥ 0.02** and nested LRT `p<0.001` | ΔAUC < 0.01 → **declare Tier B** |
| **H3** | predicted structure | reversal rate is **non-uniform** in the geometry: monotone increasing in off-manifold residual **and** elevated near pre-labeled regime boundaries, not flat interior (pre-committed bins) | no monotone structure / uniform |
| **H4** | low-rank (Pillar 1 in law) | case-ensemble tensor is effectively low-rank: `k*` (elbow) ≤ 8 and rank-`k*` explains ≥ 70% variance | needs near-full rank |
| **P0** | placebo / internal null | `S` does **not** predict a geometrically-irrelevant label (filing quarter; opinion length decile) | `S` predicts placebo → pipeline artifact, whole study voided |

## 6. Appeal-selection model (Priest–Klein — the make-or-break control)

Reversal is observed only for **appealed** cases, and appeal is endogenous (Priest–Klein selection). We
pre-commit to controlling it, in order of preference:

1. **Instrument via random trial-judge assignment** where the court uses random assignment: judge
   identity instruments decision "quality"/appeal propensity (examiner-design logic; Bhuller et al.).
2. If (1) is infeasible for the fixed court set, a **two-stage / Heckman selection model**: stage 1
   models `P(appeal)`, stage 2 models `P(reverse | appeal)` with the inverse-Mills correction; `S`
   enters stage 2.
3. **Sensitivity bound:** report H1/H2 under both raw and selection-corrected models; the headline claim
   uses the selection-corrected estimate. If the sign/threshold flips between them, H1 is **not**
   considered confirmed.

## 7. Analysis plan

- **Split:** temporal — train on years `< t0`, validate `[t0,t1)`, **test on future years `≥ t1`**
  (predict future reversals; fixed cut in scope file). No case appears in two splits.
- **Primary metric:** held-out AUC and calibration for reversal; §5 thresholds evaluated on the test
  split **once**.
- **Baselines:** (a) base rate; (b) length + court + year logistic; (c) **legal-BERT on redacted text**
  (the flat-feature competitor H2 must beat).
- **Multiplicity:** the five rows of §5 are the only confirmatory tests; Holm correction across them.
  Anything else is exploratory and labeled as such.
- **Power:** with reversal base rate ~10–20% and n ≥ 20,000 test decisions, OR = 1.25/SD is detectable
  at power > 0.9; the scope file fixes the minimum n and the study does not proceed to confirmatory
  testing below it.

## 8. What each outcome means (committed interpretation)

- **H1+H2+H3 pass:** Tier-A result — a novel, uniquely-geometric, human-confirmed prediction: the
  geometry of a decision predicts, and structurally explains, its own reversal, beyond flat text.
- **H1 passes, H2 fails:** Tier B — reversal is predictable but geometry adds nothing over language
  models; reported as re-description, not a win for GDT's distinctive content.
- **H1 fails:** the failure-as-pathology thesis is falsified in law; reported as a negative result
  (into the graveyard, [[EVIDENCE]]).
- **P0 fails:** pipeline artifact; the study is void and re-designed.

## 9. Honest limitations (stated before data)

- One jurisdiction/window; a positive result is not universal (cross-court replication is future work).
- **Moral ≠ legal.** The compiler encodes normative/moral structure (GDT coordinates), not the full
  legal apparatus (precedent, statutory interpretation, procedure). Reversals from purely legal-technical
  error are invisible to it — hence the gate-aligned primary target. A null on all-grounds reversal with
  a hit on gate-aligned reversal is the *expected* honest shape, not a failure.
- **Extractor dependence.** The MoralGraph is LLM/SRL-extracted, so the geometry partly reflects the
  extractor's reading. Mitigation: the extractor + version is part of the frozen pipeline, and
  inter-extractor stability is reported on a sample.
- Reversal conflates legal error, changed law, new evidence, discretionary reversal — a noisy proxy for
  "wrong decision."
- The compiler's only prior human benchmark (aesthetics) gave small effects (`r≈0.05`); the geometric
  signal here may likewise be small, which H1's OR threshold is set to respect.
- Westlaw is validation-only; the corpus must remain open for reproducibility and legal cleanliness.

## 10. Freeze

Committed artifacts frozen together: this file **and** `legal_reversal_scope.json` (court set, year
cuts, tensor axis semantics, `S` weights, bins, minimum n). Record the hash and tag before label
linkage or any modeling:

    sha256sum PREREG_legal_reversal.md legal_reversal_scope.json   # tag: prereg-legal-reversal-v1

No line above may change without breaking the hash.
