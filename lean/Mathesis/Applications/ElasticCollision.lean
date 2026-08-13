/-
  Mathesis/Applications/ElasticCollision.lean — Use case 2 (physics).

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  THE CLAIM
  ---------
  The standard 1-D elastic collision formulae conserve both momentum and kinetic
  energy exactly, for any masses with m₁ + m₂ ≠ 0.

      v₁ = ((m₁ - m₂)u₁ + 2m₂u₂)/(m₁ + m₂)
      v₂ = ((m₂ - m₁)u₂ + 2m₁u₁)/(m₁ + m₂)

  WHY THIS IS USE CASE 2
  ----------------------
  First contact with physics, and the first place the float ban does real work.
  The textbook treatment of this problem is numerical and the conservation check
  is reported as "agrees to 10⁻¹⁵". That number is not a check — it is a report
  about a rounding mode. Over ℚ the two quantities are conserved or they are not,
  and here they are, identically.

  ON WORKING OVER ℚ
  -----------------
  Deliberate, and not merely convenient. The Tier B harness for this claim uses
  Python's `Fraction`; this file uses `ℚ`. Those are the *same* mathematical
  object, so the Tier A theorem and the Tier B check are statements about one
  structure rather than two that happen to agree numerically. Over ℝ the theorem
  would be marginally more general and the correspondence with the harness would
  be looser. The generality is not what is scarce here.

  WHAT THIS DOES NOT CLAIM
  -----------------------
  That any real collision is elastic. That is an empirical question about a
  physical system, and it is Tier C at best for any actual apparatus. This file
  proves that *the formulae* have the conservation property, nothing more.
-/
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace Mathesis.Applications.ElasticCollision

variable (m₁ m₂ u₁ u₂ : ℚ)

/-- Post-collision velocity of body 1. -/
noncomputable def v₁ : ℚ := ((m₁ - m₂) * u₁ + 2 * m₂ * u₂) / (m₁ + m₂)

/-- Post-collision velocity of body 2. -/
noncomputable def v₂ : ℚ := ((m₂ - m₁) * u₂ + 2 * m₁ * u₁) / (m₁ + m₂)

/-- **UC2a — momentum is conserved.** -/
theorem momentum_conserved (h : m₁ + m₂ ≠ 0) :
    m₁ * v₁ m₁ m₂ u₁ u₂ + m₂ * v₂ m₁ m₂ u₁ u₂ = m₁ * u₁ + m₂ * u₂ := by
  unfold v₁ v₂
  field_simp
  ring

/-- **UC2b — kinetic energy is conserved.**

The factor of ½ is omitted from both sides; it cancels, and carrying it would
introduce a division that says nothing. -/
theorem kinetic_energy_conserved (h : m₁ + m₂ ≠ 0) :
    m₁ * (v₁ m₁ m₂ u₁ u₂) ^ 2 + m₂ * (v₂ m₁ m₂ u₁ u₂) ^ 2
      = m₁ * u₁ ^ 2 + m₂ * u₂ ^ 2 := by
  unfold v₁ v₂
  field_simp
  ring

/-! ### Non-vacuity witnesses (HARDNESS.md H5)

Both theorems are conditional on `m₁ + m₂ ≠ 0`. An implication whose hypothesis
is never satisfiable is not evidence of anything, so the hypothesis is exhibited
as satisfiable, and the conclusion is exhibited on a concrete collision. -/

/-- Equal masses exchange velocities — the classic Newton's-cradle case. -/
example : v₁ 1 1 3 (-1) = -1 ∧ v₂ 1 1 3 (-1) = 3 := by
  unfold v₁ v₂; norm_num

/-- A concrete unequal-mass collision, with both conserved quantities checked
by the kernel rather than asserted. -/
example : (2 : ℚ) * v₁ 2 3 5 0 + 3 * v₂ 2 3 5 0 = 2 * 5 + 3 * 0 := by
  unfold v₁ v₂; norm_num

/-- **The hypothesis is load-bearing.** With `m₂ = -m₁` the formulae divide by
zero, Lean's junk-value convention makes both velocities `0`, and momentum is
*not* conserved. This witness is why `h` appears in both statements. -/
example : (1 : ℚ) * v₁ 1 (-1) 4 0 + (-1) * v₂ 1 (-1) 4 0 ≠ 1 * 4 + (-1) * 0 := by
  unfold v₁ v₂; norm_num

/-! ### Axiom footprints -/

#print axioms momentum_conserved
#print axioms kinetic_energy_conserved

end Mathesis.Applications.ElasticCollision
