//! `mathesis-verify` — the independent ledger checker (SPEC.md §7.3).
//!
//! This crate implements the tier calculus a second time, written against
//! `SPEC.md` §2 rather than against `python/mathesis/`. Gate 3 runs both over
//! the same corpus and fails the build if their verdicts differ, **without
//! adjudicating which side is right** — that is an E-3 escalation for a human.
//!
//! Two implementations are worth the duplication only if they are genuinely
//! independent, so: no crates.io dependencies, own JSON parser, own traversal.

pub mod json;

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

use json::Value;

/// Citation strength. Mirrors `Tier` in `lean/Mathesis/TierCalculus.lean`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Tier {
    /// Exploratory — floats, sampling, LLM output. May never be cited.
    X = 0,
    /// Conjecture, analogy, unverified reduction.
    C = 1,
    /// Peer-reviewed literature, cited to a quoted theorem statement.
    L = 2,
    /// Exact-arithmetic decided, with a failing negative control.
    B = 3,
    /// Kernel-verified: compiles, no `sorry`, declared axiom footprint.
    A = 4,
}

impl Tier {
    pub fn from_letter(letter: &str) -> Option<Tier> {
        match letter {
            "X" => Some(Tier::X),
            "C" => Some(Tier::C),
            "L" => Some(Tier::L),
            "B" => Some(Tier::B),
            "A" => Some(Tier::A),
            _ => None,
        }
    }

    pub fn letter(self) -> &'static str {
        match self {
            Tier::X => "X",
            Tier::C => "C",
            Tier::L => "L",
            Tier::B => "B",
            Tier::A => "A",
        }
    }

    /// Tier X may never be cited (SPEC.md §2.1).
    pub fn citable(self) -> bool {
        self != Tier::X
    }
}

const STREAM_CODES: [&str; 8] = ["AE", "HG", "MF", "MX", "QK", "RM", "TN", "VD"];

/// Which evidence kinds may support which tier. Mirrors `ADMISSIBLE_EVIDENCE`.
fn evidence_cap(kind: &str) -> Option<Tier> {
    match kind {
        "lean_axioms" => Some(Tier::A),
        "exact_harness" => Some(Tier::B),
        "citation" => Some(Tier::L),
        "argument" => Some(Tier::C),
        "numeric" | "llm_output" => Some(Tier::X),
        _ => None,
    }
}

fn known_evidence_kinds() -> String {
    let mut kinds = vec![
        "argument",
        "citation",
        "exact_harness",
        "lean_axioms",
        "llm_output",
        "numeric",
    ];
    kinds.sort_unstable();
    kinds.join(", ")
}

#[derive(Debug, Clone)]
pub struct Claim {
    pub id: String,
    pub tier: Tier,
    pub evidence_kind: String,
    pub supports: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Finding {
    pub code: String,
    pub claim_id: String,
    pub detail: String,
}

impl fmt::Display for Finding {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} [{}] {}", self.code, self.claim_id, self.detail)
    }
}

fn finding(code: &str, claim_id: impl Into<String>, detail: impl Into<String>) -> Finding {
    Finding { code: code.into(), claim_id: claim_id.into(), detail: detail.into() }
}

#[derive(Debug, Default)]
pub struct Ledger {
    pub claims: BTreeMap<String, Claim>,
}

/// Parse `<STREAM>-<TIER>-<NNNN>`. Returns the tier encoded in the identifier.
fn parse_claim_id(id: &str) -> Result<Tier, String> {
    let parts: Vec<&str> = id.split('-').collect();
    let malformed = || {
        format!("malformed claim id {id:?}; expected <STREAM>-<TIER>-<NNNN>, e.g. MF-A-0007")
    };
    if parts.len() != 3 {
        return Err(malformed());
    }
    let (stream, tier, seq) = (parts[0], parts[1], parts[2]);
    if stream.len() != 2 || !stream.chars().all(|c| c.is_ascii_uppercase()) {
        return Err(malformed());
    }
    if seq.len() != 4 || !seq.chars().all(|c| c.is_ascii_digit()) {
        return Err(malformed());
    }
    let tier = Tier::from_letter(tier).ok_or_else(malformed)?;
    if !STREAM_CODES.contains(&stream) {
        return Err(format!(
            "unknown stream code {stream:?} in {id:?}; known codes: {}",
            STREAM_CODES.join(", ")
        ));
    }
    Ok(tier)
}

