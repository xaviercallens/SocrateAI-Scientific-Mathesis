# The Tier Calculus — a collision, its resolution, and the migration

**Status:** §1 is a Tier C observation (`MX-C-0001`). §3 is a Tier C proposal (`MX-C-0002`),
**adopted by no stream**. §2 is Tier A (`MX-A-0001`…`MX-A-0004`), kernel-verified.

---

## 1. The collision

Two streams already use the letter **B** for incompatible admission criteria. Both quoted
verbatim from the working trees as they stood on 2026-08-13:

**Stream 1 — `SocrateAI-Scientific-MechanicaFluidorum/SPEC.md` §0:**

> | **B — Checkable** | identities validated in exact rational arithmetic; certified witnesses; no floats | `tests/` harness exits 0 |

**Stream 5 — `SocrateAI-Scientific-RajMathRecovery/README.md`:**

> | **Tier B** | Established | Peer-reviewed literature, pinned to exact values |

These are not two phrasings of one idea. They are two different *kinds of evidence*:

|  | Stream 1's B | Stream 5's B |
|---|---|---|
| What did the checking | a deterministic program | a journal referee |
| Scope of the claim | a finite instance set | a universally quantified theorem |
| Reproducible on demand | yes, by running the harness | no, only by reading the paper |
| Fails how | the harness exits non-zero | it doesn't; it was wrong all along |

### Why this is live rather than hypothetical

The two repositories are not independent:

- Stream 1's Gate 2 kernel-compiles against **Stream 5's** Mathlib build. Stream 1's
  `CLAUDE.md` documents this: *"Gate 2 and all manual compiles reuse the already-built
  Mathlib checkout at `~/xdev/SocrateAI-Scientific-RajMathRecovery/dualscale/lean`"*.
- Stream 1's `PLAN.md` task F1 imports a Lean theorem **from Stream 5's tree**
  (`dualscale/lean/DualScale/K3Lock/Basic.lean`) into Stream 1's Tier A core.

So artifacts already cross the boundary. The moment a *claim* crosses with its tier letter
attached, a peer-reviewed citation arrives in a repository whose gate reads "B" as "the
harness exits 0" — and no check in either repository would notice. The failure is silent by
construction: both sides are individually consistent.

### What this observation is not

It is not a criticism of either stream's design. Each letter is well-chosen for its own
repository, and neither stream did anything wrong. The defect appears only at the seam, which
is precisely the surface no single stream owns — and precisely what Stream 0 is for.

---

## 2. The resolution: separate the axes

Stream 5's "B" and Stream 1's "B" were doing different jobs because *tier* was being asked to
encode two independent things: **how strong the claim is** and **what kind of evidence backs
it**. Splitting them is the whole fix.

### 2.1 Tier — one linear order of citation strength

```
X  <  C  <  L  <  B  <  A
```

| Tier | Admission criterion |
|---|---|
| **A** Kernel | Lean 4 compiles; zero `sorry`; `#print axioms` matches the file's declared allowlist |
| **B** Checkable | finite statement decided in exact arithmetic (ℚ/ℤ), deterministic, ships a negative control demonstrated to fail |
| **L** Literature | peer-reviewed, cited to a **quoted theorem statement** — not an abstract, not a summary |
| **C** Conjecture | proposal, analogy, physical narrative, unverified reduction |
| **X** Exploratory | floats, sampling, plots, LLM output. **May never be cited.** |

**L is the new letter, and it is what resolves the collision.** Stream 5's literature rows
were never Stream 1's B; they were always L, and the program had no name for it.

The requirement that L cite a *quoted theorem statement* is not pedantry. Stream 1 recorded
an incident that is exactly this failure mode: `SPEC.md` §2.3.1 documents a track description
resting on a regularity class read off **an abstract plus a tool-generated summary**, and the
note refuses to "fix" the description in either direction until someone reads the published
theorem. Tier L exists so that the difference between "I read the theorem" and "I read about
the theorem" has somewhere to live.

