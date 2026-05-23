#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.6

Public README Shortform.

This builder creates a short public-facing README entry section.

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


VERSION = "v4.6"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
README_PATH = ROOT / "README.md"

SOURCE_BRIEF_CERTIFICATE = RESULTS_DIR / "native_public_research_brief_certificate.json"
SOURCE_BRIEF_JSON = RESULTS_DIR / "native_public_research_brief.json"
SOURCE_CONSOLIDATION_CERTIFICATE = RESULTS_DIR / "native_audit_report_consolidation_certificate.json"

OUTPUT_JSON = RESULTS_DIR / "public_readme_shortform.json"
OUTPUT_MD = RESULTS_DIR / "public_readme_shortform.md"
OUTPUT_CERTIFICATE = RESULTS_DIR / "public_readme_shortform_certificate.json"

SHORTFORM_MARKER = "<!-- V4.6_PUBLIC_README_SHORTFORM -->"


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def build_shortform() -> Dict[str, Any]:
    brief_certificate = read_json(SOURCE_BRIEF_CERTIFICATE)
    brief_json = read_json(SOURCE_BRIEF_JSON)
    consolidation_certificate = read_json(SOURCE_CONSOLIDATION_CERTIFICATE)

    return {
        "version": VERSION,
        "layer": "public_readme_shortform",
        "status": "shortform_defined",
        "marker": SHORTFORM_MARKER,
        "one_sentence_description": (
            "COLLATZ-NATIVE-MATH is a native structural reading of Collatz dynamics."
        ),
        "central_question": "What is Collatz before it becomes a conjecture?",
        "core_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "what_this_is": [
            "a native-language description program",
            "a bounded artifact system",
            "a grammar mapping of Collatz-generated structures",
            "a public non-proof research route",
        ],
        "what_this_is_not": [
            "not a proof of Collatz",
            "not a claim that Collatz is solved",
            "not a theorem layer",
            "not a global closure claim",
            "not a global invariant claim",
        ],
        "current_bounded_status": [
            "artifact consistency audit passes",
            "native language index contains 101 indexed items",
            "bounded invariant candidate map contains 45 candidates",
            "danger-release invariant candidates are present",
            "dangerous-stability invariant candidates are present",
            "no obstruction-relevant invariant candidate is detected in the current bounded maps",
        ],
        "public_brief_link": "results/native_public_research_brief.md",
        "consolidated_report_link": "results/native_audit_report_consolidation.md",
        "source_integrity": {
            "public_brief_version": brief_certificate.get("version"),
            "public_brief_status": brief_certificate.get("status"),
            "audit_total_failure_count": brief_certificate.get("audit_total_failure_count"),
            "index_total_items": brief_certificate.get("index_total_items"),
            "invariant_candidate_count": brief_certificate.get("invariant_candidate_count"),
            "danger_release_invariant_candidate_count": brief_certificate.get("danger_release_invariant_candidate_count"),
            "dangerous_stability_invariant_candidate_count": brief_certificate.get("dangerous_stability_invariant_candidate_count"),
            "obstruction_relevant_invariant_candidate_count": brief_certificate.get("obstruction_relevant_invariant_candidate_count"),
            "consolidation_version": consolidation_certificate.get("version"),
            "consolidation_status": consolidation_certificate.get("status"),
        },
        "allowed_reader_takeaway": (
            "This repository is building a native description of Collatz before attempting "
            "any proof-oriented translation."
        ),
        "forbidden_reader_takeaway": (
            "This repository proves Collatz or claims Collatz is solved."
        ),
        "next_recommended_version": "v4.7 Public Entry Consistency Audit",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "collatz_status": "not_claimed_solved",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
        "not_theory_layer": True,
        "not_proof_layer": True,
    }


