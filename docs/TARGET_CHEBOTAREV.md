# TARGET — Chebotarëv's theorem on roots of unity, and T-TAO

**Tier of this document:** L for the quoted statements, C for the formalisation plan.
Nothing here is proved in Lean yet. No row may cite it.

---

## Why this document exists before any Lean

`SelfDual.lean` records **T-TAO** — Tao's refinement of Donoho–Stark for prime `N`:

> `|supp f| + |supp f̂| ≥ N + 1`

marked `[LL-6 retrieval pass required]`, because it had been written from memory.

I estimated this target twice from memory and was wrong twice, in the same direction both times.
First I guessed Frenkel's proof used a differential operator and a `p`-adic valuation argument, and
called it multi-session, Mathlib-grade work. **It uses neither.** The retrieval pass is below and
it makes the target materially cheaper than I said. This is the second instance of the same error
in two days (see `MX-C-0011`), so the rule is now explicit: *estimate from the retrieved proof,
never from a remembered one.*

---

## The source, retrieved 2026-08-15 (LL-7: quoted statements, not summaries)

P. E. Frenkel, *Simple proof of Chebotarëv's theorem on roots of unity*,
arXiv:math/0312398v3, 1 Jul 2004. <https://arxiv.org/abs/math/0312398>

Let `p` be a prime and `ω` a primitive `p`-th root of unity; `F_p` is the field with `p` elements.

**Theorem (Chebotarëv, 1926), quoted verbatim:**

> *For any sets `I, J ⊆ F_p` with equal cardinality, the matrix `(ω^{ij})_{i∈I, j∈J}` has non-zero
> determinant.*

**The equivalence that gives T-TAO, quoted verbatim from the paper's introduction:**

> *Tao points out that the theorem is equivalent to the inequality `|supp f| + |supp f̂| ≥ p + 1`
> holding for any function `0 ≢ f : F_p → C` and its Fourier transform `f̂`.*

So **T-TAO is not a separate target.** It is this theorem, restated. The primary reference for the
uncertainty-principle form is T. Tao, *An uncertainty principle for cyclic groups of prime order*,
arXiv:math.CA/0308286.

**Lemma 1, quoted verbatim:**

> *`Z[ω]/(1 − ω) = F_p`.*

**Lemma 2, quoted verbatim:**

> *Let `0 ≢ g(x) ∈ F_p[x]` be a polynomial of degree `< p`. Then the multiplicity of any element
> `0 ≠ a ∈ F_p` as a root of `g(x)` is strictly less than the number of non-zero coefficients of
> `g(x)`.*

**Proof of the theorem, as given in the paper.** The theorem is equivalent to: if `a_j ∈ Q(ω)`
(`j ∈ J`) satisfy `∑_{j∈J} a_j ω^{ij} = 0` for all `i ∈ I`, then all `a_j` are zero. One may assume
`a_j ∈ Z[ω]`. Those equalities say the polynomial `g(x) = ∑_{j∈J} a_j x^j ∈ Z[ω][x]` vanishes at
`ω^i` for every `i ∈ I`, so `g` is divisible by `∏_{i∈I}(x − ω^i)`. Applying the homomorphism
`Z[ω] → Z[ω]/(1−ω) = F_p` to the coefficients gives `ḡ(x) ∈ F_p[x]` divisible by `(x − 1)^{|I|}`.
But `ḡ` has at most `|J|` non-zero coefficients, and `|I| = |J|`, so Lemma 2 forces `ḡ ≡ 0`. Hence
every `a_j` is divisible by `1 − ω`; divide through and iterate. **Infinite descent** unless all
`a_j` are zero.

---

## What this means for cost, honestly

The mathematics is **elementary**. There is no deep number theory in it:

| Step | Nature | Expected difficulty |
|---|---|---|
| Lemma 2 | induction on `deg g`, splitting on `g(0) = 0`, using `g'` | elementary; the fiddly part is "number of non-zero coefficients" as a `Finset.card` and its behaviour under `derivative` |
| Lemma 1 | `Z[Ω]/(Φ_p(Ω)) = Z[ω]` and `Z[Ω]/(1−Ω, p) = F_p`; the second kernel contains the first because `Φ_p(Ω) ≡ p mod (1−Ω)` | Mathlib has cyclotomic polynomials and `IsPrimitiveRoot`; the quotient bookkeeping is the work |
| descent | `a_j ∈ (1−ω)` for all `j`, divide, repeat | needs a well-founded measure — in `Z[ω]`, `(1−ω)` is prime, so valuation strictly decreases |
| T-TAO | restatement of the theorem via the Fourier equivalence | the equivalence is *stated* by Frenkel, not proved there — **it needs its own source (Tao, math.CA/0308286) and its own retrieval pass** |

**Verified prerequisite inventory** (checked in the resolved `LEAN_ENV_DIR`, per `MX-C-0005` — a
missing module and a false statement report identically):

- `Mathlib/NumberTheory/Cyclotomic/` — `Basic`, `PrimitiveRoots`, `Rat`, `Gal`, `Discriminant`
  present; **17 `.olean` built**
- `Mathlib/LinearAlgebra/Vandermonde.lean` — `det_vandermonde`, `det_vandermonde_ne_zero_iff`
- `Mathlib/Analysis/Fourier/ZMod.lean` — `dft` (built); Parseval **not** in Mathlib, but now proved
  in `Duality/Uncertainty.lean` (`MX-A-0013`)
- **Chebotarëv itself: absent.** `grep -rl "Chebotarev" Mathlib/` returns nothing.

## The one caveat that is not about difficulty

The last row of that table is the risk. Frenkel *asserts* the equivalence with Tao's inequality and
attributes it; he does not prove it. So a Lean development that proves Chebotarëv does **not**
thereby give T-TAO — the bridge is a second theorem, from a second paper, and I have not read it.
Filing T-TAO as "follows from Chebotarëv" without that pass would be citing an abstract instead of
a theorem statement, which is exactly `LL-7`.

## Suggested order

1. **Lemma 2 first.** Fully elementary, self-contained, needs nothing from cyclotomic theory, and
   it is the load-bearing combinatorial input. If it goes smoothly the rest is bookkeeping; if it
   does not, the estimate above is wrong again and that is worth learning cheaply.
2. Lemma 1.
3. The descent, hence Chebotarëv.
4. **Separately**: retrieve Tao's paper, quote the equivalence, then T-TAO.
