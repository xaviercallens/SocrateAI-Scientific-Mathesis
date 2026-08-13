# ROADMAP.md — staged plan

**Calendar is aspirational; `PLAN.md` is operational.** Where the two conflict, `PLAN.md`
wins; where `PLAN.md` conflicts with `SPEC.md`'s rules, `SPEC.md` wins.

Stages are gated by *state*, not by date. A stage is entered when its predecessor's exit
criteria are mechanically true — not when the calendar says so.

---

## Stage 0 — Foundations ✅ *(2026-08-13)*

Build the notation, prove the theorem about it, and gate the whole thing.

| Deliverable | State |
|---|---|
| Tier lattice + soundness theorem in Lean 4, Mathlib-free | ✅ `MX-A-0001`…`MX-A-0004`, footprints as declared |
| Python reference checker | ✅ `python/mathesis/` |
| Independent Rust checker, zero dependencies | ✅ `rust/mathesis-verify/`, 11 unit tests |
| Four-gate `verify.sh` | ✅ all green; Gate 2 demonstrated to fail on a planted `sorry` |
| Stream 0's own ledger | ✅ 9 rows, `Sound`, Gate 4 cross-checks `LEDGER.md` ↔ `ledger.jsonl` |
| Claude skills | ✅ `.claude/skills/` |
| Cross-stream collision documented | ✅ `MX-C-0001`, `docs/TIER_CALCULUS.md` |

**Exit criterion not yet met:** the human statement-adequacy audit of the Lean core. The
kernel has checked the proofs; nobody has yet certified that `Sound` is the right condition.
Stage 0 is *built* but not *signed off*, and the ledger says so.

## Stage 1 — Adoption

Get one real stream's claims into the notation, and let the notation lose the resulting
argument.

**Deliverables**
1. `MX-C-0001` promoted to Tier B — a harness checking both trees at pinned commits.
2. One stream, chosen with its owner, exports its existing claims to `ledger.jsonl`.
3. `mathesis-verify` callable from another repository's CI in one line.
4. The Tier B/L migration **proposed** to Streams 1 and 5. Proposed, not imposed.

**Exit criterion:** one stream's CI runs Gate 4 against its own ledger, and it passes.

**The risk worth naming.** The schema is currently untested against reality — it was designed
by reading other streams' documents, not by migrating their history. A real ledger with real
provenance will break it. That is the point of doing this early and with one stream rather
than six.

## Stage 2 — Kernel service

End the situation where one stream's gate depends on another stream's working tree.

**Deliverables**
1. A pinned, cold-buildable Mathlib owned by Stream 0, with a documented path and a `lake`
   manifest under version control.
2. Stream 1's Gate 2 repointed at it — closing a Stage-0 chore that stream has carried open.
3. A cold-build CI job, so "works on the machine where it was built" stops being the standard.

**Exit criterion:** Stream 1's `verify.sh` passes with `LEAN_ENV_DIR` pointing at Stream 0,
from a clean checkout with no `.olean` cache.

## Stage 3 — The Claude 5 loop

Implement `docs/CLAUDE5_LOOP.md`: propose → refute → check → formalize → **human audit** →
ledger.

**Deliverables**
1. Stages 0–2 (propose, refute, check) as a runnable pipeline against one stream's open
   problems.
2. Stage 3 (formalize) with the effort-tier split enforced: top-tier authors statements,
   executing agents implement specified skeletons, never the reverse.
3. Stage 4 (audit) as a **human workflow with tooling** — a review packet that makes the
   audit fast, never a system that performs it.
4. Kill-rate instrumentation. A loop that promotes everything it proposes is broken, and the
   ratio is the diagnostic.

**Exit criterion:** one full cycle ending in a ledger row — *including one candidate that
fails the human audit and is recorded as failing.* A loop that has never produced a rejection
has not been tested.

## Stage 4 — Universal notation

The shared mathematical objects, defined once.

**Deliverables**
1. `Reff(α,R) = max(R, α/R)` as one audited Tier A definition, imported by Streams 1, 4, 6
   instead of re-derived in each.
2. The Sym² recurrence lock, likewise.
3. A drift detector: when a stream's local copy of a shared object diverges, the gate says so.

**Exit criterion:** at least two streams importing the shared definition, with their local
copies deleted rather than left alongside.

## The Frontier — unscheduled

`FRONTIER.md`. Not promised, not planned, and deliberately not given dates: the cross-stream
ledger, proof-carrying claims, the Leibniz test, retraction infrastructure.

---

## What would make this roadmap wrong

Stated in advance, so the answer is not constructed after the fact:

- **No stream adopts the notation.** Then Stream 0 is infrastructure for nobody, and the right
  move is to shrink it to the one thing that had independent value — the collision finding —
  and stop.
- **The tier calculus survives contact with a real ledger unchanged.** Suspicious rather than
  reassuring: it would mean the schema was designed to fit what was already easy to record.
- **Gate 3 never disagrees again.** Either the corpus stopped growing with the code, or the
  two implementations have quietly converged on one author's assumptions.
- **The human audit backlog grows without bound.** Then the loop is producing formalizations
  faster than anyone can certify they mean anything, and the correct response is to slow the
  loop — not to automate the audit.
