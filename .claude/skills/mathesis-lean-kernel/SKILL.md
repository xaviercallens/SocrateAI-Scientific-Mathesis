---
name: mathesis-lean-kernel
description: Write, compile, and verify Lean 4 proofs to Tier A standard across the SocrateAI streams — checking axiom footprints, avoiding sorry and custom axioms, adding non-vacuity witnesses, and handling the shared Mathlib build. Use when writing or reviewing any .lean file, when a proof will not close, when checking whether a theorem is really verified, or when a Lean build fails.
---

# Lean kernel work

## The gate is the footprint, not the source

```lean
#print axioms Namespace.theorem_name
```

**Never accept "there is no `sorry` in the source" as evidence.** A failed proof still defines
the theorem name in the environment. The source looks clean; the footprint says `sorryAx`.
Stream 1 caught two broken proofs this way that had been reported as passing.

Every file declares its allowlist in its header, **per declaration class**, and the gate
enforces that map. Stream 0's core declares:

```
theory declarations   : []          -- no axioms at all
witness declarations  : [propext]   -- decide-only; inherited from core's Fin decidability
```

If your edit changes a footprint, **amend the declaration, not the check.** Loosening the check
is one character and re-deriving the claim is a paragraph — that asymmetry is exactly how a
declared property goes stale (`LL.md` LL-2).

## Never do these

- **Never add `axiom`.** Unproven infrastructure enters as an explicit **hypothesis parameter**,
  visible in the theorem's type. `axiom c_pos : 0 < c` pollutes every downstream footprint
  forever. (`opaque c : ℝ` adds no axiom and is preferable when you need an opaque constant —
  but any `axiom` *about* it still pollutes.)
- **Never weaken a statement to make a proof close.** If it will not prove, that is a finding.
  Escalate (E-4). This is the rule most likely to be violated by anything optimizing for a
  green check.
- **Never fix a quantified parameter as a global constant.** If the science quantifies over it,
  the formalization must too — everything still typechecks after you fix it, and the statement
  has silently become a weaker one. Stream 1's Hypothesis U is the canonical case: its entire
  content is the α′ → 0 limit, and fixing α′ destroys that while compiling perfectly.
- **Never create `_v2` / `_final` / `verify_*.lean` files.** One active file per module; git
  history is the archive.

## Always do these

**Ship a witness with every definition** and an `example` instantiating every theorem's
hypotheses. For a predicate, ship **both polarities** — a satisfying instance *and* a violating
one. A `Sound` theorem with no exhibited unsound instance is consistent with `Sound` being
identically true.

```lean
theorem witnessSound_sound : Sound witnessSound := by ...
theorem witnessUnsound_not_sound : ¬ Sound witnessUnsound := by ...   -- the one that matters
```

**Guard junk values.** Lean's `x / 0 = 0` and "integral of non-integrable = 0" make vacuous
theorems easy to state and hard to notice. Every division and every integral inside a Tier A
statement carries a witnessed side condition.

## Building

Stream 0's own core is **Mathlib-free** and needs nothing:

```bash
cd lean && lean Mathesis/TierCalculus.lean     # ~2 seconds, no imports
```

For streams that need Mathlib: the build is currently a shared checkout, and
`import Mathlib.Tactic` is generally **not** built — import narrow modules
(`Mathlib.Tactic.Ring`, `Mathlib.Tactic.Linarith`). Check before importing:

```bash
ls "$LEAN_ENV_DIR"/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/<Path>.olean
```

Compile a single file against it:
```bash
cd "$LEAN_ENV_DIR" && lake env lean /abs/path/to/File.lean
```

**Prefer no Mathlib when the mathematics is elementary.** A dependency-free file cold-builds in
seconds and cannot be broken by another stream's build state.

## When a proof will not close

In order:

1. Re-read the statement. Is it *true*? Try to refute it at small parameters in exact
   arithmetic first — this is cheaper than proof effort and kills most bad conjectures.
2. Check for a missing hypothesis. If the statement needs one it does not have, that is a
   finding about the statement, not a proof problem — escalate rather than adding it silently.
3. Check junk values. Division or integral without a side condition?
4. **Do not** weaken the goal. **Do not** add an axiom. **Do not** `sorry` it and move on.

Three genuinely different failed repairs → **E-2**. Tempted to change what the theorem says →
**E-4**, always.

## Checklist before claiming Tier A

- [ ] Compiles from a clean state
- [ ] `#print axioms` printed for every theorem, matching the header's declared allowlist
- [ ] Zero `sorry` — confirmed by footprint, not by grep
- [ ] Zero custom `axiom` declarations
- [ ] Witnesses present; both polarities for predicates
- [ ] Wired into `scripts/verify.sh` Gate 2
- [ ] Statement-adequacy audit done by a **human**, or the row explicitly records it as pending

That last box is not a formality. The kernel confirms the proof establishes the statement.
Nothing mechanical confirms the statement is the one anyone meant.
