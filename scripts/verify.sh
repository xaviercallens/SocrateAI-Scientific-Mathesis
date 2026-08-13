#!/usr/bin/env bash
# Mathesis — the four-gate verification entry point (SPEC.md §5).
#
# This is the only thing that counts as "it works". Everything else is a report,
# and reports are not evidence (SPEC.md §7.6).
#
#   Gate 1  Tier B   every tests/tier_b_*.py exits 0, negative controls included
#   Gate 2  Tier A   Lean kernel-compiles; no sorry; axiom footprints as declared
#   Gate 3  Diff     Python and Rust checkers agree on every corpus case
#   Gate 4  Ledger   ledger.jsonl is sound, and LEDGER.md agrees with it
#
# Usage:  ./scripts/verify.sh [--gate N]

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ONLY_GATE=""
if [[ "${1:-}" == "--gate" ]]; then ONLY_GATE="${2:-}"; fi

RED=$'\033[31m'; GREEN=$'\033[32m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
if [[ ! -t 1 ]]; then RED=""; GREEN=""; BOLD=""; RESET=""; fi

FAILED=0
skip_gate() { [[ -n "$ONLY_GATE" && "$ONLY_GATE" != "$1" ]]; }
pass() { echo "${GREEN}PASS${RESET}  $*"; }
fail() { echo "${RED}FAIL${RESET}  $*"; FAILED=1; }
banner() { echo; echo "${BOLD}=== $* ===${RESET}"; }

# ---------------------------------------------------------------------------
# Gate 1 — Tier B
# ---------------------------------------------------------------------------
gate1() {
  banner "Gate 1 — Tier B (exact arithmetic + negative controls)"
  local harnesses found=0
  harnesses=$(find tests -name 'tier_b_*.py' -type f | sort)
  if [[ -z "$harnesses" ]]; then
    fail "Gate 1: no tier_b_*.py harness found — an empty gate is not a gate"
    return
  fi
  while IFS= read -r harness; do
    found=$((found + 1))
    if output=$(python3 "$harness" 2>&1); then
      echo "$output"
    else
      echo "$output"
      fail "Gate 1: $harness"
    fi
  done <<< "$harnesses"
  [[ $FAILED -eq 0 ]] && pass "Gate 1 ($found harness(es))"
}

# ---------------------------------------------------------------------------
# Gate 2 — Tier A
#
# The gate is the axiom footprint, not the absence of the word `sorry` in the
# source: a failed proof still defines the theorem name, and only
# `#print axioms` reveals the stray `sorryAx` (SPEC.md §7.6).
#
# Delegated to scripts/check_footprints.py, which reads each module's declared
# `MATHESIS-GATE:` contract. See that file for why the allowlist is per
# declaration rather than per file.
# ---------------------------------------------------------------------------
gate2() {
  banner "Gate 2 — Tier A (Lean kernel + declared axiom footprints)"
  if ! command -v lean >/dev/null 2>&1; then
    fail "Gate 2: lean not on PATH"
    return
  fi
  # Each module declares its own contract in `MATHESIS-GATE:` header lines:
  # which build environment it needs, and which axioms are permitted for which
  # declarations. The gate is the footprint, never a grep for `sorry`.
  if output=$(python3 scripts/check_footprints.py 2>&1); then
    echo "$output"
  else
    echo "$output"
    fail "Gate 2"
  fi
}

