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
| `MX-A-0015` | **Phase winding around a discrete loop is quantized** — staged here as the intended Tier A core of the QuantumFluids stream's first theorem, before that stream exists. For nonvanishing `ψ` on `ZMod L`, `∑ₖ arg(ψ(k+1)/ψ(k)) = 2π·n` with `n ∈ ℤ`. The integer is **not assumed**: the increments exponentiate to a product that telescopes to `1` (because `k ↦ k+1` is a bijection of `ZMod L`), and `exp(θi)=1` forces `θ ∈ 2πℤ`. Two witnesses on **the same loop, differing in one amplitude**: `full4 = (1,i,−1,−i)` totals `2π` (winding 1, so not vacuously `n=0`); `hole4`, with site 2 zeroed, totals `π` — **not** a multiple of `2π`, so nonvanishing is load-bearing. *A theorem about complex numbers: no fluid, no `h`, no circulation. Named `Winding`, not `Circulation` — LL-17 applied before the fact.* | `Applications/Winding.lean` — 6 declarations | — |
| `MX-A-0013` | **Parseval on `ZMod N` — Mathlib does not have this.** `∑ₖ 𝓕f(k)·conj 𝓕f(k) = N·∑ⱼ f(j)·conj f(j)`, plus the real-norm form. `Analysis/Fourier/ZMod.lean` defines `dft` but carries **no norm or inner-product lemma at all**; Mathlib's Parseval results are for `AddCircle` and the continuous transform. Built from character orthogonality (`AddChar.sum_mulShift` + `ZMod.isPrimitive_stdAddChar`). The factor `N` is `dft`'s unnormalised convention and is what makes Donoho–Stark's bound `N`. Both `.olean`s verified **built** before estimating (MX-C-0005). | `Duality/Uncertainty.lean` — 5 declarations | — |
| `MX-A-0014` | **Donoho–Stark on `ZMod N` — discharges TARGET T-DS.** For `f ≠ 0`, `N ≤ \|supp f\|·\|supp 𝓕f\|`. From `MX-A-0013` + Cauchy–Schwarz (`sq_sum_le_card_mul_sum_sq`). Corollary `sqrt_le_max_support`: the larger support is `≥ √N` — **`MX-A-0012`'s abstract bound A.1 at `C = N`, applied for the first time to a product hypothesis that is proved rather than assumed.** 2 witnesses: `f ≠ 0` is load-bearing (at `f = 0` both supports are empty, `0 < N`), and the bound is **attained** at `N = 1`. *Says nothing about quantum mechanics — the shared name is an analogy between two inequalities (LL-17).* | `Duality/Uncertainty.lean` — 5 declarations | `MX-A-0013`, `MX-A-0012` |
| `MX-A-0012` | **The abstract self-dual bound, and its instances.** `C ≤ x·y → √C ≤ max x y` (plus the dual, the sandwich, two-term AM–GM, and `x = C/x ↔ x = √C`). Instances as corollaries: `Reff ≥ √α`; the ℕ cast; the **Wilson EOQ** bound `2√(DKh/2) ≤ DK/Q + hQ/2` **with attainment** at `Q* = √(2DK/h)`; and `sinh(2K)² = 1 ∧ K > 0 → K = log(1+√2)/2`. **4 non-vacuity witnesses, both polarities** — the bound is attained, is strict off the self-dual point, is **false** without the sign hypotheses (`x=−1, y=−4`), and the `sinh` hypothesis is satisfiable. 14 declarations. | `lean/Mathesis/Duality/SelfDual.lean` | — |
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
| `MX-B-0007` | **UC6 — the refutation case.** Three proposed conservation laws refuted by explicit exact counterexamples (individual KE in an elastic collision; Lotka–Volterra conserving `x+y`; `Reff` multiplicative in `R`). A fourth of the same kind — relative speed in an elastic collision — is **true** and survives 192 exact cases; the harness fails if it is refuted. | `tests/tier_b_refutations.py` | `MX-A-0007`, `MX-A-0005` |
| `MX-B-0009` | **Exact companion to `MX-A-0015`.** `arg` is transcendental, so the float ban forces a form needing **no angles**: partition nonzero Gaussian rationals into quadrants by *sign*, accumulate transitions in `{−1,0,+1}`, reject the half-turn as ambiguous. Winding = total ÷ 4, and the theorem becomes **"the total is divisible by 4"** — decidable in integers, no π, no rounding. 56 admissible loops (48 correctly refused; **fails if all are skipped**); the unit loop gives **1**, the same number the kernel proves for that loop; reversal `−1`, double traversal `2`, single-quadrant loop `0`; 16 rotations; 12 additivity cases. **5 negative controls, all fired** — including that an **open** path is not quantized, showing divisibility comes from *closure*, the harness twin of `prod_ratio_eq_one`. Two defects planted in copies, observed to exit 1 (LL-3). | `tests/tier_b_winding.py` | `MX-A-0015` |
| `MX-B-0008` | **Exact companion to `MX-A-0012`.** `√C` is irrational for almost every rational `C`, so the bound is checked **squared** — `C ≤ max(x,y)²` — equivalent over the nonnegatives and exactly rational. The float ban forced the reformulation, as it did for Kepler III. 700 cases for the bound; attainment at the self-dual point; `Reff` over 100 cases with equality occurring **exactly twice**, and only where `R² = α`; EOQ optimality over **116 families** whose `2DK/h` is a perfect rational square (1160 comparisons) with the dual costs verified to balance at `Q*`; and the `sinh` core, which **fails if it does not see both roots** of `s²=1`. **5 negative controls, all demonstrated to fire.** Two defects planted and observed to exit 1 before filing (LL-3). | `tests/tier_b_selfdual.py` | `MX-A-0012`, `MX-A-0005` |
| `MX-B-0006` | Gate 2's parser handles Lean's **wrapped** `#print axioms` output, and footprints parsed must equal `#print axioms` directives per file. Self-tests run on every invocation. | `scripts/check_footprints.py#self_test` | — |
| `MX-B-0004` | Stream 0's own Lean tree contains **zero** custom `axiom` declarations and **zero** `sorry`, by a scan that strips Lean comments first and matches declarations at any indentation. | `tests/tier_b_axiom_hygiene.py` (**7 negative controls**) | — |