/// Read a `ledger.jsonl`. Malformed rows become findings, not errors.
pub fn load_jsonl(text: &str) -> (Ledger, Vec<Finding>) {
    let mut ledger = Ledger::default();
    let mut findings = Vec::new();

    for (index, line) in text.lines().enumerate() {
        let lineno = index + 1;
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with('#') {
            continue;
        }
        let value = match json::parse(trimmed) {
            Ok(v) => v,
            Err(_) => {
                // Canonical message, no parser diagnostic — see the matching
                // comment in `python/mathesis/ledger.py`. The two parsers are
                // independent by design (SPEC.md §7.3), so their prose differs;
                // what Gate 3 requires them to agree on is the verdict.
                findings.push(finding("E-SCHEMA", format!("line {lineno}"), "invalid JSON"));
                continue;
            }
        };
        if !value.is_object() {
            findings.push(finding("E-SCHEMA", format!("line {lineno}"), "row is not an object"));
            continue;
        }

        let mut missing: Vec<&str> = ["evidence_kind", "id", "statement", "tier"]
            .into_iter()
            .filter(|field| value.get(field).is_none())
            .collect();
        if !missing.is_empty() {
            missing.sort_unstable();
            let id = value.get("id").and_then(Value::as_str).unwrap_or("<no id>");
            findings.push(finding(
                "E-SCHEMA",
                format!("line {lineno}"),
                format!("row {id:?} is missing required field(s): {}", missing.join(", ")),
            ));
            continue;
        }

        let id = value.get("id").and_then(Value::as_str).unwrap_or_default().to_string();
        let tier_letter = value.get("tier").and_then(Value::as_str).unwrap_or_default();
        let tier = match Tier::from_letter(tier_letter) {
            Some(t) => t,
            None => {
                findings.push(finding(
                    "E-SCHEMA",
                    format!("line {lineno}"),
                    format!("unknown tier letter {tier_letter:?}; expected one of X, C, L, B, A"),
                ));
                continue;
            }
        };

        let supports = match value.get("supports") {
            None => Vec::new(),
            Some(Value::Array(items)) => {
                if items.iter().any(|i| i.as_str().is_none()) {
                    findings.push(finding(
                        "E-SCHEMA",
                        format!("line {lineno}"),
                        format!("row {id:?}: `supports` must be a list of strings"),
                    ));
                    continue;
                }
                items.iter().map(|i| i.as_str().unwrap().to_string()).collect()
            }
            Some(_) => {
                findings.push(finding(
                    "E-SCHEMA",
                    format!("line {lineno}"),
                    format!("row {id:?}: `supports` must be a list of strings"),
                ));
                continue;
            }
        };

        let id_tier = match parse_claim_id(&id) {
            Ok(t) => t,
            Err(message) => {
                findings.push(finding("E-SCHEMA", id.clone(), message));
                continue;
            }
        };

        if id_tier != tier {
            findings.push(finding(
                "E-TIERMATCH",
                id.clone(),
                format!(
                    "identifier says tier {}, `tier` field says {}; a promotion must change the \
                     identifier (SPEC.md §2.5)",
                    id_tier.letter(),
                    tier.letter()
                ),
            ));
            continue;
        }

        if ledger.claims.contains_key(&id) {
            findings.push(finding("E-DUP", id.clone(), format!("duplicate row at line {lineno}")));
            continue;
        }

        let evidence_kind =
            value.get("evidence_kind").and_then(Value::as_str).unwrap_or_default().to_string();
        ledger.claims.insert(id.clone(), Claim { id, tier, evidence_kind, supports });
    }

    (ledger, findings)
}

