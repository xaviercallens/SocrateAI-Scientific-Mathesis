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

## LL-11 — Gate 2 silently skipped every theorem whose footprint wrapped *(2026-08-13, Stream 0)*

**What happened.** `check_footprints.py` matched `#print axioms` output line by line, anchored
with `^`. Lean wraps that output when the declaration name plus footprint exceeds its line
width:

```
'Mathesis.Applications.ElasticCollision.kinetic_energy_conserved' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
```

The wrapped form has no closing bracket on its first line, so the pattern did not match and the
declaration was **skipped without comment**. Gate 2 reported `ElasticCollision.lean: 1
footprint(s) as declared` for a file with two theorems, and passed.

**Why it is the worst available failure mode.** Not a false alarm — a *false all-clear*, in the
gate that is the sole evidence for every Tier A row. And it was biased: wrapping is triggered by
long names, so it hid precisely the deeply-namespaced declarations in new modules, which are the
ones least likely to have been read carefully.

**How it was found.** Not by the gate. By noticing that the compiler output for a new file had
three lines where the others had one, and checking what the gate made of it. Nothing in the
suite would have reported it, because the gate's own output — a count — was the only symptom,
and there was nothing to compare the count against.

**Fix, in two parts.** The pattern now runs over the whole output rather than per line. More
importantly, the gate now counts `#print axioms` **directives in the source** and fails if that
differs from the number of footprints parsed. That converts "the parser dropped one" from an
invisible condition into a gate failure. A theorem you forget to print is now also a failure.

**Rule.** A checker that reports a count must have something to check the count *against*.
A number with no expected value attached is decoration — it looks like evidence and cannot
disagree with anything.

**Rule.** Gates need negative controls too. Gate 2 is the harness, so it now runs parser
self-tests on every invocation, including the exact wrapped-output shape that defeated it. They
cannot be skipped because they run before any file is examined.

**Also found by the same audit.** Two theorems — `Tier.X_le` and `witnessChain_reach` — had no
`#print axioms` line at all and had therefore never been checked by Gate 2 since they were
written. Closed. The directive-count guard is what makes that class of omission impossible to
repeat.

---

## LL-12 — Three non-vacuity witnesses were wrong on the first attempt *(2026-08-13, Stream 0)*

**What happened.** While building the five application use cases, three witnesses required by
`HARDNESS.md` H5 were written by inspection and were all wrong:

1. `preyRate 2 1 3 2 = -4` — the actual value is **0**, because `α − βy = 0` at those
   parameters. The witness intended to show "the terms are individually non-zero, so the
   cancellation is real" would have exhibited the one case that demonstrates nothing.
2. `(1/2)² + 2(1/2)(1/2) + (1/2)² ≠ 1` — offered as "frequencies that do not sum to one", but
   `½ + ½ = 1`, so the expression *is* 1 and the claimed counterexample is false.
3. `dVdt 2 1 1 1 0 2 ≠ 0` — at `x = 0` the expression **is** zero, because `α − βy = 0` makes
   the junk value coincide with the limit. Correct at `y = 1`, where it is 1.

All three were caught by the kernel with `⊢ False`. Cost: three compile cycles. A thirty-second
`Fraction` computation would have caught all three before the file was written.

**Why they were all the same mistake.** Each picked a "generic-looking" parameter set without
evaluating it. Degenerate cases are not rare in small hand-chosen integers — they are *common*,
because the small values that are easy to type are the ones where things cancel.

**Rule.** Compute non-vacuity witnesses in exact arithmetic before writing them into Lean. The
kernel is a correct but slow way to discover you picked the degenerate case, and a witness that
merely compiles is not a witness — it has to be the case you meant.

---

## LL-13 — Which Mathlib you borrow determines what you can prove *(2026-08-13, Stream 0)*

**What happened.** UC5's analytic bridge was recorded OPEN on the grounds that the calculus
infrastructure was unavailable. It was available — in the *other* checkout.

`Analysis.SpecialFunctions.Log.Deriv` and `Analysis.Calculus.Deriv.{Add,Mul}` are **not built**
in `RajMathRecovery/dualscale/lean` and **are built** in `MechanicaFluidorum/lean_src`. Pointed
at the first, the file does not compile. Pointed at the second, it compiles on the first attempt
and the proof is nine lines.

