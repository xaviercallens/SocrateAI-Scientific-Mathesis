# SocrateAI-Scientific-Mathesis — Stream 0 Specification v0.1 (2026-08-13)

**Program:** the *mathesis universalis* layer of SocrateAI. Stream 0 does not do the science.
It provides the **shared formal notation, the shared verification kernel, and the shared
epistemic bookkeeping** that every other stream uses to state what it knows and how strongly
it knows it.

**Status of this document:** single active specification (§7.4 discipline inherited from
Stream 1). Companions: `PLAN.md` (operational law), `LEDGER.md` (claims), `HARDNESS.md`
(invariants), `FRONTIER.md` (TODO / NOTODO / Frontier), `LL.md` (lessons learned).

---

## 0. Epistemic Charter

Oversight split, inherited verbatim from Stream 1 and hereby made **program-wide**:

> **The machine verifier checks the proofs; the human mathematician audits the questions.**
> No LLM output gates a tier promotion.

Stream 0's own contribution to that charter is this: *the bookkeeping itself must be
machine-checked.* A program that reasons carefully but records its conclusions in prose has
no defence against its own enthusiasm six months later. Therefore:

**The ledger is a mathematical object, and Stream 0's first theorem is about the ledger.**

---

## 1. The Problem Stream 0 Solves

Six scientific streams are running concurrently:

| Stream | Repository | Object of study |
|---|---|---|
| **0 — Mathesis** | `SocrateAI-Scientific-Mathesis` | the notation, kernel, and ledger that the others share |
| **1 — MechanicaFluidorum** | `SocrateAI-Scientific-MechanicaFluidorum` | 3D Navier–Stokes regularity (HoloAlg / Hypothesis U) |
| **2 — AutoEvolve** | `SocrateAI-Scientific-AutoEvolve-K3xT2` | K3 selection in the DualScale K3×T² landscape |
| **3 — Quantum Agora** | `SocrateAI-Scientific-Quantum-K3xT2` | quantum execution of landscape search (QUBO / Cirq / TN) |
| **4 — Hypergraph** | `SocrateAI-Scientific-Hypergraph-K3xT2` | discrete hypergraph cosmology, Wolfram CAG |
| **5 — RajMath / RAMA** | `SocrateAI-Scientific-RajMathRecovery` | Ramanujan neuro-symbolic engine, mock modular forms |
| **6 — TNN Univers Model** | `SocrateAI-Scientific-TNN-UniversModel` | Topological/Thermodynamic Neural Network, vHPU |

They already share mathematics — the T-dual radius `Reff(α,R) = max(R, α/R)` appears in
Stream 1's Lean core, Stream 4's rulial inversion, and Stream 6's `RulialInversionHook`.
They do **not** share a way of saying how well any of it is known. That is the defect
Stream 0 exists to repair.

### 1.1 The observed collision — **[verified 2026-08-13, see `docs/TIER_CALCULUS.md` §1]**

Two streams already use the letter **B** for incompatible things:

- Stream 1 (`SPEC.md` §0): *"**B — Checkable**: identities validated in exact rational
  arithmetic; certified witnesses; no floats"*.
- Stream 5 (`README.md`): *"**Tier B — Established**: Peer-reviewed literature, pinned to
  exact values"*.

A claim exported from Stream 5 at "Tier B" and imported by Stream 1 as "Tier B" would silently
convert **a citation into a computation**. Nothing in either repository would catch it. This is
not a hypothetical: both repositories are live, both cite the other's Mathlib build, and Stream 1
already imports a Lean file from Stream 5's tree (`PLAN.md` F1).

**Stream 0's resolution:** separate the axes that were conflated (§2), and make the letter
carry a machine-checked meaning (§3).

---

## 2. The Tier Calculus

### 2.1 The five tiers — one linear order of *citation strength*

| Tier | Name | Admission criterion | Who can certify |
|---|---|---|---|
| **A** | Kernel | Lean 4 compiles; zero `sorry`; `#print axioms` footprint is exactly the declared allowlist | the kernel |
| **B** | Checkable | finite statement decided in exact arithmetic (ℚ/ℤ), deterministic, **ships a negative control that is demonstrated to fail** | the harness |
| **L** | Literature | statement appears in peer-reviewed work, cited to a **quoted theorem statement**, not an abstract or a summary | a human, with the quotation in the record |
| **C** | Conjecture | proposal, analogy, physical narrative, unverified reduction | anyone, if tagged |
| **X** | Exploratory | floating point, sampling, plots, LLM output | anyone; **may never be cited** |

The letter **L** is new. It exists precisely because Stream 5's "Tier B" was doing a job that
Stream 1's "Tier B" cannot do, and vice versa. Under the migration in `docs/TIER_CALCULUS.md`
§3, Stream 5's literature rows become **L**, and the letter **B** means exact arithmetic
program-wide.

### 2.2 Rank and order

