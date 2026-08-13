#!/usr/bin/env python3
"""Tier B harness — `axiom` hygiene.

Two parts, deliberately separated:

**Gated.** Stream 0's own `lean/` must contain zero `axiom` declarations
(SPEC.md §7.1, SPEC-STREAM0 L4.1). This always runs and can always fail.

**Survey (informational).** If the sibling stream trees are present, count their
`axiom` declarations and write a dated report. This **never fails the gate.**

The split matters. Making Stream 0's gate go red because another stream edited a
file would turn the foundation into a bottleneck — the exact failure mode
SPEC-STREAM0 R3.3 and HARDNESS.md H10 exist to prevent. A survey finding is a
Tier C observation about someone else's tree at a recorded hash, not a Tier B
claim about this repository.

What the survey found on 2026-08-13 is recorded in `docs/designs/RECONCILIATION.md`
§3 and as ledger row `MX-C-0003`.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDEV = ROOT.parent

#: An `axiom` declaration at the start of a line. Deliberately not matching
#: `axiom` inside comments or strings — those are prose about axioms, which is
#: what most of this repository's documentation is.
AXIOM_DECL = re.compile(r"^axiom\s+(\w+)", re.MULTILINE)

#: Sibling trees to survey, if present. Never gated on.
SURVEY_TARGETS = {
    "MechanicaFluidorum": XDEV / "SocrateAI-Scientific-MechanicaFluidorum/lean_src",
    "RajMathRecovery": XDEV / "SocrateAI-Scientific-RajMathRecovery/dualscale/lean/DualScale",
}

FAILURES: list[str] = []


def scan(directory: Path) -> list[tuple[Path, int, str]]:
    """Return (path, lineno, name) for every `axiom` declaration found."""
    hits: list[tuple[Path, int, str]] = []
    if not directory.is_dir():
        return hits
    for path in sorted(directory.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in AXIOM_DECL.finditer(text):
            lineno = text.count("\n", 0, match.start()) + 1
            hits.append((path, lineno, match.group(1)))
    return hits


def check_own_tree() -> None:
    hits = scan(ROOT / "lean")
    for path, lineno, name in hits:
        FAILURES.append(
            f"{path.relative_to(ROOT)}:{lineno}: `axiom {name}` — no custom axioms "
            "in Stream 0 (SPEC.md §7.1)"
        )


def survey() -> list[str]:
    lines: list[str] = []
    for label, directory in SURVEY_TARGETS.items():
        if not directory.is_dir():
            lines.append(f"  {label}: tree not present — not surveyed")
            continue
        hits = scan(directory)
        lines.append(f"  {label}: {len(hits)} axiom declaration(s)")
        by_file: dict[Path, list[str]] = {}
        for path, lineno, name in hits:
            by_file.setdefault(path, []).append(f"{name}:{lineno}")
        for path, names in sorted(by_file.items()):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
            rel = path.relative_to(directory.parent) if directory.parent in path.parents else path
            lines.append(f"    {rel}  sha256:{digest}  {', '.join(names)}")
    return lines


# ---------------------------------------------------------------------------
# Negative controls (SPEC.md §7.2)
# ---------------------------------------------------------------------------


def control_scanner_finds_a_planted_axiom() -> bool:
    """The regex must actually match a declaration."""
    source = "namespace X\naxiom foo : Nat\ntheorem bar : True := trivial\nend X\n"
    return [m.group(1) for m in AXIOM_DECL.finditer(source)] == ["foo"]


def control_scanner_ignores_prose() -> bool:
    """`axiom` in a comment or mid-line is not a declaration.

    Without this the harness would flag its own documentation, be dismissed as
    noisy, and stop being run — which is how a rule dies.
    """
    source = "-- no axiom declarations allowed\n/- the axiom foo pattern -/\nx := 1 -- axiom bar\n"
    return list(AXIOM_DECL.finditer(source)) == []


CONTROLS = [
    ("scanner finds a planted axiom", control_scanner_finds_a_planted_axiom),
    ("scanner ignores prose", control_scanner_ignores_prose),
]


def main() -> int:
    check_own_tree()

    for label, control in CONTROLS:
        if not control():
            FAILURES.append(f"NEGATIVE CONTROL DID NOT FIRE: {label}")

    if FAILURES:
        print(f"FAIL  tier_b_axiom_hygiene  ({len(FAILURES)} failure(s))")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    print("PASS  tier_b_axiom_hygiene  (own tree: 0 axioms, 2 negative controls)")
    if "--survey" in sys.argv:
        print("SURVEY (informational — never gates; Tier C, see MX-C-0003):")
        for line in survey():
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
