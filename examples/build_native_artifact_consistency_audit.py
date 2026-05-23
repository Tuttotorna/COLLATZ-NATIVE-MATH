#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.3

Native Artifact Consistency Audit.

This builder audits the repository after v4.2.

It does not add theory.
It does not solve Collatz.
It does not prove Collatz.
It does not claim global closure.
It does not claim global invariance.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v4.3"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

INDEX_JSON_PATH = RESULTS_DIR / "native_language_index.json"
INDEX_CERTIFICATE_PATH = RESULTS_DIR / "native_language_index_certificate.json"

AUDIT_JSON_PATH = RESULTS_DIR / "native_artifact_consistency_audit.json"
AUDIT_MD_PATH = RESULTS_DIR / "native_artifact_consistency_audit.md"
AUDIT_CERTIFICATE_PATH = RESULTS_DIR / "native_artifact_consistency_audit_certificate.json"

ENTRY_FILES = [
    "README.md",
    "START_HERE.md",
    "CRC_CONJECTURE.md",
]

CORE_CERTIFICATES = [
    "results/native_language_summary_certificate.json",
    "results/native_language_index_certificate.json",
    "results/native_invariant_candidate_certificate.json",
    "results/native_conservation_certificate.json",
    "results/native_grammar_stability_certificate.json",
    "results/native_grammar_mutation_certificate.json",
    "results/native_grammar_recurrence_certificate.json",
    "results/native_sentence_atlas_certificate.json",
    "results/native_sentence_certificate.json",
]

LATEST_BUILDERS = [
    "examples/build_native_language_summary.py",
    "examples/build_native_language_index.py",
    "examples/build_native_invariant_candidate_map.py",
    "examples/build_native_conservation_map.py",
    "examples/build_native_grammar_stability_map.py",
    "examples/build_native_grammar_mutation_atlas.py",
    "examples/build_native_grammar_recurrence_map.py",
    "examples/build_native_sentence_atlas.py",
    "examples/extract_native_sentences.py",
]

REQUIRED_NATIVE_PHRASES = [
    "No solution before native language.",
    "not_a_proof",
    "not_claimed_solved",
]

