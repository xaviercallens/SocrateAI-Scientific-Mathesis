# SPEC-STREAM0 (DRAFT): MATHESIS — The Foundation Stream
## Shared Lean 4 Library, Notation Standard, and Certified Solver Interface

**Status:** DRAFT specification — pending human owner audit and naming decision.
**Repository (proposed):** `SocrateAI-Scientific-Mathesis`
**Lean namespace (proposed):** `Mathesis`
**Role:** Stream 0. Every other stream imports from it; it imports from none.
**Tier of this document:** governance and definitions. No mathematical result is claimed.

---

## 1. Purpose

Four streams currently exist (MechanicaFluidorum / Hypothesis U; SOCRATES–DualScale /
K3 & Cooper sequences; the PIVP "Poly-Algebraic" solver; OP-7 interaction complex).
They already share objects — `Reff`, the Sym² lock, `QuantumFiber`, tier gates,
exact-arithmetic harnesses — by **copy**, which is how version drift and silent
divergence begin (two repos currently carry near-duplicate `Reff` theorem sets).

Stream 0 exists to hold, exactly once:

1. **The core Lean 4 library** (`Mathesis/`): shared definitions and kernel-verified
   theorems, single source of truth, downstream repos import by pinned tag.
2. **The notation standard** (§5): one mathematical notation across all papers,
   memos, and Lean identifiers, with a LaTeX macro file.
3. **The certified solver interface** (§6): one certificate schema and three
   computation engines (exact algebra, enclosures, PIVP) behind one Gate-1 replayer
   discipline.
4. **The epistemic tooling** (§7): the tier system, axiom-footprint CI, ledger
   schema — packaged as reusable infrastructure rather than re-implemented per repo.

