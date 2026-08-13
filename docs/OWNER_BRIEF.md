# Owner brief — decisions reserved to you

**Date:** 2026-08-13 · **From:** Stream 0 review · **Tier:** C (an argument about documents and
trees; the underlying counts are reproducible via `tests/tier_b_axiom_hygiene.py --survey`)

Six decisions, ranked by consequence. Each states what I recommend, why, and what it costs to
defer. Only **D1** is time-sensitive.

---

## Bottom line

Stream 0's four gates are green and its own house is in order, with one gap it declares openly
(no human audit yet — **D2**).

The review found something more important than anything inside Stream 0: **Stream 5 states five
CI rules that no CI enforces.** The file its README names, `dualscale_ci.yml`, does not exist,
and the repository has no `.github/` directory. Its Lean tree contains 34 `axiom` declarations
(Rule R1 forbids them) and 2 `sorry` (Rule R2 tracks them). The commit that introduced both
`sorry`s is titled *"zero-sorry Lean 4 verification"*.

This is not a discipline problem. It is what happens to everyone when nothing checks — and it is
the clearest possible argument for why Stream 0 exists. **Stream 1 has already been through this
exact audit and demoted itself**; Stream 5 has not been checked at all.

---

## D1 — Install a footprint gate in Stream 5, and re-tier what it covers · **URGENT**

### What was found

| Fact | Evidence |
|---|---|
| `dualscale_ci.yml` does not exist; no `.github/` at repo root | `find` across the tree |
| 34 `axiom` declarations across 14 files | `tier_b_axiom_hygiene.py --survey`, per-file `sha256` |
| 2 `sorry` in `Physics/HolographicDemonstration.lean` | same |
| The commit adding both `sorry`s is titled *"zero-sorry Lean 4 verification"* | `git show e3a82fb` |
| This material is reproduced in `RAMA_Compendium_EN/FR` (`.tex`, `.pdf`, `Final_Release_Package.zip`) | `grep` on the release `.tex` |

The sharpest case is `DualScale/Physics/AubinLions.lean`:

```lean
axiom VelocityField : Type                                  -- the type, opaque, no inhabitant
axiom enstrophy_of : VelocityField → ℝ                      -- the observable, opaque
axiom aubin_lions_compactness (S : Set VelocityField) : Prop -- the CONCLUSION, opaque
axiom aubin_lions_apply … : aubin_lions_compactness S       -- the IMPLICATION, asserted

theorem aubin_lions_enstrophy_compactness … : aubin_lions_compactness S := by
  …
  exact aubin_lions_apply h_ens_bound h_ke_bound            -- the proof IS the axiom
```

The conclusion predicate has no definition, so the theorem asserts nothing falsifiable; the proof
is the axiom applied; and because `VelocityField` has no exhibited inhabitant, `S` may be empty
and every hypothesis vacuously true. By Stream 5's **own Rule R3** — *"theorem statements … that
are logically vacuous are strictly prohibited and will fail the build"* — this fails. Nothing ran.

### Why this is not a new standard

`MechanicaFluidorum/lean_src/MillenniumReduction.lean` carries this header, dated the same day:

> **TIER C (DRAFT), demoted 2026-08-13 by external audit.** The external audit's B1 verdict:
> `AubinLionsStatement` and `ProdiSerrinStatement` as bare `Prop → Prop` arrows *"completely
> bypass PDE theory. The Lean kernel is merely verifying a logical tautology (A → B → C)."*
> **Accepted.**

Stream 1 handled the *same mathematical content* the stricter way — named hypothesis parameters,
**never axioms** — was audited anyway, was found vacuous, and **accepted demotion to Tier C while
keeping the file compiled and gated so it cannot rot.**

Stream 5's version of that content is strictly weaker than the version Stream 1 already demoted.

### Recommendation

1. **Install the gate first, before touching any proof.** Copy `scripts/check_footprints.py` from
   here; it needs only a `MATHESIS-GATE:` header per module. Let it fail loudly. A red board is
   the correct state and it is information.
2. **Convert `axiom` → hypothesis parameter, mechanically.** This is the fix that *preserves the
   work*: the same theorems survive, become explicitly conditional, and the dependency becomes
   visible in the type instead of invisible in the footprint. Nothing is deleted.
3. **Re-tier accordingly** — by the precedent you already accepted for Stream 1, these land at
   Tier C until the analytic content is real.
4. **Decide separately** whether `RAMA_Compendium` needs an erratum. That is a judgement about an
   already-released document and it is entirely yours; I am flagging exposure, not prescribing.

### Rationale

Every other item in this brief is internal bookkeeping that costs nothing to defer a month. This
one has **left the repository** — into a PDF, in two languages, inside a file named
`Final_Release_Package.zip`. Retraction cost is the one cost in this program that compounds with
time and audience rather than with effort.

### Cost of deferring

Each further release built on the current tree widens the gap between what the documents say and
what the kernel checked. The fix is mechanical today; it becomes a correction notice later.

### What I did **not** do

I did not edit Stream 5's tree. Stream 0 proposes; the streams dispose (`SPEC-STREAM0` §10,
"authority creep"). Deleting those axioms would break the build and destroy the roadmap intent
they encode — they are scaffolding, and the fix is to *relabel* the scaffolding, not remove it.

---

## D2 — Do the statement-adequacy audit of Stream 0's Lean core (`PLAN.md` A1)

**Recommendation.** Timebox one hour. Three questions, answered in writing in
`docs/designs/A1-adequacy-audit.md`:

