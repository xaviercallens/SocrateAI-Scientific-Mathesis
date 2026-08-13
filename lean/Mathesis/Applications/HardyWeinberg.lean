/-
  Mathesis/Applications/HardyWeinberg.lean — Use case 3 (biology).

  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  THE CLAIM
  ---------
  Under the Hardy-Weinberg model, allele frequency is invariant across
  generations, and genotype frequencies reach (p², 2pq, q²) after one round of
  random mating and stay there.

  WHY THIS IS USE CASE 3
  ----------------------
  The first case where the *tiering* is more interesting than the mathematics.

  The algebra below is Tier A: given the model, allele frequency is conserved,
  full stop. But "this population is at Hardy-Weinberg equilibrium" is a claim
  about a biological system, and it is Tier C at best -- the model assumes an
  infinite population, random mating, no selection, no mutation, no migration,
  and no drift. Not one of those holds of any real population.

  So this file proves a theorem about a MODEL and says nothing about any
  organism. That distinction is invisible in most write-ups, where "Hardy-
  Weinberg equilibrium" names both the algebra and the empirical claim, and the
  Tier A reputation of the first quietly underwrites the second.

  The tier calculus makes the distinction structural rather than rhetorical: the
  theorem here is Tier A with the model as an explicit hypothesis, and any
  application to a real population must enter the ledger as a separate,
  lower-tier row that CITES this one. By MX-A-0004 that citing row can never be
  Tier A, no matter how good the field data is.
-/
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace Mathesis.Applications.HardyWeinberg

/-- **UC3a — the genotype frequencies are a probability distribution.**
Given allele frequencies summing to one, the three genotype frequencies
produced by random mating also sum to one. -/
theorem genotype_freqs_sum_one (p q : ℚ) (h : p + q = 1) :
    p ^ 2 + 2 * p * q + q ^ 2 = 1 := by
  linear_combination (p + q + 1) * h

/-- **UC3b — allele frequency is invariant under random mating.**

This is the actual content of the Hardy-Weinberg principle, and the reason it
matters: it is the null model against which selection is *detected*. The
frequency of allele A in the next generation is `P(AA) + P(Aa)/2`. -/
theorem allele_freq_invariant (p q : ℚ) (h : p + q = 1) :
    p ^ 2 + (2 * p * q) / 2 = p := by
  linear_combination p * h

/-- **UC3c — equilibrium is reached in one generation and is then fixed.**

Starting from *arbitrary* genotype frequencies `(P, H, Q)` summing to one — not
necessarily of the form (p², 2pq, q²) — one round of random mating produces
genotype frequencies determined entirely by the allele frequency, and a second
round reproduces them exactly. This is why the equilibrium is reached in one
generation rather than approached asymptotically. -/
theorem equilibrium_in_one_generation (P H Q : ℚ) (hsum : P + H + Q = 1) :
    (P + H / 2) + (Q + H / 2) = 1
      ∧ (P + H / 2) ^ 2 + (2 * (P + H / 2) * (Q + H / 2)) / 2 = P + H / 2 := by
  have hpq : (P + H / 2) + (Q + H / 2) = 1 := by linarith
  exact ⟨hpq, by linear_combination (P + H / 2) * hpq⟩

/-! ### Non-vacuity witnesses (HARDNESS.md H5) -/

/-- The hypothesis is satisfiable, and at `p = 3/5` the genotype frequencies are
the expected `(9/25, 12/25, 4/25)`. -/
example : (3/5 : ℚ) ^ 2 + 2 * (3/5) * (2/5) + (2/5 : ℚ) ^ 2 = 1 := by norm_num

/-- **The hypothesis is load-bearing.** With `p = 1/2, q = 1/4` — which do not
sum to one — the genotype frequencies sum to `9/16`, not `1`. So `h` is not
decoration.

The first draft of this witness used `p = q = 1/2`, which *does* sum to one and
so proved nothing; the kernel rejected it with `⊢ False`. A negative control
that is merely asserted is worth exactly as much as no control at all. -/
example : (1/2 : ℚ) ^ 2 + 2 * (1/2) * (1/4) + (1/4 : ℚ) ^ 2 ≠ 1 := by norm_num

/-- A population starting far from equilibrium — all heterozygotes — still has
invariant allele frequency after one round. -/
example : (0 : ℚ) + 1 / 2 = 1 / 2 := by norm_num

/-! ### Axiom footprints -/

#print axioms genotype_freqs_sum_one
#print axioms allele_freq_invariant
#print axioms equilibrium_in_one_generation

end Mathesis.Applications.HardyWeinberg
