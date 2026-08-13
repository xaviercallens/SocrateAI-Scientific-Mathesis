---
name: mathesis-claude5-loop
description: Run the autoformalization loop for a SocrateAI stream — propose conjectures, refute them cheaply, certify survivors in exact arithmetic, formalize in Lean, then hand to a human audit. Use when asked to search for results, generate or test conjectures, formalize a body of mathematics, or set up an automated discovery pipeline.
---

# The Claude 5 loop

```
0 PROPOSE  →  1 REFUTE  →  2 CHECK  →  3 FORMALIZE  →  4 ██ HUMAN AUDIT ██  →  5 LEDGER
  Tier X       most die     Tier B       Tier A            citable              recorded
```

The design goal is not throughput. It is that **nothing reaches the ledger without something
other than a model having checked it.**

## Stage 0 — Propose (Tier X)

Generate candidates from the stream's ledger, open problems, and design memos. Volume is fine;
the output is worthless until something survives downstream.

**The proposer must not see the gate.** A generator that can observe which candidates pass will
learn to produce candidates that pass — which is not the same as candidates that are true.

## Stage 1 — Refute before proving

Run the falsification sweep **first**: degenerate inputs, boundary cases, exact-arithmetic
checks at small parameters.

This inverts the instinct and it is worth real effort. A false conjecture absorbs unbounded
proof time and returns nothing; a five-second sweep kills most of them. Stream 1 found a
convolution formula — sourced from a web search — that was **identically zero**, caught at
M = 1, 2, 3 by exact arithmetic. No amount of proof effort would have surfaced it: the
statement was perfectly provable and perfectly useless.

Expect most candidates to die here. That is the stage working.

## Stage 2 — Check (Tier B)

Deterministic exact-arithmetic harness, `Fraction`/`int` only, with a negative control
demonstrated to fail. Wire it into the gate in the same commit. *(See the
`mathesis-exact-harness` skill.)*

## Stage 3 — Formalize (Tier A proof, not yet citable)

Claude writes Lean; the kernel decides. *(See the `mathesis-lean-kernel` skill.)*

The effort split is not optional:

> **A top-tier model authors the statement and derives the mathematics in a design memo. An
> executing agent implements a fully-specified skeleton. Never the reverse.**

An agent handed an under-specified goal will invent a definition to fill the gap, and a
hallucinated definition passes every gate. If the skeleton is not fully specified, that is an
E-1, not something to work around.

## Stage 4 — ██ HUMAN AUDIT ██

**A theorem is Tier A when the kernel accepts it. It is *citable* only after this stage.**

The kernel confirms the proof establishes the statement. Nothing mechanical confirms the
statement is the one anyone meant. The auditor answers:

- Does the formal statement say what the informal gloss claims?
- Are the hypotheses non-vacuous — is there a witness satisfying them?
- **Are the quantifiers where the science needs them?**

The third is where formalizations actually fail. Stream 1's Hypothesis U is
`sup_{α′>0} sup_t ‖∇u^(α′)(t)‖_{L²} < ∞` — quantified *over* α′, its whole content being the
α′ → 0 limit. Fix α′ as a global constant and every symbol still typechecks, every proof still
compiles, and the claim has quietly become a much weaker one. No kernel catches that.

**Do not automate this.** Not with an LLM judge, not with a heuristic, not "provisionally to
unblock the pipeline". No LLM output gates a tier promotion — including yours. This is the one
step whose result cannot be predicted from the loop's own signals, which is exactly why it
cannot be removed to go faster.

What you *may* build is **tooling that makes the audit fast**: a review packet with the
statement, its gloss, its witnesses, its hypotheses, and the design memo side by side.

## Stage 5 — Ledger

Artifact, `LEDGER.md` row, `ledger.jsonl` row, and gate output in **one commit**.

## Reading the loop's health

The diagnostic is the **kill ratio**, not the promotion count.

| Symptom | Diagnosis |
|---|---|
| Almost everything proposed gets promoted | Broken. Either stage 1 is not refuting or the proposer is seeing the gate |
| Nothing survives stage 1 | The proposer lacks context; seed it from the ledger and the design memos |
| Everything passes the human audit | Suspicious — either statements are trivial, or the audit has become a rubber stamp |
| The audit backlog grows without bound | The loop is outrunning certification. **Slow the loop.** Do not automate the audit |

A good run: 400 proposed, 380 refuted, 15 certified at B, 4 formalized, **1 failing the human
audit and recorded as failing**. A loop that has never produced a rejection has not been tested.

## Never

- Promote a tier on your own judgment
- Weaken a statement so a proof closes (E-4)
- Invent a definition to fill a gap (E-1)
- Cite your own output as evidence — `llm_output` caps at Tier X, always
- Report adjectives instead of gate output

Full specification: `docs/CLAUDE5_LOOP.md`.
