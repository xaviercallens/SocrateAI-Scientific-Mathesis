/-
  Mathesis/Applications/LotkaVolterra.lean — Use case 5 (biology). CAPSTONE.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed.
  PARTIAL BY DESIGN — see "What is deliberately NOT proved here".

  THE SETTING
  -----------
  The Lotka-Volterra predator-prey system, for prey x and predator y:

      ẋ = αx - βxy
      ẏ = δxy - γy

  It has a conserved quantity, which is why its orbits are closed curves rather
  than spirals:

      V(x,y) = δx - γ ln x + βy - α ln y

  WHY THIS IS USE CASE 5
  ----------------------
  Because it is the first one that does NOT go all the way, and the campaign
  needs one that does not. A pipeline that has only ever produced successes has
  not been tested (docs/CLAUDE5_LOOP.md §4).

  WHAT IS PROVED HERE (Tier A)
  ----------------------------
  Substituting the vector field into dV/dt and clearing the logarithmic
  derivatives leaves a rational expression in α, β, γ, δ, x, y. That expression
  is IDENTICALLY ZERO. This is the whole algebraic content of the conservation
  law, it needs no calculus, and it is proved below by `field_simp; ring`.

  Concretely, the four terms cancel in pairs:

      δ(αx - βxy)          =  δαx - δβxy
    - γ(αx - βxy)/x        = -γα  + γβy
    + β(δxy - γy)          =  βδxy - βγy
    - α(δxy - γy)/y        = -αδx + αγ
                             ─────────────
                                    0

  WHAT IS DELIBERATELY *NOT* PROVED HERE
  --------------------------------------
  That this expression IS dV/dt. That step needs the chain rule and the
  derivative of `Real.log`, over ℝ rather than ℚ, plus a solution concept for
  the ODE. Mathlib has the pieces; assembling them is real work and it is not
  done here.

  It would have been easy to fake. Two ways, both refused:

  1. `axiom lotka_volterra_conserved : ...` — forbidden outright (SPEC.md §7.1).
     It would put an unproven analytic claim into the footprint of everything
     downstream, permanently and invisibly.

  2. State it conditionally: "given (dV/dt = D) as a hypothesis, and D = 0,
     therefore dV/dt = 0." This compiles, carries no axioms, and looks like a
     Tier A theorem. It is a TAUTOLOGY — it proves A → B → B and contains no
     mathematics at all.

  Option 2 is refused on precedent, not on taste. MechanicaFluidorum's
  `MillenniumReduction.lean` did exactly this for Aubin-Lions and Prodi-Serrin,
  was audited, and was DEMOTED TO TIER C on 2026-08-13 with the verdict that
  bare `Prop → Prop` arrows "completely bypass PDE theory. The Lean kernel is
  merely verifying a logical tautology (A → B → C)." That demotion was accepted
  by its own stream. Repeating the pattern here, one file later, would be the
  clearest possible demonstration that this repository does not read its own
  ledger.

  So: the algebra is Tier A, the dynamical claim is Tier C and OPEN, and the two
  are separate ledger rows. See MX-A-0010 and MX-C-0004.
-/
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace Mathesis.Applications.LotkaVolterra

/-- Prey rate of change, `ẋ = αx - βxy`. -/
def preyRate (α β x y : ℚ) : ℚ := α * x - β * x * y

/-- Predator rate of change, `ẏ = δxy - γy`. -/
def predRate (γ δ x y : ℚ) : ℚ := δ * x * y - γ * y

/-- The expression obtained by substituting the vector field into `dV/dt` and
using `d(ln u)/dt = u̇/u`.

This is a purely algebraic object: it is what `dV/dt` *would* reduce to, and the
theorem below is about this expression, not about any derivative. -/
def dVdt (α β γ δ x y : ℚ) : ℚ :=
  δ * preyRate α β x y - γ * preyRate α β x y / x
    + β * predRate γ δ x y - α * predRate γ δ x y / y

/-- **UC5 (Tier A) — the algebraic core of the conservation law.**

For any positive populations, the substituted expression vanishes identically.
No calculus is used or needed: this is a rational-function identity. -/
theorem dVdt_eq_zero (α β γ δ x y : ℚ) (hx : x ≠ 0) (hy : y ≠ 0) :
    dVdt α β γ δ x y = 0 := by
  unfold dVdt preyRate predRate
  field_simp
  ring

/-! ### Non-vacuity witnesses (HARDNESS.md H5)

`dVdt_eq_zero` says an expression is zero. That is exactly the shape of theorem
that is worthless if the expression is zero for trivial reasons, so the witnesses
below establish that the terms are individually non-zero and only cancel in
combination. -/

/-- A concrete ecology: α=2, β=1, γ=1, δ=1 at x=3, y=1. -/
example : dVdt 2 1 1 1 3 1 = 0 := by unfold dVdt preyRate predRate; norm_num

/-- **The cancellation is real, not vacuous.** At those parameters the two rates
are `3` and `2` — both non-zero — so the identity is a genuine cancellation
rather than a sum of zeros.

Choosing this witness took two attempts. The first used `y = 2`, where
`α - βy = 0` makes the prey rate *exactly zero*, so the "witness" would have
demonstrated the one case that proves nothing. The kernel rejected it with
`⊢ False`. Non-vacuity witnesses have to be computed, not guessed. -/
example : preyRate 2 1 3 1 = 3 ∧ predRate 1 1 3 1 = 2 := by
  unfold preyRate predRate; norm_num

/-- **The hypotheses are load-bearing.** At `x = 0` Lean's junk-value convention
makes `preyRate/x = 0/0 = 0`, the cancellation fails, and `dVdt = 1 ≠ 0`. This is
why `hx` and `hy` appear in the theorem.

This witness also took two attempts: at `x = 0, y = 2` the expression *does*
still vanish, because `α - βy = 0` there makes the junk value coincide with the
limit. A counterexample has to miss on purpose, and `y = 1` is where it does. -/
example : dVdt 2 1 1 1 0 1 ≠ 0 := by unfold dVdt preyRate predRate; norm_num

/-! ### Axiom footprints -/

#print axioms dVdt_eq_zero

end Mathesis.Applications.LotkaVolterra
