# Stream Map — the seven streams and the surfaces between them

Stream 0's customers. Recorded as observed in `~/xdev/` on 2026-08-13; where a stream's own
documents make a claim about itself, that is a **Tier C** report of what the file says, not a
Stream 0 endorsement.

---

## The streams

| # | Code | Repository | Object of study |
|---|---|---|---|
| **0** | `MX` | `SocrateAI-Scientific-Mathesis` | the notation, kernel, and ledger the others share |
| **1** | `MF` | `SocrateAI-Scientific-MechanicaFluidorum` | 3D Navier–Stokes global regularity — the **HoloAlg** program, organized around Hypothesis U |
| **2** | `AE` | `SocrateAI-Scientific-AutoEvolve-K3xT2` | **K3 selection** in the DualScale K3×T² landscape, via neuro-symbolic evolutionary search |
| **3** | `QK` | `SocrateAI-Scientific-Quantum-K3xT2` | quantum execution of landscape search — tensor networks, QUBO, Cirq |
| **4** | `HG` | `SocrateAI-Scientific-Hypergraph-K3xT2` | discrete hypergraph cosmology; Wolfram computation-augmented generation |
| **5** | `RM` | `SocrateAI-Scientific-RajMathRecovery` | the **RAMA** Ramanujan neuro-symbolic engine; mock modular forms |
| **6** | `TN` | `SocrateAI-Scientific-TNN-UniversModel` | the **Topological Neural Network** / Univers Model; the vHPU |
| **7** | `VD` | `SocrateAI-Scientific-Videoo-K3xT2` | scientific communication and video generation |

Stream 7 produces no claims and needs no ledger; it is listed because it *consumes* them, and
a promotional video is exactly where an un-tiered claim does the most damage.

---

## Stream 1 — MechanicaFluidorum (HoloAlg / Navier–Stokes)

**What it is.** A staged, verifier-in-the-loop program on the global regularity of 3D
Navier–Stokes, organized around **Hypothesis U**: uniform-in-α′ enstrophy control of the
frequency-truncated system,

    sup_{α′>0} sup_{0≤t≤T} ‖∇u^(α′)(t)‖_{L²(𝕋³)} < ∞.

**What Stream 0 takes from it.** Almost everything procedural. Stream 1 is the most mature
governance model in the program, and Stream 0's SPEC is largely its rules generalized:
the three-tier gating, the honesty clause, counterexample-before-attack, the single-active-file
discipline, non-vacuity witnesses, and the rule that agent self-reports are not evidence.
Two of those were written after real incidents; see `LL.md`.

**What Stream 0 owes it.**
- A standalone Mathlib build. Stream 1's Gate 2 currently compiles against **Stream 5's**
  working tree — its own `CLAUDE.md` says so, and calls the standalone cold build a
  still-open Stage-0 chore. That is a cross-stream dependency on an uncontrolled directory,
  and it is Stream 0's to own (`PLAN.md` K1).
- Tier **L**, so that results like Proposition 5.1 — currently tagged *"Tier C: paper-level
  standard result"* — and the five obstructions (Tao 2016, CKN 1982, Buckmaster–Vicol) can be
  filed as what they are: established literature, not conjecture.

**Interface.** `lean_src/CallensDualScale.lean` defines `Reff`, which Streams 4 and 6 also
use. That is the first candidate for the shared notation layer (Stage 4).

## Stream 2 — AutoEvolve (K3 selection)

**What it is.** Evolutionary search for the K3×T² geometry reproducing observed cosmological
parameters, treating the string landscape as a search space rather than an anthropic accident.

**Interface with Stream 0.** This stream generates candidates mechanically, which makes it the
one most exposed to tier inflation: a search result is Tier X until something checks it, and
the gap between "the search proposed it" and "we verified it" is where a landscape program
loses its footing. Its `lean_oracle/` is the natural Tier A boundary.

**Open question for the human owner.** Whether a search-produced candidate that passes an
exact-arithmetic filter is Tier B, or Tier X with a Tier B *filter result* attached. These
are different claims and the distinction matters; Stream 0 has not decided it.

## Stream 3 — Quantum Agora

**What it is.** Three execution paradigms for landscape search: tensor networks, D-Wave QUBO
annealing, Cirq on Google Quantum AI.

**Interface.** Hardware results are irreducibly Tier X — sampled, noisy, non-deterministic.
The tier calculus already handles this correctly and unsentimentally: `numeric` caps at X, and
X may never be cited. A quantum annealer's output can *steer* a search; it can never
*support* a claim. Stream 3 already ships a `quantum-execution` skill, which is the closest
prior art to Stream 0's skills.

## Stream 4 — Hypergraph (Wolfram CAG)

**What it is.** Discrete hypergraph cosmology, replacing retrieval-augmented generation with
**computation**-augmented generation — deterministic symbolic evaluation instead of
probabilistic recall, explicitly to eliminate mathematical hallucination.

**Interface.** CAG is the same instinct as the tier calculus, applied to a different layer:
do not trust a language model about a number. A Wolfram evaluation is `exact_harness` (Tier B)
when it is exact and deterministic, `numeric` (Tier X) when it is not — and which one it is
depends on the call, not on the tool.

## Stream 5 — RajMath / RAMA

**What it is.** An automated Ramanujan-style discovery pipeline: heuristic conjecture
generation, then filtering, then formal verification.

**Interface.** Stream 5 owns the Mathlib build the whole program compiles against, and it is
the other half of the Tier B collision (`docs/TIER_CALCULUS.md` §1). Its CI rules R1–R5 are
independently derived versions of Stream 0's — R3 in particular (*"theorem statements of type
`True` or logically vacuous propositions are strictly prohibited"*) is the non-vacuity rule,
arrived at separately. Two streams inventing the same rule independently is the strongest
available evidence that it belongs in the shared layer.

## Stream 6 — TNN Univers Model

**What it is.** A physics foundation model: thermodynamic, topological, tensor neural
networks, trained against energy and geometry rather than statistical loss.

**Interface.** Stream 6 supplied the **hardness / frontier** vocabulary this repository uses
(`HARDNESS.md`, `FRONTIER.md`), including the NOTODO list — anti-patterns stated as strongly
as goals. Its `Best_Practices_and_Hardness.md` demands zero-`sorry` Lean verification of the
core algebraic rules; that demand lands on Stream 0.

Its inputs are also where tier discipline is hardest and matters most: a trained model's
output is Tier X, always, no matter how well it validates. `llm_output` capping at X is not
a slight against Stream 6 — it is what lets Stream 6 be cited *for what it actually
establishes* (that a model reproduces a dynamic) rather than for what it suggests.

---

## The surfaces where claims cross

Ranked by how much damage a silent failure does.

| # | Surface | Status |
|---|---|---|
| 1 | **Tier letters** between Stream 1 and Stream 5 | **Collision, unresolved.** `MX-C-0001` |
| 2 | **The Mathlib build** — Stream 1's gate depends on Stream 5's working tree | Known fragility, documented by Stream 1 itself. `PLAN.md` K1 |
| 3 | **`Reff`** — three streams maintain their own account of one object | No shared definition. Stage 4 |
| 4 | **Lean theorems** — Stream 1's task F1 imports from Stream 5's tree | Works; unversioned |
| 5 | **Narrative → publication** — Stream 7 renders claims for an audience | No tier survives the trip to video. Highest-consequence surface, least instrumented |

Surface 5 deserves its ranking. Every other failure here is caught eventually by a gate or a
reviewer. A claim that reaches a video has left the system entirely, and the retraction, if
one is ever needed, is public.
