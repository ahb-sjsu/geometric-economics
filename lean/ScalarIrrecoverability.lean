/-
  Theorem 4 of `nobel-roadmap.txt`, the scalar irrecoverability theorem, machine
  checked.

  The roadmap states it for the cube and argues by compactness. It takes the
  image of `[0,1]^d` to be a compact connected subset of `ℝ`, hence an interval,
  and then observes that deleting an interior point disconnects an interval while
  deleting a point from the cube does not.

  The proof below is shorter and assumes less. Compactness is not needed and the
  cube is not needed. It holds for any real normed space of rank greater than one,
  so in particular for `ℝ^d` with `d ≥ 2` and for the nine-dimensional decision
  space of the programme, and it constrains `φ` on the whole space rather than on
  a full-dimensional region of it.

  The argument. If `φ` were a continuous injection into `ℝ`, then for any point
  `p` the set `{p}ᶜ` is connected, because the rank exceeds one. Its image under
  `φ` is a connected subset of `ℝ` that misses `φ p`, by injectivity. A connected
  subset of `ℝ` missing a value lies entirely on one side of it. So every point of
  the space is either a strict global maximum of `φ` or a strict global minimum.
  A space with three distinct points cannot have that, since two strict maxima
  would each have to exceed the other.

  Statement: there is no continuous injection from a real normed space of rank
  greater than one into `ℝ`.

  Checked against mathlib with `lake env lean`. No `sorry`.
-/
import Mathlib.Analysis.Normed.Module.Connected
import Mathlib.Topology.Order.IntermediateValue

open Set

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- If `φ` is a continuous injection into `ℝ` on a space whose punctured sets are
connected, then every point is a strict global extremum of `φ`. This is the whole
content of the theorem; the rest is counting. -/
theorem strict_extremum_of_continuous_injective
    (hrank : 1 < Module.rank ℝ E)
    {φ : E → ℝ} (hcont : Continuous φ) (hinj : Function.Injective φ) (p : E) :
    (∀ q, q ≠ p → φ q < φ p) ∨ (∀ q, q ≠ p → φ p < φ q) := by
  -- the punctured space is connected, which is where `1 < rank` is used
  have hconn : IsConnected ({p}ᶜ : Set E) :=
    isConnected_compl_singleton_of_one_lt_rank hrank p
  have himg : IsPreconnected (φ '' ({p}ᶜ : Set E)) :=
    (hconn.image φ hcont.continuousOn).isPreconnected
  -- injectivity keeps `φ p` out of the image of the punctured space
  have hnot : φ p ∉ φ '' ({p}ᶜ : Set E) := by
    rintro ⟨q, hq, hq'⟩
    exact hq (hinj hq')
  by_contra hcon
  push Not at hcon
  obtain ⟨⟨a, hap, hage⟩, ⟨b, hbp, hble⟩⟩ := hcon
  -- `a ≠ p` and `¬ (φ a < φ p)` give `φ p < φ a`, since injectivity forbids equality
  have hane : φ p ≠ φ a := fun h => hap (hinj h.symm)
  have hpa : φ p < φ a := lt_of_le_of_ne hage hane
  have hbne : φ b ≠ φ p := fun h => hbp (hinj h)
  have hbp' : φ b < φ p := lt_of_le_of_ne hble hbne
  -- both endpoints are in the image, so the interval between them is too
  have hamem : φ a ∈ φ '' ({p}ᶜ : Set E) := ⟨a, hap, rfl⟩
  have hbmem : φ b ∈ φ '' ({p}ᶜ : Set E) := ⟨b, hbp, rfl⟩
  have : Icc (φ b) (φ a) ⊆ φ '' ({p}ᶜ : Set E) := himg.Icc_subset hbmem hamem
  exact hnot (this ⟨le_of_lt hbp', le_of_lt hpa⟩)

/-- **Theorem 4, scalar irrecoverability.** No continuous map from a real normed
space of rank greater than one to `ℝ` is injective.

Read as the programme reads it: if the decision state genuinely varies in more
than one independent direction, then no continuous scalar summary of it is
invertible, so scalarization destroys information that cannot be recovered. The
antecedent is an empirical claim about behaviour and is not supplied here. -/
theorem no_continuous_injection_to_real
    (hrank : 1 < Module.rank ℝ E)
    (φ : E → ℝ) (hcont : Continuous φ) : ¬ Function.Injective φ := by
  intro hinj
  -- rank exceeds one, so the space is nontrivial and carries a nonzero vector
  have hnt : Nontrivial E := by
    rw [← rank_pos_iff_nontrivial (R := ℝ)]
    exact lt_trans zero_lt_one hrank
  obtain ⟨v, hv⟩ := exists_ne (0 : E)
  -- three distinct points suffice
  have h12 : v ≠ (0 : E) := hv
  have h13 : (2 : ℝ) • v ≠ (0 : E) := by
    simpa using smul_ne_zero (two_ne_zero' (α := ℝ)) hv
  have h23 : (2 : ℝ) • v ≠ v := by
    intro h
    apply hv
    have : (2 : ℝ) • v - (1 : ℝ) • v = 0 := by rw [one_smul, h, sub_self]
    rwa [← sub_smul, show (2 : ℝ) - 1 = 1 by norm_num, one_smul] at this
  -- every point is a strict maximum or a strict minimum
  have k0 := strict_extremum_of_continuous_injective hrank hcont hinj 0
  have k1 := strict_extremum_of_continuous_injective hrank hcont hinj v
  have k2 := strict_extremum_of_continuous_injective hrank hcont hinj ((2 : ℝ) • v)
  -- two of the three must be of the same kind, and two strict maxima, or two
  -- strict minima, each have to beat the other
  -- Two of the three points must be of the same kind. Whichever pair it is, the
  -- two strict maxima, or the two strict minima, each have to beat the other.
  rcases k0 with h0 | h0 <;> rcases k1 with h1 | h1 <;> rcases k2 with h2 | h2 <;>
    first
      | linarith [h0 v h12, h1 0 (Ne.symm h12)]
      | linarith [h0 ((2 : ℝ) • v) h13, h2 0 (Ne.symm h13)]
      | linarith [h1 ((2 : ℝ) • v) h23, h2 v (Ne.symm h23)]

/-- The programme's own case, stated for `ℝ^d` with `d ≥ 2`. The nine-dimensional
decision space of the monograph is `d = 9`. -/
theorem no_continuous_injection_euclidean
    {d : ℕ} (hd : 2 ≤ d) (φ : (Fin d → ℝ) → ℝ) (hcont : Continuous φ) :
    ¬ Function.Injective φ := by
  apply no_continuous_injection_to_real _ φ hcont
  rw [rank_fin_fun]
  have h1d : 1 < d := hd
  exact_mod_cast h1d
