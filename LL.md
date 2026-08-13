# LL.md — Lessons Learned

*Why each process rule exists, with the evidence. A rule whose incident nobody remembers is a
rule that gets deleted in the next cleanup.*

Entries marked **[inherited]** were recorded by another stream; they are repeated here because
Stream 0's rules descend from them and would otherwise look arbitrary.

---

## LL-1 — The differential gate caught a divergence on its first run *(2026-08-13, Stream 0)*

**What happened.** Gate 3 was implemented, the corpus written, and the first run reported
**15 of 30 cases disagreeing** between the Python and Rust checkers.

Every disagreement was the same defect: Python's `{value!r}` renders a string as `'MX-A-0001'`;
Rust's `{:?}` renders it as `"MX-A-0001"`. Identical verdicts, identical exit codes, different
quotation marks — and the gate compares byte-for-byte, so it failed all fifteen.

**Why it is recorded as a success rather than an annoyance.** The gate was built to catch
divergence between two independent implementations and it caught divergence between two
independent implementations on the first thing it was ever pointed at. Had the two been written
by copying one another, it would have found nothing, and it would also have been worthless.

**Second finding, from the same run.** Two cases still disagreed after the quoting fix: the
two hand-written JSON parsers produce different prose for a malformed row
(`Expecting property name enclosed in double quotes: line 1 column 20` vs.
`expected object key at 19`). This is not fixable and must not be fixed: forcing the strings
to match would mean one implementation copying the other's messages, which is exactly the
shared dependency `HARDNESS.md` H4 forbids.

**Rule.** Gate 3 compares **verdicts**, not diagnostics. The finding for a malformed row is the
canonical string `invalid JSON` on both sides, with no parser detail. Where two independent
implementations *must* agree is on admissibility; where they may legitimately differ is on how
they explain themselves.

**Rule.** A differential corpus must contain cases whose expected verdict is a *finding*. A
corpus of only-valid ledgers compares "OK" to "OK" and is the checker-that-cannot-fail one
level up. 21 of the 30 cases are deliberately broken.

---

## LL-2 — A declared axiom footprint went stale one edit after it was written *(2026-08-13, Stream 0)*

**What happened.** `TierCalculus.lean` was written with the header `AXIOM ALLOWLIST: []` and,
at the time, that was true — every theorem was axiom-free. The non-vacuity witnesses required
by `HARDNESS.md` H5 were then added. They are closed by `decide`, and Lean core's `Decidable`
instance for a quantifier over `Fin n` is built using `propext`. The five witness lemmas came
back `[propext]`.

The header still said `[]`. The file had been correct for about four minutes.

**Why it matters more than it looks.** Nothing was wrong with the mathematics. `propext` is a
standard axiom of Lean's logic and appears in Stream 1's allowlist too. The defect was purely
in the *record*: a declared property that had silently stopped being true, in the one
repository whose entire purpose is keeping declared properties true. Had the gate checked
`grep -c sorry` instead of the footprint, nothing would ever have surfaced it.

**Rule.** Axiom allowlists are declared **per declaration class**, not per file, and Gate 2
enforces the map: only declarations named `witness*` may carry `propext`; anything else with
any footprint fails. The header explains *why* the split exists rather than merely stating it.

**Rule.** When a declared property is falsified by your own edit, amend the declaration — do
not amend the check to match. The temptation runs the other way, because loosening the check is
one character and re-deriving the claim is a paragraph.

---

## LL-3 — Gate 2 was verified to fail before it was trusted to pass *(2026-08-13, Stream 0)*

**What happened.** Gate 2 reported PASS. Before recording `MX-A-0001`…`MX-A-0004`, a temporary
file containing `theorem planted_sorry : 1 = 1 := by sorry` was added to `lean/Mathesis/` and
the gate re-run. It reported:

```
FAIL  Gate 2: lean/Mathesis/_ControlProbe.lean uses sorry
```

The probe was then deleted and the gate re-run green.

**Why.** A gate that has only ever been observed passing is indistinguishable from a gate that
cannot fail. This is `HARDNESS.md` H2 applied to the gates themselves rather than to the
harnesses they run — and the gates are exactly where nobody thinks to apply it, because
watching them go green feels like evidence.

**Rule.** A new gate is demonstrated to reject a planted defect before any claim is filed
under its authority. Record the probe and its output here.

---

## LL-4 — Two streams invented the same rule independently *(2026-08-13, Stream 0)*

**Observation.** Stream 1's `SPEC.md` §7.5 requires non-vacuity: *"existence statements
quantify over the data (no trivial-witness 'well-posedness')"*. Stream 5's CI rule R3
independently bans *"theorem statements of type `True` or logically vacuous propositions"*.
Neither cites the other.

**Why it is worth recording.** Two independent derivations of one rule are the strongest
available evidence that it belongs in the shared layer rather than in each stream's local
conventions. It is also a small measurement of how much duplicated design work the absence of
Stream 0 was already costing.

