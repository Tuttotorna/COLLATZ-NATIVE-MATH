#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.4

Native Audit Report Consolidation.

This builder consolidates the current repository state into one readable
native-language status report.

It does not add theory.
It does not prove Collatz.
It does not claim Collatz is solved.
It does not claim global closure.
It does not claim global invariance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "v4.4"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

OUTPUT_JSON = RESULTS_DIR / "native_audit_report_consolidation.json"
OUTPUT_MD = RESULTS_DIR / "native_audit_report_consolidation.md"
OUTPUT_CERTIFICATE = RESULTS_DIR / "native_audit_report_consolidation_certificate.json"

SOURCE_PATHS = {
    "audit_v43": RESULTS_DIR / "native_artifact_consistency_audit_certificate.json",
    "index_v42": RESULTS_DIR / "native_language_index_certificate.json",
    "summary_v40": RESULTS_DIR / "native_language_summary_certificate.json",
    "invariant_v39": RESULTS_DIR / "native_invariant_candidate_certificate.json",
    "conservation_v38": RESULTS_DIR / "native_conservation_certificate.json",
    "stability_v37": RESULTS_DIR / "native_grammar_stability_certificate.json",
    "mutation_v36": RESULTS_DIR / "native_grammar_mutation_certificate.json",
    "recurrence_v35": RESULTS_DIR / "native_grammar_recurrence_certificate.json",
    "sentence_atlas_v34": RESULTS_DIR / "native_sentence_atlas_certificate.json",
    "sentences_v33": RESULTS_DIR / "native_sentence_certificate.json",
}


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def optional_value(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    return data.get(key, default)


def load_sources() -> Dict[str, Dict[str, Any]]:
    return {name: read_json(path) for name, path in SOURCE_PATHS.items()}


def build_consolidation(sources: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    audit = sources["audit_v43"]
    index = sources["index_v42"]
    summary = sources["summary_v40"]
    invariant = sources["invariant_v39"]
    conservation = sources["conservation_v38"]
    stability = sources["stability_v37"]
    mutation = sources["mutation_v36"]
    recurrence = sources["recurrence_v35"]
    atlas = sources["sentence_atlas_v34"]
    sentences = sources["sentences_v33"]

    observed_patterns: List[str] = [
        "native_language_route_established",
        "native_language_index_complete",
        "artifact_consistency_audit_passed",
        "danger_release_invariant_candidates_present",
        "dangerous_stability_invariant_candidates_present",
        "no_obstruction_relevant_invariant_candidate_detected_in_bounded_artifacts",
        "dangerous_grammar_appears_unstable_in_this_atlas",
        "dangerous_mutations_present_without_obstruction_mutation",
        "dangerous_recurrence_present_without_obstruction_recurrence",
        "dangerous_sentences_present_without_obstruction_sentence",
    ]

    source_versions = {
        name: optional_value(data, "version")
        for name, data in sources.items()
    }

    boundary_status = {
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "collatz_status": "not_claimed_solved",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
    }

    public_summary = (
        "COLLATZ-NATIVE-MATH is currently a native structural reading of "
        "Collatz dynamics. The repository has an indexed native-language route, "
        "a passing artifact consistency audit, bounded sentence and grammar maps, "
        "bounded invariant candidate artifacts, and no proof or solution claim."
    )

    current_native_answer = (
        "Within the bounded artifacts, Collatz appears to generate dangerous "
        "native sentence forms, release behavior, unstable dangerous grammar, "
        "and bounded invariant candidates around danger-release and dangerous "
        "stability. No obstruction-relevant invariant candidate is detected in "
        "the current bounded maps."
    )

    return {
        "version": VERSION,
        "layer": "native_audit_report_consolidation",
        "status": "consolidated",
        "primary_position": "A native structural reading of the Collatz dynamics.",
        "central_question": "What is Collatz before it becomes a conjecture?",
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "public_summary": public_summary,
        "current_native_answer": current_native_answer,
        "source_versions": source_versions,
        "source_statuses": {
            "audit_v43_status": audit.get("status"),
            "audit_v43_total_failure_count": audit.get("total_failure_count"),
            "index_v42_missing_required_count": index.get("missing_required_count"),
            "summary_v40_native_interpretation": summary.get("native_interpretation"),
            "invariant_v39_native_interpretation": invariant.get("native_interpretation"),
            "conservation_v38_native_interpretation": conservation.get("native_interpretation"),
            "stability_v37_native_interpretation": stability.get("native_interpretation"),
            "mutation_v36_native_interpretation": mutation.get("native_interpretation"),
            "recurrence_v35_native_interpretation": recurrence.get("native_interpretation"),
            "sentence_atlas_v34_native_interpretation": atlas.get("native_interpretation"),
        },
        "current_counts": {
            "indexed_items": index.get("total_indexed_items"),
            "index_sections": index.get("section_count"),
            "audit_total_failure_count": audit.get("total_failure_count"),
            "native_language_object_count": summary.get("native_language_object_count"),
            "learned_pattern_count": summary.get("learned_pattern_count"),
            "invariant_candidate_count": invariant.get("invariant_candidate_count"),
            "danger_release_invariant_candidate_count": invariant.get("danger_release_invariant_candidate_count"),
            "dangerous_stability_invariant_candidate_count": invariant.get("dangerous_stability_invariant_candidate_count"),
            "obstruction_relevant_invariant_candidate_count": invariant.get("obstruction_relevant_invariant_candidate_count"),
            "conservation_candidate_count": conservation.get("conservation_candidate_count"),
            "stability_edge_count": stability.get("stability_edge_count"),
            "dangerous_unstable_edge_count": stability.get("dangerous_unstable_edge_count"),
            "mutation_edge_count": mutation.get("mutation_edge_count"),
            "dangerous_mutation_count": mutation.get("dangerous_mutation_count"),
            "recurrence_total_edge_count": recurrence.get("total_edge_count"),
            "dangerous_recurrence_edge_count": recurrence.get("dangerous_edge_count"),
            "sentence_count": atlas.get("sentence_count"),
            "dangerous_sentence_count": atlas.get("dangerous_sentence_count"),
            "obstruction_sentence_count": atlas.get("obstruction_sentence_count"),
        },
        "observed_patterns": observed_patterns,
        "reader_boundary": [
            "This is not a proof.",
            "This is not a solution claim.",
            "This is not a theorem layer.",
            "Bounded artifacts are not global proof.",
            "No obstruction detected in bounded artifacts is not obstruction impossibility.",
            "Termination remains a deferred classical translation endpoint.",
        ],
        "native_route_status": [
            "v3.1 native language inversion",
            "v3.2 native grammar map",
            "v3.3 native sentence extractor",
            "v3.4 native sentence atlas",
            "v3.5 native grammar recurrence map",
            "v3.6 native grammar mutation atlas",
            "v3.7 native grammar stability map",
            "v3.8 native conservation map",
            "v3.9 native invariant candidate map",
            "v4.0 native language summary",
            "v4.1 README consolidation",
            "v4.2 native language index",
            "v4.3 native artifact consistency audit",
            "v4.4 native audit report consolidation",
        ],
        "next_recommended_version": "v4.5 Native Public Research Brief",
        **boundary_status,
        "not_theory_layer": True,
        "not_proof_layer": True,
    }


def make_markdown(report: Dict[str, Any]) -> str:
    counts = report["current_counts"]
    statuses = report["source_statuses"]

    lines: List[str] = []

    lines.append("# Native Audit Report Consolidation")
    lines.append("")
    lines.append("Version: v4.4")
    lines.append("")
    lines.append("## Position")
    lines.append("")
    lines.append(report["primary_position"])
    lines.append("")
    lines.append("Central question:")
    lines.append("")
    lines.append("    " + report["central_question"])
    lines.append("")
    lines.append("Core rule:")
    lines.append("")
    lines.append("    " + report["mother_rule"])
    lines.append("")
    lines.append("## Public summary")
    lines.append("")
    lines.append(report["public_summary"])
    lines.append("")
    lines.append("## Current native answer")
    lines.append("")
    lines.append(report["current_native_answer"])
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append("- proof_status: " + report["proof_status"])
    lines.append("- theorem_status: " + report["theorem_status"])
    lines.append("- collatz_status: " + report["collatz_status"])
    lines.append("- global_closure_status: " + report["global_closure_status"])
    lines.append("- global_invariant_status: " + report["global_invariant_status"])
    lines.append("")
    lines.append("## Source status")
    lines.append("")
    for key, value in statuses.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Current counts")
    lines.append("")
    for key, value in counts.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Observed patterns")
    lines.append("")
    for item in report["observed_patterns"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Reader boundary")
    lines.append("")
    for item in report["reader_boundary"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Native route")
    lines.append("")
    for item in report["native_route_status"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(report["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(report: Dict[str, Any]) -> Dict[str, Any]:
    counts = report["current_counts"]

    return {
        "version": VERSION,
        "certificate_type": "native_audit_report_consolidation_certificate",
        "status": report["status"],
        "primary_position": report["primary_position"],
        "central_question": report["central_question"],
        "mother_rule": report["mother_rule"],
        "source_versions": report["source_versions"],
        "audit_total_failure_count": counts.get("audit_total_failure_count"),
        "indexed_items": counts.get("indexed_items"),
        "invariant_candidate_count": counts.get("invariant_candidate_count"),
        "danger_release_invariant_candidate_count": counts.get("danger_release_invariant_candidate_count"),
        "dangerous_stability_invariant_candidate_count": counts.get("dangerous_stability_invariant_candidate_count"),
        "obstruction_relevant_invariant_candidate_count": counts.get("obstruction_relevant_invariant_candidate_count"),
        "observed_pattern_count": len(report["observed_patterns"]),
        "reader_boundary_count": len(report["reader_boundary"]),
        "native_route_status_count": len(report["native_route_status"]),
        "proof_status": report["proof_status"],
        "theorem_status": report["theorem_status"],
        "collatz_status": report["collatz_status"],
        "global_closure_status": report["global_closure_status"],
        "global_invariant_status": report["global_invariant_status"],
        "not_theory_layer": report["not_theory_layer"],
        "not_proof_layer": report["not_proof_layer"],
        "next_recommended_version": report["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v4.4")
    print("=" * 80)
    print("Native Audit Report Consolidation")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    sources = load_sources()
    report = build_consolidation(sources)
    markdown = make_markdown(report)
    certificate = make_certificate(report)

    OUTPUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(markdown + "\n", encoding="utf-8")
    OUTPUT_CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"status: {report['status']}")
    print(f"primary_position: {report['primary_position']}")
    print(f"audit_total_failure_count: {certificate['audit_total_failure_count']}")
    print(f"indexed_items: {certificate['indexed_items']}")
    print(f"invariant_candidate_count: {certificate['invariant_candidate_count']}")
    print(f"obstruction_relevant_invariant_candidate_count: {certificate['obstruction_relevant_invariant_candidate_count']}")
    print(f"proof_status: {certificate['proof_status']}")
    print(f"collatz_status: {certificate['collatz_status']}")
    print(f"mother_rule: {certificate['mother_rule']}")
    print(f"next: {certificate['next_recommended_version']}")
    print(f"Wrote JSON report to: {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown report to: {OUTPUT_MD.relative_to(ROOT)}")
    print(f"Wrote certificate to: {OUTPUT_CERTIFICATE.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