**Why this is worse than a missing dependency.** The failure mode is not "build error, install
the module". Lean reports an unknown identifier, which is indistinguishable at a glance from
*the lemma does not exist* or *the statement is false*. A missing module masquerades as a
mathematical obstruction. The OPEN row was filed in good faith on exactly that confusion.

**What it cost.** One deferral that should never have been one, plus the reasoning built on top
of it: `LotkaVolterra.lean`'s docstring argued at length about why the step could not be taken.
The argument was sound and the premise was wrong.

**Rule.** Before recording a step as OPEN for want of infrastructure, **check every available
build**, and record which ones were checked. "Not available" is a claim about the environment
and it needs the same evidence as any other claim.

**Rule.** The gate prints which Mathlib provider it resolved to. A borrowed dependency that is
invisible in the output is one nobody will think to question.

**Correction issued.** `docs/OWNER_BRIEF.md` D5 downgraded the K1 kernel-service task after
observing that Stream 1 has its own build and does not need Stream 5's. That reasoning was
correct about Stream 1 and incomplete about Stream 0, which owns no build at all and had just
been silently constrained by the difference. Recorded as `MX-C-0005`; D5 partially reversed.

---

## LL-14 — The deferral was the most valuable thing in the campaign, and it was wrong *(2026-08-13, Stream 0)*

**Observation, not an incident.** UC5 was designed to demonstrate honest deferral: prove the
algebra, refuse to axiomatize the analysis, refuse the vacuous conditional restatement, file the
gap as Tier C OPEN. As pedagogy it worked — the refusals are all correct and the precedent it
cites (Stream 1's Tier C demotion) is real.

Then the deferral turned out to be unnecessary, and closing it produced something the campaign
did not otherwise have: **the first tier promotion in the ledger.** `MX-C-0004` → `MX-A-0011`,
new identifier, `supersedes` recorded, the old row kept as the historical trace.

Until that moment the promotion mechanism specified in `SPEC.md` §2.5 had never been exercised
by anything. It was schema with no instance.

**Rule.** A campaign should try to close its own OPEN rows before shipping, not because deferral
is shameful but because **the promotion path is itself a mechanism that needs testing**, and an
OPEN row is the only thing that can test it. A ledger with no promotions has an untested
transition in it.

**What stays true.** The refusals were right regardless. Had the calculus genuinely been
unavailable, `axiom` and the tautological conditional would both still have been wrong answers.
The lesson is about diligence in establishing the premise, not about the reasoning from it.

---

## LL-15 — A subagent's headline number was wrong by a factor of twenty *(2026-08-13, Stream 0)*

**What happened.** A survey subagent was asked to inventory the sibling repositories. It
reported that RajMathRecovery's Lean tree contains **"839 `sorry` and 264 `axiom`"**. The figure
was alarming and specific, and it was wrong.

Re-measured directly, excluding the vendored Mathlib under `.lake/`:

```
  .lean files (no .lake): 747
  sorry  (no .lake):        2
  axiom  (no .lake):       34
```

Including `.lake` gives 438 and 255 — close to the reported numbers. **The agent had counted
Mathlib itself.** Mathlib legitimately contains `sorry` in test and documentation files, and
`axiom` declarations are how `propext`, `Classical.choice` and `Quot.sound` are *defined*.
Counting them as defects in the host repository is a scope error, not a finding.

**Why it nearly landed anyway.** The number was directionally consistent with a real finding
already on file (`MX-C-0003`, 34 axioms), it arrived with confident specificity, and it made the
case being argued *stronger*. Every one of those is a reason to check it harder, and all three
push the other way.

**The rest of the same report held up.** `NAMAGIRI.lean`'s `Real := Float` and `Prop := True`
stubs, and the TNN dashboard's hardcoded `"PROVEN (Zero-Sorry)"` over a file containing `sorry`,
were each confirmed by direct inspection — with **corrected file paths**, since the report's
paths were wrong there too (the TNN repository contains a nested duplicate of itself).

**Rule.** `HARDNESS.md` H8 — *agent self-reports are not evidence* — applies to subagents this
session spawned, and applies hardest when the report supports what you already believe. Verify
every number before it enters a document, and verify the *path* before quoting a file.

**Rule.** When a count is reported over a tree, establish the **scope** first. `find | wc -l`
next to the count, and an explicit statement of what was excluded, would have made this
self-evident to the agent that produced it.

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