**Rule.** When a rule is found independently in two streams, it is a candidate for `HARDNESS.md`
and should be recorded here with both sources — not quietly adopted as if Stream 0 had thought
of it.

---

## LL-9 — A negative control bought noise-immunity by paying with evasion-immunity *(2026-08-13, Stream 0)*

**What happened.** `tier_b_axiom_hygiene.py` matched `^axiom` at column 0, and shipped a control
proving it ignored the word `axiom` in prose. Both looked right. During review, a second probe
showed it also ignored:

```lean
namespace Foo
  axiom sneaky : Nat     -- one leading space
private axiom hidden : Nat
@[simp] axiom tagged : Nat
```

The control that "proved" the scanner was not noisy passed *for the same reason* the scanner was
evadable: it matched nothing that was not at column 0. One property was bought with the other,
and the test suite could not tell the difference.

**Why the count was still right.** Re-scanning Stream 5's tree with a permissive pattern returned
the same 34. Every axiom there happens to sit at column 0. The reported number was correct; the
*method* was one space from being wrong, and nothing in the suite would have said so.

**Rule.** When a checker can fail in two independent directions — missing a real hit, or flagging
a false one — it needs a control for **each direction**, and they must not be satisfiable by the
same mechanism. The scanner now strips Lean comments and then matches at any indentation, so
noise-immunity comes from the stripper and evasion-immunity from the pattern. Seven controls, four
of which would have failed the previous implementation.

**Rule.** A survey number that is right today is not evidence the method is right. Re-derive it a
second way before filing it. That second derivation is what turned this up.

---

## LL-10 — Gate 4 demonstrated to fail *(2026-08-13, Stream 0)*

**What happened.** `LL-3` recorded a planted-defect probe for Gate 2 but not for Gates 1, 3, or 4.
Gate 4 was therefore trusted on the strength of having only ever been seen green — the exact
condition `LL-3` was written to forbid.

A row was appended to `ledger.jsonl` with no matching row in `LEDGER.md`:

```
FAIL  Gate 4: MX-A-0099 is in ledger.jsonl but not in LEDGER.md
GATES FAILED — nothing may be committed as verified
```

The probe was removed and the gate re-run green.

**Rule.** `LL-3` applies to **every** gate, not to whichever one was newest when it was written.
Gates 1 and 3 have working demonstrations by construction (Gate 1's controls are its own probes;
Gate 3 caught a real divergence, `LL-1`). Gate 4's was missing and is now recorded here.

---

## LL-5 **[inherited, Stream 1]** — "No `sorry` in the source" is not the gate

**What happened.** Stream 1 caught **two** broken Lean proofs that a concurrent process's own
report had described as passing. A failed proof still defines the theorem name in the
environment; the source contains no `sorry`; only `#print axioms` reveals the `sorryAx`.

**Rule.** The gate is the axiom footprint. Agent and tool self-reports are not evidence —
independently re-run the compiler on the exact artifact (`HARDNESS.md` H8).

---

## LL-6 **[inherited, Stream 1]** — `git add -A` stages another agent's half-written file

**What happened.** Twice in one session, a broad `git add` swept in files a background workflow
was mid-way through writing. One was a Tier B harness that happened to already be correct
(lucky). One was a Lean proof mid-fix, carrying `sorryAx` in five theorems (not lucky — caught
only because the authoring agent flagged the discrepancy on its next run).

**Rule.** While any background process may be writing to the repository, `git add` **by
explicit path**, and re-run the relevant gate on the exact file about to be staged, immediately
before staging it.

---

## LL-7 **[inherited, Stream 1]** — An abstract is not a theorem statement

**What happened.** While verifying citations, Stream 1 retrieved an abstract plus a
tool-generated summary and found an apparent conflict with how one of its research tracks was
described. Rather than "fixing" the description, it filed the item as **UNRESOLVED**, noting
that asserting the correction on the strength of a paraphrase would repeat the very error the
citation rule exists to prevent.

**Why Stream 0 keeps it.** This is the direct origin of Tier **L**'s admission criterion. The
difference between "I read the theorem" and "I read about the theorem" had nowhere to live in
the old three-tier scheme, so it lived in a footnote. Now it is the tier's definition.

**Rule.** Tier L requires a **quoted theorem statement** from the published source. Not an
abstract, not a summary, not a retrieval result.

---

## LL-8 **[inherited, Stream 1]** — An unwired harness rots silently

**What happened.** A test file existed, was correct, and was not listed in `verify.sh`. It
therefore never ran, and nothing reported that it never ran. A passing test suite that silently
excludes a file is worse than a missing test, because it is counted.

**Rule.** Wire every new harness into `scripts/verify.sh` in the **same commit** as the
harness. Gate 1 discovers `tests/tier_b_*.py` by glob specifically so that this failure mode
requires actively misnaming a file rather than merely forgetting a line.
