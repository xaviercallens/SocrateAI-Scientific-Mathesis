# Tier A audit pack — 15 rows

**Tier of this document:** C. It is a reading aid for a decision only a person can make.
It asserts nothing and licenses nothing.

---

## What you are being asked to do, and why no machine can do it

Every row below is **kernel-clean**: Lean accepted the proof, and `#print axioms` confirms the
footprint matches the module's declared allowlist. Gate 2 proves that on every run.

None of that establishes that the theorem *says what anyone meant*. A statement can compile, be
non-vacuous, carry witnesses in both polarities, and still be the wrong statement — about a
degenerate case, with a quantifier in the wrong order, or named after a theorem it does not
contain. Three of the entries below exist because that happened here:

- `MX-A-0012` was proposed with a theorem named for **Donoho–Stark** whose entire Fourier content
  was its own hypothesis (LL-17).
- The same file named another theorem for **Kramers–Wannier** while containing no Ising model.
- The foundations paper asserted something **false** about the central theorem for a week, in
  seven files, because prose is not gated (LL-16).

The kernel caught none of those. This is the step that does.

**What "audited" means:** you have read the statement, and you assert that it is the claim you
would defend if someone cited it. Not that the proof is correct — Lean has that covered.

**What it costs to skip:** by this repository's own rule, a row is Tier A when the kernel accepts
it and **citable** only after this sign-off. At present **no Tier A row is citable.**

### How to record sign-off

```bash
# all of them
python3 scripts/audit_signoff.py --all --by "Xavier Callens, 2026-08-14"

# or selectively
python3 scripts/audit_signoff.py MX-A-0001 MX-A-0003 --by "Xavier Callens, 2026-08-14"

./scripts/verify.sh      # Gate 4 must still pass afterwards
```

Rows you are *not* satisfied with: leave unsigned and say so. An unsigned row is the system
working, not a failure.

---

## Group 1 — the tier calculus itself (`TierCalculus.lean`)

This is the only group whose subject matter *is* Stream 0. Everything else is an application.
Footprint: `[]` — no axioms at all, not even `propext`, for the theory declarations.

### `MX-A-0001` — the tier order is a total order with `A` on top

> `X < C < L < B < A`, ranked `0..4`. `s ≤ A` for every `s`; `X ≤ s` for every `s`;
> `A ≤ s → s = A`; antisymmetry.

**Does not say:** that these five tiers are the right five, or that "Literature" belongs
between "Conjecture" and "Checkable". That ordering is a *convention* this project adopted —
it is the claim that a peer-reviewed result is stronger evidence than an argument and weaker
than an exact finite computation. **This is the most contestable thing in the repository and
the kernel has nothing to say about it.** If you disagree with the ordering, nothing downstream
survives, so it is worth a minute here.

### `MX-A-0002` — dependency is transitive

> `Depends L a b → Depends L b c → Depends L a c`.

**Does not say:** anything about cycles. A ledger with `a → b → a` is transitively closed and
this theorem is silent on it. Cycle rejection lives in the *checkers* (Gate 3), not here.

### `MX-A-0003` — soundness propagates through the transitive closure

> If `Sound L` and `Depends L a b`, then `tier(a) ≤ tier(b)`.

The core theorem. Soundness is defined only on **direct** edges; this says checking every direct
edge is enough to constrain the whole reachable set.

**Does not say:** that a checker validating direct edges will *report* the right thing. It won't —
that is the point of LL-16. Given `B → B → L`, a per-row check flags the **middle** row and says
nothing about the **head**, and the head is the one people cite. The theorem tells you the head
is contaminated; the report has to be written to say so.

### `MX-A-0004` — a Tier A claim cannot rest on anything weaker

> In a `Sound` ledger the entire transitive support set of a Tier A row is Tier A.

**Does not say:** that this is achievable in practice. It is the constraint that forces the
"take the literature result as an explicit hypothesis parameter" pattern. Read together with
`MX-A-0013`: Donoho–Stark is Tier A here *because it was proved*, not because a paper was cited.

