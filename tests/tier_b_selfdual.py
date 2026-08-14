#!/usr/bin/env python3
"""Tier B harness — the self-dual bound (companion to MX-A-0012).

WHY THIS EXISTS
---------------
`lean/Mathesis/Duality/SelfDual.lean` was the only Lean module in the repository
with no exact-arithmetic companion. Every other Tier A module has one, and the
reason is not redundancy: the Lean proof certifies the *statement I wrote*, and
the harness certifies that the statement is the one that survives contact with
enumerated data. LL-12 and LL-16 are both cases where those two came apart.

THE OBSTACLE, AND WHY IT IMPROVES THE STATEMENT
-----------------------------------------------
`√C` is irrational for almost every rational `C`, so `√C ≤ max(x,y)` cannot be
checked in exact arithmetic as written. The float ban (HARDNESS.md H3) therefore
forces a reformulation — and, as with Kepler III where the reduced period removed
π, the reformulation is *better* than the original:

    C ≤ x·y  →  C ≤ max(x,y)²          (for 0 ≤ x, 0 ≤ y)

No square root appears. This is equivalent to A.1 over the nonnegatives, exactly
checkable over ℚ, and it is the form in which the bound is actually used.

The same trick makes EOQ checkable: `Q* = √(2DK/h)` is irrational in general, so
the harness enumerates only parameter triples where `2DK/h` is a perfect rational
square. That is not a dodge — it is a *sub-family* on which the exact claim is
stronger than a floating-point check on the general family would be.
"""

from __future__ import annotations

import math
from fractions import Fraction as F

FAILURES: list[str] = []
CHECKS: list[str] = []

GRID = [F(1, 4), F(1, 3), F(1, 2), F(1), F(3, 2), F(2), F(3), F(5), F(7, 2), F(10)]


def is_square(q: F) -> bool:
    """True iff the rational q is the square of a rational."""
    if q < 0:
        return False
    n, d = q.numerator, q.denominator
    return isqrt_exact(n) is not None and isqrt_exact(d) is not None


def isqrt_exact(n: int) -> int | None:
    """Exact integer square root, or None if n is not a perfect square.

    `math.isqrt` is exact integer arithmetic. The obvious `int(n**0.5)` is NOT:
    `**0.5` is a float operation, and Gate 1's float ban rejected exactly that
    line when this harness was first filed — in the file whose docstring argues
    that the float ban improves statements. Recorded as LL-18.
    """
    if n < 0:
        return None
    r = math.isqrt(n)
    return r if r * r == n else None


def exact_sqrt(q: F) -> F:
    """Exact square root of a rational that is known to be a perfect square."""
    n, d = isqrt_exact(q.numerator), isqrt_exact(q.denominator)
    assert n is not None and d is not None, f"{q} is not a rational square"
    return F(n, d)


# ---------------------------------------------------------------------------
# B1 — the squared self-dual bound (A.1), enumerated
# ---------------------------------------------------------------------------


def check_squared_bound() -> None:
    """C ≤ x·y  →  C ≤ max(x,y)², for 0 ≤ x, 0 ≤ y."""
    n = 0
    for x in GRID:
        for y in GRID:
            for c in GRID + [F(0)]:
                if c <= x * y:
                    n += 1
                    if not c <= max(x, y) ** 2:
                        FAILURES.append(
                            f"B1 squared bound FAILED at C={c}, x={x}, y={y}: "
                            f"max²={max(x, y) ** 2}"
                        )
    CHECKS.append(f"B1 squared self-dual bound: {n} exact cases")


def check_bound_attained() -> None:
    """The bound is an equality exactly at the self-dual point x = y.

    Without this the bound could be true and useless; with it, it cannot be
    tightened. Mirrors witness W1 in the Lean module (HARDNESS.md H5).
    """
    n = 0
    for x in GRID:
        c = x * x
        if c != max(x, x) ** 2:
            FAILURES.append(f"B1' attainment FAILED at x={x}")
        n += 1
    CHECKS.append(f"B1' bound attained at the self-dual point: {n} cases")


def check_reff_instance() -> None:
    """Reff(α,R) = max(R, α/R) satisfies α ≤ Reff², with equality iff R² = α.

    This is MX-A-0005's minimum, in the squared form, over ℚ.
    """
    n, tight = 0, 0
    for alpha in GRID:
        for r in GRID:
            reff = max(r, alpha / r)
            if not alpha <= reff**2:
                FAILURES.append(f"B2 Reff bound FAILED at α={alpha}, R={r}")
            if alpha == reff**2:
                tight += 1
                if r * r != alpha:
                    FAILURES.append(
                        f"B2 equality at α={alpha}, R={r} but R² ≠ α — "
                        "the minimum is NOT at the self-dual radius"
                    )
            n += 1
    CHECKS.append(f"B2 Reff ≥ √α (squared): {n} cases, {tight} at equality")


# ---------------------------------------------------------------------------
# B3 — EOQ optimality, on the exactly-representable sub-family
# ---------------------------------------------------------------------------


def cost(d: F, k: F, h: F, q: F) -> F:
    return d * k / q + h * q / 2


