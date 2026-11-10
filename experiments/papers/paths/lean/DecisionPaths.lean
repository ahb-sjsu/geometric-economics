/-
Decisions as least-cost paths: what Definitions 6.1 and 6.2 of `geometric-methods`
Chapter 6 do and do not imply.

A decision complex is a set of states with a weight on each ordered pair. The
weight is a symmetric distance term plus a sum of boundary penalties
(Definition 6.1). A decision is a walk of least total weight to a goal set
(Definition 6.2). Weights live in the extended non-negative reals, as in the
definition, so a penalty may be infinite.

Checked here:

1. `cost_append`              the weight of a walk is additive over a history and its continuation
2. `ranking_history_free`     so two histories that end in the same state rank continuations alike
3. `best_continuation_history_free`  and have the same best continuations to any goal set
4. `history_can_matter_if_weight_reads_the_past`  this fails once a weight may depend on the previous state
5. `direction_difference`     the two directions of one pair differ only by boundary penalties
6. `boundary_edge_costs_its_penalty`  of two moves at equal distance, the one crossing a boundary costs its penalty more
7. `weight_top_of_sacred`, `cost_eq_top_of_crossesTop`, `no_finite_path_through_sacred`
                              an infinite penalty on every route leaves no route of finite weight (Theorem 6.4)

Nothing here says anything about what people do. These are consequences of the definitions.
-/
import Mathlib

open scoped ENNReal BigOperators

namespace DecisionPaths

variable {V : Type*}

/-- Total weight of the walk that starts at `v` and then visits the states in `p` in order. -/
def cost (w : V → V → ℝ≥0∞) : V → List V → ℝ≥0∞
  | _, [] => 0
  | v, u :: p => w v u + cost w u p

/-- The state a walk ends in. -/
def endOf : V → List V → V
  | v, [] => v
  | _, u :: p => endOf u p

/-- The weight of a history followed by a continuation is the sum of the two. -/
theorem cost_append (w : V → V → ℝ≥0∞) (s : V) (h p : List V) :
    cost w s (h ++ p) = cost w s h + cost w (endOf s h) p := by
  induction h generalizing s with
  | nil => simp [cost, endOf]
  | cons u h ih => simp [cost, endOf, ih, add_assoc]

/-- Two histories of finite weight that end in the same state rank any two continuations
the same way. The past adds the same amount to both and cancels. -/
theorem ranking_history_free (w : V → V → ℝ≥0∞) (s₁ s₂ : V) (h₁ h₂ p q : List V)
    (hend : endOf s₁ h₁ = endOf s₂ h₂)
    (f₁ : cost w s₁ h₁ ≠ ⊤) (f₂ : cost w s₂ h₂ ≠ ⊤) :
    cost w s₁ (h₁ ++ p) ≤ cost w s₁ (h₁ ++ q) ↔
      cost w s₂ (h₂ ++ p) ≤ cost w s₂ (h₂ ++ q) := by
  rw [cost_append, cost_append, cost_append, cost_append, hend,
    ENNReal.add_le_add_iff_left f₁, ENNReal.add_le_add_iff_left f₂]

/-- So the best continuations to a goal set are the same after either history.
This is the sense in which Definition 6.2 makes the decision depend on the present
state and the goal and on nothing before. -/
theorem best_continuation_history_free (w : V → V → ℝ≥0∞) (s₁ s₂ : V)
    (h₁ h₂ p : List V) (G : Set V)
    (hend : endOf s₁ h₁ = endOf s₂ h₂)
    (f₁ : cost w s₁ h₁ ≠ ⊤) (f₂ : cost w s₂ h₂ ≠ ⊤) :
    (∀ q, endOf (endOf s₁ h₁) q ∈ G → cost w s₁ (h₁ ++ p) ≤ cost w s₁ (h₁ ++ q)) ↔
      (∀ q, endOf (endOf s₂ h₂) q ∈ G → cost w s₂ (h₂ ++ p) ≤ cost w s₂ (h₂ ++ q)) := by
  constructor
  · intro H q hq
    exact (ranking_history_free w s₁ s₂ h₁ h₂ p q hend f₁ f₂).mp
      (H q (by rw [hend]; exact hq))
  · intro H q hq
    exact (ranking_history_free w s₁ s₂ h₁ h₂ p q hend f₁ f₂).mpr
      (H q (by rw [← hend]; exact hq))

/-- History independence is a property of weights that read only the present state and
the next. If a weight may also read the previous state, as a reference point that
moves with the past would, two histories ending in the same state can prefer
different next states. Here a move back to where one came from is free and any
other move costs one. -/
theorem history_can_matter_if_weight_reads_the_past :
    ∃ w3 : Fin 3 → Fin 3 → Fin 3 → ℕ,
      w3 0 2 0 < w3 0 2 1 ∧ w3 1 2 1 < w3 1 2 0 :=
  ⟨fun prev _ next => if next = prev then 0 else 1, by decide, by decide⟩

