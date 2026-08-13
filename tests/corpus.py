"""Deterministic corpus of ledgers for the differential gate (SPEC.md §5, Gate 3).

Every case is written out as a `.jsonl` file, then fed to both the Python and
the Rust checker. The two must agree on every verdict.

Determinism is not decoration: `PLAN.md` §2 bans wall-clock and unseeded
randomness in anything a gate depends on. These cases are enumerated by hand so
that a Gate 3 failure names a specific, reproducible file.

The corpus deliberately includes cases where the *expected* verdict is a
finding. A differential gate that only ever compares "OK" to "OK" is the
checker-that-cannot-fail of SPEC.md §7.2, one level up.
"""

from __future__ import annotations

import json
from pathlib import Path

__all__ = ["CASES", "write_corpus"]


def _row(
    claim_id: str,
    tier: str,
    evidence: str,
    supports: list[str] | None = None,
    statement: str = "s",
) -> str:
    return json.dumps(
        {
            "id": claim_id,
            "tier": tier,
            "statement": statement,
            "evidence_kind": evidence,
            "supports": supports or [],
        },
        sort_keys=True,
    )


#: name -> file contents. Names double as filenames, so keep them path-safe.
CASES: dict[str, str] = {
    # --- cases that must come back OK -------------------------------------
    "empty": "",
    "comments_and_blank_lines": "\n# a comment\n\n",
    "single_kernel_row": _row("MX-A-0001", "A", "lean_axioms"),
    "kernel_chain": "\n".join(
        [
            _row("MX-A-0001", "A", "lean_axioms", ["MX-A-0002"]),
            _row("MX-A-0002", "A", "lean_axioms", ["MX-A-0003"]),
            _row("MX-A-0003", "A", "lean_axioms"),
        ]
    ),
    "descending_tiers_are_fine": "\n".join(
        [
            _row("MX-C-0001", "C", "argument", ["MX-L-0002"]),
            _row("MX-L-0002", "L", "citation", ["MX-B-0003"]),
            _row("MX-B-0003", "B", "exact_harness", ["MX-A-0004"]),
            _row("MX-A-0004", "A", "lean_axioms"),
        ]
    ),
    "diamond": "\n".join(
        [
            _row("MX-B-0001", "B", "exact_harness", ["MX-B-0002", "MX-B-0003"]),
            _row("MX-B-0002", "B", "exact_harness", ["MX-A-0004"]),
            _row("MX-B-0003", "B", "exact_harness", ["MX-A-0004"]),
            _row("MX-A-0004", "A", "lean_axioms"),
        ]
    ),
    "cross_stream": "\n".join(
        [
            _row("MF-A-0001", "A", "lean_axioms", ["MX-A-0001"]),
            _row("MX-A-0001", "A", "lean_axioms"),
        ]
    ),
    # --- cases that must produce findings ---------------------------------
    "unsound_direct": "\n".join(
        [
            _row("MX-A-0001", "A", "lean_axioms", ["MX-C-0002"]),
            _row("MX-C-0002", "C", "argument"),
        ]
    ),
    "unsound_transitive": "\n".join(
        [
            _row("MX-B-0001", "B", "exact_harness", ["MX-B-0002"]),
            _row("MX-B-0002", "B", "exact_harness", ["MX-L-0003"]),
            _row("MX-L-0003", "L", "citation"),
        ]
    ),
    "unsound_deep_chain": "\n".join(
        [_row("MX-A-0001", "A", "lean_axioms", ["MX-A-0002"])]
        + [_row(f"MX-A-{i:04d}", "A", "lean_axioms", [f"MX-A-{i + 1:04d}"]) for i in range(2, 40)]
        + [_row("MX-A-0040", "A", "lean_axioms", ["MX-X-0041"]), _row("MX-X-0041", "X", "numeric")]
    ),
    "cycle_two": "\n".join(
        [
            _row("MX-A-0001", "A", "lean_axioms", ["MX-A-0002"]),
            _row("MX-A-0002", "A", "lean_axioms", ["MX-A-0001"]),
        ]
    ),
    "cycle_self": _row("MX-A-0001", "A", "lean_axioms", ["MX-A-0001"]),
    "cycle_three": "\n".join(
        [
            _row("MX-B-0001", "B", "exact_harness", ["MX-B-0002"]),
            _row("MX-B-0002", "B", "exact_harness", ["MX-B-0003"]),
            _row("MX-B-0003", "B", "exact_harness", ["MX-B-0001"]),
        ]
    ),
    "dangling": _row("MX-A-0001", "A", "lean_axioms", ["MX-A-9999"]),
    "duplicate": "\n".join(
        [_row("MX-A-0001", "A", "lean_axioms"), _row("MX-A-0001", "A", "lean_axioms")]
    ),
    "tier_letter_mismatch": _row("MX-A-0001", "C", "argument"),
    "evidence_overclaim_citation_at_A": _row("MX-A-0001", "A", "citation"),
    "evidence_overclaim_llm_at_B": _row("MX-B-0001", "B", "llm_output"),
    "evidence_unknown_kind": _row("MX-A-0001", "A", "haruspicy"),
    "tier_x_cited": "\n".join(
        [
            _row("MX-C-0001", "C", "argument", ["MX-X-0002"]),
            _row("MX-X-0002", "X", "numeric"),
        ]
    ),
    "unknown_stream_code": _row("ZZ-A-0001", "A", "lean_axioms"),
    "malformed_id_short_seq": _row("MX-A-1", "A", "lean_axioms"),
    "malformed_id_no_tier": _row("MXA0001", "A", "lean_axioms"),
    "missing_fields": json.dumps({"id": "MX-A-0001", "tier": "A"}, sort_keys=True),
    "supports_not_a_list": json.dumps(
        {
            "id": "MX-A-0001",
            "tier": "A",
            "statement": "s",
            "evidence_kind": "lean_axioms",
            "supports": "MX-A-0002",
        },
        sort_keys=True,
    ),
    "supports_contains_non_string": json.dumps(
        {
            "id": "MX-A-0001",
            "tier": "A",
            "statement": "s",
            "evidence_kind": "lean_axioms",
            "supports": [7],
        },
        sort_keys=True,
    ),
    "invalid_json": '{"id": "MX-A-0001", ',
    "row_is_an_array": "[1, 2, 3]",
    "unknown_tier_letter": json.dumps(
        {"id": "MX-A-0001", "tier": "Q", "statement": "s", "evidence_kind": "lean_axioms"},
        sort_keys=True,
    ),
    "mixed_valid_and_invalid": "\n".join(
        [
            _row("MX-A-0001", "A", "lean_axioms"),
            "{ this is not json",
            _row("MX-C-0002", "C", "argument", ["MX-A-0001"]),
        ]
    ),
}


def write_corpus(directory: Path) -> list[Path]:
    """Materialise every case into `directory`. Returns the paths, sorted."""
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for name, contents in sorted(CASES.items()):
        path = directory / f"{name}.jsonl"
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("corpus")
    paths = write_corpus(target)
    print(f"wrote {len(paths)} cases to {target}")
