/-
  Mathesis/Duality/SelfDual.lean — the abstract self-dual bound.

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  THE CLAIM
  ---------
  One theorem, several instances. If a product is bounded below, the larger
  factor is bounded below by the square root:

      C ≤ x·y  →  √C ≤ max x y

  `Reff(α′,R) = max(R, α′/R) ≥ √α′` (MX-A-0005) is this with `x·y = α′`. So is
  the finite-support balance behind the Donoho–Stark uncertainty principle. So
  is the Wilson EOQ lot-size bound from inventory theory. The mathematics of the
  bound is domain-free; physics enters only through *which* product is conserved.

  PROVENANCE
  ----------
  Proposed 2026-08-14 as `Mathesis.Duality.SelfDual` by an external session, with
  the note that it had not been compiled. It had not. Compiling it against
  Mathlib found two defects, both of which had shipped as `sorryAx`:

    - `eoq_lower_bound`: `field_simp` already closed the goal, so the following
      `ring` errored with "No goals to be solved";
    - `kramers_wannier_self_dual`: `Real.sinh_pos` does not exist. The lemma is
      `Real.sinh_pos_iff`.

  Both theorem *names* were nevertheless defined, with `sorryAx` in the
  footprint. This is the case HARDNESS.md H1 and CLAUDE.md exist for: the gate is
  `#print axioms`, never the absence of the word `sorry` in the source. Recorded
  as LL-17.

  WHAT THIS FILE DOES NOT CONTAIN
  -------------------------------
  Read the two renames below as load-bearing, not cosmetic.

  1. There is NO Fourier analysis here. The proposal named §B.2
     "the Donoho–Stark consequence". Donoho–Stark is the statement
     `N ≤ |supp x| · |supp x̂|` for nonzero `x` on `ℤ/N` — and that statement is
     this file's *hypothesis*, not its conclusion. What is proved is the trivial
     half. Taking the literature result as an explicit hypothesis parameter is
     exactly the prescribed way for a Tier A theorem to stand on a Tier L one
     (CLAUDE.md, MX-A-0004); naming the result after the theorem you assumed is
     not. Hence `sqrt_le_max_of_le_mul_nat`. The Fourier statement was then
     **proved** in `Duality/Uncertainty.lean` (2026-08-14), so the hypothesis is
     no longer assumed — but the rename stands, because the name should say what
     *this* theorem proves.

  2. There is NO Ising model here — no lattice, no partition function, no
     duality map. `sinh_selfDual_coupling` proves: if `sinh(2K)² = 1` and
     `K > 0`, then `K = log(1+√2)/2`. That value is Onsager's critical coupling,
     and the Kramers–Wannier argument is what makes the fixed point interesting.
     But "self-duality *locates the critical point*" needs the further premise
     that the transition is unique — Kramers–Wannier (1941) assumed it; Onsager
     (1944) proved it. That premise is absent from this file, so the physics
     reading is a separate, lower-tier claim (MX-C-0009), not this theorem.

  In both cases the mathematics the proposal shipped is correct. What was wrong
  was the *label*, which is the only part the kernel does not check.
-/

import Mathlib

namespace Mathesis.Duality

/-! ## Part A — the abstract core -/

/-- **A.1 (self-dual lower bound).** If a product is bounded below by `C`, the
larger factor is at least `√C`. The "no scale below `√α′`" phenomenon with the
physics removed. -/
theorem sqrt_le_max_of_le_mul {C x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y)
    (h : C ≤ x * y) : Real.sqrt C ≤ max x y := by
  have hmax : 0 ≤ max x y := le_max_of_le_left hx
  have h2 : C ≤ (max x y) ^ 2 := by
    calc C ≤ x * y := h
      _ ≤ max x y * max x y :=
          mul_le_mul (le_max_left x y) (le_max_right x y) hy hmax
      _ = (max x y) ^ 2 := (pow_two _).symm
  calc Real.sqrt C ≤ Real.sqrt ((max x y) ^ 2) := Real.sqrt_le_sqrt h2
    _ = max x y := Real.sqrt_sq hmax