1. Does `Sound` actually capture *"no claim outranks its support"*, or only a convenient shadow of it?
2. Are the witnesses non-vacuous in **both** polarities — is there a genuinely unsound ledger exhibited?
3. Is `Ledger` totality (unrecorded ids ↦ Tier X) a modelling convenience, or a hidden assumption
   that would bite when a real stream has dangling references?

**Rationale.** Everything downstream is provisional until this lands, and there is a credibility
asymmetry that matters: Stream 0 is the component telling other streams that kernel-compilation is
not adequacy. It currently has five kernel-verified rows and no audit. Question 3 is the one I would
actually expect to surface something.

**Cost of deferring.** Low technically, high rhetorically. You cannot ask Stream 5 to accept D1
while Stream 0 carries the same gap it is naming.

---

## D3 — Tier L: adopt or reject, but decide while it is still free

**Recommendation.** Adopt — but only file the migration request to Streams 1 and 5 after `PLAN.md`
A2 makes the collision Tier B (a harness reading both tier tables at pinned commits). Asking on the
strength of a Tier C reading would be the exact error the finding describes.

**Rationale.** Today, removing Tier L costs one constructor and a recompile; the theorem does not
depend on how many tiers there are. Once two streams have exported ledgers using it, removal is a
migration. **Decide now, in whichever direction.**

**Cost of deferring.** The decision gets more expensive monotonically, and silently.

---

## D4 — `TierCalculus` has zero consumers, which your own R3.4 forbids

**The rule** (`SPEC-STREAM0` §R3.4): *"Any abstraction with < 2 consumers MUST NOT enter Mathesis
(YAGNI rule — over-abstraction is this stream's failure mode)."*

`Mathesis.Scale.Reff` qualifies — three streams reference that object. `Mathesis.TierCalculus`
has **zero** consumers. By a strict reading it should not be in the library.

**Recommendation.** Set a date. If no stream's CI calls the checker by, say, end of September,
shrink Stream 0 to the one thing with independent value — the collision finding and the survey
harness — and drop the rest. Do not let it sit unadopted indefinitely.

**Rationale.** I am flagging my own work against your rule because that is what the rule is for.
An unadopted foundation is not a foundation; it is a second opinion with a build system.

---

## D5 — Mathlib kernel service (`PLAN.md` K1): **downgrade** — I over-ranked this

**Correction.** I previously called Stream 1's dependency on Stream 5's Mathlib checkout a live
fragility. It is not currently active: `lean_src/.lake` exists, and Stream 1's `verify.sh` prefers
it, falling back to Stream 5's tree only if that build is absent.

**Recommendation.** Defer. Keep the documented `LEAN_ENV_DIR` fallback. Revisit only if Stream 1's
local build is ever discarded.

**Rationale.** The failure mode is real but dormant, and K1 is days of work. Priority belongs to D1.

---

## D6 — Two small items to batch whenever convenient

- **Naming collision pass for "Mathesis"** in formal-methods / package-index contexts
  (`SPEC-STREAM0` §2 reserves this to you). Record the verdict in `LEDGER.md`.
- **Where `B-dyn` sits** relative to `X < C < L < B < A` — a tier, an evidence kind, or a
  qualifier on `B`. `schemas/certificate.schema.json` currently records it and relies on nothing.

---

## What I recommend against

- **Do not delete Stream 5's axioms to make a gate green.** Convert them to hypothesis parameters.
  Deleting destroys the roadmap they encode; converting keeps the work and makes it honest.
- **Do not automate the adequacy audit** — not with a judge model, not "provisionally to unblock".
  It is the only step whose output cannot be predicted from the pipeline's own signals, which is
  exactly why it cannot be removed to go faster.
- **Do not let Stream 0 edit another stream's tree.** It ships the tooling; that makes restraint
  more important, not less.
- **Do not treat green gates as a scientific licence.** They say a record is internally consistent.
  Nothing here bears on Navier–Stokes, K3 selection, or the universe.

---

## Suggested sequence

| Order | Item | Effort | Who |
|---|---|---|---|
| 1 | **D1** — gate into Stream 5, watch it fail, convert axioms → hypothesis parameters | ~1 day | agent, you decide the re-tiering |
| 2 | **D2** — Stream 0 adequacy audit | ~1 hour | **you only** |
| 3 | **D3** — Tier L: adopt or reject | ~15 min | **you only** |
| 4 | **D1(4)** — Compendium erratum: needed or not | ~30 min | **you only** |
| 5 | **A2** — collision harness at pinned commits, then file the migration request | ~half day | agent |
| 6 | **D4** — set the adoption deadline for Stream 0 | ~10 min | **you only** |

Four of the six are yours alone, and together they are under two hours. The agent work is blocked
behind none of them except the re-tiering call in D1.

---

## What would make this brief wrong

Stated in advance so the answer is not constructed afterwards:

- **If the 34 axioms are deliberate, documented scaffolding with a tier already attached
  somewhere I did not look** — then D1 collapses to "add the gate so it stays true", and I have
  overstated it. I checked the README, the Lean headers, and the release `.tex`; I did not find
  such a record, but absence of evidence in three places is not proof.
- **If `RAMA_Compendium` already marks these results as conditional**, the exposure argument
  weakens substantially and D1 drops below D2.
- **If no stream ever adopts the tier calculus**, D4 fires and most of Stream 0 should be deleted
  rather than maintained.
