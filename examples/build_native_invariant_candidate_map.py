#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.9

Native Invariant Candidate Map.

This builder reads the v3.8 conservation map and asks:

Which conserved behaviors are strong enough to become native invariant candidates?

It does not solve Collatz.
It does not prove Collatz.
It does not claim global invariance.
It does not turn bounded conservation into theorem.

Outputs:
- results/native_invariant_candidate_map.json
- results/native_invariant_candidate_map.md
- results/native_invariant_candidate_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v3.9"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

CONSERVATION_MAP_PATH = RESULTS_DIR / "native_conservation_map.json"
CONSERVATION_CERTIFICATE_PATH = RESULTS_DIR / "native_conservation_certificate.json"

INVARIANT_MAP_PATH = RESULTS_DIR / "native_invariant_candidate_map.json"
INVARIANT_REPORT_PATH = RESULTS_DIR / "native_invariant_candidate_map.md"
INVARIANT_CERTIFICATE_PATH = RESULTS_DIR / "native_invariant_candidate_certificate.json"


def ensure_source_artifacts() -> None:
    if CONSERVATION_MAP_PATH.exists() and CONSERVATION_CERTIFICATE_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_conservation_map.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.8 native conservation map builder.")

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


def collect_conservation_candidates(conservation_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []

    for key in [
        "strongest_conservation_candidates",
        "danger_release_conservation_candidates",
        "instability_conservation_candidates",
        "dangerous_stability_conservation_candidates",
        "obstruction_relevant_conservation_candidates",
        "near_9780657630_conservation",
    ]:
        for item in conservation_map.get(key, []):
            copy = dict(item)
            copy["source_list"] = key
            candidates.append(copy)

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
            item.get("conservation_status"),
            item.get("conservation_class"),
        )
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(item)

    return unique


def invariant_strength(item: Dict[str, Any]) -> float:
    base = safe_float(item.get("mutation_strength"), 0.0)
    status = str(item.get("conservation_status", "unknown"))

    multiplier = 1.0

    if status == "obstruction_relevant_conservation":
        multiplier = 100.0
    elif status == "dangerous_stability_conservation":
        multiplier = 20.0
    elif status == "danger_release_conservation":
        multiplier = 10.0
    elif status == "instability_conservation":
        multiplier = 5.0
    elif status == "stability_conservation":
        multiplier = 3.0

    return base * multiplier


def classify_invariant_candidate(item: Dict[str, Any]) -> Dict[str, Any]:
    status = str(item.get("conservation_status", "unknown"))
    conserved_features = list(item.get("conserved_features", []))
    lost_features = list(item.get("lost_features", []))
    strength = invariant_strength(item)

    if status == "obstruction_relevant_conservation":
        candidate_type = "obstruction_relevant_invariant_candidate"
        candidate_strength = "open_critical_candidate"
    elif status == "dangerous_stability_conservation":
        candidate_type = "dangerous_stability_invariant_candidate"
        candidate_strength = "strong_bounded_candidate"
    elif status == "danger_release_conservation":
        candidate_type = "danger_release_invariant_candidate"
        candidate_strength = "strong_bounded_candidate"
    elif status == "instability_conservation":
        candidate_type = "instability_invariant_candidate"
        candidate_strength = "medium_bounded_candidate"
    elif status == "stability_conservation":
        candidate_type = "stability_invariant_candidate"
        candidate_strength = "medium_bounded_candidate"
    else:
        candidate_type = "weak_invariant_candidate"
        candidate_strength = "weak_bounded_candidate"

    if "obstruction_relevance" in conserved_features:
        logical_status = "requires_immediate_native_review"
    elif "danger" in conserved_features and "stability_behavior" in conserved_features:
        logical_status = "danger_stability_not_proof"
    elif "release_behavior" in conserved_features:
        logical_status = "release_behavior_candidate"
    elif "instability_behavior" in conserved_features:
        logical_status = "instability_behavior_candidate"
    else:
        logical_status = "bounded_candidate_only"

    return {
        "from_n0": item.get("from_n0"),
        "to_n0": item.get("to_n0"),
        "from_class": item.get("from_class"),
        "to_class": item.get("to_class"),
        "from_family": item.get("from_family"),
        "to_family": item.get("to_family"),
        "conservation_status": status,
        "conservation_class": item.get("conservation_class"),
        "conserved_features": conserved_features,
        "lost_features": lost_features,
        "candidate_type": candidate_type,
        "candidate_strength": candidate_strength,
        "logical_status": logical_status,
        "invariant_strength": strength,
        "native_interpretation": interpret_candidate(candidate_type),
    }