### 2.2 Evidence kind — what may support what

Orthogonal to tier, each row declares how it was established. The evidence kind **caps** the
tier; it does not set it.

| Evidence kind | Caps at |
|---|---|
| `lean_axioms` | A |
| `exact_harness` | B |
| `citation` | L |
| `argument` | C |
| `numeric`, `llm_output` | X |

A row backed by `citation` may not be filed above L however distinguished the source, and a
row backed by `llm_output` may not be filed above X however convincing the output — that one
is the epistemic charter (SPEC.md §0) made mechanical.

### 2.3 The theorem

Soundness (`Sound`): no claim is filed at a tier above any claim it **directly** cites.

**`tier_le_of_depends` (Tier A, `MX-A-0003`):** in a sound ledger, the condition holds across
the whole **transitive** closure.

**`no_kernel_claim_rests_on_weaker` (Tier A, `MX-A-0004`):** hence the entire transitive
support set of a Tier A row is Tier A.

Why kernel-verify something this elementary? Because transitivity is the property informal
bookkeeping loses first. Every stream checks the direct condition by eye when adding a row.
None of them checks the closure — and the closure is where the leak lives. A chain
`B → B → L` is sound at every direct edge and still means the head rests on literature.

### 2.4 The consequence people will trip over

**A Tier A claim may not cite a Tier L theorem.** A Lean proof needing Bourgain–Demeter as an
input must take it as an explicit hypothesis parameter, making the theorem Tier A
*conditionally*, with the hypothesis recorded.

This is not a new burden. It is Stream 1's existing rule — *"unproven infrastructure enters
as explicit hypothesis parameters, visible in the theorem's type"* (`SPEC.md` §7.1) — now
**derived from the tier order** rather than maintained as a separate convention that has to
be remembered.

---

## 3. The proposed migration — **NOT ADOPTED**

Nothing below has been agreed with Stream 1 or Stream 5. It is written down so the proposal
can be argued with, not so it can be executed.

### 3.1 Stream 5 — RajMathRecovery

1. Reclassify every current Tier B row: literature rows become **L**; any row backed by an
   exact-arithmetic certificate (the `README.md` Rule R5 rows — *"Numerical claims require
   exact-arithmetic PASS/FAIL certificates over ℚ"*) stays **B**.
2. Renumber identifiers, since the tier letter is in the id (SPEC.md §2.5). The old id is
   retained as `supersedes`.
3. Rule R4 (*"Tier B claims must cite their sources"*) becomes the L admission criterion, and
   tightens: the citation must include the quoted theorem statement.

**Expected friction, stated up front:** step 2 invalidates every existing citation of a
Stream 5 claim id, in prose, in commit messages, and in the paper drafts. That is the cost of
putting the tier in the identifier, and it is the point — a stale citation becomes lexically
wrong instead of silently wrong. Whether that cost is worth paying is Stream 5's call, not
Stream 0's.

### 3.2 Stream 1 — MechanicaFluidorum

Little changes. Its B is already this B. Two additions:

1. Rows currently Tier C *because they are standard published results* move to **L** — e.g.
   Proposition 5.1, tagged *"Tier C: paper-level standard result"*. Tier L says what was
   meant: established, not machine-checked here.
2. The obstruction ledger (O1–O5: Tao 2016, CKN 1982, Buckmaster–Vicol) is a set of Tier L
   rows. Those are the program's hardest constraints and currently have no tier at all.

### 3.3 What Stream 0 must build first

The migration cannot be asked of anyone until `MX-C-0001` is Tier B — i.e. until a harness
checks both trees at pinned commits rather than a human reading them once. See
`PLAN.md` task A2. **Filing a migration request on the strength of a Tier C observation
would be the exact error this document describes**, one level up.

---

*Authored 2026-08-13. §1's quotations were read directly from the two working trees; if
either has since changed, the quotation is the record of what it said, and the discrepancy is
an E-3.*
