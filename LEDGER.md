# LEDGER.md — Stream 0 claim inventory

**A claim absent from this file has no tier and may not be cited.** (SPEC.md §0)

This is the human-readable mirror of `ledger.jsonl`. Gate 4 fails the build if the two disagree
on which identifiers exist — two ledgers that drift apart are worse than one.

Tier semantics: `A` kernel · `B` exact arithmetic · `L` literature · `C` conjecture ·
`X` exploratory (uncitable). See SPEC.md §2.

---

## Tier A — kernel-verified

| ID | Claim | Artifact | Rests on |
|---|---|---|---|
| `MX-A-0001` | The five tiers `X<C<L<B<A` form a linear order: reflexive, transitive, antisymmetric, `A` top, `X` bottom. | `lean/Mathesis/TierCalculus.lean` — `Tier.le_antisymm`, `Tier.le_A`, `Tier.X_le`, `Tier.eq_A_of_A_le` | — |
| `MX-A-0002` | The dependency relation `Depends` is transitive. | `lean/Mathesis/TierCalculus.lean` — `Depends.trans` | — |
| `MX-A-0003` | **Transitive tier monotonicity.** In a `Sound` ledger, `Depends L a b → (L a).tier ≤ (L b).tier`. Soundness stated on *direct* edges propagates through the whole transitive closure. | `lean/Mathesis/TierCalculus.lean` — `tier_le_of_depends` | `MX-A-0001` |
| `MX-A-0004` | In a `Sound` ledger the entire transitive support set of a Tier A row is Tier A. Equivalently: a Tier A claim resting (however indirectly) on a sub-A claim cannot exist. | `lean/Mathesis/TierCalculus.lean` — `no_kernel_claim_rests_on_weaker`, `not_A_of_weak_support` | `MX-A-0001`, `MX-A-0003` |
| `MX-A-0006` | **UC1 (mathematics).** `1+3+…+(2n−1) = n²`. Mathlib-free. | `Applications/OddSums.lean` | — |
| `MX-A-0007` | **UC2 (physics).** The 1-D elastic collision formulae conserve momentum **and** kinetic energy exactly over ℚ, for `m₁+m₂ ≠ 0`. | `Applications/ElasticCollision.lean` | — |
| `MX-A-0008` | **UC3 (biology).** Hardy–Weinberg: genotype frequencies sum to 1, allele frequency is invariant, equilibrium is reached in **one** generation. *A theorem about the model; no claim about any population.* | `Applications/HardyWeinberg.lean` | — |
| `MX-A-0009` | **UC4 (physics).** Kepler III from the inverse-square law for circular orbits, `ω²r³ = GM`, stated with the reduced period so π leaves the statement and it becomes exactly rational. Force law is a **hypothesis parameter**. | `Applications/Kepler.lean` | — |
| `MX-A-0010` | **UC5 (biology), algebraic core.** The substituted Lotka–Volterra `dV/dt` expression is identically zero for non-zero populations. No calculus. **Does not** establish that it *is* `dV/dt` — see `MX-C-0004`. | `Applications/LotkaVolterra.lean` | — |
| `MX-A-0011` | **UC5 (complete) — `V` is conserved along the Lotka–Volterra flow.** Proved over ℝ via `HasDerivAt.log`; the system's two equations are hypothesis parameters. **Closes `MX-C-0004`** — the first tier promotion in this ledger. | `Applications/LotkaVolterraFlow.lean` | `MX-A-0010` |
| `MX-A-0005` | **The T-dual effective radius.** `Reff(α,R) = max(R, α/R)` is positive; bounded below by `√α` with the minimum attained at **exactly** the self-dual radius; invariant under `R ↦ α/R`; equal to `α/R` below `√α` and to `R` above. Plus §4.1's new target: `√α ≤ x → 1/x² ≤ 1/α`. | `lean/Mathesis/Scale/Reff.lean` — 10 declarations | — |

