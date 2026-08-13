# CLAUDE.md

Guidance for Claude Code sessions in this repository.

## What this repository is

**Stream 0 of SocrateAI** — the *mathesis universalis* layer: the shared notation, verification
kernel, and epistemic bookkeeping the other six scientific streams use to state what they know
and how strongly they know it.

Stream 0 does no science. Its object of study **is the record**: the first theorem here is
about ledgers, not about geometry.

Read `SPEC.md` before doing anything substantive — it is the normative rulebook, not
background. `PLAN.md` is the agent-executable task list with DoD criteria and the escalation
protocol. `LEDGER.md` is the claim inventory: **a claim not listed there has no tier and may
not be cited.**

## The one command that counts

```bash
./scripts/verify.sh              # all four gates
./scripts/verify.sh --gate 3     # one gate, while iterating
```

| Gate | Checks |
|---|---|
| 1 | Every `tests/tier_b_*.py` exits 0, negative controls included |
| 2 | Lean kernel-compiles; no `sorry`; axiom footprints match each file's declared allowlist |
| 3 | Python and Rust checkers agree on all 30 corpus cases, byte-for-byte |
| 4 | `ledger.jsonl` is `Sound`; `LEDGER.md` and `ledger.jsonl` name the same ids |

Nothing is "working" until all four are green. A report saying otherwise is not evidence
(`HARDNESS.md` H8).

## The tier system (governs everything)

```
X  <  C  <  L  <  B  <  A
```

- **A — Kernel.** Lean 4, zero `sorry`, footprint matches the file's declared allowlist. The
  gate is `#print axioms`, **never** the absence of the word `sorry` in the source — a failed
  proof still defines the theorem name, and only the footprint reveals the `sorryAx`.
- **B — Checkable.** Finite statement decided in exact arithmetic (`Fraction`/`int`),
  deterministic, **ships a negative control demonstrated to fail**. A checker that cannot fail
  is not a checker.
- **L — Literature.** Peer-reviewed, cited to a **quoted theorem statement**. Not an abstract,
  not a summary (`LL.md` LL-7).
- **C — Conjecture.** Proposal, analogy, unverified reduction.
- **X — Exploratory.** Floats, sampling, LLM output. **May never be cited.**

Orthogonally, each row declares an **evidence kind** that *caps* its tier: `lean_axioms`→A,
`exact_harness`→B, `citation`→L, `argument`→C, `numeric`/`llm_output`→X.

**The consequence people trip over:** a Tier A claim may not cite a Tier L theorem. Take the
literature result as an explicit hypothesis parameter instead — the theorem is then Tier A
*conditionally*, and the ledger records the condition.

## Architecture

**`lean/Mathesis/TierCalculus.lean`** — the Tier A core. Deliberately **Mathlib-free**; it
cold-builds in ~2 seconds with no `import` at all. This is not minimalism: Stream 0's gate is
what every other stream will eventually call, so it must never be the reason another stream is
blocked (`HARDNESS.md` H10).

Compile it directly while iterating:
```bash
cd lean && lean Mathesis/TierCalculus.lean
```

Its header declares the axiom allowlist **per declaration class** — `[]` for the theory,
`[propext]` for the `decide`-closed `witness*` lemmas, which inherit it from Lean core's
decidability instance for `Fin n` quantifiers, not from the mathematics. Gate 2 enforces
exactly that split. See `LL.md` LL-2 for why it is declared this way.

**`python/mathesis/`** — the reference checker. Standard library only, no floats anywhere.

**`rust/mathesis-verify/`** — an independent second implementation, written against `SPEC.md`
rather than against the Python. **No crates.io dependencies, including for JSON.** If you are
about to add one, read `HARDNESS.md` H4 first: a differential gate whose two sides call the
same library tests that library once and the ledger logic zero times.

```bash
cd rust/mathesis-verify && cargo test --offline
```

**`tests/`** — Tier B harnesses, each with negative controls. `tests/corpus.py` is the
enumerated differential corpus; 21 of its 30 cases are deliberately broken, because a corpus
that only compares `OK` to `OK` proves nothing.

**`ledger.jsonl` + `LEDGER.md`** — the same claims, machine- and human-readable. Gate 4 fails if
they disagree. Update **both** in the same commit as the artifact.

## Working conventions specific to this repo

- **Never invent a mathematical definition or theorem statement.** If a task needs an object
  `SPEC.md` does not define, that is an E-1 escalation (`PLAN.md` §3), not a gap to fill. A
  hallucinated definition compiles fine and poisons everything downstream.
- **Never weaken a statement to close a proof.** E-4.
- **When the two checkers disagree, do not pick a winner.** E-3. That is a discovery; report it
  prominently.
- **When a declared property is falsified by your own edit, amend the declaration — not the
  check.** Loosening the check is one character; re-deriving the claim is a paragraph. That
  asymmetry is why `LL.md` LL-2 happened.
- **Demonstrate a new gate can fail before filing anything under its authority.** Plant a
  defect, watch it fail, remove it, record it in `LL.md` (LL-3).
- **`git add` by explicit path, never `-A` or `.`,** while any background process might be
  writing here (`LL.md` LL-6).
- **No adjectives in reports.** Numbers, file paths, gate output.

## What this repository must never do

Issue a scientific verdict. Automate the human statement-adequacy audit. Claim that a green
gate licenses anything beyond internal consistency of a record. See `FRONTIER.md`'s NOTODO
list — it is as normative as the TODO list.
