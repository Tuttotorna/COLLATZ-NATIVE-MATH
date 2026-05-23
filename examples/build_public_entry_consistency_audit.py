#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.7

Public Entry Consistency Audit.

This builder audits the public entry layer after v4.6.

It checks README.md, START_HERE.md, CRC_CONJECTURE.md, and public brief artifacts.

It does not add theory.
It does not prove Collatz.
It does not claim Collatz is solved.
It does not claim global closure.
It does not claim global invariance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v4.7"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

README_PATH = ROOT / "README.md"
START_HERE_PATH = ROOT / "START_HERE.md"
CRC_PATH = ROOT / "CRC_CONJECTURE.md"

SHORTFORM_MARKER = "<!-- V4.6_PUBLIC_README_SHORTFORM -->"

SOURCE_SHORTFORM_CERTIFICATE = RESULTS_DIR / "public_readme_shortform_certificate.json"
SOURCE_PUBLIC_BRIEF_CERTIFICATE = RESULTS_DIR / "native_public_research_brief_certificate.json"
SOURCE_CONSOLIDATION_CERTIFICATE = RESULTS_DIR / "native_audit_report_consolidation_certificate.json"

OUTPUT_JSON = RESULTS_DIR / "public_entry_consistency_audit.json"
OUTPUT_MD = RESULTS_DIR / "public_entry_consistency_audit.md"
OUTPUT_CERTIFICATE = RESULTS_DIR / "public_entry_consistency_audit_certificate.json"

FORBIDDEN_STANDALONE_CLAIMS = [
    "Collatz is solved.",
    "We solved Collatz.",
    "Proof of Collatz.",
    "Collatz proof complete.",
    "Global closure is proved.",
    "Global invariant is proved.",
    "Obstruction is impossible.",
    "Bounded evidence implies theorem.",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def is_standalone_assertive_claim(text: str, phrase: str) -> bool:
    target = phrase.lower().strip().strip("`*_ .:").rstrip(".").strip()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        lower = line.lower().strip()

        if not lower:
            continue

        if lower.startswith(("-", "*", ">", "`", "#")):
            continue

        normalized = lower.strip("`*_ .:").rstrip(".").strip()

        if normalized == target:
            return True

    return False


def find_forbidden_claims(text: str) -> List[str]:
    return [
        phrase
        for phrase in FORBIDDEN_STANDALONE_CLAIMS
        if is_standalone_assertive_claim(text, phrase)
    ]


def audit_text_file(path: Path, required_phrases: List[str]) -> Dict[str, Any]:
    text = read_text(path)

    missing_required = [
        phrase
        for phrase in required_phrases
        if phrase not in text
    ]

    forbidden_found = find_forbidden_claims(text)

    passes = path.exists() and not missing_required and not forbidden_found

    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "missing_required_phrases": missing_required,
        "forbidden_found": forbidden_found,
        "passes": passes,
    }


def audit_public_entry() -> Dict[str, Any]:
    readme_required = [
        SHORTFORM_MARKER,
        "## Public shortform",
        "COLLATZ-NATIVE-MATH is a native structural reading of Collatz dynamics.",
        "What is Collatz before it becomes a conjecture?",
        "No solution before native language.",
        "results/native_public_research_brief.md",
        "results/native_audit_report_consolidation.md",
        "proof_status: not_a_proof",
        "collatz_status: not_claimed_solved",
        "global_closure_status: not_claimed",
        "global_invariant_status: not_claimed",
    ]

    start_here_required = [
        "v4.6 public README shortform",
        "No solution before native language.",
        "results/public_readme_shortform.md",
        "docs/PUBLIC_README_SHORTFORM.md",
    ]

    crc_required = [
        "Public README shortform",
        "no solution before native language",
        "README shortform != proof",
        "README shortform != theorem",
        "README shortform != Collatz solved",
    ]

    rows = [
        audit_text_file(README_PATH, readme_required),
        audit_text_file(START_HERE_PATH, start_here_required),
        audit_text_file(CRC_PATH, crc_required),
    ]

    failures = [
        row for row in rows
        if not row["passes"]
    ]

    return {
        "entry_file_count": len(rows),
        "entry_files_passing": sum(1 for row in rows if row["passes"]),
        "entry_failure_count": len(failures),
        "entry_failures": failures,
        "entry_rows": rows,
    }


