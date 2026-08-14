#!/usr/bin/env python3
"""Record a human statement-adequacy sign-off on ledger rows (PLAN.md A1).

A row is Tier A when the kernel accepts it. It becomes *citable* only when a
person has confirmed the statement is the one anyone meant — a step that does
not parallelise and cannot be delegated to a model (docs/AUDIT_PACK.md).

This script only writes the `audited_by` field. It cannot make a row Tier A, it
cannot alter a statement, and it refuses to sign a row that does not exist.

    python3 scripts/audit_signoff.py --all --by "Name, 2026-08-14"
    python3 scripts/audit_signoff.py MX-A-0001 MX-A-0003 --by "Name, 2026-08-14"
    python3 scripts/audit_signoff.py --list        # what is signed, what is not

Run ./scripts/verify.sh afterwards. Gate 4 must still pass.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / "ledger.jsonl"


def load() -> tuple[list[str], list[dict]]:
    comments, rows = [], []
    for line in LEDGER.read_text().splitlines():
        if not line.strip():
            continue
        if line.startswith("#"):
            comments.append(line)
            continue
        rows.append(json.loads(line))
    return comments, rows


def save(comments: list[str], rows: list[dict]) -> None:
    body = "\n".join(comments + [json.dumps(r) for r in rows])
    LEDGER.write_text(body + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ids", nargs="*", help="row ids to sign")
    ap.add_argument("--all", action="store_true", help="sign every Tier A row")
    ap.add_argument("--by", help='signer, e.g. "Name, 2026-08-14"')
    ap.add_argument("--list", action="store_true", help="show sign-off status")
    ap.add_argument("--revoke", action="store_true", help="clear audited_by instead")
    args = ap.parse_args()

    comments, rows = load()
    index = {r["id"]: r for r in rows}

    if args.list:
        a_rows = [r for r in rows if r["tier"] == "A"]
        signed = [r for r in a_rows if r.get("audited_by")]
        print(f"Tier A rows: {len(a_rows)}   signed: {len(signed)}   "
              f"unsigned: {len(a_rows) - len(signed)}")
        for r in a_rows:
            mark = "signed  " if r.get("audited_by") else "UNSIGNED"
            who = f"  [{r['audited_by']}]" if r.get("audited_by") else ""
            print(f"  {mark}  {r['id']}{who}")
        other = [r for r in rows if r["tier"] != "A" and r.get("audited_by")]
        for r in other:
            print(f"  signed    {r['id']} (tier {r['tier']})  [{r['audited_by']}]")
        return 0

    if args.all:
        targets = [r["id"] for r in rows if r["tier"] == "A"]
    else:
        targets = args.ids

    if not targets:
        print("no rows named; use --all, or list ids, or --list", file=sys.stderr)
        return 2

    if not args.revoke and not args.by:
        print("--by is required when signing (who is asserting adequacy?)",
              file=sys.stderr)
        return 2

    missing = [i for i in targets if i not in index]
    if missing:
        print(f"no such row(s): {', '.join(missing)}", file=sys.stderr)
        return 1

    changed = 0
    for rid in targets:
        row = index[rid]
        new = None if args.revoke else args.by
        if row.get("audited_by") != new:
            row["audited_by"] = new
            changed += 1

    save(comments, rows)
    verb = "revoked" if args.revoke else "signed"
    print(f"{verb} {changed} row(s) of {len(targets)} named")
    print("now run ./scripts/verify.sh — Gate 4 must still pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
