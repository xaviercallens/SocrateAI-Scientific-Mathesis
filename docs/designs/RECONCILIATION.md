# Reconciliation — this repository against the received `SPEC-STREAM0 (DRAFT)`

**Date:** 2026-08-13. **Tier:** C (an argument about documents and trees, not a verified claim).

The received draft specification — preserved verbatim at
[`docs/SPEC-STREAM0-DRAFT-received.md`](../SPEC-STREAM0-DRAFT-received.md), commit `55ae1f8` —
is the authoritative statement of what Stream 0 is for. This document maps what was built
against it, states every deviation, and records two findings where the draft's premises did
not survive contact with the working trees.

---

## 1. What was built, against the draft's sections

| Draft § | Requirement | State |
|---|---|---|
| §4.1 | `Mathesis.Scale.Reff` — consolidated, person-name removed | **Done.** `lean/Mathesis/Scale/Reff.lean`, footprint `[propext, Classical.choice, Quot.sound]`, incl. the new §4.1 target `one_div_sq_le_of_sqrt_le` |
| §4.2–4.7 | `Sym2`, `Fiber`, `Complexes`, `Dyadic`, `Statements`, `Certificates` | **Not built.** Migration work; see §5 below |
| §5 | Notation standard + `latex/mathesis.sty` | **v1 done.** `latex/mathesis.sty`, notation table in `docs/NOTATION.md` |
| §6.4 | Certificate schema | **v1 done.** `schemas/certificate.schema.json` |
| §7 (G7.1) | Canonical SPEC relocated to Mathesis | **Done.** `SPEC.md` |
| §7 (G7.2) | LEDGER schema packaged, machine-checked | **Done, and exceeded.** `schemas/ledger.schema.json`, two checkers, Gate 4 |
| §7 (G7.3) | Human-audit gates unchanged | **Honoured.** No LLM output promotes a tier anywhere |
| §L4.1 | Zero `axiom`; footprint checked on the compiled artifact | **Done.** `scripts/check_footprints.py`; demonstrated to fail (`LL.md` LL-3) |
| §L4.2 | Every structure ships a kernel-accepted witness | **Done.** Both polarities, which the draft does not require but which `Sound` needs |
| §L4.4 | `AUDITED` / `DRAFT` module markers | **Done.** Both modules are `DRAFT`; no human audit has occurred |
| §L4.5 | Naming; no person names | **Done.** `CallensDualScale` → `Mathesis/Scale/Reff` |
| §R3.1 | Import acyclicity | **Trivially satisfied** — Stream 0 imports nothing downstream. Not yet *checked*; see §5 |
| §M0 | Bootstrap: repo, CI, `Reff`, `.sty` | **Done except the downstream half** — no stream yet consumes `Reff` by tag |

**Beyond the draft.** The tier calculus (`lean/Mathesis/TierCalculus.lean`) and its
differential checkers are not in the draft. The draft asks for the tier system to be
"packaged as reusable infrastructure" (§1.4); this went further and made the ledger a
mathematical object with a kernel-verified soundness theorem. Justification: §7's G7.2 requires
the ledger to be *machine-checked*, and the property worth checking — that soundness holds
across the transitive closure — is not one that a schema can express.

---

## 2. Deviations from the draft, stated plainly

### 2.1 A fifth tier, `L`

**The draft does not have it.** It inherits the programme's `A/B/C` plus `B-dyn`.

`docs/TIER_CALCULUS.md` §1 documents why one was added: Stream 1 and Stream 5 use the letter
**B** for incompatible admission criteria (exact arithmetic vs. peer-reviewed literature), and
neither meaning can absorb the other. `L` is where Stream 5's literature rows belong.

**This is a proposal (`MX-C-0002`), adopted by nobody**, and it is the single largest deviation
in this document. If the owner rejects it, the tier calculus works unchanged with four tiers —
`Tier` is an inductive with a `rank`, and removing a constructor costs one edit and a
recompile. The theorem does not depend on how many tiers there are.

**Unresolved interaction:** the draft's `B-dyn` (§6.4, enclosure certificates) has no place in
the five-tier order yet. Whether `B-dyn` is a tier, an evidence kind, or a `B` with a
qualifier is reserved to the owner — the draft's §11 already reserves "whether B-dyn
certificates may ever gate promotions".

