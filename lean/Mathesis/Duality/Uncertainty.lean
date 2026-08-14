/-
  Mathesis/Duality/Uncertainty.lean — Parseval and Donoho–Stark on `ZMod N`.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  WHAT THIS DISCHARGES
  --------------------
  `Duality/SelfDual.lean` proves `N ≤ a·b → √N ≤ max a b` and calls it
  `sqrt_le_max_of_le_mul_nat`, with a header saying flatly that the Fourier
  content — the hypothesis `N ≤ a·b` — was **not** proved and was recorded as
  TARGET T-DS. This file proves it. `sqrt_le_max_of_le_mul_nat` may now be
  applied to a discharged hypothesis rather than an assumed one.

  WHY IT WAS NOT A CITATION
  -------------------------
  Mathlib has the discrete Fourier transform on `ZMod N` (`ZMod.dft`) but, as of
  the tree Stream 0 resolves, **no Parseval or Plancherel identity for it** —
  `Mathlib/Analysis/Fourier/ZMod.lean` contains no norm or inner-product lemma at
  all, and the Parseval results that do exist are for `AddCircle` and the
  continuous transform. So `dft_parseval` below is not a wrapper around a library
  result; it is the missing step, built from character orthogonality
  (`AddChar.sum_mulShift`, which Mathlib does have).

  Checked before estimating, per MX-C-0005: `Analysis/Fourier/ZMod.olean` and
  `Analysis/Fourier/FiniteAbelian/Orthogonality.olean` are **built** in the
  resolved environment. A missing module and a false statement report
  identically, so this is verified rather than assumed.

  THE STATEMENT, AND WHAT IT IS NOT
  ---------------------------------
  For `f ≠ 0` on `ZMod N`,

      N ≤ |supp f| · |supp (𝓕 f)|

  A signal and its spectrum cannot both be concentrated: their supports have
  product at least `N`. Combined with `sqrt_le_max_of_le_mul_nat`, the larger
  support is at least `√N` — which is the self-dual bound of `SelfDual.lean` A.1
  with `C = N`, and the reason this file lives beside it.

  This is a theorem about `ZMod N` and finite sums. It says **nothing** about
  quantum mechanics, about the Heisenberg uncertainty principle, or about
  measurement. The shared name is an analogy between two inequalities, and this
  file does not license transporting one to the other. See LL-17 on names.

  NOT PROVED HERE: Tao's refinement for `N` prime, `|supp f| + |supp 𝓕f| ≥ N+1`.
  It is strictly stronger on primes and is left as TARGET T-TAO in `SelfDual`.
-/

import Mathlib

namespace Mathesis.Duality

open Finset

variable {N : ℕ} [NeZero N]

/-! ## Part A — the two ingredients -/

/-- The standard additive character is unimodular, so conjugation negates it. -/
theorem conj_stdAddChar (j : ZMod N) :
    (starRingEnd ℂ) (ZMod.stdAddChar j) = ZMod.stdAddChar (-j) := by
  simp [ZMod.stdAddChar_apply, ← Circle.coe_inv_eq_conj, AddChar.map_neg_eq_inv]

/-- **Character orthogonality on `ZMod N`.** The character sum is `N` at `b = 0`
and vanishes otherwise. This is Mathlib's `AddChar.sum_mulShift` specialised to
the standard character, whose primitivity Mathlib also provides. -/
theorem sum_stdAddChar (b : ZMod N) :
    ∑ k : ZMod N, ZMod.stdAddChar (k * b) = if b = 0 then (N : ℂ) else 0 := by
  have h := AddChar.sum_mulShift b (ZMod.isPrimitive_stdAddChar N)
  simpa [ZMod.card] using h

