# The Claude 5 Loop — autoformalization with the human audit welded in

**Status:** specification, Tier C. No stage below is implemented. This document says what
must be built and, more importantly, what must never be automated.

---

## 0. The one non-negotiable

The loop is designed around a single constraint from the epistemic charter (SPEC.md §0):

> **The machine verifier checks the proofs; the human mathematician audits the questions.**

Everything in this document is an elaboration of where that line falls. The loop may generate
conjectures, filter them, formalize them, and prove them. It may **never** decide that a
formal statement means what its informal gloss says. That step is the entire difference
between a proof assistant and a machine that produces impressive-looking nonsense at scale.

---

## 1. The stages

```
  ┌──────────────┐
  │  0  PROPOSE  │  Claude 5 generates candidate statements          → Tier X
  └──────┬───────┘
         │  every candidate, no filtering yet
  ┌──────▼───────┐
  │  1  REFUTE   │  exact-arithmetic counterexample sweep            → most die here
  └──────┬───────┘
         │  survivors only
  ┌──────▼───────┐
  │  2  CHECK    │  exact ℚ/ℤ harness + negative control             → Tier B
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │  3  FORMALIZE│  Claude 5 writes Lean; kernel compiles it         → Tier A (proof)
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │  4  AUDIT    │  ██ HUMAN ██  statement adequacy                  → Tier A (citable)
  └──────┬───────┘
         │
  ┌──────▼───────┐
  │  5  LEDGER   │  row + artifact + gate output, one commit
  └──────────────┘
```

### Stage 0 — Propose (Tier X)

Claude 5 generates candidate statements from a seeded context: the stream's existing ledger,
its open problems, its design memos. Output is Tier X and stays Tier X. Volume is fine here;
this stage is cheap and its product is worthless until something downstream survives.

**Rule.** The proposer never sees the gate. A model that can observe which candidates pass
will learn to produce candidates that pass, which is not the same as candidates that are true.

### Stage 1 — Refute *before* attempting to prove

This inverts the obvious order, and it is Stream 1's rule §7.3 (*"counterexample before
attack"*). Before any proof effort: degenerate and boundary probes, then an exact-arithmetic
falsification sweep.

The reason is economic. A false conjecture consumes unbounded proof effort and returns
nothing; a five-second sweep at small parameters kills most of them. Stream 1 recorded a case
where this paid directly: a convolution formula sourced from a web search turned out to be
**identically zero**, caught by an exact-arithmetic check at M = 1, 2, 3 — a defect no amount
of proof effort would have surfaced, because the statement was perfectly provable and
perfectly useless.

### Stage 2 — Check (Tier B)

A deterministic exact-arithmetic harness, `Fraction`/`int` only, **shipping a negative control
demonstrated to fail**. Wired into Gate 1 in the same commit — Stream 1 records that an
unwired harness silently rots.

### Stage 3 — Formalize (Tier A, proof only)

Claude 5 writes Lean; the kernel decides. Three rules, each written after a real failure:

1. **The gate is the axiom footprint, not the source.** A failed proof still defines the
   theorem name in the environment. Only `#print axioms` reveals the `sorryAx`. Never accept
   "no `sorry` in the source" as a substitute (SPEC.md §7.6).
2. **Never weaken a statement to close a proof.** If the statement will not prove, that is a
   finding, not an obstacle. Escalate (E-4). This is the single rule most likely to be
   violated by a system optimizing for green checkmarks.
3. **Unproven infrastructure enters as a hypothesis parameter, never an axiom** — visible in
   the theorem's type, so the ledger can record what the result is conditional on.

### Stage 4 — Audit ██ HUMAN ██

**A theorem is Tier A the moment the kernel accepts it. It is *citable* only after this
stage.** The kernel confirms that the proof establishes the statement. Nothing mechanical
confirms that the statement is the one anyone meant.

The auditor answers three questions:

- Does the formal statement say what the informal gloss claims?
- Are the hypotheses non-vacuous — is there a witness satisfying them?
- Are the quantifiers where the science needs them?

The third is where formalizations actually fail, and Stream 1 has the canonical example.
Hypothesis U is `sup_{α′>0} sup_t ‖∇u^(α′)(t)‖_{L²} < ∞` — quantified *over* α′, its entire
content being the α′ → 0 limit. Fix α′ as a global constant and every symbol still typechecks,
every proof still compiles, and the statement has become a different, far weaker claim. No
kernel catches that. A reader who knows what the physics is asking catches it in a minute.

**Not automatable, not delegable, and not a formality.** An LLM judge at this stage would be
an LLM output gating a tier promotion, which the charter forbids in as many words.

### Stage 5 — Ledger

Artifact, ledger row, and gate output land in **one commit** (PLAN.md §9). A claim that
exists without a ledger row has no tier and may not be cited.

---

## 2. Where each Claude tier belongs

Adapted from Stream 1's `[any]` / `[top]` / `[human]` effort tiers.

| Stage | Who | Why |
|---|---|---|
| 0 Propose | any model | volume; the product is Tier X regardless |
| 1 Refute | any model | mechanical, fully specified, cheap to re-run |
| 2 Check | any model | the harness spec is the design memo; no judgment |
| 3 Formalize | **Opus/Fable-class** | proof search needs the strongest available model |
| 3′ Statement authoring | **Opus/Fable-class**, then human | *what to prove* is above the executing tier by definition |
| 4 Audit | **human only** | see above |
| 5 Ledger | any model | mechanical, gate-checked |

The split at stage 3 is Stream 1's standing practice, and it is worth stating in the general
form: **a top-tier model authors the statement and derives the mathematics in a design memo;
an executing agent implements a fully-specified skeleton. Never the reverse.** An agent handed
an under-specified goal will invent a definition to fill the gap, and a hallucinated definition
poisons everything downstream — which is why "do not invent a mathematical definition" is the
loudest rule in Stream 1's plan.

---

## 3. Failure modes this design is defending against

| Failure | Defence |
|---|---|
| Statement drifts to make a proof close | E-4: escalate rather than edit. Stage 4 re-reads the statement against the memo |
| `sorry` slips through | Gate 2 checks the axiom footprint, not the source text |
| A checker that cannot fail | Every Tier B harness ships a negative control, and Gate 1 fails if the control passes |
| Tier inflation over time | Tier letter is in the identifier; promotion changes the id and leaves a `supersedes` trail |
| Model output cited as evidence | `llm_output` caps at Tier X, mechanically |
| Silent cross-stream tier confusion | The tier calculus and Gate 4 |
| A harness that rots | Wired into `verify.sh` in the same commit as the artifact |
| Loop optimizes for green gates | The proposer never sees the gate; and stage 4 is not mechanical, so there is nothing there to optimize against |

That last row is the one that keeps the design honest. Every other defence is a check the
loop could in principle learn to satisfy without being right. The human audit is the only
step whose output cannot be predicted from the loop's own signals — which is precisely why it
cannot be removed to make the loop faster.

---

## 4. What "done" looks like

The loop is working when it **kills** things efficiently. A run that proposes 400 candidates,
refutes 380 in stage 1, certifies 15 at Tier B, formalizes 4, and has 1 fail the human audit
is a good run. A run that promotes everything it proposes is broken, and the number of
promotions is not the diagnostic — the ratio is.

The campaign-level version of the same point, from Stream 1's plan: *if the campaign produces
a negative verdict or kills tracks, the campaign still counts as done and successful as
science.* That is what falsifiable structure means, and a loop that cannot report a negative
result is not an instrument.