def interpret_candidate(candidate_type: str) -> str:
    if candidate_type == "obstruction_relevant_invariant_candidate":
        return "obstruction-relevant behavior may be conserved and requires native review"
    if candidate_type == "dangerous_stability_invariant_candidate":
        return "dangerous stability appears as bounded invariant candidate"
    if candidate_type == "danger_release_invariant_candidate":
        return "danger-release behavior appears as bounded invariant candidate"
    if candidate_type == "instability_invariant_candidate":
        return "instability itself appears as bounded invariant candidate"
    if candidate_type == "stability_invariant_candidate":
        return "stability behavior appears as bounded invariant candidate"
    return "weak bounded invariant candidate only"


def build_invariant_candidate_map(
    conservation_map: Dict[str, Any],
    conservation_certificate: Dict[str, Any],
) -> Dict[str, Any]:
    conservation_candidates = collect_conservation_candidates(conservation_map)
    invariant_candidates = [
        classify_invariant_candidate(item)
        for item in conservation_candidates
    ]

    candidate_type_counts = Counter(item["candidate_type"] for item in invariant_candidates)
    candidate_strength_counts = Counter(item["candidate_strength"] for item in invariant_candidates)
    logical_status_counts = Counter(item["logical_status"] for item in invariant_candidates)

    obstruction_relevant = [
        item for item in invariant_candidates
        if item["candidate_type"] == "obstruction_relevant_invariant_candidate"
    ]

    dangerous_stability = [
        item for item in invariant_candidates
        if item["candidate_type"] == "dangerous_stability_invariant_candidate"
    ]

    danger_release = [
        item for item in invariant_candidates
        if item["candidate_type"] == "danger_release_invariant_candidate"
    ]

    instability = [
        item for item in invariant_candidates
        if item["candidate_type"] == "instability_invariant_candidate"
    ]

    weak = [
        item for item in invariant_candidates
        if item["candidate_type"] == "weak_invariant_candidate"
    ]

    near_9780657630 = [
        item for item in invariant_candidates
        if abs(safe_int(item.get("from_n0")) - 9780657630) <= 8
        or abs(safe_int(item.get("to_n0")) - 9780657630) <= 8
    ]

    strongest = sorted(
        invariant_candidates,
        key=lambda item: item["invariant_strength"],
        reverse=True,
    )[:50]

    total = max(1, len(invariant_candidates))

    if obstruction_relevant:
        native_interpretation = "OBSTRUCTION_RELEVANT_INVARIANT_CANDIDATE_PRESENT"
    elif dangerous_stability and danger_release:
        native_interpretation = "DANGER_RELEASE_AND_DANGEROUS_STABILITY_INVARIANT_CANDIDATES_PRESENT"
    elif danger_release:
        native_interpretation = "DANGER_RELEASE_INVARIANT_CANDIDATE_DOMINANT"
    elif dangerous_stability:
        native_interpretation = "DANGEROUS_STABILITY_INVARIANT_CANDIDATE_PRESENT"
    elif instability:
        native_interpretation = "INSTABILITY_INVARIANT_CANDIDATE_PRESENT"
    else:
        native_interpretation = "ONLY_WEAK_INVARIANT_CANDIDATES_PRESENT"

    invariant_map = {
        "version": VERSION,
        "layer": "native_invariant_candidate_map",
        "source_conservation_version": conservation_certificate.get("version", conservation_map.get("version")),
        "source_conservation_candidate_count": conservation_certificate.get("conservation_candidate_count", conservation_map.get("conservation_candidate_count")),
        "source_danger_release_conservation_count": conservation_certificate.get("danger_release_conservation_count", conservation_map.get("danger_release_conservation_count")),
        "source_dangerous_stability_conservation_count": conservation_certificate.get("dangerous_stability_conservation_count", conservation_map.get("dangerous_stability_conservation_count")),
        "source_obstruction_relevant_conservation_count": conservation_certificate.get("obstruction_relevant_conservation_count", conservation_map.get("obstruction_relevant_conservation_count")),
        "invariant_candidate_count": len(invariant_candidates),
        "candidate_type_counts": dict(candidate_type_counts),
        "candidate_strength_counts": dict(candidate_strength_counts),
        "logical_status_counts": dict(logical_status_counts),
        "obstruction_relevant_invariant_candidate_count": len(obstruction_relevant),
        "dangerous_stability_invariant_candidate_count": len(dangerous_stability),
        "danger_release_invariant_candidate_count": len(danger_release),
        "instability_invariant_candidate_count": len(instability),
        "weak_invariant_candidate_count": len(weak),
        "obstruction_detected": len(obstruction_relevant) > 0,
        "danger_release_invariant_ratio": len(danger_release) / total,
        "dangerous_stability_invariant_ratio": len(dangerous_stability) / total,
        "obstruction_relevant_invariant_ratio": len(obstruction_relevant) / total,
        "strongest_invariant_candidates": strongest,
        "danger_release_invariant_candidates": danger_release[:50],
        "dangerous_stability_invariant_candidates": dangerous_stability[:50],
        "instability_invariant_candidates": instability[:50],
        "obstruction_relevant_invariant_candidates": obstruction_relevant[:50],
        "near_9780657630_invariant_candidates": near_9780657630[:50],
        "native_interpretation": native_interpretation,
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "Which conserved behaviors are strong enough to become native invariant candidates?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "global_invariant_status": "not_claimed",
        "negative_result_boundary": "Bounded invariant candidates are not global invariants and do not imply theorem or proof.",
        "next_recommended_version": "v4.0 Native Language Summary",
    }

    return invariant_map


