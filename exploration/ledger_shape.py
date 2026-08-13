# TIER X — EXPLORATORY, NO CLAIMS
"""Shape statistics of a ledger. Floats permitted here and nowhere else.

This file exists partly to do a small useful thing and partly to make the
Tier X machinery non-vacuous: `tests/tier_b_no_floats.py` exempts this directory
but requires the banner above, and an exemption that nothing exercises is an
exemption nobody notices has broken.

Nothing here may support a ledger row. Ratios below are float arithmetic and are
Tier X by construction — they may steer a decision about where to look, never
justify a claim about what is known.

    python3 exploration/ledger_shape.py ledger.jsonl
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from mathesis.ledger import load_jsonl  # noqa: E402
from mathesis.tiers import Tier  # noqa: E402


def main(path: str) -> int:
    ledger, findings = load_jsonl(Path(path))
    if findings:
        print(f"{len(findings)} load finding(s); shape below is of what parsed")

    tiers = Counter(claim.tier for claim in ledger)
    total = len(ledger)
    if total == 0:
        print("empty ledger")
        return 0

    print(f"rows: {total}")
    for tier in [Tier.A, Tier.B, Tier.L, Tier.C, Tier.X]:
        count = tiers[tier]
        share = 100.0 * count / total
        print(f"  {tier.name}: {count:3d}  ({share:5.1f}%)")

    cited = Counter()
    for claim in ledger:
        for support in claim.supports:
            cited[support] += 1

    leaves = [c.id for c in ledger if not c.supports]
    unused = [c.id for c in ledger if cited[c.id] == 0]

    print(f"\nleaves (rest on nothing):  {len(leaves)}")
    print(f"uncited (nothing rests on them): {len(unused)}")

    # The question worth asking of a real ledger: which Tier A results is the
    # program not actually using? A high count here is not a defect, but it is
    # a hint about where effort went versus where it was needed.
    unused_kernel = [c.id for c in ledger if c.tier is Tier.A and cited[c.id] == 0]
    if unused_kernel:
        print(f"uncited Tier A rows: {', '.join(sorted(unused_kernel))}")

    if cited:
        depth = max(len(set(ledger.depends(c.id))) for c in ledger)
        print(f"deepest transitive support set: {depth}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "ledger.jsonl"))
