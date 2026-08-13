# USECASES.md — five worked cases, increasing in complexity

The tier calculus had **zero consumers** until this campaign, which its own governing rule
forbids (`SPEC-STREAM0` §R3.4, and `docs/OWNER_BRIEF.md` D4). These five cases are the fix:
real claims, in three sciences, run end to end through the pipeline.

They are deliberately elementary. The point is not the mathematics — it is that the *apparatus*
survives contact with mathematics that nobody will argue about, so that when it is pointed at
something contested, a failure is a failure of the claim and not of the plumbing.

```
$ ./scripts/verify.sh
PASS  tier_b_applications  (UC1-UC5, 6 negative controls)
PASS  Gate 2 (7 module(s))
ALL GATES PASS
```

---

## The five

| # | Domain | Claim | Tier A artifact | What it exercises |
|---|---|---|---|---|
| 1 | Mathematics | `1+3+…+(2n−1) = n²` | `OddSums.lean` | the pipeline itself |
| 2 | Physics | 1-D elastic collision conserves `p` and `E` | `ElasticCollision.lean` | exact arithmetic vs. "agrees to 10⁻¹⁵" |
| 3 | Biology | Hardy–Weinberg allele invariance | `HardyWeinberg.lean` | **model vs. world** |
| 4 | Physics | Kepler III from the inverse-square law | `Kepler.lean` | the float ban improving the statement |
| 5 | Biology | Lotka–Volterra conserved quantity | `LotkaVolterra.lean` | **the honest deferral** |

All five are Tier A over `ℚ`, footprints as declared, with a Tier B harness
(`tests/tier_b_applications.py`) checking the same statements on enumerated exact data.

---

## UC1 — Sum of odd numbers *(mathematics)*

`sumOdd n = n * n`, by induction. Mathlib-free, ~0.8s cold build.

**Why start here.** It is indisputable and four lines long, so a failure can only be the
pipeline. A campaign that starts on a hard problem cannot tell a broken pipeline from a hard
problem; this one can.

**What it taught.** The declared footprint went stale immediately. The header said `allow=`
(no axioms) and the proof needed `omega`, which carries `[propext, Quot.sound]`. One proof
rewrite was attempted to reach `[]` and failed, so the **declaration** was amended — the
direction `LL.md` LL-2 requires. Measurement, not assumption: `rw` and structural recursion are
axiom-free here; `omega` alone reproduces the pair on a one-line goal.

---

## UC2 — Elastic collision *(physics)*

```
v₁ = ((m₁−m₂)u₁ + 2m₂u₂)/(m₁+m₂)      v₂ = ((m₂−m₁)u₂ + 2m₁u₁)/(m₁+m₂)
```

Both momentum and kinetic energy conserved, for any `m₁+m₂ ≠ 0`.

**What it exercises.** The textbook check is numerical and reports "agreement to 10⁻¹⁵". That
is a statement about a rounding mode, not about physics. Over `ℚ` the quantities are conserved
or they are not. Here they are, identically, over 1296 enumerated mass/velocity combinations.

**The control that matters.** A perfectly **inelastic** collision conserves momentum but not
energy. An implementation checking only momentum would pass it. That control is what makes the
energy check mean something.

**Witness.** With `m₂ = −m₁` the formulae divide by zero, Lean's junk-value convention returns
`0`, and momentum is *not* conserved — which is why `m₁+m₂ ≠ 0` is in both statements.

---

## UC3 — Hardy–Weinberg *(biology)* — the model/world split

`p² + (2pq)/2 = p`: allele frequency is invariant under random mating, and equilibrium is
reached in **one** generation from arbitrary starting genotype frequencies.

**This is where the tiering gets more interesting than the mathematics.**

The algebra is Tier A: given the model, allele frequency is conserved, full stop. But *"this
population is at Hardy–Weinberg equilibrium"* is a claim about a biological system, and it is
Tier C at best — the model assumes infinite population, random mating, no selection, no
mutation, no migration, no drift. Not one holds of any real population.

In most write-ups "Hardy–Weinberg equilibrium" names **both** the algebra and the empirical
claim, and the Tier A reputation of the first quietly underwrites the second. The calculus makes
the split structural rather than rhetorical: any application to a real population is a separate
row that *cites* this one, and by `MX-A-0004` it can never be Tier A, however good the field
data is.

**The control that matters.** Selection against the recessive homozygote **moves** the allele
frequency. Hardy–Weinberg exists to make selection visible; a check that could not detect a
violation would render the null model unfalsifiable — the opposite of its purpose.

---

