#!/usr/bin/env python3
"""Tier B harness — UC6: the refutation case.

WHY THIS EXISTS
---------------
The campaign could produce a proof (UC1-UC4), and a deferral that was later
closed (UC5). It had never produced a **rejection**. By this repository's own
standard — `docs/CLAUDE5_LOOP.md` §4, "a loop that cannot report a negative
result is not an instrument" — that made the loop untested in the one direction
that matters most, because a pipeline optimising for green checkmarks fails
silently and a pipeline that can say *no* does not.

So this harness proposes four conservation laws and tries to break them. Three
are false and must be refuted with an explicit exact counterexample. One is true
and must **survive** — because a refuter that refutes everything is exactly as
useless as one that refutes nothing (HARDNESS.md H2).

WHY THESE THREE
---------------
Not strawmen. Each is the shape of error a competent person actually makes:
a true statement with one quantifier or one scope slipped.

  R1  "each body's kinetic energy is individually conserved in an elastic
      collision" — energy IS conserved; the error is dropping the sum.
  R2  "Lotka-Volterra conserves total population x + y" — the system HAS a
      conserved quantity; the error is guessing the obvious one instead of
      δx − γ ln x + βy − α ln y.
  R3  "Reff is multiplicative in R" — max distributes over many things; the
      error is assuming it distributes over this.

A refutation is a POSITIVE result. It is filed at Tier B like any other
exact-arithmetic finding, and the counterexamples are the evidence.
"""

from __future__ import annotations

from fractions import Fraction as F

FAILURES: list[str] = []
REFUTED: list[tuple[str, str]] = []


# ---------------------------------------------------------------------------
# The systems under test (shared with tests/tier_b_applications.py by design:
# a refutation is only interesting against the same definitions the proofs use)
# ---------------------------------------------------------------------------


def collide(m1: F, m2: F, u1: F, u2: F) -> tuple[F, F]:
    total = m1 + m2
    return (
        ((m1 - m2) * u1 + 2 * m2 * u2) / total,
        ((m2 - m1) * u2 + 2 * m1 * u1) / total,
    )


def lv_rates(a: F, b: F, g: F, d: F, x: F, y: F) -> tuple[F, F]:
    return a * x - b * x * y, d * x * y - g * y


def reff(alpha: F, r: F) -> F:
    return max(r, alpha / r)


# ---------------------------------------------------------------------------
# R1 — "each body's kinetic energy is individually conserved"
# ---------------------------------------------------------------------------


def refute_individual_ke() -> tuple[bool, str]:
    """FALSE. Only the SUM is conserved; the collision transfers energy."""
    m1, m2, u1, u2 = F(1), F(3), F(4), F(0)
    v1, v2 = collide(m1, m2, u1, u2)
    before1, after1 = m1 * u1**2, m1 * v1**2
    total_ok = m1 * v1**2 + m2 * v2**2 == m1 * u1**2 + m2 * u2**2
    if before1 == after1:
        return False, "no counterexample found at the chosen parameters"
    return True, (
        f"m=({m1},{m2}) u=({u1},{u2}) -> v=({v1},{v2}); "
        f"body 1 KE {before1} -> {after1}. "
        f"Total KE conserved: {total_ok}. The sum is conserved; the parts are not."
    )


# ---------------------------------------------------------------------------
# R2 — "Lotka-Volterra conserves total population x + y"
# ---------------------------------------------------------------------------


def refute_total_population() -> tuple[bool, str]:
    """FALSE. d(x+y)/dt = (αx − βxy) + (δxy − γy), which is not identically 0."""
    a, b, g, d, x, y = F(2), F(1), F(1), F(1), F(3), F(1)
    dx, dy = lv_rates(a, b, g, d, x, y)
    if dx + dy == 0:
        return False, "no counterexample found at the chosen parameters"
    return True, (
        f"α,β,γ,δ=({a},{b},{g},{d}) at (x,y)=({x},{y}): "
        f"dx/dt={dx}, dy/dt={dy}, d(x+y)/dt={dx + dy} ≠ 0. "
        "The system does have a conserved quantity (MX-A-0011) — just not this one."
    )


# ---------------------------------------------------------------------------
# R3 — "Reff is multiplicative in R"
# ---------------------------------------------------------------------------


def refute_reff_multiplicative() -> tuple[bool, str]:
    """FALSE. Reff(α, R₁R₂) ≠ Reff(α,R₁)·Reff(α,R₂) in general."""
    alpha, r1, r2 = F(4), F(1), F(4)
    lhs = reff(alpha, r1 * r2)
    rhs = reff(alpha, r1) * reff(alpha, r2)
    if lhs == rhs:
        return False, "no counterexample found at the chosen parameters"
    return True, (
        f"α={alpha}: Reff({alpha},{r1 * r2})={lhs} but "
        f"Reff({alpha},{r1})·Reff({alpha},{r2})={reff(alpha, r1)}·{reff(alpha, r2)}={rhs}. "
        "The bounce below √α is exactly what breaks multiplicativity."
    )


# ---------------------------------------------------------------------------
# R4 — THE ONE THAT MUST SURVIVE
# ---------------------------------------------------------------------------


def refute_relative_speed() -> tuple[bool, str]:
    """TRUE, and must NOT be refuted.

    In a 1-D elastic collision the relative speed is preserved (the relative
    velocity reverses): |u₁ − u₂| = |v₂ − v₁|.

    This is the control. It is deliberately of the same *kind* as the three
    false claims — a one-line statement about a conserved quantity in the same
    systems — so that a refuter which simply reports "refuted" for anything it
    is handed is caught here rather than trusted.
    """
    for m1 in [F(1), F(2), F(5), F(1, 3)]:
        for m2 in [F(1), F(3), F(7, 2)]:
            for u1 in [F(0), F(4), F(-2), F(5, 3)]:
                for u2 in [F(0), F(-1), F(3), F(-7, 4)]:
                    v1, v2 = collide(m1, m2, u1, u2)
                    if abs(u1 - u2) != abs(v2 - v1):
                        return True, (
                            f"UNEXPECTED counterexample at m=({m1},{m2}) u=({u1},{u2})"
                        )
    return False, "survived 192 exact cases — relative speed is preserved"


# ---------------------------------------------------------------------------

PROPOSALS = [
    ("R1 each body's KE is individually conserved", refute_individual_ke, True),
    ("R2 Lotka-Volterra conserves x + y", refute_total_population, True),
    ("R3 Reff is multiplicative in R", refute_reff_multiplicative, True),
    ("R4 elastic collision preserves relative speed", refute_relative_speed, False),
]


def main() -> int:
    for label, probe, should_refute in PROPOSALS:
        refuted, detail = probe()
        if refuted and not should_refute:
            FAILURES.append(
                f"OVER-REFUTATION: {label} is TRUE but was refuted — {detail}"
            )
        elif not refuted and should_refute:
            FAILURES.append(
                f"MISSED REFUTATION: {label} is FALSE but survived — {detail}"
            )
        else:
            REFUTED.append((label, detail))

    if FAILURES:
        print(f"FAIL  tier_b_refutations  ({len(FAILURES)} failure(s))")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    refuted_n = sum(1 for _, _, s in PROPOSALS if s)
    print(
        f"PASS  tier_b_refutations  ({refuted_n} proposal(s) refuted, "
        f"1 true claim survived)"
    )
    for label, detail in REFUTED:
        verdict = "REFUTED " if label.startswith(("R1", "R2", "R3")) else "SURVIVED"
        print(f"  {verdict} {label}")
        print(f"           {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
