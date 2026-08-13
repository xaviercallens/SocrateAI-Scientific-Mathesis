#!/usr/bin/env python3
"""Tier B harness — the float ban, enforced by parsing rather than by grep.

SPEC.md §4: floats are barred outside `exploration/`. This is not stylistic.
Stream 1 records the reason: a Tier B claim is only as exact as its arithmetic,
and a single `0.1` in a certified path silently converts a proof into an
estimate.

The check is an AST walk, not a regex, so `x = 1.5` is caught while the string
`"version 1.5"` and the comment `# 1.5x faster` are not. A grep-based version of
this rule would produce false positives, be disabled, and stop protecting
anything — which is how these rules actually die.

Every file in `exploration/` is exempt but must carry the Tier X banner.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Directories whose Python must be float-free.
GUARDED = [ROOT / "python", ROOT / "tests", ROOT / "scripts"]

#: The only place floats are allowed, and the banner every such file must carry.
EXPLORATION = ROOT / "exploration"
TIER_X_BANNER = "# TIER X — EXPLORATORY, NO CLAIMS"

FAILURES: list[str] = []


class FloatFinder(ast.NodeVisitor):
    """Flags float literals and calls to `float(...)`."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.hits: list[tuple[int, str]] = []

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, float):
            self.hits.append((node.lineno, f"float literal {node.value!r}"))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == "float":
            self.hits.append((node.lineno, "call to float()"))
        self.generic_visit(node)


def guarded_files() -> list[Path]:
    files: list[Path] = []
    for directory in GUARDED:
        if directory.is_dir():
            files.extend(sorted(directory.rglob("*.py")))
    return files


def check_float_ban() -> None:
    for path in guarded_files():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            FAILURES.append(f"{path.relative_to(ROOT)}: does not parse: {exc}")
            continue
        finder = FloatFinder(path)
        finder.visit(tree)
        for lineno, what in finder.hits:
            FAILURES.append(f"{path.relative_to(ROOT)}:{lineno}: {what} (SPEC.md §4)")


def check_exploration_banners() -> None:
    if not EXPLORATION.is_dir():
        return
    for path in sorted(EXPLORATION.rglob("*.py")):
        head = path.read_text(encoding="utf-8").lstrip().splitlines()[:5]
        if not any(line.strip().startswith(TIER_X_BANNER) for line in head):
            FAILURES.append(
                f"{path.relative_to(ROOT)}: missing the `{TIER_X_BANNER}` banner "
                "in its first five lines (SPEC.md §3)"
            )


# ---------------------------------------------------------------------------
# Negative control (SPEC.md §7.2)
# ---------------------------------------------------------------------------


def control_finder_detects_a_planted_float() -> bool:
    """Feed the finder a float and confirm it reports it.

    Without this, a refactor that broke `visit_Constant` would turn the whole
    harness into a green light that checks nothing.
    """
    source = "x = 1\ny = 2.5\nz = float('3')\nw = 'not 4.5'  # nor 5.5\n"
    finder = FloatFinder(Path("<control>"))
    finder.visit(ast.parse(source))
    lines = {lineno for lineno, _ in finder.hits}
    return lines == {2, 3}


def control_banner_check_rejects_a_bare_file() -> bool:
    """A file without the banner must be flagged."""
    return not any(
        line.strip().startswith(TIER_X_BANNER) for line in "import os\n".splitlines()[:5]
    )


CONTROLS = [
    ("float finder detects a planted float", control_finder_detects_a_planted_float),
    ("banner check rejects a bare file", control_banner_check_rejects_a_bare_file),
]


def main() -> int:
    check_float_ban()
    check_exploration_banners()

    for label, control in CONTROLS:
        if not control():
            FAILURES.append(f"NEGATIVE CONTROL DID NOT FIRE: {label}")

    scanned = len(guarded_files())
    if FAILURES:
        print(f"FAIL  tier_b_no_floats  ({len(FAILURES)} failure(s), {scanned} file(s) scanned)")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1

    print(f"PASS  tier_b_no_floats  ({scanned} file(s) scanned, 2 negative controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