## Tier L — literature

| id | claim | artifact | supports |
|---|---|---|---|
| `MX-L-0001` | **Chebotarëv's theorem on roots of unity**, retrieved and **quoted** 2026-08-15 (Frenkel, arXiv:math/0312398v3). *For any `I, J ⊆ F_p` of equal cardinality, `(ω^{ij})_{i∈I,j∈J}` has non-zero determinant.* Both lemmas quoted verbatim; proof is reduction mod `(1−ω)` plus **infinite descent** — no differential operator, no `p`-adic valuation, contrary to what I had estimated from memory. **Not proved here; no Lean file contains it.** **Caveat:** Frenkel *asserts* (attributing Tao) that this is equivalent to `\|supp f\| + \|supp f̂\| ≥ p+1`, but does not prove it — so proving Chebotarëv does **not** by itself give T-TAO. That bridge is a separate paper, unretrieved (LL-7). | `docs/TARGET_CHEBOTAREV.md` | — |

## Tier C — conjecture / observation

| ID | Claim | Artifact | Rests on |
|---|---|---|---|
| `MX-C-0001` | Stream 1 and Stream 5 use the letter **B** for incompatible admission criteria — exact rational arithmetic vs. peer-reviewed literature. A claim exported from one and imported by the other would silently convert a citation into a computation. | `docs/TIER_CALCULUS.md` §1 (both definitions quoted verbatim) | — |
| `MX-C-0002` | **Proposed resolution:** introduce Tier `L` for literature, migrate Stream 5's literature rows `B → L`, reserve `B` for exact arithmetic program-wide. | `docs/TIER_CALCULUS.md` §3 | `MX-C-0001` |
| `MX-C-0004` | ~~**UC5 analytic bridge — OPEN.**~~ **SUPERSEDED by `MX-A-0011`** (2026-08-13): proved, not open. Row retained as the record of the deferral — the promotion changed the identifier rather than editing the tier letter (SPEC.md §2.5). | `Applications/LotkaVolterraFlow.lean` | `MX-A-0010` |
| `MX-C-0007` | **Owner decisions, 2026-08-14.** (1) **Tier L adopted** — five tiers are the programme notation; Stream 5's literature rows migrate `B → L`. (2) **R3.4 waived for `TierCalculus`, on the record** — nothing imports it and no external CI calls it; the accepted rationale is that the Python/Rust checkers consume the calculus in substance and the module is cheap (Mathlib-free, ~2s, no deps). *Counter-argument retained:* "exempt because it is cheap" is how every abstraction survives a YAGNI rule, and the waiver removes the only scheduled forcing function for adoption. (3) Stream 0 opens PRs rather than only reporting. | `docs/OWNER_BRIEF.md` | `MX-C-0001`, `MX-C-0002` |
| `MX-C-0006` | **Cross-stream status survey, verified directly.** (a) `RajMathRecovery/NAMAGIRI.lean` (repo root, imported by nothing) defines `Real := Float`, defines `uniformBoundedness`/`topologicalFracture` as `Prop := True`, and proves `hypothesis_U_bound` and `prevents_singularity` `by trivial` — with docstrings claiming to prove Hypothesis U and to prevent the singularity. (b) `TNN/specs/TNN_Invariants.lean:46` has `sorry` in `energy_conservation` while `dashboard/backend/main.py` hardcodes `"PROVEN (Zero-Sorry)"` **15×** as a string literal. (c) RajMath's `dualscale/lean` **excluding vendored Mathlib** has 2 `sorry`/34 `axiom`, confirming `MX-C-0003`. | `docs/FOUNDATIONS.md` §11 | `MX-C-0003` |
| `MX-C-0011` | **The duplicate `Reff` proof stays — and a correction to my own estimate.** (1) `Reff` is proved twice (bespoke in `Scale/Reff.lean`, instance in `SelfDual.lean`). **Both survive, by owner decision:** two independent kernel proofs of one statement is Gate 3's differential philosophy applied *inside* Lean — if an edit breaks one and not the other, that disagreement is information rather than a silent regression. Cost: ~2s of build. `Uncertainty.lean` makes the same trade deliberately, since Gate 2 compiles standalone with no lakefile. (2) **Correction:** I estimated T-DS as multi-day and recommended dropping it, because Mathlib has no Parseval for `ZMod.dft`. Premise true, estimate wrong — the two *hard* ingredients were already there. The owner overrode me and was right. **A theorem's absence from a library is not evidence about the cost of proving it**; cost is set by which ingredients are present, which is a separate question that must be asked separately. | `Uncertainty.lean` (header) + `Scale/Reff.lean` | `MX-A-0005`, `MX-A-0012`, `MX-A-0014` |
| `MX-C-0009` | **The Ising reading of `sinh_selfDual_coupling` — filed apart from the theorem, because it is not what the theorem proves.** Kramers–Wannier pairs couplings by `sinh(2K)·sinh(2K*) = 1`; `K* = K` gives the hypothesis, and `log(1+√2)/2` is Onsager's critical coupling. Going from *self-dual point* to *critical point* needs the transition to be **unique** — assumed by Kramers–Wannier (1941), proved by Onsager (1944) — and that premise is nowhere in the file, which has no lattice, no partition function, no duality map. Tier L citation with a quoted statement still owed (LL-7). Theorem renamed from `kramers_wannier_self_dual`. | `Duality/SelfDual.lean` (header) | `MX-A-0012` |
| `MX-C-0010` | **Review of the proposed `Duality/SelfDual`, by compiling it.** It shipped uncompiled. Two defects: a trailing `ring` after a `field_simp` that had already closed the goal, and `Real.sinh_pos`, which does not exist (`Real.sinh_pos_iff`). **Both theorems were still defined, each with `sorryAx`** — a source-level `sorry` grep would have called the file clean (LL-5, LL-17). 7 of 9 were correct. Two further findings are statement-adequacy failures **no gate detects**: a theorem named for Donoho–Stark whose Fourier content was its own undischarged hypothesis, and one named for Kramers–Wannier containing no Ising model. Two offered citations checked and **real**: Hirschel *et al.*, *Phys. Rev. D* **109**, 095011 (2024); Godfrin *et al.*, *Phys. Rev. B* **103**, 104516 (2021). Neither is citable at Tier L yet — titles verified, quoted statements not on file. | `LL.md#LL-17` | `MX-A-0012` |
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
