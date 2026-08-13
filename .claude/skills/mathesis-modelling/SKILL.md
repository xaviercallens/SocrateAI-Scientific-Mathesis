---
name: mathesis-modelling
description: Tier a scientific claim by separating the mathematics from the empirical claim about the world — for physics, biology, chemistry, economics, or any modelled system. Use when formalizing a physical law, a population model, a rate equation, or a conservation principle; when asked whether a scientific result is "proven"; or whenever a claim mentions both a model and a real system.
---

# Tiering across the model–world gap

A scientific claim is almost always **two claims wearing one name**, and they belong at
different tiers:

| | Claim | Ceiling |
|---|---|---|
| **M** | The mathematics follows from the model | **Tier A** — provable |
| **W** | The model describes the system | **Tier C** at best — empirical |

"Hardy–Weinberg equilibrium" names both the algebra and the assertion that a population is at
it. "Conservation of energy" names both a theorem about a Hamiltonian and a claim about an
apparatus. The Tier A reputation of **M** silently underwrites **W**, and nobody notices,
because one phrase covers both.

**Split them before you write anything down.** They get separate ledger rows, and the row for
**W** *cites* the row for **M** — which by `MX-A-0004` means **W can never be Tier A**, no
matter how good the data is.

## The procedure

### 1. Write the model as an explicit hypothesis, never an axiom

The modelling assumptions go **in the theorem's type**, where the gate can see them:

```lean
def CircularOrbit (μ r ω : ℚ) : Prop := ω ^ 2 * r = μ / r ^ 2

theorem kepler_third (h₁ : CircularOrbit μ r₁ ω₁) (h₂ : CircularOrbit μ r₂ ω₂) : …
```

Not `axiom inverse_square_law : …`. An axiom puts the modelling assumption into the footprint
of everything downstream, permanently and invisibly — so the one thing a reader most needs to
know (*what did you assume about the world?*) becomes the one thing they cannot see.

### 2. Ask what the theorem would still say if the model were false

If the answer is "the same thing", you have separated correctly. `kepler_third` is true whether
or not gravity is inverse-square; it says *if* the force balance holds, *then* ω²r³ is constant.
That is Tier A and it is honest.

If the answer is "nothing", you have smuggled **W** into **M**.

### 3. Exhibit a witness — the model must be satisfiable

```lean
example : CircularOrbit 1 1 1 := by unfold CircularOrbit; norm_num
example : ¬ CircularOrbit 1 4 1 := by unfold CircularOrbit; norm_num   -- and constraining
```

Both polarities. A model predicate satisfied by everything constrains nothing, and a theorem
about an unsatisfiable model is true and empty. **Compute the witness — do not guess it.** In
this repository two witnesses in a row were wrong on the first attempt: one picked parameters
where the quantity was accidentally zero, the other picked a "counterexample" that wasn't one.
The kernel caught both with `⊢ False`.

### 4. File **W** separately, at its real tier

```
MX-A-0009  Kepler III follows from the inverse-square law for circular orbits   [lean_axioms]
MX-L-0012  Planetary orbits obey T² ∝ a³                        [citation]  → cites MX-A-0009
MX-C-0031  This exoplanet's orbit is circular to within σ       [argument]  → cites MX-L-0012
```

Each row's tier is capped by what actually checked it. The observational row is Tier L because
a referee checked it; the fit to a particular system is Tier C because it rests on a model
selection nobody proved.

## Floats are the tell

If the claim can only be stated in floating point, you are usually looking at **W** dressed as
**M** — or at an **M** that has not been formulated properly yet.

**Kepler III is the case worth learning.** Written as `T² ∝ a³` it carries π, which is
irrational, so nothing is checkable exactly and the standard move is to go to floats and report
"agreement to 10⁻¹⁵" — which certifies a rounding mode, not a law.

But π was never carrying any physics. Use the **reduced period** `τ = T/2π = 1/ω`:

```
r³/τ² = ω²r³ = GM        — exactly rational, and the constant is GM, not 4π²/GM
```

Nothing was approximated and nothing was lost; the proportionality follows immediately because
`T` and `τ` differ by the same factor for every orbit. The float ban did not make the physics
harder to state — **it located a constant that was decoration and removed it.**

When you cannot do this, the honest move is Tier X in `exploration/` under the
`# TIER X — EXPLORATORY, NO CLAIMS` banner. Floats may *steer*: locate the regime, then certify
it exactly.

## Prove the algebra, defer the analysis — do not fake the bridge

Most conservation laws split cleanly:

- **Algebraic core** — substitute the vector field, cancel. No calculus. **Tier A, provable now.**
- **Analytic bridge** — that the cancelled expression *is* `dV/dt`. Chain rule, `Real.log`
  derivative, a solution concept for the ODE. **Often not available.**

Prove the core. Record the bridge as **OPEN**. Two temptations, both refused:

1. `axiom conserved : …` — forbidden (`SPEC.md` §7.1).
2. Stating it conditionally: *"given `dV/dt = D` as a hypothesis, and `D = 0`, therefore
   `dV/dt = 0`."* This compiles, carries no axioms, and looks like Tier A. It is a **tautology**
   — `A → B → B`, containing no mathematics.

Temptation 2 is refused on precedent, not taste. Stream 1's `MillenniumReduction.lean` did
exactly this for Aubin–Lions and Prodi–Serrin, was audited, and was **demoted to Tier C** with
the verdict that bare `Prop → Prop` arrows *"completely bypass PDE theory. The Lean kernel is
merely verifying a logical tautology."* Its own stream accepted the demotion.

## Checklist

- [ ] **M** and **W** written as separate sentences before any code
- [ ] Model assumptions are hypothesis parameters, visible in the type — no `axiom`
- [ ] The theorem still says something if the model is empirically false
- [ ] Witness that the model is satisfiable, **and** one showing it constrains — both computed
- [ ] Exact arithmetic; if impossible, reformulate before reaching for floats
- [ ] **W** filed as its own row, at its own tier, citing **M**
- [ ] Anything not proved recorded as OPEN — not axiomatized, not made conditional-and-vacuous

## The sentence to keep

> A theorem about a model is a theorem about the model.

Worked examples: `lean/Mathesis/Applications/` and `docs/USECASES.md`.