**Axiom footprints.** `TierCalculus.lean` theory declarations: `[]` — no axioms at all. Witness lemmas
(`witness*`, closed by `decide`): `[propext]`, inherited from Lean core's decidability
instance for quantifiers over `Fin n`, not from the mathematics. Gate 2 enforces exactly
this split; see the header of `TierCalculus.lean` for why it is declared rather than glossed.
`Reff.lean` declares `[propext, Classical.choice, Quot.sound]` — the `SPEC-STREAM0` L4.1
footprint — because it imports Mathlib.

**Module status (L4.4): both Lean modules are `DRAFT`, not `AUDITED`.**

**Statement-adequacy audit: NOT YET PERFORMED.** The kernel has checked these proofs. No
human has yet certified that `Sound` is the *right* condition to be checking. Under SPEC.md
§0 that audit is what licenses the informal gloss, and it is the human owner's to do.

## Tier B — exact arithmetic

| ID | Claim | Artifact | Rests on |
|---|---|---|---|
| `MX-B-0001` | The Python reference checker agrees with the Lean theorem on concrete ledgers, and additionally rejects cycles, dangling citations, tier/identifier mismatches, evidence overclaims, and citations of Tier X. | `tests/tier_b_tier_calculus.py` (B1–B4, **5 negative controls**) | `MX-A-0003` |
| `MX-B-0002` | No float literal and no call to `float()` occurs under `python/`, `tests/`, or `scripts/` — checked by AST walk, not grep. | `tests/tier_b_no_floats.py` (**2 negative controls**) | — |
| `MX-B-0003` | The Python reference and the dependency-free Rust checker return byte-identical output and identical exit codes on every corpus case, including unsound, cyclic, and malformed ledgers. | `tests/corpus.py` + `scripts/verify.sh` Gate 3 (30 cases) | `MX-B-0001` |
| `MX-B-0005` | All five use-case claims hold on enumerated exact data: UC1 to n=500, UC2 over 1296 combinations, UC3 over 21 frequencies + 5 arbitrary starts, UC4 over 4 primaries × 5 radii, UC5 over 15 625 combinations. | `tests/tier_b_applications.py` (**6 negative controls**) | `MX-A-0006`…`MX-A-0010` |
| `MX-B-0006` | Gate 2's parser handles Lean's **wrapped** `#print axioms` output, and footprints parsed must equal `#print axioms` directives per file. Self-tests run on every invocation. | `scripts/check_footprints.py#self_test` | — |
| `MX-B-0004` | Stream 0's own Lean tree contains **zero** custom `axiom` declarations and **zero** `sorry`, by a scan that strips Lean comments first and matches declarations at any indentation. | `tests/tier_b_axiom_hygiene.py` (**7 negative controls**) | — |

## Tier C — conjecture / observation

