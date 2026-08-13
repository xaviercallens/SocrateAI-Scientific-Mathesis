#!/usr/bin/env python3
"""Tier B harness — the tier calculus, checked in exact arithmetic.

Mirrors `lean/Mathesis/TierCalculus.lean`. The Lean file proves the theorem;
this file checks that the *implementation* the other streams will actually call
agrees with it on concrete ledgers, including ones the Lean witnesses do not
cover (cycles, dangling ids, malformed rows).

Per SPEC.md §7.2, every check ships a **negative control** that is demonstrated
to fail. `main` runs the controls too, and the harness exits non-zero if a
control unexpectedly passes — a checker that cannot fail is not a checker.

No floats appear in this file. Tier ranks are `int`; there is no arithmetic
here that could round.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from mathesis.ledger import Claim, Finding, Ledger, check  # noqa: E402
from mathesis.tiers import ClaimIdError, Tier, parse_claim_id  # noqa: E402

FAILURES: list[str] = []


def expect(condition: bool, label: str) -> None:
    if not condition:
        FAILURES.append(label)


def build(rows: list[tuple[str, Tier, str, list[str]]]) -> Ledger:
    ledger = Ledger()
    for claim_id, tier, evidence, supports in rows:
        ledger.claims[claim_id] = Claim(
            id=claim_id,
            tier=tier,
            statement="s",
            evidence_kind=evidence,
            supports=tuple(supports),
        )
    return ledger


def codes(findings: list[Finding]) -> set[str]:
    return {f.code for f in findings}


# ---------------------------------------------------------------------------
# B1 — the tier order is a linear order on five elements
# ---------------------------------------------------------------------------


def b1_order() -> None:
    tiers = [Tier.X, Tier.C, Tier.L, Tier.B, Tier.A]
    expect([t.rank for t in tiers] == [0, 1, 2, 3, 4], "B1: ranks are 0..4 in order")
    expect(all(a <= b for a, b in zip(tiers, tiers[1:])), "B1: chain is ascending")

    # Reflexivity, transitivity, antisymmetry over all 125 triples — exhaustive,
    # not sampled, because five elements make exhaustive cheap.
    for a in tiers:
        expect(a <= a, f"B1: reflexivity at {a.name}")
        for b in tiers:
            expect(
                not (a <= b and b <= a) or a is b,
                f"B1: antisymmetry at ({a.name}, {b.name})",
            )
            for c in tiers:
                expect(
                    not (a <= b and b <= c) or a <= c,
                    f"B1: transitivity at ({a.name}, {b.name}, {c.name})",
                )

    expect(all(t <= Tier.A for t in tiers), "B1: A is the top")
    expect(all(Tier.X <= t for t in tiers), "B1: X is the bottom")
    expect(not Tier.X.citable, "B1: X is not citable")
    expect(all(t.citable for t in tiers if t is not Tier.X), "B1: every other tier is citable")


# ---------------------------------------------------------------------------
# B2 — soundness propagates transitively (the Lean theorem, on data)
# ---------------------------------------------------------------------------


def b2_transitive_soundness() -> None:
    sound = build(
        [
            ("MX-A-0001", Tier.A, "lean_axioms", ["MX-A-0002"]),
            ("MX-A-0002", Tier.A, "lean_axioms", ["MX-A-0003"]),
            ("MX-A-0003", Tier.A, "lean_axioms", []),
        ]
    )
    expect(check(sound) == [], "B2: kernel chain is sound")
    expect(
        set(sound.depends("MX-A-0001")) == {"MX-A-0002", "MX-A-0003"},
        "B2: transitive closure reaches the far end of the chain",
    )

    # The case the direct check cannot see: every edge is sound, but the head
    # still transitively rests on a weaker row.
    leak = build(
        [
            ("MX-B-0001", Tier.B, "exact_harness", ["MX-B-0002"]),
            ("MX-B-0002", Tier.B, "exact_harness", ["MX-L-0003"]),
            ("MX-L-0003", Tier.L, "citation", []),
        ]
    )
    findings = check(leak)
    expect("E-UNSOUND" in codes(findings), "B2: transitive leak is caught")
    expect(
        any("transitively rests on" in f.detail for f in findings),
        "B2: the transitive case is reported as such",
    )

    # A Tier A row may not rest on a Tier L row — SPEC.md §2.4's consequence.
    on_literature = build(
        [
            ("MX-A-0001", Tier.A, "lean_axioms", ["MX-L-0002"]),
            ("MX-L-0002", Tier.L, "citation", []),
        ]
    )
    expect(
        "E-UNSOUND" in codes(check(on_literature)),
        "B2: a kernel claim may not cite literature",
    )

    # Descending tiers are always fine.
    descending = build(
        [
            ("MX-C-0001", Tier.C, "argument", ["MX-L-0002"]),
            ("MX-L-0002", Tier.L, "citation", ["MX-B-0003"]),
            ("MX-B-0003", Tier.B, "exact_harness", ["MX-A-0004"]),
            ("MX-A-0004", Tier.A, "lean_axioms", []),
        ]
    )
    expect(check(descending) == [], "B2: descending chain is sound")


# ---------------------------------------------------------------------------
# B3 — structural hygiene: cycles, dangling ids, uncitable rows
# ---------------------------------------------------------------------------


def b3_structure() -> None:
    cycle = build(
        [
            ("MX-A-0001", Tier.A, "lean_axioms", ["MX-A-0002"]),
            ("MX-A-0002", Tier.A, "lean_axioms", ["MX-A-0001"]),
        ]
    )
    findings = check(cycle)
    expect("E-CYCLE" in codes(findings), "B3: two-cycle is reported")
    expect(
        "E-UNSOUND" not in codes(findings),
        "B3: a cycle suppresses derived soundness noise",
    )
    expect(len([f for f in findings if f.code == "E-CYCLE"]) == 1, "B3: cycle reported once")

    self_loop = build([("MX-A-0001", Tier.A, "lean_axioms", ["MX-A-0001"])])
    expect("E-CYCLE" in codes(check(self_loop)), "B3: self-loop is reported")

    dangling = build([("MX-A-0001", Tier.A, "lean_axioms", ["MX-A-9999"])])
    expect("E-DANGLING" in codes(check(dangling)), "B3: dangling citation is reported")

    uncitable = build(
        [
            ("MX-C-0001", Tier.C, "argument", ["MX-X-0002"]),
            ("MX-X-0002", Tier.X, "numeric", []),
        ]
    )
    expect("E-UNCITABLE" in codes(check(uncitable)), "B3: Tier X may not be cited")

    overclaim = build([("MX-A-0001", Tier.A, "citation", [])])
    expect("E-EVIDENCE" in codes(check(overclaim)), "B3: citation cannot support Tier A")

    unknown = build([("MX-A-0001", Tier.A, "haruspicy", [])])
    expect("E-EVIDENCE" in codes(check(unknown)), "B3: unknown evidence kind is rejected")


# ---------------------------------------------------------------------------
# B4 — claim identifiers
# ---------------------------------------------------------------------------


def b4_claim_ids() -> None:
    stream, tier, seq = parse_claim_id("MF-A-0007")
    expect((stream, tier, seq) == ("MF", Tier.A, 7), "B4: MF-A-0007 parses")

    for bad in ["MX-A-1", "MXA0001", "mx-a-0001", "MX-Q-0001", "ZZ-A-0001", "MX-A-00001", ""]:
        try:
            parse_claim_id(bad)
        except ClaimIdError:
            pass
        else:
            FAILURES.append(f"B4: {bad!r} should not parse")

    for good in ["MX-X-0000", "MF-A-9999", "RM-L-0031", "TN-C-0001"]:
        try:
            parse_claim_id(good)
        except ClaimIdError:
            FAILURES.append(f"B4: {good!r} should parse")


# ---------------------------------------------------------------------------
# Negative controls (SPEC.md §7.2)
#
# Each returns True when it behaved as required, i.e. when the check it targets
# DID fail on deliberately broken input. If any returns False, the corresponding
# check is incapable of failing and every result above is worthless.
# ---------------------------------------------------------------------------


def control_soundness_can_fail() -> bool:
    """The soundness check must reject a kernel claim resting on a conjecture."""
    broken = build(
        [
            ("MX-A-0001", Tier.A, "lean_axioms", ["MX-C-0002"]),
            ("MX-C-0002", Tier.C, "argument", []),
        ]
    )
    return "E-UNSOUND" in codes(check(broken))


def control_transitivity_is_load_bearing() -> bool:
    """A direct-only check would pass this ledger; ours must not.

    This is the control that matters most: it is the only one that distinguishes
    the implementation from a naive one-hop check, which is exactly the defect
    the Lean theorem exists to rule out.
    """
    leak = build(
        [
            ("MX-B-0001", Tier.B, "exact_harness", ["MX-B-0002"]),
            ("MX-B-0002", Tier.B, "exact_harness", ["MX-C-0003"]),
            ("MX-C-0003", Tier.C, "argument", []),
        ]
    )
    direct_only = any(
        leak.claims["MX-B-0001"].tier > leak.claims[s].tier
        for s in leak.claims["MX-B-0001"].supports
    )
    return (not direct_only) and "E-UNSOUND" in codes(check(leak))


def control_order_is_strict() -> bool:
    """The order must actually separate tiers, not accept everything."""
    return not (Tier.A <= Tier.C) and not (Tier.B <= Tier.L)


def control_evidence_cap_bites() -> bool:
    """`llm_output` must never support anything above Tier X (SPEC.md §0)."""
    return "E-EVIDENCE" in codes(check(build([("MX-C-0001", Tier.C, "llm_output", [])])))


def control_clean_ledger_is_accepted() -> bool:
    """The mirror image: the checker must not reject a correct ledger.

    A checker that fails everything is as useless as one that fails nothing.
    """
    return check(build([("MX-A-0001", Tier.A, "lean_axioms", [])])) == []


CONTROLS = [
    ("soundness can fail", control_soundness_can_fail),
    ("transitivity is load-bearing", control_transitivity_is_load_bearing),
    ("order is strict", control_order_is_strict),
    ("evidence cap bites", control_evidence_cap_bites),
    ("clean ledger is accepted", control_clean_ledger_is_accepted),
]


def main() -> int:
    b1_order()
    b2_transitive_soundness()
    b3_structure()
    b4_claim_ids()

    for label, control in CONTROLS:
        if not control():
            FAILURES.append(f"NEGATIVE CONTROL DID NOT FIRE: {label}")

    if FAILURES:
        print(f"FAIL  tier_b_tier_calculus  ({len(FAILURES)} failure(s))")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    print("PASS  tier_b_tier_calculus  (B1-B4, 5 negative controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