---

## Group 2 — the T-dual radius (`Scale/Reff.lean`)

### `MX-A-0005` — `Reff(α,R) = max(R, α/R)` and its minimum

> Positive; `≥ √α`; equal to `α/R` below `√α` and to `R` above; invariant under `R ↦ α/R`;
> strictly `> √α` off the self-dual radius; `= √α` **iff** `R² = α`.

**Does not say:** anything about string theory, T-duality as a physical symmetry, or a minimum
length in nature. `α` and `R` are real numbers. The physics reading is Stream 5's and it is not
Tier A anywhere.

**Worth your attention:** every theorem carries `0 < R`, and `Reff_pos` deliberately ignores
`α`'s positivity (`_hα`). Check you are happy that the hypothesis set is the honest one and not
tuned to make proofs go through.

**Also:** this bound is now proved **twice** — here, and as a one-line instance of `MX-A-0012`.
That duplication is a recorded decision (`MX-C-0011`), not an oversight.

---

## Group 3 — the five worked use cases

These exist to exercise the pipeline on problems whose answers are already known. Their value is
methodological; none is a research result.

| Row | Says | Does **not** say |
|---|---|---|
| `MX-A-0006` | `1+3+…+(2n−1) = n²`, Mathlib-free | — (nothing to mistake here; it is the control) |
| `MX-A-0007` | The 1-D elastic collision formulae conserve momentum **and** kinetic energy over ℚ, for `m₁+m₂ ≠ 0` | That collisions in the world are elastic. The formulae are *given*; this checks they have the stated invariants |
| `MX-A-0008` | Hardy–Weinberg: frequencies sum to 1, allele frequency invariant, equilibrium in **one** generation | Anything about any population. No selection, drift, migration or mutation — it is a theorem about the model, and the model is known to be false of real populations |
| `MX-A-0009` | Kepler III, `ω²r³ = GM`, for circular orbits under an inverse-square force | That the force law holds. It is a **hypothesis parameter**. Also: circular orbits only — nothing here covers ellipses |
| `MX-A-0010` | The substituted Lotka–Volterra `dV/dt` expression is identically zero | That it *is* `dV/dt`. No calculus. That gap was open for a day and closed by `MX-A-0011` |
| `MX-A-0011` | `V` is genuinely conserved along the flow, over ℝ, via `HasDerivAt` | That predator–prey systems behave this way. The two equations are hypothesis parameters |

**The one to look at hardest is `MX-A-0009`.** The statement uses the *reduced* period `τ = T/2π`
so that π leaves the statement and it becomes exactly rational. That was done to satisfy the
float ban. Confirm you regard the reduced-period form as **the same law** and not a weakened
one — this is exactly the "never weaken a statement to close a proof" boundary (E-4), and I
judged it a reformulation rather than a weakening. That judgement is yours to ratify.

---

## Group 4 — the self-dual bound (`Duality/SelfDual.lean`)

### `MX-A-0012` — one theorem, several instances

> `C ≤ x·y → √C ≤ max x y` (for `0 ≤ x, y`), plus the dual, the sandwich, AM–GM, and
> `x = C/x ↔ x = √C`. Instances: `Reff ≥ √α`; the ℕ cast; the Wilson EOQ bound **with
> attainment** at `Q* = √(2DK/h)`; and `sinh(2K)² = 1 ∧ K > 0 → K = log(1+√2)/2`.

**Does not say** — and this is the row where the naming matters most:

- `sqrt_le_max_of_le_mul_nat` is **not** Donoho–Stark. It is arithmetic. (The Fourier statement
  was later proved separately — `MX-A-0014` — but this theorem still is not it.)
- `sinh_selfDual_coupling` contains **no Ising model**. The value it returns is Onsager's
  critical coupling, but "self-duality locates the critical point" needs the transition to be
  *unique*, which is not in the file. Filed apart as `MX-C-0009`.

