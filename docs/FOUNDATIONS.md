# Mathesis — Foundations of a Tier Calculus for Scientific Claims

**Stream 0 of SocrateAI** · Version 1.0 · 2026-08-13
**Tier of this document:** C (governance and exposition). It states no mathematical result of
its own. Every technical claim it makes is either a citation to a Tier A artifact in this
repository, or a Tier C observation about another repository, and is labelled as such.

---

## Table of contents

1. [Context](#1-context) — seven streams, one missing layer
2. [Motivation](#2-motivation) — three failures that were found, not imagined
3. [Narrative](#3-narrative-newton-leibniz-and-the-century-of-ghosts)
4. [Key concepts](#4-key-concepts)
5. [Notation](#5-notation-the-characteristica)
6. [Solver principles](#6-solver-principles)
7. [Methodology](#7-methodology-the-loop)
8. [Domains](#8-domains)
9. [The five use cases](#9-the-five-use-cases)
10. [Benefit, measured](#10-benefit-measured-not-asserted)
11. [Future work: the hard problems](#11-future-work-the-hard-problems)
12. [Conclusion](#12-conclusion)

---

## 1. Context

SocrateAI runs seven concurrent scientific streams. They share mathematics — the T-dual
effective radius `Reff`, the Sym² recurrence lock, dyadic shell decompositions, enstrophy
functionals — and they share a verification technology, Lean 4. What they did **not** share,
before this repository existed, was a way of saying *how strongly anything is known*.

| # | Code | Object of study |
|---|---|---|
| 0 | `MX` | **Mathesis** — the notation, kernel, and ledger the others use |
| 1 | `MF` | MechanicaFluidorum — 3D Navier–Stokes global regularity, via Hypothesis U |
| 2 | `AE` | AutoEvolve — K3 selection in the DualScale K3×T² landscape |
| 3 | `QK` | Quantum Agora — tensor-network, QUBO, and Cirq execution of landscape search |
| 4 | `HG` | Hypergraph — discrete hypergraph cosmology, computation-augmented generation |
| 5 | `RM` | RajMath — the RAMA Ramanujan engine, mock modular forms, BPS entropy |
| 6 | `TN` | TNN Univers Model — thermodynamic/topological neural networks |
| 7 | `VD` | Videoo — scientific communication |

Stream 0 does no science. **Its object of study is the record.** The first theorem here is
about ledgers, not about geometry — and that is the point, because the record is the one
artifact every other stream produces and none of them owns.

## 2. Motivation

Not from first principles. From three failures found by looking.

### 2.1 One letter, two meanings

Stream 1's specification defines:

> **B — Checkable**: identities validated in exact rational arithmetic; no floats.

Stream 5's README defines:

> **Tier B — Established**: Peer-reviewed literature, pinned to exact values.

One means *a program checked it*. The other means *a referee checked it*. These are not close.
And artifacts already cross between those two repositories: Stream 1's Lean gate compiles
against Stream 5's working tree. The day a **claim** crosses with its letter attached, a
citation silently becomes a computation, and nothing in either repository notices.

This is `MX-C-0001`. It is the founding observation.

### 2.2 A rule with no gate

Stream 5's README states five CI rules, attributing them to `dualscale_ci.yml`:

> **Rule R1**: No `axiom` declarations allowed in `.lean` files.

That file does not exist. The repository has no `.github/` directory. A comment-stripped scan
of its Lean tree on 2026-08-13 found **34 `axiom` declarations across 14 files**, plus two
`sorry`. The commit that introduced both `sorry`s is titled *"zero-sorry Lean 4 verification"*.

The sharpest instance, `DualScale/Physics/AubinLions.lean`, axiomatizes the type, the
observable, the **conclusion predicate**, and the **implication** — then proves a theorem by
applying the axiom. Since `aubin_lions_compactness` has no definition, the theorem asserts
nothing falsifiable; and since `VelocityField` has no exhibited inhabitant, the hypotheses may
be vacuous. By that stream's **own Rule R3** — *"logically vacuous propositions are strictly
prohibited and will fail the build"* — it fails. Nothing ran.

This is `MX-C-0003`. It is not an accusation. It is what happens to everyone when no gate runs,
and it is the most legible argument available for why Stream 0 exists.

### 2.3 The same content, handled correctly, still failed

Stream 1 met the *same mathematics* — Aubin–Lions compactness — the stricter way: as named
hypothesis parameters, **never axioms**. It was audited anyway. The verdict, recorded in that
file's own header:

> `AubinLionsStatement` and `ProdiSerrinStatement` as bare `Prop → Prop` arrows *"completely
> bypass PDE theory. The Lean kernel is merely verifying a logical tautology (A → B → C)."*
> **Accepted.** This file remains kernel-compiled and gated (so it cannot rot) but its claims
> are **TIER C** until repaired.

A stream demoted its own flagship reduction and kept the file gated so the demotion could not
be quietly forgotten. That is the standard. Stream 0's job is to make it cheap and general.

## 3. Narrative: Newton, Leibniz, and the century of ghosts

The calculus was founded twice, independently, in the late seventeenth century. Both foundings
were correct. Both built on infinitesimal ideas reaching back through Cavalieri and Fermat to
Archimedes' method of exhaustion. The story of what happened next is the argument of this
document, and it has three acts.

### Act I — Notation is not cosmetic

Newton's *method of fluxions* wrote the derivative of `x` as `ẋ` and reasoned about quantities
flowing in time. Leibniz wrote `dy/dx` and `∫ y dx`, and reasoned about ratios and sums of
differentials.

The two systems are mathematically equivalent. **Leibniz's notation won**, and it won for
reasons that have nothing to do with mathematical content:

- `dy/dx` *displays the chain rule*. `dy/dt = (dy/dx)(dx/dt)` looks like cancellation, so it is
  hard to get wrong. Fluxion notation gives you no such scaffolding.
- `∫ y dx` *carries the variable of integration*. Substitution becomes bookkeeping instead of
  insight.
- Higher derivatives, partial derivatives, and multiple integrals extend by pattern in the
  Leibnizian system, and by invention in the Newtonian one.

British mathematics, loyal to Newton after the priority dispute, kept fluxions and fell behind
Continental analysis for roughly a century. It was not less able. It was worse equipped. The
Analytical Society at Cambridge in the 1810s campaigned explicitly for what it called *"the
principles of pure D-ism against the Dot-age of the University"* — a pun that was also a
correct diagnosis.

**The lesson Stream 0 takes:** the notation you record results in determines which errors are
easy to make and which are impossible to miss. `X < C < L < B < A` is a notation claim, not a
philosophy claim. It is chosen so that "this Tier A theorem cites a Tier L result" becomes
*visibly* wrong — the way `dy/dx` makes a botched chain rule visibly wrong.

### Act II — The dispute was an epistemics failure, and the adjudication was rigged

The priority quarrel was not a disagreement about mathematics. Both men had it. It was a
failure of *record-keeping*: no shared notation, no dated ledger of who established what and
when, no agreed standard of evidence for a claim of precedence.

In 1712 the Royal Society convened a committee to settle it and published the
*Commercium Epistolicum*. The committee was appointed by the Society's president. Its report
was written, anonymously, by the same president — Newton. He then reviewed it, also anonymously.

An institution issued a verdict on a dispute in which its head was a party, and signed it with
its own authority. **The verdict happened to favour the person who was, on the evidence, first
to the method** — and it was still worthless as adjudication, because nothing independent
checked it.

This is exactly §2.2, three centuries earlier: an authority certifying itself, with no gate.
It is why `HARDNESS.md` H8 says *agent self-reports are not evidence*, why Gate 3 fails the
build when two implementations disagree **without adjudicating which is right**, and why this
repository is forbidden from issuing scientific verdicts about the streams it serves.

### Act III — A century of computing on foundations nobody had

Newton and Leibniz both reasoned with infinitesimals that neither could justify. In 1734 George
Berkeley published *The Analyst* and named the problem exactly:

> "And what are these Fluxions? The Velocities of evanescent Increments? And what are these same
> evanescent Increments? They are neither finite Quantities, nor Quantities infinitely small,
> nor yet nothing. May we not call them the Ghosts of departed Quantities?"

Berkeley was **right**. The objection stood, essentially unanswered, until Cauchy and
Weierstrass built the ε–δ foundations in the nineteenth century — roughly 150 years later. And
Abraham Robinson's non-standard analysis (1961) eventually vindicated the infinitesimals
themselves, so the original intuition was sound all along.

Now: **during those 150 years, everyone kept computing, and it worked.** Euler produced an
enormous body of correct results on foundations that did not exist. Withholding the calculus
until it was rigorous would have been a catastrophe for science.

**This is the subtlest and most important lesson, and it is the one a naive reading of a tier
system gets wrong.** The tier calculus does *not* say "do not compute before you are rigorous".
Euler at Tier C was worth more than almost anyone at Tier A. What it says is:

> **Record which one you have.**

Tier X is not a rebuke. It is a *permission* — permission to explore with floats, sample,
guess, and follow intuition, on the single condition that the result is labelled and cannot be
cited as though a machine had checked it. The failure mode is never "someone conjectured". It
is "someone conjectured, and eighteen months later the conjecture was being cited as a
theorem, and nobody could point to when it changed status."

Leibniz himself wanted the fix. His programme had two halves:

- the ***characteristica universalis***, a universal formal notation for concepts;
- the ***calculus ratiocinator***, a mechanical procedure for deciding what follows from what.

His famous promise for disputes — *"Let us calculate, Sir, and see who is right"* —
**never arrived**. What arrived instead, in the twentieth century, was the proof assistant:
a *calculus ratiocinator* that actually runs. Stream 0 is the missing half, the
*characteristica*, built for the specific job of recording scientific certainty rather than
scientific content.

## 4. Key concepts

### 4.1 The tier lattice

Five tiers in one linear order:

```
X   <   C   <   L   <   B   <   A

A  Kernel        Lean 4, zero sorry, axiom footprint matches its declared allowlist
B  Checkable     finite statement decided in exact ℚ/ℤ, deterministic,
                 shipping a negative control DEMONSTRATED TO FAIL
L  Literature    peer-reviewed, cited to a QUOTED THEOREM STATEMENT — not an abstract
C  Conjecture    proposal, analogy, unverified reduction, design memo
X  Exploratory   floats, sampling, plots, LLM output — MAY NEVER BE CITED
```

The order is about **how much of the checking a machine did** — not about mathematical depth.
A Tier L theorem of Bourgain is deeper than every Tier A row in this repository.

Tier `L` is the tier that did not exist before. Its absence is what forced literature and
computation to share the letter `B` (§2.1), and its admission criterion — a *quoted theorem
statement*, never an abstract or a retrieval summary — came from a real incident where a
tool-generated paraphrase conflicted with a stream's own description of its work.

### 4.2 Evidence kinds cap tiers

Orthogonal to the order, every claim declares **how** it was established, and that caps what it
may claim:

| evidence kind | ceiling |
|---|---|
| `lean_axioms` | A |
| `exact_harness` | B |
| `citation` | L |
| `argument` | C |
| `numeric`, `llm_output` | X |

`llm_output` caps at X **by charter**. No model output promotes a tier — including the output
of the model that wrote this sentence.

### 4.3 Soundness, and the theorem that matters

A ledger assigns to each identifier a tier and a list of claims it rests on. It is `Sound` when

> no claim is filed at a tier above any claim it **directly** cites.

Every stream already checks that, informally, by eye. The kernel-verified content of Stream 0 is
that soundness on direct edges propagates through the **entire transitive closure**:

```lean
theorem tier_le_of_depends (hL : Sound L) :
    ∀ {a b : ι}, Depends L a b → (L a).tier ≤ (L b).tier

theorem no_kernel_claim_rests_on_weaker (hL : Sound L)
    (ha : (L a).tier = Tier.A) (hab : Depends L a b) : (L b).tier = Tier.A
```

*(`MX-A-0003`, `MX-A-0004` — Mathlib-free, footprint `[]`.)*

**Why this elementary result earns a kernel proof.** Transitivity is the property informal
bookkeeping loses *first*. A chain `B → B → L` is sound at every direct edge and the head still
rests on literature. Nobody checks the closure by eye, because doing so requires holding the
whole graph in mind, and the graph is exactly the thing that got too big to hold.

The consequence people trip over: **a Tier A claim may not cite a Tier L theorem.** The
resolution is not to weaken the tier system — it is to take the literature result as an explicit
**hypothesis parameter**. The theorem becomes Tier A *conditionally*, the condition is visible
in its type, and the ledger records it.

### 4.4 The model/world split

This is the concept that makes the calculus usable in science rather than only in mathematics.

A scientific claim is almost always **two claims wearing one name**:

| | Claim | Ceiling |
|---|---|---|
| **M** | the mathematics follows from the model | **Tier A** — provable |
| **W** | the model describes the system | **Tier C** at best — empirical |

"Hardy–Weinberg equilibrium" names both the algebra and the assertion that a population is at
it. "Conservation of energy" names both a theorem about a Hamiltonian and a claim about an
apparatus. The Tier A reputation of **M** silently underwrites **W**.

Under the calculus the split is structural rather than rhetorical: **W** is a separate row that
*cites* **M**, and by `MX-A-0004` it can never be Tier A — however good the data is.

### 4.5 Identifiers carry their tier

```
<STREAM>-<TIER>-<NNNN>          e.g.  MF-A-0007,  MX-C-0003
```

The tier letter is **in the identifier**, so a promotion changes the identifier and every stale
citation elsewhere becomes *lexically* wrong instead of *silently* wrong. The old row is kept
and rewritten to point forward; `supersedes` records the trail.

*Worked instance:* `MX-C-0004` (Lotka–Volterra bridge, OPEN) → `MX-A-0011` (proved), 2026-08-13.

## 5. Notation (the *characteristica*)

One symbol table, three columns that must never diverge: LaTeX macro, meaning, Lean identifier.
`latex/mathesis.sty` provides the macros; `docs/NOTATION.md` is the table.

**First-use rule (normative):** a symbol may appear in prose only if its row exists in the table.

| LaTeX | Meaning | Lean |
|---|---|---|
| `\Reff{\alpha'}{R}` | T-dual effective radius `max(R, α'/R)` | `Mathesis.Scale.Reff` |
| `\seam` | fundamental length `√α'` | — derived |
| `\HypU` | Hypothesis U — **quantifier order normative** | `Mathesis.Statements.HypothesisU` |
| `\tier{A}` | epistemic tier tag | `schemas/ledger.schema.json` |
| `\lean{Name}` | the declaration a claim rests on | — |

**Reserved vocabulary.** These words carry gate-backed meanings:

| Word | Reserved for |
|---|---|
| **theorem** | Tier A only |
| **verified** | a kernel or exact-arithmetic gate accepted it, here, reproducibly |
| **established** | Tier A or Tier L — never a Tier B instance check |
| **proven** | Tier A. Not "we checked 10 000 cases" |
| **uniform** | never without its quantifier order stated explicitly |

The `.sty` enforces this structurally: the `mtheorem` environment takes a **mandatory** Lean
declaration name, and `mclaim` takes a **mandatory** tier. An untiered claim in a programme
paper is exactly what the package exists to prevent.

**On quantifier order.** Hypothesis U is `∃C ∀cutoff`, not `∀cutoff ∃C`. Its entire content is
uniformity in the cutoff. Swap the quantifiers and every symbol still typechecks, every proof
still compiles, and the statement has become a much weaker one. No kernel catches that. This is
why quantifier order is normative in prose and why the human audit (§6.5) exists.

## 6. Solver principles

### 6.1 What "solver" means here

> **A solver is a producer of claims that a dumb exact checker can replay.**

Not a thing that computes an answer — a thing that emits a record another, simpler program can
independently re-decide. A certificate that cannot be replayed by a checker simpler than the
producer is not a certificate. Schema: `schemas/certificate.schema.json`.

### 6.2 The four gates

| Gate | Checks | Demonstrated to fail |
|---|---|---|
| 1 | every `tests/tier_b_*.py` exits 0, negative controls included | by construction — the controls are its probes |
| 2 | Lean kernel-compiles; no `sorry`; footprints match declared allowlists | planted `sorry`, `LL-3`; planted indented axiom |
| 3 | Python and Rust checkers agree on 30 corpus cases, byte-for-byte | caught a real divergence on its first run, `LL-1` |
| 4 | `ledger.jsonl` is `Sound`; `LEDGER.md` and it name the same ids | planted orphan id, `LL-10` |

**A gate that has only ever been observed passing is indistinguishable from a gate that cannot
fail.** Every one of the four has been shown to reject a planted defect, and each demonstration
is recorded in `LL.md`.

### 6.3 The footprint is the gate

Never accept "there is no `sorry` in the source" as evidence. A failed proof still defines the
theorem name in the environment; the source looks clean and only `#print axioms` reveals the
`sorryAx`. Stream 1 caught two broken proofs this way that had been *reported as passing*.

### 6.4 Two implementations, no shared dependency

The ledger checker exists in Python and in Rust, each written against the specification rather
than against the other. The Rust crate has **zero** crates.io dependencies, including for JSON —
a differential gate whose two sides call the same library tests that library once and the ledger
logic zero times. When they disagree, **neither is trusted** until a human adjudicates.

### 6.5 The human audit is not automatable

**A theorem is Tier A the moment the kernel accepts it. It is *citable* only after a human has
audited the statement.** The kernel confirms the proof establishes the statement; nothing
mechanical confirms the statement is the one anyone meant.

This is the only step in the pipeline whose output cannot be predicted from the pipeline's own
signals — which is exactly why it cannot be removed to go faster.

### 6.6 No dependency Stream 0 cannot rebuild in a minute

The Lean core is Mathlib-free and cold-builds in ~2s with no `import` at all. The Rust crate has
no dependencies. The Python package is standard-library only. Stream 0's gate is what every other
stream will eventually call; it must never be the reason another stream is blocked.

## 7. Methodology: the loop

```
0 SPLIT  →  1 REFUTE  →  2 CHECK  →  3 PROVE  →  4 ██ HUMAN ██  →  5 FILE
  M vs W     minutes      Tier B     Tier A       audit            both ledgers
```

**0 — Split.** Write **M** and **W** as separate sentences. Only **M** enters the Lean file.

**1 — Refute before proving.** Perturb a coefficient, zero a variable, try the degenerate case,
in exact arithmetic at small parameters. A false conjecture absorbs unbounded proof effort and
returns nothing; a five-second sweep kills most. Stream 1 found a convolution formula, sourced
from a web search, that was **identically zero** — caught at M = 1, 2, 3, and invisible to any
amount of proof effort because the statement was perfectly provable and perfectly useless.

**2 — Check.** Exhaustive over a small exact grid beats random over a large one: a failure names
a reproducible tuple rather than a seed. Ship a control targeting the **plausible near-miss**.

**3 — Prove.** Declare the gate contract in the header. Work over `ℚ` when the harness uses
`Fraction`, so the theorem and the check are about *one* structure rather than two that agree
numerically.

**4 — Audit.** Human. Three questions: does the formal statement say what the gloss claims; are
the hypotheses non-vacuous; **are the quantifiers where the science needs them**.

**5 — File.** Artifact + both ledger rows + gate output, one commit.

**Health is the kill ratio, not the promotion count.** A good run refutes most of what it
proposes. A loop that promotes everything is broken, and a loop that has never produced a
rejection has not been tested.

## 8. Domains

The apparatus is domain-agnostic because it constrains *evidence*, not *content*. What varies by
domain is where the model/world seam falls and which tier is reachable at all.

| Domain | Typical **M** ceiling | Typical **W** ceiling | The characteristic trap |
|---|---|---|---|
| Pure mathematics | **A** | n/a | vacuous statements; junk values (`x/0 = 0`) |
| Theoretical physics | **A** conditional on the force/action law | **L** | fixing a quantified parameter as a global constant |
| Computational physics | **B** | **C** | floats certifying a rounding mode, not a law |
| Population biology | **A** for the model | **C** | the model's assumptions hold of nothing real |
| Molecular biology / genomics | **B** | **C** | statistical significance read as mechanism |
| Machine learning | **X** | **X** | a validated model treated as evidence about the world |
| Quantum hardware | **X** | **X** | sampled, noisy, non-deterministic by construction |

Two rows deserve comment.

**Machine learning and quantum hardware cap at X, and this is not a slight.** It is what lets
them be cited *for what they actually establish*. A quantum annealer's output can **steer** a
landscape search; it can never **support** a claim. A trained model reproducing a dynamic is
Tier X evidence about the model, which is exactly what it is.

**Computational physics is where the float ban does its work.** "Agrees to 10⁻¹⁵" certifies a
rounding mode. The discipline is to reformulate until the statement is exact — and §9's Kepler
case shows that reformulating usually *improves* the statement rather than restricting it.

## 9. The five use cases

Five claims, three sciences, increasing complexity, all Tier A over ℚ or ℝ with an
exact-arithmetic harness checking the same statements. They are deliberately elementary: the
point is that the *apparatus* survives contact with mathematics nobody will argue about, so
that when it is pointed at something contested, a failure is a failure of the claim and not of
the plumbing.

| # | Domain | Claim | Artifact | What it exercises |
|---|---|---|---|---|
| 1 | Mathematics | `1+3+…+(2n−1) = n²` | `OddSums.lean` | the pipeline itself |
| 2 | Physics | elastic collision conserves `p` **and** `E` | `ElasticCollision.lean` | exact vs. "agrees to 10⁻¹⁵" |
| 3 | Biology | Hardy–Weinberg allele invariance | `HardyWeinberg.lean` | **model vs. world** |
| 4 | Physics | Kepler III from inverse-square | `Kepler.lean` | the float ban improving a statement |
| 5 | Biology | Lotka–Volterra conservation | `LotkaVolterra{,Flow}.lean` | **deferral, then promotion** |

### UC1 — Sum of odd numbers

Mathlib-free, ~0.8s. Chosen because a failure can only be the pipeline.

*Taught:* the declared footprint went stale within minutes. The header said `allow=` and the
proof needed `omega`, which carries `[propext, Quot.sound]`. A proof rewrite was attempted to
reach `[]`, failed, and the **declaration** was amended — the direction the rule requires.

### UC2 — Elastic collision

Both momentum and kinetic energy conserved exactly, over 1296 enumerated mass/velocity
combinations, for `m₁+m₂ ≠ 0`.

*The control that matters:* a perfectly **inelastic** collision conserves momentum but **not**
energy. A momentum-only implementation passes it. That control is what makes the energy check
mean something.

*Witness:* at `m₂ = −m₁` the formulae divide by zero, Lean's junk-value convention returns `0`,
and momentum is **not** conserved — which is why the side condition is in both statements.

### UC3 — Hardy–Weinberg: the model/world split

Allele frequency is invariant under random mating; equilibrium is reached in **one** generation
from arbitrary starting genotype frequencies.

The algebra is Tier A. *"This population is at Hardy–Weinberg equilibrium"* is Tier C at best —
the model assumes infinite population, random mating, no selection, mutation, migration, or
drift, and not one holds of any real population. In most write-ups one phrase covers both, and
the Tier A reputation of the first underwrites the second.

*The control that matters:* selection against the recessive homozygote **moves** the allele
frequency. Hardy–Weinberg exists to make selection visible; a check that could not detect a
violation would make the null model unfalsifiable.

### UC4 — Kepler III: the float ban earning its keep

`T² ∝ a³` carries π, which is irrational, so nothing is exactly checkable and the standard
response is floats. But **π was never carrying any physics.** With the reduced period
`τ = T/2π = 1/ω`:

```
r³/τ² = ω²r³ = GM
```

Exactly rational whenever `r` and `GM` are; the constant becomes `GM` rather than `4π²/GM`; π
has left the statement. Nothing approximated, nothing lost — `T² ∝ a³` follows because `T` and
`τ` differ by the same factor for every orbit.

**The constraint did not make the physics harder to state. It located a constant that was
decoration and removed it.**

*The control that matters:* under an inverse-**cube** force, `ω²r³` stops being constant — so
the check is about gravity, not arithmetic.

### UC5 — Lotka–Volterra: deferral, then promotion

*First half.* The algebraic core — substituting the vector field into `dV/dt` and clearing the
logarithmic derivatives leaves an expression identically zero. Four terms cancelling in pairs.
Verified over 15 625 exact parameter combinations.

The analytic step — that this expression **is** `dV/dt` — was filed **OPEN at Tier C**, refusing
both shortcuts: `axiom` (forbidden), and the conditional restatement *"given `dV/dt = D`, and
`D = 0`, therefore `dV/dt = 0`"* — which compiles, carries no axioms, looks like Tier A, and is
a tautology of exactly the shape Stream 1 was demoted for.

*Second half.* **The deferral was wrong, and finding out why was the more useful result.** The
calculus modules were absent from one Mathlib checkout and present in the other. Pointed at the
second, `conserved_along_flow` compiles on the first attempt, in nine lines. `V` is now proved
genuinely constant along any trajectory: derivative exactly `0`, not "0 given that it is 0".

`MX-C-0004` → `MX-A-0011`. New identifier, `supersedes` recorded, old row retained pointing
forward. **This is the first tier promotion in the ledger** — until it happened, the promotion
rule was schema with no instance.

*The refusals were right regardless.* Had the calculus genuinely been missing, `axiom` and the
tautological conditional would both still have been wrong answers.

## 10. Benefit, measured (not asserted)

The honest measure of an apparatus is not how many claims it certifies but **whether it has
recently caught something its author believed**. By that measure:

### Defects found in the gates, by the campaign

1. **Gate 2 was silently skipping theorems.** Lean wraps `#print axioms` output past its line
   width; the parser was line-anchored and dropped every wrapped declaration.
   `ElasticCollision.lean` reported *"1 footprint"* for a file with two theorems, **and passed**.
   Because wrapping is triggered by long names, the bug hid precisely the deeply-namespaced
   declarations in new modules. It is a false *all-clear*, in the gate that is the sole evidence
   for every Tier A row. Fixed; the gate now cross-checks `#print axioms` directives against
   footprints parsed, and runs parser self-tests on every invocation. (`LL-11`)

2. **Two theorems had never been footprint-checked** — `Tier.X_le` and `witnessChain_reach` had
   no `#print axioms` line since they were written. (`LL-11`)

3. **The axiom scanner was evadable by one space.** It matched `^axiom` at column 0, so
   `  axiom sneaky`, `private axiom`, and `@[simp] axiom` all passed. Its "ignores prose"
   control passed *for the same reason it was evadable*. One property was bought with the other
   and the suite could not tell. (`LL-9`)

4. **Three non-vacuity witnesses were wrong on first attempt** — parameters chosen by
   inspection landed on degenerate cases, and one "counterexample" was simply false (`½ + ½`
   does sum to 1). All caught by the kernel with `⊢ False`. (`LL-12`)

5. **A deferral rested on an unchecked premise.** A missing Lean module reports as an unknown
   identifier — indistinguishable from a nonexistent lemma or a false statement. An unbuilt
   module masqueraded as a mathematical obstruction. (`LL-13`)

Items 1, 2 and 3 would have stayed invisible without the campaign. That is the argument for
running elementary cases through new apparatus **before** pointing it at anything that matters.

### Findings about the streams

The Tier B collision (`MX-C-0001`); the CI file that does not exist while 34 axioms and 2
`sorry` sit in the tree it claims to gate (`MX-C-0003`); and two Mathlib subsets that differ,
neither complete, so that which one is resolved determines what is *provable* (`MX-C-0005`).

A fourth, found by direct verification on 2026-08-13 (`MX-C-0006`), is the same shape in two
more streams: `TNN/specs/TNN_Invariants.lean:46` contains `sorry` in `energy_conservation`, while
that stream's dashboard hardcodes `"lean4_status": "PROVEN (Zero-Sorry)"` **fifteen times as a
string literal**, computed from nothing. And `RajMathRecovery/NAMAGIRI.lean` proves Hypothesis U
and singularity prevention `by trivial` over `Prop := True`, with `Real` defined as `Float`.

**The recurring pattern across four of seven streams is not bad mathematics. It is a status
string that no check produces.** A README asserting a CI file that does not exist; a dashboard
field that is a literal; a docstring describing what a `trivial` proof would establish if its
predicate were not `True`. In every case the *code* is honest and the *label* is not, and there
is no gate between them. That gap is the entire product.

All were found by looking, with a scanner and a compiler. None required judgement about anyone's
science.

**One was found by *not* trusting a scanner.** A survey subagent reported "839 `sorry` and 264
`axiom`" in Stream 5's tree. Re-measured excluding the vendored Mathlib: **2 and 34**. The agent
had counted Mathlib itself, where `sorry` appears in test files and where `axiom` is how
`propext` and `Classical.choice` are *defined*. The figure was specific, confident, and made the
case being argued stronger — three reasons to check it harder, all of which push the other way.
`HARDNESS.md` H8 applies to this session's own subagents (`LL-15`).

### What is deliberately not claimed

That any of this is true of the world. Every Tier A row is a statement about a model whose
assumptions are written into the theorem's type. **A green board says the bookkeeping holds. It
licenses nothing about collisions, populations, planets, fluids, or the universe.**


---

## 11. Future work: the hard problems

This section is **Tier C throughout**. It describes what the apparatus would contribute to five
hard problems. It does not claim progress on any of them, and Stream 0 is forbidden from issuing
scientific verdicts about the streams it serves.

The contribution is the same in every case, and it is worth stating once before specialising:

> Hard problems fail at the **seams** — where an unproven analytic step is quietly absorbed,
> where a quantifier is fixed that should have stayed free, where a Tier C model assumption
> inherits the authority of the Tier A algebra built on top of it. Mathesis does not attack the
> problem. It makes the seams **visible, typed, and mechanically checked**, so that effort is
> spent where the difficulty actually is.

### 11.1 Navier–Stokes, and how to avoid the singularity

**The problem.** Global regularity for 3D Navier–Stokes: do smooth initial data remain smooth
for all time, or can enstrophy `‖∇u‖²_{L²}` blow up in finite time? Stream 1 attacks it via
**Hypothesis U** — uniform-in-α′ enstrophy control of the frequency-truncated system:

```
    sup      sup      ‖∇u^(α′)(t)‖_{L²(𝕋³)}  <  ∞
   α′>0   0≤t≤T
```

**Where the tier seam falls, and why it is the whole problem.** The quantifier order is the
content. `∃C ∀α′` says one constant works for every truncation — which is what lets `α′ → 0`
recover the true equation. `∀α′ ∃C` says each truncation has its own constant, which is nearly
free and implies nothing.

**Both typecheck. Both compile. No kernel distinguishes them.** Fix `α′` as a global constant
and every symbol still elaborates while the statement silently becomes a much weaker claim. This
is precisely why quantifier order is normative in the notation standard (§5) and why the human
audit's third question is *"are the quantifiers where the science needs them"*.

Stream 5's `TDuality.lean` shows the failure mode live: it declares
`noncomputable def alpha_prime : ℝ := 1`. With `α′` pinned, every statement about the
`α′ → 0` limit is unstateable and nothing reports it.

**Singularity avoidance — the mechanism, and what is already Tier A.** The dual-scale programme's
geometric idea is that the effective radius seen by the truncated system is

```
Reff(α′, R) = max(R, α′/R)
```

which **cannot go below `√α′`**. Below the seam the scale *bounces*: `R < √α′` gives
`Reff = α′/R > √α′`. There is no path to zero scale. Stream 0 has proved this, unconditionally
and axiom-free (`MX-A-0005`, `lean/Mathesis/Scale/Reff.lean`):

| Theorem | Content |
|---|---|
| `Reff_pos` | the effective radius is never zero |
| `Reff_ge_sqrt` | `√α′ ≤ Reff α′ R` — **a universal floor** |
| `Reff_eq_sqrt_iff` | the floor is attained at **exactly one** point, the self-dual radius |
| `Reff_bounce` | below the seam, `Reff = α′/R` — the reflection |
| `genesis_no_singularity` | `0 < tDualRadius α′ R` — no collapse |
| `one_div_sq_le_of_sqrt_le` | `√α′ ≤ x ⟹ 1/x² ≤ 1/α′` — the floor as a bound on inverse-square quantities |

That last one is the bridge to the fluid estimates: a minimum length becomes a **maximum** on
the `1/x²` factors that drive an enstrophy cascade. `Reff_ge_sqrt` upgraded from "a barrier
exists" to "the barrier is the self-dual scale and nothing below it is reachable" is exactly the
form a no-blow-up argument needs.

**What Mathesis contributes, concretely.**

1. **`α′` is a hypothesis parameter in every one of those theorems, never a global constant.**
   That is enforced, not intended.
2. **It made a demotion possible and survivable.** `MillenniumReduction.lean` encoded the shape
   *Hypothesis U ⇒ global regularity* with the two undischarged analytic steps (Aubin–Lions,
   Prodi–Serrin) as named hypothesis parameters — the correct construction. An audit found the
   bare `Prop → Prop` arrows still "completely bypass PDE theory", and the stream **accepted
   demotion to Tier C while keeping the file gated so it could not rot**. Under the calculus that
   demotion propagates automatically: by `MX-A-0004`, nothing may cite it above Tier C.
3. **It forbids the shortcut that would end the programme quietly.** `axiom aubin_lions_compactness`
   exists in Stream 5's tree today. Were Stream 1 ever to import it, its Tier A footprints would
   silently absorb an unproven analytic claim. Its own footprint gate is what prevents that, and
   `MX-C-0003` is the standing record that the temptation is one `import` line away.

**The failure mode, in the wild.** `RajMathRecovery/NAMAGIRI.lean` — a standalone file at that
repository's root — contains:

```lean
def Real := Float                                            -- line 11
def uniformBoundedness (D : EnstrophyFunctional) : Prop := True
/-- Ramanujan's sum of tails algebraically bounds the ultra-high-frequency
    modes, proving Hypothesis U. -/
theorem hypothesis_U_bound (D : EnstrophyFunctional) : uniformBoundedness D := by
  trivial

def topologicalFracture (state : Complex) : Prop := True
/-- At α′ → 0, the continued fraction forces the singular set into discrete
    non-communicating states. -/
theorem prevents_singularity (res : Nat) : topologicalFracture (fractionLimit res) := by
  trivial
```

The predicates are `True`. The proofs are `trivial`. `Real` is `Float`. The docstrings claim
Hypothesis U and singularity prevention — the two central objects of the Navier–Stokes
programme.

**In fairness, and precisely:** the file is imported by nothing and appears in no lakefile, so it
contaminates no build and no gated claim rests on it. It is a skeleton, and writing skeletons is
legitimate. What is missing is the label. Under the calculus this is Tier X — `Prop := True` is
the definition of a vacuous statement, and Stream 5's own Rule R3 forbids exactly it. The gap
between a sketch and a claim is one docstring wide, and nothing currently sits in it.

Verified directly, 2026-08-13 (`MX-C-0006`).

**First task.** Promote `MX-C-0001` to Tier B, then export Stream 1's ledger and run Gate 4
against it. The interesting output is not pass/fail but the **shape**: which Tier A results have
no Tier A consumers, and where the reduction's weight actually rests.

### 11.2 Quantum wave, T-duality, K3×T² and F-theory

**The problem.** Select the K3×T² geometry reproducing observed cosmological parameters —
treating the landscape as a search space rather than an anthropic accident. Streams 2, 3 and 4
attack it by evolutionary search, quantum execution (tensor networks, QUBO annealing, Cirq), and
discrete hypergraph cosmology.

**Where the tier seam falls.** This is the domain most exposed to **tier inflation**, because
candidates are produced *mechanically and in volume*. A search result is Tier X until something
checks it, and the gap between "the search proposed it" and "we verified it" is where a landscape
programme loses its footing.

**What Mathesis contributes.**

- **Quantum hardware output is Tier X, mechanically.** `numeric` caps at X and X may never be
  cited. A D-Wave anneal or a Cirq run can **steer** a search; it can never **support** a claim.
  This is not a limitation imposed on Stream 3 — it is what lets Stream 3's results be cited for
  what they establish.
- **The unresolved question, stated rather than assumed.** Is a search-produced candidate that
  passes an exact-arithmetic filter *Tier B*, or *Tier X with a Tier B filter-result attached*?
  These are different claims. Stream 0 has not decided it; it is reserved to the owner.
- **`Reff` becomes one definition instead of three.** Streams 1, 4 and 6 each carry their own
  account of the T-dual effective radius and nothing detects drift. `MX-A-0005` is the
  consolidation, with the person-name removed per the naming rule.
- **F-theory and Picard–Fuchs.** Stream 5's `Geometry/PicardFuchs.lean` currently carries
  `axiom pf_order_topology_map`. Converting that to a hypothesis parameter costs nothing
  mathematically and makes every downstream claim's dependence on it visible.

**First task.** Type the boundary between search and verification: a Tier X row for the search
output, a Tier B row for the filter result, and an explicit `supports` edge between them, so the
promotion path from candidate to claim is a ledger operation rather than a habit.

### 11.3 Black hole entropy

**The problem.** Reproduce the Bekenstein–Hawking entropy by microstate counting. Stream 5's
route is BPS state counting through Ramanujan-type asymptotics — `macroscopicEntropy`, `cEff`,
`isBPS`, Rademacher expansions, saddle-point asymptotics, and a Hagedorn transition at `T_H`.

**Where the tier seam falls.** Between the **counting function** and the **entropy**. The
asymptotic growth of a partition-like generating function is a hard but ordinary analytic fact.
That this growth *is* the entropy of a black hole is a physical identification resting on a chain
of dualities. These are `M` and `W`, and they are routinely written as one sentence.

**What Mathesis contributes — and here the finding is concrete.** Every step of that chain in
Stream 5's tree is currently an **axiom**:

| File | Axiom |
|---|---|
| `Asymptotics/BPSEntropy.lean` | `bps_macroscopic_entropy` |
| `Asymptotics/Rademacher.lean` | `rademacher_first_order` |
| `Asymptotics/SaddlePoint.lean` | `saddle_point_asymptotic` |
| `Physics/SpectralGap.lean` | `bps_implies_spectral_gap`, `susy_broken_no_gap`, `E_0`, `E_1` |
| `Physics/PhaseTransition.lean` | `T_H`, `t_h_pos`, `hagedorn_divergence` |
| `QSeries/ModularTransform.lean` | `modular_s_transform` |
| `QSeries/ContinuedFraction.lean` | `rogers_ramanujan_identity` |

The entropy function itself is concrete and reasonable —
`macroscopicEntropy (c_eff n : ℝ) := 2 * Real.pi * sqrt (c_eff * n / 6)`, the Cardy formula.
It is the *chain around it* that is axiomatized.

`rogers_ramanujan_identity` is a **theorem** — proved, famous, and available in the literature.
As an axiom it contributes nothing but risk: it is Tier L material entered at a level that
permanently pollutes every downstream footprint.

**The fix is mechanical and loses nothing.** Convert each `axiom` to a hypothesis parameter. The
theorems survive, become explicitly conditional, and the dependence becomes visible in the type
instead of invisible in the footprint. Results with genuine literature backing then move to
Tier **L** — the tier that did not exist before, and precisely the one this material needs.

**First task.** `Physics/AubinLions.lean` and `Asymptotics/BPSEntropy.lean`, in that order,
under a footprint gate installed *first* so the conversion is measured rather than asserted.

### 11.4 Dark matter and dark energy

**The problem.** The most evidence-rich and model-poor domain in physics: a large, consistent
body of observation (rotation curves, lensing, the CMB acoustic peaks, supernova distance
moduli, BAO) and a wide space of models fitting it — ΛCDM with a cosmological constant, modified
gravity, and the discrete-hypergraph route Stream 4 pursues.

**Where the tier seam falls, and why this domain is the hardest for tiering.** Nowhere else is
the model/world gap wider or more consequential. The **observations** are Tier L — peer-reviewed,
pinned to published values with quoted uncertainties. The **fits** are Tier B at best, and only
if the fitting is exact and deterministic, which it usually is not. The **interpretations** —
*"therefore dark energy is a cosmological constant"* — are Tier C, and they are what gets
reported.

The characteristic failure is not fabrication. It is a Tier C model selection acquiring, over a
few years of citation, the felt authority of the Tier L observations it was fitted to.

**What Mathesis contributes.**

- **Model comparison becomes a ledger query.** Competing models citing the same Tier L
  observational rows, each at its own tier, make *"what does this rest on that the alternative
  does not?"* answerable by traversing `supports` rather than by literature review.
- **Parameter provenance survives.** A cosmological parameter used downstream carries the row it
  came from — measurement, fit, or assumption. Today that distinction lives in prose and does
  not survive being copied.
- **Hypergraph cosmology gets the right instrument.** Stream 4's computation-augmented
  generation — deterministic symbolic evaluation replacing probabilistic recall, explicitly to
  eliminate mathematical hallucination — is the same instinct as the tier calculus at a
  different layer. A Wolfram evaluation is `exact_harness` (B) when exact and deterministic, and
  `numeric` (X) when it is not; **which one depends on the call, not on the tool.**
- **A simulation is Tier X.** An N-body run is sampled and floating-point. It may steer; it may
  not support.

**Honest limit.** Stream 4's tree has **not** been audited the way Stream 5's was. What is known
is only its shape: it carries `dark_matter/`, `proofs/`, `lean_oracle/`, an MFDM continuum-limit
paper, and NANOGrav SGWB specifications — and it is the only one of the seven that is **not a git
repository**, so it has no commit history to audit against. Its tier vocabulary, Lean inventory,
and `axiom`/`sorry` counts are **unmeasured**. Nothing here should be read as a finding about it,
and the absence of a finding is not a clean bill.

**First task.** One Tier L row with a quoted value and uncertainty from a published source —
a Planck parameter, say — and one Tier C row that fits to it. The point is to force the schema
to carry an uncertainty, which no current row does.

### 11.5 DNA and genetics

**The problem.** From sequence to mechanism: which variants cause which phenotypes, and by what
pathway. No SocrateAI stream works on this *yet*, though two have written it into their forward
plans: Stream 6's frontier names *"scRNA-seq topological networks … multi-gene epigenetic
regulation … in oncology"*, and Stream 5 has a design note proposing to *"treat DNA folding or
the propagation of genetic mutations as a cellular automaton"*. It is included here because it
is the domain where the model/world gap is *routinely* fatal and the tier discipline transfers
unchanged.

**Where the tier seam falls.** UC3 is already the entry point. The Hardy–Weinberg algebra is
Tier A; *"this population is at Hardy–Weinberg equilibrium"* is Tier C. Every genome-wide
association study rests on that distinction, and the characteristic failure is a **statistical
association read as a mechanism** — a Tier B correlation cited as a Tier A causal claim.

**What Mathesis contributes.**

- **The `M`/`W` split, unchanged.** Population-genetic mathematics — Hardy–Weinberg,
  Wright–Fisher, coalescent theory, linkage disequilibrium decay — is Tier A given its model.
  That any population satisfies the model is Tier C, always.
- **`llm_output` caps at X, and this domain needs it most.** Sequence models are now routinely
  used to predict variant effects. A model's confidence is Tier X evidence about the model. It
  is not evidence about a genome, however well the model validates.
- **Exact combinatorics is genuinely reachable.** Segregation ratios, linkage distances,
  pedigree probabilities, and Hardy–Weinberg expectations are all exact rational arithmetic.
  Much of classical genetics is Tier B material currently reported in floats.
- **Multiple testing becomes structural.** A significance threshold is a property of a *set* of
  claims, not of one. A ledger that records the whole tested set makes the correction auditable
  rather than trusted.

**First task.** UC6: Mendelian segregation ratios in exact arithmetic, with the negative control
being a linked-loci case where independent assortment **fails**. Same shape as UC3's selection
control, and it extends the campaign into a third biological model.

---

## 12. Conclusion

Leibniz's programme had two halves. The *calculus ratiocinator* — a mechanical procedure for
deciding what follows from what — arrived three centuries late, as the proof assistant, and it
works. The *characteristica universalis* — the notation those procedures operate on — did not
arrive, and its absence is what this repository addresses.

Not a universal notation for *concepts*. Leibniz's ambition there was too large and probably
incoherent. A universal notation for **certainty**: five tiers, one linear order, an orthogonal
evidence kind that caps what each row may claim, and one kernel-verified theorem saying that
soundness on direct citations propagates through the entire transitive closure.

The theorem is elementary. That is deliberate. It earns a kernel proof not because it is hard
but because **transitivity is the property informal bookkeeping loses first** — every stream
checks direct citations by eye, and none checks the closure, because the closure is exactly the
thing that grew too big to hold in mind.

Three things are worth carrying away.

**First, the notation is the mechanism.** Leibniz's `dy/dx` beat Newton's `ẋ` not by being more
correct but by making a botched chain rule *visibly* wrong, and a century of British mathematics
paid for the difference. `X < C < L < B < A` is chosen on the same principle: to make "this Tier
A theorem cites a Tier L result" a lexical error rather than a judgement call.

**Second, low tiers are permissions, not rebukes.** Newton and Leibniz computed for 150 years on
foundations Berkeley correctly demolished, and they were right to. Euler at Tier C was worth
more than almost anyone at Tier A. The tier calculus does not ask anyone to wait for rigour. It
asks them to **record which one they have** — because the failure was never that someone
conjectured, but that eighteen months later the conjecture was being cited as a theorem and
nobody could say when it changed status.

**Third, the apparatus must be tested on things nobody disputes.** Five elementary use cases
across mathematics, physics and biology found five defects — three in the gates themselves,
including a false all-clear in the gate that is the sole evidence for every Tier A row, and one
deferral resting on a premise nobody had checked. Three of those would have stayed invisible.
Pointing an unvalidated instrument at a Millennium Problem tells you nothing about the problem.

What Stream 0 refuses is as load-bearing as what it provides. It issues no scientific verdicts.
It does not automate the human statement-adequacy audit — the one step whose result cannot be
predicted from the pipeline's own signals, which is precisely why it cannot be removed to go
faster. It does not adjudicate when two independent implementations disagree; it fails the build
and escalates to a person. And it does not claim that a green board licenses anything beyond
the internal consistency of a record.

The 1712 *Commercium Epistolicum* reached the right conclusion about priority and was worthless
as adjudication, because the president of the deciding body wrote the verdict on his own dispute
and signed it with the institution's authority. Being right is not the same as being checkable.
A programme that cannot tell the difference will eventually be unable to tell whether it is
right.

*Calculemus* was never a promise that the calculation would succeed — only that when it did not,
everyone would be able to see exactly where.

---

### Artifacts

| | |
|---|---|
| Kernel core | `lean/Mathesis/TierCalculus.lean` — Mathlib-free, footprint `[]` |
| Consolidated `Reff` | `lean/Mathesis/Scale/Reff.lean` |
| Use cases | `lean/Mathesis/Applications/` — 5 cases, 6 modules |
| Reference checker | `python/mathesis/` — standard library only, no floats |
| Independent checker | `rust/mathesis-verify/` — zero dependencies, including JSON |
| Gates | `scripts/verify.sh` — four gates, each demonstrated to fail |
| Ledger | `LEDGER.md` + `ledger.jsonl` — 22 rows, `Sound` |
| Lessons | `LL.md` — 14 entries, each with its incident |
| Notation | `latex/mathesis.sty`, `docs/NOTATION.md` |
| Decisions reserved to the owner | `docs/OWNER_BRIEF.md` |

**Status.** All four gates green. **Not signed off**: no human statement-adequacy audit has been
performed, so Stream 0's own ledger currently carries the very gap it exists to close in others,
and says so in `LEDGER.md`. That audit is `PLAN.md` A1 and it is the first task.
