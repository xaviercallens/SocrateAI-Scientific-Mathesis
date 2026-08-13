# FRONTIER.md — TODO, NOTODO, and the Frontier

*Structure adapted from Stream 6's `TODO_NOTODO_Frontier.md`. The NOTODO list is not
decoration: an anti-pattern stated as strongly as a goal is the only kind that survives a
deadline.*

---

## ✅ TODO — immediate, ordered by what unblocks what

1. **Human statement-adequacy audit of the Lean core.** `MX-A-0001`…`MX-A-0004` are
   kernel-verified and **not yet audited**. The kernel confirms the proofs establish the
   statements; nobody has yet confirmed that `Sound` is the right condition to be checking.
   Until this is done, Stream 0's own ledger has the same gap it exists to close in others.
   *(`[human]`, blocks everything downstream.)*

2. **Make `MX-C-0001` Tier B.** The Tier B collision is currently a human reading of two
   working trees. A harness that checks both at pinned commits makes it reproducible. Until
   then no migration may be requested of anyone — asking on the strength of a Tier C reading
   would repeat the error the finding describes. *(`PLAN.md` A2.)*

3. **Stand up the shared Mathlib build.** Stream 1's Gate 2 compiles against Stream 5's
   working tree today. Pin a toolchain, own the build, publish the path. *(`PLAN.md` K1.)*

4. **Export one stream's existing claims to `ledger.jsonl`.** One stream, chosen with its
   owner, end to end. The schema is worth nothing until a real ledger with real history has
   been forced through it and the schema has lost the resulting argument.

5. **`mathesis-verify` as a callable gate.** Package the Rust binary so another stream's CI
   can invoke it in one line without building this repository.

6. **Shared `Reff` definition.** Three streams maintain their own account of
   `Reff(α,R) = max(R, α/R)`. One Tier A definition, imported. *(Stage 4.)*

7. **Escalation ergonomics.** The E-1…E-5 protocol is documented but has no tooling. An
   escalation that takes ten minutes to file will not be filed at the moment it matters most.

---

## 🚫 NOTODO — strict anti-patterns

1. **DO NOT let Stream 0 issue scientific verdicts.** Not about Navier–Stokes, not about K3
   selection, not about whether a stream's result is good. Stream 0 ships bookkeeping. The
   moment it starts adjudicating content, it becomes a seventh opinion wearing a gate's
   authority.

2. **DO NOT automate the statement-adequacy audit.** Not with an LLM judge, not with a
   heuristic, not "provisionally, to unblock the pipeline". This is the charter's line
   (SPEC.md §0) and it is the only step in the Claude 5 loop whose output cannot be predicted
   from the loop's own signals — which is exactly why it cannot be removed to go faster.

3. **DO NOT resolve a Gate 3 disagreement by picking the more plausible side.** Two
   implementations disagreeing means at least one is wrong and you do not yet know which.
   File an E-3. The temptation to "fix the obviously wrong one" is how a differential gate
   degrades into a single implementation with extra steps.

4. **DO NOT add a dependency to `rust/mathesis-verify`.** Not for JSON, not for error
   handling, not for convenience. It shares no library with the Python reference by design
   (H4). One `serde` and the gate tests `serde` twice and the ledger logic zero times.

5. **DO NOT let a tier letter cross a stream boundary without the calculus.** This is the
   documented live defect (`MX-C-0001`). Until the migration lands, treat every imported tier
   letter as untyped.

6. **DO NOT trust "no `sorry` in the source".** The gate is `#print axioms`. A failed proof
   still defines the theorem name. Stream 1 caught two proofs this way that had been reported
   as passing.

7. **DO NOT invent a definition to unblock a task.** If a task needs an object the spec does
   not define, that is an E-1 escalation, not a gap to fill in. A hallucinated definition
   poisons everything downstream and is invisible in every gate — the proofs all compile.

8. **DO NOT report adjectives.** No "strong", "promising", "clear", "successful". Numbers,
   file paths, and gate output. Adjectives are how a Tier C result becomes a Tier A memory.

9. **DO NOT `git add -A` while a background process may be writing.** By explicit path,
   always. This has produced real broken commits twice in one session in Stream 1, including
   a Lean file carrying `sorryAx` in five theorems.

10. **DO NOT grow the tier lattice without a theorem.** Five tiers, one linear order. A sixth
    tier, a partial order, or a per-stream dialect each require re-proving `MX-A-0003` and
    re-deriving both checkers. That cost is the feature: it makes the notation expensive to
    fragment, which is the only thing that has ever kept a notation universal.

---

## 🌌 The Frontier — long-term, unscheduled, not promised

**A machine-checked cross-stream ledger.** Every claim in all six streams in one `Sound`
graph, so that "what does this program actually know?" is a query rather than a literature
review of its own repositories. The interesting output is not the answer but the *shape* of
the answer — which Tier A results have no Tier A consumers, which Tier C conjectures carry the
most weight, where the program's actual load-bearing structure is versus where it believes it
is.

**Proof-carrying claims.** A ledger row that ships its own certificate, so a downstream stream
can verify a cited result without trusting the citing stream's gate. The tier calculus
currently assumes each stream's gate is honest; this would remove the assumption.

**The Leibniz test.** Two streams disagree about a claim. Both positions are stated in the
shared notation. The disagreement reduces to a gate run, and the losing side can see exactly
which row failed — *calculemus*, in its narrow, achievable form. Not settling which conjecture
is true; settling what each side has actually established.

**Formalized cross-stream mathematics.** The objects three streams genuinely share — `Reff`,
the Sym² lock, the dyadic shell model — as one audited Tier A library. Today each stream
carries its own account, and nothing detects when they drift.

**Retraction infrastructure.** The unglamorous one, and the most likely to be needed. When a
Tier A row is found to rest on a mistaken audit, the ledger should be able to answer *what
else falls* — mechanically, completely, in seconds. Every program of this ambition eventually
needs that query. Most build it after they need it.