def audit_artifact_links() -> Dict[str, Any]:
    required_artifacts = [
        "results/public_readme_shortform.json",
        "results/public_readme_shortform.md",
        "results/public_readme_shortform_certificate.json",
        "results/native_public_research_brief.md",
        "results/native_public_research_brief_certificate.json",
        "results/native_audit_report_consolidation.md",
        "results/native_audit_report_consolidation_certificate.json",
    ]

    rows: List[Dict[str, Any]] = []

    for rel in required_artifacts:
        path = ROOT / rel
        rows.append({
            "path": rel,
            "exists": path.exists(),
        })

    missing = [
        row for row in rows
        if not row["exists"]
    ]

    return {
        "artifact_count": len(rows),
        "artifact_existing_count": sum(1 for row in rows if row["exists"]),
        "artifact_missing_count": len(missing),
        "artifact_missing": missing,
        "artifact_rows": rows,
    }


def audit_certificates() -> Dict[str, Any]:
    shortform = read_json(SOURCE_SHORTFORM_CERTIFICATE)
    brief = read_json(SOURCE_PUBLIC_BRIEF_CERTIFICATE)
    consolidation = read_json(SOURCE_CONSOLIDATION_CERTIFICATE)

    rows = [
        {
            "name": "public_readme_shortform_certificate",
            "path": str(SOURCE_SHORTFORM_CERTIFICATE.relative_to(ROOT)),
            "version": shortform.get("version"),
            "status": shortform.get("status"),
            "proof_status": shortform.get("proof_status"),
            "collatz_status": shortform.get("collatz_status"),
            "audit_total_failure_count": shortform.get("audit_total_failure_count"),
            "passes": (
                shortform.get("version") == "v4.6"
                and shortform.get("status") == "shortform_defined"
                and shortform.get("proof_status") == "not_a_proof"
                and shortform.get("collatz_status") == "not_claimed_solved"
                and shortform.get("audit_total_failure_count") == 0
            ),
        },
        {
            "name": "native_public_research_brief_certificate",
            "path": str(SOURCE_PUBLIC_BRIEF_CERTIFICATE.relative_to(ROOT)),
            "version": brief.get("version"),
            "status": brief.get("status"),
            "proof_status": brief.get("proof_status"),
            "collatz_status": brief.get("collatz_status"),
            "audit_total_failure_count": brief.get("audit_total_failure_count"),
            "passes": (
                brief.get("version") == "v4.5"
                and brief.get("status") == "public_brief_defined"
                and brief.get("proof_status") == "not_a_proof"
                and brief.get("collatz_status") == "not_claimed_solved"
                and brief.get("audit_total_failure_count") == 0
            ),
        },
        {
            "name": "native_audit_report_consolidation_certificate",
            "path": str(SOURCE_CONSOLIDATION_CERTIFICATE.relative_to(ROOT)),
            "version": consolidation.get("version"),
            "status": consolidation.get("status"),
            "proof_status": consolidation.get("proof_status"),
            "collatz_status": consolidation.get("collatz_status"),
            "audit_total_failure_count": consolidation.get("audit_total_failure_count"),
            "passes": (
                consolidation.get("version") == "v4.4"
                and consolidation.get("status") == "consolidated"
                and consolidation.get("proof_status") == "not_a_proof"
                and consolidation.get("collatz_status") == "not_claimed_solved"
                and consolidation.get("audit_total_failure_count") == 0
            ),
        },
    ]

    failures = [
        row for row in rows
        if not row["passes"]
    ]

    return {
        "certificate_count": len(rows),
        "certificate_passing_count": sum(1 for row in rows if row["passes"]),
        "certificate_failure_count": len(failures),
        "certificate_failures": failures,
        "certificate_rows": rows,
    }


def build_audit() -> Dict[str, Any]:
    entry_audit = audit_public_entry()
    artifact_audit = audit_artifact_links()
    certificate_audit = audit_certificates()

    total_failure_count = (
        entry_audit["entry_failure_count"]
        + artifact_audit["artifact_missing_count"]
        + certificate_audit["certificate_failure_count"]
    )

    status = "public_entry_audit_passed" if total_failure_count == 0 else "public_entry_audit_failed"

    shortform_certificate = read_json(SOURCE_SHORTFORM_CERTIFICATE)

    return {
        "version": VERSION,
        "layer": "public_entry_consistency_audit",
        "status": status,
        "primary_position": "A native structural reading of the Collatz dynamics.",
        "central_question": "What is Collatz before it becomes a conjecture?",
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "entry_audit": entry_audit,
        "artifact_audit": artifact_audit,
        "certificate_audit": certificate_audit,
        "total_failure_count": total_failure_count,
        "source_shortform_version": shortform_certificate.get("version"),
        "source_shortform_status": shortform_certificate.get("status"),
        "source_index_total_items": shortform_certificate.get("index_total_items"),
        "source_audit_total_failure_count": shortform_certificate.get("audit_total_failure_count"),
        "source_obstruction_relevant_invariant_candidate_count": shortform_certificate.get("obstruction_relevant_invariant_candidate_count"),
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "collatz_status": "not_claimed_solved",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
        "not_theory_layer": True,
        "not_proof_layer": True,
        "next_recommended_version": "v4.8 Public Release Snapshot",
    }


