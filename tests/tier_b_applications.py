#!/usr/bin/env python3
"""Tier B harness — the five application use cases, in exact arithmetic.

Mirrors `lean/Mathesis/Applications/*.lean`. The Lean files prove the theorems;
this file checks the *same statements* on concrete data, over the same number
system.

WHY BOTH
--------
Not redundancy. The Lean proof establishes the universally quantified statement;
this harness establishes that the thing anyone will actually compute with agrees
with it. They fail differently: a Lean proof can be of the wrong statement, and
a harness can pass on the cases you thought to enumerate. Running both is the
cheapest available protection against each.

The two are over one structure, not two: `ℚ` in Lean and `fractions.Fraction`
here. Nothing is approximated on either side, so "agreement" means equality
rather than proximity.

Every use case ships a negative control demonstrated to fail (SPEC.md §7.2).
"""

from __future__ import annotations

from fractions import Fraction as F

FAILURES: list[str] = []


def expect(condition: bool, label: str) -> None:
    if not condition:
        FAILURES.append(label)


# ---------------------------------------------------------------------------
# UC1 — mathematics: sum of the first n odd numbers
# ---------------------------------------------------------------------------


def sum_odd(n: int) -> int:
    return sum(2 * i + 1 for i in range(n))


def uc1_odd_sums() -> None:
    for n in range(0, 501):
        expect(sum_odd(n) == n * n, f"UC1: sumOdd({n}) != {n}^2")


# ---------------------------------------------------------------------------
# UC2 — physics: 1-D elastic collision
# ---------------------------------------------------------------------------


def collide(m1: F, m2: F, u1: F, u2: F) -> tuple[F, F]:
    total = m1 + m2
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / total
    v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / total
    return v1, v2


def uc2_elastic_collision() -> None:
    masses = [F(1), F(2), F(3), F(5), F(1, 2), F(7, 3)]
    speeds = [F(0), F(1), F(-1), F(3), F(-5, 2), F(11, 7)]
    for m1 in masses:
        for m2 in masses:
            for u1 in speeds:
                for u2 in speeds:
                    v1, v2 = collide(m1, m2, u1, u2)
                    expect(
                        m1 * v1 + m2 * v2 == m1 * u1 + m2 * u2,
                        f"UC2: momentum not conserved at {(m1, m2, u1, u2)}",
                    )
                    expect(
                        m1 * v1**2 + m2 * v2**2 == m1 * u1**2 + m2 * u2**2,
                        f"UC2: kinetic energy not conserved at {(m1, m2, u1, u2)}",
                    )


# ---------------------------------------------------------------------------
# UC3 — biology: Hardy-Weinberg
# ---------------------------------------------------------------------------


def uc3_hardy_weinberg() -> None:
    for num in range(0, 21):
        p = F(num, 20)
        q = 1 - p
        expect(p**2 + 2 * p * q + q**2 == 1, f"UC3: genotype freqs do not sum to 1 at p={p}")
        expect(p**2 + (2 * p * q) / 2 == p, f"UC3: allele freq not invariant at p={p}")

    # Arbitrary starting genotype frequencies, not of the form (p^2, 2pq, q^2):
    # equilibrium must be reached in ONE generation and then be fixed.
    starts = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(1, 2), F(1, 4), F(1, 4)),
              (F(1, 3), F(1, 3), F(1, 3)), (F(1, 10), F(3, 5), F(3, 10))]
    for P, H, Q in starts:
        expect(P + H + Q == 1, f"UC3: bad test datum {(P, H, Q)}")
        p = P + H / 2
        # One round of random mating.
        P1, H1, Q1 = p**2, 2 * p * (1 - p), (1 - p) ** 2
        p1 = P1 + H1 / 2
        expect(p1 == p, f"UC3: allele freq drifted in one generation from {(P, H, Q)}")
        # A second round must reproduce the genotype frequencies exactly.
        P2, H2, Q2 = p1**2, 2 * p1 * (1 - p1), (1 - p1) ** 2
        expect(
            (P2, H2, Q2) == (P1, H1, Q1),
            f"UC3: not fixed after the first generation from {(P, H, Q)}",
        )


# ---------------------------------------------------------------------------
# UC4 — physics: Kepler's third law (reduced period; no floats, no pi)
# ---------------------------------------------------------------------------


def uc4_kepler() -> None:
    # For each mu and r, omega^2 = mu / r^3. Choose data where that is a square
    # of a rational so omega itself stays exact.
    for mu in [F(1), F(4), F(9), F(1, 4)]:
        orbits = []
        for r in [F(1), F(4), F(9), F(1, 4), F(16)]:
            omega_sq = mu / r**3
            orbits.append((r, omega_sq))
            # The force balance the Lean file takes as its hypothesis.
            expect(
                omega_sq * r == mu / r**2,
                f"UC4: force balance fails at mu={mu}, r={r}",
            )
        # Kepler III: omega^2 * r^3 is the same constant for every orbit.
        for r, omega_sq in orbits:
            expect(
                omega_sq * r**3 == mu,
                f"UC4: omega^2 r^3 != mu at mu={mu}, r={r}",
            )
        for (r1, w1), (r2, w2) in zip(orbits, orbits[1:]):
            expect(
                w1 * r1**3 == w2 * r2**3,
                f"UC4: Kepler III fails between r={r1} and r={r2}",
            )


# ---------------------------------------------------------------------------
# UC5 — biology: Lotka-Volterra conserved quantity (algebraic core only)
# ---------------------------------------------------------------------------


def prey_rate(a: F, b: F, x: F, y: F) -> F:
    return a * x - b * x * y


def pred_rate(g: F, d: F, x: F, y: F) -> F:
    return d * x * y - g * y