**Worth your attention:** the claim that `Reff` and the 1913 EOQ lot size are *the same lemma* is
the substantive content here. It is a claim about the reach of the notation. Decide whether you
regard that as a result or as a coincidence of algebra — I think it is real, but it is the kind
of claim that flatters itself.

---

## Group 5 — the uncertainty principle (`Duality/Uncertainty.lean`)

### `MX-A-0013` — Parseval on `ZMod N`

> `∑ₖ 𝓕f(k)·conj 𝓕f(k) = N · ∑ⱼ f(j)·conj f(j)`, and the real-norm form.

**The one factual claim here you should spot-check:** that Mathlib does not already have this.
I verified `Mathlib/Analysis/Fourier/ZMod.lean` contains no norm or inner-product lemma, and that
Mathlib's Parseval results are for `AddCircle` and the continuous transform. If that is wrong,
this row is a wrapper and should be demoted in significance (though not in tier).

**Does not say:** anything about a normalised transform. The factor `N` is `ZMod.dft`'s
convention.

### `MX-A-0014` — Donoho–Stark

> For `f ≠ 0` on `ZMod N`: `N ≤ |supp f| · |supp 𝓕f|`. Corollary: the larger support is `≥ √N`.

**Does not say:** anything about quantum mechanics, the Heisenberg principle, or measurement.
The shared word "uncertainty" is an analogy between two inequalities. **If this row is ever cited
in a physics context, that is the failure mode**, and the file says so in its header.

**Worth your attention:** the corollary is the first time the abstract bound of `MX-A-0012` has
been applied to a product hypothesis that is *proved* rather than assumed. That is the intended
payoff of the whole exercise, so it is worth confirming you read it the same way.

---

## Group 6 — phase winding (`Applications/Winding.lean`)

### `MX-A-0015` — winding is quantized

> For nonvanishing `ψ` on `ZMod L`: `∑ₖ arg(ψ(k+1)/ψ(k)) = 2π·n`, `n ∈ ℤ`.

**Does not say:** anything about superfluids, circulation, `h/m`, or vortices. There is no fluid
in the file. The file is named `Winding` and not `Circulation` **on purpose**.

**Worth your attention, because this is the one staged for another stream:** the two witnesses
differ in exactly one amplitude — `full4` winds by 1, and zeroing a single site gives a total of
`π`, which is not a multiple of `2π`. Under the intended physical reading the vanishing site is a
vortex core, and the second witness is the statement that a core has finite size. **That reading
is Tier C and is not part of this row.** If you sign this row you are signing the mathematics
only. Confirm you are content that the split is drawn in the right place, because the whole
QuantumFluids plan rests on it being drawn honestly.

---

## Summary sheet

| Row | Subject | The trap |
|---|---|---|
| `MX-A-0001` | tier order | **the ordering is a convention, not a theorem** |
| `MX-A-0002` | transitivity | silent on cycles |
| `MX-A-0003` | soundness propagates | the *report*, not the theorem, must name the head |
| `MX-A-0004` | A rests only on A | forces the hypothesis-parameter pattern |
| `MX-A-0005` | `Reff` | no physics; proved twice by decision |
| `MX-A-0006` | odd sums | none — the control |
| `MX-A-0007` | elastic collision | formulae given, not derived |
| `MX-A-0008` | Hardy–Weinberg | about the model, which is false of real populations |
| `MX-A-0009` | Kepler III | **reduced period — reformulation or weakening?** |
| `MX-A-0010` | LV algebraic core | not `dV/dt` |
| `MX-A-0011` | LV along the flow | equations are hypotheses |
| `MX-A-0012` | self-dual bound | **two theorems named after theorems they do not contain** |
| `MX-A-0013` | Parseval | check the "Mathlib lacks it" claim |
| `MX-A-0014` | Donoho–Stark | **not quantum mechanics** |
| `MX-A-0015` | winding | **not circulation; the physics is Tier C** |

Bolded rows are where I would spend the time if you only have twenty minutes.
