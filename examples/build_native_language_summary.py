#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.0

Native Language Summary.

This builder summarizes the v3.1 to v3.9 route.

It does not solve Collatz.
It does not prove Collatz.
It does not claim global closure.
It does not claim global invariance.

It summarizes what the project has learned by treating Collatz first as
a native dynamical language.

Outputs:
- results/native_language_summary.json
- results/native_language_summary.md
- results/native_language_summary_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v4.0"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

INVARIANT_MAP_PATH = RESULTS_DIR / "native_invariant_candidate_map.json"
INVARIANT_CERTIFICATE_PATH = RESULTS_DIR / "native_invariant_candidate_certificate.json"

SUMMARY_PATH = RESULTS_DIR / "native_language_summary.json"
SUMMARY_REPORT_PATH = RESULTS_DIR / "native_language_summary.md"
SUMMARY_CERTIFICATE_PATH = RESULTS_DIR / "native_language_summary_certificate.json"


def ensure_source_artifacts() -> None:
    if INVARIANT_MAP_PATH.exists() and INVARIANT_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_invariant_candidate_map.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.9 native invariant candidate map builder.")

    subprocess.run(
        [sys.executable, str(builder)],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(invariant_map: Dict[str, Any], invariant_certificate: Dict[str, Any]) -> Dict[str, Any]:
    route = [
        {
            "version": "v3.1",
            "layer": "native_language_inversion",
            "question": "What is Collatz before it becomes a conjecture?",
            "role": "route_correction",
        },
        {
            "version": "v3.2",
            "layer": "native_grammar_map",
            "question": "What grammar does Collatz generate before terminal translation?",
            "role": "grammar_definition",
        },
        {
            "version": "v3.3",
            "layer": "native_sentence_extractor",
            "question": "How does a trajectory speak as a native sentence?",
            "role": "sentence_extraction",
        },
        {
            "version": "v3.4",
            "layer": "native_sentence_atlas",
            "question": "What sentence families appear in the bounded native language?",
            "role": "sentence_atlas",
        },
        {
            "version": "v3.5",
            "layer": "native_grammar_recurrence_map",
            "question": "Which native sentence forms return?",
            "role": "recurrence_map",
        },
        {
            "version": "v3.6",
            "layer": "native_grammar_mutation_atlas",
            "question": "How does one native sentence transform into another?",
            "role": "mutation_atlas",
        },
        {
            "version": "v3.7",
            "layer": "native_grammar_stability_map",
            "question": "What does Collatz preserve under recurrence and mutation?",
            "role": "stability_map",
        },
        {
            "version": "v3.8",
            "layer": "native_conservation_map",
            "question": "What remains conserved across recurrence, mutation, and stability?",
            "role": "conservation_map",
        },
        {
            "version": "v3.9",
            "layer": "native_invariant_candidate_map",
            "question": "Which conserved behaviors are strong enough to become native invariant candidates?",
            "role": "invariant_candidate_map",
        },
    ]

    core_distinctions = {
        "recurrence": "what_returns",
        "mutation": "what_changes",
        "stability": "what_resists_change",
        "conservation": "what_remains_through_change",
        "invariant_candidate": "what_may_remain_under_repeated_native_tests",
        "proof": "deferred_translation_layer_not_claimed",
        "termination": "classical_endpoint_translation_not_native_start",
    }

    native_language_objects = [
        "expansion",
        "discharge",
        "debt",
        "shadow",
        "regeneration",
        "compensation",
        "closure",
        "obstruction",
    ]

    learned_patterns = [
        {
            "pattern": "dangerous_language_exists",
            "meaning": "Collatz can generate dangerous native sentence forms.",
        },
        {
            "pattern": "danger_release_exists",
            "meaning": "Some dangerous native forms mutate toward release behavior.",
        },
        {
            "pattern": "dangerous_stability_exists",
            "meaning": "Some dangerous native forms remain stable in the bounded map.",
        },
        {
            "pattern": "obstruction_relevant_invariant_not_detected",
            "meaning": "No obstruction-relevant invariant candidate was detected in the bounded artifacts.",
        },
        {
            "pattern": "9780657630_is_a_stress_node",
            "meaning": "9780657630 repeatedly appears as a native grammar stress node, not as a proof object.",
        },
    ]

    forbidden_claims = [
        "collatz_solved",
        "proof_claimed",
        "global_closure_claimed",
        "global_invariant_claimed",
        "obstruction_impossible",
        "bounded_evidence_equals_theorem",
        "danger_release_equals_proof",
        "dangerous_stability_equals_obstruction",
        "termination_question_is_native_start",
    ]

    summary = {
        "version": VERSION,
        "layer": "native_language_summary",
        "status": "native_language_route_summarized",
        "source_invariant_version": invariant_certificate.get("version", invariant_map.get("version")),
        "source_invariant_candidate_count": invariant_certificate.get("invariant_candidate_count", invariant_map.get("invariant_candidate_count")),
        "source_danger_release_invariant_candidate_count": invariant_certificate.get("danger_release_invariant_candidate_count", invariant_map.get("danger_release_invariant_candidate_count")),
        "source_dangerous_stability_invariant_candidate_count": invariant_certificate.get("dangerous_stability_invariant_candidate_count", invariant_map.get("dangerous_stability_invariant_candidate_count")),
        "source_obstruction_relevant_invariant_candidate_count": invariant_certificate.get("obstruction_relevant_invariant_candidate_count", invariant_map.get("obstruction_relevant_invariant_candidate_count")),
        "route": route,
        "route_version_count": len(route),
        "native_language_objects": native_language_objects,
        "core_distinctions": core_distinctions,
        "learned_patterns": learned_patterns,
        "primary_position": "Collatz is not treated first as a conjecture to solve, but as a native dynamical language whose grammar can be observed, mapped, and only later translated.",
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "What has Collatz said when read as a native dynamical language?",
        "native_interpretation": "NATIVE_LANGUAGE_ROUTE_ESTABLISHED_WITHOUT_PROOF_CLAIM",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
        "collatz_status": "not_claimed_solved",
        "forbidden_claims": forbidden_claims,
        "next_recommended_version": "v4.1 Native Language README Consolidation",
    }

    return summary


def make_report(summary: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Language Summary")
    lines.append("")
    lines.append("Version: v4.0")
    lines.append("")
    lines.append(summary["primary_position"])
    lines.append("")
    lines.append("This is not a proof layer.")
    lines.append("")
    lines.append("This is not a solution claim.")
    lines.append("")
    lines.append("This is a native-language summary.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(summary["mother_rule"])
    lines.append("")
    lines.append("## Central native question")
    lines.append("")
    lines.append(summary["central_native_question"])
    lines.append("")
    lines.append("## Route")
    lines.append("")

    for item in summary["route"]:
        lines.append(
            f"- {item['version']} | {item['layer']} | {item['role']} | {item['question']}"
        )

    lines.append("")
    lines.append("## Core distinctions")
    lines.append("")

    for key, value in summary["core_distinctions"].items():
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("## Native language objects")
    lines.append("")

    for item in summary["native_language_objects"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Learned bounded patterns")
    lines.append("")

    for item in summary["learned_patterns"]:
        lines.append(f"- {item['pattern']}: {item['meaning']}")

    lines.append("")
    lines.append("## Current source summary")
    lines.append("")
    lines.append(f"- source_invariant_version: {summary['source_invariant_version']}")
    lines.append(f"- source_invariant_candidate_count: {summary['source_invariant_candidate_count']}")
    lines.append(f"- source_danger_release_invariant_candidate_count: {summary['source_danger_release_invariant_candidate_count']}")
    lines.append(f"- source_dangerous_stability_invariant_candidate_count: {summary['source_dangerous_stability_invariant_candidate_count']}")
    lines.append(f"- source_obstruction_relevant_invariant_candidate_count: {summary['source_obstruction_relevant_invariant_candidate_count']}")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(f"- proof_status: {summary['proof_status']}")
    lines.append(f"- theorem_status: {summary['theorem_status']}")
    lines.append(f"- global_closure_status: {summary['global_closure_status']}")
    lines.append(f"- global_invariant_status: {summary['global_invariant_status']}")
    lines.append(f"- collatz_status: {summary['collatz_status']}")
    lines.append("")
    lines.append("## Forbidden claims")
    lines.append("")

    for item in summary["forbidden_claims"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(summary["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_language_summary_certificate",
        "source_invariant_version": summary["source_invariant_version"],
        "source_invariant_candidate_count": summary["source_invariant_candidate_count"],
        "source_danger_release_invariant_candidate_count": summary["source_danger_release_invariant_candidate_count"],
        "source_dangerous_stability_invariant_candidate_count": summary["source_dangerous_stability_invariant_candidate_count"],
        "source_obstruction_relevant_invariant_candidate_count": summary["source_obstruction_relevant_invariant_candidate_count"],
        "route_version_count": summary["route_version_count"],
        "native_language_object_count": len(summary["native_language_objects"]),
        "learned_pattern_count": len(summary["learned_patterns"]),
        "primary_position": summary["primary_position"],
        "mother_rule": summary["mother_rule"],
        "central_native_question": summary["central_native_question"],
        "native_interpretation": summary["native_interpretation"],
        "proof_status": summary["proof_status"],
        "theorem_status": summary["theorem_status"],
        "global_closure_status": summary["global_closure_status"],
        "global_invariant_status": summary["global_invariant_status"],
        "collatz_status": summary["collatz_status"],
        "next_recommended_version": summary["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v4.0")
    print("=" * 80)
    print("Native Language Summary")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    invariant_map = read_json(INVARIANT_MAP_PATH)
    invariant_certificate = read_json(INVARIANT_CERTIFICATE_PATH)

    summary = build_summary(invariant_map, invariant_certificate)
    certificate = make_certificate(summary)
    report = make_report(summary)

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SUMMARY_REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    SUMMARY_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_invariant_version: {summary['source_invariant_version']}")
    print(f"source_invariant_candidate_count: {summary['source_invariant_candidate_count']}")
    print(f"source_danger_release_invariant_candidate_count: {summary['source_danger_release_invariant_candidate_count']}")
    print(f"source_dangerous_stability_invariant_candidate_count: {summary['source_dangerous_stability_invariant_candidate_count']}")
    print(f"source_obstruction_relevant_invariant_candidate_count: {summary['source_obstruction_relevant_invariant_candidate_count']}")
    print(f"route_version_count: {summary['route_version_count']}")
    print(f"native_language_object_count: {len(summary['native_language_objects'])}")
    print(f"learned_pattern_count: {len(summary['learned_patterns'])}")
    print(f"native_interpretation: {summary['native_interpretation']}")
    print(f"proof_status: {summary['proof_status']}")
    print(f"collatz_status: {summary['collatz_status']}")
    print(f"mother_rule: {summary['mother_rule']}")
    print(f"next: {summary['next_recommended_version']}")

    print(f"Wrote summary JSON to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote summary Markdown to: {SUMMARY_REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {SUMMARY_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