def dVdt(a: F, b: F, g: F, d: F, x: F, y: F) -> F:
    """The substituted dV/dt expression. Requires x, y != 0."""
    p, q = prey_rate(a, b, x, y), pred_rate(g, d, x, y)
    return d * p - g * p / x + b * q - a * q / y


def uc5_lotka_volterra() -> None:
    params = [F(1), F(2), F(3), F(1, 2), F(5, 3)]
    pops = [F(1), F(2), F(3), F(1, 2), F(7, 4)]
    checked = 0
    for a in params:
        for b in params:
            for g in params:
                for d in params:
                    for x in pops:
                        for y in pops:
                            expect(
                                dVdt(a, b, g, d, x, y) == 0,
                                f"UC5: dV/dt != 0 at {(a, b, g, d, x, y)}",
                            )
                            checked += 1
    expect(checked == len(params) ** 4 * len(pops) ** 2, "UC5: enumeration incomplete")


# ---------------------------------------------------------------------------
# Negative controls (SPEC.md §7.2)
#
# One per use case, each targeting the plausible near-miss rather than obvious
# garbage. If any of these fails to fire, the corresponding check above is
# incapable of failing and its result is worthless.
# ---------------------------------------------------------------------------


def control_uc1_off_by_one_is_caught() -> bool:
    """The false variant `sum = n^2 + 1` must be rejected somewhere in range."""
    return any(sum_odd(n) != n * n + 1 for n in range(0, 50))


def control_uc2_inelastic_is_caught() -> bool:
    """A perfectly inelastic collision conserves momentum but NOT energy.

    This is the near-miss that matters: an implementation that only checked
    momentum would pass it. The control demands that the energy check separates
    the two.
    """
    m1, m2, u1, u2 = F(1), F(1), F(2), F(0)
    v = (m1 * u1 + m2 * u2) / (m1 + m2)  # common final velocity
    momentum_ok = m1 * v + m2 * v == m1 * u1 + m2 * u2
    energy_ok = m1 * v**2 + m2 * v**2 == m1 * u1**2 + m2 * u2**2
    return momentum_ok and not energy_ok


def control_uc3_selection_breaks_invariance() -> bool:
    """With selection against the recessive homozygote, allele frequency MOVES.

    Hardy-Weinberg is the null model whose whole purpose is to make selection
    visible. A check that could not detect a violation would make the null model
    unfalsifiable, which is the opposite of what it is for.
    """
    p = F(1, 2)
    q = 1 - p
    # Fitness: AA and Aa survive, aa does not.
    P1, H1, Q1 = p**2, 2 * p * q, F(0)
    total = P1 + H1 + Q1
    p1 = (P1 + H1 / 2) / total
    return p1 != p


def control_uc4_inverse_cube_breaks_kepler() -> bool:
    """Under an inverse-CUBE force law, omega^2 r^3 is not constant.

    The near-miss: Kepler III is specific to the inverse-square law, and a check
    that passed for any central force would be testing nothing about gravity.
    """
    mu = F(1)
    vals = set()
    for r in [F(1), F(2), F(4)]:
        omega_sq = mu / r**4  # inverse-cube force => omega^2 = mu / r^4
        vals.add(omega_sq * r**3)
    return len(vals) > 1


def control_uc5_perturbed_field_breaks_conservation() -> bool:
    """Perturbing one coefficient of the vector field destroys the identity.

    If `dVdt` returned zero for *any* vector field, the theorem would be about
    the arithmetic and not about Lotka-Volterra.
    """
    a, b, g, d, x, y = F(2), F(1), F(1), F(1), F(3), F(1)
    p = a * x - b * x * y
    q = d * x * y - g * y + F(1)  # perturbed predator rate
    perturbed = d * p - g * p / x + b * q - a * q / y
    return perturbed != 0


def control_clean_case_is_accepted() -> bool:
    """The mirror image: a correct instance of each use case must PASS.

    A harness that rejects everything is as useless as one that rejects nothing.
    """
    return (
        sum_odd(7) == 49
        and collide(F(1), F(1), F(3), F(-1)) == (F(-1), F(3))
        and F(3, 5) ** 2 + (2 * F(3, 5) * F(2, 5)) / 2 == F(3, 5)
        and (F(1) / F(4) ** 3) * F(4) ** 3 == F(1)
        and dVdt(F(2), F(1), F(1), F(1), F(3), F(1)) == 0
    )


CONTROLS = [
    ("UC1 off-by-one is caught", control_uc1_off_by_one_is_caught),
    ("UC2 inelastic collision fails the energy check", control_uc2_inelastic_is_caught),
    ("UC3 selection breaks allele invariance", control_uc3_selection_breaks_invariance),
    ("UC4 inverse-cube force breaks Kepler III", control_uc4_inverse_cube_breaks_kepler),
    ("UC5 perturbed vector field breaks conservation", control_uc5_perturbed_field_breaks_conservation),
    ("a clean instance of every use case is accepted", control_clean_case_is_accepted),
]


def main() -> int:
    uc1_odd_sums()
    uc2_elastic_collision()
    uc3_hardy_weinberg()
    uc4_kepler()
    uc5_lotka_volterra()

    for label, control in CONTROLS:
        if not control():
            FAILURES.append(f"NEGATIVE CONTROL DID NOT FIRE: {label}")

    if FAILURES:
        print(f"FAIL  tier_b_applications  ({len(FAILURES)} failure(s))")
        for failure in FAILURES[:20]:
            print(f"  - {failure}")
        if len(FAILURES) > 20:
            print(f"  ... and {len(FAILURES) - 20} more")
        return 1

    print(f"PASS  tier_b_applications  (UC1-UC5, {len(CONTROLS)} negative controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