### 2.2 A stricter footprint than L4.1 requires

L4.1 pins the footprint to `[propext, Classical.choice, Quot.sound]`. `TierCalculus.lean`
declares **`[]`** for its theory declarations — no axioms at all — because it is Mathlib-free
and constructive. `Reff.lean` uses the L4.1 footprint exactly.

Stricter is compatible, but it is a deviation and the gate had to grow to express it: the
allowlist is declared *per declaration class*, not per file. A file-wide list is only as tight
as its loosest declaration, and collapsing `TierCalculus.lean` to `[propext]` would silently
license a real axiom appearing in the theory later. See `LL.md` LL-2 for the incident that
forced this.

### 2.3 Layout

The draft implies `Mathesis/` as a Lean-library-shaped repository. What was built is a
repository with `lean/`, `python/`, `rust/`, `tests/`, `docs/` — because the deliverables
include two non-Lean checkers and a harness framework (§6.1). The Lean namespace is `Mathesis`
as specified.

### 2.4 The Rust checker is not in the draft at all

§6 asks for "a producer of claims that a dumb exact checker can replay". `mathesis-verify` is a
second *checker*, not a second producer — a differential implementation of the ledger logic.
Justification is `HARDNESS.md` H4, and it earned its place on its first run (`LL.md` LL-1).
This does add a maintenance surface the draft did not ask for.

---

## 3. Finding: the duplicate `Reff` the draft expects does not exist

**Draft §1:** *"two repos currently carry near-duplicate `Reff` theorem sets"*.
**Draft §4.1:** *"currently duplicated across `DualScale.lean` and `CallensDualScale.lean`"*.
**Draft §9:** duplicate theorem sets must be *"diffed before deletion; any statement mismatch
between the two existing copies is a LEDGER erratum, not a silent merge"*.

A search of every `.lean` file under `~/xdev` on 2026-08-13 found **exactly one** definition of
`Reff`, in `MechanicaFluidorum/lean_src/CallensDualScale.lean`. `DualScale.lean` in Stream 5 is
an import aggregator and defines no `Reff`; no file in that tree mentions the identifier.

So there was nothing to diff and nothing to delete. The consolidation in
`lean/Mathesis/Scale/Reff.lean` is a **rename, not a merge**, and it is labelled as such.

**But the draft's underlying worry is correct, and worse than duplication.** Stream 5 carries
`DualScale/Geometry/TDuality.lean`, which models the same physics with two choices the
programme forbids elsewhere:

```lean
noncomputable def alpha_prime : ℝ := 1                    -- α fixed as a global constant
axiom t_duality_invariance (v : StringVacuum) ... : ...   -- the content asserted, not proved
```

Compare Stream 1's own file header, which records that its v0.1 declared
`axiom alpha_prime : ℝ` and that this was **repaired** precisely because it "violat[ed] the
spec's own §5.1 (Axioms are Forbidden)". The same defect is still live in Stream 5's tree.

This is not duplication with drift. It is the same idea formalized once with α quantified and
proved, and once with α fixed and the content axiomatized — which is strictly worse, because
the second version cannot be diffed against the first. It has no theorem to compare.

Recorded as `MX-C-0003`.

## 4. Finding: 34 `axiom` declarations in Stream 5's tree, against its own Rule R1

Stream 5's `README.md` states:

> **Rule R1**: No `axiom` declarations allowed in `.lean` files.

`tests/tier_b_axiom_hygiene.py --survey` on 2026-08-13 counted **34** across 14 files, plus **2**
`sorry` in `Physics/HolographicDemonstration.lean` (per-file `sha256` in the survey output).
Stream 1's `lean_src/` has **zero** of each.

**The CI that rule names does not exist.** The README attributes R1–R5 to `dualscale_ci.yml`.
There is no such file anywhere in the repository, and no `.github/` directory at its top level.
The rule is stated; nothing checks it. That is `HARDNESS.md`'s definition of the difference
between an invariant and a preference, and it is why the count is 34 rather than 0.

