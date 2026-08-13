/-
  Mathesis/Applications/Kepler.lean — Use case 4 (physics).

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  THE CLAIM
  ---------
  For circular orbits under an inverse-square central force, ω²r³ is the same
  constant for every orbit around the same primary. That is Kepler's third law.

  WHY THIS IS USE CASE 4
  ----------------------
  Because the float ban forces a better statement, and it is worth watching it
  happen.

  Kepler III is normally written T² ∝ a³, and T = 2π/ω puts π on both sides.
  π is irrational, so nothing about T² is checkable in exact arithmetic, and the
  usual response is to go to floats and report agreement to some number of
  digits — which certifies a rounding mode, not a physical law.

  The escape is to notice that π was never carrying any physics. Work with the
  REDUCED PERIOD τ = T/2π = 1/ω. Then

      r³/τ² = ω²r³ = GM

  is exactly rational whenever r and GM are, the constant is GM rather than
  4π²/GM, and π has left the statement entirely. Nothing was approximated and
  nothing was lost: the proportionality T² ∝ a³ follows immediately, since T and
  τ differ by a factor that is the same for every orbit.

  This is the float ban doing what it is for. It did not make the physics harder
  to state; it located a constant that was decoration and removed it.

  WHAT THIS DOES NOT CLAIM
  -----------------------
  Nothing about the solar system. That planetary orbits obey this is an
  empirical claim resting on observation — Tier L, resting on Kepler's own data
  and everything since. This file proves that the law FOLLOWS FROM the
  inverse-square force law for circular orbits, which is a different statement
  and a Tier A one, conditional on the force law given as a hypothesis.
-/
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace Mathesis.Applications.Kepler

/-- **UC4a — the force balance gives ω²r³ = GM.**

`CircularOrbit μ r ω` says: the centripetal acceleration `ω²r` required to hold
a circular orbit of radius `r` at angular velocity `ω` equals the gravitational
acceleration `μ/r²`, where `μ = GM` is the standard gravitational parameter.

The force law is a HYPOTHESIS, not an axiom (SPEC.md §7.1). The theorem is
therefore conditional, and the ledger records what it is conditional on. -/
def CircularOrbit (μ r ω : ℚ) : Prop := ω ^ 2 * r = μ / r ^ 2

/-- The invariant: `ω²r³` is the gravitational parameter. -/
theorem omega_sq_r_cubed (μ r ω : ℚ) (hr : r ≠ 0) (h : CircularOrbit μ r ω) :
    ω ^ 2 * r ^ 3 = μ := by
  unfold CircularOrbit at h
  field_simp at h
  linarith [h]

/-- **UC4b — Kepler's third law.**

Two circular orbits around the same primary have the same `ω²r³`. Equivalently,
with the reduced period `τ = 1/ω`, `r³/τ²` is the same for both — which is
`T² ∝ a³` with the `4π²` divided out of both sides. -/
theorem kepler_third (μ r₁ ω₁ r₂ ω₂ : ℚ)
    (hr₁ : r₁ ≠ 0) (hr₂ : r₂ ≠ 0)
    (h₁ : CircularOrbit μ r₁ ω₁) (h₂ : CircularOrbit μ r₂ ω₂) :
    ω₁ ^ 2 * r₁ ^ 3 = ω₂ ^ 2 * r₂ ^ 3 := by
  rw [omega_sq_r_cubed μ r₁ ω₁ hr₁ h₁, omega_sq_r_cubed μ r₂ ω₂ hr₂ h₂]

/-! ### Non-vacuity witnesses (HARDNESS.md H5)

`kepler_third` has four hypotheses. If `CircularOrbit` were unsatisfiable the
theorem would be true and empty, so an orbit is exhibited. -/

/-- A satisfying orbit: `μ = 1`, `r = 1`, `ω = 1`. The hypothesis class is
non-empty, so the theorem is about something. -/
example : CircularOrbit 1 1 1 := by unfold CircularOrbit; norm_num

/-- A second, genuinely different orbit around the same primary: `r = 4` forces
`ω² = 1/64`, and `ω = 1/8` satisfies it. Two distinct radii is what makes
`kepler_third` a comparison rather than a tautology. -/
example : CircularOrbit 1 4 (1/8) := by unfold CircularOrbit; norm_num

/-- The two orbits above do satisfy Kepler III: `1²·1³ = (1/8)²·4³ = 1`. -/
example : (1 : ℚ) ^ 2 * 1 ^ 3 = (1/8 : ℚ) ^ 2 * 4 ^ 3 := by norm_num

/-- **Not every (r, ω) pair is an orbit.** `r = 4, ω = 1` does not satisfy the
force balance, so `CircularOrbit` genuinely constrains its arguments rather than
holding of everything. -/
example : ¬ CircularOrbit 1 4 1 := by unfold CircularOrbit; norm_num

/-! ### Axiom footprints -/

#print axioms omega_sq_r_cubed
#print axioms kepler_third

end Mathesis.Applications.Kepler
