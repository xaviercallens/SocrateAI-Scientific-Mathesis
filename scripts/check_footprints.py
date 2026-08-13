#!/usr/bin/env python3
"""Gate 2 — kernel-compile every Lean module and check its declared footprint.

Each module declares its own gate contract in header comments:

    MATHESIS-GATE: env=mathlib            # needs the shared Mathlib build
    MATHESIS-GATE: allow=propext,Classical.choice,Quot.sound
    MATHESIS-GATE: allow(witness)=propext # prefix-scoped override

`allow=` with an empty value means *no axioms at all*. A prefix-scoped line
`allow(<prefix>)=` applies to declarations whose final name component starts
with `<prefix>`, and overrides the file-wide list for those.

Why per-declaration and not per-file: a file-wide allowlist is only as tight as
its loosest declaration. `TierCalculus.lean` is axiom-free everywhere except
five `decide`-closed witness lemmas, which inherit `propext` from Lean core's
decidability instance for `Fin n` quantifiers. Collapsing that to one file-wide
`[propext]` would silently license a real axiom appearing in the theory later.
That is exactly how the declaration in this repository went stale once already
(LL.md LL-2).

Exit: 0 all modules as declared, 1 otherwise.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = ROOT / "lean"

#: Candidate Mathlib providers, tried in order. Override with LEAN_ENV_DIR.
#:
#: THIS IS A KNOWN FRAGILITY AND THE ORDER MATTERS (PLAN.md K1). Stream 0 owns
#: no Mathlib, so it borrows one. The two available checkouts have *different
#: built subsets and neither is complete*: MechanicaFluidorum has
#: `Analysis.Calculus.Deriv.*` and `SpecialFunctions.Log.Deriv`;
#: RajMathRecovery does not. So which tree this resolves to silently determines
#: what Stream 0 can prove -- UC5's analytic bridge is provable against the
#: first and not against the second, with no diagnostic distinguishing "false"
#: from "module not built".
#:
#: The resolved directory is printed in the gate output so the dependency is
#: visible rather than assumed. The fix is K1 (Stream 0 owns a pinned build),
#: not a longer candidate list.
DEFAULT_ENV_CANDIDATES = [
    Path.home() / "xdev/SocrateAI-Scientific-MechanicaFluidorum/lean_src",
    Path.home() / "xdev/SocrateAI-Scientific-RajMathRecovery/dualscale/lean",
]


def resolve_env() -> Path | None:
    override = os.environ.get("LEAN_ENV_DIR")
    if override:
        path = Path(override)
        return path if path.is_dir() else None
    for candidate in DEFAULT_ENV_CANDIDATES:
        if (candidate / ".lake").is_dir():
            return candidate
    return None

DIRECTIVE = re.compile(r"MATHESIS-GATE:\s*(\w+)(?:\(([^)]*)\))?\s*=\s*(.*)")

#: Matched against the WHOLE compiler output, never line by line.
#:
#: Lean wraps `#print axioms` output when the declaration name plus footprint
#: exceeds its line width, e.g.
#:
#:     'Foo.Bar.kinetic_energy_conserved' depends on axioms: [propext,
#:      Classical.choice,
#:      Quot.sound]
#:
#: A line-anchored version of this pattern silently skipped every wrapped
#: declaration -- see LL.md LL-11. Because wrapping is triggered by long names,
#: it hid precisely the deeply-namespaced declarations in new modules. The
#: negated character class already spans newlines, so matching over the full
#: output is all that is required.
FOOTPRINT = re.compile(
    r"'(?P<decl>[^']+)' "
    r"(?:depends on axioms: \[(?P<axioms>[^\]]*)\]"
    r"|(?P<none>does not depend on any axioms))"
)

#: Every `#print axioms` in the source must produce exactly one parsed
#: footprint. This is the structural guard: it converts "the parser silently
#: dropped one" from an invisible failure into a gate failure.
PRINT_AXIOMS = re.compile(r"^\s*#print\s+axioms\s+\S+", re.MULTILINE)


class Contract:
    def __init__(self) -> None:
        self.env: str = "none"
        self.file_allow: set[str] | None = None
        self.scoped: dict[str, set[str]] = {}

    def allowed_for(self, decl: str) -> set[str]:
        short = decl.rsplit(".", 1)[-1]
        for prefix, allowed in sorted(self.scoped.items(), key=lambda kv: -len(kv[0])):
            if short.startswith(prefix):
                return allowed
        return self.file_allow or set()


def parse_contract(path: Path) -> Contract:
    contract = Contract()
    for line in path.read_text(encoding="utf-8").splitlines()[:80]:
        match = DIRECTIVE.search(line)
        if match is None:
            continue
        key, scope, value = match.group(1), match.group(2), match.group(3).strip()
        items = {v.strip() for v in value.split(",") if v.strip()}
        if key == "env":
            contract.env = value or "none"
        elif key == "allow":
            if scope:
                contract.scoped[scope.rstrip("*")] = items
            else:
                contract.file_allow = items
    return contract


def compile_module(path: Path, contract: Contract) -> tuple[int, str]:
    rel = path.relative_to(LEAN_DIR)
    if contract.env == "mathlib":
        env_dir = resolve_env()
        if env_dir is None:
            return 127, (
                "no Mathlib provider found. Set LEAN_ENV_DIR, or build one of: "
                + ", ".join(str(c) for c in DEFAULT_ENV_CANDIDATES)
            )
        proc = subprocess.run(
            ["lake", "env", "lean", str(path)],
            cwd=env_dir, capture_output=True, text=True,
        )
    else:
        proc = subprocess.run(
            ["lean", str(rel)], cwd=LEAN_DIR, capture_output=True, text=True
        )
    return proc.returncode, proc.stdout + proc.stderr


def check(path: Path) -> list[str]:
    failures: list[str] = []
    contract = parse_contract(path)
    rel = path.relative_to(ROOT)

    if contract.file_allow is None and not contract.scoped:
        return [f"{rel}: no `MATHESIS-GATE: allow=` directive — the gate contract must be declared"]

    code, output = compile_module(path, contract)
    if code == 127:
        return [f"{rel}: {output}"]
    if code != 0:
        return [f"{rel}: did not compile\n{output.strip()[:2000]}"]
    if re.search(r"^.*: error:", output, re.MULTILINE):
        return [f"{rel}: reported an error\n{output.strip()[:2000]}"]
    if "declaration uses 'sorry'" in output:
        failures.append(f"{rel}: uses sorry")

    printed = 0
    for match in FOOTPRINT.finditer(output):
        printed += 1
        decl = match.group("decl")
        actual = set() if match.group("none") else {
            a.strip() for a in match.group("axioms").split(",") if a.strip()
        }
        allowed = contract.allowed_for(decl)
        extra = actual - allowed
        if extra:
            failures.append(
                f"{rel}: {decl} has undeclared axiom(s) {sorted(extra)}; "
                f"declared allowlist for this declaration is {sorted(allowed) or '[]'}"
            )

    requested = len(PRINT_AXIOMS.findall(path.read_text(encoding="utf-8")))
    if requested == 0:
        failures.append(f"{rel}: printed no axiom footprints — add `#print axioms` lines")
    elif printed != requested:
        # The parser dropped something the source asked for. Never trust the
        # remaining results from this file: an unparsed footprint is an
        # unchecked declaration, which is indistinguishable from a passing one.
        failures.append(
            f"{rel}: source has {requested} `#print axioms` directive(s) but only "
            f"{printed} footprint(s) parsed — {requested - printed} declaration(s) "
            "went unchecked (LL-11)"
        )
    elif not failures:
        env_note = contract.env
        if contract.env == "mathlib":
            resolved = resolve_env()
            env_note = f"mathlib@{resolved.name}" if resolved else "mathlib@UNRESOLVED"
        print(f"  {rel}: {printed}/{requested} footprint(s) as declared (env={env_note})")

    return failures


def _parse(output: str) -> dict[str, set[str]]:
    """Parser under test, isolated so the self-tests exercise the real thing."""
    result: dict[str, set[str]] = {}
    for match in FOOTPRINT.finditer(output):
        axioms = set() if match.group("none") else {
            a.strip() for a in match.group("axioms").split(",") if a.strip()
        }
        result[match.group("decl")] = axioms
    return result


def self_test() -> list[str]:
    """Controls for the parser, run on every invocation.

    Gate 2 has no negative-control harness of its own -- it *is* the harness --
    so its controls live here and are never skipped. LL-11 is the incident that
    made this necessary: the parser silently dropped wrapped declarations and
    reported PASS, which is the worst available failure mode for a gate.
    """
    problems: list[str] = []

    def expect(condition: bool, label: str) -> None:
        if not condition:
            problems.append(f"GATE 2 SELF-TEST FAILED: {label}")

    flat = "'A.b' depends on axioms: [propext, Quot.sound]\n"
    expect(_parse(flat) == {"A.b": {"propext", "Quot.sound"}}, "flat footprint parses")

    # The exact shape that defeated the previous implementation.
    wrapped = (
        "'A.kinetic_energy_conserved' depends on axioms: [propext,\n"
        " Classical.choice,\n"
        " Quot.sound]\n"
    )
    expect(
        _parse(wrapped) == {"A.kinetic_energy_conserved": {"propext", "Classical.choice", "Quot.sound"}},
        "WRAPPED footprint parses (LL-11)",
    )

    expect(_parse("'A.c' does not depend on any axioms\n") == {"A.c": set()},
           "axiom-free footprint parses as empty, not as missing")

    both = flat + wrapped
    expect(len(_parse(both)) == 2, "flat and wrapped footprints both counted in one output")

    expect(len(PRINT_AXIOMS.findall("#print axioms foo\n  #print axioms bar\n")) == 2,
           "directive counter finds indented directives")
    expect(len(PRINT_AXIOMS.findall("-- #print axioms commented\n")) == 0,
           "directive counter ignores a commented-out directive")

    return problems


def main() -> int:
    failures = self_test()
    if failures:
        print(f"FAIL  Gate 2 ({len(failures)} self-test failure(s)) — the checker is broken")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    modules = sorted(LEAN_DIR.rglob("*.lean"))
    if not modules:
        print("FAIL  Gate 2: no Lean modules found — an empty gate is not a gate")
        return 1

    for module in modules:
        failures.extend(check(module))

    if failures:
        print(f"FAIL  Gate 2 ({len(failures)} failure(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"PASS  Gate 2 ({len(modules)} module(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
