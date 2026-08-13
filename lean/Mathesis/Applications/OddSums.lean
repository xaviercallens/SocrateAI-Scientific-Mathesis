/-
  Mathesis/Applications/OddSums.lean — Use case 1 (mathematics, elementary).

  MATHESIS-GATE: env=none
  MATHESIS-GATE: allow=propext,Quot.sound

  STATUS: DRAFT — kernel-clean, human statement-adequacy audit NOT performed (L4.4).

  THE CLAIM
  ---------
  The sum of the first n odd numbers is n².  1 + 3 + 5 + ... + (2n-1) = n².

  WHY THIS IS USE CASE 1
  ----------------------
  It is indisputable, it is provable by induction in four lines, and nobody will
  argue about whether the statement means what it says. That makes it the right
  place to exercise the *pipeline* rather than the mathematics: propose, refute,
  check at Tier B, prove at Tier A, file the row.

  A campaign that starts on a hard problem cannot tell a broken pipeline from a
  hard problem. This one can.

  Mathlib-free; cold-builds in ~0.8s.

  ON THE FOOTPRINT
  ----------------
  Declared [propext, Quot.sound], inherited from `omega`'s decision procedure,
  not from the mathematics. This was measured, not assumed: `rw` and structural
  recursion are axiom-free here (`viaRw`, `viaRec` probes both report none), and
  `omega` alone reproduces the pair on a one-line goal.

  The first draft declared []. The proof needed `omega` and the declaration went
  stale on the spot -- LL-2, a second time, in the same repository that recorded
  it. One rewrite of the proof was attempted to get back to [] and did not, so
  the DECLARATION was amended rather than the gate. That direction is the rule.
-/

namespace Mathesis.Applications.OddSums

/-- Sum of the first `n` odd numbers, `1 + 3 + ... + (2n-1)`. -/
def sumOdd : Nat → Nat
  | 0 => 0
  | n + 1 => sumOdd n + (2 * n + 1)

/-- **UC1.** The sum of the first `n` odd numbers is `n²`. -/
theorem sumOdd_eq_sq (n : Nat) : sumOdd n = n * n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    show sumOdd k + (2 * k + 1) = (k + 1) * (k + 1)
    rw [ih, Nat.add_mul, Nat.mul_add]
    omega

/-! ### Non-vacuity witnesses (HARDNESS.md H5)

The theorem is a `∀`, so it is worth exhibiting that `sumOdd` actually computes
something and that the identity is not true by some degenerate reading. -/

example : sumOdd 0 = 0 := by decide
example : sumOdd 1 = 1 := by decide
example : sumOdd 5 = 25 := by decide
example : sumOdd 10 = 100 := by decide

/-- The negative control, in the kernel: the *false* variant is refutable.
This is what makes `sumOdd_eq_sq` a claim rather than a definition. -/
example : sumOdd 5 ≠ 5 * 5 + 1 := by decide

/-! ### Axiom footprints -/

#print axioms sumOdd_eq_sq

end Mathesis.Applications.OddSums