## UC4 — Kepler's third law *(physics)* — the float ban earning its keep

For circular orbits under an inverse-square force, `ω²r³ = GM` for every orbit around the same
primary.

**Watch the constraint improve the statement.** Kepler III is normally `T² ∝ a³`, and `T = 2π/ω`
puts π on both sides. π is irrational, so nothing is exactly checkable, and the usual response
is floats.

But **π was never carrying any physics.** Use the reduced period `τ = T/2π = 1/ω`:

```
r³/τ² = ω²r³ = GM
```

Exactly rational whenever `r` and `GM` are; the constant is `GM` rather than `4π²/GM`; π has
left the statement. Nothing was approximated and nothing was lost — `T² ∝ a³` follows because
`T` and `τ` differ by the same factor for every orbit.

**The float ban did not make the physics harder to state. It located a constant that was
decoration and removed it.**

**The control that matters.** Under an inverse-**cube** force, `ω²r³` stops being constant. A
check that passed for any central force would be testing arithmetic, not gravity.

**Tiering.** That *planets* obey this is empirical — Tier L, resting on observation. This file
proves the law *follows from* the force law, which is a different claim and a Tier A one,
conditional on a hypothesis the reader can see in the type.

---

## UC5 — Lotka–Volterra *(biology)* — the capstone, deliberately partial

```
ẋ = αx − βxy        ẏ = δxy − γy        V = δx − γ ln x + βy − α ln y
```

**Proved (Tier A).** Substituting the vector field into `dV/dt` and clearing the logarithmic
derivatives leaves a rational expression that is **identically zero**. Four terms cancelling in
pairs. No calculus needed; `field_simp; ring` closes it. Verified over 15 625 exact parameter
combinations at Tier B.

**Not proved, and recorded as OPEN (Tier C).** That this expression *is* `dV/dt`. That needs the
chain rule, the derivative of `Real.log`, ℝ rather than ℚ, and a solution concept for the ODE.
Mathlib has the pieces; assembling them is real work and it is not done.

**Two ways to fake it, both refused:**

1. `axiom lotka_volterra_conserved : …` — forbidden outright (`SPEC.md` §7.1). It would put an
   unproven analytic claim into every downstream footprint, permanently and invisibly.
2. State it conditionally: *"given `dV/dt = D`, and `D = 0`, therefore `dV/dt = 0`."* Compiles,
   carries no axioms, looks like Tier A. It is a **tautology** — `A → B → B`, no mathematics.

Option 2 is refused on **precedent**. Stream 1's `MillenniumReduction.lean` did exactly this for
Aubin–Lions and Prodi–Serrin, was audited, and was demoted to Tier C on 2026-08-13 with the
verdict that bare `Prop → Prop` arrows *"completely bypass PDE theory. The Lean kernel is merely
verifying a logical tautology (A → B → C)."* Its own stream accepted that. Repeating the pattern
one file later would prove this repository does not read its own ledger.

So: **`MX-A-0010`** for the algebra, **`MX-C-0004`** for the dynamical claim, OPEN.

---

## What the campaign found

**Three defects, in the apparatus rather than the mathematics** — which is what a campaign of
elementary cases is *for*:

1. **Gate 2 was silently skipping theorems.** Lean wraps `#print axioms` output past its line
   width; the parser was line-anchored and dropped every wrapped declaration. `ElasticCollision`
   reported "1 footprint" when it had 2. Because wrapping is triggered by long names, the bug hid
   precisely the deeply-namespaced declarations in new modules. Fixed; the gate now cross-checks
   the count of `#print axioms` directives against footprints parsed, and runs parser self-tests
   on every invocation. (`LL.md` LL-11)
2. **Two theorems had no footprint check at all** — `Tier.X_le` and `witnessChain_reach` lacked
   `#print axioms` lines. Found by the same audit; closed.
3. **Three non-vacuity witnesses were wrong on the first attempt.** One picked parameters where
   the quantity was accidentally zero; one asserted a false counterexample (`p = q = ½` *does*
   sum to 1); one picked an `x = 0` case where the junk value coincides with the limit. All three
   caught by the kernel with `⊢ False`. Witnesses have to be **computed, not guessed**.

Two of those three would have been invisible without this campaign. That is the argument for
running elementary cases through new apparatus before pointing it at anything that matters.

## What the campaign does not show

That any of this is true of the world. Every Tier A row here is a statement about a model with
its assumptions written into the theorem's type. A green board says the bookkeeping holds — it
licenses nothing about collisions, populations, or planets (`SPEC.md` §7.9).