FORBIDDEN_EXACT_PHRASES = [
    "Collatz is solved.",
    "We solved Collatz.",
    "Proof of Collatz.",
    "Collatz proof complete.",
    "global closure is proved",
    "global invariant is proved",
    "obstruction is impossible",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_assertive_forbidden_claim(text: str, phrase: str) -> bool:
    """
    Conservative detector.

    Returns True only when a forbidden phrase appears as a pure standalone
    assertive line.

    It ignores:
    - markdown lists
    - code blocks
    - quotes
    - headings
    - boundary language
    - negations
    - examples
    - status fields
    - inequality statements
    """

    target = phrase.lower().strip()
    target = target.strip("`*_ .:").rstrip(".").strip()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        lower = line.lower().strip()

        if not lower:
            continue

        # Ignore all Markdown/context/code/list lines.
        if lower.startswith(("-", "*", ">", "`", "#")):
            continue

        normalized = lower.strip("`*_ .:").rstrip(".").strip()

        # Only pure standalone assertion fails.
        if normalized == target:
            return True

    return False

def ensure_index_artifacts() -> None:
    if INDEX_JSON_PATH.exists() and INDEX_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_language_index.py"
    if not builder.exists():
        raise FileNotFoundError("Missing native language index builder.")

    subprocess.run(
        [sys.executable, str(builder)],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def audit_index_files(index: Dict[str, Any]) -> Dict[str, Any]:
    indexed_items: List[Dict[str, Any]] = []
    missing_required: List[Dict[str, Any]] = []

    for section in index.get("sections", []):
        section_id = section.get("section_id")
        for item in section.get("items", []):
            path = item.get("path")
            required = bool(item.get("required", True))
            exists = (ROOT / path).exists()

            row = {
                "section_id": section_id,
                "path": path,
                "role": item.get("role"),
                "required": required,
                "exists": exists,
            }

            indexed_items.append(row)

            if required and not exists:
                missing_required.append(row)

    return {
        "indexed_item_count": len(indexed_items),
        "missing_required_count": len(missing_required),
        "missing_required_items": missing_required,
    }


def audit_entry_files() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for rel in ENTRY_FILES:
        path = ROOT / rel
        text = read_text(path)

        missing_required_phrases = [
            phrase for phrase in REQUIRED_NATIVE_PHRASES
            if phrase not in text
        ]

        forbidden_found = [
            phrase for phrase in FORBIDDEN_EXACT_PHRASES
            if is_assertive_forbidden_claim(text, phrase)
        ]

        row = {
            "path": rel,
            "exists": path.exists(),
            "missing_required_phrases": missing_required_phrases,
            "forbidden_found": forbidden_found,
            "passes": path.exists() and not missing_required_phrases and not forbidden_found,
        }

        rows.append(row)

        if not row["passes"]:
            failures.append(row)

    return {
        "entry_file_count": len(rows),
        "entry_files_passing": sum(1 for row in rows if row["passes"]),
        "entry_failure_count": len(failures),
        "entry_failures": failures,
        "entry_rows": rows,
    }


def audit_certificates() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for rel in CORE_CERTIFICATES:
        path = ROOT / rel

        if not path.exists():
            row = {
                "path": rel,
                "exists": False,
                "passes": False,
                "errors": ["missing_certificate"],
            }
            rows.append(row)
            failures.append(row)
            continue

        data = read_json(path)
        errors: List[str] = []

        if data.get("proof_status") != "not_a_proof":
            errors.append("proof_status_not_not_a_proof")

        theorem_status = data.get("theorem_status")
        if theorem_status is not None and theorem_status != "no_theorems_introduced":
            errors.append("theorem_status_invalid")

        collatz_status = data.get("collatz_status")
        if collatz_status is not None and collatz_status != "not_claimed_solved":
            errors.append("collatz_status_invalid")

        global_closure_status = data.get("global_closure_status")
        if global_closure_status is not None and global_closure_status != "not_claimed":
            errors.append("global_closure_status_invalid")

        global_invariant_status = data.get("global_invariant_status")
        if global_invariant_status is not None and global_invariant_status != "not_claimed":
            errors.append("global_invariant_status_invalid")

        row = {
            "path": rel,
            "exists": True,
            "version": data.get("version"),
            "proof_status": data.get("proof_status"),
            "theorem_status": data.get("theorem_status"),
            "collatz_status": data.get("collatz_status"),
            "global_closure_status": data.get("global_closure_status"),
            "global_invariant_status": data.get("global_invariant_status"),
            "passes": not errors,
            "errors": errors,
        }

        rows.append(row)

        if errors:
            failures.append(row)

    return {
        "certificate_count": len(rows),
        "certificate_passing_count": sum(1 for row in rows if row["passes"]),
        "certificate_failure_count": len(failures),
        "certificate_failures": failures,
        "certificate_rows": rows,
    }


def audit_builders() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    missing: List[str] = []

    for rel in LATEST_BUILDERS:
        exists = (ROOT / rel).exists()
        rows.append({"path": rel, "exists": exists})
        if not exists:
            missing.append(rel)

    return {
        "builder_count": len(rows),
        "builder_existing_count": sum(1 for row in rows if row["exists"]),
        "builder_missing_count": len(missing),
        "builder_missing": missing,
        "builder_rows": rows,
    }


def audit_readme_route() -> Dict[str, Any]:
    readme = read_text(ROOT / "README.md")

    required_route_versions = [
        "v3.1",
        "v3.2",
        "v3.3",
        "v3.4",
        "v3.5",
        "v3.6",
        "v3.7",
        "v3.8",
        "v3.9",
        "v4.0",
        "v4.1",
        "v4.2",
    ]

    missing_versions = [
        version for version in required_route_versions
        if version not in readme
    ]

    return {
        "required_route_version_count": len(required_route_versions),
        "missing_route_version_count": len(missing_versions),
        "missing_route_versions": missing_versions,
        "passes": not missing_versions,
    }


def build_audit() -> Dict[str, Any]:
    ensure_index_artifacts()

    index = read_json(INDEX_JSON_PATH)
    index_certificate = read_json(INDEX_CERTIFICATE_PATH)

    index_audit = audit_index_files(index)
    entry_audit = audit_entry_files()
    certificate_audit = audit_certificates()
    builder_audit = audit_builders()
    readme_route_audit = audit_readme_route()

    failure_count = (
        index_audit["missing_required_count"]
        + entry_audit["entry_failure_count"]
        + certificate_audit["certificate_failure_count"]
        + builder_audit["builder_missing_count"]
        + readme_route_audit["missing_route_version_count"]
    )

    status = "audit_passed" if failure_count == 0 else "audit_failed"

    return {
        "version": VERSION,
        "layer": "native_artifact_consistency_audit",
        "status": status,
        "source_index_version": index_certificate.get("version"),
        "source_index_section_count": index_certificate.get("section_count"),
        "source_index_total_items": index_certificate.get("total_indexed_items"),
        "source_index_missing_required_count": index_certificate.get("missing_required_count"),
        "index_audit": index_audit,
        "entry_audit": entry_audit,
        "certificate_audit": certificate_audit,
        "builder_audit": builder_audit,
        "readme_route_audit": readme_route_audit,
        "total_failure_count": failure_count,
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "collatz_status": "not_claimed_solved",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
        "not_theory_layer": True,
        "not_proof_layer": True,
        "next_recommended_version": "v4.4 Native Audit Report Consolidation",
    }


def make_markdown(audit: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Artifact Consistency Audit")
    lines.append("")
    lines.append("Version: v4.3")
    lines.append("")
    lines.append("This audit checks repository consistency after v4.2.")
    lines.append("")
    lines.append("Core rule:")
    lines.append("")
    lines.append("    No solution before native language.")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append(f"- status: {audit['status']}")
    lines.append(f"- total_failure_count: {audit['total_failure_count']}")
    lines.append(f"- proof_status: {audit['proof_status']}")
    lines.append(f"- theorem_status: {audit['theorem_status']}")
    lines.append(f"- collatz_status: {audit['collatz_status']}")
    lines.append(f"- global_closure_status: {audit['global_closure_status']}")
    lines.append(f"- global_invariant_status: {audit['global_invariant_status']}")
    lines.append("")
    lines.append("## Check groups")
    lines.append("")
    lines.append(f"- indexed_missing_required_count: {audit['index_audit']['missing_required_count']}")
    lines.append(f"- entry_failure_count: {audit['entry_audit']['entry_failure_count']}")
    lines.append(f"- certificate_failure_count: {audit['certificate_audit']['certificate_failure_count']}")
    lines.append(f"- builder_missing_count: {audit['builder_audit']['builder_missing_count']}")
    lines.append(f"- readme_missing_route_version_count: {audit['readme_route_audit']['missing_route_version_count']}")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append("audit_passed does not mean proof.")
    lines.append("")
    lines.append("audit_passed does not mean Collatz solved.")
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(audit["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_artifact_consistency_audit_certificate",
        "status": audit["status"],
        "total_failure_count": audit["total_failure_count"],
        "source_index_version": audit["source_index_version"],
        "source_index_section_count": audit["source_index_section_count"],
        "source_index_total_items": audit["source_index_total_items"],
        "source_index_missing_required_count": audit["source_index_missing_required_count"],
        "indexed_missing_required_count": audit["index_audit"]["missing_required_count"],
        "entry_failure_count": audit["entry_audit"]["entry_failure_count"],
        "certificate_failure_count": audit["certificate_audit"]["certificate_failure_count"],
        "builder_missing_count": audit["builder_audit"]["builder_missing_count"],
        "readme_missing_route_version_count": audit["readme_route_audit"]["missing_route_version_count"],
        "mother_rule": audit["mother_rule"],
        "secondary_rule": audit["secondary_rule"],
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
    print("COLLATZ-NATIVE-MATH v4.3")
    print("=" * 80)
    print("Native Artifact Consistency Audit")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    report = make_markdown(audit)
    certificate = make_certificate(audit)

    AUDIT_JSON_PATH.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    AUDIT_MD_PATH.write_text(report + "\n", encoding="utf-8")
    AUDIT_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"status: {audit['status']}")
    print(f"total_failure_count: {audit['total_failure_count']}")
    print(f"indexed_missing_required_count: {audit['index_audit']['missing_required_count']}")
    print(f"entry_failure_count: {audit['entry_audit']['entry_failure_count']}")
    print(f"certificate_failure_count: {audit['certificate_audit']['certificate_failure_count']}")
    print(f"builder_missing_count: {audit['builder_audit']['builder_missing_count']}")
    print(f"readme_missing_route_version_count: {audit['readme_route_audit']['missing_route_version_count']}")
    print(f"proof_status: {audit['proof_status']}")
    print(f"collatz_status: {audit['collatz_status']}")
    print(f"mother_rule: {audit['mother_rule']}")
    print(f"next: {audit['next_recommended_version']}")
    print(f"Wrote audit JSON to: {AUDIT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote audit Markdown to: {AUDIT_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {AUDIT_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)

    if audit["total_failure_count"] != 0:
        raise SystemExit("Native artifact consistency audit failed.")


if __name__ == "__main__":
    main()