`rank : Tier → ℕ` with `X ↦ 0, C ↦ 1, L ↦ 2, B ↦ 3, A ↦ 4`, and `s ≤ t := rank s ≤ rank t`.

**The order is citation strength, not epistemic virtue.** A Tier L theorem of Bourgain is a
deeper mathematical fact than any Tier B rational identity in this program. The order says
something narrower and purely operational: *how much of the checking a machine did, and hence
how much residual human trust a downstream citation inherits.* Ranking L below B is a statement
about `sorry`-free machine confirmation, not about mathematics. §2.4 is the sharp edge of this,
and it is deliberate.

### 2.3 The soundness condition — **[Tier A, verified 2026-08-13]**

A ledger is a map `L : ι → Claim ι` where `Claim ι := { tier : Tier, supports : List ι }`.

```
Sound L  :=  ∀ a b,  b ∈ (L a).supports  →  (L a).tier ≤ (L b).tier
```

*A claim may never be filed at a tier above any claim it rests on.*

**Theorem `tier_le_of_depends`** (`lean/Mathesis/TierCalculus.lean`, kernel-verified,
axiom footprint `[]`): in a sound ledger, the condition propagates through the **transitive**
dependency closure — not merely the direct one.

**Corollary `no_kernel_claim_rests_on_weaker`:** in a sound ledger, a Tier A claim's entire
transitive support set is Tier A.

This is the guarantee Stream 0 sells to the other streams, and it is the reason the guarantee
is checked by a kernel rather than asserted in a README: transitivity is exactly the property
that human bookkeeping loses first. Every stream checks the direct condition informally today.
None of them checks the closure.

### 2.4 What the theorem does *not* say

It does not say the tiers are correctly assigned. `Sound` is a **consistency** property of a
ledger, not a **soundness** property of the science: a ledger in which every row is filed at
Tier C is perfectly `Sound` and completely worthless. Assigning the right tier to a row is a
human audit, unchanged by anything in this repository.

It also has a consequence worth stating plainly rather than discovering later:
**a Tier A claim may not cite a Tier L theorem.** A Lean proof that needs Bourgain–Demeter as
an input must take it as an explicit hypothesis parameter — at which point the theorem is
Tier A *conditionally*, and the ledger records the hypothesis. This is exactly Stream 1's
existing rule ("unproven infrastructure enters as explicit hypothesis parameters, visible in
the theorem's type", Stream 1 `SPEC.md` §7.1), now derived from the tier order rather than
imposed as a separate convention.

### 2.5 Claim identifiers

```
<STREAM>-<TIER>-<NNNN>          e.g.  MF-A-0007,  RM-L-0031,  MX-B-0002
```

Stream codes: `MX` Mathesis, `MF` MechanicaFluidorum, `AE` AutoEvolve, `QK` Quantum,
`HG` Hypergraph, `RM` RajMath, `TN` TNN, `VD` Videoo.

The tier letter is **in the identifier**. A promotion therefore changes the identifier, and
the old identifier is retained as a `supersedes` link. This is deliberate: it makes a stale
citation in another stream's prose *lexically* wrong rather than silently wrong.

---

## 3. Repository Layout

```
SocrateAI-Scientific-Mathesis/
├── SPEC.md                  ← this file (normative rules)
├── PLAN.md                  ← operational law: tasks, DoD, escalation
├── LEDGER.md                ← Stream 0's own claim inventory
├── HARDNESS.md              ← structural invariants (what must never bend)
├── FRONTIER.md              ← TODO / NOTODO / Frontier
├── ROADMAP.md               ← staged roadmap
├── LL.md                    ← lessons learned, with evidence
├── CLAUDE.md                ← guidance for Claude Code sessions
├── docs/
│   ├── VISION.md            ← why Stream 0 exists
│   ├── STREAM_MAP.md        ← the seven streams and their interfaces
│   ├── TIER_CALCULUS.md     ← the collision, the resolution, the migration
│   ├── CLAUDE5_LOOP.md      ← the autoformalization loop specification
│   ├── designs/             ← derivation memos, authored before implementation
│   ├── escalations/         ← filed blockers (E-1…E-5)
│   └── proposals/           ← externally submitted artifacts, verbatim + kernel log
├── lean/Mathesis/
│   ├── TierCalculus.lean    ← Tier A core: the ledger soundness theorem
│   └── Ledger.lean          ← executable ledger checker (Lean-side)
├── python/mathesis/         ← reference implementation (exact arithmetic only)
├── rust/mathesis-verify/    ← independent second implementation (differential gate)
├── tests/                   ← Tier B harnesses, each with a negative control
├── schemas/ledger.schema.json
├── scripts/verify.sh        ← the four-gate CI entry point
└── exploration/             ← the only place floats are permitted (Tier X)
```

## 4. Toolchain

- **Lean 4** `v4.33.0-rc2`. Stream 0's core is **Mathlib-free by design** (§7.7) — it cold-builds
  from zero cache in seconds and cannot be broken by another stream's Mathlib state.
- **Python 3.12**, `fractions.Fraction` / `int` only in `tests/` and `python/`; floats barred
  outside `exploration/`.
- **Rust** (stable, 1.97+), no external crates in `mathesis-verify` — the independent
  implementation must not share a dependency with the reference implementation, or the
  differential gate (§5, Gate 3) tests one bug twice.

## 5. Verification Gates

`scripts/verify.sh` runs, in order, and is the only thing that counts as "it works":

1. **Gate 1 — Tier B.** Every `tests/tier_b_*.py` exits 0, including its negative control.
2. **Gate 2 — Tier A.** Every file in `lean/Mathesis/` kernel-compiles; zero `sorry`; every
   `#print axioms` line matches the allowlist declared in that file's header.
3. **Gate 3 — Differential.** The Rust and Python ledger checkers are run on the same corpus
   of generated ledgers (sound, unsound, cyclic, malformed) and **must agree on every verdict**.
   Disagreement fails the build without adjudicating which side is right — that is an E-3.
4. **Gate 4 — Ledger integrity.** Every row in `LEDGER.md` maps to a passing artifact; the
   machine-readable `ledger.jsonl` validates against `schemas/ledger.schema.json`; the ledger
   is `Sound` and acyclic.

## 6. Staged Roadmap

Summarized here; the calendar is `ROADMAP.md`, the executable form is `PLAN.md`.

- **Stage 0 — Foundations.** Tier calculus in Lean; Python reference; Rust differential;
  four gates green; Stream 0's own ledger populated. *(this repository's initial state)*