impl Ledger {
    /// Everything reachable from `start` through `supports`. Iterative, so a
    /// deep or adversarial ledger is reported rather than overflowing the stack.
    pub fn depends(&self, start: &str) -> BTreeSet<String> {
        let mut seen = BTreeSet::new();
        let mut stack: Vec<String> = match self.claims.get(start) {
            Some(claim) => claim.supports.clone(),
            None => Vec::new(),
        };
        while let Some(current) = stack.pop() {
            if !seen.insert(current.clone()) {
                continue;
            }
            if let Some(claim) = self.claims.get(&current) {
                stack.extend(claim.supports.iter().cloned());
            }
        }
        seen
    }
}

/// Run every structural check. An empty result means the ledger is sound.
pub fn check(ledger: &Ledger) -> Vec<Finding> {
    let mut findings = Vec::new();

    for claim in ledger.claims.values() {
        match evidence_cap(&claim.evidence_kind) {
            None => findings.push(finding(
                "E-EVIDENCE",
                &claim.id,
                format!(
                    "unknown evidence kind {:?}; known kinds: {}",
                    claim.evidence_kind,
                    known_evidence_kinds()
                ),
            )),
            Some(cap) if claim.tier > cap => findings.push(finding(
                "E-EVIDENCE",
                &claim.id,
                format!(
                    "filed at tier {} but evidence kind {:?} supports at most tier {}",
                    claim.tier.letter(),
                    claim.evidence_kind,
                    cap.letter()
                ),
            )),
            Some(_) => {}
        }
    }

    for claim in ledger.claims.values() {
        for support in &claim.supports {
            if !ledger.claims.contains_key(support) {
                findings.push(finding(
                    "E-DANGLING",
                    &claim.id,
                    format!("cites {support:?}, which has no row in this ledger"),
                ));
            }
        }
    }

    for claim in ledger.claims.values() {
        for support in &claim.supports {
            if let Some(cited) = ledger.claims.get(support) {
                if !cited.tier.citable() {
                    findings.push(finding(
                        "E-UNCITABLE",
                        &claim.id,
                        format!(
                            "cites {support:?}, which is Tier X; Tier X may never be cited \
                             (SPEC.md §2.1)"
                        ),
                    ));
                }
            }
        }
    }

    let mut cycle_found = false;
    let mut reported: Vec<BTreeSet<String>> = Vec::new();
    for id in ledger.claims.keys() {
        let reachable = ledger.depends(id);
        if reachable.contains(id) {
            cycle_found = true;
            let mut loop_members: BTreeSet<String> = BTreeSet::new();
            loop_members.insert(id.clone());
            for other in &reachable {
                if ledger.depends(other).contains(id) {
                    loop_members.insert(other.clone());
                }
            }
            if reported.contains(&loop_members) {
                continue;
            }
            reported.push(loop_members.clone());
            let members: Vec<&str> = loop_members.iter().map(String::as_str).collect();
            findings.push(finding(
                "E-CYCLE",
                id,
                format!("support graph has a cycle through {{{}}}", members.join(", ")),
            ));
        }
    }

    // Soundness over the transitive closure is only meaningful on an acyclic
    // graph — on a cycle every node reaches every other and the report becomes
    // derived noise hiding the one real defect.
    if !cycle_found {
        for claim in ledger.claims.values() {
            for support_id in ledger.depends(&claim.id) {
                let Some(support) = ledger.claims.get(&support_id) else { continue };
                if claim.tier > support.tier {
                    let direct = claim.supports.contains(&support_id);
                    findings.push(finding(
                        "E-UNSOUND",
                        &claim.id,
                        format!(
                            "filed at tier {} but {} {} at tier {}",
                            claim.tier.letter(),
                            if direct { "cites" } else { "transitively rests on" },
                            support_id,
                            support.tier.letter()
                        ),
                    ));
                }
            }
        }
    }

    findings
}