What Stream 0 is NOT: it hosts *statements* (e.g. Hypothesis U's formal shape) but
never *attacks*. No physics claim, no track work, no verdicts. It is load-bearing
wall, not battlefield.

---

## 2. Name

**Recommended: MATHESIS.** Rationale (one line, narrative-eligible, carries no
weight): *mathesis universalis* — the Leibniz programme of a universal formal
notation serving all sciences — is precisely this stream's job description.
Practical properties: short, pronounceable in FR/EN, valid Lean namespace,
descriptive of role (foundation/notation), no claim embedded in the name
(Rule N-1 compliant: it names a codebase, not a mathematical structure).

Alternates for the owner's decision:
- **CLAVIS** ("key" — the key to the Sym² lock; Latin theme matches
  MechanicaFluidorum). Known collision: ID Quantique's "Clavis" QKD product line.
- **FUNDAMENTA** — advised against: collides with the journal *Fundamenta
  Mathematicae*.

**Owner action before adoption (LL-6-style pass on names):** GitHub / package-index /
trademark search for "Mathesis" in formal-methods contexts; record verdict in
LEDGER.md. Per prior decision, no structure inside the library carries a person's
name.

---

## 3. Stream dependency contract

```
                    ┌────────────────────────────┐
                    │  Stream 0: MATHESIS        │
                    │  (defs, notation, gates)   │
                    └──────┬──────┬──────┬───────┘
              imports      │      │      │      imports
        ┌──────────────────┘      │      └──────────────────┐
        ▼                         ▼                         ▼
  MechanicaFluidorum      SOCRATES–DualScale          PIVP Solver
  (Hypothesis U)          (K3, Cooper, Sym²)          (Poly-Algebraic)
        ▲                         ▲                         ▲
        └───────────── OP-7 Interaction Complex ────────────┘
                 (consumes Mathesis.Complexes + stream data)
```

Rules:
- **R3.1 (acyclicity).** Stream 0 never imports downstream. Enforced by CI
  (import-graph check in Gate 2).
- **R3.2 (pinning).** Downstream repos consume Mathesis by **pinned release tag**,
  never by branch. A Mathesis release pins its Mathlib commit; downstream inherits it.
- **R3.3 (no blocking).** A downstream stream may vendor a copy *temporarily* under
  a dated `vendored/` directory with an expiry entry in its LEDGER; expired vendored
  copies fail CI. This prevents the foundation from becoming a bottleneck while
  making drift visible and finite.
- **R3.4 (promotion path).** Any definition used by ≥ 2 streams MUST be proposed for
  promotion into Mathesis. Any abstraction with < 2 consumers MUST NOT enter
  Mathesis (YAGNI rule — over-abstraction is this stream's failure mode).

---

## 4. Lean 4 library specification

Global rules (inherited from the programme, restated as library law):
- **L4.1** Zero `axiom` declarations. Footprint pinned to
  `[propext, Classical.choice, Quot.sound]`, checked per module by CI on the
  compiled artifact (not source grep — the sorryAx lesson).
- **L4.2** Every `structure`/`class` ships a kernel-accepted witness in the same
  module (`*.Models` section). A structure without a model does not merge.
- **L4.3** Analytic debt lives in **hypothesis types**, never axioms
  (the `MillenniumReduction` pattern).
- **L4.4** Two status markers in module docstrings: `AUDITED` (human
  statement-adequacy audit passed, LEDGER row exists) or `DRAFT`. Kernel-clean but
  unaudited modules stay `DRAFT` — compilation is not adequacy.
- **L4.5** Naming: `snake_case` theorems, `UpperCamel` types, no abbreviations
  that collide with Mathlib, and no person names in identifiers.

### 4.1 `Mathesis.Scale.Reff` — status: consolidation of existing Tier A
Single source of truth for the T-dual effective radius (currently duplicated
across `DualScale.lean` and `CallensDualScale.lean`; the latter is renamed on
migration, §9).

```lean
noncomputable def Reff (α R : ℝ) : ℝ := max R (α / R)

theorem Reff_pos           (hα : 0 < α) (hR : 0 < R) : 0 < Reff α R
theorem Reff_ge_sqrt       (hα : 0 < α) (hR : 0 < R) : Real.sqrt α ≤ Reff α R
theorem Reff_bounce        (hα : 0 < α) (hR : 0 < R) (h : R < Real.sqrt α) :
    Reff α R = α / R
theorem Reff_inertial      (hα : 0 < α) (hR : 0 < R) (h : Real.sqrt α ≤ R) :
    Reff α R = R
theorem Reff_tdual         (hα : 0 < α) (hR : 0 < R) : Reff α (α / R) = Reff α R
theorem Reff_eq_sqrt_iff   (hα : 0 < α) (hR : 0 < R) :
    Reff α R = Real.sqrt α ↔ R = Real.sqrt α
theorem one_div_sq_le_of_sqrt_le (hα : 0 < α) (hx : Real.sqrt α ≤ x) :
    1 / x ^ 2 ≤ 1 / α
```

### 4.2 `Mathesis.Sym2.Recurrence` — status: Tier A existing + new targets
```lean
/-- Constant-coefficient discrete lock (existing, kernel-verified). -/
theorem sym2_recurrence (a b : ℝ) (u : ℕ → ℝ)
    (hrec : ∀ n, u (n+2) = a * u (n+1) + b * u n) :
    ∀ n, (u (n+3))^2 = (a^2+b)*(u (n+2))^2 + b*(a^2+b)*(u (n+1))^2 - b^3*(u n)^2

/-- Spectral content (existing): elementary symmetric functions of {λ², λμ, μ²}. -/
theorem sym2_symmetric_functions : ...

/-- NEW TARGET T4.2a (variable coefficients — the Apéry shape).
    Coefficients are functions ℕ → ℝ; conclusion is the order-3 recurrence with
    explicitly constructed coefficient functions. Milestone gate: must specialize
    to the Apéry recurrence (n+1)³u_{n+1} = (34n³+51n²+27n+5)u_n − n³u_{n−1}
    as the canonical positive-control instance (MEMO-K3 §2.1). -/
theorem sym2_recurrence_poly (a b : ℕ → ℝ) ... : ...   -- DRAFT target

/-- NEW TARGET T4.2b (self-reciprocity of the Apéry symbol; MEMO-K3 Fact 3).
    Five-line lemma; ships with Vieta corollary z₁z₂ = 1. -/
theorem apery_symbol_self_reciprocal (z : ℝ) (hz : z ≠ 0) :
    z^2 * (1 - 34*(1/z) + (1/z)^2) = 1 - 34*z + z^2
```

Deferred honestly: the ODE-level Sym² (Clausen) — Mathlib's ODE theory is not yet
adequate; recorded as OPEN, not simulated by axioms.

### 4.3 `Mathesis.Fiber.Quantum` — status: Tier A existing + rank-r target
```lean
structure QuantumFiber where
  disc : ℤ
  disc_ne : disc ≠ 0

noncomputable def couplingMass (F : QuantumFiber) : ℝ := 1 / |(F.disc : ℝ)|
-- existing: resonance_law, couplingMass_pos, couplingMass_ne_zero,
--           couplingMass_le_one, mass_determines_disc

/-- NEW TARGET T4.3a: lattice fiber of rank r with Gram matrix; disc := det. -/
structure LatticeFiber (r : ℕ) where
  gram : Matrix (Fin r) (Fin r) ℤ
  symm : gram.IsSymm
  disc_ne : gram.det ≠ 0
-- Bridge lemma target: LatticeFiber r → QuantumFiber via det.
-- Instantiation hook: Apéry–Fermi transcendental lattice (rank 3) — BLOCKED on
-- Peters 1986 retrieval (MEMO-K3 §5.2); placeholder witnesses must not claim
-- provenance (MEMO-K3 §2.3).
```

### 4.4 `Mathesis.Complexes.Interaction` — status: NEW (OP-7 dependent)
```lean
def latticeBall (M : ℕ) : Finset (Fin 3 → ℤ) := ...    -- Λ_M, computable
def triads (M : ℕ) : Finset (Finset (Fin 3 → ℤ)) := ... -- T_M (zero-sum, distinct)
def lockedBall (S : Set ℕ) [DecidablePred (· ∈ S)] (M : ℕ) : Finset _ := ...

/-- Tier A counting anchor (unconditional). -/
theorem card_squares_le (X : ℕ) :
    ((Finset.range (X+1)).filter (fun n => ∃ m, n = m^2)).card = Nat.sqrt X + 1
```
Division of labor (fixed by this spec): Lean proves the **general** counting and
structure lemmas and cross-checks cardinalities at tiny M (`M ≤ 2`) by evaluation;
the Tier B Python harness produces all production-scale counts (W3). Lean never
pretends to be the counting engine; Python never pretends to be the proof.

### 4.5 `Mathesis.Dyadic` — status: consolidation
`DyadicShells`, `EnstrophyProduction`, `EnstrophyProductionBound` move here
verbatim (they are already cross-stream: MF proves them, SOCRATES Stage 1
measures against them). Their LEDGER rows migrate with them.

### 4.6 `Mathesis.Statements` — status: relocation of drafts
`HypothesisU_Statements` and `MillenniumReduction` relocate here, keeping their
`DRAFT pending human audit` markers and their machine-checked refutation of the
prior false formalization. Rationale: statements are shared infrastructure;
attacks stay downstream.

### 4.7 `Mathesis.Certificates` — status: NEW (D6 dependent)
```lean
/-- B-dyn certificate: step boxes with rational endpoints, step sizes,
    remainder bounds. -/
structure EnclosureCert where
  dim   : ℕ
  steps : List (Step dim)          -- boxes: lo hi : Fin dim → ℚ
  ...

/-- The dumb exact checker (Lean function, executable). -/
def replayOk (c : EnclosureCert) : Bool := ...

/-- Soundness statement (DRAFT — theorem statement now, proof is the declared
    Tier A upgrade path per D6 §4; Immler 2018 is the feasibility precedent). -/
theorem replay_sound (c : EnclosureCert) (h : replayOk c = true) :
    TrajectoryInBoxes c := ...   -- DRAFT: statement-level, proof deferred, no axiom
```
v1 ships `replayOk` + the *statement* of soundness with the proof obligation
tracked in the type (L4.3), plus the Python replayer as the operational Gate-1
harness. The two replayers cross-check on shared certificates.

---

## 5. Notation standard (papers + Lean + harnesses)

One table, three columns that must never diverge. First-use rule: a symbol may
appear in prose only if its row exists here.

| Symbol (LaTeX) | Meaning | Lean identifier |
|---|---|---|
| `\Reff(\alpha', R)` | T-dual effective radius `max(R, α'/R)` | `Mathesis.Reff` |
| `\sqrt{\alpha'}` | fundamental length; "the seam" | — (derived) |
| `\Sym^2(L_2) = L_3` | symmetric-square lock | `sym2_recurrence` (+ poly target) |
| `\HypU` | Hypothesis U (∃C ∀cutoff — quantifier order is normative) | `Mathesis.Statements.HypothesisU` |
| `X_M`, `X_M^S` | interaction complex; locked subcomplex | `Mathesis.Complexes.*` |
| `\Omega`, `S_N` | enstrophy; production sum | `Mathesis.Dyadic.*` |
| `\disc`, `m_c` | fiber discriminant; coupling mass `1/\|disc\|` | `Mathesis.Fiber.*` |
| `\tier{A/B/C}`, B-dyn | epistemic tier tags | LEDGER schema |

Deliverable: `latex/mathesis.sty` providing `\Reff, \Sym, \HypU, \tier{}, \lean{}`,
the theorem environments with Lean-tag support used in the NS article, and the
`VERIFIED / [unverified]` citation marks. All programme papers import it; the NS
article (dual_scale_ns.tex) is retrofitted as the first consumer.

Prose conventions (normative): quantifier order stated explicitly whenever a
uniformity claim is made; "theorem" reserved for Tier A; "verified" reserved for
kernel or exact-arithmetic gates; person-free structure names; no new symbol
without a definitional anchor (Rule N-1).

---

## 6. The solver: three engines, one certificate discipline

"Solver" in Mathesis means: **a producer of claims that a dumb exact checker can
replay.** Three engines, one schema.

### 6.1 Engine A — Exact algebra (exists; generalized here)
Rational-arithmetic identity/inequality harnesses (`fractions.Fraction`/`int`
only), each with a demonstrated-to-fail negative control. Mathesis packages the
harness framework (runner, negative-control registry, `.meta` writer) so streams
stop re-implementing it.

### 6.2 Engine B — Enclosures (D6)
Rounded-rational interval trajectories for ODE systems (quadratic nonlinearities
first). Claim form: `∀t ∈ [0,T] : state ∈ boxes`. Certificate: `EnclosureCert`.
Controls: tamper-reject, honest-failure on inviscid blow-up, Cheskidov positive
control (D6 §3).

### 6.3 Engine C — PIVP (the Poly-Algebraic solver, scoped)
Pipeline stages, each with its certificate obligation:
1. **Compile** (target constant → PIVP): the compilation transcript is the
   certificate; independent re-derivation check.
2. **Quadraticize** (degree ≤ 2 via product variables): exactness of the
   rewriting is Engine-A-checkable (polynomial identity over ℚ).
3. **Integrate**: Engine B runs the quadratic PIVP — the two engines compose;
   PIVP gets trajectory rigor for free from D6.
4. **Converge**: target claim form `|y_k(t) − α| ≤ C e^{−t}`; v1 records the
   convergence certificate as DRAFT-conditional (the contraction estimate as a
   hypothesis type) until proved per instance.
MUM-point handling and the conifold-ratio device are documented against the
canonical geometry (MEMO-K3 §2.4). `[LL-6 pending]` before any equivalence claim:
Bournez–Graça–Pouly.

### 6.4 Certificate schema (all engines)
```json
{ "claim": "...", "engine": "A|B|C", "inputs_sha256": "...",
  "replay_cmd": "...", "negative_controls": ["..."],
  "tier": "B|B-dyn", "meta": { "tool_versions": "...", "date": "..." } }
```
Gate 1 = replay of every certificate; Gate 2 = Lean kernel + footprint. Identical
to the MF pipeline, now owned in one place.

---

## 7. Governance

- **G7.1** The canonical `SPEC.md` (tiers, honesty clause, obstruction ledger,
  E-escalations, LL rules) **moves to Mathesis**; downstream repos pin a SPEC
  version exactly as they pin the library. One law, versioned.
- **G7.2** LEDGER schema is packaged (a claim not in a ledger has no tier — now
  machine-checked: CI fails if a public doc cites an unledgered claim ID).
- **G7.3** Human-audit gates are unchanged and unchangeable by this spec: no LLM
  output promotes a tier; `DRAFT → AUDITED` requires the owner.
- **G7.4** Releases: semver; a release = (Lean modules + sty + harness framework +
  SPEC version + pinned Mathlib commit), tagged, with full Gate output archived.

## 8. Milestones

- **M0 — Bootstrap.** Repo, CI (footprint + import-acyclicity + ledger checks),
  `Mathesis.Scale.Reff` consolidated, `mathesis.sty` v1. DoD: both gates green;
  one downstream repo (MF) consumes Reff by tag with its local copy deleted.
- **M1 — Consolidation.** `Sym2`, `Fiber`, `Dyadic`, `Statements` migrated with
  ledger rows; downstream duplicates removed; NS article retrofitted to the sty.
- **M2 — New floors.** `Complexes.Interaction` (with T4.4 counting anchor) and
  `Certificates` v1 (`replayOk` + Python replayer cross-check). Gate for OP-7's W3
  and D6's first certified run.
- **M3 — Sym² poly + Apéry control.** T4.2a/T4.2b landed; Stream-1 checker wired
  to the Apéry positive control (MEMO-K3 action 3).
- **M4 — Solver unification.** Engine C stages 2–3 running on Engines A/B;
  first end-to-end certified constant (Catalan system) as demonstration artifact.

## 9. Migration and renames

- `CallensDualScale.lean` → `Mathesis/Scale/Reff.lean` (person-name removal per
  standing decision); deprecation aliases for one release cycle.
- Duplicate theorem sets diffed before deletion; any statement mismatch between
  the two existing copies is a LEDGER erratum, not a silent merge.
- Existing `.meta` sidecars and gate outputs are preserved verbatim (audit trail).

## 10. Risks and their controls

- **Over-abstraction** → R3.4 two-consumer rule.
- **Foundation as bottleneck** → R3.3 dated vendoring with CI-enforced expiry.
- **Version skew** → R3.2 pinning; Mathlib commit owned by Mathesis releases.
- **Authority creep** (Stream 0 quietly deciding mathematics for streams) → §1
  scope rule: statements yes, attacks no; verdicts remain the owner's.

## 11. Open items reserved to the human owner

Naming decision (§2, with collision pass); adoption of G7.1 (SPEC relocation);
M0 date; whether B-dyn certificates may ever gate promotions (inherits D6 §7);
audit of every `DRAFT` marker introduced here.
