//! CLI: `mathesis-verify check <ledger.jsonl>`.
//!
//! Output must match `python3 -m mathesis check` byte-for-byte; Gate 3 diffs
//! them. Exit codes: 0 sound, 1 findings, 2 unreadable file.

use std::process::ExitCode;

use mathesis_verify::{check, format_report, load_jsonl};

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 || args[1] != "check" {
        eprintln!("usage: mathesis-verify check <ledger.jsonl>");
        return ExitCode::from(2);
    }

    let path = &args[2];
    let text = match std::fs::read_to_string(path) {
        Ok(text) => text,
        Err(e) => {
            eprintln!("E-IO [{path}] {e}");
            return ExitCode::from(2);
        }
    };

    let (ledger, load_findings) = load_jsonl(&text);
    let mut findings = load_findings;
    findings.extend(check(&ledger));

    println!("{}", format_report(&findings));
    println!("rows: {}  findings: {}", ledger.claims.len(), findings.len());

    if findings.is_empty() { ExitCode::SUCCESS } else { ExitCode::from(1) }
}
