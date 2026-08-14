# mathesis-gate

A portable verification gate for Lean repositories. **One file, no dependencies,
Python 3.9+ standard library only.**

```bash
curl -O https://raw.githubusercontent.com/xaviercallens/SocrateAI-Scientific-Mathesis/main/tools/mathesis-gate/mathesis_gate.py
python3 mathesis_gate.py . --lean-src lean_src --report-only
```

It does not import from Mathesis and does not need that repository present.

## What it checks

| Check | Catches |
|---|---|
| **axiom hygiene** | `axiom` declarations and `sorry`, at any indentation, `private`/attributed included |
| **vacuity** | `... : Prop := True` predicates, theorems concluding one, and `def Real := Float` type shadowing |
| **footprints** | every module's `#print axioms` output against the allowlist that module declares |
| **ledger** | tier soundness across the **transitive** closure, evidence caps, cycles, dangling ids |

Each is independently switchable (`--skip-hygiene`, `--skip-vacuity`,
`--skip-footprints`), because a gate you cannot adopt incrementally is a gate
nobody adopts. `--report-only` prints findings and exits 0, so you can land it
in CI before you have fixed anything.

## Why the vacuity check exists

A file can be entirely free of `axiom` and `sorry`, pass every other check, and
still assert nothing:

```lean
def uniformBoundedness (D : EnstrophyFunctional) : Prop := True

/-- Ramanujan's sum of tails bounds the ultra-high-frequency modes,
    proving Hypothesis U. -/
theorem hypothesis_U_bound (D : EnstrophyFunctional) : uniformBoundedness D := by
  trivial
```

The Lean is honest. The **docstring** carries the claim, and no gate reads
docstrings. This shape was found in the wild while building this tool, which is
why the check is here.

## The gate is the footprint, not the source

A failed proof still defines the theorem name in the environment: the source
contains no `sorry` and `#print axioms` reports `sorryAx`. **Any check that
greps the source for `sorry` will pass a broken proof.** This one asks the
kernel.

## Declaring a contract

A module opts in to the footprint check from its own header:

```lean
/-
  MATHESIS-GATE: env=mathlib
  MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound
  MATHESIS-GATE: allow(witness)=propext   -- prefix-scoped override
-/
```

`allow=` with an empty value means **no axioms at all**. Modules without a
directive are skipped by the footprint check and still scanned for hygiene and
vacuity, so you can adopt file by file.

The allowlist is **per declaration class**, not per file, because a file-wide
list is only as tight as its loosest declaration.

## Adoption path

```bash
# 1. See where you stand. Never fails.
python3 mathesis_gate.py . --lean-src lean_src --report-only

# 2. Land it in CI non-blocking, so the number is visible and cannot grow silently.
# 3. Declare contracts on the modules you have already cleaned.
# 4. Drop --report-only when the count reaches zero.
```

## Self-tests

Thirteen negative controls run on **every invocation**, before any file is
examined, and the gate exits non-zero if they fail. A gate that has only ever
been observed passing is indistinguishable from one that cannot fail.

```bash
python3 mathesis_gate.py --self-test
```

They cover the shapes that have actually defeated earlier versions: an indented
axiom, a `private` axiom, an axiom in a nested block comment, and a **wrapped**
`#print axioms` line — Lean wraps past its line width, and a line-anchored
parser silently drops those, producing a false all-clear in the one check that
evidences a kernel-verified claim.

## CI

`github-workflow.yml` in this directory is a ready-made GitHub Actions job.

## What it does not do

It does not read docstrings, judge whether a statement is the one you meant, or
issue a verdict about your science. **A green board says the bookkeeping holds.**
Whether a theorem says what its gloss claims is a human audit, and this tool is
explicitly not it.

MIT. Part of SocrateAI Stream 0 (Mathesis).
