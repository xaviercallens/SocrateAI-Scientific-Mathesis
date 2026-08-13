---
name: mathesis-ledger
description: Record, validate, or query a claim in a SocrateAI stream ledger (LEDGER.md and ledger.jsonl). Use after producing any result worth keeping, when asked what a stream knows or has proven, when a ledger check fails, or when citing a result from another stream.
---

# The ledger

**A claim absent from the ledger has no tier and may not be cited.** That is the whole
contract. A result that exists only in a commit message, a report, or a conversation is not
part of what the program knows.

## Two files, one truth

| File | For | Gate |
|---|---|---|
| `ledger.jsonl` | machines — one JSON object per line | checked by the tier calculus |
| `LEDGER.md` | humans — tables with context and caveats | must name the same ids |

Gate 4 fails if they disagree. Update **both**, in the same commit as the artifact. Two
ledgers that drift apart are worse than one.

## A row

```json
{"id": "MX-A-0003", "tier": "A", "stream": "Mathesis",
 "statement": "Transitive tier monotonicity: in a Sound ledger, Depends L a b implies (L a).tier <= (L b).tier.",
 "evidence_kind": "lean_axioms",
 "artifact": "lean/Mathesis/TierCalculus.lean#tier_le_of_depends",
 "supports": ["MX-A-0001"], "audited_by": null, "supersedes": null}
```

**`id`** — `<STREAM>-<TIER>-<NNNN>`. Streams: `MX` Mathesis, `MF` MechanicaFluidorum,
`AE` AutoEvolve, `QK` Quantum, `HG` Hypergraph, `RM` RajMath, `TN` TNN, `VD` Videoo.

**`statement`** — one self-contained sentence. A reader must be able to tell what would falsify
it without opening the artifact. No adjectives.

**`artifact`** — the thing a gate re-runs: file plus declaration names, a harness path, or for
Tier L the citation **with the quoted theorem statement**.

**`audited_by`** — who signed the statement-adequacy audit. `null` means NOT AUDITED. For a
Tier A row that means the kernel checked the proof and nobody has yet certified the statement
means what its gloss says. **Never set this to a model.**

**`supports`** — ids this rests on. Every one must be at this tier or higher, transitively.

## Running the check

```bash
PYTHONPATH=python python3 -m mathesis check ledger.jsonl     # reference
rust/mathesis-verify/target/debug/mathesis-verify check ledger.jsonl   # independent
./scripts/verify.sh --gate 4
```

## Reading the findings

| Code | Meaning | Fix |
|---|---|---|
| `E-UNSOUND` | filed above something it rests on, directly or transitively | lower the row's tier, or raise the support's — by earning it |
| `E-TIERMATCH` | the id's letter disagrees with the `tier` field | a promotion must change the **id**; never edit a letter in place |
| `E-EVIDENCE` | evidence kind cannot support that tier | the row is overclaiming; the cap is not negotiable |
| `E-DANGLING` | cites an id with no row | add the row, or stop citing it |
| `E-UNCITABLE` | cites a Tier X row | X may never be cited. Certify it at B first |
| `E-CYCLE` | the support graph has a cycle | a real modelling error — two claims justifying each other |
| `E-DUP` | two rows share an id | — |
| `E-SCHEMA` | malformed row or id | — |

**`E-UNSOUND` on a row whose direct citations all look fine** is the transitive case, and it is
the finding this system exists for. Read the whole chain.

## Promotion

The tier is in the id, so a promotion creates a **new row**:

```
MX-C-0001  (Tier C observation)
   ↓  a harness now decides it
MX-B-0004  with  "supersedes": "MX-C-0001"
```

This invalidates existing citations of the old id — deliberately. A stale citation becomes
lexically wrong instead of silently wrong.

## Citing another stream

1. Check the tier letter means what you think. Two streams currently use **B** for
   incompatible things (`docs/TIER_CALCULUS.md` §1). Until the migration lands, treat an
   imported letter as untyped and verify against the source stream's own definition.
2. Your row may not exceed the cited row's tier.
3. Record the cited id in `supports`, not the prose description.

## Before committing

- [ ] Row in **both** files, same commit as the artifact
- [ ] `statement` self-contained, no adjectives
- [ ] `artifact` points at something a gate re-runs
- [ ] `supports` complete — including what you assumed without noticing
- [ ] `audited_by` set, or `null` and the pending audit noted in `LEDGER.md`
- [ ] `./scripts/verify.sh --gate 4` green
