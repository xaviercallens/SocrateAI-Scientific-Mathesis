"""CLI: `python3 -m mathesis check <ledger.jsonl>`.

Output is line-oriented and deterministic so Gate 3 can diff it against the
Rust implementation byte-for-byte.

Exit codes:
    0  ledger is sound
    1  findings reported
    2  the file could not be read
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ledger import check, format_report, load_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mathesis", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    check_cmd = sub.add_parser("check", help="validate a ledger.jsonl")
    check_cmd.add_argument("path", type=Path)

    args = parser.parse_args(argv)

    if args.command == "check":
        try:
            ledger, load_findings = load_jsonl(args.path)
        except OSError as exc:
            print(f"E-IO [{args.path}] {exc}", file=sys.stderr)
            return 2
        findings = load_findings + check(ledger)
        print(format_report(findings))
        print(f"rows: {len(ledger)}  findings: {len(findings)}")
        return 1 if findings else 0

    return 2  # pragma: no cover - argparse rejects unknown commands first


if __name__ == "__main__":
    raise SystemExit(main())
