# PLAN.md — Agent Execution Plan for Stream 0 (v1.0, 2026-08-13)

**Audience:** implementation agents of any capability tier. Every task states what to do, what
"done" means, how it is validated, and when to stop and escalate.
**Normative companions:** `SPEC.md` (rules), `LEDGER.md` (claims), `HARDNESS.md` (invariants),
`FRONTIER.md` (anti-patterns), `ROADMAP.md` (calendar — aspirational; this file is operational).

---

## 0. How to use this plan

1. Pick the lowest-numbered OPEN task whose **Prereqs** are satisfied. Tasks marked
   `BLOCKED` may not be started by anyone.
2. Follow the **Steps** literally. Do not improvise mathematics. Do not "fix" a statement that
   will not prove — escalate (§3).
3. A task is done only when every line of its **DoD** is mechanically true. Run
   `./scripts/verify.sh` before every commit; all four gates must pass.
4. Report using §9's template. Update `LEDGER.md` **and** `ledger.jsonl` in the same commit as
   the artifact.
5. **Effort tier** says who may run the task: `[any]` safe for low-tier models; `[top]`
   requires Opus/Fable-class judgment; `[human]` requires the human owner.

---

## 1. Goals

- **G1 — The notation exists and is proven.** Tier lattice, soundness theorem, both checkers,
  four gates. *(Done, pending G5.)*
- **G2 — The collision is reproducible.** `MX-C-0001` promoted from a human reading to a
  harness at pinned commits.
- **G3 — One stream adopts it.** A real ledger, exported, passing Gate 4 in its own CI.
- **G4 — The kernel service exists.** A Stream 0-owned Mathlib that Stream 1's Gate 2 uses.
- **G5 — Ledger integrity.** Every row tier-tagged, human-audited where the tier requires it,
  no claim outside `LEDGER.md`.

**Explicit NON-goals.** Any verdict about Navier–Stokes, K3 selection, or any stream's
science. Any adoption decision on another stream's behalf. Any publication claim. Stream 0
proposes; the streams dispose.

---

## 2. Frontier — DO / DO NOT

### DO NOT
- **DO NOT invent a definition.** If a task needs an object `SPEC.md` does not define, STOP
  and escalate (E-1). A hallucinated definition passes every gate and poisons everything
  downstream.
- **DO NOT use floating point** outside `exploration/`, and there only under the
  `# TIER X — EXPLORATORY, NO CLAIMS` banner.
- **DO NOT add `axiom` or `sorry`, and DO NOT trust "no sorry in the source".** The only
  evidence is `#print axioms` against the file's declared allowlist.
- **DO NOT weaken a theorem statement to close a proof.** Escalate (E-4).
- **DO NOT resolve a Gate 3 disagreement by choosing a side.** Escalate (E-3).
- **DO NOT add a dependency to `rust/mathesis-verify`.** See `HARDNESS.md` H4.
- **DO NOT issue verdicts or scientific conclusions.** Deliver data and gate output.
- **DO NOT create versioned file copies** (`_v2`, `_final`). Git history is the archive.
- **DO NOT report adjectives.** Numbers, paths, gate output.
- **DO NOT `git add -A`/`.`** while any background process may be writing (§9.4).

### DO
- **DO run the negative control first.** Before trusting a new check, break the input it is
  supposed to reject and confirm it does.
- **DO attach a witness** to every new definition, and **both polarities** to every predicate.
- **DO wire every new harness into `scripts/verify.sh`** in the same commit. An unwired
  harness silently rots.
- **DO pin determinism.** No wall-clock, no unseeded randomness, no network in a gated path.
- **DO commit atomically:** artifact + `LEDGER.md` row + `ledger.jsonl` row + report.

---

## 3. Escalation protocol

Create `docs/escalations/<date>-<taskID>.md` (§9.2), set the task to ESCALATED, and stop.

