---
name: mathesis-tier-gate
description: Assign or promote the epistemic tier (A/B/L/C/X) of a scientific claim in any SocrateAI stream. Use whenever about to write down what is known — a result, a conjecture, a citation, a measurement — or when asked whether something "counts", is "verified", "proven", "established", or can be cited. Also use before promoting a claim, before citing another stream's result, and before any statement that a milestone is met.
---

# Tier gate

The tier is not a label added after the work. It is a **question about what actually did the
checking**, and it must be answered before the claim is written down.

## The decision, in order

Ask these in sequence and stop at the first "yes".

1. **Did the Lean kernel accept it, with the file's declared axiom footprint and no `sorry`?**
   → **Tier A**.
   The gate is `#print axioms`, *never* the absence of the word `sorry` in the source. A failed
   proof still defines the theorem name; only the footprint reveals the `sorryAx`.

2. **Did a deterministic exact-arithmetic program decide it, and does that program ship a
   negative control demonstrated to fail?** → **Tier B**.
   `Fraction`/`int` only. No control, no Tier B — a checker that cannot fail is not a checker.

3. **Is it a theorem in peer-reviewed literature, and do you have the theorem statement
   quoted?** → **Tier L**.
   An abstract is not a theorem statement. A retrieval summary is not a theorem statement. If
   you have not read the statement, you have a Tier C belief *about* a paper.

4. **Is it floating point, sampled, plotted, or model-generated?** → **Tier X**. Uncitable.

5. **Otherwise** → **Tier C**.

## Evidence caps the tier

The evidence kind is a ceiling, independent of how convincing the result is:

| evidence_kind | caps at |
|---|---|
| `lean_axioms` | A |
| `exact_harness` | B |
| `citation` | L |
| `argument` | C |
| `numeric`, `llm_output` | X |

`llm_output` caps at X by charter: no LLM output gates a tier promotion. This includes your
own output. If you derived something convincing and nothing else checked it, it is Tier C at
best — and if it came out of a model, X.

## Promotion

A promotion **changes the identifier**, because the tier letter is in it:

```
MX-C-0001  →  MX-B-0004    (new id; the old row records `supersedes`)
```

Never edit a tier letter in place. The renumbering is the feature: it makes every stale
citation lexically wrong instead of silently wrong.

Promotion requires the *new* tier's admission criterion to be met **now**, by an artifact a
gate can re-run. "We're confident it would pass" is Tier C.

## The rule that catches people

**A claim may not be filed above anything it rests on — transitively.**

So a Tier A theorem may not cite a Tier L result. If a Lean proof needs a published theorem as
an input, take it as an **explicit hypothesis parameter**, visible in the theorem's type. The
result is then Tier A *conditionally*, and the ledger records what it is conditional on. Never
introduce it as an `axiom`: that pollutes every downstream footprint and hides the dependency
from the gate.

Check the closure, not just the direct edges. `B → B → L` is sound at every direct edge and
still means the head rests on literature.

## Before writing any claim down

- [ ] Tier assigned by the ladder above, not by how confident it feels
- [ ] Evidence kind declared, and it permits that tier
- [ ] Every support id is at that tier or higher, **transitively**
- [ ] Artifact path recorded — the thing a gate re-runs
- [ ] For Tier A: statement-adequacy audit noted as done, or explicitly as pending
- [ ] Row added to **both** `LEDGER.md` and `ledger.jsonl`, same commit as the artifact

## What never gets a tier

Adjectives. "Strong evidence", "promising", "essentially proven", "clear". Report the tier, the
number, and the path. Adjectives are how a Tier C result becomes a Tier A memory eighteen
months later.

Reference: `SPEC.md` §2, `docs/TIER_CALCULUS.md`.