- **Stage 1 — Adoption.** Each stream exports its existing claims to `ledger.jsonl`. The
  Stream 5 B→L migration lands. Cross-stream `Sound` check runs over the union.
- **Stage 2 — Kernel service.** A shared, pinned Mathlib build owned by Stream 0, ending the
  situation where Stream 1's Gate 2 depends on Stream 5's working tree (Stream 1 `CLAUDE.md`
  documents this as a known fragility).
- **Stage 3 — The Claude 5 loop.** The conjecture → exact check → formalization → audit loop
  (`docs/CLAUDE5_LOOP.md`), with the human audit step non-optional and non-automatable.
- **Stage 4 — Universal notation.** Shared Lean definitions for the objects that genuinely
  recur across streams (`Reff`, the Sym² lock, the dyadic shell model), so that three streams
  stop maintaining three copies.

## 7. Rules (Do's and Don'ts)

**7.1 No axioms; declare the footprint per file.** Every Lean file states its expected
`#print axioms` allowlist in its header, and Gate 2 enforces exactly that. Stream 0's own core
declares `[]` — no axioms at all, not even `propext`. A file that needs more must say so in
its header and justify it in review.

**7.2 The negative control is the checker.** Every Tier B harness ships a control that is
*demonstrated to fail*, and Gate 1 fails if the control passes. A checker that cannot fail is
not a checker. Stream 1 recorded this rule after a real incident; Stream 0 adopts it as an
invariant rather than a lesson.

**7.3 Two implementations, no shared dependency.** The ledger checker exists in Python and in
Rust, written against the specification, not against each other. Gate 3 compares them. When
they disagree, **neither is trusted** until a human adjudicates (E-3).

**7.4 Single active file.** One active version per module; git history is the archive. No
`_v2`, `_final`, no `verify_*.lean` litter. (Stream 1 accumulated exactly this litter in the
borrowed Mathlib tree; the evidence is `verify_6b443be5c4e.lean` sitting in Stream 5's `lean/`.)

**7.5 Non-vacuity.** Every definition ships an explicit witness; every theorem ships an
`example` instantiating its hypotheses; every predicate ships **both** a satisfying and a
violating instance. A `Sound` ledger theorem with no exhibited unsound ledger is not evidence
that `Sound` says anything.

**7.6 Agent self-reports are not evidence.** Re-run the compiler or the harness on the exact
artifact before trusting it. Stream 1 caught two broken Lean proofs whose authoring process had
reported them as passing. A named theorem in the environment is *not* evidence: a failed proof
still defines the name, and only the axiom footprint reveals the `sorryAx`.

**7.7 Stream 0's core takes no dependency it cannot rebuild in a minute.** The tier calculus is
elementary and stays elementary. This is not minimalism for its own sake: Stream 0 is the thing
every other stream's gate will eventually call, so its own gate must never be the reason another
stream is blocked.

**7.8 Honest difficulty language.** "Reformulation", not "reduction". "Conjecture", not
"mechanism", until tiered. This applies to Stream 0's infrastructure claims too: a ledger that
is machine-checked for consistency is *consistent*, not *correct*.

**7.9 Nothing in this repository licenses a scientific claim.** Stream 0 ships bookkeeping.
A green Stream 0 gate says a stream's records are internally consistent. It says nothing
whatsoever about Navier–Stokes, K3 selection, or the universe.

---

*v0.1 authored 2026-08-13. The next edit to this file goes through review like any other
artifact.*
