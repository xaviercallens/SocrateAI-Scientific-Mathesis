---
name: mathesis-stream-bridge
description: Move a result, definition, or claim between SocrateAI streams — MechanicaFluidorum, AutoEvolve, Quantum, Hypergraph, RajMath, TNN, Mathesis. Use when citing another stream's result, importing a Lean file or definition from another repository, reconciling shared mathematics like Reff, or when a task spans more than one stream.
---

# Crossing a stream boundary

The seam between streams is the surface no single stream owns, and it is where claims degrade
silently — because each side is individually consistent.

## The streams

| Code | Repository | Studies |
|---|---|---|
| `MX` | `SocrateAI-Scientific-Mathesis` | the notation and kernel the others share |
| `MF` | `SocrateAI-Scientific-MechanicaFluidorum` | Navier–Stokes regularity (HoloAlg / Hypothesis U) |
| `AE` | `SocrateAI-Scientific-AutoEvolve-K3xT2` | K3 selection in the DualScale K3×T² landscape |
| `QK` | `SocrateAI-Scientific-Quantum-K3xT2` | quantum landscape search (TN / QUBO / Cirq) |
| `HG` | `SocrateAI-Scientific-Hypergraph-K3xT2` | hypergraph cosmology, Wolfram CAG |
| `RM` | `SocrateAI-Scientific-RajMathRecovery` | the RAMA engine, mock modular forms |
| `TN` | `SocrateAI-Scientific-TNN-UniversModel` | the TNN Univers Model, vHPU |
| `VD` | `SocrateAI-Scientific-Videoo-K3xT2` | scientific communication |

## ⚠ Tier letters do not currently mean the same thing

**This is a live, documented defect** (`MX-C-0001`).

- Stream 1's **Tier B** = *validated in exact rational arithmetic*.
- Stream 5's **Tier B** = *peer-reviewed literature, pinned to exact values*.

A claim exported from Stream 5 at "Tier B" and imported by Stream 1 as "Tier B" silently
converts **a citation into a computation**. Nothing in either repository catches it.

**Until the migration lands, treat every imported tier letter as untyped.** Do not translate it;
re-derive it:

1. Open the source stream's own tier definition (its `SPEC.md` or `README.md`).
2. Read what *that* letter admits.
3. Map to the Mathesis tier by the admission criterion, not the letter:
   - a program checked it in exact arithmetic → **B**
   - a referee checked it in a journal → **L**
   - the kernel checked it → **A**
4. Record the source id in `supports`, and note the re-derivation.

Under the Mathesis calculus, Stream 5's literature rows are **L** — a letter the old scheme
did not have, which is why they ended up sharing **B** with something else entirely.

## Importing a Lean file

Stream 1's task F1 imports a theorem from Stream 5's tree, so this is routine — and worth
doing carefully:

1. **Archive it verbatim first** under `docs/proposals/`, before any edit.
2. **Compile it as-submitted** and save the kernel log. A named theorem in the environment is
   not evidence; only the axiom footprint is.
3. **Check the footprint** against your file's declared allowlist — the source stream's
   allowlist may be wider than yours.
4. **Then** merge in repaired form into a single active file, crediting the source.

Never trust the source repository's own report that it passes. Re-run the compiler on the exact
artifact (`HARDNESS.md` H8).

## Shared mathematical objects

Three streams carry their own account of the T-dual effective radius:

```
Reff(α, R) = max(R, α/R)
```

Stream 1 has it in Lean as the geometric inspiration for the Navier–Stokes cutoff; Stream 4 as
a rulial inversion; Stream 6 as the `RulialInversionHook`. **Nothing detects when they drift.**

Until a shared Tier A definition exists (Roadmap Stage 4): when you touch one copy, check the
others and record any divergence you find as a Tier C observation. Do not unify them
unilaterally — the differences may be deliberate, and deciding that is the streams' call.

## The Mathlib dependency

Stream 1's Gate 2 compiles against **Stream 5's** working tree
(`~/xdev/SocrateAI-Scientific-RajMathRecovery/dualscale/lean`). Only a subset of Mathlib is
built there, and `import Mathlib.Tactic` is generally **not** among it.

Consequences when working across these two:
- Check an `.olean` exists before importing a new module.
- A change to Stream 5's tree can break Stream 1's gate with no change to Stream 1.
- Do not "clean up" that directory. Other streams' gates depend on it.

Stream 0 owns fixing this (`PLAN.md` K1).

## Before crossing

- [ ] Source stream's tier definition read, not assumed
- [ ] Tier re-derived from the admission criterion, not translated from the letter
- [ ] Imported artifact re-compiled or re-run here; footprint checked against *your* allowlist
- [ ] Source id recorded in `supports`
- [ ] Your row's tier does not exceed the source's
- [ ] Divergence in shared objects recorded rather than silently reconciled

## Never

Modify another stream's gate, ledger, or working tree without its owner's agreement. Stream 0
proposes; the streams dispose. That applies most strongly to the stream that ships the tools.