/-- **A.2 (dual upper bound).** Symmetrically, the smaller factor is at most
`√C` when the product is at most `C`. -/
theorem min_le_sqrt_of_mul_le {C x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y)
    (h : x * y ≤ C) : min x y ≤ Real.sqrt C := by
  have hmin : 0 ≤ min x y := le_min hx hy
  have h2 : (min x y) ^ 2 ≤ C := by
    calc (min x y) ^ 2 = min x y * min x y := pow_two _
      _ ≤ x * y := mul_le_mul (min_le_left x y) (min_le_right x y) hmin hx
      _ ≤ C := h
  calc min x y = Real.sqrt ((min x y) ^ 2) := (Real.sqrt_sq hmin).symm
    _ ≤ Real.sqrt C := Real.sqrt_le_sqrt h2

/-- **A.3 (the sandwich).** An exactly conserved product pins `√C` between the
two dual factors. -/
theorem sqrt_between_duals {C x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y)
    (h : x * y = C) : min x y ≤ Real.sqrt C ∧ Real.sqrt C ≤ max x y :=
  ⟨min_le_sqrt_of_mul_le hx hy h.le, sqrt_le_max_of_le_mul hx hy h.ge⟩

/-- **A.4 (additive twin: two-term AM–GM).** The same conserved product read
additively: a total cost split into two dual terms is at least `2√(xy)`. -/
theorem two_sqrt_mul_le_add {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    2 * Real.sqrt (x * y) ≤ x + y := by
  have h1 : Real.sqrt (x * y) = Real.sqrt x * Real.sqrt y := Real.sqrt_mul hx y
  nlinarith [sq_nonneg (Real.sqrt x - Real.sqrt y), Real.sq_sqrt hx,
             Real.sq_sqrt hy, Real.sqrt_nonneg x, Real.sqrt_nonneg y]

/-- **A.5 (self-dual fixed point).** For `x > 0`, being one's own dual is exactly
being the fundamental scale. -/
theorem self_dual_fixed_point {C x : ℝ} (hC : 0 < C) (hx : 0 < x) :
    x = C / x ↔ x = Real.sqrt C := by
  constructor
  · intro h
    have h2 : x * x = C := by
      field_simp at h
      linarith
    rw [← h2, Real.sqrt_mul_self hx.le]
  · intro h
    subst h
    rw [eq_div_iff (Real.sqrt_pos.mpr hC).ne', Real.mul_self_sqrt hC.le]

/-! ## Part A′ — non-vacuity witnesses (HARDNESS.md H5, both polarities)

A bound that is never tight and a hypothesis that is never load-bearing are the
two ways a true theorem can still be worthless. Both are checked here. -/

/-- **W1 (the bound is attained).** At the self-dual point `R = √α` the
inequality of A.1 is an equality, so it cannot be weakened. -/
theorem witness_sqrt_le_max_tight : Real.sqrt 4 = max (2 : ℝ) (4 / 2) := by
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  norm_num

/-- **W2 (the bound is not an identity).** Away from the self-dual point it is
strict, so A.1 is not secretly `√C = max`. -/
theorem witness_sqrt_le_max_strict : Real.sqrt 4 < max (1 : ℝ) (4 / 1) := by
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  norm_num

/-- **W3 (negative polarity: the sign hypotheses are load-bearing).** With
`x = -1, y = -4` the product hypothesis `C ≤ x·y` holds and the conclusion is
FALSE. A.1 without `hx`/`hy` is not a weaker theorem, it is a wrong one. -/
theorem witness_sqrt_le_max_needs_nonneg :
    (4 : ℝ) ≤ (-1) * (-4) ∧ ¬(Real.sqrt 4 ≤ max (-1 : ℝ) (-4)) := by
  refine ⟨by norm_num, ?_⟩
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  norm_num

/-! ## Part B — instances -/

/-- **B.1 (dual-scale metric).** `Reff ≥ √α′` re-derived as an instance of A.1:
the conserved product is `R · (α′/R) = α′`. Independent of the bespoke proof in
`Mathesis/Scale/Reff.lean`; consolidating the two is a separate decision, since
the bespoke proof is the one Stream 5's kernel already accepted. -/
theorem Reff_ge_sqrt_of_selfDual {α R : ℝ} (hα : 0 < α) (hR : 0 < R) :
    Real.sqrt α ≤ max R (α / R) := by
  have hprod : R * (α / R) = α := by
    rw [mul_comm]; exact div_mul_cancel₀ α hR.ne'
  exact sqrt_le_max_of_le_mul hR.le (div_nonneg hα.le hR.le) hprod.ge

/-- **B.2 (support balance).** A.1 cast to naturals. Read the file header before
citing this: the Fourier content of Donoho–Stark is the hypothesis `N ≤ a * b`,
which this file does not discharge. See TARGET T-DS. -/
theorem sqrt_le_max_of_le_mul_nat {a b N : ℕ} (h : N ≤ a * b) :
    Real.sqrt (N : ℝ) ≤ max (a : ℝ) (b : ℝ) :=
  sqrt_le_max_of_le_mul (Nat.cast_nonneg a) (Nat.cast_nonneg b)
    (by exact_mod_cast h)

/-- **B.3 (Wilson EOQ lower bound).** Ordering cost `DK/Q` and holding cost
`hQ/2` have conserved product `DKh/2` independent of `Q`, so total cost is at
least `2√(DKh/2)` — an instance of A.4 that inventory theory has been running
industrially since 1913. -/
theorem eoq_lower_bound {D K h Q : ℝ}
    (hD : 0 < D) (hK : 0 < K) (hh : 0 < h) (hQ : 0 < Q) :
    2 * Real.sqrt (D * K * h / 2) ≤ D * K / Q + h * Q / 2 := by
  have hxy : (D * K / Q) * (h * Q / 2) = D * K * h / 2 := by
    field_simp
  calc 2 * Real.sqrt (D * K * h / 2)
      = 2 * Real.sqrt ((D * K / Q) * (h * Q / 2)) := by rw [hxy]
    _ ≤ D * K / Q + h * Q / 2 :=
        two_sqrt_mul_le_add (by positivity) (by positivity)

/-- **B.3′ (the EOQ bound is attained).** At the self-dual lot size
`Q* = √(2DK/h)` the bound of B.3 is an equality. This is the witness that makes
B.3 the *optimal* lot size rather than merely a true inequality — and it is the
economics counterpart of W1: the interesting quantity sits where the two dual
costs balance. -/
theorem eoq_attained {D K h : ℝ} (hD : 0 < D) (hK : 0 < K) (hh : 0 < h) :
    D * K / Real.sqrt (2 * D * K / h) + h * Real.sqrt (2 * D * K / h) / 2
      = 2 * Real.sqrt (D * K * h / 2) := by
  have hpos : (0 : ℝ) < 2 * D * K / h := by positivity
  have hs : 0 < Real.sqrt (2 * D * K / h) := Real.sqrt_pos.mpr hpos
  have hsq : Real.sqrt (2 * D * K / h) ^ 2 = 2 * D * K / h := Real.sq_sqrt hpos.le
  have hq : (0 : ℝ) < D * K * h / 2 := by positivity
  have hprod : Real.sqrt (D * K * h / 2) * Real.sqrt (2 * D * K / h) = D * K := by
    rw [← Real.sqrt_mul hq.le,
        show (D * K * h / 2) * (2 * D * K / h) = (D * K) ^ 2 by field_simp]
    exact Real.sqrt_sq (by positivity)
  have hsq' : Real.sqrt (2 * D * K / h) * Real.sqrt (2 * D * K / h) * h
      = 2 * D * K := by
    have hd : Real.sqrt (2 * D * K / h) * Real.sqrt (2 * D * K / h)
        = 2 * D * K / h := by nlinarith [hsq]
    rw [hd]; field_simp
  rw [div_add_div _ _ (ne_of_gt hs) (by norm_num : (2 : ℝ) ≠ 0),
      div_eq_iff (by positivity)]
  nlinarith [hprod, hsq']

/-! ## Part C — the self-dual coupling -/

/-- **C.1 (the self-dual coupling).** If `sinh(2K)² = 1` with `K > 0`, then
`K = log(1+√2)/2`.

The Kramers–Wannier duality of the 2-D Ising model pairs couplings by
`sinh(2K)·sinh(2K*) = 1`; setting `K* = K` gives this hypothesis, and the value
obtained is Onsager's critical coupling. **That identification is not proved
here** — see the file header. This theorem is A.5 for `sinh`, and nothing more.
-/
theorem sinh_selfDual_coupling {K : ℝ} (hK : 0 < K)
    (hfix : Real.sinh (2 * K) * Real.sinh (2 * K) = 1) :
    K = Real.log (1 + Real.sqrt 2) / 2 := by
  have hpos : 0 < Real.sinh (2 * K) := Real.sinh_pos_iff.mpr (by linarith)
  have h2 : (Real.sinh (2 * K) - 1) * (Real.sinh (2 * K) + 1) = 0 := by
    linear_combination hfix
  have h1 : Real.sinh (2 * K) = 1 := by
    rcases mul_eq_zero.mp h2 with h | h
    · linarith
    · linarith
  have h3 : 2 * K = Real.arsinh 1 := by
    have h4 := Real.arsinh_sinh (2 * K)
    rw [← h4, h1]
  have h5 : Real.arsinh 1 = Real.log (1 + Real.sqrt 2) := by
    rw [Real.arsinh]
    norm_num
  rw [h5] at h3
  linarith

/-- **W4 (C.1 is not vacuous).** The hypothesis of C.1 is satisfiable: the value
it returns does solve `sinh(2K)² = 1`. Without this, C.1 could be an implication
with an empty antecedent — true, and about nothing. This is the same check that
caught three bad witnesses in `Applications/` (LL-12). -/
theorem witness_sinh_selfDual_satisfiable :
    Real.sinh (2 * (Real.log (1 + Real.sqrt 2) / 2)) *
      Real.sinh (2 * (Real.log (1 + Real.sqrt 2) / 2)) = 1 := by
  have ha : Real.arsinh 1 = Real.log (1 + Real.sqrt 2) := by
    rw [Real.arsinh]; norm_num
  have he : 2 * (Real.log (1 + Real.sqrt 2) / 2) = Real.arsinh 1 := by
    rw [ha]; ring
  rw [he, Real.sinh_arsinh]; norm_num

/-! ## TARGETS — stated, not asserted; nothing below is axiomatised

TARGET T-DS — **DISCHARGED 2026-08-14** in `Mathesis/Duality/Uncertainty.lean`.
  `donoho_stark` proves `N ≤ |supp f| · |supp 𝓕f|` for nonzero `f : ZMod N → ℂ`,
  so B.2 may now be applied to a *proved* product bound rather than an assumed
  one, and `sqrt_le_max_support` states the resulting `√N` bound directly.
  The load-bearing step was **Parseval on `ZMod N`**, which Mathlib does not
  have; the two ingredients it does have are `AddChar.sum_mulShift` and
  `sq_sum_le_card_mul_sum_sq`. Recorded as `MX-A-0013`/`MX-A-0014`.

TARGET T-TAO (Tao 2005, `N` prime) — `|supp x| + |supp x̂| ≥ N + 1`, strictly
  stronger than Donoho–Stark on primes. Of interest here because arithmetic
  structure *hardens* a duality bound. [LL-6 retrieval pass required; the
  statement above is from memory and is not citable until a quoted theorem
  statement is on file (LL-7).]

TARGET T-KW (Kramers–Wannier as an involution) — package `K ↦ K*` with
  `sinh(2K)·sinh(2K*) = 1` as an explicit involution on `(0,∞)` and derive C.1's
  hypothesis from `K* = K`, rather than assuming it. This is the piece that would
  let C.1 legitimately carry the Kramers–Wannier name. Finite-lattice partition
  identities are Tier B and belong in the exact-arithmetic harness, not here.
-/

#print axioms sqrt_le_max_of_le_mul
#print axioms min_le_sqrt_of_mul_le
#print axioms sqrt_between_duals
#print axioms two_sqrt_mul_le_add
#print axioms self_dual_fixed_point
#print axioms witness_sqrt_le_max_tight
#print axioms witness_sqrt_le_max_strict
#print axioms witness_sqrt_le_max_needs_nonneg
#print axioms Reff_ge_sqrt_of_selfDual
#print axioms sqrt_le_max_of_le_mul_nat
#print axioms eoq_lower_bound
#print axioms eoq_attained
#print axioms sinh_selfDual_coupling
#print axioms witness_sinh_selfDual_satisfiable

end Mathesis.Duality
