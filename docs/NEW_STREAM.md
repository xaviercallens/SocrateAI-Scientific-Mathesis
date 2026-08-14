# Starting a new stream on Stream 0 — worked for QuantumFluids

**Tier of this document:** C (guidance and proposal). It states no result and makes no claim
about superfluids. Where it says a claim "would be Tier A", that is a statement about what the
*admission criterion* would require, not a prediction that the proof exists.

---

## Why a new stream is the easy case

Every finding Stream 0 has produced in six sibling repositories is a **migration** problem: a
rule stated before anything enforced it, an axiom added when the gate did not exist, a label
that became false while nobody was checking. None of them was created by a bad decision. They
were created by *ordering* — the claims came first and the checking came later, and by the time
the gate arrived the tree was too large to bring into compliance cheaply.

A new stream has no legacy. **Gate from commit one and none of it happens.** The cost of doing
this at the start is roughly a day; the cost of doing it after two hundred commits is what
`docs/OWNER_BRIEF.md` D1 is about.

## Day-one checklist

```bash
# 1. The gate. One file, stdlib only, nothing to install.
mkdir -p tools/mathesis-gate
curl -O https://raw.githubusercontent.com/xaviercallens/SocrateAI-Scientific-Mathesis/main/tools/mathesis-gate/mathesis_gate.py
mv mathesis_gate.py tools/mathesis-gate/
python3 tools/mathesis-gate/mathesis_gate.py --self-test

# 2. CI, BINDING from the start — no --report-only, because there is nothing to grandfather.
mkdir -p .github/workflows
curl -o .github/workflows/ci.yml https://raw.githubusercontent.com/xaviercallens/SocrateAI-Scientific-Mathesis/main/tools/mathesis-gate/github-workflow.yml
# then delete the `--report-only` line

# 3. An empty ledger. It is checked from the first row.
printf '# <STREAM>-<TIER>-<NNNN>. A claim absent from here has no tier and may not be cited.\n' > ledger.jsonl

# 4. Plant a defect and watch the gate fail. Do this BEFORE filing anything.
printf 'def vacuous : Prop := True\n' > lean/_Probe.lean
python3 tools/mathesis-gate/mathesis_gate.py . --lean-src lean   # must exit 1
rm lean/_Probe.lean
```

Step 4 is not optional and not ceremony. A gate that has only ever been observed passing is
indistinguishable from a gate that cannot fail, and every gate in Stream 0 has a recorded
demonstration of rejecting a planted defect. Record yours.

**Claim a stream code** before the first ledger row: `QF` is free. Identifiers are
`QF-A-0001`, `QF-B-0001`, and so on, and the tier letter is *in* the identifier so a promotion
changes it and stale citations become lexically wrong rather than silently wrong.

---

## Why QuantumFluids is the right domain to try this on

The dual-scale programme's core idea is that there is a **fundamental length below which the
geometry does not go** — `Reff(α′,R) = max(R, α′/R) ≥ √α′`, with a bounce rather than a
collapse. Stream 0 has that proved, unconditionally and axiom-free (`MX-A-0005`).

In Navier–Stokes (Stream 1) that minimum scale is **conjectural infrastructure**: it is
motivation for Hypothesis U, and the physics does not hand it to you. The programme has to earn
it.

In a quantum fluid it is **physical, quantized, and measured**:

| Dual-scale object | Classical fluid | Quantum fluid |
|---|---|---|
| minimum length `√α′` | conjectured cutoff | the **healing length** `ξ`, set by the equation of state |
| "the geometry bounces" | hypothesis | vortex cores have finite size; the order parameter cannot vary faster than `ξ` |
| discreteness | none | **circulation is quantized**: `∮ v·dl = n·h/m`, `n ∈ ℤ` |
| singularity | the open question | reconnections are regularized by `ξ`; no infinite-vorticity limit |
| governing equation | Navier–Stokes | Gross–Pitaevskii — nonlinear Schrödinger, far more tractable |
| evidence | none direct | cold atoms and helium-4; decades of published measurement |

**The reason this matters for the tier calculus specifically:** in Stream 1 the minimum-scale
hypothesis can only be filed at Tier C, and everything conditional on it inherits that ceiling
by `MX-A-0004`. In a quantum fluid the same structural claim has a **Tier L** anchor — published,
peer-reviewed, quotable to a theorem or a measurement — and an exactly-stateable **Tier B**
core. The dual-scale hypothesis stops being the thing you assume and becomes the thing you cite.

That is the whole argument for the domain, and it is an argument about *evidence*, not about
physics. Whether the analogy carries scientific weight is not Stream 0's call.

---

## The first thing to prove — and it is unusually clean

**Quantized circulation.** `∮ v·dl = n·h/m` with `n` an **integer**.