- **E-1 Missing definition** — the task needs an object this plan does not define.
- **E-2 Gate failure ×3** — `verify.sh` fails after three genuinely different repairs.
- **E-3 Contradiction** — your result contradicts a `LEDGER.md` row, **or the two checkers
  disagree**. This is a *discovery*; report it prominently, do not bury it.
- **E-4 Statement judgment** — you are tempted to change what a theorem says. Any question of
  *what should be proven* (vs. *how*) is above the executing tier by definition.
- **E-5 Anomaly** — runtime > 2× estimate, denominator blow-up, or output qualitatively unlike
  the task description.

---

## 4. Phase A — Adoption (OPEN)

### A1 — Human statement-adequacy audit of the Lean core  `[human]`
- **Objective:** certify that `Sound` is the condition worth checking, and that
  `MX-A-0001`…`MX-A-0004` say what `SPEC.md` §2 claims they say.
- **Questions to answer, in writing:** (i) Does `Sound` capture "no claim outranks its
  support"? (ii) Are the witnesses non-vacuous in both polarities? (iii) Is totality of
  `Ledger` (unrecorded ids ↦ Tier X) a modelling convenience or a hidden assumption?
- **DoD:** `docs/designs/A1-adequacy-audit.md` with a dated sign-off; `audited_by` set on the
  four rows in `ledger.jsonl`; Gate 4 green.
- **Status:** OPEN. **Everything downstream is provisional until this lands** — Stream 0's own
  ledger currently has exactly the gap it exists to close in others.

### A2 — Promote `MX-C-0001` to Tier B  `[any]`
- **Objective:** make the Tier B collision reproducible rather than a human reading.
- **Steps:** new `tests/tier_b_cross_stream_tiers.py`. Read the two tier tables from pinned
  commits of Stream 1's `SPEC.md` and Stream 5's `README.md` (record the commit SHAs in-file;
  if the repos are not git, record `sha256sum` of the files and treat a mismatch as E-3).
  Assert the two definitions of "Tier B" differ. **Negative control:** feed it two *identical*
  tier tables and assert it reports no collision. Wire into Gate 1.
- **DoD:** harness passes; control demonstrably fails when enabled; new row `MX-B-0005`
  supersedes `MX-C-0001`; both ledgers updated; Gate 4 green.
- **Note:** the new id is `MX-B-0005`, not a re-tiered `MX-C-0001` — the tier is in the
  identifier (SPEC.md §2.5). The same treatment applies to `MX-C-0003` (the axiom survey),
  which becomes Tier B under the same pinned-commit harness.

### A3 — Export one stream's ledger  `[top]` designs, `[any]` runs
- **Prereq:** A1, A2. **Do not start the `[any]` half before the design memo exists.**
- **Objective:** one stream, chosen **with its owner**, exports its existing claims to
  `ledger.jsonl`.
- **Expected outcome:** the schema breaks. That is the deliverable. Record every field the
  real ledger needed and the schema lacked in `docs/designs/A3-schema-gaps.md`.
- **DoD:** the stream's ledger passes Gate 4, or a dated list of exactly why it cannot.
- **Status:** BLOCKED on A1 and on an owner conversation.

---

## 5. Phase K — Kernel service (OPEN)

### K1 — Stand up the shared Mathlib  `[any]`
- **Objective:** end Stream 1's dependency on Stream 5's working tree.
- **Context:** Stream 1's `CLAUDE.md` states its Gate 2 compiles against
  `~/xdev/SocrateAI-Scientific-RajMathRecovery/dualscale/lean`, that only a subset of Mathlib
  is built there, and that a standalone cold build is a still-open chore.
- **Steps:** `lean-mathlib/` with a pinned toolchain and committed `lake-manifest.json`;
  `lake exe cache get && lake build` from a clean checkout; document the path and the
  `LEAN_ENV_DIR` override; record build time and disk footprint.
- **DoD:** cold build from zero `.olean` succeeds and is reproducible; `docs/designs/K1-kernel-service.md`
  records the pinned commit and the measured numbers. **No claim about Stream 1 until K2.**