def make_markdown(shortform: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append(SHORTFORM_MARKER)
    lines.append("## Public shortform")
    lines.append("")
    lines.append(shortform["one_sentence_description"])
    lines.append("")
    lines.append("**Central question:**")
    lines.append("")
    lines.append("```text")
    lines.append(shortform["central_question"])
    lines.append("```")
    lines.append("")
    lines.append("**Core rule:**")
    lines.append("")
    lines.append("```text")
    lines.append(shortform["core_rule"])
    lines.append("```")
    lines.append("")
    lines.append("**What this is:**")
    lines.append("")
    for item in shortform["what_this_is"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**What this is not:**")
    lines.append("")
    for item in shortform["what_this_is_not"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Current bounded status:**")
    lines.append("")
    for item in shortform["current_bounded_status"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Read next:**")
    lines.append("")
    lines.append(f"- `{shortform['public_brief_link']}`")
    lines.append(f"- `{shortform['consolidated_report_link']}`")
    lines.append("")
    lines.append("**Boundary:**")
    lines.append("")
    lines.append("```text")
    lines.append("proof_status: not_a_proof")
    lines.append("collatz_status: not_claimed_solved")
    lines.append("global_closure_status: not_claimed")
    lines.append("global_invariant_status: not_claimed")
    lines.append("```")
    lines.append("<!-- /V4.6_PUBLIC_README_SHORTFORM -->")

    return "\n".join(lines)


def make_certificate(shortform: Dict[str, Any]) -> Dict[str, Any]:
    source = shortform["source_integrity"]

    return {
        "version": VERSION,
        "certificate_type": "public_readme_shortform_certificate",
        "status": shortform["status"],
        "marker": shortform["marker"],
        "central_question": shortform["central_question"],
        "core_rule": shortform["core_rule"],
        "what_this_is_count": len(shortform["what_this_is"]),
        "what_this_is_not_count": len(shortform["what_this_is_not"]),
        "current_bounded_status_count": len(shortform["current_bounded_status"]),
        "public_brief_link": shortform["public_brief_link"],
        "consolidated_report_link": shortform["consolidated_report_link"],
        "audit_total_failure_count": source.get("audit_total_failure_count"),
        "index_total_items": source.get("index_total_items"),
        "invariant_candidate_count": source.get("invariant_candidate_count"),
        "danger_release_invariant_candidate_count": source.get("danger_release_invariant_candidate_count"),
        "dangerous_stability_invariant_candidate_count": source.get("dangerous_stability_invariant_candidate_count"),
        "obstruction_relevant_invariant_candidate_count": source.get("obstruction_relevant_invariant_candidate_count"),
        "proof_status": shortform["proof_status"],
        "theorem_status": shortform["theorem_status"],
        "collatz_status": shortform["collatz_status"],
        "global_closure_status": shortform["global_closure_status"],
        "global_invariant_status": shortform["global_invariant_status"],
        "not_theory_layer": shortform["not_theory_layer"],
        "not_proof_layer": shortform["not_proof_layer"],
        "next_recommended_version": shortform["next_recommended_version"],
    }


def update_readme(markdown: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")

    if SHORTFORM_MARKER in text:
        start = text.index(SHORTFORM_MARKER)
        end_marker = "<!-- /V4.6_PUBLIC_README_SHORTFORM -->"
        end = text.index(end_marker, start) + len(end_marker)
        new_text = text[:start].rstrip() + "\n\n" + markdown + "\n\n" + text[end:].lstrip()
    else:
        lines = text.splitlines()
        if lines and lines[0].startswith("# "):
            insert_at = 1
        else:
            insert_at = 0
        new_lines = lines[:insert_at] + ["", markdown, ""] + lines[insert_at:]
        new_text = "\n".join(new_lines).rstrip() + "\n"

    README_PATH.write_text(new_text, encoding="utf-8")


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v4.6")
    print("=" * 80)
    print("Public README Shortform")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    shortform = build_shortform()
    markdown = make_markdown(shortform)
    certificate = make_certificate(shortform)

    OUTPUT_JSON.write_text(json.dumps(shortform, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(markdown + "\n", encoding="utf-8")
    OUTPUT_CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    update_readme(markdown)

    print(f"status: {shortform['status']}")
    print(f"central_question: {shortform['central_question']}")
    print(f"core_rule: {shortform['core_rule']}")
    print(f"audit_total_failure_count: {certificate['audit_total_failure_count']}")
    print(f"index_total_items: {certificate['index_total_items']}")
    print(f"obstruction_relevant_invariant_candidate_count: {certificate['obstruction_relevant_invariant_candidate_count']}")
    print(f"proof_status: {certificate['proof_status']}")
    print(f"collatz_status: {certificate['collatz_status']}")
    print(f"next: {certificate['next_recommended_version']}")
    print(f"Wrote JSON shortform to: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown shortform to: {OUTPUT_MD.relative_to(ROOT)}")
    print(f"Wrote certificate to: {OUTPUT_CERTIFICATE.relative_to(ROOT)}")
    print("Updated README.md")
    print("=" * 80)


if __name__ == "__main__":
    main()
