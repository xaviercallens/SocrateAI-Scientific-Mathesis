/-
  Mathesis/Duality/Chebotarev.lean — towards Chebotarëv's theorem on roots of unity.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).
  PARTIAL: this file proves **Frenkel's Lemma 2 only**. Chebotarëv itself is NOT here.

  WHAT IS PROVED HERE
  -------------------
  Frenkel's Lemma 2, quoted verbatim in `docs/TARGET_CHEBOTAREV.md` (`MX-L-0001`):

    Let `0 ≢ g(x) ∈ F_p[x]` be a polynomial of degree `< p`. Then the multiplicity
    of any element `0 ≠ a ∈ F_p` as a root of `g(x)` is strictly less than the
    number of non-zero coefficients of `g(x)`.

  In Lean: `rootMultiplicity a g < g.support.card`, with `g.support.card` the
  number of non-zero coefficients.

  WHY THIS ONE FIRST
  ------------------
  It is the load-bearing combinatorial input to Frenkel's proof, it is entirely
  elementary, and it needs nothing from cyclotomic theory. So it is the cheapest
  place to discover that the cost estimate is wrong — and that estimate has now
  been wrong twice in two days, both times by my reasoning from a remembered
  proof rather than a retrieved one (`MX-C-0011`, `MX-L-0001`).

  WHAT IS NOT PROVED HERE, AND MUST NOT BE INFERRED
  -------------------------------------------------
  - **Chebotarëv's theorem itself.** That needs Lemma 1 (`ℤ[ω]/(1−ω) ≅ F_p`) and
    the infinite descent. Neither is in this file.
  - **T-TAO.** Frenkel *asserts*, attributing Tao, that Chebotarëv is equivalent
    to `|supp f| + |supp f̂| ≥ p+1`; he does not prove it. That bridge is a
    separate paper, unretrieved. Proving everything in this file and then
    Chebotarëv would still not license T-TAO (LL-7).

  WHERE `p` PRIME AND `deg g < p` ARE ACTUALLY USED
  -------------------------------------------------
  Only to know `derivative g ≠ 0`. In characteristic `p` a nonconstant polynomial
  can have vanishing derivative — `X^p` is the standard example — and the whole
  induction collapses if that happens. The hypothesis `natDegree g < p` is exactly
  what rules it out, and `witness_needs_degree_lt` exhibits the failure without it.
-/

import Mathlib

namespace Mathesis.Duality

open Polynomial Finset

variable {p : ℕ} [Fact p.Prime]

/-! ## Part A — the two combinatorial steps -/

/-- Differentiating cannot create a non-zero coefficient: every index in the
support of `derivative g` comes from a **non-zero** index in the support of `g`.
So the derivative's support is strictly smaller whenever `g.coeff 0 ≠ 0`. -/
theorem card_support_derivative_lt {R : Type*} [CommRing R] {g : R[X]}
    (h0 : g.coeff 0 ≠ 0) : (derivative g).support.card < g.support.card := by
  classical
  have hsub : (derivative g).support.image (· + 1) ⊆ g.support.erase 0 := by
    intro n hn
    simp only [Finset.mem_image, mem_support_iff] at hn
    obtain ⟨m, hm, rfl⟩ := hn
    refine Finset.mem_erase.mpr ⟨Nat.succ_ne_zero m, mem_support_iff.mpr ?_⟩
    intro hc
    exact hm (by simp [coeff_derivative, hc])
  have hinj : (derivative g).support.card
      = ((derivative g).support.image (· + 1)).card :=
    (Finset.card_image_of_injective _ (add_left_injective 1)).symm
  have h0mem : (0 : ℕ) ∈ g.support := mem_support_iff.mpr h0
  calc (derivative g).support.card
      = ((derivative g).support.image (· + 1)).card := hinj
    _ ≤ (g.support.erase 0).card := Finset.card_le_card hsub
    _ < g.support.card := Finset.card_erase_lt_of_mem h0mem

/-- Multiplying by `X` shifts the support, so the number of non-zero
coefficients is unchanged. -/
theorem card_support_X_mul {R : Type*} [CommRing R] [Nontrivial R] (h : R[X]) :
    (X * h).support.card = h.support.card := by
  classical
  have : (X * h).support = h.support.image (· + 1) := by
    ext n
    cases n with
    | zero => simp [coeff_X_mul_zero]
    | succ m =>
        simp only [mem_support_iff, coeff_X_mul, Finset.mem_image]
        constructor
        · intro hm; exact ⟨m, hm, rfl⟩
        · rintro ⟨j, hj, hje⟩
          have : j = m := by omega
          subst this
          exact hj
  rw [this, Finset.card_image_of_injective _ (add_left_injective 1)]

