---
name: mathesis-usecase-loop
description: Run one scientific claim end-to-end through the Mathesis pipeline — refute, check in exact arithmetic, prove in Lean, exhibit witnesses, file ledger rows. Use when asked to formalize, verify, or add a new result in mathematics, physics, biology, or any modelled science, and when adding a use case to the applications campaign.
---

# The use-case loop

One claim, six steps, one commit. The loop is designed so that **most candidates die cheaply**
and the survivors arrive with their evidence attached.

```
0 SPLIT → 1 REFUTE → 2 CHECK → 3 PROVE → 4 WITNESS → 5 FILE
  M vs W    minutes     Tier B    Tier A    both        both ledgers
```

## 0 — Split the claim (`mathesis-modelling`)

Write two sentences: **M**, the mathematics that follows from the model; **W**, the claim that
the model describes something real. Only **M** enters the Lean file. **W** gets its own row at
its own tier, and it can never be Tier A.

Skipping this step is the most common way a use case goes wrong, and it goes wrong invisibly:
everything compiles.

## 1 — Refute before proving

**Try to break it first**, in exact arithmetic, at small parameters. Perturb a coefficient.
Set a variable to zero. Try the degenerate case.

This inverts the instinct and it pays. A false conjecture absorbs unbounded proof effort and
returns nothing; a five-second sweep kills most of them. It also tells you what the hypotheses
have to be — the cases where it breaks are exactly the side conditions.

**Compute your parameters, never guess them.** Two witnesses in this campaign were wrong on the
first attempt: one chose parameters where the quantity was accidentally zero (proving the one
case that proves nothing), the other chose a "counterexample" that wasn't one. Both were caught
by the kernel with `⊢ False`. A thirty-second Python check would have caught both sooner:

```python
from fractions import Fraction as F
print(prey_rate(F(2), F(1), F(3), F(2)))   # 0 — this witness is worthless
print(prey_rate(F(2), F(1), F(3), F(1)))   # 3 — this one works
```

## 2 — Check at Tier B

Enumerate exactly, in `Fraction`/`int`. Exhaustive over a small grid beats random over a large
one: a failure names a reproducible tuple rather than a seed.

Ship a **negative control that targets the plausible near-miss**, not obvious garbage. The
controls that earned their place here:

| Use case | Control | What it separates |
|---|---|---|
| Elastic collision | a perfectly **inelastic** collision | conserves momentum but *not* energy — a momentum-only check passes it |
| Hardy–Weinberg | selection against `aa` | allele frequency *moves*; a check that couldn't see this makes the null model unfalsifiable |
| Kepler III | inverse-**cube** force | `ω²r³` stops being constant — proves the check is about gravity, not arithmetic |
| Lotka–Volterra | perturb one coefficient | proves the identity is about *this* vector field |

Add the mirror image too: a correct instance must be **accepted**. A harness that rejects
everything is as useless as one that rejects nothing.

## 3 — Prove at Tier A

Declare the gate contract in the file header:

```
MATHESIS-GATE: env=mathlib
MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound
```

Work over `ℚ` when the harness uses `Fraction` — then the Lean theorem and the Tier B check are
statements about **one** structure, not two that happen to agree numerically. `ℝ` buys
generality you rarely need and loosens that correspondence.

`field_simp; ring` closes most conservation identities. `linear_combination h` closes most
"given `p + q = 1`" algebra.

**Expect the footprint to change and amend the declaration, not the gate.** In this campaign a
file declared `allow=` (no axioms), then needed `omega`, which carries `[propext, Quot.sound]`.
One proof rewrite was attempted to get back to `[]`; it didn't, so the *declaration* was
amended. That direction is the rule (`LL.md` LL-2). Measure before you write the header —
`rw` and structural recursion are axiom-free, `omega`, `simp`, and `decide` are not.

**Add `#print axioms` for every theorem.** Gate 2 fails if the count of directives and the count
of parsed footprints disagree, so a theorem you forget to print is a gate failure, not a silent
gap (`LL.md` LL-11).