### K2 — Repoint Stream 1's Gate 2  `[human]` decides, `[any]` executes
- **Prereq:** K1. Requires Stream 1's owner's agreement — this modifies another stream's gate.
- **DoD:** Stream 1's `verify.sh` passes with `LEAN_ENV_DIR` pointing at Stream 0, from a
  clean checkout. Verified by running it, not by reasoning about it.
- **Status:** BLOCKED on K1 and on owner agreement.

---

## 6. Phase L — The Claude 5 loop (BLOCKED)

`BLOCKED on A1 and A3.` Building an autoformalization pipeline before one real ledger has been
migrated would be building against an imagined interface. Design: `docs/CLAUDE5_LOOP.md`.

| ID | Task | Blocked on |
|---|---|---|
| L1 | Propose/refute/check pipeline over one stream's open problems | A3 |
| L2 | Formalize stage with the effort-tier split enforced | L1 |
| L3 | Human audit **tooling** — a review packet, never an automated judgment | L2 |
| L4 | Kill-rate instrumentation (a loop that promotes everything is broken) | L1 |

---

## 7. Definition of Done — campaign level

- [ ] A1 signed off; `audited_by` populated on all four Tier A rows.
- [ ] A2 landed: the collision is Tier B, reproducible from pinned commits.
- [ ] A3: one stream's real ledger passes Gate 4, **or** a dated record of why it cannot.
- [ ] K1: the shared Mathlib cold-builds reproducibly.
- [ ] Every `LEDGER.md` row maps to a passing artifact; no orphan claims.
- [ ] Every harness wired into `verify.sh`; every negative control demonstrated to fail.

Note what is absent: "every stream adopts the notation". Adoption is not Stream 0's to
declare. If the streams evaluate the tier calculus and decline it, this campaign is still
done, and the evaluation is the result.

---

## 8. Criteria for validation

| Artifact class | Requirement |
|---|---|
| Tier A (Lean) | `verify.sh` green; footprint matches the file's declared allowlist; non-vacuity witnesses present; statement adequacy signed by a human |
| Tier B (exact) | Deterministic; `Fraction`/`int` only; negative control included **and shown to fail**; wired into Gate 1; reproduces from one documented command |
| Tier L (literature) | Quoted theorem statement from the published source — never an abstract, never a summary |
| Tier C / X | Labeled; may steer decisions; may never support a ledger row above its own tier |
| Cross-stream claim | Both checkers agree (Gate 3); tier letter validated by the calculus |
| Any verdict | **Human owner only.** Agents never issue verdicts |

---

## 9. Reporting & commit protocol

### 9.1 Per-task report
```
TASK: <ID> — <DONE | ESCALATED>
GATES: <last verify.sh lines, pasted verbatim>
ARTIFACTS: <paths + sha256 for any data>
LEDGER: <rows added/changed, both files>
ANOMALIES: <none | E-# filed at path>
```

### 9.2 Escalation file template
```
Task / Rule triggered (E-1…E-5) / What I was doing / Exact blocker (verbatim error or
missing object) / What I did NOT do (no improvisation) / Smallest question that unblocks me
```

### 9.3 Commit message
`<taskID>: <one-line outcome>`, body listing DoD items satisfied, one task per commit,
artifact + both ledger files + report together.

### 9.4 The `git add -A` race
Inherited from Stream 1, which recorded it after it happened **twice in one session**. A broad
`add` stages whatever is on disk at that instant — including another agent's file mid-edit,
before its gate ran. This produced two real broken commits, one of them a Lean proof carrying
`sorryAx` in five theorems.

**Rule:** while any background process may be writing here, `git add` **by path**, and re-run
the relevant gate on the **exact file about to be staged** immediately before staging it —
not on a cached belief that it was checked a few tool calls ago.

---

*This plan is the operational law of Stream 0. Where it conflicts with `ROADMAP.md`'s
calendar, this plan wins; where it conflicts with `SPEC.md`'s rules, `SPEC.md` wins.*
