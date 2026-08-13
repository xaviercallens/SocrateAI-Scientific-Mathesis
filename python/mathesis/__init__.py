"""Mathesis — Stream 0 of SocrateAI.

The shared formal notation, verification kernel, and epistemic bookkeeping used
by the other streams. This package ships the *reference* implementation of the
tier calculus; `rust/mathesis-verify` ships an independent one, and Gate 3
compares them (SPEC.md §7.3).

Nothing in this package licenses a scientific claim (SPEC.md §7.9).
"""

from .ledger import Claim, Finding, Ledger, check, load_jsonl
from .tiers import STREAM_CODES, ClaimIdError, Tier, parse_claim_id

__version__ = "0.1.0"

__all__ = [
    "Claim",
    "Finding",
    "Ledger",
    "Tier",
    "STREAM_CODES",
    "ClaimIdError",
    "check",
    "load_jsonl",
    "parse_claim_id",
    "__version__",
]
