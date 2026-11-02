# Archived papers and tests

Archived 2026-11-02 at the owner's direction.

## Why

These drafts and tests present or test a version of GDT that the programme does not hold.

- The metric is diagonal (`strata/strata_models.py:55, 75, 128`).
- Each option is reduced to one scalar cost before choice.
- The coordinates are chosen by hand: EV and SD, or g, l, π+ and π−.
- Each lottery is reduced to expectations over its outcomes before the metric acts.

The programme's commitments are different:
- a full Mahalanobis metric;
- an evaluation tensor whose contraction is deferred;
- coordinates discovered from data, as the moral-spectrum-analyzer does.

The sealed verdicts here stand as records of the version that was tested. They are not evidence about
those commitments.

## What is here

| Item | What it was |
|---|---|
| `README-papers-index.md` | The former index of `experiments/papers`, which stated the earlier central claim |
| `paper_flagship_gdt.md` and `.docx`, `paper_00_theory.md` to `paper_04_stratified_kappa.md` | Drafts of the flagship and its pillar papers |
| `COMPANION-PLAN.md` | The plan pairing Part II with the theory paper |
| `tcss-part2/` | Part II manuscripts, their README and the 2026-10-30 corrections record |
| `theory/` | Theory paper draft and `STATEMENTS.md` |
| `psych101/` | `prereg-psych101-v1`, Part II's frozen models on Wulff 2018, run 2026-10-30 |
| `strata/` | `prereg-strata-v1`, the stratified and consumer variants on five corpora, run 2026-10-30 |
| `strata2/` | Exploration of probability readers and norm exponents on the same corpora |
| `completeness/` | Completeness and restrictiveness, partial stake and diameter scaling inside CPT, the confidence runs, and the power simulations for a proposed range study |

## What still works

- **Code.** Every folder sits at the same depth as before, so relative paths such as
  `../../datasets` and `../strata` still resolve, and the code runs from here.
- **Seals.** Signed tags and seal files are unchanged. A seal is checked at its tag.
- **Records left in place.** Three files stayed in `experiments/papers/tcss-part2/`.
  - `codebook-v1.md`, because `prereg-learned-v1` reads it at that path.
  - `prereg-dimensions-v1` and `power/`, which are registration records, not drafts.