# ---------------------------------------------------------------------------
# Gate 3 — Differential
#
# Disagreement fails the build WITHOUT adjudicating which side is right. That
# is an E-3 escalation for a human (SPEC.md §7.3).
# ---------------------------------------------------------------------------
gate3() {
  banner "Gate 3 — Differential (Python reference vs. Rust implementation)"
  if ! command -v cargo >/dev/null 2>&1; then
    fail "Gate 3: cargo not on PATH"
    return
  fi

  if ! (cd rust/mathesis-verify && cargo build --quiet --offline 2>&1); then
    fail "Gate 3: cargo build failed"
    return
  fi
  if ! (cd rust/mathesis-verify && cargo test --quiet --offline 2>&1); then
    fail "Gate 3: cargo test failed"
    return
  fi

  local bin="rust/mathesis-verify/target/debug/mathesis-verify"
  local corpus; corpus=$(mktemp -d)
  trap 'rm -rf "$corpus"' RETURN

  python3 tests/corpus.py "$corpus" >/dev/null || { fail "Gate 3: corpus generation failed"; return; }

  local cases=0 disagreements=0
  for case_file in "$corpus"/*.jsonl; do
    cases=$((cases + 1))
    local py_out py_rc rs_out rs_rc
    py_out=$(PYTHONPATH=python python3 -m mathesis check "$case_file" 2>&1); py_rc=$?
    rs_out=$("$bin" check "$case_file" 2>&1); rs_rc=$?

    if [[ "$py_out" != "$rs_out" || "$py_rc" -ne "$rs_rc" ]]; then
      disagreements=$((disagreements + 1))
      echo "  ${RED}DISAGREEMENT${RESET} on $(basename "$case_file")"
      echo "    python (rc=$py_rc): $py_out" | head -5
      echo "    rust   (rc=$rs_rc): $rs_out" | head -5
    fi
  done

  if [[ $cases -eq 0 ]]; then
    fail "Gate 3: corpus was empty — a differential gate with no cases proves nothing"
  elif [[ $disagreements -gt 0 ]]; then
    fail "Gate 3: $disagreements/$cases case(s) disagree — file an E-3, do not pick a winner"
  else
    pass "Gate 3 ($cases corpus case(s), both implementations agree)"
  fi
}

# ---------------------------------------------------------------------------
# Gate 4 — Ledger integrity
# ---------------------------------------------------------------------------
gate4() {
  banner "Gate 4 — Ledger integrity"
  if [[ ! -f ledger.jsonl ]]; then
    fail "Gate 4: ledger.jsonl not found"
    return
  fi

  local output rc
  output=$(PYTHONPATH=python python3 -m mathesis check ledger.jsonl 2>&1); rc=$?
  echo "$output"
  if [[ $rc -ne 0 ]]; then
    fail "Gate 4: ledger.jsonl is not sound"
    return
  fi

  # Every id in the machine-readable ledger must appear in the human-readable
  # one, and vice versa. Two ledgers that drift apart are worse than one.
  local missing=0
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    if ! grep -qF "$id" LEDGER.md; then
      fail "Gate 4: $id is in ledger.jsonl but not in LEDGER.md"
      missing=1
    fi
  done < <(grep -oE '"id": *"[A-Z]{2}-[XCLBA]-[0-9]{4}"' ledger.jsonl | sed -E 's/.*"([A-Z]{2}-[XCLBA]-[0-9]{4})"/\1/')

  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    if ! grep -qF "\"$id\"" ledger.jsonl; then
      fail "Gate 4: $id is in LEDGER.md but not in ledger.jsonl"
      missing=1
    fi
  done < <(grep -oE '\b[A-Z]{2}-[XCLBA]-[0-9]{4}\b' LEDGER.md | sort -u)

  [[ $missing -eq 0 ]] && pass "Gate 4"
}

# ---------------------------------------------------------------------------

echo "${BOLD}Mathesis verification — $(date -u '+%Y-%m-%dT%H:%M:%SZ')${RESET}"
skip_gate 1 || gate1
skip_gate 2 || gate2
skip_gate 3 || gate3
skip_gate 4 || gate4

echo
if [[ $FAILED -eq 0 ]]; then
  echo "${GREEN}${BOLD}ALL GATES PASS${RESET}"
else
  echo "${RED}${BOLD}GATES FAILED${RESET} — nothing may be committed as verified"
fi
exit $FAILED
