#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.8

Native Conservation Map.

This builder reads the v3.7 stability map and asks:

What remains conserved across recurrence, mutation, and stability?

It does not solve Collatz.
It does not prove Collatz.
It does not treat bounded conservation as theorem.
It treats conservation as native-language behavior.

Outputs:
- results/native_conservation_map.json
- results/native_conservation_map.md
- results/native_conservation_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v3.8"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

STABILITY_MAP_PATH = RESULTS_DIR / "native_grammar_stability_map.json"
STABILITY_CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_stability_certificate.json"

CONSERVATION_MAP_PATH = RESULTS_DIR / "native_conservation_map.json"
CONSERVATION_REPORT_PATH = RESULTS_DIR / "native_conservation_map.md"
CONSERVATION_CERTIFICATE_PATH = RESULTS_DIR / "native_conservation_certificate.json"


def ensure_source_artifacts() -> None:
    if STABILITY_MAP_PATH.exists() and STABILITY_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_grammar_stability_map.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.7 native grammar stability map builder.")

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


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def conservation_candidate_from_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    stability_type = str(edge.get("stability_type", "unknown"))
    mutation_type = str(edge.get("mutation_type", "unknown"))
    from_family = str(edge.get("from_family", "unknown"))
    to_family = str(edge.get("to_family", "unknown"))
    from_class = str(edge.get("from_class", "unknown"))
    to_class = str(edge.get("to_class", "unknown"))

    conserved = []
    lost = []

    if from_family == to_family:
        conserved.append("family")
    else:
        lost.append("family")

    if from_class == to_class:
        conserved.append("class")
    else:
        lost.append("class")

    if "dangerous" in from_family and "dangerous" in to_family:
        conserved.append("danger")
    elif "dangerous" in from_family and "dangerous" not in to_family:
        lost.append("danger")
    elif "dangerous" not in from_family and "dangerous" in to_family:
        conserved.append("danger_emergence")

    if "release" in stability_type:
        conserved.append("release_behavior")

    if "unstable" in stability_type:
        conserved.append("instability_behavior")

    if "stable" in stability_type and "unstable" not in stability_type:
        conserved.append("stability_behavior")

    if "obstruction" in stability_type or "obstruction" in mutation_type:
        conserved.append("obstruction_relevance")

    if not conserved:
        conserved.append("transition_only")

    conservation_class = " + ".join(conserved)

    if "obstruction_relevance" in conserved:
        conservation_status = "obstruction_relevant_conservation"
    elif "danger" in conserved and "stability_behavior" in conserved:
        conservation_status = "dangerous_stability_conservation"
    elif "danger" in lost and "release_behavior" in conserved:
        conservation_status = "danger_release_conservation"
    elif "instability_behavior" in conserved:
        conservation_status = "instability_conservation"
    elif "stability_behavior" in conserved:
        conservation_status = "stability_conservation"
    else:
        conservation_status = "weak_conservation"

    return {
        "from_n0": edge.get("from_n0"),
        "to_n0": edge.get("to_n0"),
        "from_class": from_class,
        "to_class": to_class,
        "from_family": from_family,
        "to_family": to_family,
        "mutation_type": mutation_type,
        "stability_type": stability_type,
        "conserved_features": conserved,
        "lost_features": lost,
        "conservation_class": conservation_class,
        "conservation_status": conservation_status,
        "mutation_strength": safe_float(edge.get("mutation_strength"), 0.0),
        "native_interpretation": interpret_conservation(conservation_status),
    }


def interpret_conservation(status: str) -> str:
    if status == "obstruction_relevant_conservation":
        return "obstruction-relevant structure is conserved in the bounded map"
    if status == "dangerous_stability_conservation":
        return "danger persists together with stability"
    if status == "danger_release_conservation":
        return "danger tends to release rather than preserve itself"
    if status == "instability_conservation":
        return "instability itself is the conserved behavior"
    if status == "stability_conservation":
        return "stable grammar form is conserved"
    return "only weak conservation is visible"