## 4 — Witness, both polarities

```lean
example : CircularOrbit 1 1 1 := by unfold CircularOrbit; norm_num      -- satisfiable
example : ¬ CircularOrbit 1 4 1 := by unfold CircularOrbit; norm_num    -- and constraining
example : dVdt 2 1 1 1 0 1 ≠ 0 := by unfold dVdt …; norm_num            -- hypothesis is load-bearing
```

Three kinds, all required when applicable:
- the hypotheses are **satisfiable** (else the theorem is true and empty);
- the predicate **constrains** (else it holds of everything);
- each side condition is **load-bearing** — show the conclusion failing without it.

The third is what justifies every `≠ 0` in the statement. Lean's junk-value convention
(`x / 0 = 0`) makes it easy to write a theorem that is quietly about nothing.

## 5 — File both ledgers, one commit

Artifact + `LEDGER.md` row + `ledger.jsonl` row + gate output, together. Run
`./scripts/verify.sh` first; all four gates must be green.

## Before you declare a wall — check the environment

**"The infrastructure isn't available" is a claim, and it needs evidence like any other.**

Lean reports a missing lemma as an unknown identifier, which looks identical to *the lemma does
not exist* and to *your statement is false*. A module that was simply never built masquerades as
a mathematical obstruction.

This happened here. UC5's analytic step was filed OPEN because `HasDerivAt.log` appeared
unavailable. It was unavailable in one Mathlib checkout and **present in the other**. Pointed at
the second, the proof is nine lines and compiled first try. The deferral, and the paragraphs
arguing for it, rested on a premise nobody checked.

```bash
# Check every provider before concluding anything is missing.
for env in ~/xdev/*/lean_src ~/xdev/*/dualscale/lean; do
  [ -d "$env/.lake" ] && echo "== $env" && (cd "$env" && lake env lean /tmp/probe.lean 2>&1 | head -3)
done
```

Record which environments you checked. Then, if it is genuinely absent, defer.

## When you hit a wall — the honest exit

If the last step needs infrastructure you do not have (ODE theory, measure theory, a real
solution concept), **prove the part you can and record the rest as OPEN**.

Do not axiomatize it. Do not restate it conditionally as *"given `X`, and `X → Y`, therefore
`Y`"* — that compiles, carries no axioms, looks like Tier A, and is a tautology. Stream 1 shipped
exactly that shape, was audited, and accepted **demotion to Tier C**.

The Lotka–Volterra case is the worked example of *both halves*. The algebraic cancellation went
in as Tier A; the claim that the cancelled expression *is* `dV/dt` went in as Tier C and OPEN, in
a separate row — and was later **closed and promoted** once the environment turned out to have
the calculus after all. Defer honestly, then go back and try to close it.

**A campaign with no deferrals and no rejections has not been tested.** Report the ratio, not
the count.

**But try to close your OPEN rows before shipping.** Not because deferral is shameful — it is
the correct move when the wall is real — but because **the promotion path is itself a mechanism
that needs exercising**, and an OPEN row is the only thing that can exercise it. A ledger with
no promotions has an untested transition in it. Closing UC5 produced this repository's first
promotion (`MX-C-0004` → `MX-A-0011`), and until then §2.5's promotion rule was schema with no
instance.

## Checklist

- [ ] **M** and **W** split before any code
- [ ] Refutation attempted first; side conditions came from where it broke
- [ ] Tier B harness enumerates exactly, with a near-miss control **and** an accept control
- [ ] Lean over the same number system as the harness
- [ ] `MATHESIS-GATE` header matches the measured footprint
- [ ] `#print axioms` for every theorem
- [ ] Witnesses: satisfiable, constraining, side conditions load-bearing — all **computed**
- [ ] Both ledgers updated in the same commit as the artifact
- [ ] `./scripts/verify.sh` green

Worked examples: `docs/USECASES.md`. Frontier: `docs/APPLICATIONS_FRONTIER.md`.
