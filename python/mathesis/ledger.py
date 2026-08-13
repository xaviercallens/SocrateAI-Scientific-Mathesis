"""Ledger loading and checking — the Python mirror of the Lean `Sound` predicate.

The checks implemented here, in order of what they catch:

    E-SCHEMA     a row is malformed, or an id is not `<STREAM>-<TIER>-<NNNN>`
    E-DUP        two rows share an id
    E-DANGLING   a row cites an id that has no row
    E-TIERMATCH  a row's tier letter disagrees with its `tier` field
    E-EVIDENCE   a row's evidence kind is not admissible at its tier
    E-CYCLE      the support graph has a cycle
    E-UNSOUND    a row is filed above something it (transitively) rests on
    E-UNCITABLE  a row cites a Tier X row

`E-UNSOUND` is reported over the **transitive** closure, which is the content of
`tier_le_of_depends` in the Lean core. Everything else is bookkeeping hygiene
that has to hold before the theorem's hypotheses even make sense.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

from .tiers import ClaimIdError, Tier, parse_claim_id

__all__ = [
    "Claim",
    "Ledger",
    "Finding",
    "ADMISSIBLE_EVIDENCE",
    "load_jsonl",
    "check",
]

#: Which evidence kinds may support which tier (SPEC.md §2.1).
#:
#: A row's tier is capped by what its evidence can establish. A `lean_axioms`
#: row may be filed at A; a `citation` row may not be filed above L, however
#: distinguished the source. This is the mechanical half of the Tier B/L
#: collision fix (docs/TIER_CALCULUS.md).
ADMISSIBLE_EVIDENCE: dict[str, Tier] = {
    "lean_axioms": Tier.A,      # #print axioms footprint matching a declared allowlist
    "exact_harness": Tier.B,    # deterministic ℚ/ℤ check with a failing negative control
    "citation": Tier.L,         # peer-reviewed, quoted theorem statement
    "argument": Tier.C,         # prose derivation, analogy, proposal
    "numeric": Tier.X,          # floats, sampling, plots
    "llm_output": Tier.X,       # never above X, by charter (SPEC.md §0)
}


@dataclass(frozen=True)
class Claim:
    """One ledger row."""

    id: str
    tier: Tier
    statement: str
    evidence_kind: str
    supports: tuple[str, ...] = ()
    artifact: str | None = None
    stream: str | None = None
    audited_by: str | None = None
    supersedes: str | None = None

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "Claim":
        missing = {"id", "tier", "statement", "evidence_kind"} - raw.keys()
        if missing:
            raise ClaimIdError(
                'row "' + str(raw.get('id', '<no id>')) + '" is missing required field(s): '
                f"{', '.join(sorted(missing))}"
            )
        supports = raw.get("supports", [])
        if not isinstance(supports, list) or not all(isinstance(s, str) for s in supports):
            raise ClaimIdError('row "' + str(raw["id"]) + '": `supports` must be a list of strings')
        return Claim(
            id=raw["id"],
            tier=Tier.from_letter(raw["tier"]),
            statement=raw["statement"],
            evidence_kind=raw["evidence_kind"],
            supports=tuple(supports),
            artifact=raw.get("artifact"),
            stream=raw.get("stream"),
            audited_by=raw.get("audited_by"),
            supersedes=raw.get("supersedes"),
        )


@dataclass(frozen=True)
class Finding:
    """A single problem with a ledger. `code` is one of the E-* codes above."""

    code: str
    claim_id: str
    detail: str

    def __str__(self) -> str:  # pragma: no cover - formatting only
        return f"{self.code} [{self.claim_id}] {self.detail}"


@dataclass
class Ledger:
    """A collection of rows, indexed by id."""

    claims: dict[str, Claim] = field(default_factory=dict)

    def __iter__(self) -> Iterator[Claim]:
        return iter(self.claims.values())

    def __len__(self) -> int:
        return len(self.claims)

    def depends(self, start: str) -> Iterator[str]:
        """Every id reachable from `start` through `supports`, excluding `start`
        itself unless a cycle leads back to it.

        This is the transitive closure the Lean `Depends` relation describes.
        Iterative rather than recursive: a ledger is a data file, and a deep or
        adversarial one must not blow the Python stack instead of being reported.
        """
        seen: set[str] = set()
        stack = list(self.claims[start].supports) if start in self.claims else []
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            yield current
            claim = self.claims.get(current)
            if claim is not None:
                stack.extend(claim.supports)


def load_jsonl(path: Path | str) -> tuple[Ledger, list[Finding]]:
    """Read a `ledger.jsonl`. Malformed rows become findings, not exceptions —
    the caller wants every problem in one pass, not the first one.
    """
    ledger = Ledger()
    findings: list[Finding] = []
    text = Path(path).read_text(encoding="utf-8")

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            raw = json.loads(stripped)
        except json.JSONDecodeError:
            # The message is deliberately canonical and carries no parser
            # diagnostic. Gate 3 compares this output byte-for-byte against the
            # Rust checker, which has its own hand-written parser; their prose
            # for the same malformed row will never coincide, and forcing it to
            # would mean one implementation copying the other's strings —
            # exactly the shared dependency SPEC.md §7.3 forbids. What must
            # agree is the *verdict*: this row is not admissible.
            findings.append(Finding("E-SCHEMA", f"line {lineno}", "invalid JSON"))
            continue
        if not isinstance(raw, dict):
            findings.append(Finding("E-SCHEMA", f"line {lineno}", "row is not an object"))
            continue
        try:
            claim = Claim.from_dict(raw)
        except ClaimIdError as exc:
            findings.append(Finding("E-SCHEMA", f"line {lineno}", str(exc)))
            continue

        try:
            _, id_tier, _ = parse_claim_id(claim.id)
        except ClaimIdError as exc:
            findings.append(Finding("E-SCHEMA", claim.id, str(exc)))
            continue

        if id_tier is not claim.tier:
            findings.append(
                Finding(
                    "E-TIERMATCH",
                    claim.id,
                    f"identifier says tier {id_tier.name}, `tier` field says "
                    f"{claim.tier.name}; a promotion must change the identifier "
                    "(SPEC.md §2.5)",
                )
            )
            continue

        if claim.id in ledger.claims:
            findings.append(Finding("E-DUP", claim.id, f"duplicate row at line {lineno}"))
            continue

        ledger.claims[claim.id] = claim

    return ledger, findings


def check(ledger: Ledger) -> list[Finding]:
    """Run every structural check. Empty result == the ledger is sound."""
    findings: list[Finding] = []
    findings.extend(_check_evidence(ledger))
    findings.extend(_check_dangling(ledger))
    findings.extend(_check_uncitable(ledger))
    cycles = list(_check_cycles(ledger))
    findings.extend(cycles)
    # Soundness over the transitive closure is only meaningful on an acyclic
    # graph — on a cycle every node reaches every other, so the report would be
    # a wall of derived noise hiding the one real defect.
    if not cycles:
        findings.extend(_check_sound(ledger))
    return findings


def _check_evidence(ledger: Ledger) -> Iterable[Finding]:
    for claim in ledger:
        cap = ADMISSIBLE_EVIDENCE.get(claim.evidence_kind)
        if cap is None:
            yield Finding(
                "E-EVIDENCE",
                claim.id,
                f'unknown evidence kind "{claim.evidence_kind}"; known kinds: '
                f"{', '.join(sorted(ADMISSIBLE_EVIDENCE))}",
            )
        elif claim.tier > cap:
            yield Finding(
                "E-EVIDENCE",
                claim.id,
                f"filed at tier {claim.tier.name} but evidence kind "
                f'"{claim.evidence_kind}" supports at most tier {cap.name}',
            )


def _check_dangling(ledger: Ledger) -> Iterable[Finding]:
    for claim in ledger:
        for support in claim.supports:
            if support not in ledger.claims:
                yield Finding(
                    "E-DANGLING",
                    claim.id,
                    f'cites "{support}", which has no row in this ledger',
                )


def _check_uncitable(ledger: Ledger) -> Iterable[Finding]:
    for claim in ledger:
        for support in claim.supports:
            cited = ledger.claims.get(support)
            if cited is not None and not cited.tier.citable:
                yield Finding(
                    "E-UNCITABLE",
                    claim.id,
                    f'cites "{support}", which is Tier X; Tier X may never be '
                    "cited (SPEC.md §2.1)",
                )


def _check_cycles(ledger: Ledger) -> Iterable[Finding]:
    """Report each cycle once, at its lexicographically smallest member."""
    reported: set[frozenset[str]] = set()
    for claim in sorted(ledger.claims):
        reachable = set(ledger.depends(claim))
        if claim in reachable:
            loop = frozenset({claim} | {r for r in reachable if claim in set(ledger.depends(r))})
            if loop in reported:
                continue
            reported.add(loop)
            yield Finding(
                "E-CYCLE",
                claim,
                f"support graph has a cycle through {{{', '.join(sorted(loop))}}}",
            )


def _check_sound(ledger: Ledger) -> Iterable[Finding]:
    """The mechanised content of `tier_le_of_depends`.

    Direct edges alone are not enough: a chain A -> A -> L is sound at no direct
    edge, but a chain B -> B -> L is sound at every direct edge and still means
    the head rests on literature. The Lean theorem says the transitive check is
    implied by the direct one *when the ledger is sound*; this function is what
    establishes that hypothesis, so it checks the closure directly.
    """
    for claim in ledger:
        for support_id in ledger.depends(claim.id):
            support = ledger.claims.get(support_id)
            if support is None:
                continue  # already reported as E-DANGLING
            if claim.tier > support.tier:
                direct = support_id in claim.supports
                yield Finding(
                    "E-UNSOUND",
                    claim.id,
                    f"filed at tier {claim.tier.name} but "
                    f"{'cites' if direct else 'transitively rests on'} "
                    f"{support_id} at tier {support.tier.name}",
                )


def format_report(findings: Sequence[Finding]) -> str:
    """Deterministic, sorted, no adjectives (PLAN.md §2)."""
    if not findings:
        return "OK"
    return "\n".join(str(f) for f in sorted(findings, key=lambda f: (f.code, f.claim_id)))
