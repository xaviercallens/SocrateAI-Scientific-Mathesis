#!/usr/bin/env python3
"""Tier B harness — phase winding around a discrete loop (companion to MX-A-0015).

WHY THIS EXISTS
---------------
`lean/Mathesis/Applications/Winding.lean` proves that the principal phase
increments around a nonvanishing cyclic loop sum to `2π` times an integer. That
theorem is about `Complex.arg`, which is transcendental and cannot be evaluated
in exact arithmetic — so a naive harness would have to use floats, and floats are
banned (SPEC.md §4, HARDNESS.md H3).

THE REFORMULATION THE BAN FORCES, AGAIN BETTER THAN THE ORIGINAL
-----------------------------------------------------------------
The winding number does not need angles at all. Partition the nonzero Gaussian
rationals into four quadrants by the **signs** of the real and imaginary parts,
and track quadrant transitions:

    q(z) = 0 if re>0, im>=0     1 if re<=0, im>0
           2 if re<0, im<=0     3 if re>=0, im<0

Each step contributes `(q(w) − q(z)) mod 4`, mapped into `{−1, 0, +1}` — with the
half-turn value `2` **rejected**, because a step that jumps by half a turn has
genuinely ambiguous direction and no algorithm can resolve it. The winding number
is the total divided by 4.

Everything here is integer arithmetic on exact `Fraction` coordinates. There is
no angle, no π, and no rounding. And the theorem's content becomes a divisibility
statement: **the total must be divisible by 4.** That is the quantization,
stated in a form a machine can decide.

The rejection of half-turn steps is not a dodge. It is the discrete analogue of
the sampling condition every real winding-number computation needs, and making it
an explicit precondition — checked, with a negative control — is better than
leaving it implicit.
"""

from __future__ import annotations

from fractions import Fraction as F

FAILURES: list[str] = []
CHECKS: list[str] = []

Point = tuple[F, F]  # (re, im)


class AmbiguousStep(Exception):
    """A step of half a turn: direction is genuinely undetermined."""


class VanishingSite(Exception):
    """The order parameter is zero somewhere on the loop — winding undefined."""


def quadrant(z: Point) -> int:
    re, im = z
    if re == 0 and im == 0:
        raise VanishingSite(f"zero at {z}")
    if re > 0 and im >= 0:
        return 0
    if re <= 0 and im > 0:
        return 1
    if re < 0 and im <= 0:
        return 2
    return 3


def quarter_turns(loop: list[Point]) -> int:
    """Total quarter-turns around the closed loop. Exact integer arithmetic."""
    total = 0
    n = len(loop)
    for k in range(n):
        z, w = loop[k], loop[(k + 1) % n]
        dq = (quadrant(w) - quadrant(z)) % 4
        if dq == 2:
            raise AmbiguousStep(f"half-turn step {z} -> {w}")
        total += dq if dq != 3 else -1
    return total


def winding(loop: list[Point]) -> int:
    total = quarter_turns(loop)
    if total % 4 != 0:
        raise AssertionError(f"total {total} not divisible by 4")
    return total // 4


# ---------------------------------------------------------------------------
# The loops
# ---------------------------------------------------------------------------

UNIT4: list[Point] = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
HOLE4: list[Point] = [(F(1), F(0)), (F(0), F(1)), (F(0), F(0)), (F(0), F(-1))]

# a coarser but still unambiguous octagon, with rational (not unit-modulus) sites
OCT8: list[Point] = [
    (F(1), F(0)), (F(2, 3), F(2, 3)), (F(0), F(1)), (F(-2, 3), F(2, 3)),
    (F(-1), F(0)), (F(-2, 3), F(-2, 3)), (F(0), F(-1)), (F(2, 3), F(-2, 3)),
]

GRID = [F(-3), F(-2), F(-1), F(-1, 2), F(1, 2), F(1), F(2), F(3)]


def rotate(loop: list[Point], k: int) -> list[Point]:
    return loop[k:] + loop[:k]


# ---------------------------------------------------------------------------
# B1 — quantization: the total is always divisible by 4
# ---------------------------------------------------------------------------


def check_quantization() -> None:
    """Every admissible loop has quarter-turn total divisible by 4.

    This is the exact-arithmetic form of `winding_is_integer`.
    """
    n, skipped = 0, 0
    base = [UNIT4, OCT8, list(reversed(UNIT4)), UNIT4 + UNIT4, OCT8 + OCT8]
    loops = [rotate(b, k) for b in base for k in range(len(b))]
    # plus loops built from the rational grid, keeping only admissible ones
    for a in GRID:
        for b in GRID:
            loops.append([(F(1), F(0)), (a, F(1)), (F(-1), F(0)), (b, F(-1))])
    for loop in loops:
        try:
            total = quarter_turns(loop)
        except (AmbiguousStep, VanishingSite):
            skipped += 1
            continue
        n += 1
        if total % 4 != 0:
            FAILURES.append(
                f"B1 NOT QUANTIZED: loop {loop} has quarter-turn total {total}, "
                f"which is not divisible by 4"
            )
    if n == 0:
        FAILURES.append("B1 VACUOUS: every loop was skipped; nothing was checked")
    CHECKS.append(f"B1 quantization: {n} admissible loops, {skipped} inadmissible")


