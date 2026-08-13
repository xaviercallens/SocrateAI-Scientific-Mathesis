# SocrateAI-Scientific-Mathesis — Stream 0

> *la mathesis universalis de Leibniz, le programme d'une notation formelle universelle au
> service de toutes les sciences, est littéralement la fiche de poste de ce stream 0*

The shared **notation**, **verification kernel**, and **epistemic bookkeeping** for the
SocrateAI scientific streams. Stream 0 does no science of its own. Its object of study is the
record: the first theorem here is about ledgers, not about geometry.

```
$ ./scripts/verify.sh
PASS  Gate 1 (2 harness(es))                             Tier B: exact arithmetic + controls
PASS  Gate 2                                             Tier A: Lean kernel + footprints
PASS  Gate 3 (30 corpus case(s), both implementations agree)   differential
PASS  Gate 4                                             ledger integrity
ALL GATES PASS
```

---

## Why

Six scientific streams run concurrently — Navier–Stokes regularity, K3 selection in the
DualScale K3×T² landscape, quantum landscape search, hypergraph cosmology, the Ramanujan
engine, the TNN Univers Model. They already share mathematics. They do **not** share a way of
saying how well any of it is known.

That gap has a measured consequence. Two streams use the letter **B** for incompatible things:

| Stream 1 | Stream 5 |
|---|---|
| *"**B — Checkable**: identities validated in exact rational arithmetic; no floats"* | *"**Tier B — Established**: Peer-reviewed literature, pinned to exact values"* |

One means *a program checked it*. The other means *a referee checked it*. Artifacts already
cross between those repositories — Stream 1's Lean gate compiles against Stream 5's working
tree, and imports a theorem from it. The day a **claim** crosses with its letter attached, a
citation silently becomes a computation, and nothing in either repository notices.

Full account with both definitions quoted: [`docs/TIER_CALCULUS.md`](docs/TIER_CALCULUS.md).

## What Stream 0 ships

**A notation.** Five tiers in one linear order, plus an orthogonal *evidence kind* that caps
what a row may claim — the two axes that were being conflated into one colliding letter.

```
X  <  C  <  L  <  B  <  A

A  kernel-verified      Lean 4, zero sorry, declared axiom footprint
B  exact-arithmetic     deterministic ℚ/ℤ check + a negative control that fails
L  literature           peer-reviewed, quoted theorem statement — not an abstract
C  conjecture           proposal, analogy, unverified reduction
X  exploratory          floats, sampling, LLM output — may never be cited
```

**A theorem about that notation.** A ledger is `Sound` when no claim is filed above anything it
*directly* cites. The kernel-verified result is that soundness then holds across the entire
**transitive** closure:

```lean
theorem tier_le_of_depends (hL : Sound L) :
    ∀ {a b : ι}, Depends L a b → (L a).tier ≤ (L b).tier

theorem no_kernel_claim_rests_on_weaker (hL : Sound L)
    (ha : (L a).tier = Tier.A) (hab : Depends L a b) : (L b).tier = Tier.A
```

Elementary mathematics — and that is the point. It earns a kernel proof not because it is hard
but because transitivity is *the property informal bookkeeping loses first*. Every stream
already checks the direct condition by eye. None checks the closure. A chain `B → B → L` is
sound at every direct edge and still rests on literature.

**Three implementations that must agree.** The theorem in Lean 4; a Python reference checker; an
independent Rust checker sharing no dependency with it — not even a JSON library. Gate 3 runs
the two checkers over 30 enumerated cases and fails the build if they disagree, *without
adjudicating which is right*, because that is a question for a human.

It earned its keep immediately: it caught a real divergence on its first run
([`LL.md`](LL.md) LL-1).

## Layout

```
SPEC.md          normative rules            HARDNESS.md   structural invariants
PLAN.md          tasks, DoD, escalation     FRONTIER.md   TODO / NOTODO / Frontier
LEDGER.md        claim inventory            ROADMAP.md    staged plan
ledger.jsonl     the same, machine-readable LL.md         lessons learned, with evidence

lean/Mathesis/   Tier A core — Mathlib-free, cold-builds in ~2s
python/mathesis/ reference checker — standard library only, no floats
rust/            independent checker — zero dependencies, by design
tests/           Tier B harnesses + the differential corpus
scripts/         verify.sh — the four gates
docs/            VISION · STREAM_MAP · TIER_CALCULUS · CLAUDE5_LOOP
.claude/skills/  skills for agents working across the streams
```

## Quick start

```bash
./scripts/verify.sh                          # all four gates
cd lean && lean Mathesis/TierCalculus.lean   # the Tier A core alone (~2s, no Mathlib)
cd rust/mathesis-verify && cargo test        # the independent implementation
PYTHONPATH=python python3 -m mathesis check ledger.jsonl
```

## What Stream 0 is not

- **Not an oracle.** `Sound` is a consistency property of a *record*, not of the science. A
  ledger in which every row is Tier C is perfectly sound and completely worthless. Whether a
  row deserves its tier is a human audit.
- **Not a license.** A green gate says a stream's records are internally consistent. It says
  nothing about Navier–Stokes, K3 selection, or the universe.
- **Not an authority.** The migration proposed in `docs/TIER_CALCULUS.md` §3 has been adopted
  by nobody, and will not be filed as a request until the observation behind it is Tier B —
  asking on the strength of a Tier C reading would be the exact error it describes.

## Status

Stage 0 complete, **not yet signed off**: the five Tier A rows are kernel-verified and await
the human statement-adequacy audit (`PLAN.md` A1). Both Lean modules are marked `DRAFT`, not
`AUDITED` — compilation is not adequacy. Stream 0's ledger currently has the very gap it exists
to close in others, and says so.

Built against the received [`SPEC-STREAM0 (DRAFT)`](docs/SPEC-STREAM0-DRAFT-received.md);
every deviation, and two findings where that draft's premises did not survive contact with the
working trees, are recorded in [`docs/designs/RECONCILIATION.md`](docs/designs/RECONCILIATION.md).

---

*Part of the [SocrateAI](https://github.com/xaviercallens) scientific program.
`calculemus` was never a promise that the calculation would succeed — only that when it
didn't, everyone would be able to see exactly where.*