/-! ## Part B — the derivative is non-zero below degree `p` -/

/-- **Where the hypotheses earn their place.** For `0 < natDegree g < p` over
`ZMod p`, the derivative is non-zero: its coefficient at `natDegree g - 1` is
`leadingCoeff g * natDegree g`, and `natDegree g` is invertible mod `p` precisely
because `0 < natDegree g < p`. -/
theorem derivative_ne_zero_of_natDegree_lt {g : (ZMod p)[X]}
    (hpos : 0 < g.natDegree) (hlt : g.natDegree < p) : derivative g ≠ 0 := by
  intro hzero
  obtain ⟨m, hm⟩ : ∃ m, g.natDegree = m + 1 := ⟨g.natDegree - 1, by omega⟩
  have hg : g ≠ 0 := fun h => by simp [h] at hpos
  have hlead : g.coeff g.natDegree ≠ 0 := Polynomial.leadingCoeff_ne_zero.mpr hg
  have hn : ((m + 1 : ℕ) : ZMod p) ≠ 0 := by
    rw [Ne, ZMod.natCast_eq_zero_iff]
    intro hdvd
    have := Nat.le_of_dvd (by omega) hdvd
    omega
  have hcoeff : (derivative g).coeff m = g.coeff (m + 1) * ((m + 1 : ℕ) : ZMod p) := by
    rw [coeff_derivative]; push_cast; ring
  rw [hzero, Polynomial.coeff_zero] at hcoeff
  rw [hm] at hlead
  exact (mul_ne_zero hlead hn) hcoeff.symm

/-! ## Part C — Frenkel's Lemma 2 -/

/-- **Frenkel's Lemma 2.** For `g ≠ 0` in `F_p[X]` of degree `< p` and `a ≠ 0`,
the multiplicity of `a` as a root of `g` is **strictly less** than the number of
non-zero coefficients of `g`.

The induction is on `natDegree g`, splitting on whether `g.coeff 0` vanishes:

- if it does, `g = X * h` and both quantities are unchanged (`a ≠ 0` is what makes
  the multiplicity survive the factor `X`);
- if it does not, the derivative has strictly fewer non-zero coefficients, while
  the multiplicity drops by at most one. -/
theorem rootMultiplicity_lt_card_support :
    ∀ (n : ℕ) (g : (ZMod p)[X]), g.natDegree = n → g ≠ 0 → g.natDegree < p →
      ∀ a : ZMod p, a ≠ 0 → g.rootMultiplicity a < g.support.card := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro g hn hg hdeg a ha
    rcases Nat.eq_zero_or_pos n with hzero | hpos
    · -- constant: `a` is not a root at all
      subst hn
      have hc : g = C (g.coeff 0) := Polynomial.eq_C_of_natDegree_eq_zero hzero
      have hne : g.eval a ≠ 0 := by
        rw [hc]
        simpa using fun h => hg (by rw [hc, h, map_zero])
      have : g.rootMultiplicity a = 0 :=
        Polynomial.rootMultiplicity_eq_zero (fun hr => hne hr)
      rw [this]
      exact Finset.card_pos.mpr ⟨g.natDegree, mem_support_iff.mpr
        (Polynomial.leadingCoeff_ne_zero.mpr hg)⟩
    by_cases h0 : g.coeff 0 = 0
    · -- `X ∣ g`; peel it off
      obtain ⟨h, rfl⟩ := Polynomial.X_dvd_iff.mpr h0
      have hh : h ≠ 0 := fun hc => hg (by rw [hc, mul_zero])
      have hXh : (X : (ZMod p)[X]) * h ≠ 0 := hg
      have hdegh : h.natDegree < p := by
        have := Polynomial.natDegree_X_mul (p := h) hh
        omega
      have hlt : h.natDegree < n := by
        have := Polynomial.natDegree_X_mul (p := h) hh
        omega
      have hrec := ih h.natDegree hlt h rfl hh hdegh a ha
      have hmul : (X * h).rootMultiplicity a = h.rootMultiplicity a := by
        rw [Polynomial.rootMultiplicity_mul hXh]
        have : (X : (ZMod p)[X]).rootMultiplicity a = 0 :=
          Polynomial.rootMultiplicity_eq_zero (by simpa [Polynomial.IsRoot] using ha)
        omega
      rw [hmul, card_support_X_mul h]
      exact hrec
    · -- differentiate
      have hd0 : derivative g ≠ 0 :=
        derivative_ne_zero_of_natDegree_lt (by omega) hdeg
      have hdlt : (derivative g).natDegree < n := by
        have := Polynomial.natDegree_derivative_lt (p := g) (by omega)
        omega
      have hddeg : (derivative g).natDegree < p := by omega
      have hrec := ih (derivative g).natDegree hdlt (derivative g) rfl hd0 hddeg a ha
      have hmult : g.rootMultiplicity a - 1 ≤ (derivative g).rootMultiplicity a :=
        rootMultiplicity_sub_one_le_derivative_rootMultiplicity_of_ne_zero g a hd0
      have hcard : (derivative g).support.card < g.support.card :=
        card_support_derivative_lt h0
      omega