This is the ideal first Tier A target for three independent reasons:

1. **It is integer-valued.** No floats, no rounding, no "agrees to 10⁻¹⁵". The float ban
   (`HARDNESS.md` H3) costs nothing here — the physics is already discrete.
2. **It is a topological statement**, not an analytic one. The winding number of a complex order
   parameter around a loop is `ℤ`-valued because the phase is single-valued. Mathlib has the
   machinery; no PDE theory is required.
3. **It is the discreteness the dual-scale picture wants**, stated exactly, at the outset.

Suggested `QF-A-0001`: *for a single-valued complex order parameter non-vanishing on a loop, the
phase winding is an integer, and the circulation is that integer times `h/m`.*

**`QF-B-0001`** is then the exact-arithmetic companion: enumerate winding numbers over rational
sample phases and check additivity under loop composition, with a negative control where the
order parameter **vanishes** on the loop and the winding is undefined — the trap that makes the
non-vanishing hypothesis load-bearing.

Note what that gives you: a Tier A theorem whose hypothesis (`ψ ≠ 0` on the loop) is exactly the
physical condition that fails *inside a vortex core*. The side condition is not bookkeeping —
it **is** the core, and the witness that the theorem fails without it is the statement that
vortices have finite size.

### A plausible first ledger

```
QF-A-0001  phase winding is ℤ-valued; circulation = n·h/m            lean_axioms
QF-B-0001  winding additivity + non-vanishing control                exact_harness  → QF-A-0001
QF-L-0001  measured quantized circulation in He-II / BEC             citation
QF-C-0001  healing length ξ is the quantum-fluid analogue of √α′     argument       → QF-A-0001, QF-L-0001
QF-X-0001  GPE simulation of a reconnection                          numeric
```

Read the tiers off that and the discipline does its work by itself. `QF-C-0001` — the analogy
that is the *point* of the stream — sits at Tier C and cites the two rows that carry real
evidence. It can never be Tier A, because by `MX-A-0004` a claim cannot outrank its support, and
an analogy between two physical systems is not a theorem. `QF-X-0001` may steer the search and
may never be cited.

---

## The traps in this domain specifically

**The model/world split is sharper here than anywhere.** Gross–Pitaevskii is a mean-field
approximation valid for weakly-interacting dilute gases. Every theorem you prove is about
**GPE**, and "helium-4 obeys GPE" is false in the regime most people care about. Write both
sentences before writing any Lean:

- **M**: *in the GPE, quantities X and Y are related thus.* Tier A.
- **W**: *this fluid is described by the GPE.* Tier C, always, and it cites M.

**ħ, m and g are hypothesis parameters, never global constants.** This is the same rule that
Stream 5's `TDuality.lean` broke with `def alpha_prime : ℝ := 1` — with the constant pinned,
every statement about a limit becomes unstateable and nothing reports it. If a claim concerns the
`ξ → 0` limit, `ξ` must be quantified in the statement, and the quantifier order is normative:
`∃C ∀ξ`, not `∀ξ ∃C`.

**Dimensionless groups before floats.** As with Kepler III, where the reduced period `τ = T/2π`
removed `π` from the statement and made it exactly rational, most quantum-fluid relations become
exact once written in units of `ξ` and `h/m`. If a statement cannot be made exact, reformulate it
before reaching for floats — that reformulation usually *improves* the statement.

**A simulation is Tier X.** A GPE integration is floating-point and discretized. It may locate
the interesting regime; the certification has to be exact.

---

## What Stream 0 gives you, and what it does not

**Gives you:** the tier notation and its kernel-verified soundness theorem; the portable gate;
the LaTeX notation package (`latex/mathesis.sty`); a consolidated Tier A `Reff` with the
minimum-scale theorems already proved; six worked use cases to copy the shape from; and sixteen
recorded lessons, most of them written after something went wrong.

**Does not give you:** any verdict about superfluids, any licence from a green board, and any
substitute for the human statement-adequacy audit. A theorem is Tier A when the kernel accepts
it and **citable** only once a person has confirmed the statement is the one anyone meant. That
step does not parallelize and cannot be delegated to a model — including for the claim, above,
that quantized circulation is the right place to start.

---

## Reading order

| | |
|---|---|
| `README.md` | what this is, in five minutes |
| `docs/FOUNDATIONS.md` | the argument, including why notation is the mechanism |
| `docs/USECASES.md` | six worked cases; copy the shape |
| `.claude/skills/mathesis-modelling/` | the M/W split — **read before writing any physics** |
| `.claude/skills/mathesis-usecase-loop/` | the six-step pipeline for one claim |
| `HARDNESS.md` | the invariants, each with the check that enforces it |
| `LL.md` | sixteen lessons. Most were written after a mistake; the shortest path is to not repeat them |
