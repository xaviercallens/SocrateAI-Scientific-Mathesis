# HARDNESS.md — structural invariants

*The rules that do not bend under schedule pressure. Adapted from Stream 6's
`Best_Practices_and_Hardness.md` and Stream 1's `SPEC.md` §7, generalized to the whole program.*

An invariant differs from a preference in one way: **there is a mechanical check that fails
when it is violated.** Every entry below names its check. An entry that loses its check is
not an invariant any more, and should be moved to `FRONTIER.md` as an aspiration until the
check comes back.

---

## H1 — Zero-sorry verification

Every Tier A claim is Lean 4 kernel-compiled with zero `sorry` and an axiom footprint matching
the allowlist its file declares.

**The check is `#print axioms`, never the source text.** A failed proof still defines the
theorem name in the environment; grepping for `sorry` finds nothing and the `sorryAx` is
right there in the footprint. Stream 1 caught two broken proofs this way that a concurrent
process had reported as passing.

*Enforced by:* `scripts/verify.sh` Gate 2. *Demonstrated to fail:* a planted `sorry` was
rejected on 2026-08-13 (`LL.md` LL-2).

## H2 — The negative control is the checker

Every Tier B harness ships a control that is **demonstrated to fail**, and Gate 1 fails if the
control passes. A checker that cannot fail is not a checker.

The control that matters is not the one proving the harness rejects garbage. It is the one
proving the harness rejects the *plausible near-miss* — for the tier calculus, a ledger sound
at every direct edge and unsound transitively. Without that case, a one-hop implementation
passes every test and the theorem is decoration.

*Enforced by:* Gate 1. `tests/tier_b_tier_calculus.py` ships 5 controls,
`tests/tier_b_no_floats.py` ships 2.

## H3 — Exact arithmetic in every certified path

`fractions.Fraction` and `int` only. Floats are confined to `exploration/`, behind a
`# TIER X — EXPLORATORY, NO CLAIMS` banner.

Checked by AST walk, not grep — `x = 1.5` is a violation, `"version 1.5"` and `# 1.5x faster`
are not. A grep version produces false positives, gets disabled, and stops protecting
anything; that is how these rules actually die.

*Enforced by:* `tests/tier_b_no_floats.py`, Gate 1.

## H4 — Two implementations, no shared dependency

The ledger checker exists in Python and in Rust, each written against `SPEC.md` rather than
against the other. Gate 3 compares them on an enumerated corpus. **When they disagree, neither
is trusted** until a human adjudicates (E-3).

The Rust crate has no crates.io dependencies, including its JSON parser. A differential gate
whose two sides call the same library tests that library once and the ledger logic zero times.

*Enforced by:* Gate 3, 30 corpus cases. *Already earned its keep:* it caught a real divergence
on its first run (`LL.md` LL-3).

## H5 — Non-vacuity

Every definition ships a witness; every theorem ships an `example` instantiating its
hypotheses; every predicate ships **both** a satisfying and a violating instance.

A `Sound` theorem with no exhibited *unsound* ledger is not evidence that `Sound` says
anything — it is consistent with `Sound` being identically true. Stream 5 reached the same
rule independently (its CI rule R3 bans theorem statements of type `True`), which is the
strongest available evidence that it belongs in the shared layer.

*Enforced by:* review, plus the `witness*` lemmas in `TierCalculus.lean` (both polarities).

## H6 — No claim outside the ledger

A claim absent from `LEDGER.md` has no tier and may not be cited. The machine-readable
`ledger.jsonl` and the human-readable `LEDGER.md` must name the same identifiers — two
ledgers that drift apart are worse than one.

*Enforced by:* Gate 4.

## H7 — Tier monotonicity

No claim is filed at a tier above anything it rests on, **transitively**. A Tier A claim's
entire transitive support set is Tier A.

This is the one invariant that is also a theorem (`MX-A-0003`, `MX-A-0004`). Its consequence
is load-bearing and people will trip over it: a Lean proof needing a literature result must
take that result as an explicit hypothesis parameter, making the theorem conditional, with the
condition recorded.

*Enforced by:* Gate 4, mirroring `lean/Mathesis/TierCalculus.lean`.

## H8 — Agent self-reports are not evidence

Independently re-run the compiler or harness on the exact artifact before trusting or
committing it. This applies to Stream 0's own reports about itself.

Corollary, recorded after it happened twice in one session in Stream 1: **`git add` by
explicit path, never `-A` or `.`, while any background process might be writing to the repo.**
A broad `add` stages whatever is on disk at that instant, including another agent's file
mid-edit, before its gate ran.

*Enforced by:* review discipline. **This is the weakest invariant in the list** — it has no
mechanical check, which is exactly why it is stated loudly and why it is the one most likely
to be violated.

## H9 — Determinism

No wall-clock, no unseeded randomness, no network access in anything a gate depends on. Every
dataset ships its generating command and `sha256sum`. The differential corpus is enumerated by
hand, not generated randomly, so that a Gate 3 failure names a specific reproducible file.

*Enforced by:* corpus construction; review.

## H10 — Stream 0 takes no dependency it cannot rebuild in a minute

The Lean core is **Mathlib-free** and cold-builds in ~2 seconds. The Rust crate has no
dependencies. The Python package uses only the standard library.

This is not minimalism for its own sake. Stream 0's gate is the thing every other stream will
eventually call; if it can be broken by an upstream change, it becomes the reason another
stream is blocked. Stream 1's current situation — its Gate 2 compiling against Stream 5's
working tree — is the failure mode being avoided.

*Enforced by:* `Cargo.toml` has an empty `[dependencies]`; the Lean core has no `import`.

---

## What is deliberately *not* an invariant

**"Claims must be true."** Not checkable, and pretending otherwise is the failure this whole
apparatus exists to prevent. Every gate here checks *consistency of the record*. Whether a row
deserves its tier is a human audit (SPEC.md §2.4).

**"Tier A means important."** The tier order is citation strength — how much of the checking a
machine did. A Tier L theorem of Bourgain is deeper than every Tier A row in this repository.

**"The gates are sufficient."** They are necessary. A green board means the bookkeeping holds;
it licenses no scientific claim whatsoever (SPEC.md §7.9).
