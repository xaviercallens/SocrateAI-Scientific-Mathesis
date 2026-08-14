/-
  Mathesis/Applications/Winding.lean — phase winding around a discrete loop.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  WHAT THIS IS, AND WHAT IT IS NOT
  --------------------------------
  Staged here as the Tier A core of the intended `QF-A-0001` (quantized
  circulation) before the QuantumFluids stream exists. Read the split before
  citing it, because it is the whole point:

    - **This file** proves a theorem about complex numbers: for a nonvanishing
      `ψ` on a cyclic loop, the principal phase increments around the loop sum
      to an integer multiple of `2π`. No physics, no fluid, no `ħ`.
    - **`QF-C-0001`** will be the reading that `ψ` is a superfluid order
      parameter and that `∮v·dl = n·h/m` follows. That is a *world* claim about
      whether a fluid is described by this model, it is Tier C, and it does not
      belong inside a Tier A statement (`docs/NEW_STREAM.md`, the M/W split).

  Naming this file `Circulation.lean` would have been the LL-17 error committed
  on purpose: a theorem named for the physics it does not contain.

  WHY THE DISCRETE FORM
  ---------------------
  A loop is modelled as `ZMod L` — cyclicity is then definitional rather than a
  wraparound condition to be stated and got wrong. Each increment is
  `arg (ψ(k+1) / ψ k)`, the principal value, which is what a simulation actually
  computes site-to-site. The integer is not put in by hand: it appears because
  the increments telescope to `1` and `exp` is `2πi`-periodic.

  WHY THE HYPOTHESIS IS THE PHYSICS
  ---------------------------------
  `∀ k, ψ k ≠ 0` is load-bearing — `witness_needs_nonvanishing` exhibits a loop
  with a zero on which the conclusion fails. Under the intended reading, that
  hypothesis failing *is* a vortex core, and the witness is the statement that a
  core has finite size. The side condition is not bookkeeping.
-/

import Mathlib

namespace Mathesis.Applications

open Finset

variable {L : ℕ} [NeZero L]

/-! ## Part A — the telescoping product -/

/-- Shifting the index around a cyclic loop does not change the product:
`k ↦ k + 1` is a bijection of `ZMod L`. -/
theorem prod_shift (ψ : ZMod L → ℂ) :
    ∏ k : ZMod L, ψ (k + 1) = ∏ k : ZMod L, ψ k :=
  Fintype.prod_equiv (Equiv.addRight (1 : ZMod L)) _ _ (fun _ => rfl)

/-- The consecutive ratios around a loop multiply to `1`. This is where
"the loop closes" enters, and it is the only place it does. -/
theorem prod_ratio_eq_one (ψ : ZMod L → ℂ) (hψ : ∀ k, ψ k ≠ 0) :
    ∏ k : ZMod L, (ψ (k + 1) / ψ k) = 1 := by
  rw [Finset.prod_div_distrib, prod_shift]
  exact div_self (Finset.prod_ne_zero_iff.mpr fun k _ => hψ k)

/-! ## Part B — the winding number is an integer -/

/-- **Phase winding is quantized.**

For a nonvanishing `ψ` on the cyclic loop `ZMod L`, the principal phase
increments `arg (ψ(k+1) / ψ k)` sum to `2π` times an **integer**.