def check_known_windings() -> None:
    """The witnessed values, matching the Lean witnesses exactly.

    `UNIT4` is `full4` from `Winding.lean` and must give winding 1 — the same
    number the kernel proves there (`witness_winding_one`, total `2π`).
    """
    cases = [
        ("UNIT4 (= Lean full4)", UNIT4, 1),
        ("UNIT4 reversed", list(reversed(UNIT4)), -1),
        ("UNIT4 traversed twice", UNIT4 + UNIT4, 2),
        ("OCT8", OCT8, 1),
        ("constant-quadrant loop", [(F(1), F(0)), (F(2), F(1)), (F(3), F(2))], 0),
    ]
    for label, loop, expected in cases:
        got = winding(loop)
        if got != expected:
            FAILURES.append(f"B2 {label}: winding {got}, expected {expected}")
    CHECKS.append(f"B2 known windings: {len(cases)} loops, all as expected")


def check_rotation_invariance() -> None:
    """Winding does not depend on where the loop starts."""
    n = 0
    for loop in (UNIT4, OCT8, list(reversed(UNIT4))):
        base = winding(loop)
        for k in range(len(loop)):
            n += 1
            got = winding(rotate(loop, k))
            if got != base:
                FAILURES.append(
                    f"B3 rotation changed winding: {loop} start {k} gave {got}, "
                    f"expected {base}"
                )
    CHECKS.append(f"B3 rotation invariance: {n} rotations")


def check_additivity() -> None:
    """Traversing a loop m times multiplies the winding by m."""
    n = 0
    for loop, base in ((UNIT4, 1), (OCT8, 1), (list(reversed(UNIT4)), -1)):
        for m in (1, 2, 3, 4):
            n += 1
            got = winding(loop * m)
            if got != base * m:
                FAILURES.append(
                    f"B4 additivity: {m} traversals gave {got}, expected {base * m}"
                )
    CHECKS.append(f"B4 additivity under repeated traversal: {n} cases")


# ---------------------------------------------------------------------------
# NEGATIVE CONTROLS — each must FAIL, or the harness certifies nothing
# ---------------------------------------------------------------------------


def control_vanishing_site_rejected() -> bool:
    """HOLE4 has a zero: winding must be refused, not silently computed.

    This is the harness twin of the Lean witness `witness_needs_nonvanishing`.
    """
    try:
        quarter_turns(HOLE4)
    except VanishingSite:
        return True
    return False


def control_half_turn_rejected() -> bool:
    """A loop stepping directly across the origin is ambiguous and refused."""
    loop = [(F(1), F(0)), (F(-1), F(0)), (F(1), F(1)), (F(-1), F(1))]
    try:
        quarter_turns(loop)
    except AmbiguousStep:
        return True
    return False


def control_open_path_not_quantized() -> bool:
    """Drop the closing step and quantization fails.

    This is the sharpest control here: it shows the divisibility-by-4 is NOT an
    artifact of the encoding but comes from the loop actually closing — which is
    exactly `prod_ratio_eq_one` in the Lean proof.
    """
    total = 0
    path = UNIT4
    for k in range(len(path) - 1):  # NB: no wraparound
        dq = (quadrant(path[k + 1]) - quadrant(path[k])) % 4
        total += dq if dq != 3 else -1
    return total % 4 != 0


def control_wrong_winding_detected() -> bool:
    """Claiming UNIT4 has winding 2 is false."""
    return winding(UNIT4) != 2


def control_reversal_changes_sign() -> bool:
    """A reversed loop has the opposite winding, not the same one."""
    return winding(list(reversed(UNIT4))) == -winding(UNIT4) != 0


CONTROLS = [
    ("a vanishing site is refused, not computed", control_vanishing_site_rejected),
    ("a half-turn step is refused as ambiguous", control_half_turn_rejected),
    ("an OPEN path is not quantized — closure is what forces it",
     control_open_path_not_quantized),
    ("UNIT4 does not have winding 2", control_wrong_winding_detected),
    ("reversal flips the sign", control_reversal_changes_sign),
]


def main() -> int:
    check_quantization()
    check_known_windings()
    check_rotation_invariance()
    check_additivity()

    fired = []
    for label, control in CONTROLS:
        if not control():
            FAILURES.append(
                f"NEGATIVE CONTROL DID NOT FIRE: {label} — a control that cannot "
                "detect its defect proves nothing (HARDNESS.md H2)"
            )
        else:
            fired.append(label)

    if FAILURES:
        print(f"FAIL  tier_b_winding  ({len(FAILURES)} failure(s))")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    print(f"PASS  tier_b_winding  ({len(CHECKS)} check(s), {len(fired)} negative controls)")
    for check in CHECKS:
        print(f"  {check}")
    for label in fired:
        print(f"  control fired: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
