# Part II manuscript: registered tests of the diagonal model

Drafted 2026-11-09. `part2_registered_tests.tex`, IEEEtran journal class, 9 pages, target IEEE TCSS
(about 10 pages plus at most 2 overlength). **Draft. Not reviewed by the owner, not submitted.**

It replaces the archived draft `../../../papers-archive/tcss-part2/part2_manuscript_revised.tex`. The
archived draft led with the results that held and stopped at CPC18. This one reports every set of
predictions and its outcome (Table I), and adds the three registrations run after the archived draft
was written.

## What changed against the archived draft

| Change | Source |
|---|---|
| Title and framing: the model tested is named the diagonal model, and its three simplifications are stated in the introduction | `../../../papers-archive/README.md` |
| New Section IV.B: `prereg-psych101-v1` (Wulff et al. corpus) | `../../../papers-archive/psych101/results/grade_real.json` |
| New Sections IV.C and IV.D, Table III, Fig. 1: `prereg-strata-v1` (five corpora) | `../../../papers-archive/strata/results/graded_strata_real.json` |
| New paragraph on `prereg-menus-v1` | `../../menus/results/graded_menus_real.json` |
| Table I: every record, how it was frozen, what held, what failed | the records above, `../../boundary/RESULTS.md`, the archived `CORRECTIONS-2026-10-30.md` |
| Caveat on the CPC18 CPT (weights misplaced on losses and mixed problems) placed beside Table II | `prereg-strata-v1.md`, Section 4 |
| The two CPC18 tables merged into one | archived draft |
| The transfer section shortened, and its 97 to 100 percent result tied to the psych101 finding that the shape transfers at 99 percent while the model fails to beat expected value | `grade_real.json`, `transfer_efficiency` |
| The citation of the theory paper removed (that draft is archived). The two facts it supplied are stated without it or dropped | archived draft, Section V.A |
| Section "Related Findings in the Social-Preference Literature" deleted. It reported no test of the model | Claude's choice |
| Discussion rewritten: what holds, what the diagonal model gets wrong, what the tests did not reach, with `prereg-learned-v1` and `prereg-correlation-v1` named | `../../learned/RESULTS.md`, `../../correlation/DESIGN.md` |

Numbers in Sections III, V and VI and in the panel table are carried from the archived draft, whose
corrections record says each was re-derived on 2026-10-30. They were not re-derived again on
2026-11-09. Numbers in Section IV.B to IV.D and the menus paragraph were checked on 2026-11-09 against
the graded JSON files named above.

## Choices made in drafting (Claude's, the owner may change any)

1. The paper is framed as a record of tests with more failures than passes. The abstract says so.
2. The exploratory work on the spent corpora (probability readers, completeness, range-scaled CPT) is
   left out. It is not confirmatory and would lengthen the paper.
3. The statement that the failures belong to the diagonal specification appears three times (abstract,
   introduction, discussion) and is paired each time with the statement that the fuller proposal is
   untested, not supported.
4. Part III is cited as a registration with a public record, with one sentence of result.

## Open before submission

- Owner review of the framing and of choice 2.
- References marked `% verify` in the source: Part I volume and pages, Andersen, Slonim and Roth,
  Cameron, Falk, and the ten added on 2026-11-09 (Wulff, Binz, Glöckner and Pachur, three Pachur and
  Zilker papers, Babula, Molter, Cao and Tsetsos). The Babula entry has only a DOI.
- Confirm that OSF `osf.io/ead4x` is public.
- Author e-mail and affiliation line are carried from the archived draft.
- The six effects counted in Section IV.D are not named in the text.
- A Word copy has not been built.

## Build

```
cd build && python fig_risky.py && cd ..
pdflatex part2_registered_tests.tex && pdflatex part2_registered_tests.tex
python build/check_prose.py part2_registered_tests.tex
```

`fig_risky.py` reads the two graded JSON files and fits nothing. `check_prose.py` reports colons,
semicolons and em-dashes in prose, control characters, and the abstract's length. On 2026-11-09 it
reported two table rows (the semicolon is LaTeX spacing) and no control characters.