def make_report(invariant_map: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Invariant Candidate Map")
    lines.append("")
    lines.append("Version: v3.9")
    lines.append("")
    lines.append("This report maps bounded native invariant candidates.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("It does not claim global invariance.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(invariant_map["mother_rule"])
    lines.append("")
    lines.append("## Central native question")
    lines.append("")
    lines.append(invariant_map["central_native_question"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    keys = [
        "source_conservation_version",
        "source_conservation_candidate_count",
        "invariant_candidate_count",
        "obstruction_relevant_invariant_candidate_count",
        "dangerous_stability_invariant_candidate_count",
        "danger_release_invariant_candidate_count",
        "instability_invariant_candidate_count",
        "weak_invariant_candidate_count",
        "obstruction_detected",
        "danger_release_invariant_ratio",
        "dangerous_stability_invariant_ratio",
        "obstruction_relevant_invariant_ratio",
        "native_interpretation",
        "proof_status",
        "global_invariant_status",
    ]

    for key in keys:
        lines.append(f"- {key}: {invariant_map[key]}")

    lines.append("")
    lines.append("## Candidate type counts")
    lines.append("")

    for key, value in sorted(invariant_map["candidate_type_counts"].items()):
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("## Strongest invariant candidates")
    lines.append("")

    for item in invariant_map["strongest_invariant_candidates"][:25]:
        lines.append(
            f"- {item.get('from_n0')} -> {item.get('to_n0')} "
            f"type={item.get('candidate_type')} "
            f"strength={item.get('candidate_strength')} "
            f"score={item.get('invariant_strength')}"
        )

    lines.append("")
    lines.append("## Danger-release invariant candidates")
    lines.append("")

    if not invariant_map["danger_release_invariant_candidates"]:
        lines.append("- none observed")
    else:
        for item in invariant_map["danger_release_invariant_candidates"][:25]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"{item.get('from_class')} -> {item.get('to_class')}"
            )

    lines.append("")
    lines.append("## Dangerous-stability invariant candidates")
    lines.append("")

    if not invariant_map["dangerous_stability_invariant_candidates"]:
        lines.append("- none observed")
    else:
        for item in invariant_map["dangerous_stability_invariant_candidates"][:25]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"{item.get('from_class')} -> {item.get('to_class')}"
            )

    lines.append("")
    lines.append("## Obstruction-relevant invariant candidates")
    lines.append("")

    if not invariant_map["obstruction_relevant_invariant_candidates"]:
        lines.append("- none observed in this bounded map")
    else:
        for item in invariant_map["obstruction_relevant_invariant_candidates"][:25]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"{item.get('from_class')} -> {item.get('to_class')}"
            )

    lines.append("")
    lines.append("## Near 9780657630")
    lines.append("")

    if not invariant_map["near_9780657630_invariant_candidates"]:
        lines.append("- no invariant candidates near 9780657630 in this bounded map")
    else:
        for item in invariant_map["near_9780657630_invariant_candidates"][:25]:
            lines.append(
                f"- {item.get('from_n0')} -> {item.get('to_n0')} "
                f"type={item.get('candidate_type')} "
                f"status={item.get('logical_status')}"
            )

    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(invariant_map["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(invariant_map["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(invariant_map: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_invariant_candidate_certificate",
        "source_conservation_version": invariant_map["source_conservation_version"],
        "source_conservation_candidate_count": invariant_map["source_conservation_candidate_count"],
        "invariant_candidate_count": invariant_map["invariant_candidate_count"],
        "obstruction_relevant_invariant_candidate_count": invariant_map["obstruction_relevant_invariant_candidate_count"],
        "dangerous_stability_invariant_candidate_count": invariant_map["dangerous_stability_invariant_candidate_count"],
        "danger_release_invariant_candidate_count": invariant_map["danger_release_invariant_candidate_count"],
        "instability_invariant_candidate_count": invariant_map["instability_invariant_candidate_count"],
        "weak_invariant_candidate_count": invariant_map["weak_invariant_candidate_count"],
        "obstruction_detected": invariant_map["obstruction_detected"],
        "danger_release_invariant_ratio": invariant_map["danger_release_invariant_ratio"],
        "dangerous_stability_invariant_ratio": invariant_map["dangerous_stability_invariant_ratio"],
        "obstruction_relevant_invariant_ratio": invariant_map["obstruction_relevant_invariant_ratio"],
        "native_interpretation": invariant_map["native_interpretation"],
        "mother_rule": invariant_map["mother_rule"],
        "central_native_question": invariant_map["central_native_question"],
        "proof_status": invariant_map["proof_status"],
        "theorem_status": invariant_map["theorem_status"],
        "global_invariant_status": invariant_map["global_invariant_status"],
        "negative_result_boundary": invariant_map["negative_result_boundary"],
        "next_recommended_version": invariant_map["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.9")
    print("=" * 80)
    print("Native Invariant Candidate Map")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    conservation_map = read_json(CONSERVATION_MAP_PATH)
    conservation_certificate = read_json(CONSERVATION_CERTIFICATE_PATH)

    invariant_map = build_invariant_candidate_map(conservation_map, conservation_certificate)
    certificate = make_certificate(invariant_map)
    report = make_report(invariant_map)

    INVARIANT_MAP_PATH.write_text(json.dumps(invariant_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    INVARIANT_REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    INVARIANT_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_conservation_version: {invariant_map['source_conservation_version']}")
    print(f"source_conservation_candidate_count: {invariant_map['source_conservation_candidate_count']}")
    print(f"invariant_candidate_count: {invariant_map['invariant_candidate_count']}")
    print(f"obstruction_relevant_invariant_candidate_count: {invariant_map['obstruction_relevant_invariant_candidate_count']}")
    print(f"dangerous_stability_invariant_candidate_count: {invariant_map['dangerous_stability_invariant_candidate_count']}")
    print(f"danger_release_invariant_candidate_count: {invariant_map['danger_release_invariant_candidate_count']}")
    print(f"instability_invariant_candidate_count: {invariant_map['instability_invariant_candidate_count']}")
    print(f"weak_invariant_candidate_count: {invariant_map['weak_invariant_candidate_count']}")
    print(f"obstruction_detected: {invariant_map['obstruction_detected']}")
    print(f"native_interpretation: {invariant_map['native_interpretation']}")
    print(f"proof_status: {invariant_map['proof_status']}")
    print(f"global_invariant_status: {invariant_map['global_invariant_status']}")
    print(f"mother_rule: {invariant_map['mother_rule']}")
    print(f"next: {invariant_map['next_recommended_version']}")

    print(f"Wrote invariant candidate map JSON to: {INVARIANT_MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote invariant candidate map Markdown to: {INVARIANT_REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {INVARIANT_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