/// Deterministic, sorted, no adjectives (PLAN.md §2). Must match the Python
/// `format_report` byte-for-byte — Gate 3 diffs the two.
pub fn format_report(findings: &[Finding]) -> String {
    if findings.is_empty() {
        return "OK".to_string();
    }
    let mut sorted = findings.to_vec();
    sorted.sort();
    sorted.iter().map(Finding::to_string).collect::<Vec<_>>().join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    const SOUND: &str = r#"
{"id":"MX-A-0001","tier":"A","statement":"head","evidence_kind":"lean_axioms","supports":["MX-A-0002"]}
{"id":"MX-A-0002","tier":"A","statement":"base","evidence_kind":"lean_axioms","supports":[]}
"#;

    #[test]
    fn sound_ledger_has_no_findings() {
        let (ledger, load) = load_jsonl(SOUND);
        assert!(load.is_empty());
        assert_eq!(ledger.claims.len(), 2);
        assert!(check(&ledger).is_empty());
        assert_eq!(format_report(&check(&ledger)), "OK");
    }

    #[test]
    fn kernel_claim_on_a_conjecture_is_unsound() {
        let text = r#"
{"id":"MX-A-0001","tier":"A","statement":"head","evidence_kind":"lean_axioms","supports":["MX-C-0002"]}
{"id":"MX-C-0002","tier":"C","statement":"guess","evidence_kind":"argument","supports":[]}
"#;
        let (ledger, _) = load_jsonl(text);
        let findings = check(&ledger);
        assert!(findings.iter().any(|f| f.code == "E-UNSOUND"));
    }

    /// The transitive case: every *direct* edge is fine, but the head still
    /// rests on literature two hops down. This is the whole point of the Lean
    /// theorem, so it is the test that must not be allowed to rot.
    #[test]
    fn transitive_leak_is_caught() {
        let text = r#"
{"id":"MX-B-0001","tier":"B","statement":"head","evidence_kind":"exact_harness","supports":["MX-B-0002"]}
{"id":"MX-B-0002","tier":"B","statement":"mid","evidence_kind":"exact_harness","supports":["MX-L-0003"]}
{"id":"MX-L-0003","tier":"L","statement":"cited","evidence_kind":"citation","supports":[]}
"#;
        let (ledger, _) = load_jsonl(text);
        let findings = check(&ledger);
        let unsound: Vec<&Finding> = findings.iter().filter(|f| f.code == "E-UNSOUND").collect();
        assert_eq!(unsound.len(), 2, "head and mid both outrank the literature row");
        assert!(unsound.iter().any(|f| f.detail.contains("transitively rests on")));
    }

    #[test]
    fn evidence_kind_caps_the_tier() {
        let text = r#"
{"id":"MX-A-0001","tier":"A","statement":"overclaim","evidence_kind":"citation","supports":[]}
"#;
        let (ledger, _) = load_jsonl(text);
        assert!(check(&ledger).iter().any(|f| f.code == "E-EVIDENCE"));
    }

    #[test]
    fn identifier_tier_must_match_the_field() {
        let text = r#"
{"id":"MX-A-0001","tier":"C","statement":"mismatch","evidence_kind":"argument","supports":[]}
"#;
        let (_, load) = load_jsonl(text);
        assert!(load.iter().any(|f| f.code == "E-TIERMATCH"));
    }

    #[test]
    fn cycles_are_reported_and_suppress_soundness_noise() {
        let text = r#"
{"id":"MX-A-0001","tier":"A","statement":"a","evidence_kind":"lean_axioms","supports":["MX-A-0002"]}
{"id":"MX-A-0002","tier":"A","statement":"b","evidence_kind":"lean_axioms","supports":["MX-A-0001"]}
"#;
        let (ledger, _) = load_jsonl(text);
        let findings = check(&ledger);
        assert!(findings.iter().any(|f| f.code == "E-CYCLE"));
        assert!(!findings.iter().any(|f| f.code == "E-UNSOUND"));
    }

    #[test]
    fn tier_x_may_not_be_cited() {
        let text = r#"
{"id":"MX-C-0001","tier":"C","statement":"rests on a plot","evidence_kind":"argument","supports":["MX-X-0002"]}
{"id":"MX-X-0002","tier":"X","statement":"a plot","evidence_kind":"numeric","supports":[]}
"#;
        let (ledger, _) = load_jsonl(text);
        assert!(check(&ledger).iter().any(|f| f.code == "E-UNCITABLE"));
    }
}
