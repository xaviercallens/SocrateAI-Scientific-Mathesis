/-
  Mathesis/Scale/Reff.lean — the T-dual effective radius.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed.
  (L4.4: compilation is not adequacy. This module becomes AUDITED only when a
   LEDGER row records the owner's sign-off.)

  ORIGIN AND CONSOLIDATION (SPEC-STREAM0 §4.1, §9)
  ------------------------------------------------
  Single source of truth for `Reff`. Consolidated from
  `SocrateAI-Scientific-MechanicaFluidorum/lean_src/CallensDualScale.lean`,
  renamed per the standing decision that no structure in this library carries a
  person's name (§9, L4.5). The mathematics is unchanged; the proofs are the
  ones that stream's kernel already accepted.

  ON THE "DUPLICATE" §4.1 EXPECTED TO FIND
  ----------------------------------------
  §1 and §4.1 state that `Reff` is "currently duplicated across `DualScale.lean`
  and `CallensDualScale.lean`", and §9 requires the two copies to be diffed
  before deletion. **The second copy does not exist under that name.** A search
  of every `.lean` file in ~/xdev on 2026-08-13 found exactly one definition of
  `Reff`, in MechanicaFluidorum.

  What Stream 5 carries instead is `DualScale/Geometry/TDuality.lean`, which
  models the same physics with different — and weaker — formal choices:
  it fixes `alpha_prime : ℝ := 1` as a global constant, and states T-duality
  invariance as `axiom t_duality_invariance`. So the divergence §1 predicted is
  real, but it is not a duplicated theorem set: it is the same idea formalized
  once with α quantified and once with α fixed and the content axiomatized.
  Recorded as `MX-C-0003`; see `docs/designs/RECONCILIATION.md` §3.

  There is therefore nothing to diff and nothing to delete. Consolidation here
  is a rename, not a merge.
-/
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.Ring

namespace Mathesis.Scale

/-! ## The effective radius

`Reff α R = max R (α / R)` — the scale the dual-scale geometry actually sees.

`α` is a **hypothesis parameter in every statement below**, never a global
constant. This is not bookkeeping: the physical content of the dual-scale
picture is how the geometry behaves *as α varies*, and a formalization that
fixes α still typechecks while saying something strictly weaker. Stream 1
records the same discipline (its SPEC §7.1), and `TDuality.lean` in Stream 5 is
what the other choice looks like. -/

/-- T-dual effective radius for fundamental area `α > 0` and scale `R`. -/
noncomputable def Reff (α R : ℝ) : ℝ := max R (α / R)

/-- The effective radius is positive: the geometry never collapses. -/
theorem Reff_pos {α R : ℝ} (_hα : 0 < α) (hR : 0 < R) : 0 < Reff α R :=
  lt_of_lt_of_le hR (le_max_left _ _)

/-- T-dual bound: `√α` is a universal minimum scale. -/
theorem Reff_ge_sqrt {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    Real.sqrt α ≤ Reff α R := by
  have hdiv : 0 < α / R := div_pos hα hR
  have hmax : 0 < Reff α R := Reff_pos hα hR
  have hsq : α ≤ Reff α R ^ 2 := by
    have h1 : R * (α / R) ≤ Reff α R * Reff α R :=
      mul_le_mul (le_max_left _ _) (le_max_right _ _) hdiv.le hmax.le
    have h2 : R * (α / R) = α := by field_simp
    calc α = R * (α / R) := h2.symm
      _ ≤ Reff α R * Reff α R := h1
      _ = Reff α R ^ 2 := by ring
  calc Real.sqrt α ≤ Real.sqrt (Reff α R ^ 2) := Real.sqrt_le_sqrt hsq
    _ = Reff α R := Real.sqrt_sq hmax.le

/-- Bounce: below the fundamental length the scale reflects to `α / R`. -/
theorem Reff_bounce {α R : ℝ} (hα : 0 < α) (hR : 0 < R)
    (h : R < Real.sqrt α) : Reff α R = α / R := by
  have hs : (0:ℝ) ≤ Real.sqrt α := Real.sqrt_nonneg α
  have hsq : R ^ 2 < α := by
    have h2 : R ^ 2 < Real.sqrt α ^ 2 := by nlinarith
    rwa [Real.sq_sqrt hα.le] at h2
  have hlt : R < α / R := by
    rw [lt_div_iff₀ hR]; nlinarith
  exact max_eq_right hlt.le

/-- Inertial invisibility: at or above `√α` the metric is classical. -/
theorem Reff_inertial {α R : ℝ} (hα : 0 < α) (hR : 0 < R)
    (h : Real.sqrt α ≤ R) : Reff α R = R := by
  have hs : (0:ℝ) ≤ Real.sqrt α := Real.sqrt_nonneg α
  have hsq : α ≤ R ^ 2 := by
    have h2 : Real.sqrt α ^ 2 ≤ R ^ 2 := by nlinarith
    rwa [Real.sq_sqrt hα.le] at h2
  have hle : α / R ≤ R := by
    rw [div_le_iff₀ hR]; nlinarith
  exact max_eq_left hle

/-- T-duality: the effective geometry cannot distinguish `R` from `α / R`. -/
theorem Reff_tdual {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    Reff α (α / R) = Reff α R := by
  have h : α / (α / R) = R := by field_simp
  unfold Reff
  rw [h, max_comm]

/-! ### Sharpness

`Reff_ge_sqrt` alone leaves open whether `√α` is *attained*. It is, at exactly
one point — the self-dual radius. That upgrades the statement from "a barrier
exists" to "the barrier is the self-dual scale", which is what the physical
narrative actually needs. -/

/-- Away from the self-dual radius the bound is strict. -/
theorem Reff_gt_sqrt_of_ne {α R : ℝ} (hα : 0 < α) (hR : 0 < R)
    (hne : R ≠ Real.sqrt α) : Real.sqrt α < Reff α R := by
  have hs : 0 < Real.sqrt α := Real.sqrt_pos.mpr hα
  have hsq : Real.sqrt α * Real.sqrt α = α := Real.mul_self_sqrt hα.le
  rcases lt_or_gt_of_ne hne with h | h
  · rw [Reff_bounce hα hR h, lt_div_iff₀ hR]
    nlinarith
  · rw [Reff_inertial hα hR h.le]
    exact h

/-- The minimum is attained at exactly one point: `R = √α`. -/
theorem Reff_eq_sqrt_iff {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    Reff α R = Real.sqrt α ↔ R = Real.sqrt α := by
  constructor
  · intro h
    by_contra hne
    have hlt := Reff_gt_sqrt_of_ne hα hR hne
    rw [h] at hlt
    exact lt_irrefl _ hlt
  · intro h
    rw [h]
    unfold Reff
    rw [Real.div_sqrt, max_self]

/-- **New target T4.1 (SPEC-STREAM0 §4.1).** Above the fundamental length,
`1/x²` is bounded by `1/α`.

This is the inequality the downstream enstrophy estimates want: it converts the
minimum-scale statement into the bound on inverse-square quantities that a
frequency cutoff at `√α` actually delivers. -/
theorem one_div_sq_le_of_sqrt_le {α x : ℝ} (hα : 0 < α) (hx : Real.sqrt α ≤ x) :
    1 / x ^ 2 ≤ 1 / α := by
  have hs : 0 < Real.sqrt α := Real.sqrt_pos.mpr hα
  have hxpos : 0 < x := lt_of_lt_of_le hs hx
  have hsq : α ≤ x ^ 2 := by
    have h2 : Real.sqrt α ^ 2 ≤ x ^ 2 := by nlinarith
    rwa [Real.sq_sqrt hα.le] at h2
  exact one_div_le_one_div_of_le hα hsq

/-! ### The piecewise presentation

The geometry is often written piecewise ("bounce below `√α`, classical above").
The two forms agree — but only for `R > 0`, and the failure off that range is
not a technicality. It is Lean's junk-value discipline catching a real mismatch,
and the witness below is why the side condition stays in every statement. -/

/-- Piecewise ("bounce") presentation. -/
noncomputable def tDualRadius (α R : ℝ) : ℝ :=
  if R < Real.sqrt α then α / R else R

/-- The two presentations coincide on the physical range. -/
theorem tDualRadius_eq_Reff {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    tDualRadius α R = Reff α R := by
  unfold tDualRadius
  split_ifs with h
  · exact (Reff_bounce hα hR h).symm
  · exact (Reff_inertial hα hR (not_lt.mp h)).symm

/-- The effective radius never collapses to zero — axiom-free, with `α` a
hypothesis rather than a global constant. -/
theorem genesis_no_singularity {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    0 < tDualRadius α R := by
  rw [tDualRadius_eq_Reff hα hR]
  exact Reff_pos hα hR

/-! ### Non-vacuity witnesses (L4.2) -/

/-- With `α = 4`, the scale `R = 1` sits below `√α = 2` and bounces to `4`. -/
example : Reff 4 1 = 4 := by unfold Reff; norm_num [max_def]

/-- The self-dual point is inhabited: at `R = √α` the minimum is attained. -/
example : Reff 4 2 = 2 := by unfold Reff; norm_num [max_def]

/-- **The side condition is not decorative.** At `α = 4, R = -1` the two
presentations disagree: `Reff` gives `-1` and `tDualRadius` gives `-4`. Every
theorem above therefore carries `0 < R`, and this witness is why. -/
example : Reff 4 (-1) = -1 ∧ tDualRadius 4 (-1) = -4 := by
  constructor
  · unfold Reff; norm_num [max_def]
  · unfold tDualRadius
    rw [if_pos (by rw [show (4:ℝ) = 2^2 by norm_num, Real.sqrt_sq (by norm_num)]; norm_num)]
    norm_num

/-! ### Axiom footprints -/

#print axioms Reff_pos
#print axioms Reff_ge_sqrt
#print axioms Reff_bounce
#print axioms Reff_inertial
#print axioms Reff_tdual
#print axioms Reff_gt_sqrt_of_ne
#print axioms Reff_eq_sqrt_iff
#print axioms one_div_sq_le_of_sqrt_le
#print axioms tDualRadius_eq_Reff
#print axioms genesis_no_singularity

end Mathesis.Scale