/-- Expanding `|𝓕f(k)|²` as a double sum over the group. The character identity
`χ(-(jk))·χ(lk) = χ(k(l−j))` is what turns the product into a single character
evaluated at a difference — which is what orthogonality can then collapse. -/
theorem dft_mul_conj_expand (f : ZMod N → ℂ) (k : ZMod N) :
    ZMod.dft f k * (starRingEnd ℂ) (ZMod.dft f k)
      = ∑ j : ZMod N, ∑ l : ZMod N,
          ZMod.stdAddChar (k * (l - j)) * (f j * (starRingEnd ℂ) (f l)) := by
  simp only [ZMod.dft_apply, smul_eq_mul, map_sum, map_mul, conj_stdAddChar, neg_neg]
  rw [Finset.sum_mul_sum]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun l _ => ?_
  have hchar : ZMod.stdAddChar (-(j * k)) * ZMod.stdAddChar (l * k)
      = ZMod.stdAddChar (k * (l - j)) := by
    rw [← AddChar.map_add_eq_mul]; congr 1; ring
  rw [← hchar]; ring

/-! ## Part B — Parseval

Mathlib does not have this for `ZMod.dft`. It is the load-bearing step. -/

/-- **Parseval on `ZMod N`.** `∑ₖ 𝓕f(k)·conj(𝓕f(k)) = N · ∑ⱼ f(j)·conj(f(j))`.

The factor `N` (rather than `1`) is the unnormalised convention `ZMod.dft` uses;
it is what makes the Donoho–Stark bound `N` rather than `1`. -/
theorem dft_parseval (f : ZMod N → ℂ) :
    ∑ k : ZMod N, ZMod.dft f k * (starRingEnd ℂ) (ZMod.dft f k)
      = (N : ℂ) * ∑ j : ZMod N, f j * (starRingEnd ℂ) (f j) := by
  classical
  simp only [dft_mul_conj_expand]
  rw [Finset.mul_sum, Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Finset.sum_comm]
  have step : ∀ l : ZMod N,
      ∑ k : ZMod N, ZMod.stdAddChar (k * (l - j)) * (f j * (starRingEnd ℂ) (f l))
        = (if l - j = 0 then (N : ℂ) else 0) * (f j * (starRingEnd ℂ) (f l)) := by
    intro l; rw [← Finset.sum_mul, sum_stdAddChar]
  simp only [step, sub_eq_zero, ite_mul, zero_mul]
  rw [Finset.sum_ite_eq' Finset.univ j
    (fun l => (N : ℂ) * (f j * (starRingEnd ℂ) (f l)))]
  simp

/-- Parseval in real norms, which is the form the estimate uses. -/
theorem dft_parseval_norm (f : ZMod N → ℂ) :
    ∑ k : ZMod N, ‖ZMod.dft f k‖ ^ 2 = (N : ℝ) * ∑ j : ZMod N, ‖f j‖ ^ 2 := by
  have h := dft_parseval f
  simp only [Complex.mul_conj] at h
  have hcast : ((∑ k : ZMod N, Complex.normSq (ZMod.dft f k) : ℝ) : ℂ)
      = (((N : ℝ) * ∑ j : ZMod N, Complex.normSq (f j) : ℝ) : ℂ) := by
    push_cast
    exact h
  have := Complex.ofReal_inj.mp hcast
  simpa [Complex.normSq_eq_norm_sq] using this

/-! ## Part C — Donoho–Stark -/

/-- Every Fourier coefficient is bounded by the support size times the energy.
Cauchy–Schwarz over the support: a signal supported on few points cannot have a
large transform anywhere. -/
theorem norm_dft_sq_le (f : ZMod N → ℂ) (k : ZMod N) :
    ‖ZMod.dft f k‖ ^ 2
      ≤ ((univ.filter fun j : ZMod N => f j ≠ 0).card : ℝ)
          * ∑ j : ZMod N, ‖f j‖ ^ 2 := by
  classical
  set S := univ.filter fun j : ZMod N => f j ≠ 0 with hSdef
  have hzero : ∀ j ∈ univ, j ∉ S → ‖f j‖ = 0 := by
    intro j _ hj
    simp only [hSdef, mem_filter, mem_univ, true_and, not_not] at hj
    simp [hj]
  have hsum : ∑ j : ZMod N, ‖f j‖ = ∑ j ∈ S, ‖f j‖ :=
    (Finset.sum_subset (filter_subset _ _) hzero).symm
  have hsq : ∑ j : ZMod N, ‖f j‖ ^ 2 = ∑ j ∈ S, ‖f j‖ ^ 2 :=
    (Finset.sum_subset (filter_subset _ _)
      (fun j hj hjs => by rw [hzero j hj hjs]; ring)).symm
  have hb : ‖ZMod.dft f k‖ ≤ ∑ j ∈ S, ‖f j‖ := by
    rw [← hsum, ZMod.dft_apply]
    refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun j _ => ?_)
    rw [smul_eq_mul, norm_mul, ZMod.stdAddChar_apply, Circle.norm_coe, one_mul]
  calc ‖ZMod.dft f k‖ ^ 2 ≤ (∑ j ∈ S, ‖f j‖) ^ 2 := by
        exact pow_le_pow_left₀ (norm_nonneg _) hb 2
    _ ≤ (S.card : ℝ) * ∑ j ∈ S, ‖f j‖ ^ 2 := sq_sum_le_card_mul_sum_sq
    _ = (S.card : ℝ) * ∑ j : ZMod N, ‖f j‖ ^ 2 := by rw [hsq]

