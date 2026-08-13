# NOTATION.md — the programme notation standard

**SPEC-STREAM0 §5.** One table, three columns that must never diverge.

**First-use rule (normative):** a symbol may appear in prose only if its row exists here.
No new symbol without a definitional anchor.

LaTeX macros: [`latex/mathesis.sty`](../latex/mathesis.sty). All programme papers import it.

---

## Symbols

| LaTeX | Meaning | Lean identifier |
|---|---|---|
| `\Reff{\alpha'}{R}` | T-dual effective radius, `max(R, α'/R)` | `Mathesis.Scale.Reff` |
| `\seam` | fundamental length `√α'` — "the seam" | — (derived) |
| `\symlock` | symmetric-square lock, `Sym²(L₂) = L₃` | `Mathesis.Sym2.sym2_recurrence` ⚠ *not yet migrated* |
| `\HypU` | Hypothesis U — **quantifier order is normative** | `Mathesis.Statements.HypothesisU` ⚠ *not yet migrated* |
| `\Xcomplex{M}`, `\Xlocked{M}{S}` | interaction complex; locked subcomplex | `Mathesis.Complexes.*` ⚠ *not yet built* |
| `\enstrophy`, `\prodsum{N}` | enstrophy; production sum | `Mathesis.Dyadic.*` ⚠ *not yet migrated* |
| `\disc`, `\cmass` | fiber discriminant; coupling mass `1/|disc|` | `Mathesis.Fiber.*` ⚠ *not yet migrated* |
| `\tier{A}`…`\tier{X}` | epistemic tier tag | `schemas/ledger.schema.json` |
| `\lean{Name}` | the declaration a claim rests on | — |

⚠ marks a row whose Lean identifier is **specified but not yet built**. The row exists so the
notation is fixed before the module lands, not to imply the module exists. See
`docs/designs/RECONCILIATION.md` §5 for what remains.

## Reserved vocabulary

These words carry gate-backed meanings and may not be used loosely:

| Word | Reserved for |
|---|---|
| **theorem** | Tier A only. Anything else is a *claim*, *conjecture*, or *observation* |
| **verified** | a kernel or exact-arithmetic gate accepted it, here, reproducibly |
| **established** | Tier A or Tier L. Never a Tier B instance check |
| **proven** | Tier A. Not "we checked 10 000 cases" |
| **uniform** | never without its quantifier order stated explicitly |

The `mathesis.sty` environments enforce this structurally: `mtheorem` takes a **mandatory**
Lean declaration name, and `mclaim` takes a **mandatory** tier. An untiered claim in a
programme paper is exactly what this package exists to prevent.

## Quantifier order

**Normative:** whenever a uniformity claim is made, state the quantifier order explicitly.

Hypothesis U is `∃C ∀cutoff`, not `∀cutoff ∃C`. The whole content is uniformity in the
cutoff — swapping the quantifiers produces a statement that typechecks in Lean, compiles
without warning, and says far less. No kernel catches that; only a reader who knows what the
physics is asking does.

This is why `\uniformly{α'}` exists as a macro: to make omitting the qualifier take effort.

## Naming rules (L4.5)

- `snake_case` theorems, `UpperCamel` types.
- No abbreviations colliding with Mathlib.
- **No person names in identifiers.** `CallensDualScale.lean` → `Mathesis/Scale/Reff.lean`
  (§9). A library names mathematics, not people.
