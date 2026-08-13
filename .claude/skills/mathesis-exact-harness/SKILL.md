---
name: mathesis-exact-harness
description: Write a Tier B exact-arithmetic verification harness with a negative control, for any SocrateAI stream. Use when asked to check, verify, validate, or test a mathematical identity, bound, count, or numerical claim; when writing anything under tests/; or when a result needs to be established computationally rather than by proof.
---

# Exact-arithmetic harness (Tier B)

A Tier B harness is a program that **decides a finite statement exactly** and **can be shown to
fail**. Both halves are required.

## Exact arithmetic only

`fractions.Fraction` and `int`. No floats, anywhere in the harness, ever.

```python
from fractions import Fraction
x = Fraction(1, 3)          # yes
x = 1/3                     # no — this is a Tier X approximation wearing a Tier B badge
```

Floats belong in `exploration/`, under a `# TIER X — EXPLORATORY, NO CLAIMS` banner. They may
*steer* decisions — locate the interesting regime, then certify it exactly. They may never
support a ledger row above Tier X.

Enforce with an AST walk, not grep: `x = 1.5` is a violation, `"version 1.5"` and
`# 1.5x faster` are not. A grep-based rule produces false positives, gets disabled, and stops
protecting anything.

## The negative control is the point

Every harness ships a control that is **demonstrated to fail**, and the gate fails if the
control *passes*.

The control that matters is not the one showing the harness rejects garbage. It is the one
showing it rejects the **plausible near-miss** — the input a subtly wrong implementation would
accept.

```python
def control_transitivity_is_load_bearing() -> bool:
    """A direct-only check would pass this; ours must not."""
    leak = build([("A", B, ["B"]), ("B", B, ["C"]), ("C", C, [])])
    direct_only = any(head.tier > s.tier for s in head.supports)   # a naive check sees nothing
    return (not direct_only) and "E-UNSOUND" in codes(check(leak))
```

Ship the mirror image too: a control confirming the harness **accepts a correct input**. A
checker that fails everything is as useless as one that fails nothing.

## Structure

```python
FAILURES: list[str] = []

def expect(condition: bool, label: str) -> None:
    if not condition:
        FAILURES.append(label)

def main() -> int:
    b1_...(); b2_...()                       # the checks
    for label, control in CONTROLS:          # then the controls
        if not control():
            FAILURES.append(f"NEGATIVE CONTROL DID NOT FIRE: {label}")
    if FAILURES:
        print(f"FAIL  {NAME}  ({len(FAILURES)} failure(s))")
        for f in FAILURES: print(f"  - {f}")
        return 1
    print(f"PASS  {NAME}  (B1-B4, {len(CONTROLS)} negative controls)")
    return 0
```

Collect all failures and report them together. Failing on the first one hides the other four
and turns one debugging session into five.

## Determinism

No wall-clock. No unseeded randomness. No network. Enumerate small cases by hand rather than
sampling — exhaustive over five elements beats random over five hundred, and a failure names a
specific reproducible input instead of a seed.

Every dataset ships its generating command and `sha256sum` in a sidecar.

## Refute before you prove

Before formalizing anything, run the falsification sweep: perturb the identity, feed degenerate
and boundary inputs, and confirm the checker rejects them.

This has caught real errors. Stream 1 found a convolution formula, sourced from a web search,
that was **identically zero** — surfaced in seconds by an exact check at small parameters, and
invisible to any amount of proof effort, because the statement was perfectly provable and
perfectly useless.

## Wire it in immediately

Add the harness to `scripts/verify.sh` in the **same commit**. An unwired harness never runs
and nothing reports that it never runs — a passing suite that silently excludes a file is worse
than a missing test, because it is counted (`LL.md` LL-8).

## Checklist

- [ ] `Fraction`/`int` only; no float literal, no `float()` call
- [ ] Deterministic: no clock, no unseeded randomness, no network
- [ ] Negative control present, and **demonstrated to fail** when the check is broken
- [ ] Control targets the plausible near-miss, not just obvious garbage
- [ ] Positive control: a correct input is accepted
- [ ] All failures collected and reported together
- [ ] Wired into the gate, same commit
- [ ] Ledger rows added to `LEDGER.md` **and** `ledger.jsonl`