The integer is not assumed. It arises because the increments exponentiate to a
product that telescopes to `1`, and `exp θi = 1` forces `θ ∈ 2πℤ`. -/
theorem winding_is_integer (ψ : ZMod L → ℂ) (hψ : ∀ k, ψ k ≠ 0) :
    ∃ n : ℤ, ∑ k : ZMod L, Complex.arg (ψ (k + 1) / ψ k) = 2 * Real.pi * n := by
  have hne : ∀ k : ZMod L, ψ (k + 1) / ψ k ≠ 0 := fun k =>
    div_ne_zero (hψ (k + 1)) (hψ k)
  -- each increment exponentiates to the unit-modulus part of the ratio
  have hexp : ∀ k : ZMod L,
      Complex.exp ((Complex.arg (ψ (k + 1) / ψ k) : ℂ) * Complex.I)
        = (ψ (k + 1) / ψ k) / (‖ψ (k + 1) / ψ k‖ : ℂ) := by
    intro k
    have hz : ((‖ψ (k + 1) / ψ k‖ : ℝ) : ℂ) ≠ 0 := by
      simpa [Complex.ofReal_ne_zero, norm_ne_zero_iff] using hne k
    rw [eq_div_iff hz, mul_comm]
    exact Complex.norm_mul_exp_arg_mul_I _
  -- the product of those unit parts is 1
  have hprod : ∏ k : ZMod L,
      ((ψ (k + 1) / ψ k) / (‖ψ (k + 1) / ψ k‖ : ℂ)) = 1 := by
    rw [Finset.prod_div_distrib, prod_ratio_eq_one ψ hψ]
    have hn : ∏ k : ZMod L, ((‖ψ (k + 1) / ψ k‖ : ℝ) : ℂ)
        = ((‖∏ k : ZMod L, (ψ (k + 1) / ψ k)‖ : ℝ) : ℂ) := by
      rw [← Complex.ofReal_prod, ← norm_prod]
    rw [hn, prod_ratio_eq_one ψ hψ]
    norm_num
  -- so the summed phase exponentiates to 1
  have hsum : Complex.exp
      (((∑ k : ZMod L, Complex.arg (ψ (k + 1) / ψ k) : ℝ) : ℂ) * Complex.I) = 1 := by
    rw [show (((∑ k : ZMod L, Complex.arg (ψ (k + 1) / ψ k) : ℝ) : ℂ) * Complex.I)
        = ∑ k : ZMod L, ((Complex.arg (ψ (k + 1) / ψ k) : ℂ) * Complex.I) by
      push_cast; rw [Finset.sum_mul]]
    rw [Complex.exp_sum]
    simp only [hexp]
    exact hprod
  obtain ⟨n, hn⟩ := Complex.exp_eq_one_iff.mp hsum
  refine ⟨n, ?_⟩
  have hcancel : ((∑ k : ZMod L, Complex.arg (ψ (k + 1) / ψ k) : ℝ) : ℂ)
      = ((2 * Real.pi * n : ℝ) : ℂ) := by
    apply mul_right_cancel₀ Complex.I_ne_zero
    rw [hn]; push_cast; ring
  exact_mod_cast hcancel

/-! ## Part C — non-vacuity witnesses (HARDNESS.md H5, both polarities) -/

/-- A four-site loop carrying the phases `1, i, −1, −i`. Nonvanishing. -/
def full4 : ZMod 4 → ℂ :=
  fun k => if k = 0 then 1 else if k = 1 then Complex.I else if k = 2 then -1
           else -Complex.I

/-- **The same loop with one site emptied.** Only `full4 2 = -1` is replaced by
`0`; every other site is identical. The pair is deliberately minimal so that W1
and W2 differ in exactly one amplitude. -/
def hole4 : ZMod 4 → ℂ :=
  fun k => if k = 0 then 1 else if k = 1 then Complex.I else if k = 2 then 0
           else -Complex.I

/-- **W1 (the winding can be nonzero).** Every increment of `full4` is exactly
`i`, contributing `π/2`, and the total is `2π` — winding number **1**.

Without this the theorem could hold vacuously with `n = 0` always, and the word
"quantized" would be describing nothing. -/
theorem witness_winding_one :
    ∑ k : ZMod 4, Complex.arg (full4 (k + 1) / full4 k) = 2 * Real.pi * (1 : ℤ) := by
  have huniv : (Finset.univ : Finset (ZMod 4)) = {0, 1, 2, 3} := by decide
  rw [huniv]
  simp +decide [full4, Complex.arg_I]
  ring

/-- **W2 (negative polarity: nonvanishing is load-bearing).** Zeroing that one
site makes two increments `arg 0 = 0` (Lean's `z / 0 = 0` makes this concrete
rather than undefined), and the total collapses to `π` — **not** an integer
multiple of `2π`. The conclusion genuinely fails without `hψ`, so the hypothesis
is not bookkeeping.

Under the intended physical reading the vanishing site is a vortex core, and
this witness is the statement that a core has finite size. -/
theorem witness_hole_sum :
    ∑ k : ZMod 4, Complex.arg (hole4 (k + 1) / hole4 k) = Real.pi := by
  have huniv : (Finset.univ : Finset (ZMod 4)) = {0, 1, 2, 3} := by decide
  rw [huniv]
  simp +decide [hole4, Complex.arg_I]

/-- **W2 (conclusion).** With the hole, no integer works. -/
theorem witness_needs_nonvanishing :
    ¬∃ n : ℤ, ∑ k : ZMod 4,
      Complex.arg (hole4 (k + 1) / hole4 k) = 2 * Real.pi * n := by
  rintro ⟨n, hn⟩
  rw [witness_hole_sum] at hn
  have hpi : (0 : ℝ) < Real.pi := Real.pi_pos
  have h1 : (1 : ℝ) = 2 * (n : ℝ) := by
    have h2 : Real.pi * 1 = Real.pi * (2 * (n : ℝ)) := by linarith [hn]
    exact mul_left_cancel₀ (ne_of_gt hpi) h2
  have h3 : (1 : ℤ) = 2 * n := by exact_mod_cast h1
  omega

#print axioms prod_shift
#print axioms prod_ratio_eq_one
#print axioms winding_is_integer
#print axioms witness_winding_one
#print axioms witness_hole_sum
#print axioms witness_needs_nonvanishing

end Mathesis.Applications