/-- The statement in the form Frenkel writes it. -/
theorem frenkel_lemma_two {g : (ZMod p)[X]} (hg : g ≠ 0) (hdeg : g.natDegree < p)
    {a : ZMod p} (ha : a ≠ 0) : g.rootMultiplicity a < g.support.card :=
  rootMultiplicity_lt_card_support g.natDegree g rfl hg hdeg a ha

/-! ## Part D — non-vacuity witnesses (HARDNESS.md H5, both polarities) -/

/-- Needed as a global instance, not a local `have`: instances derived from a
local hypothesis carry a free variable, and `decide` then refuses the goal. -/
private instance factPrimeFive : Fact (Nat.Prime 5) := ⟨by norm_num⟩

/-- **W1 (the bound is attained).** `g = X - 1` over `F_5` has one simple root at
`a = 1` and two non-zero coefficients: `1 < 2`. So the inequality is tight and
cannot be strengthened to a gap of two. -/
theorem witness_lemma_two_tight :
    (X - 1 : (ZMod 5)[X]).rootMultiplicity 1 = 1 ∧
      (X - 1 : (ZMod 5)[X]).support.card = 2 := by
  have hb : (X - 1 : (ZMod 5)[X])
      = C (-1 : ZMod 5) * X ^ 0 + C (1 : ZMod 5) * X ^ 1 := by
    simp; ring
  refine ⟨?_, ?_⟩
  · rw [show (X - 1 : (ZMod 5)[X]) = X - C 1 by simp,
      Polynomial.rootMultiplicity_X_sub_C_self]
  · rw [hb]
    exact Polynomial.card_support_binomial (by norm_num)
      (by decide : (-1 : ZMod 5) ≠ 0) (by decide : (1 : ZMod 5) ≠ 0)

/-- **W2 (negative polarity: `deg g < p` is load-bearing).** Over `F_5`,
`g = X^5 - 1 = (X - 1)^5` has `derivative g = 0`, root multiplicity `5` at
`a = 1`, and only **two** non-zero coefficients. The conclusion `5 < 2` is false.

This is not a corner case: it is the reason the hypothesis exists. In
characteristic `p` a nonconstant polynomial may have vanishing derivative, and
the induction in Part C has nothing left to descend on. -/
theorem witness_needs_degree_lt :
    derivative (X ^ 5 - 1 : (ZMod 5)[X]) = 0 ∧
      ¬((X ^ 5 - 1 : (ZMod 5)[X]).rootMultiplicity 1
          < (X ^ 5 - 1 : (ZMod 5)[X]).support.card) := by
  have hfact : (X ^ 5 - 1 : (ZMod 5)[X]) = (X - C 1) ^ 5 := by
    rw [sub_pow_char]
    simp
  refine ⟨?_, ?_⟩
  · rw [hfact]
    simp only [derivative_pow, derivative_sub, derivative_X, derivative_C, sub_zero,
      mul_one]
    rw [show ((5 : ℕ) : ZMod 5) = 0 by decide, map_zero, zero_mul]
  · have hmult : (X ^ 5 - 1 : (ZMod 5)[X]).rootMultiplicity 1 = 5 := by
      rw [hfact, Polynomial.rootMultiplicity_X_sub_C_pow]
    have hsupp : (X ^ 5 - 1 : (ZMod 5)[X]).support.card = 2 := by
      rw [show (X ^ 5 - 1 : (ZMod 5)[X])
          = C (-1 : ZMod 5) * X ^ 0 + C (1 : ZMod 5) * X ^ 5 by simp; ring]
      exact Polynomial.card_support_binomial (by norm_num)
        (by decide : (-1 : ZMod 5) ≠ 0) (by decide : (1 : ZMod 5) ≠ 0)
    rw [hmult, hsupp]
    omega

#print axioms card_support_derivative_lt
#print axioms card_support_X_mul
#print axioms derivative_ne_zero_of_natDegree_lt
#print axioms rootMultiplicity_lt_card_support
#print axioms frenkel_lemma_two
#print axioms witness_lemma_two_tight
#print axioms witness_needs_degree_lt

end Mathesis.Duality
