#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.7

Native Grammar Stability Map.

This builder reads the v3.6 mutation atlas and asks:

What does Collatz preserve in its own grammar?

It does not solve Collatz.
It does not prove Collatz.
It does not treat stability as proof.
It does not treat instability as failure.

Outputs:
- results/native_grammar_stability_map.json
- results/native_grammar_stability_map.md
- results/native_grammar_stability_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


VERSION = "v3.7"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

MUTATION_ATLAS_PATH = RESULTS_DIR / "native_grammar_mutation_atlas.json"
MUTATION_CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_mutation_certificate.json"

STABILITY_MAP_PATH = RESULTS_DIR / "native_grammar_stability_map.json"
STABILITY_REPORT_PATH = RESULTS_DIR / "native_grammar_stability_map.md"
STABILITY_CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_stability_certificate.json"


def ensure_source_artifacts() -> None:
    if MUTATION_ATLAS_PATH.exists() and MUTATION_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_grammar_mutation_atlas.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.6 native grammar mutation atlas builder.")

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


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def collect_mutations(atlas: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []

    for key in [
        "strongest_mutations",
        "dangerous_mutations",
        "dangerous_release_mutations",
        "dangerous_persistence_mutations",
        "near_9780657630_mutations",
    ]:
        for item in atlas.get(key, []):
            item_copy = dict(item)
            item_copy["source_list"] = key
            candidates.append(item_copy)

    seen = set()
    unique: List[Dict[str, Any]] = []

    for item in candidates:
        identity = (
            item.get("from_n0"),
            item.get("to_n0"),
            item.get("from_class"),
            item.get("to_class"),
            item.get("from_family"),
            item.get("to_family"),
            item.get("mutation_type"),
            item.get("transition_label"),
        )
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(item)

    return unique


def edge_stability_type(edge: Dict[str, Any]) -> str:
    mutation_type = str(edge.get("mutation_type", "unknown"))
    from_class = str(edge.get("from_class", "unknown"))
    to_class = str(edge.get("to_class", "unknown"))
    from_family = str(edge.get("from_family", "unknown"))
    to_family = str(edge.get("to_family", "unknown"))

    if "obstruction" in mutation_type or "obstruction" in from_family or "obstruction" in to_family:
        return "obstruction_relevant_stability_signal"

    if mutation_type == "stable_repeat_mutation" or from_class == to_class:
        if "dangerous" in from_class or "dangerous" in to_class:
            return "dangerous_class_stable"
        return "class_stable"

    if from_family == to_family:
        if "dangerous" in from_family:
            return "dangerous_family_stable"
        return "family_stable"

    if mutation_type == "dangerous_release_mutation":
        return "dangerous_unstable_release"

    if "dangerous" in from_family and "dangerous" not in to_family:
        return "dangerous_unstable_release"

    if "dangerous" not in from_family and "dangerous" in to_family:
        return "toward_dangerous_transition"

    if from_family != to_family:
        return "cross_family_unstable"

    return "undecided_stability"


def node_key(value: Any) -> str:
    return str(value)


def build_node_profiles(edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    profiles: Dict[str, Dict[str, Any]] = {}

    def ensure(n0: Any) -> Dict[str, Any]:
        key = node_key(n0)
        if key not in profiles:
            profiles[key] = {
                "n0": safe_int(n0),
                "outgoing_count": 0,
                "incoming_count": 0,
                "stable_outgoing_count": 0,
                "unstable_outgoing_count": 0,
                "dangerous_outgoing_count": 0,
                "release_outgoing_count": 0,
                "obstruction_relevant_count": 0,
                "max_mutation_strength": 0.0,
                "classes_seen": [],
                "families_seen": [],
            }
        return profiles[key]

    for edge in edges:
        from_n0 = edge.get("from_n0")
        to_n0 = edge.get("to_n0")
        stability_type = edge.get("stability_type", edge_stability_type(edge))
        strength = safe_float(edge.get("mutation_strength"), 0.0)

        source = ensure(from_n0)
        target = ensure(to_n0)

        source["outgoing_count"] += 1
        target["incoming_count"] += 1

        if "stable" in stability_type and "unstable" not in stability_type:
            source["stable_outgoing_count"] += 1

        if "unstable" in stability_type or "release" in stability_type or "transition" in stability_type:
            source["unstable_outgoing_count"] += 1

        if "dangerous" in stability_type:
            source["dangerous_outgoing_count"] += 1

        if "release" in stability_type:
            source["release_outgoing_count"] += 1

        if "obstruction" in stability_type:
            source["obstruction_relevant_count"] += 1

        source["max_mutation_strength"] = max(source["max_mutation_strength"], strength)

        for class_key in ["from_class", "to_class"]:
            value = str(edge.get(class_key, "unknown"))
            if value not in source["classes_seen"]:
                source["classes_seen"].append(value)

        for family_key in ["from_family", "to_family"]:
            value = str(edge.get(family_key, "unknown"))
            if value not in source["families_seen"]:
                source["families_seen"].append(value)

    output = []
    for profile in profiles.values():
        outgoing = profile["outgoing_count"]
        stable = profile["stable_outgoing_count"]
        release = profile["release_outgoing_count"]
        dangerous = profile["dangerous_outgoing_count"]

        profile["stability_ratio"] = stable / outgoing if outgoing else 0.0
        profile["release_ratio"] = release / outgoing if outgoing else 0.0
        profile["dangerous_ratio"] = dangerous / outgoing if outgoing else 0.0

        if profile["obstruction_relevant_count"] > 0:
            profile["node_role"] = "obstruction_relevant_node"
        elif profile["release_ratio"] > 0:
            profile["node_role"] = "release_node"
        elif profile["dangerous_ratio"] > 0 and profile["stability_ratio"] > 0:
            profile["node_role"] = "dangerous_stability_node"
        elif profile["stability_ratio"] > 0:
            profile["node_role"] = "stable_node"
        elif outgoing > 0:
            profile["node_role"] = "transition_node"
        else:
            profile["node_role"] = "incoming_only_node"

        output.append(profile)

    return sorted(
        output,
        key=lambda item: (
            item["obstruction_relevant_count"],
            item["max_mutation_strength"],
            item["outgoing_count"],
        ),
        reverse=True,
    )


def build_stability_map(mutation_atlas: Dict[str, Any], mutation_certificate: Dict[str, Any]) -> Dict[str, Any]:
    raw_edges = collect_mutations(mutation_atlas)
    enriched_edges = []

    for edge in raw_edges:
        copy = dict(edge)
        copy["stability_type"] = edge_stability_type(copy)
        enriched_edges.append(copy)

    stability_type_counts = Counter(edge["stability_type"] for edge in enriched_edges)
    mutation_type_counts = Counter(str(edge.get("mutation_type", "unknown")) for edge in enriched_edges)
    family_pair_counts = Counter(
        (str(edge.get("from_family", "unknown")), str(edge.get("to_family", "unknown")))
        for edge in enriched_edges
    )
    class_pair_counts = Counter(
        (str(edge.get("from_class", "unknown")), str(edge.get("to_class", "unknown")))
        for edge in enriched_edges
    )

    stable_edges = [
        edge for edge in enriched_edges
        if "stable" in edge["stability_type"] and "unstable" not in edge["stability_type"]
    ]
    unstable_edges = [
        edge for edge in enriched_edges
        if "unstable" in edge["stability_type"]
        or "release" in edge["stability_type"]
        or "transition" in edge["stability_type"]
    ]
    dangerous_stable_edges = [
        edge for edge in stable_edges
        if "dangerous" in edge["stability_type"]
    ]
    dangerous_unstable_edges = [
        edge for edge in unstable_edges
        if "dangerous" in edge["stability_type"]
    ]
    release_edges = [
        edge for edge in enriched_edges
        if "release" in edge["stability_type"]
    ]
    obstruction_relevant_edges = [
        edge for edge in enriched_edges
        if "obstruction" in edge["stability_type"]
    ]

    node_profiles = build_node_profiles(enriched_edges)

    near_9780657630_nodes = [
        profile for profile in node_profiles
        if abs(safe_int(profile["n0"]) - 9780657630) <= 8
    ]

    near_9780657630_edges = [
        edge for edge in enriched_edges
        if abs(safe_int(edge.get("from_n0")) - 9780657630) <= 8
        or abs(safe_int(edge.get("to_n0")) - 9780657630) <= 8
    ]

    stability_score = (
        len(stable_edges) / len(enriched_edges)
        if enriched_edges
        else 0.0
    )
    release_score = (
        len(release_edges) / len(enriched_edges)
        if enriched_edges
        else 0.0
    )
    dangerous_instability_score = (
        len(dangerous_unstable_edges) / max(1, len(dangerous_stable_edges) + len(dangerous_unstable_edges))
    )

    if obstruction_relevant_edges:
        native_interpretation = "OBSTRUCTION_RELEVANT_STABILITY_SIGNAL_PRESENT"
    elif dangerous_unstable_edges and not dangerous_stable_edges:
        native_interpretation = "DANGEROUS_GRAMMAR_APPEARS_UNSTABLE_IN_THIS_ATLAS"
    elif dangerous_stable_edges:
        native_interpretation = "DANGEROUS_GRAMMAR_STABILITY_SIGNAL_PRESENT_WITHOUT_OBSTRUCTION"
    else:
        native_interpretation = "NO_DANGEROUS_STABILITY_SIGNAL_DETECTED"

    stability_map = {
        "version": VERSION,
        "layer": "native_grammar_stability_map",
        "source_mutation_version": mutation_certificate.get("version", mutation_atlas.get("version")),
        "source_mutation_edge_count": mutation_certificate.get("mutation_edge_count", mutation_atlas.get("mutation_edge_count")),
        "source_dangerous_mutation_count": mutation_certificate.get("dangerous_mutation_count", mutation_atlas.get("dangerous_mutation_count")),
        "source_obstruction_mutation_count": mutation_certificate.get("obstruction_mutation_count", mutation_atlas.get("obstruction_mutation_count")),
        "stability_edge_count": len(enriched_edges),
        "stable_edge_count": len(stable_edges),
        "unstable_edge_count": len(unstable_edges),
        "dangerous_stable_edge_count": len(dangerous_stable_edges),
        "dangerous_unstable_edge_count": len(dangerous_unstable_edges),
        "release_edge_count": len(release_edges),
        "obstruction_relevant_edge_count": len(obstruction_relevant_edges),
        "obstruction_detected": len(obstruction_relevant_edges) > 0,
        "stability_score": stability_score,
        "release_score": release_score,
        "dangerous_instability_score": dangerous_instability_score,
        "stability_type_counts": dict(stability_type_counts),
        "mutation_type_counts": dict(mutation_type_counts),
        "family_pair_counts": [
            {"from_family": key[0], "to_family": key[1], "count": value}
            for key, value in family_pair_counts.most_common()
        ],
        "class_pair_counts": [
            {"from_class": key[0], "to_class": key[1], "count": value}
            for key, value in class_pair_counts.most_common()
        ],
        "stable_edges": stable_edges[:40],
        "unstable_edges": unstable_edges[:40],
        "dangerous_stable_edges": dangerous_stable_edges[:40],
        "dangerous_unstable_edges": dangerous_unstable_edges[:40],
        "release_edges": release_edges[:40],
        "obstruction_relevant_edges": obstruction_relevant_edges[:40],
        "node_profiles": node_profiles[:60],
        "near_9780657630_nodes": near_9780657630_nodes[:40],
        "near_9780657630_edges": near_9780657630_edges[:40],
        "native_interpretation": native_interpretation,
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "What does Collatz preserve under recurrence and mutation?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction-stable grammar detected in this bounded stability map is not proof that obstruction-stable grammar cannot exist.",
        "next_recommended_version": "v3.8 Native Conservation Map",
    }

    return stability_map


def make_report(stability_map: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Grammar Stability Map")
    lines.append("")
    lines.append("Version: v3.7")
    lines.append("")
    lines.append("This report studies what Collatz preserves in its own grammar.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("It asks what remains stable under recurrence and mutation.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(stability_map["mother_rule"])
    lines.append("")
    lines.append("## Central native question")
    lines.append("")
    lines.append(stability_map["central_native_question"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    keys = [
        "source_mutation_version",
        "source_mutation_edge_count",
        "stability_edge_count",
        "stable_edge_count",
        "unstable_edge_count",
        "dangerous_stable_edge_count",
        "dangerous_unstable_edge_count",
        "release_edge_count",
        "obstruction_relevant_edge_count",
        "obstruction_detected",
        "stability_score",
        "release_score",
        "dangerous_instability_score",
        "native_interpretation",
        "proof_status",
    ]
    for key in keys:
        lines.append(f"- {key}: {stability_map[key]}")
    lines.append("")
    lines.append("## Stability type counts")
    lines.append("")
    for key, value in sorted(stability_map["stability_type_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Strong node profiles")
    lines.append("")
    for profile in stability_map["node_profiles"][:20]:
        lines.append(
            f"- n0={profile['n0']} role={profile['node_role']} "
            f"out={profile['outgoing_count']} in={profile['incoming_count']} "
            f"stable_ratio={profile['stability_ratio']} release_ratio={profile['release_ratio']} "
            f"dangerous_ratio={profile['dangerous_ratio']}"
        )
    lines.append("")
    lines.append("## Dangerous unstable edges")
    lines.append("")
    for edge in stability_map["dangerous_unstable_edges"][:20]:
        lines.append(
            f"- {edge.get('from_n0')} -> {edge.get('to_n0')} "
            f"{edge.get('from_class')} -> {edge.get('to_class')} "
            f"type={edge.get('stability_type')}"
        )
    lines.append("")
    lines.append("## Dangerous stable edges")
    lines.append("")
    if not stability_map["dangerous_stable_edges"]:
        lines.append("- none observed in this bounded stability map")
    else:
        for edge in stability_map["dangerous_stable_edges"][:20]:
            lines.append(
                f"- {edge.get('from_n0')} -> {edge.get('to_n0')} "
                f"{edge.get('from_class')} -> {edge.get('to_class')} "
                f"type={edge.get('stability_type')}"
            )
    lines.append("")
    lines.append("## Near 9780657630")
    lines.append("")
    for profile in stability_map["near_9780657630_nodes"][:20]:
        lines.append(
            f"- n0={profile['n0']} role={profile['node_role']} "
            f"out={profile['outgoing_count']} stable_ratio={profile['stability_ratio']} "
            f"release_ratio={profile['release_ratio']} dangerous_ratio={profile['dangerous_ratio']}"
        )
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(stability_map["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(stability_map["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(stability_map: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_grammar_stability_certificate",
        "source_mutation_version": stability_map["source_mutation_version"],
        "source_mutation_edge_count": stability_map["source_mutation_edge_count"],
        "stability_edge_count": stability_map["stability_edge_count"],
        "stable_edge_count": stability_map["stable_edge_count"],
        "unstable_edge_count": stability_map["unstable_edge_count"],
        "dangerous_stable_edge_count": stability_map["dangerous_stable_edge_count"],
        "dangerous_unstable_edge_count": stability_map["dangerous_unstable_edge_count"],
        "release_edge_count": stability_map["release_edge_count"],
        "obstruction_relevant_edge_count": stability_map["obstruction_relevant_edge_count"],
        "obstruction_detected": stability_map["obstruction_detected"],
        "stability_score": stability_map["stability_score"],
        "release_score": stability_map["release_score"],
        "dangerous_instability_score": stability_map["dangerous_instability_score"],
        "native_interpretation": stability_map["native_interpretation"],
        "mother_rule": stability_map["mother_rule"],
        "central_native_question": stability_map["central_native_question"],
        "proof_status": stability_map["proof_status"],
        "theorem_status": stability_map["theorem_status"],
        "negative_result_boundary": stability_map["negative_result_boundary"],
        "next_recommended_version": stability_map["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.7")
    print("=" * 80)
    print("Native Grammar Stability Map")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    mutation_atlas = read_json(MUTATION_ATLAS_PATH)
    mutation_certificate = read_json(MUTATION_CERTIFICATE_PATH)

    stability_map = build_stability_map(mutation_atlas, mutation_certificate)
    certificate = make_certificate(stability_map)
    report = make_report(stability_map)

    STABILITY_MAP_PATH.write_text(json.dumps(stability_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    STABILITY_REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    STABILITY_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_mutation_version: {stability_map['source_mutation_version']}")
    print(f"source_mutation_edge_count: {stability_map['source_mutation_edge_count']}")
    print(f"stability_edge_count: {stability_map['stability_edge_count']}")
    print(f"stable_edge_count: {stability_map['stable_edge_count']}")
    print(f"unstable_edge_count: {stability_map['unstable_edge_count']}")
    print(f"dangerous_stable_edge_count: {stability_map['dangerous_stable_edge_count']}")
    print(f"dangerous_unstable_edge_count: {stability_map['dangerous_unstable_edge_count']}")
    print(f"release_edge_count: {stability_map['release_edge_count']}")
    print(f"obstruction_relevant_edge_count: {stability_map['obstruction_relevant_edge_count']}")
    print(f"obstruction_detected: {stability_map['obstruction_detected']}")
    print(f"stability_score: {stability_map['stability_score']}")
    print(f"release_score: {stability_map['release_score']}")
    print(f"dangerous_instability_score: {stability_map['dangerous_instability_score']}")
    print(f"native_interpretation: {stability_map['native_interpretation']}")
    print(f"proof_status: {stability_map['proof_status']}")
    print(f"mother_rule: {stability_map['mother_rule']}")
    print(f"next: {stability_map['next_recommended_version']}")

    print(f"Wrote stability map JSON to: {STABILITY_MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote stability map Markdown to: {STABILITY_REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {STABILITY_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
