# prereg-d4stability — is the interior chirality stable inside one corpus?

**v2 is the live registration and it ran.** W1, W2 and W3 all PASS: the chirality
is **not** stable, running from `+0.2279` at the smallest stakes to `−0.5003` at
the largest, Cochran's Q `103.0` against a null mean of `9.93`, permutation
`p = 0.0005`, range `0.728` against a bar of `0.565`. The reason is that the
six-term model explains a weighted `R² = 0.361` of a freely estimated kappa
surface. **Read `RESULTS-v2.md`.**

---

## v1 — **VOID**

> **This registration is VOID and none of its numbers may be cited.** The design
> matrix was built as `A − B`, differencing the options in declaration order,
> while the outcome was built as "chose the riskier option". Those disagree
> whenever B is the riskier option, which is 74.8 percent of rows, so the risk
> term was fitted with its sign reversed on most of the corpus. Reorienting
> improves the fit by 2,675 log-likelihood units and **flips the chirality from
> `−0.1775` to `+0.2506`**. See `RESULTS.md` for the full account and the fix.
> `prereg-d4interior-v3` does not share the defect and stands.


**Does the interior chirality `c2` hold still inside one corpus?**

`prereg-d4interior-v3` found that the CPC18 interior chirality of `+0.4438` does
not replicate on choices13k, coming out at `−0.1216`, a sign reversal at a power
of 1.000. That leaves two readings and the record cannot choose between them.
Either the chirality is real and one of those corpora is unrepresentative, or it
is not a stable quantity and moves with whatever stimuli are in hand.

This asks the second question of a single corpus, splitting it into four folds
along outcome scale and comparing the spread of `c2` against random partitions of
the same fold sizes. The search for a third corpus was run first and closed.
`experiments/datasets/DATASET-INVENTORY.md` records it.

**The falsifier points at the cheap answer.** If the spread is no larger than a
random split gives, `c2` is stable, the between-corpus disagreement is a real
corpus-level difference, and the question is not closed. The designed grid in
`../d4design/` then has to be run as a study.

## The corpus, and the three parsers it took to find it

`peterson2021using/exp1.csv` from Psych-101. 13,735 participants, 1,097,375 key
presses, choices13k at the level of the individual choice rather than a rate over
a median of sixteen subjects.

The first parser lost 91 percent of the corpus in silence. The second replaced
silence with accounting and the accounting immediately indicted it, putting 45.8
percent of presses in a bucket named "no declared menu". `peterson_parse.py` is
the third, and its rule is that **every press token lands in a named bucket and
the buckets sum to the corpus total**, asserted in code.

| bucket | presses | share |
|---|---|---|
| `first_press_description` | 96,237 | 8.77% |
| `repeat_press_experience` | 384,948 | 35.08% |
| `ambiguous_unknown_probability` | 210,965 | 19.22% |
| `multi_outcome_out_of_scope` | 405,225 | 36.93% |
| `press_with_no_declared_menu` | **0** | 0.00% |
| `press_key_not_on_menu` | **0** | 0.00% |

What is analysed is 95,748 first-choice description trials over 5,674 strictly
two-outcome problems from 13,735 participants.

## Files

| file | what it is |
|---|---|
| `prereg-d4stability-v1.md` | the registration |
| `prereg-d4stability-v1.sha256` | the seal, component and combined hashes |
| `analysis/peterson_parse.py` | the parser, with the press accounting |
| `analysis/stability_rows.py` | row builder, writes covariates and outcomes to **separate** files |
| `analysis/stability_stat.py` | the spread statistic and its random-split null |
| `analysis/d4stab_fit_v1.py` | the confirmatory fit, the only script that opens the choices |
| `analysis/d4stab_grade_v1.py` | the grader, holds every bar, reads the seal at run time |
| `analysis/launch_fit.sh` | pins the BLAS thread counts and calls the fit |
| `power/power_d4stability_v1.py` | power and size, and `--hash` writes the seal |
| `analysis/peterson_probe*.py` | the audit trail. **`peterson_probe.py` is superseded and its numbers are wrong** |

`analysis/rows_covariates.npz` carries no choice column. The power simulation
loads only that file, so it cannot read the outcome even by accident.
`analysis/rows_outcome.npz` holds the choices.

## Reproducing

Run on Atlas, never on a laptop. The row build downloads Psych-101, about ten
minutes, and both `.npz` files are committed so it can be skipped.

    python analysis/stability_rows.py        # optional, regenerates the .npz
    python power/power_d4stability_v1.py     # power and size, cannot read choices
    python power/power_d4stability_v1.py --hash
    bash analysis/launch_fit.sh 2000         # only after the seal
    python analysis/d4stab_grade_v1.py analysis/results_stability_v1.json

**Thermals.** `N_JOBS = 6` with BLAS pinned to one thread per worker. A first run
at 20 workers with BLAS unpinned took Atlas CPU package 0 to 100 C, its critical
alarm, and was shed. Do not raise it.