def collect_stability_edges(stability_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    edges: List[Dict[str, Any]] = []

    for key in [
        "stable_edges",
        "unstable_edges",
        "dangerous_stable_edges",
        "dangerous_unstable_edges",
        "release_edges",
        "obstruction_relevant_edges",
        "near_9780657630_edges",
    ]:
        for edge in stability_map.get(key, []):
            item = dict(edge)
            item["source_list"] = key
            edges.append(item)

    seen = set()
    unique = []

    for edge in edges:
        identity = (
            edge.get("from_n0"),
            edge.get("to_n0"),
            edge.get("from_class"),
            edge.get("to_class"),
            edge.get("from_family"),
            edge.get("to_family"),
            edge.get("mutation_type"),
            edge.get("stability_type"),
        )
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(edge)

    return unique


def build_conservation_map(stability_map: Dict[str, Any], stability_certificate: Dict[str, Any]) -> Dict[str, Any]:
    edges = collect_stability_edges(stability_map)
    conservation_candidates = [conservation_candidate_from_edge(edge) for edge in edges]

    status_counts = Counter(item["conservation_status"] for item in conservation_candidates)
    class_counts = Counter(item["conservation_class"] for item in conservation_candidates)

    obstruction_relevant = [
        item for item in conservation_candidates
        if item["conservation_status"] == "obstruction_relevant_conservation"
    ]

    dangerous_stability = [
        item for item in conservation_candidates
        if item["conservation_status"] == "dangerous_stability_conservation"
    ]

    danger_release = [
        item for item in conservation_candidates
        if item["conservation_status"] == "danger_release_conservation"
    ]

    instability_conservation = [
        item for item in conservation_candidates
        if item["conservation_status"] == "instability_conservation"
    ]

    stability_conservation = [
        item for item in conservation_candidates
        if item["conservation_status"] == "stability_conservation"
    ]

    near_9780657630 = [
        item for item in conservation_candidates
        if abs(safe_int(item.get("from_n0")) - 9780657630) <= 8
        or abs(safe_int(item.get("to_n0")) - 9780657630) <= 8
    ]

    strongest_conservation = sorted(
        conservation_candidates,
        key=lambda item: item["mutation_strength"],
        reverse=True,
    )[:40]

    if obstruction_relevant:
        native_interpretation = "OBSTRUCTION_RELEVANT_CONSERVATION_PRESENT"
    elif dangerous_stability:
        native_interpretation = "DANGEROUS_STABILITY_CONSERVATION_PRESENT_WITHOUT_PROOF"
    elif danger_release:
        native_interpretation = "DANGER_RELEASE_IS_CONSERVED_IN_THIS_BOUNDED_MAP"
    elif instability_conservation:
        native_interpretation = "INSTABILITY_IS_THE_DOMINANT_CONSERVED_NATIVE_BEHAVIOR"
    else:
        native_interpretation = "ONLY_WEAK_NATIVE_CONSERVATION_DETECTED"

    total = max(1, len(conservation_candidates))

    conservation_map = {
        "version": VERSION,
        "layer": "native_conservation_map",
        "source_stability_version": stability_certificate.get("version", stability_map.get("version")),
        "source_stability_edge_count": stability_certificate.get("stability_edge_count", stability_map.get("stability_edge_count")),
        "source_dangerous_stable_edge_count": stability_certificate.get("dangerous_stable_edge_count", stability_map.get("dangerous_stable_edge_count")),
        "source_dangerous_unstable_edge_count": stability_certificate.get("dangerous_unstable_edge_count", stability_map.get("dangerous_unstable_edge_count")),
        "source_release_edge_count": stability_certificate.get("release_edge_count", stability_map.get("release_edge_count")),
        "conservation_candidate_count": len(conservation_candidates),
        "conservation_status_counts": dict(status_counts),
        "conservation_class_counts": dict(class_counts),
        "obstruction_relevant_conservation_count": len(obstruction_relevant),
        "dangerous_stability_conservation_count": len(dangerous_stability),
        "danger_release_conservation_count": len(danger_release),
        "instability_conservation_count": len(instability_conservation),
        "stability_conservation_count": len(stability_conservation),
        "obstruction_detected": len(obstruction_relevant) > 0,
        "danger_release_conservation_ratio": len(danger_release) / total,
        "instability_conservation_ratio": len(instability_conservation) / total,
        "dangerous_stability_conservation_ratio": len(dangerous_stability) / total,
        "obstruction_relevant_conservation_ratio": len(obstruction_relevant) / total,
        "strongest_conservation_candidates": strongest_conservation,
        "danger_release_conservation_candidates": danger_release[:40],
        "instability_conservation_candidates": instability_conservation[:40],
        "dangerous_stability_conservation_candidates": dangerous_stability[:40],
        "obstruction_relevant_conservation_candidates": obstruction_relevant[:40],
        "near_9780657630_conservation": near_9780657630[:40],
        "native_interpretation": native_interpretation,
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "What remains conserved across recurrence, mutation, and stability?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "Bounded conservation signals do not imply global theorem or global closure.",
        "next_recommended_version": "v3.9 Native Invariant Candidate Map",
    }

    return conservation_map


def make_report(conservation_map: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Conservation Map")
    lines.append("")
    lines.append("Version: v3.8")
    lines.append("")
    lines.append("This report asks what remains conserved across recurrence, mutation, and stability.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(conservation_map["mother_rule"])
    lines.append("")
    lines.append("## Central native question")
    lines.append("")
    lines.append(conservation_map["central_native_question"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    keys = [
        "source_stability_version",
        "source_stability_edge_count",
        "conservation_candidate_count",
        "obstruction_relevant_conservation_count",
        "dangerous_stability_conservation_count",
        "danger_release_conservation_count",
        "instability_conservation_count",
        "stability_conservation_count",
        "obstruction_detected",
        "danger_release_conservation_ratio",
        "instability_conservation_ratio",
        "dangerous_stability_conservation_ratio",
        "obstruction_relevant_conservation_ratio",
        "native_interpretation",
        "proof_status",
    ]

    for key in keys:
        lines.append(f"- {key}: {conservation_map[key]}")

    lines.append("")
    lines.append("## Conservation status counts")
    lines.append("")

    for key, value in sorted(conservation_map["conservation_status_counts"].items()):
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("## Strongest conservation candidates")
    lines.append("")

    for item in conservation_map["strongest_conservation_candidates"][:20]:
        lines.append(
            f"- {item.get('from_n0')} -> {item.get('to_n0')} "
            f"status={item.get('conservation_status')} "
            f"class={item.get('conservation_class')} "
            f"strength={item.get('mutation_strength')}"
        )

    lines.append("")
    lines.append("## Danger-release conservation")
    lines.append("")

    if not conservation_map["danger_release_conservation_candidates"]:
        lines.append("- none observed")
    else:
        for item in conservation_map["danger_release_conservation_candidates"][:20]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"{item.get('from_class')} -> {item.get('to_class')}"
            )

    lines.append("")
    lines.append("## Dangerous-stability conservation")
    lines.append("")

    if not conservation_map["dangerous_stability_conservation_candidates"]:
        lines.append("- none observed in this bounded conservation map")
    else:
        for item in conservation_map["dangerous_stability_conservation_candidates"][:20]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"{item.get('from_class')} -> {item.get('to_class')}"
            )

    lines.append("")
    lines.append("## Near 9780657630")
    lines.append("")

    if not conservation_map["near_9780657630_conservation"]:
        lines.append("- no conservation candidates near 9780657630 in this bounded map")
    else:
        for item in conservation_map["near_9780657630_conservation"][:20]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"status={item.get('conservation_status')} "
                f"class={item.get('conservation_class')}"
            )

    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(conservation_map["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(conservation_map["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(conservation_map: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_conservation_certificate",
        "source_stability_version": conservation_map["source_stability_version"],
        "source_stability_edge_count": conservation_map["source_stability_edge_count"],
        "conservation_candidate_count": conservation_map["conservation_candidate_count"],
        "obstruction_relevant_conservation_count": conservation_map["obstruction_relevant_conservation_count"],
        "dangerous_stability_conservation_count": conservation_map["dangerous_stability_conservation_count"],
        "danger_release_conservation_count": conservation_map["danger_release_conservation_count"],
        "instability_conservation_count": conservation_map["instability_conservation_count"],
        "stability_conservation_count": conservation_map["stability_conservation_count"],
        "obstruction_detected": conservation_map["obstruction_detected"],
        "danger_release_conservation_ratio": conservation_map["danger_release_conservation_ratio"],
        "instability_conservation_ratio": conservation_map["instability_conservation_ratio"],
        "dangerous_stability_conservation_ratio": conservation_map["dangerous_stability_conservation_ratio"],
        "obstruction_relevant_conservation_ratio": conservation_map["obstruction_relevant_conservation_ratio"],
        "native_interpretation": conservation_map["native_interpretation"],
        "mother_rule": conservation_map["mother_rule"],
        "central_native_question": conservation_map["central_native_question"],
        "proof_status": conservation_map["proof_status"],
        "theorem_status": conservation_map["theorem_status"],
        "negative_result_boundary": conservation_map["negative_result_boundary"],
        "next_recommended_version": conservation_map["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.8")
    print("=" * 80)
    print("Native Conservation Map")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    stability_map = read_json(STABILITY_MAP_PATH)
    stability_certificate = read_json(STABILITY_CERTIFICATE_PATH)

    conservation_map = build_conservation_map(stability_map, stability_certificate)
    certificate = make_certificate(conservation_map)
    report = make_report(conservation_map)

    CONSERVATION_MAP_PATH.write_text(json.dumps(conservation_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CONSERVATION_REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    CONSERVATION_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_stability_version: {conservation_map['source_stability_version']}")
    print(f"source_stability_edge_count: {conservation_map['source_stability_edge_count']}")
    print(f"conservation_candidate_count: {conservation_map['conservation_candidate_count']}")
    print(f"obstruction_relevant_conservation_count: {conservation_map['obstruction_relevant_conservation_count']}")
    print(f"dangerous_stability_conservation_count: {conservation_map['dangerous_stability_conservation_count']}")
    print(f"danger_release_conservation_count: {conservation_map['danger_release_conservation_count']}")
    print(f"instability_conservation_count: {conservation_map['instability_conservation_count']}")
    print(f"stability_conservation_count: {conservation_map['stability_conservation_count']}")
    print(f"obstruction_detected: {conservation_map['obstruction_detected']}")
    print(f"native_interpretation: {conservation_map['native_interpretation']}")
    print(f"proof_status: {conservation_map['proof_status']}")
    print(f"mother_rule: {conservation_map['mother_rule']}")
    print(f"next: {conservation_map['next_recommended_version']}")

    print(f"Wrote conservation map JSON to: {CONSERVATION_MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote conservation map Markdown to: {CONSERVATION_REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CONSERVATION_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