/-! ### A reference that moves with the past

The smallest addition to Definition 6.1 that lets history in: each edge weight may read
a reference `r`, and the reference is updated after every step. The pair of state and
reference then does the work the state did alone. -/

section Reference

variable {R : Type*}

/-- Weight of a walk when each edge weight reads a reference that `step` updates. -/
def costRef (w : R → V → V → ℝ≥0∞) (step : R → V → V → R) : R → V → List V → ℝ≥0∞
  | _, _, [] => 0
  | r, v, u :: p => w r v u + costRef w step (step r v u) u p

/-- The reference a walk ends with. -/
def refAfter (step : R → V → V → R) : R → V → List V → R
  | r, _, [] => r
  | r, v, u :: p => refAfter step (step r v u) u p

theorem endOf_append (s : V) (h p : List V) :
    endOf s (h ++ p) = endOf (endOf s h) p := by
  induction h generalizing s with
  | nil => simp [endOf]
  | cons u h ih => simp [endOf, ih]

theorem refAfter_append (step : R → V → V → R) (r : R) (s : V) (h p : List V) :
    refAfter step r s (h ++ p) = refAfter step (refAfter step r s h) (endOf s h) p := by
  induction h generalizing r s with
  | nil => simp [refAfter, endOf]
  | cons u h ih => simp [refAfter, endOf, ih]

theorem costRef_append (w : R → V → V → ℝ≥0∞) (step : R → V → V → R) (r : R) (s : V)
    (h p : List V) :
    costRef w step r s (h ++ p) =
      costRef w step r s h + costRef w step (refAfter step r s h) (endOf s h) p := by
  induction h generalizing r s with
  | nil => simp [costRef, refAfter, endOf]
  | cons u h ih => simp [costRef, refAfter, endOf, ih, add_assoc]

/-- With a moving reference, two histories that end in the same state **and the same
reference** rank continuations alike. History enters through the reference and through
nothing else. -/
theorem ranking_depends_on_state_and_reference (w : R → V → V → ℝ≥0∞)
    (step : R → V → V → R) (r₁ r₂ : R) (s₁ s₂ : V) (h₁ h₂ p q : List V)
    (hend : endOf s₁ h₁ = endOf s₂ h₂)
    (href : refAfter step r₁ s₁ h₁ = refAfter step r₂ s₂ h₂)
    (f₁ : costRef w step r₁ s₁ h₁ ≠ ⊤) (f₂ : costRef w step r₂ s₂ h₂ ≠ ⊤) :
    costRef w step r₁ s₁ (h₁ ++ p) ≤ costRef w step r₁ s₁ (h₁ ++ q) ↔
      costRef w step r₂ s₂ (h₂ ++ p) ≤ costRef w step r₂ s₂ (h₂ ++ q) := by
  rw [costRef_append, costRef_append, costRef_append, costRef_append, hend, href,
    ENNReal.add_le_add_iff_left f₁, ENNReal.add_le_add_iff_left f₂]

/-- A weight that ignores the reference gives back the original cost. Definition 6.1 is
the special case. -/
theorem costRef_const (w : V → V → ℝ≥0∞) (step : R → V → V → R) (r : R) (v : V)
    (p : List V) : costRef (fun _ => w) step r v p = cost w v p := by
  induction p generalizing r v with
  | nil => simp [costRef, cost]
  | cons u p ih => simp [costRef, cost, ih]

/-- If the reference is the state just left, a history that ends by going from `a` to `b`
ends with reference `a`, whatever came before. -/
theorem refAfter_previous_state (r : V) (s : V) (g : List V) (a b : V) :
    refAfter (fun _ v _ => v) r s (g ++ [a, b]) = a := by
  have h : g ++ [a, b] = (g ++ [a]) ++ [b] := by simp
  rw [h, refAfter_append, endOf_append]
  simp [refAfter, endOf]

/-- So when the reference is the state just left, two histories that share their last
step rank continuations alike. Fixing the last move is then enough to remove every
effect of what came earlier. -/
theorem last_step_suffices_when_reference_is_previous_state (w : V → V → V → ℝ≥0∞)
    (r₁ r₂ s₁ s₂ : V) (g₁ g₂ p q : List V) (a b : V)
    (f₁ : costRef w (fun _ v _ => v) r₁ s₁ (g₁ ++ [a, b]) ≠ ⊤)
    (f₂ : costRef w (fun _ v _ => v) r₂ s₂ (g₂ ++ [a, b]) ≠ ⊤) :
    costRef w (fun _ v _ => v) r₁ s₁ ((g₁ ++ [a, b]) ++ p) ≤
        costRef w (fun _ v _ => v) r₁ s₁ ((g₁ ++ [a, b]) ++ q) ↔
      costRef w (fun _ v _ => v) r₂ s₂ ((g₂ ++ [a, b]) ++ p) ≤
        costRef w (fun _ v _ => v) r₂ s₂ ((g₂ ++ [a, b]) ++ q) := by
  apply ranking_depends_on_state_and_reference _ _ _ _ _ _ _ _ _ _ _ _ f₁ f₂
  · have e : ∀ (s : V) (g : List V), endOf s (g ++ [a, b]) = b := by
      intro s g
      rw [endOf_append]
      simp [endOf]
    rw [e, e]
  · rw [refAfter_previous_state, refAfter_previous_state]

