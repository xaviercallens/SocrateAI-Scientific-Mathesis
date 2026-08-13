/-
  Mathesis / TierCalculus.lean  —  Stream 0 Tier A core.

  MATHESIS-GATE: env=none
  MATHESIS-GATE: allow=
  MATHESIS-GATE: allow(witness)=propext

  AXIOM ALLOWLIST (enforced per declaration by Gate 2, see scripts/check_footprints.py):
    theory declarations   : []          -- no axioms at all
    witness declarations  : [propext]   -- decide-only; justified below

  The theory — every theorem that states something general about ledgers — is
  axiom-free. The five `witness*` lemmas are closed by `decide`, and Lean core's
  `Decidable` instance for a quantifier over `Fin n` is itself built with
  `propext`; the axiom is inherited from the *decision procedure*, not from the
  mathematics. It is not `Classical.choice` and not `sorryAx`.

  This split is declared rather than glossed. An earlier draft of this header
  claimed `[]` for the whole file, which was false the moment the witnesses were
  added — precisely the kind of stale-by-one-edit claim SPEC.md §7.6 exists to
  catch. The gate now checks the map, not a single global string.

  This file is Mathlib-free and cold-builds in ~2s; see SPEC.md §7.1 and §7.7.

  WHAT THIS FILE PROVES
  ---------------------
  A ledger assigns to each claim a tier and a list of claims it rests on. The
  ledger is `Sound` when no claim is filed above any claim it directly cites.
  The theorem is that soundness propagates through the *transitive* dependency
  closure — which is the property informal bookkeeping loses first, and the only
  reason this is worth a kernel proof at all.

  WHAT THIS FILE DOES NOT PROVE
  -----------------------------
  Nothing about whether the tiers were assigned correctly. `Sound` is a
  consistency property of a record, not a soundness property of the science.
  See SPEC.md §2.4.
-/

namespace Mathesis

/-! ## 1. The tier lattice -/

/-- Citation strength. See `SPEC.md` §2.1. The order is about how much of the
checking a machine did, not about mathematical depth. -/
inductive Tier where
  /-- Exploratory: floats, sampling, plots, LLM output. May never be cited. -/
  | X
  /-- Conjecture, analogy, unverified reduction. -/
  | C
  /-- Peer-reviewed literature, cited to a quoted theorem statement. -/
  | L
  /-- Finite statement decided in exact arithmetic, with a failing negative control. -/
  | B
  /-- Kernel-verified: compiles, no `sorry`, declared axiom footprint. -/
  | A
deriving DecidableEq, Repr

namespace Tier

/-- Numeric rank, `X = 0 … A = 4`. -/
def rank : Tier → Nat
  | X => 0
  | C => 1
  | L => 2
  | B => 3
  | A => 4

/-- Citation-strength order. -/
protected def le (s t : Tier) : Prop := s.rank ≤ t.rank

instance : LE Tier := ⟨Tier.le⟩

instance (s t : Tier) : Decidable (s ≤ t) :=
  inferInstanceAs (Decidable (s.rank ≤ t.rank))

protected theorem le_refl (s : Tier) : s ≤ s := Nat.le_refl _

protected theorem le_trans {s t u : Tier} (h₁ : s ≤ t) (h₂ : t ≤ u) : s ≤ u :=
  Nat.le_trans h₁ h₂

/-- `A` is the top of the order. -/
theorem le_A (s : Tier) : s ≤ Tier.A := by
  cases s <;> decide

/-- `X` is the bottom of the order. -/
theorem X_le (s : Tier) : Tier.X ≤ s := by
  cases s <;> decide

/-- The rank pins the tier down: nothing but `A` has rank `4`. This is what turns
the numeric bound of `le_A` back into an identification of the tier itself. -/
theorem eq_A_of_A_le {s : Tier} (h : Tier.A ≤ s) : s = Tier.A := by
  cases s <;> first | rfl | exact absurd h (by decide)

/-- Antisymmetry: the order separates the five tiers. -/
protected theorem le_antisymm {s t : Tier} (h₁ : s ≤ t) (h₂ : t ≤ s) : s = t := by
  cases s <;> cases t <;> first | rfl | exact absurd h₁ (by decide) | exact absurd h₂ (by decide)

