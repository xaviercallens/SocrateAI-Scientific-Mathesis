# APPLICATIONS_FRONTIER.md — where the use-case campaign goes next

Companion to `docs/USECASES.md` (the five that are done) and `FRONTIER.md` (Stream 0 as a
whole). Same structure: TODO, NOTODO, Frontier — the NOTODO list is as normative as the TODO.

**Ladder position.** UC1–UC5 are all *closed-form algebra over ℚ*. Everything below is a step
off that plateau, and each step names the specific capability it needs.

---

## ✅ TODO — ordered by what unblocks what

1. **UC5's analytic bridge — close the OPEN row.** Prove that the cancelled expression *is*
   `dV/dt`, over ℝ, using `Real.log` differentiability and the chain rule. This is the first
   case needing genuine calculus, and it converts `MX-C-0004` from OPEN to Tier A. Everything
   in group 2 below needs the same infrastructure, so this is the unblocking task.
   *Effort: `[top]` to author the statement, `[any]` to execute.*

2. **UC6 — SIR epidemic threshold.** `R₀ = β/γ`, and `dI/dt < 0` at `t = 0` iff `R₀S₀ < 1`.
   Algebraic, so it lands at Tier A now, but it is the first case where the **W** claim has
   policy consequences — which makes the model/world split worth demonstrating where it bites.
   *Blocked on nothing.*

3. **UC7 — Michaelis–Menten under the quasi-steady-state assumption.** The first case where the
   *model itself* is an approximation with a stated validity domain (`[S] ≫ [E]`). The QSSA has
   to enter as a hypothesis with its own witness, and the ledger has to record a Tier A theorem
   about an approximation — a shape none of UC1–UC5 exercises.

4. **A negative use case — one that gets refuted.** Deliberately propose a plausible-but-false
   conservation law and take it through stages 0–1, recording the refutation as the deliverable.
   The campaign currently has a *deferral* (UC5) but no *rejection*, and by
   `docs/CLAUDE5_LOOP.md` §4 a loop that has never produced one has not been tested.
   **Cheapest item here and the most diagnostic.**

5. **Cross-cite between use cases.** No UC currently cites another, so the transitive machinery
   (`MX-A-0003`) is unexercised by the campaign — the very theorem the repository exists for.
   UC4 citing UC2's conservation would do it. Then plant a tier violation and watch Gate 4 catch
   it across the chain.

6. **A `W`-tier row with real data.** Every row so far is **M**. Add one honest **W**: an
   observational claim at Tier L or C, citing its **M** row, so the model/world split appears in
   `ledger.jsonl` and not only in prose.

---

## 🚫 NOTODO — anti-patterns for this campaign specifically

1. **DO NOT add a use case whose Tier A statement needs floats.** If it cannot be stated
   exactly, reformulate it (Kepler's reduced period is the worked example) or file it Tier X in
   `exploration/`. Do not lower the bar to admit a domain.

2. **DO NOT axiomatize an analytic step to reach a Tier A row.** UC5 is the standing precedent:
   the algebra is proved and the bridge is OPEN. An axiom would put the unproven claim into
   every downstream footprint invisibly.

3. **DO NOT restate a missing step as a conditional and call it Tier A.** *"Given `X`, and
   `X → Y`, therefore `Y`"* compiles, carries no axioms, and is a tautology. Stream 1 shipped
   that shape, was audited, and accepted demotion to Tier C. Repeating it here would be the
   clearest evidence that this repository does not read its own ledger.

4. **DO NOT let a use case assert anything about the world.** Every row here is **M**. A **W**
   claim is a separate row at its own tier that cites the **M** row, and it can never be Tier A
   (`MX-A-0004`).

5. **DO NOT guess a non-vacuity witness.** Three were wrong on the first attempt in this
   campaign. Compute them in `Fraction` first — it takes thirty seconds and the kernel is a slow
   way to discover you picked the degenerate case.

6. **DO NOT grow the campaign past the point where every case is read.** Five cases that a human
   has actually audited beat fifty that were generated. The bottleneck is deliberate: the
   statement-adequacy audit does not parallelize (`SPEC.md` §0).

7. **DO NOT let the campaign become the product.** Its purpose is to give the tier calculus real
   consumers and to stress the apparatus. If it stops finding defects in the apparatus, it has
   finished its job and should stop growing.

---

## 🌌 Frontier — unscheduled, not promised

**A use case whose Tier B and Tier A disagree.** Everything so far agrees, which means the
differential relationship between the harness and the kernel is untested where it matters. The
interesting case is one where the enumerated check passes and the proof *fails* — because the
statement quantifies over something the enumeration silently excluded. That failure mode is
the one the campaign cannot currently detect, and finding one deliberately would be worth more
than ten more agreeing cases.

**Tier-parameterized modelling.** A theorem whose *conclusion tier* is computed from its
hypotheses' tiers — so that "Tier A given a Tier L input" is a machine-checked judgement rather
than a convention someone follows. This is the tier calculus turned on the theorem statements
themselves rather than on the ledger rows about them.

**A shared witness library.** Every use case reinvents its non-vacuity witnesses, and three of
them got it wrong. A small library of *computed* witnesses — with the computation attached, so
the witness carries its own evidence — would make step 4 of the loop mechanical.

**Reaching a claim someone would argue about.** The whole ladder points here. UC1–UC5 are
chosen so nobody disputes them; the apparatus is being calibrated, not applied. The campaign
becomes interesting the first time it produces a Tier A row in a domain where a referee would
push back — and the honest measure of readiness is not how many cases pass, but whether the
apparatus has recently caught something the author believed.

By that measure it is working: this campaign found three defects in the gates, two of which
would have stayed invisible. It has not yet found one in the mathematics.
