#!/usr/bin/env python3
"""Tier B harness — `axiom` and `sorry` hygiene.

Two parts, deliberately separated:

**Gated.** Stream 0's own `lean/` must contain zero `axiom` declarations and
zero `sorry` (SPEC.md §7.1, SPEC-STREAM0 L4.1). This always runs and can always
fail.

**Survey (informational).** If the sibling stream trees are present, count their
`axiom` and `sorry` occurrences and report them with per-file `sha256`. This
**never fails the gate.**

The split matters. Making Stream 0's gate go red because another stream edited a
file would turn the foundation into a bottleneck — the exact failure mode
SPEC-STREAM0 R3.3 and HARDNESS.md H10 exist to prevent. A survey finding is a
Tier C observation about someone else's tree at a recorded hash, not a Tier B
claim about this repository.

WHY THIS SCANS STRIPPED SOURCE
------------------------------
An earlier version anchored the pattern at column 0 (`^axiom`). That made its
"ignores prose" control pass for the wrong reason: the pattern missed comments
because it missed *everything* not at column 0 — including
`  axiom sneaky : Nat` inside a namespace, and `private axiom hidden`. A checker
a single space can evade is not a checker (HARDNESS.md H2).

This version strips Lean comments first, then matches declarations anywhere.
Both properties are now controlled for independently: the indentation controls
prove it cannot be evaded, the comment controls prove it is not noisy.

WHAT THIS IS NOT
----------------
A lexical scan is not the kernel. Stream 0's own tree is additionally gated on
`#print axioms` (Gate 2), which is the authoritative check. For *other* streams'
trees we cannot compile — that needs their build environment — so the survey is
a lexical approximation, and everything it produces is Tier C by construction.
See `docs/designs/RECONCILIATION.md` §4 and ledger row `MX-C-0003`.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDEV = ROOT.parent

#: An `axiom` declaration anywhere in stripped source, with any leading
#: whitespace, attribute, or modifier. Lean identifiers may contain `'`, `!`, `?`.
AXIOM_DECL = re.compile(
    r"^[ \t]*(?:@\[[^\]]*\][ \t]*)*"
    r"(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|scoped[ \t]+)*"
    r"axiom[ \t]+([\w'!?]+)",
    re.MULTILINE,
)

#: `sorry` as a whole token. Stream 5 states Rule R2 about these, so the survey
#: reports them; Stream 0 forbids them outright.
SORRY_TOKEN = re.compile(r"\bsorry\b")

#: Sibling trees to survey, if present. Never gated on.
SURVEY_TARGETS = {
    "MechanicaFluidorum": XDEV / "SocrateAI-Scientific-MechanicaFluidorum/lean_src",
    "RajMathRecovery": XDEV / "SocrateAI-Scientific-RajMathRecovery/dualscale/lean/DualScale",
}

FAILURES: list[str] = []


def strip_comments(text: str) -> str:
    """Blank out Lean comments, preserving line structure and offsets.

    Handles `--` line comments and nestable `/- -/` block comments (including
    `/-- -/` doc comments). Newlines are preserved so line numbers stay exact;
    everything else inside a comment becomes a space.

    Not a Lean parser: a `--` inside a string literal is treated as a comment.
    That direction is safe here — it can only cause the scanner to *miss* a
    declaration hidden in a string, which is not a thing Lean source does.
    """
    out: list[str] = []
    i, n = 0, len(text)
    depth = 0  # block-comment nesting depth
    in_line_comment = False

    while i < n:
        ch = text[i]
        two = text[i : i + 2]

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
                out.append("\n")
            else:
                out.append(" ")
            i += 1
        elif depth > 0:
            if two == "/-":
                depth += 1
                out.append("  ")
                i += 2
            elif two == "-/":
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if ch == "\n" else " ")
                i += 1
        elif two == "/-":
            depth = 1
            out.append("  ")
            i += 2
        elif two == "--":
            in_line_comment = True
            out.append("  ")
            i += 2
        else:
            out.append(ch)
            i += 1

    return "".join(out)


def scan(directory: Path) -> tuple[list[tuple[Path, int, str]], list[tuple[Path, int]]]:
    """Return (axiom hits, sorry hits) over stripped source."""
    axioms: list[tuple[Path, int, str]] = []
    sorries: list[tuple[Path, int]] = []
    if not directory.is_dir():
        return axioms, sorries
    for path in sorted(directory.rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for match in AXIOM_DECL.finditer(text):
            axioms.append((path, text.count("\n", 0, match.start()) + 1, match.group(1)))
        for match in SORRY_TOKEN.finditer(text):
            sorries.append((path, text.count("\n", 0, match.start()) + 1))
    return axioms, sorries


def check_own_tree() -> None:
    axioms, sorries = scan(ROOT / "lean")
    for path, lineno, name in axioms:
        FAILURES.append(
            f"{path.relative_to(ROOT)}:{lineno}: `axiom {name}` — no custom axioms "
            "in Stream 0 (SPEC.md §7.1)"
        )
    for path, lineno in sorries:
        FAILURES.append(
            f"{path.relative_to(ROOT)}:{lineno}: `sorry` — Stream 0 ships no open proofs"
        )


def survey() -> list[str]:
    lines: list[str] = []
    for label, directory in SURVEY_TARGETS.items():
        if not directory.is_dir():
            lines.append(f"  {label}: tree not present — not surveyed")
            continue
        axioms, sorries = scan(directory)
        lines.append(f"  {label}: {len(axioms)} axiom(s), {len(sorries)} sorry(s)")
        by_file: dict[Path, list[str]] = {}
        for path, lineno, name in axioms:
            by_file.setdefault(path, []).append(f"axiom {name}:{lineno}")
        for path, lineno in sorries:
            by_file.setdefault(path, []).append(f"sorry:{lineno}")
        for path, names in sorted(by_file.items()):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
            rel = path.relative_to(directory.parent) if directory.parent in path.parents else path
            lines.append(f"    {rel}  sha256:{digest}  {', '.join(names)}")
    return lines


# ---------------------------------------------------------------------------
# Negative controls (SPEC.md §7.2)
#
# Two families, because the scanner has two independent ways to be wrong:
# it can miss a real declaration (evasion), or flag prose (noise). The earlier
# column-0 version bought the second by sacrificing the first.
# ---------------------------------------------------------------------------


def _axioms_in(source: str) -> list[str]:
    return [m.group(1) for m in AXIOM_DECL.finditer(strip_comments(source))]


def control_finds_plain_axiom() -> bool:
    return _axioms_in("namespace X\naxiom foo : Nat\nend X\n") == ["foo"]


def control_finds_indented_axiom() -> bool:
    """A single leading space must not hide a declaration.

    This is the control the previous implementation would have failed.
    """
    return _axioms_in("namespace X\n  axiom sneaky : Nat\nend X\n") == ["sneaky"]


def control_finds_modified_axiom() -> bool:
    """`private`, `protected`, and attributes must not hide a declaration."""
    source = "private axiom a : Nat\n@[simp] axiom b : Nat\nprotected axiom c : Nat\n"
    return _axioms_in(source) == ["a", "b", "c"]


def control_ignores_line_comment() -> bool:
    return _axioms_in("-- axiom foo : Nat\nx := 1  -- axiom bar\n") == []


def control_ignores_block_comment() -> bool:
    """Block and doc comments, including nested ones, are not declarations."""
    source = "/- axiom foo : Nat -/\n/-- axiom bar -/\n/- outer /- axiom baz -/ still -/\n"
    return _axioms_in(source) == []


def control_stripper_preserves_line_numbers() -> bool:
    """Line numbers must survive stripping, or every report points nowhere."""
    source = "-- comment\n/- block\nspanning -/\naxiom real : Nat\n"
    stripped = strip_comments(source)
    match = AXIOM_DECL.search(stripped)
    return match is not None and stripped.count("\n", 0, match.start()) + 1 == 4


def control_finds_sorry_but_not_in_comment() -> bool:
    source = "theorem t : True := by\n  sorry\n-- sorry in a comment\n"
    stripped = strip_comments(source)
    hits = [stripped.count("\n", 0, m.start()) + 1 for m in SORRY_TOKEN.finditer(stripped)]
    return hits == [2]


CONTROLS = [
    ("finds a plain axiom", control_finds_plain_axiom),
    ("finds an INDENTED axiom", control_finds_indented_axiom),
    ("finds private/attributed axioms", control_finds_modified_axiom),
    ("ignores a line comment", control_ignores_line_comment),
    ("ignores block and nested comments", control_ignores_block_comment),
    ("stripper preserves line numbers", control_stripper_preserves_line_numbers),
    ("finds sorry in code, not in comments", control_finds_sorry_but_not_in_comment),
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

    print(
        f"PASS  tier_b_axiom_hygiene  (own tree: 0 axioms, 0 sorry, "
        f"{len(CONTROLS)} negative controls)"
    )
    if "--survey" in sys.argv:
        print("SURVEY (informational — never gates; Tier C, see MX-C-0003):")
        for line in survey():
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
