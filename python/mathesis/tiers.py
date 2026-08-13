"""Tier lattice — the Python mirror of `lean/Mathesis/TierCalculus.lean` §1.

This module is the reference implementation. It is deliberately written against
`SPEC.md` §2, not against the Lean file and not against the Rust crate: Gate 3
compares Python and Rust verdicts, and that comparison is worthless if either
side was written by reading the other.

Exact arithmetic only. No floats appear anywhere in this package (SPEC.md §4).
"""

from __future__ import annotations

import enum
import re
from typing import Final

__all__ = [
    "Tier",
    "STREAM_CODES",
    "CLAIM_ID_RE",
    "parse_claim_id",
    "ClaimIdError",
]


class Tier(enum.Enum):
    """Citation strength. See SPEC.md §2.1.

    The order is about how much of the checking a machine did, not about
    mathematical depth: a Tier L theorem of Bourgain is deeper than any Tier B
    rational identity in this program. Ranking L below B is a statement about
    machine confirmation only.
    """

    X = 0  # exploratory — floats, sampling, LLM output. May never be cited.
    C = 1  # conjecture, analogy, unverified reduction
    L = 2  # peer-reviewed literature, quoted theorem statement
    B = 3  # exact-arithmetic decided, with a failing negative control
    A = 4  # kernel-verified: compiles, no sorry, declared axiom footprint

    @property
    def rank(self) -> int:
        """Mirror of `Tier.rank` in the Lean core."""
        return self.value

    def __lt__(self, other: "Tier") -> bool:
        if not isinstance(other, Tier):
            return NotImplemented
        return self.rank < other.rank

    def __le__(self, other: "Tier") -> bool:
        if not isinstance(other, Tier):
            return NotImplemented
        return self.rank <= other.rank

    def __gt__(self, other: "Tier") -> bool:
        if not isinstance(other, Tier):
            return NotImplemented
        return self.rank > other.rank

    def __ge__(self, other: "Tier") -> bool:
        if not isinstance(other, Tier):
            return NotImplemented
        return self.rank >= other.rank

    @classmethod
    def from_letter(cls, letter: str) -> "Tier":
        try:
            return cls[letter]
        except KeyError:
            raise ClaimIdError(
                f'unknown tier letter "{letter}"; expected one of '
                f"{', '.join(t.name for t in cls)}"
            ) from None

    @property
    def citable(self) -> bool:
        """Tier X may never be cited (SPEC.md §2.1)."""
        return self is not Tier.X


#: Stream code -> repository short name. SPEC.md §2.5.
STREAM_CODES: Final[dict[str, str]] = {
    "MX": "Mathesis",
    "MF": "MechanicaFluidorum",
    "AE": "AutoEvolve",
    "QK": "Quantum",
    "HG": "Hypergraph",
    "RM": "RajMath",
    "TN": "TNN",
    "VD": "Videoo",
}

#: `<STREAM>-<TIER>-<NNNN>`, e.g. `MF-A-0007`.
CLAIM_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?P<stream>[A-Z]{2})-(?P<tier>[XCLBA])-(?P<seq>\d{4})$"
)


class ClaimIdError(ValueError):
    """A claim identifier is malformed, or names an unknown stream/tier."""


def parse_claim_id(claim_id: str) -> tuple[str, Tier, int]:
    """Split `MF-A-0007` into `("MF", Tier.A, 7)`.

    The tier letter lives *in* the identifier so that a stale citation elsewhere
    is lexically wrong rather than silently wrong (SPEC.md §2.5).
    """
    match = CLAIM_ID_RE.match(claim_id)
    if match is None:
        raise ClaimIdError(
            f'malformed claim id "{claim_id}"; expected <STREAM>-<TIER>-<NNNN>, '
            "e.g. MF-A-0007"
        )
    stream = match.group("stream")
    if stream not in STREAM_CODES:
        raise ClaimIdError(
            f'unknown stream code "{stream}" in "{claim_id}"; known codes: '
            f"{', '.join(sorted(STREAM_CODES))}"
        )
    return stream, Tier.from_letter(match.group("tier")), int(match.group("seq"))
