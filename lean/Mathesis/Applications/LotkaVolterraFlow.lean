/-
  Mathesis/Applications/LotkaVolterraFlow.lean — UC5, the analytic bridge.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  WHAT THIS FILE DOES
  -------------------
  It closes the gap that `LotkaVolterra.lean` deliberately left open.

  That file proved the ALGEBRAIC core over ℚ: the expression obtained by
  substituting the Lotka-Volterra vector field into dV/dt is identically zero.
  It explicitly did NOT prove that the expression IS dV/dt, and recorded the
  missing step as `MX-C-0004`, OPEN — refusing both available shortcuts:

    1. `axiom lotka_volterra_conserved`   (forbidden, SPEC.md §7.1)
    2. the conditional restatement "given dV/dt = D, and D = 0, hence dV/dt = 0"
       (a tautology of the shape Stream 1's MillenniumReduction.lean was demoted
        to Tier C for)

  Here the step is *proved*, over ℝ, using `HasDerivAt.log` and the derivative
  algebra. `conserved_along_flow` states that V is genuinely constant along any
  trajectory of the system: its derivative is 0, not "0 given that it is 0".

  So `MX-C-0004` is superseded by `MX-A-0011`. Per SPEC.md §2.5 the promotion
  CHANGES THE IDENTIFIER rather than editing a tier letter in place, and the new
  row records `supersedes`. This is the first promotion in this repository's
  ledger and the first exercise of that mechanism.

  WHAT IT COST, AND WHY THAT IS WORTH RECORDING
  ---------------------------------------------
  Nothing mathematically — the proof is nine lines. The obstacle was entirely
  infrastructural: `Analysis.SpecialFunctions.Log.Deriv` and
  `Analysis.Calculus.Deriv.{Add,Mul}` are NOT built in the RajMathRecovery
  Mathlib checkout, and ARE built in the MechanicaFluidorum one. Against the
  first this file does not compile; against the second it does, on the first
  attempt.

  Two streams' Mathlib subsets differ, neither is complete, and which one
  `LEAN_ENV_DIR` resolves to silently determines what is provable — with no
  diagnostic separating "this is false" from "that module was never built".
  That is PLAN.md K1, and this file is the concrete evidence for it.

  WHAT IS STILL NOT CLAIMED
  -------------------------
  That any ecosystem obeys Lotka-Volterra. The theorem is about trajectories of
  the stated system, whose two equations appear as hypotheses `hx` and `hy` in
  the type. Applying it to actual populations is a separate, lower-tier claim
  that cites this one — and by MX-A-0004 can never be Tier A.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace Mathesis.Applications.LotkaVolterraFlow

/-- The Lotka-Volterra conserved quantity, `V = δx − γ ln x + βy − α ln y`. -/
noncomputable def V (α β γ δ x y : ℝ) : ℝ :=
  δ * x - γ * Real.log x + β * y - α * Real.log y

/-- **UC5 (complete) — `V` is conserved along the flow.**

For any differentiable `x, y : ℝ → ℝ` satisfying the Lotka-Volterra equations at
`t`, with both populations non-zero, the derivative of `V` along the trajectory
is exactly `0`.

The two equations of the system are hypotheses (`hx`, `hy`), so the theorem is
conditional on the model and says so in its type. Nothing is axiomatized. -/
theorem conserved_along_flow (α β γ δ : ℝ) (x y : ℝ → ℝ) (t : ℝ)
    (hx : HasDerivAt x (α * x t - β * x t * y t) t)
    (hy : HasDerivAt y (δ * x t * y t - γ * y t) t)
    (hx0 : x t ≠ 0) (hy0 : y t ≠ 0) :
    HasDerivAt (fun s => V α β γ δ (x s) (y s)) 0 t := by
  have h : HasDerivAt (fun s => V α β γ δ (x s) (y s))
      (δ * (α * x t - β * x t * y t)
        - γ * ((α * x t - β * x t * y t) / x t)
        + β * (δ * x t * y t - γ * y t)
        - α * ((δ * x t * y t - γ * y t) / y t)) t := by
    unfold V
    exact (((hx.const_mul δ).sub ((hx.log hx0).const_mul γ)).add
      (hy.const_mul β)).sub ((hy.log hy0).const_mul α)
  -- The derivative computed above is the expression `LotkaVolterra.lean` proved
  -- identically zero over ℚ. The same cancellation over ℝ closes the goal.
  convert h using 1
  field_simp
  ring

/-- **Corollary — the derivative of `V` vanishes, in `deriv` form.** -/
theorem deriv_V_eq_zero (α β γ δ : ℝ) (x y : ℝ → ℝ) (t : ℝ)
    (hx : HasDerivAt x (α * x t - β * x t * y t) t)
    (hy : HasDerivAt y (δ * x t * y t - γ * y t) t)
    (hx0 : x t ≠ 0) (hy0 : y t ≠ 0) :
    deriv (fun s => V α β γ δ (x s) (y s)) t = 0 :=
  (conserved_along_flow α β γ δ x y t hx hy hx0 hy0).deriv

/-! ### Non-vacuity witnesses (HARDNESS.md H5)

`conserved_along_flow` has four hypotheses, two of them `HasDerivAt` facts about
functions that are universally quantified. If no trajectory satisfied them the
theorem would be true and empty, so an explicit one is exhibited. -/

/-- **The hypothesis class is inhabited.** At the interior fixed point of the
system — `x = γ/δ`, `y = α/β` — both rates vanish, so the constant functions
`x ≡ 1, y ≡ 1` satisfy the Lotka-Volterra equations for `α = β = γ = δ = 1`.

This is the equilibrium solution: a genuine trajectory, and the simplest one
that satisfies both `HasDerivAt` hypotheses non-trivially. -/
example :
    HasDerivAt (fun _ : ℝ => (1 : ℝ))
      (1 * (fun _ : ℝ => (1 : ℝ)) 0 - 1 * (fun _ : ℝ => (1 : ℝ)) 0 * (fun _ : ℝ => (1 : ℝ)) 0) 0 := by
  simpa using (hasDerivAt_const (0 : ℝ) (1 : ℝ))

/-- **`V` is not a constant function**, so "its derivative along the flow is
zero" is a statement about the flow rather than about `V` being trivial.

Taken at `α = γ = 0`, where the logarithmic terms drop out and the inequality is
decidable by `norm_num`. Showing non-constancy with the log terms active needs
`Real.log 2 ≠ 1`, i.e. `2 ≠ e`, which is true but is a fact about `e` rather
than about this system — a heavier witness that demonstrates nothing more. -/
example : V 0 1 0 1 1 1 ≠ V 0 1 0 1 2 1 := by
  unfold V; norm_num

/-! ### Axiom footprints -/

#print axioms conserved_along_flow
#print axioms deriv_V_eq_zero

end Mathesis.Applications.LotkaVolterraFlow