end Reference

section Finite

variable {K : Type*} [Fintype K]

/-- The edge weight of Definition 6.1 with finite penalties: a distance term plus the
penalties of the boundaries the edge crosses. -/
noncomputable def weight (d : V → V → ℝ) (β : K → ℝ) (cross : K → V → V → Prop)
    [∀ k a b, Decidable (cross k a b)] (a b : V) : ℝ :=
  d a b + ∑ k, β k * (if cross k a b then 1 else 0)

/-- With a symmetric distance term, the two directions of one pair of states differ by
the boundary penalties alone. The distance cancels whatever it is. -/
theorem direction_difference (d : V → V → ℝ) (β : K → ℝ) (cross : K → V → V → Prop)
    [∀ k a b, Decidable (cross k a b)] (hsymm : ∀ a b, d a b = d b a) (a b : V) :
    weight d β cross a b - weight d β cross b a =
      ∑ k, β k * ((if cross k a b then (1 : ℝ) else 0) - (if cross k b a then 1 else 0)) := by
  unfold weight
  rw [hsymm a b]
  simp only [mul_sub, Finset.sum_sub_distrib]
  ring

/-- Of two moves from the same state at the same distance, one crossing exactly the
boundary `k` and the other crossing none, the first costs `β k` more. -/
theorem boundary_edge_costs_its_penalty [DecidableEq K] (d : V → V → ℝ) (β : K → ℝ)
    (cross : K → V → V → Prop) [∀ k a b, Decidable (cross k a b)] (a b c : V) (k : K)
    (hd : d a b = d a c) (hb : ∀ j, cross j a b ↔ j = k) (hc : ∀ j, ¬ cross j a c) :
    weight d β cross a b = weight d β cross a c + β k := by
  unfold weight
  simp [hd, hb, hc]

/-- An infinite penalty on a boundary the edge crosses makes the edge weight infinite. -/
theorem weight_top_of_sacred (d : V → V → ℝ≥0∞) (β : K → ℝ≥0∞) (cross : K → V → V → Prop)
    [∀ k a b, Decidable (cross k a b)] (a b : V) (k : K)
    (hβ : β k = ⊤) (hk : cross k a b) :
    d a b + ∑ j, β j * (if cross j a b then (1 : ℝ≥0∞) else 0) = ⊤ := by
  have h : β k * (if cross k a b then (1 : ℝ≥0∞) else 0) ≤
      ∑ j, β j * (if cross j a b then (1 : ℝ≥0∞) else 0) :=
    Finset.single_le_sum
      (f := fun j => β j * (if cross j a b then (1 : ℝ≥0∞) else 0))
      (fun _ _ => zero_le) (Finset.mem_univ k)
  rw [hβ, if_pos hk, mul_one, top_le_iff] at h
  rw [h]
  exact add_top _

end Finite

/-- The walk uses at least one edge of infinite weight. -/
def crossesTop (w : V → V → ℝ≥0∞) : V → List V → Prop
  | _, [] => False
  | v, u :: p => w v u = ⊤ ∨ crossesTop w u p

/-- A walk that uses an edge of infinite weight has infinite weight. -/
theorem cost_eq_top_of_crossesTop (w : V → V → ℝ≥0∞) (v : V) (p : List V)
    (h : crossesTop w v p) : cost w v p = ⊤ := by
  induction p generalizing v with
  | nil => simp [crossesTop] at h
  | cons u p ih =>
    rcases h with h | h
    · simp [cost, h]
    · simp [cost, ih u h]

/-- Theorem 6.4 of Chapter 6. If every walk from `s` to the goal set uses an edge of
infinite weight, no walk from `s` to the goal set has finite weight. -/
theorem no_finite_path_through_sacred (w : V → V → ℝ≥0∞) (s : V) (G : Set V)
    (hall : ∀ p, endOf s p ∈ G → crossesTop w s p) :
    ∀ p, endOf s p ∈ G → cost w s p = ⊤ :=
  fun p hp => cost_eq_top_of_crossesTop w s p (hall p hp)

end DecisionPaths