def make_markdown(audit: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Public Entry Consistency Audit")
    lines.append("")
    lines.append("Version: v4.7")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This report audits the public entry layer after v4.6.")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append(f"- status: {audit['status']}")
    lines.append(f"- total_failure_count: {audit['total_failure_count']}")
    lines.append(f"- entry_failure_count: {audit['entry_audit']['entry_failure_count']}")
    lines.append(f"- artifact_missing_count: {audit['artifact_audit']['artifact_missing_count']}")
    lines.append(f"- certificate_failure_count: {audit['certificate_audit']['certificate_failure_count']}")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(f"- proof_status: {audit['proof_status']}")
    lines.append(f"- theorem_status: {audit['theorem_status']}")
    lines.append(f"- collatz_status: {audit['collatz_status']}")
    lines.append(f"- global_closure_status: {audit['global_closure_status']}")
    lines.append(f"- global_invariant_status: {audit['global_invariant_status']}")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append("    " + audit["mother_rule"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(audit["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "public_entry_consistency_audit_certificate",
        "status": audit["status"],
        "total_failure_count": audit["total_failure_count"],
        "entry_failure_count": audit["entry_audit"]["entry_failure_count"],
        "artifact_missing_count": audit["artifact_audit"]["artifact_missing_count"],
        "certificate_failure_count": audit["certificate_audit"]["certificate_failure_count"],
        "central_question": audit["central_question"],
        "mother_rule": audit["mother_rule"],
        "source_shortform_version": audit["source_shortform_version"],
        "source_shortform_status": audit["source_shortform_status"],
        "source_index_total_items": audit["source_index_total_items"],
        "source_audit_total_failure_count": audit["source_audit_total_failure_count"],
        "source_obstruction_relevant_invariant_candidate_count": audit["source_obstruction_relevant_invariant_candidate_count"],
        "proof_status": audit["proof_status"],
        "theorem_status": audit["theorem_status"],
        "collatz_status": audit["collatz_status"],
        "global_closure_status": audit["global_closure_status"],
        "global_invariant_status": audit["global_invariant_status"],
        "not_theory_layer": audit["not_theory_layer"],
        "not_proof_layer": audit["not_proof_layer"],
        "next_recommended_version": audit["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v4.7")
    print("=" * 80)
    print("Public Entry Consistency Audit")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    markdown = make_markdown(audit)
    certificate = make_certificate(audit)

    OUTPUT_JSON.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(markdown + "\n", encoding="utf-8")
    OUTPUT_CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"status: {audit['status']}")
    print(f"total_failure_count: {audit['total_failure_count']}")
    print(f"entry_failure_count: {audit['entry_audit']['entry_failure_count']}")
    print(f"artifact_missing_count: {audit['artifact_audit']['artifact_missing_count']}")
    print(f"certificate_failure_count: {audit['certificate_audit']['certificate_failure_count']}")
    print(f"source_shortform_version: {audit['source_shortform_version']}")
    print(f"source_index_total_items: {audit['source_index_total_items']}")
    print(f"proof_status: {audit['proof_status']}")
    print(f"collatz_status: {audit['collatz_status']}")
    print(f"mother_rule: {audit['mother_rule']}")
    print(f"next: {audit['next_recommended_version']}")
    print(f"Wrote audit JSON to: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote audit Markdown to: {OUTPUT_MD.relative_to(ROOT)}")
    print(f"Wrote certificate to: {OUTPUT_CERTIFICATE.relative_to(ROOT)}")
    print("=" * 80)

    if audit["total_failure_count"] != 0:
        raise SystemExit("Public entry consistency audit failed.")


if __name__ == "__main__":
    main()