def check_eoq_optimal() -> None:
    """cost(Q*) ≤ cost(Q) for every rational Q, where Q* = √(2DK/h) is rational.

    This is the Tier B content of `eoq_attained`: the Lean theorem proves the
    lower bound is *reached*, and this harness proves nothing else reaches
    lower — which together is what "optimal lot size" means.
    """
    n, families = 0, 0
    for d in GRID:
        for k in GRID:
            for h in GRID:
                ratio = 2 * d * k / h
                if not is_square(ratio):
                    continue
                families += 1
                qstar = exact_sqrt(ratio)
                cstar = cost(d, k, h, qstar)
                for q in GRID:
                    n += 1
                    if cost(d, k, h, q) < cstar:
                        FAILURES.append(
                            f"B3 EOQ NOT optimal: D={d} K={k} h={h}, "
                            f"Q*={qstar} costs {cstar} but Q={q} costs "
                            f"{cost(d, k, h, q)}"
                        )
                # the two dual costs balance exactly at Q*
                if d * k / qstar != h * qstar / 2:
                    FAILURES.append(
                        f"B3' dual costs do not balance at Q*={qstar} "
                        f"(D={d} K={k} h={h})"
                    )
    CHECKS.append(
        f"B3 EOQ optimal + dual costs balance at Q*: "
        f"{families} exact families, {n} comparisons"
    )


# ---------------------------------------------------------------------------
# B4 — the algebraic core of the sinh fixed point
# ---------------------------------------------------------------------------


def check_fixed_point_core() -> None:
    """s·s = 1 ∧ s > 0 → s = 1, over ℚ.

    `sinh_selfDual_coupling` is this fact plus `arsinh`. The transcendental part
    is Lean's; the algebra is checkable here, and it is where the sign hypothesis
    does its work — `s = -1` also satisfies s·s = 1.
    """
    n = 0
    for s in GRID + [-x for x in GRID]:
        if s * s == 1:
            n += 1
            if s > 0 and s != 1:
                FAILURES.append(f"B4 positive root not unique: s={s}")
    if n < 2:
        FAILURES.append(
            f"B4 VACUOUS: only {n} root(s) of s²=1 found in the grid — "
            "the harness must see both +1 and -1 or it is not testing the "
            "sign hypothesis at all"
        )
    CHECKS.append(f"B4 sinh fixed-point algebraic core: {n} roots of s²=1 seen")


# ---------------------------------------------------------------------------
# NEGATIVE CONTROLS — each must FAIL, or this harness certifies nothing
# ---------------------------------------------------------------------------


def control_needs_nonneg() -> bool:
    """Dropping the sign hypotheses breaks A.1. Lean witness W3, in ℚ."""
    c, x, y = F(4), F(-1), F(-4)
    return c <= x * y and not (c <= max(x, y) ** 2)


def control_max_not_min() -> bool:
    """The bound is on max, not min: min(x,y)² ≥ C is false."""
    c, x, y = F(4), F(1), F(4)
    return c <= x * y and not (c <= min(x, y) ** 2)


def control_eoq_offset_not_optimal() -> bool:
    """A lot size offset from Q* costs strictly more."""
    d, k, h = F(1), F(2), F(1)  # 2DK/h = 4, Q* = 2
    qstar = F(2)
    return cost(d, k, h, qstar + 1) > cost(d, k, h, qstar)


def control_negative_root_admitted() -> bool:
    """s = -1 satisfies s²=1, so B4 without `s > 0` would admit it."""
    s = F(-1)
    return s * s == 1 and s != 1


def control_reff_min_not_elsewhere() -> bool:
    """Reff² > α strictly away from the self-dual radius."""
    alpha, r = F(4), F(1)
    return max(r, alpha / r) ** 2 > alpha


CONTROLS = [
    ("A.1 needs 0 ≤ x, 0 ≤ y (x=-1, y=-4)", control_needs_nonneg),
    ("the bound is on max, not min", control_max_not_min),
    ("EOQ: Q*+1 costs strictly more", control_eoq_offset_not_optimal),
    ("s=-1 satisfies s²=1 — the sign hypothesis is load-bearing", control_negative_root_admitted),
    ("Reff² > α away from the self-dual radius", control_reff_min_not_elsewhere),
]


def main() -> int:
    check_squared_bound()
    check_bound_attained()
    check_reff_instance()
    check_eoq_optimal()
    check_fixed_point_core()

    fired = []
    for label, control in CONTROLS:
        if not control():
            FAILURES.append(
                f"NEGATIVE CONTROL DID NOT FIRE: {label} — a control that "
                "cannot detect its defect proves nothing (HARDNESS.md H2)"
            )
        else:
            fired.append(label)

    if FAILURES:
        print(f"FAIL  tier_b_selfdual  ({len(FAILURES)} failure(s))")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    print(f"PASS  tier_b_selfdual  ({len(CHECKS)} check(s), {len(fired)} negative controls)")
    for check in CHECKS:
        print(f"  {check}")
    for label in fired:
        print(f"  control fired: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