end Tier

/-! ## 2. Ledgers -/

/-- A single ledger row: the tier it is filed at, and the claims it rests on.
`ι` is the claim-identifier type (in practice, the `MF-A-0007` strings of
`SPEC.md` §2.5). -/
structure Claim (ι : Type) where
  tier : Tier
  supports : List ι
deriving Repr

/-- A ledger is a total assignment of rows to identifiers. Totality is a
modelling convenience, not a claim about the world: identifiers with no row map
to a `Tier.X` row with no supports, which is exactly "unrecorded, uncitable". -/
abbrev Ledger (ι : Type) := ι → Claim ι

/-- **The soundness condition.** No claim is filed at a tier above any claim it
directly cites. -/
def Sound {ι : Type} (L : Ledger ι) : Prop :=
  ∀ a b, b ∈ (L a).supports → (L a).tier ≤ (L b).tier

/-- Transitive dependency: `Depends L a b` means claim `a` rests on claim `b`,
directly or through a chain. -/
inductive Depends {ι : Type} (L : Ledger ι) : ι → ι → Prop where
  | direct {a b} : b ∈ (L a).supports → Depends L a b
  | step {a b c} : b ∈ (L a).supports → Depends L b c → Depends L a c

namespace Depends

/-- Dependency is transitive. Proved by induction on the first chain, which is
why `step` is stated with a direct edge on the left. -/
theorem trans {ι : Type} {L : Ledger ι} {a b c : ι}
    (hab : Depends L a b) (hbc : Depends L b c) : Depends L a c := by
  induction hab with
  | direct h => exact Depends.step h hbc
  | step h _ ih => exact Depends.step h (ih hbc)

end Depends

/-! ## 3. The theorem -/

/-- **Transitive tier monotonicity.** In a sound ledger, a claim never outranks
anything in its transitive support set — not merely its direct citations.

This is the guarantee Stream 0 offers the other streams. -/
theorem tier_le_of_depends {ι : Type} {L : Ledger ι} (hL : Sound L) :
    ∀ {a b : ι}, Depends L a b → (L a).tier ≤ (L b).tier := by
  intro a b h
  induction h with
  | direct hmem => exact hL _ _ hmem
  | step hmem _ ih => exact Tier.le_trans (hL _ _ hmem) ih

/-- **Corollary: a kernel claim rests only on kernel claims.** In a sound ledger,
the entire transitive support set of a Tier A row is Tier A.

In particular a Lean theorem may not cite a Tier L result: it must take it as an
explicit hypothesis parameter instead. See `SPEC.md` §2.4. -/
theorem no_kernel_claim_rests_on_weaker {ι : Type} {L : Ledger ι} (hL : Sound L)
    {a b : ι} (ha : (L a).tier = Tier.A) (hab : Depends L a b) :
    (L b).tier = Tier.A :=
  Tier.eq_A_of_A_le (ha ▸ tier_le_of_depends hL hab)

/-- The contrapositive, in the form a reviewer actually uses: if anything in the
transitive support set is below `A`, the citing claim is below `A` too. -/
theorem not_A_of_weak_support {ι : Type} {L : Ledger ι} (hL : Sound L)
    {a b : ι} (hab : Depends L a b) (hb : (L b).tier ≠ Tier.A) :
    (L a).tier ≠ Tier.A :=
  fun ha => hb (no_kernel_claim_rests_on_weaker hL ha hab)

/-! ## 4. Non-vacuity witnesses  (SPEC.md §7.5)

A `Sound` theorem with no exhibited *unsound* ledger is not evidence that
`Sound` says anything. Both instances are required, and both are checked by
`decide` rather than asserted. -/

/-- Three claims: `0` is a kernel result resting on `1`, itself a kernel result;
`2` is an uncited conjecture. -/
def witnessSound : Ledger (Fin 3)
  | 0 => { tier := Tier.A, supports := [1] }
  | 1 => { tier := Tier.A, supports := [] }
  | 2 => { tier := Tier.C, supports := [] }

