#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.6

Native Grammar Mutation Atlas.

This builder reads the v3.5 recurrence map and turns recurrence edges into
a mutation atlas.

It does not solve Collatz.
It does not prove Collatz.
It does not treat dangerous mutation as obstruction.

It asks:
How does one native sentence transform into another?

Outputs:
- results/native_grammar_mutation_atlas.json
- results/native_grammar_mutation_atlas.md
- results/native_grammar_mutation_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


VERSION = "v3.6"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

RECURRENCE_MAP_PATH = RESULTS_DIR / "native_grammar_recurrence_map.json"
RECURRENCE_CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_recurrence_certificate.json"

ATLAS_PATH = RESULTS_DIR / "native_grammar_mutation_atlas.json"
REPORT_PATH = RESULTS_DIR / "native_grammar_mutation_atlas.md"
CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_mutation_certificate.json"


def ensure_source_artifacts() -> None:
    if RECURRENCE_MAP_PATH.exists() and RECURRENCE_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_grammar_recurrence_map.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.5 native grammar recurrence map builder.")

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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def collect_edges(recurrence_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    edges: List[Dict[str, Any]] = []

    for key in ["strongest_mutation_edges", "dangerous_to_non_obstruction_edges"]:
        for edge in recurrence_map.get(key, []):
            edge_copy = dict(edge)
            edge_copy["source_list"] = key
            edges.append(edge_copy)

    seen = set()
    unique_edges = []

    for edge in edges:
        identity = (
            edge.get("from_n0"),
            edge.get("to_n0"),
            edge.get("from_class"),
            edge.get("to_class"),
            edge.get("transition_label"),
        )
        if identity in seen:
            continue
        seen.add(identity)
        unique_edges.append(edge)

    return unique_edges


def classify_mutation(edge: Dict[str, Any]) -> str:
    label = str(edge.get("transition_label", "unknown"))
    from_family = str(edge.get("from_family", "unknown"))
    to_family = str(edge.get("to_family", "unknown"))

    if label == "repeat":
        return "stable_repeat_mutation"

    if label == "family_mutation":
        return "within_family_mutation"

    if label == "dangerous_to_non_obstruction":
        return "dangerous_release_mutation"

    if label == "toward_obstruction_candidate":
        return "toward_obstruction_mutation"

    if label == "recovery_to_regeneration":
        return "recovery_to_regeneration_mutation"

    if label == "regeneration_to_recovery":
        return "regeneration_to_recovery_mutation"

    if from_family == "dangerous_regeneration_family" and to_family == "dangerous_regeneration_family":
        return "dangerous_persistence_mutation"

    if from_family != to_family:
        return "cross_family_mutation"

    return "unclassified_mutation"


def mutation_strength(edge: Dict[str, Any]) -> float:
    score_delta = abs(as_float(edge.get("recovery_score_delta"), 0.0))
    debt_delta = abs(as_float(edge.get("debt_window_delta"), 0.0))
    dangerous_delta = abs(as_float(edge.get("dangerous_regeneration_delta"), 0.0))
    obstruction_delta = abs(as_float(edge.get("obstruction_candidate_delta"), 0.0))

    return score_delta + debt_delta + dangerous_delta * 10.0 + obstruction_delta * 1000.0


def enrich_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    enriched = dict(edge)
    enriched["mutation_type"] = classify_mutation(edge)
    enriched["mutation_strength"] = mutation_strength(edge)
    enriched["native_interpretation"] = interpret_mutation(enriched)
    return enriched


def interpret_mutation(edge: Dict[str, Any]) -> str:
    mutation_type = edge["mutation_type"]

    if mutation_type == "dangerous_release_mutation":
        return "dangerous sentence changes without becoming obstruction"

    if mutation_type == "dangerous_persistence_mutation":
        return "dangerous sentence remains in dangerous family"

    if mutation_type == "toward_obstruction_mutation":
        return "mutation points toward obstruction-candidate family"

    if mutation_type == "recovery_to_regeneration_mutation":
        return "recovery is followed by renewed debt expression"

    if mutation_type == "regeneration_to_recovery_mutation":
        return "regeneration is followed by recovery behavior"

    if mutation_type == "stable_repeat_mutation":
        return "same sentence class repeats"

    if mutation_type == "within_family_mutation":
        return "sentence mutates inside the same native family"

    if mutation_type == "cross_family_mutation":
        return "sentence crosses native family boundary"

    return "mutation remains unclassified"


def build_mutation_atlas(recurrence_map: Dict[str, Any], recurrence_certificate: Dict[str, Any]) -> Dict[str, Any]:
    seed_edges = collect_edges(recurrence_map)
    enriched_edges = [enrich_edge(edge) for edge in seed_edges]

    mutation_type_counts = Counter(edge["mutation_type"] for edge in enriched_edges)
    transition_label_counts = Counter(str(edge.get("transition_label", "unknown")) for edge in enriched_edges)
    family_pair_counts = Counter(
        (str(edge.get("from_family", "unknown")), str(edge.get("to_family", "unknown")))
        for edge in enriched_edges
    )
    class_pair_counts = Counter(
        (str(edge.get("from_class", "unknown")), str(edge.get("to_class", "unknown")))
        for edge in enriched_edges
    )

    dangerous_mutations = [
        edge for edge in enriched_edges
        if "dangerous" in edge["mutation_type"]
        or "dangerous" in str(edge.get("from_family", ""))
        or "dangerous" in str(edge.get("to_family", ""))
    ]

    obstruction_mutations = [
        edge for edge in enriched_edges
        if "obstruction" in edge["mutation_type"]
        or "obstruction" in str(edge.get("from_family", ""))
        or "obstruction" in str(edge.get("to_family", ""))
    ]

    release_mutations = [
        edge for edge in enriched_edges
        if edge["mutation_type"] == "dangerous_release_mutation"
    ]

    persistence_mutations = [
        edge for edge in enriched_edges
        if edge["mutation_type"] == "dangerous_persistence_mutation"
    ]

    strongest_mutations = sorted(
        enriched_edges,
        key=lambda edge: edge["mutation_strength"],
        reverse=True,
    )[:30]

    near_9780657630 = [
        edge for edge in enriched_edges
        if abs(as_int(edge.get("from_n0")) - 9780657630) <= 8
        or abs(as_int(edge.get("to_n0")) - 9780657630) <= 8
    ]

    family_profiles = [
        {
            "from_family": key[0],
            "to_family": key[1],
            "count": value,
        }
        for key, value in family_pair_counts.most_common()
    ]

    class_profiles = [
        {
            "from_class": key[0],
            "to_class": key[1],
            "count": value,
        }
        for key, value in class_pair_counts.most_common()
    ]

    native_interpretation = (
        "OBSTRUCTION_MUTATION_PRESENT"
        if obstruction_mutations
        else "DANGEROUS_MUTATIONS_PRESENT_WITHOUT_OBSTRUCTION_MUTATION"
        if dangerous_mutations
        else "NO_DANGEROUS_MUTATION_PRESENT"
    )

    atlas = {
        "version": VERSION,
        "layer": "native_grammar_mutation_atlas",
        "source_recurrence_version": recurrence_certificate.get("version", recurrence_map.get("version")),
        "source_sentence_count": recurrence_certificate.get("sentence_count", recurrence_map.get("sentence_count")),
        "source_total_edge_count": recurrence_certificate.get("total_edge_count", recurrence_map.get("total_edge_count")),
        "mutation_edge_count": len(enriched_edges),
        "mutation_type_counts": dict(mutation_type_counts),
        "transition_label_counts": dict(transition_label_counts),
        "family_mutation_profiles": family_profiles,
        "class_mutation_profiles": class_profiles[:40],
        "dangerous_mutation_count": len(dangerous_mutations),
        "dangerous_release_mutation_count": len(release_mutations),
        "dangerous_persistence_mutation_count": len(persistence_mutations),
        "obstruction_mutation_count": len(obstruction_mutations),
        "obstruction_detected": len(obstruction_mutations) > 0,
        "strongest_mutations": strongest_mutations,
        "dangerous_mutations": dangerous_mutations[:40],
        "dangerous_release_mutations": release_mutations[:40],
        "dangerous_persistence_mutations": persistence_mutations[:40],
        "near_9780657630_mutations": near_9780657630[:40],
        "native_interpretation": native_interpretation,
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "How does one native sentence transform into another?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction mutation detected in this bounded mutation atlas is not proof that obstruction mutation cannot exist.",
        "next_recommended_version": "v3.7 Native Grammar Stability Map",
    }

    return atlas


def make_report(atlas: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Grammar Mutation Atlas")
    lines.append("")
    lines.append("Version: v3.6")
    lines.append("")
    lines.append("This report maps how native sentence forms transform.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("It treats mutation as native-language behavior.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(atlas["mother_rule"])
    lines.append("")
    lines.append("## Central native question")
    lines.append("")
    lines.append(atlas["central_native_question"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- source_recurrence_version: {atlas['source_recurrence_version']}")
    lines.append(f"- source_sentence_count: {atlas['source_sentence_count']}")
    lines.append(f"- source_total_edge_count: {atlas['source_total_edge_count']}")
    lines.append(f"- mutation_edge_count: {atlas['mutation_edge_count']}")
    lines.append(f"- dangerous_mutation_count: {atlas['dangerous_mutation_count']}")
    lines.append(f"- dangerous_release_mutation_count: {atlas['dangerous_release_mutation_count']}")
    lines.append(f"- dangerous_persistence_mutation_count: {atlas['dangerous_persistence_mutation_count']}")
    lines.append(f"- obstruction_mutation_count: {atlas['obstruction_mutation_count']}")
    lines.append(f"- obstruction_detected: {atlas['obstruction_detected']}")
    lines.append(f"- native_interpretation: {atlas['native_interpretation']}")
    lines.append(f"- proof_status: {atlas['proof_status']}")
    lines.append("")
    lines.append("## Mutation type counts")
    lines.append("")
    for key, value in sorted(atlas["mutation_type_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Family mutation profiles")
    lines.append("")
    for item in atlas["family_mutation_profiles"][:20]:
        lines.append(f"- {item['from_family']} -> {item['to_family']}: {item['count']}")
    lines.append("")
    lines.append("## Class mutation profiles")
    lines.append("")
    for item in atlas["class_mutation_profiles"][:20]:
        lines.append(f"- {item['from_class']} -> {item['to_class']}: {item['count']}")
    lines.append("")
    lines.append("## Strongest mutations")
    lines.append("")
    for edge in atlas["strongest_mutations"][:20]:
        lines.append(
            f"- {edge.get('from_n0')} -> {edge.get('to_n0')} "
            f"{edge.get('from_class')} -> {edge.get('to_class')} "
            f"type={edge.get('mutation_type')} strength={edge.get('mutation_strength')}"
        )
    lines.append("")
    lines.append("## Dangerous release mutations")
    lines.append("")
    for edge in atlas["dangerous_release_mutations"][:20]:
        lines.append(
            f"- {edge.get('from_n0')} -> {edge.get('to_n0')} "
            f"{edge.get('from_class')} -> {edge.get('to_class')}"
        )
    lines.append("")
    lines.append("## Near 9780657630 mutations")
    lines.append("")
    for edge in atlas["near_9780657630_mutations"][:20]:
        lines.append(
            f"- {edge.get('from_n0')} -> {edge.get('to_n0')} "
            f"{edge.get('from_class')} -> {edge.get('to_class')} "
            f"type={edge.get('mutation_type')}"
        )
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(atlas["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(atlas["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(atlas: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_grammar_mutation_certificate",
        "source_recurrence_version": atlas["source_recurrence_version"],
        "source_sentence_count": atlas["source_sentence_count"],
        "source_total_edge_count": atlas["source_total_edge_count"],
        "mutation_edge_count": atlas["mutation_edge_count"],
        "dangerous_mutation_count": atlas["dangerous_mutation_count"],
        "dangerous_release_mutation_count": atlas["dangerous_release_mutation_count"],
        "dangerous_persistence_mutation_count": atlas["dangerous_persistence_mutation_count"],
        "obstruction_mutation_count": atlas["obstruction_mutation_count"],
        "obstruction_detected": atlas["obstruction_detected"],
        "native_interpretation": atlas["native_interpretation"],
        "mother_rule": atlas["mother_rule"],
        "central_native_question": atlas["central_native_question"],
        "proof_status": atlas["proof_status"],
        "theorem_status": atlas["theorem_status"],
        "negative_result_boundary": atlas["negative_result_boundary"],
        "next_recommended_version": atlas["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.6")
    print("=" * 80)
    print("Native Grammar Mutation Atlas")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    recurrence_map = read_json(RECURRENCE_MAP_PATH)
    recurrence_certificate = read_json(RECURRENCE_CERTIFICATE_PATH)

    atlas = build_mutation_atlas(recurrence_map, recurrence_certificate)
    certificate = make_certificate(atlas)
    report = make_report(atlas)

    ATLAS_PATH.write_text(json.dumps(atlas, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_recurrence_version: {atlas['source_recurrence_version']}")
    print(f"source_sentence_count: {atlas['source_sentence_count']}")
    print(f"source_total_edge_count: {atlas['source_total_edge_count']}")
    print(f"mutation_edge_count: {atlas['mutation_edge_count']}")
    print(f"dangerous_mutation_count: {atlas['dangerous_mutation_count']}")
    print(f"dangerous_release_mutation_count: {atlas['dangerous_release_mutation_count']}")
    print(f"dangerous_persistence_mutation_count: {atlas['dangerous_persistence_mutation_count']}")
    print(f"obstruction_mutation_count: {atlas['obstruction_mutation_count']}")
    print(f"obstruction_detected: {atlas['obstruction_detected']}")
    print(f"native_interpretation: {atlas['native_interpretation']}")
    print(f"proof_status: {atlas['proof_status']}")
    print(f"mother_rule: {atlas['mother_rule']}")
    print(f"next: {atlas['next_recommended_version']}")

    print(f"Wrote mutation atlas JSON to: {ATLAS_PATH.relative_to(ROOT)}")
    print(f"Wrote mutation atlas Markdown to: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