/-- **The Donoho–Stark uncertainty principle on `ZMod N`.**

For a nonzero `f`, the supports of `f` and of its discrete Fourier transform
satisfy `N ≤ |supp f| · |supp 𝓕f|`. A signal and its spectrum cannot both be
concentrated.

This discharges TARGET T-DS and, with `sqrt_le_max_of_le_mul_nat`, gives
`√N ≤ max |supp f| |supp 𝓕f|` — the self-dual bound with `C = N`. -/
theorem donoho_stark (f : ZMod N → ℂ) (hf : f ≠ 0) :
    N ≤ (univ.filter fun j : ZMod N => f j ≠ 0).card
        * (univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0).card := by
  classical
  set S := univ.filter fun j : ZMod N => f j ≠ 0 with hSdef
  set T := univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0 with hTdef
  set E := ∑ j : ZMod N, ‖f j‖ ^ 2 with hEdef
  -- the energy is positive, which is where `f ≠ 0` is used
  have hEpos : 0 < E := by
    obtain ⟨j₀, hj₀⟩ := Function.ne_iff.mp hf
    refine Finset.sum_pos' (fun j _ => by positivity) ⟨j₀, mem_univ j₀, ?_⟩
    have : ‖f j₀‖ ≠ 0 := by simpa using hj₀
    positivity
  -- off the spectral support the summand vanishes
  have hTzero : ∀ k ∈ univ, k ∉ T → ‖ZMod.dft f k‖ ^ 2 = 0 := by
    intro k _ hk
    simp only [hTdef, mem_filter, mem_univ, true_and, not_not] at hk
    simp [hk]
  have hTsum : ∑ k : ZMod N, ‖ZMod.dft f k‖ ^ 2 = ∑ k ∈ T, ‖ZMod.dft f k‖ ^ 2 :=
    (Finset.sum_subset (filter_subset _ _) hTzero).symm
  -- N · E = ‖𝓕f‖² ≤ |T| · (|S| · E)
  have hchain : (N : ℝ) * E ≤ (T.card : ℝ) * ((S.card : ℝ) * E) := by
    rw [← dft_parseval_norm f, hTsum]
    calc ∑ k ∈ T, ‖ZMod.dft f k‖ ^ 2
        ≤ ∑ _k ∈ T, (S.card : ℝ) * E :=
          Finset.sum_le_sum fun k _ => norm_dft_sq_le f k
      _ = (T.card : ℝ) * ((S.card : ℝ) * E) := by
          rw [Finset.sum_const, nsmul_eq_mul]
  have hfinal : (N : ℝ) ≤ (S.card : ℝ) * (T.card : ℝ) := by nlinarith
  exact_mod_cast hfinal

/-! ## Part C′ — the payoff: T-DS meets the self-dual bound -/

/-- **The larger support is at least `√N`.**

This is `SelfDual.lean` A.1 with `C = N`, applied to a hypothesis that is now
**proved** rather than assumed — which is the whole point of this file. Before
it, `sqrt_le_max_of_le_mul_nat` could only be applied to a product bound
somebody else had to supply.

