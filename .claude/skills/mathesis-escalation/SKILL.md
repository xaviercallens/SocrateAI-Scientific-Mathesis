---
name: mathesis-escalation
description: Decide whether to stop and escalate rather than proceed, and file the escalation, in any SocrateAI stream. Use when a needed definition is missing, a gate keeps failing, a result contradicts the ledger, two checkers disagree, a theorem statement seems wrong, or there is a temptation to improvise mathematics to keep going.
---

# Escalation

Escalating is not failure. **Improvising past a blocker is.** A hallucinated definition
compiles fine, passes every gate, and poisons everything downstream — which is why the rule
against inventing one is the loudest rule in the program.

## When to stop

| Code | Trigger |
|---|---|
| **E-1** | **Missing definition** — the task needs an object the spec does not define |
| **E-2** | **Gate failure ×3** — the gate fails after three *genuinely different* repairs |
| **E-3** | **Contradiction** — your result contradicts a ledger row, **or two independent checkers disagree** |
| **E-4** | **Statement judgment** — you are tempted to change what a theorem *says* |
| **E-5** | **Anomaly** — runtime > 2× estimate, denominator blow-up, or output qualitatively unlike the task description |

### E-1 is the one that matters most

If a task needs a mathematical object that `SPEC.md` or the design memo does not define, **you
may not define it.** Not "provisionally", not "as a placeholder", not "obviously it must be
this". The definition *is* the mathematical content; choosing it is the research, and choosing
it wrongly produces work that looks correct at every checkpoint and means nothing.

### E-4: how vs. what

*How* to prove something is your job. *What* should be proven is above the executing tier by
definition. The moment you consider adding a hypothesis, weakening a bound, or rephrasing a
conclusion so a proof closes — stop. That is a finding about the statement.

### E-3: do not pick a winner

When two independent implementations disagree, at least one is wrong and you do not know which.
Resolving it by choosing the more plausible side is how a differential gate quietly degrades
into a single implementation with extra steps. File the escalation with both outputs.

E-3 is a **discovery**. Report it prominently. Do not bury it in a status line.

## How to file

Create `docs/escalations/<YYYY-MM-DD>-<taskID>.md`:

```markdown
# <taskID> — E-<n>

**Rule triggered:** E-<n>, <name>
**What I was doing:** <the task, in two sentences>
**Exact blocker:** <verbatim error output, or the precise object that is missing>
**What I did NOT do:** <the improvisation you declined — name it explicitly>
**Smallest question that unblocks me:** <one question, answerable without redesigning anything>
```

Then set the task to ESCALATED in your report and **stop working on it**. Pick up a different
unblocked task.

The "what I did NOT do" line is not ceremony. It tells the reader which tempting wrong turn was
available, which is often the fastest route to the right answer — and it is the record that the
rule held under pressure.

## The smallest-question discipline

A good escalation asks one question with a bounded answer:

> "Should `Reff` in the shared library take α as an explicit parameter, or is the per-stream
> convention of fixing it acceptable for the drift detector?"

A bad one hands the problem back:

> "How should we handle Reff across streams?"

The first can be answered in a sentence and unblocks you. The second re-opens the design.

## What is *not* an escalation

- A gate failing once, or twice, for a reason you understand → fix it.
- A result you find surprising but that contradicts nothing recorded → record it and continue.
- Uncertainty about the *significance* of a result → not your call to make **or** to escalate.
  Deliver the data; verdicts belong to the human owner.

Reference: `PLAN.md` §3.