**The record and the tree disagree.** Commit `e3a82fb`, titled *"zero-sorry Lean 4 verification"*,
is the commit that **added** `HolographicDemonstration.lean` — the file containing both `sorry`
occurrences. This is not offered as an accusation: it is what happens to everyone when no gate
runs, and it is the single most legible argument for why Stream 0 exists.

Three overlaps matter more than the count, because they are places where **one stream
axiomatizes what another proves**:

| Object | Stream 5 | Stream 1 |
|---|---|---|
| Aubin–Lions compactness | `axiom aubin_lions_compactness` — in **two** files (`NS/AubinLions.lean:89`, `Physics/AubinLions.lean:35`) | an explicit **hypothesis parameter** in `MillenniumReduction.lean` |
| Dyadic cascade conservation | `axiom dyadic_cascade_conservation` (`Physics/DyadicShell.lean:34`) | **proved** — the telescoping identity in `DyadicShells.lean`, Tier A |
| Enstrophy | `axiom enstrophy_of`, `axiom enstrophy_pos` (`Physics/AubinLions.lean`) | defined, with the production identity proved |

An axiom is not a weaker proof; it is a *permanent, invisible* assumption that propagates into
the footprint of everything downstream.

**Contamination is latent, not live — verified.** Stream 1's `lean_src/` imports only `Mathlib.*`
modules; there is no `import DualScale.…` anywhere. Its gate uses Stream 5's checkout purely as a
Mathlib *provider* (`lake env lean`), so the DualScale namespace is never loaded and none of these
34 axioms reaches a Stream 1 footprint today. The protection that would catch it if someone wrote
that import is Stream 1's own `#print axioms` gate, and it would work. So the finding is about
**Stream 5's own claims**, not about Stream 1's — and the fix is a gate in Stream 5, not a
restriction on Stream 1.

**What Stream 0 does about this: nothing, yet.** Recorded as `MX-C-0003`, surfaced to the
owner. It is not Stream 0's place to edit another stream's tree (draft §10, "authority creep"),
and the finding is Tier C until a harness checks it at pinned commits (`PLAN.md` A2).

**Why the harness does not gate on it.** Making Stream 0's build fail because another stream
edited a file would make the foundation a bottleneck — draft §R3.3 and `HARDNESS.md` H10. The
survey is informational and always exits 0.

---

## 5. What the draft asks for that is not built

Stated so the gap is visible rather than implied:

- **§4.2–4.7** — `Sym2`, `Fiber.Quantum`, `Complexes.Interaction`, `Dyadic`, `Statements`,
  `Certificates` modules. All are migrations of existing downstream material, and §9 requires
  each to be diffed against its origin before it moves. That is a task per module, with the
  owner in the loop.
- **§4.2 T4.2a/T4.2b** — the variable-coefficient Sym² recurrence and the Apéry
  self-reciprocity lemma. **New mathematics**, not migration. Not attempted: authoring a
  theorem statement is a `[top]`+`[human]` task under `PLAN.md`, and inventing one here would
  be the E-1 violation this repository is loudest about.
- **§6.2/§6.3** — Engines B (enclosures) and C (PIVP). The certificate *schema* exists; no
  engine does.
- **§R3.1** — the import-acyclicity CI check. Trivially true today (Stream 0 imports nothing)
  and therefore untestable in a way that would catch a regression; it needs a downstream
  consumer first.
- **§R3.4** — the two-consumer rule. Nothing enforces it. `Reff` qualifies (three streams
  reference the object); `TierCalculus` currently has **zero** consumers and by a strict
  reading should not be in the library at all. Flagged deliberately: it is the clearest case of
  this repository doing something the draft's own YAGNI rule cautions against.
- **§2** — the naming collision pass for "Mathesis" in formal-methods contexts. Reserved to the
  owner by §11; not performed.

## 6. Open items still reserved to the owner (draft §11)

Unchanged by anything here, and listed so nothing is assumed settled: the naming decision and
its collision pass; adoption of G7.1; the M0 date; whether `B-dyn` certificates may gate
promotions; and the audit of every `DRAFT` marker — which now includes the two introduced by
this repository, plus the Tier L proposal in §2.1 above.