The two-line proof is repeated here rather than imported: Stream 0's Lean
modules are compiled standalone by Gate 2 (`lake env lean <file>`), with no
lakefile, so there is no cross-module import. The duplication is deliberate and
is the same trade `Scale/Reff.lean` makes. -/
theorem sqrt_le_max_support (f : ZMod N → ℂ) (hf : f ≠ 0) :
    Real.sqrt (N : ℝ)
      ≤ max ((univ.filter fun j : ZMod N => f j ≠ 0).card : ℝ)
            ((univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0).card : ℝ) := by
  have h : (N : ℝ)
      ≤ ((univ.filter fun j : ZMod N => f j ≠ 0).card : ℝ)
        * ((univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0).card : ℝ) := by
    exact_mod_cast donoho_stark f hf
  have hmax : (0 : ℝ) ≤ max ((univ.filter fun j : ZMod N => f j ≠ 0).card : ℝ)
      ((univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0).card : ℝ) :=
    le_max_of_le_left (Nat.cast_nonneg _)
  have h2 : (N : ℝ) ≤ (max ((univ.filter fun j : ZMod N => f j ≠ 0).card : ℝ)
      ((univ.filter fun k : ZMod N => ZMod.dft f k ≠ 0).card : ℝ)) ^ 2 := by
    refine le_trans h ?_
    rw [pow_two]
    exact mul_le_mul (le_max_left _ _) (le_max_right _ _) (Nat.cast_nonneg _) hmax
  calc Real.sqrt (N : ℝ) ≤ Real.sqrt (_ ^ 2) := Real.sqrt_le_sqrt h2
    _ = _ := Real.sqrt_sq hmax

/-! ## Part D — non-vacuity witnesses (HARDNESS.md H5) -/

/-- **W1 (the hypothesis is load-bearing).** For `f = 0` the conclusion is false:
both supports are empty, so the product is `0 < N`. Donoho–Stark without
`f ≠ 0` is not a weaker theorem, it is a wrong one. -/
theorem witness_donoho_stark_needs_ne_zero (hN : 0 < N) :
    ¬(N ≤ (univ.filter fun j : ZMod N => (0 : ZMod N → ℂ) j ≠ 0).card
          * (univ.filter fun k : ZMod N => ZMod.dft (0 : ZMod N → ℂ) k ≠ 0).card) := by
  classical
  have h1 : (univ.filter fun j : ZMod N => (0 : ZMod N → ℂ) j ≠ 0) = ∅ := by
    ext j; simp
  have h2 : (univ.filter fun k : ZMod N => ZMod.dft (0 : ZMod N → ℂ) k ≠ 0) = ∅ := by
    ext k; simp
  rw [h1, h2, card_empty, Nat.zero_mul]
  omega

/-- **W2 (the bound is attained).** At `N = 1` the only nonzero `f` has
`|supp f| = |supp 𝓕f| = 1`, so `N = 1 = 1·1` and the inequality is an equality.
The bound therefore cannot be improved in general. -/
theorem witness_donoho_stark_tight (f : ZMod 1 → ℂ) (hf : f ≠ 0) :
    (univ.filter fun j : ZMod 1 => f j ≠ 0).card
      * (univ.filter fun k : ZMod 1 => ZMod.dft f k ≠ 0).card = 1 := by
  classical
  have h := donoho_stark f hf
  have hle : (univ.filter fun j : ZMod 1 => f j ≠ 0).card
      * (univ.filter fun k : ZMod 1 => ZMod.dft f k ≠ 0).card ≤ 1 := by
    calc _ ≤ (univ : Finset (ZMod 1)).card * (univ : Finset (ZMod 1)).card :=
          Nat.mul_le_mul (card_filter_le _ _) (card_filter_le _ _)
      _ = 1 := by simp
  omega

#print axioms conj_stdAddChar
#print axioms sum_stdAddChar
#print axioms dft_mul_conj_expand
#print axioms dft_parseval
#print axioms dft_parseval_norm
#print axioms norm_dft_sq_le
#print axioms donoho_stark
#print axioms sqrt_le_max_support
#print axioms witness_donoho_stark_needs_ne_zero
#print axioms witness_donoho_stark_tight

end Mathesis.Duality