| ID | Claim | Artifact | Rests on |
|---|---|---|---|
| `MX-C-0001` | Stream 1 and Stream 5 use the letter **B** for incompatible admission criteria — exact rational arithmetic vs. peer-reviewed literature. A claim exported from one and imported by the other would silently convert a citation into a computation. | `docs/TIER_CALCULUS.md` §1 (both definitions quoted verbatim) | — |
| `MX-C-0002` | **Proposed resolution:** introduce Tier `L` for literature, migrate Stream 5's literature rows `B → L`, reserve `B` for exact arithmetic program-wide. | `docs/TIER_CALCULUS.md` §3 | `MX-C-0001` |
| `MX-C-0004` | ~~**UC5 analytic bridge — OPEN.**~~ **SUPERSEDED by `MX-A-0011`** (2026-08-13): proved, not open. Row retained as the record of the deferral — the promotion changed the identifier rather than editing the tier letter (SPEC.md §2.5). | `Applications/LotkaVolterraFlow.lean` | `MX-A-0010` |
| `MX-C-0006` | **Cross-stream status survey, verified directly.** (a) `RajMathRecovery/NAMAGIRI.lean` (repo root, imported by nothing) defines `Real := Float`, defines `uniformBoundedness`/`topologicalFracture` as `Prop := True`, and proves `hypothesis_U_bound` and `prevents_singularity` `by trivial` — with docstrings claiming to prove Hypothesis U and to prevent the singularity. (b) `TNN/specs/TNN_Invariants.lean:46` has `sorry` in `energy_conservation` while `dashboard/backend/main.py` hardcodes `"PROVEN (Zero-Sorry)"` **15×** as a string literal. (c) RajMath's `dualscale/lean` **excluding vendored Mathlib** has 2 `sorry`/34 `axiom`, confirming `MX-C-0003`. | `docs/FOUNDATIONS.md` §11 | `MX-C-0003` |
| `MX-C-0005` | **Two Mathlib subsets, neither complete.** `MechanicaFluidorum/lean_src` has `Analysis.Calculus.Deriv.*` and `SpecialFunctions.Log.Deriv`; `RajMathRecovery/dualscale/lean` does not. `MX-A-0011` fails against the second and compiles first-try against the first — so `LEAN_ENV_DIR` determines what is *provable*, with no diagnostic separating "false" from "not built". Concrete evidence for `PLAN.md` K1; **partially reverses the K1 downgrade in `OWNER_BRIEF.md` D5.** | `check_footprints.py#DEFAULT_ENV_CANDIDATES` | — |
| `MX-C-0004-old` | *(historical anchor — see `MX-C-0004` above)* | — | — | That the expression proved zero in `MX-A-0010` *is* `dV/dt` along Lotka–Volterra trajectories is **not established**: it needs the chain rule, `Real.log` differentiability, ℝ rather than ℚ, and a solution concept for the ODE. Deliberately **not** axiomatized and deliberately **not** restated as a conditional implication — that shape is the tautology Stream 1's `MillenniumReduction.lean` was demoted to Tier C for on the same date. | `Applications/LotkaVolterra.lean` docstring | `MX-A-0010` |
| `MX-C-0003` | **Axiom / `sorry` survey, 2026-08-13** (comment-stripped lexical scan; Tier C because those trees cannot be compiled from here). Stream 1 `lean_src/`: **0** axioms, **0** `sorry`. Stream 5 `DualScale/`: **34** axioms across 14 files + **2** `sorry`. Stream 5's README states Rules R1/R2 are enforced by `dualscale_ci.yml`; **that file does not exist** and the repo has no `.github/`. The commit introducing both `sorry`s (`e3a82fb`) is titled *"zero-sorry Lean 4 verification"*. **Contamination is latent, not live** — Stream 1 imports only Mathlib and uses Stream 5's tree solely as a Mathlib provider, so no DualScale axiom enters a Stream 1 footprint today. Three overlaps would become load-bearing if one `import` line were added: `aubin_lions_compactness` (axiom there ×2, hypothesis parameter in Stream 1), `dyadic_cascade_conservation` (axiom there, **proved** Tier A in Stream 1), `enstrophy` (axiomatized there, defined in Stream 1). Separately: the `Reff` duplicate `SPEC-STREAM0` §1 expects **does not exist**. | `docs/designs/RECONCILIATION.md` §3–§4 + `tests/tier_b_axiom_hygiene.py --survey` | — |

`MX-C-0003` is filed at Tier C for the same reason as `MX-C-0001`: it is a true observation
about *other repositories' working trees*, recorded with per-file `sha256`, and no gate in this
repository can hold those trees still. The survey that produced it is **informational and never
gates** — making Stream 0's build fail because another stream edited a file would turn the
foundation into a bottleneck (`SPEC-STREAM0` R3.3, `HARDNESS.md` H10).

`MX-C-0001` is filed at Tier C rather than higher on purpose. It is a true observation about
two files as they stood on 2026-08-13, quoted verbatim — but it is a claim about *other
repositories' working trees*, which no gate in this repository can hold still. It becomes
Tier B the day a harness checks both trees at a pinned commit. **`MX-C-0002` is a proposal,
adopted by neither stream.** Nothing here has been agreed with Stream 1 or Stream 5.

---

## What is deliberately absent

No row asserts anything about Navier–Stokes, K3 selection, the string landscape, or the
universe. Stream 0 ships bookkeeping. A green gate here says a stream's records are
internally consistent; it says nothing about physics (SPEC.md §7.9).

*Last verified: see the output of `./scripts/verify.sh`. Ledger rows are added in the same
commit as the artifact that justifies them (PLAN.md §9).*
