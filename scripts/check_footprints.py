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

#: Where the shared Mathlib build lives. Override with LEAN_ENV_DIR.
#: This is a cross-stream dependency and a known fragility (PLAN.md K1).
DEFAULT_ENV = Path.home() / "xdev/SocrateAI-Scientific-RajMathRecovery/dualscale/lean"

DIRECTIVE = re.compile(r"MATHESIS-GATE:\s*(\w+)(?:\(([^)]*)\))?\s*=\s*(.*)")
FOOTPRINT = re.compile(r"^'(?P<decl>[^']+)' (?:depends on axioms: \[(?P<axioms>[^\]]*)\]|(?P<none>does not depend on any axioms))")


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
        env_dir = Path(os.environ.get("LEAN_ENV_DIR", DEFAULT_ENV))
        if not env_dir.is_dir():
            return 127, f"LEAN_ENV_DIR not found: {env_dir}"
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
    for line in output.splitlines():
        match = FOOTPRINT.match(line.strip())
        if match is None:
            continue
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

    if printed == 0:
        failures.append(f"{rel}: printed no axiom footprints — add `#print axioms` lines")
    elif not failures:
        print(f"  {rel}: {printed} footprint(s) as declared (env={contract.env})")

    return failures


def main() -> int:
    modules = sorted(LEAN_DIR.rglob("*.lean"))
    if not modules:
        print("FAIL  Gate 2: no Lean modules found — an empty gate is not a gate")
        return 1

    failures: list[str] = []
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
