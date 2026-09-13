# Machine-checked results

## `ScalarIrrecoverability.lean` — Theorem 4

`nobel-program.md` calls Theorem 4 "the one with teeth" and the only conditionally
load-bearing result in the package. It is now machine checked.

| | |
|---|---|
| Checked | 2026-09-12, on Atlas |
| Toolchain | Lean 4.33.1 with the mathlib in `~/dmo-lean/.lake/packages` |
| Command | `lake env lean ScalarIrrecoverability.lean` |
| Output | none, so no errors and no warnings |
| Axioms | `propext`, `Classical.choice`, `Quot.sound` on all three results, and no `sorryAx` |

### What is proved

```
theorem no_continuous_injection_to_real
    (hrank : 1 < Module.rank ℝ E) (φ : E → ℝ) (hcont : Continuous φ) :
    ¬ Function.Injective φ
```

for any real normed space `E`, with the corollary
`no_continuous_injection_euclidean` specialising it to `Fin d → ℝ` for `d ≥ 2`,
which covers the nine-dimensional decision space at `d = 9`.

### It is stronger than the roadmap's statement

The roadmap argues on the cube. It takes the image of `[0,1]^d` to be compact and
connected in `ℝ`, hence an interval, then notes that deleting an interior point
disconnects an interval and does not disconnect the cube.

The machine-checked proof drops both the cube and compactness. It runs on the
whole space, and the only structural input is that the complement of a point is
connected, which mathlib supplies as
`isConnected_compl_singleton_of_one_lt_rank` for rank above one.

The argument is three steps. For any point `p`, the punctured space `{p}ᶜ` is
connected, so its image under `φ` is a connected subset of `ℝ`, and injectivity
keeps `φ p` out of that image. A connected subset of `ℝ` missing a value lies
entirely on one side of it, so **every point of the space is a strict global
maximum of `φ` or a strict global minimum**. Three distinct points cannot all be
one or the other, because two strict maxima would each have to exceed the other.
The helper `strict_extremum_of_continuous_injective` carries the first two steps
and is the substance; the main theorem is the counting.

The roadmap's claim, that no continuous injection exists on any full-dimensional
region, is weaker than what is proved here and follows from it.

### What it does not establish

The theorem is about continuous maps and says nothing about behaviour. Its use in
the programme is conditional and the condition is empirical. Scalarization is
information-losing **if** the decision state genuinely varies in more than one
independent direction. That antecedent is not supplied by any theorem, is the
thing the projection-gap work exists to test, and `nobel-program.md` is explicit
that the nesting results are scientifically empty without it. Machine checking
Theorem 4 removes doubt about the mathematics and moves none of the empirical
burden.

### Reproducing

The file is checked against the mathlib already built for the textbook project on
Atlas rather than against a copy of its own, so there is no second mathlib build.

```
scp lean/ScalarIrrecoverability.lean atlas:~/dmo-lean/
ssh atlas 'cd ~/dmo-lean && lake env lean ScalarIrrecoverability.lean'
```

Append `#print axioms no_continuous_injection_to_real` to confirm the axiom list.
The scratch copy was removed from `~/dmo-lean` after checking, so that project is
unchanged.