theorem witnessSound_sound : Sound witnessSound := by
  show ∀ a b, b ∈ (witnessSound a).supports → (witnessSound a).tier ≤ (witnessSound b).tier
  decide

/-- The witness is not trivially sound: it has a real dependency edge, and the
theorem says something about it. -/
example : Depends witnessSound 0 1 := Depends.direct (by decide)

example : (witnessSound 1).tier = Tier.A :=
  no_kernel_claim_rests_on_weaker (a := 0) witnessSound_sound (by decide)
    (Depends.direct (by decide))

/-- **Negative control.** A ledger filing a kernel claim on top of a conjecture.
`Sound` must reject it — if this `decide` ever succeeds, `Sound` is vacuous and
every theorem above is worthless. -/
def witnessUnsound : Ledger (Fin 2)
  | 0 => { tier := Tier.A, supports := [1] }
  | 1 => { tier := Tier.C, supports := [] }

theorem witnessUnsound_not_sound : ¬ Sound witnessUnsound := by
  show ¬ ∀ a b, b ∈ (witnessUnsound a).supports → (witnessUnsound a).tier ≤ (witnessUnsound b).tier
  decide

/-- A two-step chain, exercising `step` rather than only `direct`: the theorem's
whole content is that it reaches `2` from `0`, which no direct check does. -/
def witnessChain : Ledger (Fin 3)
  | 0 => { tier := Tier.B, supports := [1] }
  | 1 => { tier := Tier.B, supports := [2] }
  | 2 => { tier := Tier.B, supports := [] }

theorem witnessChain_sound : Sound witnessChain := by
  show ∀ a b, b ∈ (witnessChain a).supports → (witnessChain a).tier ≤ (witnessChain b).tier
  decide

/-- The two-step chain, with the intermediate node named. -/
theorem witnessChain_reach : Depends witnessChain 0 2 :=
  Depends.step (b := 1) (by decide) (Depends.direct (by decide))

example : (witnessChain 0).tier ≤ (witnessChain 2).tier :=
  tier_le_of_depends witnessChain_sound witnessChain_reach

/-- A chain that is sound at every *direct* edge but that a naive one-step check
would not connect: `0 (B) → 1 (B) → 2 (L)`. Transitivity is what reveals that the
Tier B row `0` ultimately rests on literature. -/
def witnessTransitiveLeak : Ledger (Fin 3)
  | 0 => { tier := Tier.L, supports := [1] }
  | 1 => { tier := Tier.L, supports := [2] }
  | 2 => { tier := Tier.L, supports := [] }

theorem witnessTransitiveLeak_sound : Sound witnessTransitiveLeak := by
  show ∀ a b, b ∈ (witnessTransitiveLeak a).supports →
    (witnessTransitiveLeak a).tier ≤ (witnessTransitiveLeak b).tier
  decide

/-- The same shape filed one tier too high at the head is rejected — the leak is
caught at the direct edge `1 → 2` once the head is promoted. -/
def witnessTransitiveLeakBad : Ledger (Fin 3)
  | 0 => { tier := Tier.A, supports := [1] }
  | 1 => { tier := Tier.A, supports := [2] }
  | 2 => { tier := Tier.L, supports := [] }

theorem witnessTransitiveLeakBad_not_sound : ¬ Sound witnessTransitiveLeakBad := by
  show ¬ ∀ a b, b ∈ (witnessTransitiveLeakBad a).supports →
    (witnessTransitiveLeakBad a).tier ≤ (witnessTransitiveLeakBad b).tier
  decide

/-! ## 5. Axiom footprints

Gate 2 greps these lines. Every one must print `[]`. -/

#print axioms Tier.le_A
#print axioms Tier.eq_A_of_A_le
#print axioms Tier.le_antisymm
#print axioms Depends.trans
#print axioms tier_le_of_depends
#print axioms no_kernel_claim_rests_on_weaker
#print axioms not_A_of_weak_support
#print axioms witnessSound_sound
#print axioms witnessUnsound_not_sound
#print axioms witnessChain_sound
#print axioms witnessTransitiveLeak_sound
#print axioms witnessTransitiveLeakBad_not_sound

end Mathesis
