#!/usr/bin/env python3
"""mathesis-gate — a portable verification gate for Lean repositories.

    curl -O .../mathesis_gate.py && python3 mathesis_gate.py

ONE FILE. NO DEPENDENCIES. Python 3.9+, standard library only. Copy it into any
repository and run it. It does not import from Mathesis and does not need this
repository present.

WHAT IT CHECKS
--------------
  1. axiom hygiene   no `axiom` declarations, no `sorry`, in the scanned tree
  2. vacuity         no `... : Prop := True` predicates, no theorems concluding
                     one, no shadowing of core numeric types (`def Real := Float`)
  3. footprints      every Lean module's `#print axioms` output matches the
                     allowlist that module declares in its own header
  4. ledger          if a ledger.jsonl is present: tier soundness across the
                     TRANSITIVE closure, evidence caps, cycles, dangling ids

Check 2 exists because a file can be entirely free of `axiom` and `sorry`, pass
every other check, and still assert nothing: define a predicate as `True`, prove
it `by trivial`, and put the actual claim in the docstring. That shape was found
in the wild while building this tool.

Each is independently switchable, because a gate you cannot adopt incrementally
is a gate nobody adopts.

DECLARING THE CONTRACT
----------------------
A module opts in to the footprint check by declaring its contract in a header
comment:

    MATHESIS-GATE: env=mathlib          # needs a Mathlib build (see --lean-env)
    MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound
    MATHESIS-GATE: allow(witness)=propext   # prefix-scoped override

`allow=` with an empty value means NO AXIOMS AT ALL. Modules with no directive
are skipped by the footprint check and still scanned for axiom hygiene, so
adoption can be file-by-file.

THE GATE IS THE FOOTPRINT, NOT THE SOURCE
-----------------------------------------
A failed proof still defines the theorem name in the environment. The source
contains no `sorry` and `#print axioms` reports `sorryAx`. Any check that greps
the source for `sorry` will pass a broken proof. This one asks the kernel.

SELF-TESTS
----------
The parser's negative controls run on EVERY invocation, before any file is
examined, and the gate exits non-zero if they fail. A gate that has only ever
been observed passing is indistinguishable from a gate that cannot fail; these
are the probes that make the difference visible. `--self-test` runs them alone.

Exit 0 if every enabled check passes, 1 otherwise.

Part of SocrateAI Stream 0 (Mathesis). MIT.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Lexical scanning
# ---------------------------------------------------------------------------

AXIOM_DECL = re.compile(
    r"^[ \t]*(?:@\[[^\]]*\][ \t]*)*"
    r"(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|scoped[ \t]+)*"
    r"axiom[ \t]+([\w'!?]+)",
    re.MULTILINE,
)
SORRY_TOKEN = re.compile(r"\bsorry\b")

#: A predicate defined as identically `True` states nothing and can be "proved"
#: by `trivial`. Stream conventions that forbid vacuous statements (e.g. Rule R3
#: in the RAMA programme) are about exactly this shape, and neither an `axiom`
#: scan nor a `sorry` scan detects it -- the file is honest Lean and the CLAIM
#: lives in the docstring above it.
VACUOUS_PROP = re.compile(
    r"^[ \t]*(?:noncomputable[ \t]+|private[ \t]+|protected[ \t]+)*"
    r"(?:def|abbrev)[ \t]+([\w'!?]+)[^\n]*?:[ \t]*Prop[ \t]*:=[ \t]*True[ \t]*$",
    re.MULTILINE,
)

#: Shadowing a core numeric type. `def Real := Float` silently converts every
#: subsequent statement about the reals into a statement about floating point.
TYPE_SHADOW = re.compile(
    r"^[ \t]*(?:noncomputable[ \t]+)*(?:def|abbrev)[ \t]+"
    r"(Real|Complex|Rat|Int|Nat)[ \t]*:=", re.MULTILINE,
)
DIRECTIVE = re.compile(r"MATHESIS-GATE:\s*(\w+)(?:\(([^)]*)\))?\s*=\s*(.*)")
PRINT_AXIOMS = re.compile(r"^\s*#print\s+axioms\s+\S+", re.MULTILINE)

#: Matched against the WHOLE compiler output, never line by line. Lean wraps
#: `#print axioms` output past its line width, and a line-anchored pattern
#: silently drops every wrapped declaration -- a false all-clear in the only
#: check that evidences a kernel-verified claim.
FOOTPRINT = re.compile(
    r"'(?P<decl>[^']+)' "
    r"(?:depends on axioms: \[(?P<axioms>[^\]]*)\]"
    r"|(?P<none>does not depend on any axioms))"
)


def strip_comments(text: str) -> str:
    """Blank out Lean comments, preserving newlines so line numbers stay exact.

    Handles `--` line comments and nestable `/- -/` blocks. Not a parser: a `--`
    inside a string literal is treated as a comment. That direction is safe --
    it can only cause a declaration hidden in a string to be missed, which is
    not a thing Lean source does.
    """
    out: list[str] = []
    i, n, depth, line_comment = 0, len(text), 0, False
    while i < n:
        ch, two = text[i], text[i : i + 2]
        if line_comment:
            out.append("\n" if ch == "\n" else " ")
            if ch == "\n":
                line_comment = False
            i += 1
        elif depth > 0:
            if two == "/-":
                depth += 1; out.append("  "); i += 2
            elif two == "-/":
                depth -= 1; out.append("  "); i += 2
            else:
                out.append("\n" if ch == "\n" else " "); i += 1
        elif two == "/-":
            depth = 1; out.append("  "); i += 2
        elif two == "--":
            line_comment = True; out.append("  "); i += 2
        else:
            out.append(ch); i += 1
    return "".join(out)


def lean_files(root: Path, excludes: list[str]) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.lean")):
        parts = set(path.parts)
        if ".lake" in parts or "lake-packages" in parts:
            continue  # vendored Mathlib is not this repository's code
        if any(e in str(path) for e in excludes):
            continue
        out.append(path)
    return out


# ---------------------------------------------------------------------------
# Check 1 — axiom hygiene
# ---------------------------------------------------------------------------


def check_vacuity(files: list[Path], root: Path) -> list[str]:
    """Statements that typecheck, compile, and assert nothing."""
    problems = []
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        rel = path.relative_to(root)
        vacuous = set()
        for m in VACUOUS_PROP.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            vacuous.add(m.group(1))
            problems.append(
                f"{rel}:{line}: `{m.group(1)} ... : Prop := True` — a predicate that is "
                "identically true. Any theorem concluding it is vacuous.")
        for m in TYPE_SHADOW.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(
                f"{rel}:{line}: `def {m.group(1)} :=` shadows a core numeric type — "
                "every later statement silently changes meaning.")
        # Theorems whose conclusion is one of this file's vacuous predicates.
        for name in vacuous:
            for m in re.finditer(
                    r"^[ \t]*theorem[ \t]+([\w'!?]+)[^\n]*:[^\n]*\b"
                    + re.escape(name) + r"\b", text, re.MULTILINE):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(
                    f"{rel}:{line}: theorem `{m.group(1)}` concludes the vacuous "
                    f"predicate `{name}` — it establishes nothing.")
    return problems


def check_hygiene(files: list[Path], root: Path, allow_sorry: bool) -> list[str]:
    problems = []
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        rel = path.relative_to(root)
        for m in AXIOM_DECL.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(f"{rel}:{line}: `axiom {m.group(1)}` — unproven assumption")
        if not allow_sorry:
            for m in SORRY_TOKEN.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(f"{rel}:{line}: `sorry` — open proof")
    return problems


# ---------------------------------------------------------------------------
# Check 2 — declared axiom footprints
# ---------------------------------------------------------------------------


class Contract:
    def __init__(self) -> None:
        self.env = "none"
        self.file_allow: set[str] | None = None
        self.scoped: dict[str, set[str]] = {}

    def allowed_for(self, decl: str) -> set[str]:
        short = decl.rsplit(".", 1)[-1]
        for prefix, allowed in sorted(self.scoped.items(), key=lambda kv: -len(kv[0])):
            if short.startswith(prefix):
                return allowed
        return self.file_allow or set()

    @property
    def declared(self) -> bool:
        return self.file_allow is not None or bool(self.scoped)


def parse_contract(path: Path) -> Contract:
    c = Contract()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:100]:
        m = DIRECTIVE.search(line)
        if not m:
            continue
        key, scope, value = m.group(1), m.group(2), m.group(3).strip()
        items = {v.strip() for v in value.split(",") if v.strip()}
        if key == "env":
            c.env = value or "none"
        elif key == "allow":
            if scope:
                c.scoped[scope.rstrip("*")] = items
            else:
                c.file_allow = items
    return c


def compile_module(path: Path, contract: Contract, lean_env: Path | None,
                   lean_root: Path) -> tuple[int, str]:
    if contract.env.startswith("mathlib"):
        if lean_env is None:
            return 127, "module declares env=mathlib but no --lean-env was given"
        p = subprocess.run(["lake", "env", "lean", str(path.resolve())],
                           cwd=lean_env, capture_output=True, text=True)
    else:
        p = subprocess.run(["lean", str(path.resolve())],
                           cwd=lean_root, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def check_footprints(files: list[Path], root: Path, lean_env: Path | None,
                     verbose: bool) -> list[str]:
    problems: list[str] = []
    checked = 0
    for path in files:
        contract = parse_contract(path)
        if not contract.declared:
            continue  # opt-in, so adoption can be file-by-file
        rel = path.relative_to(root)
        code, output = compile_module(path, contract, lean_env, root)
        if code == 127:
            problems.append(f"{rel}: {output}"); continue
        if code != 0 or re.search(r"^.*: error:", output, re.MULTILINE):
            problems.append(f"{rel}: did not compile\n{output.strip()[:1200]}"); continue
        if "declaration uses 'sorry'" in output:
            problems.append(f"{rel}: uses sorry")

        printed = 0
        for m in FOOTPRINT.finditer(output):
            printed += 1
            actual = set() if m.group("none") else {
                a.strip() for a in m.group("axioms").split(",") if a.strip()}
            extra = actual - contract.allowed_for(m.group("decl"))
            if extra:
                problems.append(
                    f"{rel}: {m.group('decl')} has undeclared axiom(s) {sorted(extra)}; "
                    f"declared allowlist is {sorted(contract.allowed_for(m.group('decl'))) or '[]'}")

        requested = len(PRINT_AXIOMS.findall(path.read_text(encoding="utf-8", errors="replace")))
        if requested == 0:
            problems.append(f"{rel}: declares a contract but prints no footprints — "
                            "add `#print axioms` for each theorem")
        elif printed != requested:
            problems.append(
                f"{rel}: {requested} `#print axioms` directive(s) but {printed} footprint(s) "
                f"parsed — {requested - printed} declaration(s) went unchecked")
        else:
            checked += 1
            if verbose:
                print(f"    {rel}: {printed}/{requested} footprint(s) as declared")
    if verbose and checked:
        print(f"    ({checked} module(s) with a declared contract)")
    return problems


# ---------------------------------------------------------------------------
# Check 3 — ledger soundness
# ---------------------------------------------------------------------------

TIER_RANK = {"X": 0, "C": 1, "L": 2, "B": 3, "A": 4}
EVIDENCE_CAP = {
    "lean_axioms": "A", "exact_harness": "B", "citation": "L",
    "argument": "C", "numeric": "X", "llm_output": "X",
}
CLAIM_ID = re.compile(r"^[A-Z]{2}-([XCLBA])-\d{4}$")


def check_ledger(path: Path) -> list[str]:
    problems: list[str] = []
    rows: dict[str, dict] = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            row = json.loads(line)
        except Exception:
            problems.append(f"{path.name}:{n}: invalid JSON"); continue
        cid = row.get("id", "")
        m = CLAIM_ID.match(cid)
        if not m:
            problems.append(f"{path.name}:{n}: malformed id \"{cid}\""); continue
        if cid in rows:
            problems.append(f"{path.name}:{n}: duplicate id {cid}"); continue
        if row.get("tier") != m.group(1):
            problems.append(f"{cid}: tier field \"{row.get('tier')}\" disagrees with the id")
        cap = EVIDENCE_CAP.get(row.get("evidence_kind", ""))
        if cap is None:
            problems.append(f"{cid}: unknown evidence_kind \"{row.get('evidence_kind')}\"")
        elif TIER_RANK.get(row.get("tier"), 0) > TIER_RANK[cap]:
            problems.append(f"{cid}: evidence_kind \"{row['evidence_kind']}\" caps at "
                            f"tier {cap} but the row is filed at {row.get('tier')}")
        rows[cid] = row

    for cid, row in rows.items():
        for s in row.get("supports", []):
            if s not in rows:
                problems.append(f"{cid}: cites {s}, which has no row")
            elif rows[s].get("tier") == "X":
                problems.append(f"{cid}: cites {s}, which is Tier X and may not be cited")

    # Transitive closure. The direct check flags the offending EDGE; this flags
    # every claim contaminated through it, which is the retraction question.
    for cid, row in rows.items():
        seen, stack = set(), list(row.get("supports", []))
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in rows:
                continue
            seen.add(cur)
            if TIER_RANK.get(row.get("tier"), 0) > TIER_RANK.get(rows[cur].get("tier"), 0):
                problems.append(
                    f"{cid} (tier {row.get('tier')}) transitively rests on {cur} "
                    f"(tier {rows[cur].get('tier')})")
            stack.extend(rows[cur].get("supports", []))
        if cid in seen:
            problems.append(f"{cid}: is in its own transitive support — cycle")
    return problems


# ---------------------------------------------------------------------------
# Self-tests — negative controls, run on every invocation
# ---------------------------------------------------------------------------


def self_test() -> list[str]:
    bad: list[str] = []

    def want(cond: bool, label: str) -> None:
        if not cond:
            bad.append(f"SELF-TEST FAILED: {label}")

    ax = lambda src: [m.group(1) for m in AXIOM_DECL.finditer(strip_comments(src))]
    want(ax("axiom foo : Nat\n") == ["foo"], "finds a plain axiom")
    want(ax("  axiom sneaky : Nat\n") == ["sneaky"], "finds an INDENTED axiom")
    want(ax("private axiom a : N\n@[simp] axiom b : N\n") == ["a", "b"],
         "finds private and attributed axioms")
    want(ax("-- axiom foo\n/- axiom bar -/\n/- /- axiom baz -/ -/\n") == [],
         "ignores line, block and nested comments")
    want(strip_comments("--x\n/-y\nz-/\naxiom real : N\n").count("\n", 0,
         AXIOM_DECL.search(strip_comments("--x\n/-y\nz-/\naxiom real : N\n")).start()) + 1 == 4,
         "stripper preserves line numbers")

    fp = lambda o: {m.group("decl") for m in FOOTPRINT.finditer(o)}
    want(fp("'A.b' depends on axioms: [propext]\n") == {"A.b"}, "flat footprint parses")
    want(fp("'A.long_name' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]\n")
         == {"A.long_name"}, "WRAPPED footprint parses")
    want(fp("'A.c' does not depend on any axioms\n") == {"A.c"},
         "axiom-free footprint parses as present, not missing")
    want(len(PRINT_AXIOMS.findall("#print axioms a\n  #print axioms b\n")) == 2,
         "directive counter finds indented directives")

    vac = lambda src: [m.group(1) for m in VACUOUS_PROP.finditer(strip_comments(src))]
    want(vac("def uniformBoundedness (D : F) : Prop := True\n") == ["uniformBoundedness"],
         "finds a `Prop := True` predicate")
    want(vac("def realPredicate (x : Nat) : Prop := x > 0\n") == [],
         "does NOT flag a predicate with actual content")
    want([m.group(1) for m in TYPE_SHADOW.finditer("def Real := Float\n")] == ["Real"],
         "finds a shadowed core type")
    want([m.group(1) for m in TYPE_SHADOW.finditer("def RealBound := 3\n")] == [],
         "does NOT flag a name merely starting with a core type")
    return bad


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Portable Lean verification gate (Mathesis Stream 0).")
    ap.add_argument("path", nargs="?", default=".", help="repository root to scan")
    ap.add_argument("--lean-src", default=None,
                    help="subdirectory containing Lean sources (default: whole tree)")
    ap.add_argument("--lean-env", default=os.environ.get("LEAN_ENV_DIR"),
                    help="Lake project providing Mathlib, for modules declaring env=mathlib")
    ap.add_argument("--ledger", default=None, help="path to a ledger.jsonl")
    ap.add_argument("--exclude", action="append", default=[],
                    help="substring to exclude from scanning (repeatable)")
    ap.add_argument("--allow-sorry", action="store_true",
                    help="report axioms but tolerate `sorry` (staged adoption)")
    ap.add_argument("--skip-hygiene", action="store_true")
    ap.add_argument("--skip-vacuity", action="store_true")
    ap.add_argument("--skip-footprints", action="store_true")
    ap.add_argument("--report-only", action="store_true",
                    help="print findings but always exit 0")
    ap.add_argument("--self-test", action="store_true", help="run controls and exit")
    ap.add_argument("--version", action="version", version=f"mathesis-gate {VERSION}")
    args = ap.parse_args()

    failures = self_test()
    if failures:
        print(f"FAIL  mathesis-gate: the checker itself is broken ({len(failures)})")
        for f in failures:
            print(f"  - {f}")
        return 1
    if args.self_test:
        print(f"PASS  mathesis-gate self-test ({VERSION}) — 13 controls")
        return 0

    root = Path(args.path).resolve()
    scan_root = root / args.lean_src if args.lean_src else root
    files = lean_files(scan_root, args.exclude) if scan_root.is_dir() else []

    print(f"mathesis-gate {VERSION} — {root}")
    print(f"  {len(files)} Lean file(s) scanned"
          + (f", excluding {args.exclude}" if args.exclude else ""))

    problems: list[tuple[str, list[str]]] = []
    if not args.skip_hygiene:
        problems.append(("axiom hygiene", check_hygiene(files, root, args.allow_sorry)))
    if not args.skip_vacuity:
        problems.append(("vacuity", check_vacuity(files, root)))
    if not args.skip_footprints and files:
        env = Path(args.lean_env).resolve() if args.lean_env else None
        problems.append(("declared footprints", check_footprints(files, root, env, True)))
    if args.ledger:
        lp = Path(args.ledger)
        problems.append(("ledger", check_ledger(lp) if lp.is_file()
                         else [f"{lp}: not found"]))

    total = 0
    for name, found in problems:
        if found:
            total += len(found)
            print(f"\nFAIL  {name} ({len(found)} finding(s))")
            for f in found[:40]:
                print(f"  - {f}")
            if len(found) > 40:
                print(f"  ... and {len(found) - 40} more")
        else:
            print(f"PASS  {name}")

    if total == 0:
        print("\nALL CHECKS PASS")
        return 0
    print(f"\n{total} finding(s)."
          + ("  (--report-only: exiting 0)" if args.report_only else ""))
    return 0 if args.report_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
