#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.5

Native Grammar Recurrence Map.

This builder reads v3.4 Native Sentence Atlas artifacts and maps recurrence
between native sentence forms.

It does not solve Collatz.
It does not prove Collatz.
It does not treat termination as the native meaning.

It asks:
Which native sentence forms repeat, mutate, stabilize, or disappear?

Outputs:
- results/native_grammar_recurrence_map.json
- results/native_grammar_recurrence_map.md
- results/native_grammar_recurrence_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


VERSION = "v3.5"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

ATLAS_PATH = RESULTS_DIR / "native_sentence_atlas.json"
ATLAS_CERTIFICATE_PATH = RESULTS_DIR / "native_sentence_atlas_certificate.json"
SENTENCES_PATH = RESULTS_DIR / "native_sentences.jsonl"

MAP_PATH = RESULTS_DIR / "native_grammar_recurrence_map.json"
REPORT_PATH = RESULTS_DIR / "native_grammar_recurrence_map.md"
CERTIFICATE_PATH = RESULTS_DIR / "native_grammar_recurrence_certificate.json"


def ensure_source_artifacts() -> None:
    if ATLAS_PATH.exists() and ATLAS_CERTIFICATE_PATH.exists() and SENTENCES_PATH.exists():
        return

    builder = ROOT / "examples" / "build_native_sentence_atlas.py"
    if not builder.exists():
        raise FileNotFoundError("Missing v3.4 native sentence atlas builder.")

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


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def get_first(row: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in row:
            return row[key]
    return default


def normalize_sentence(row: Dict[str, Any]) -> Dict[str, Any]:
    n0 = as_int(get_first(row, ["n0", "number", "start", "odd_start"], 0))

    sentence_class = str(
        get_first(
            row,
            [
                "sentence_class",
                "native_sentence_class",
                "native_sentence_type",
                "closure_result_type",
                "class",
                "classification",
            ],
            "UNDECIDED_SENTENCE",
        )
    )

    debt_windows = as_int(get_first(row, ["debt_window_count", "bad_windows", "bad_window_count"], 0))
    regeneration_count = as_int(get_first(row, ["regeneration_count", "regenerations"], 0))
    dangerous_regeneration_count = as_int(
        get_first(row, ["dangerous_regeneration_count", "dangerous_regenerations"], 0)
    )
    obstruction_candidate_count = as_int(
        get_first(row, ["obstruction_candidate_count", "obstruction_candidates"], 0)
    )

    recovery_score = as_float(
        get_first(row, ["hardest_recovery_score", "recovery_score", "score", "hardness"], 0.0)
    )

    surplus_value = get_first(
        row,
        ["min_positive_surplus", "tightest_positive_surplus", "surplus", "min_surplus"],
        None,
    )

    min_positive_surplus = None if surplus_value is None else as_float(surplus_value)

    if obstruction_candidate_count > 0 and "OBSTRUCTION" not in sentence_class.upper():
        sentence_class = "OBSTRUCTION_CANDIDATE_SENTENCE"

    return {
        "n0": n0,
        "sentence_class": sentence_class,
        "family": classify_family(sentence_class),
        "debt_window_count": debt_windows,
        "regeneration_count": regeneration_count,
        "dangerous_regeneration_count": dangerous_regeneration_count,
        "obstruction_candidate_count": obstruction_candidate_count,
        "recovery_score": recovery_score,
        "min_positive_surplus": min_positive_surplus,
    }


def classify_family(sentence_class: str) -> str:
    upper = sentence_class.upper()

    if "OBSTRUCTION" in upper:
        return "obstruction_candidate_family"
    if "DANGEROUS" in upper:
        return "dangerous_regeneration_family"
    if "REGENERATED" in upper or "REGENERATION" in upper:
        return "regeneration_family"
    if "RECOVERY" in upper or "RECOVERED" in upper or "COMPENSATED" in upper:
        return "recovery_family"
    if "NO_DEBT" in upper:
        return "no_debt_family"
    if "UNDECIDED" in upper:
        return "undecided_family"

    return "unclassified_family"


def transition_label(a: Dict[str, Any], b: Dict[str, Any]) -> str:
    if a["sentence_class"] == b["sentence_class"]:
        return "repeat"

    if a["family"] == b["family"]:
        return "family_mutation"

    if a["family"] == "dangerous_regeneration_family" and b["family"] == "dangerous_regeneration_family":
        return "dangerous_repeat"

    if a["family"] == "dangerous_regeneration_family" and b["family"] != "obstruction_candidate_family":
        return "dangerous_to_non_obstruction"

    if b["family"] == "obstruction_candidate_family":
        return "toward_obstruction_candidate"

    if a["family"] == "recovery_family" and b["family"] in {"regeneration_family", "dangerous_regeneration_family"}:
        return "recovery_to_regeneration"

    if a["family"] in {"regeneration_family", "dangerous_regeneration_family"} and b["family"] == "recovery_family":
        return "regeneration_to_recovery"

    return "cross_family_mutation"


def recurrence_relation(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "from_n0": a["n0"],
        "to_n0": b["n0"],
        "delta": b["n0"] - a["n0"],
        "from_class": a["sentence_class"],
        "to_class": b["sentence_class"],
        "from_family": a["family"],
        "to_family": b["family"],
        "transition_label": transition_label(a, b),
        "recovery_score_delta": b["recovery_score"] - a["recovery_score"],
        "debt_window_delta": b["debt_window_count"] - a["debt_window_count"],
        "dangerous_regeneration_delta": b["dangerous_regeneration_count"] - a["dangerous_regeneration_count"],
        "obstruction_candidate_delta": b["obstruction_candidate_count"] - a["obstruction_candidate_count"],
    }


def build_recurrence_map(sentences: List[Dict[str, Any]], atlas: Dict[str, Any], atlas_certificate: Dict[str, Any]) -> Dict[str, Any]:
    normalized = [normalize_sentence(row) for row in sentences if as_int(get_first(row, ["n0", "number", "start", "odd_start"], 0)) > 0]
    normalized = sorted(normalized, key=lambda row: row["n0"])

    by_n0 = {row["n0"]: row for row in normalized}

    neighbor_edges: List[Dict[str, Any]] = []
    for row in normalized:
        next_row = by_n0.get(row["n0"] + 1)
        if next_row:
            neighbor_edges.append(recurrence_relation(row, next_row))

    local_window_edges: List[Dict[str, Any]] = []
    for row in normalized:
        for delta in [2, 3, 4, 5, 8]:
            next_row = by_n0.get(row["n0"] + delta)
            if next_row:
                local_window_edges.append(recurrence_relation(row, next_row))

    all_edges = neighbor_edges + local_window_edges

    transition_counts = Counter(edge["transition_label"] for edge in all_edges)
    class_pair_counts = Counter((edge["from_class"], edge["to_class"]) for edge in all_edges)
    family_pair_counts = Counter((edge["from_family"], edge["to_family"]) for edge in all_edges)

    repeat_edges = [edge for edge in all_edges if edge["transition_label"] == "repeat"]
    mutation_edges = [edge for edge in all_edges if edge["transition_label"] != "repeat"]
    dangerous_edges = [
        edge for edge in all_edges
        if edge["from_family"] == "dangerous_regeneration_family"
        or edge["to_family"] == "dangerous_regeneration_family"
    ]
    obstruction_edges = [
        edge for edge in all_edges
        if edge["from_family"] == "obstruction_candidate_family"
        or edge["to_family"] == "obstruction_candidate_family"
    ]

    high_delta_edges = sorted(
        all_edges,
        key=lambda edge: abs(float(edge["recovery_score_delta"])),
        reverse=True,
    )[:20]

    dangerous_to_non_obstruction = [
        edge for edge in dangerous_edges
        if edge["from_family"] == "dangerous_regeneration_family"
        and edge["to_family"] != "obstruction_candidate_family"
    ]

    recurrence_profiles = []
    for key, count in family_pair_counts.most_common():
        recurrence_profiles.append(
            {
                "from_family": key[0],
                "to_family": key[1],
                "count": count,
            }
        )

    class_profiles = []
    for key, count in class_pair_counts.most_common():
        class_profiles.append(
            {
                "from_class": key[0],
                "to_class": key[1],
                "count": count,
            }
        )

    repeated_classes = Counter(row["sentence_class"] for row in normalized)
    stable_classes = [
        {
            "sentence_class": key,
            "count": value,
        }
        for key, value in repeated_classes.most_common()
        if value > 1
    ]

    rare_classes = [
        {
            "sentence_class": key,
            "count": value,
        }
        for key, value in sorted(repeated_classes.items(), key=lambda item: (item[1], item[0]))
        if value == 1
    ]

    native_interpretation = (
        "OBSTRUCTION_RECURRENCE_PRESENT"
        if obstruction_edges
        else "DANGEROUS_RECURRENCE_PRESENT_WITHOUT_OBSTRUCTION_RECURRENCE"
        if dangerous_edges
        else "NO_DANGEROUS_RECURRENCE_PRESENT"
    )

    recurrence_map = {
        "version": VERSION,
        "layer": "native_grammar_recurrence_map",
        "source_atlas_version": atlas_certificate.get("version", atlas.get("version")),
        "sentence_count": len(normalized),
        "neighbor_edge_count": len(neighbor_edges),
        "local_window_edge_count": len(local_window_edges),
        "total_edge_count": len(all_edges),
        "repeat_edge_count": len(repeat_edges),
        "mutation_edge_count": len(mutation_edges),
        "dangerous_edge_count": len(dangerous_edges),
        "obstruction_edge_count": len(obstruction_edges),
        "obstruction_detected": len(obstruction_edges) > 0,
        "native_interpretation": native_interpretation,
        "transition_counts": dict(transition_counts),
        "family_pair_recurrence_profiles": recurrence_profiles,
        "class_pair_recurrence_profiles": class_profiles[:30],
        "stable_classes": stable_classes,
        "rare_classes": rare_classes,
        "strongest_mutation_edges": high_delta_edges,
        "dangerous_to_non_obstruction_edges": dangerous_to_non_obstruction[:30],
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "Which native sentence forms repeat, mutate, stabilize, or disappear?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction recurrence detected in this bounded recurrence map is not proof that obstruction recurrence cannot exist.",
        "next_recommended_version": "v3.6 Native Grammar Mutation Atlas",
    }

    return recurrence_map


def make_report(data: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Grammar Recurrence Map")
    lines.append("")
    lines.append("Version: v3.5")
    lines.append("")
    lines.append("This report maps recurrence between native sentence forms.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("It asks which sentence forms repeat, mutate, stabilize, or disappear.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(data["mother_rule"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- sentence_count: {data['sentence_count']}")
    lines.append(f"- total_edge_count: {data['total_edge_count']}")
    lines.append(f"- repeat_edge_count: {data['repeat_edge_count']}")
    lines.append(f"- mutation_edge_count: {data['mutation_edge_count']}")
    lines.append(f"- dangerous_edge_count: {data['dangerous_edge_count']}")
    lines.append(f"- obstruction_edge_count: {data['obstruction_edge_count']}")
    lines.append(f"- obstruction_detected: {data['obstruction_detected']}")
    lines.append(f"- native_interpretation: {data['native_interpretation']}")
    lines.append(f"- proof_status: {data['proof_status']}")
    lines.append("")
    lines.append("## Transition counts")
    lines.append("")
    for key, value in sorted(data["transition_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Family recurrence profiles")
    lines.append("")
    for item in data["family_pair_recurrence_profiles"][:20]:
        lines.append(f"- {item['from_family']} -> {item['to_family']}: {item['count']}")
    lines.append("")
    lines.append("## Class recurrence profiles")
    lines.append("")
    for item in data["class_pair_recurrence_profiles"][:20]:
        lines.append(f"- {item['from_class']} -> {item['to_class']}: {item['count']}")
    lines.append("")
    lines.append("## Stable classes")
    lines.append("")
    for item in data["stable_classes"][:20]:
        lines.append(f"- {item['sentence_class']}: {item['count']}")
    lines.append("")
    lines.append("## Rare classes")
    lines.append("")
    for item in data["rare_classes"][:20]:
        lines.append(f"- {item['sentence_class']}: {item['count']}")
    lines.append("")
    lines.append("## Strongest mutation edges")
    lines.append("")
    for edge in data["strongest_mutation_edges"][:20]:
        lines.append(
            f"- {edge['from_n0']} -> {edge['to_n0']} "
            f"{edge['from_class']} -> {edge['to_class']} "
            f"label={edge['transition_label']} score_delta={edge['recovery_score_delta']}"
        )
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(data["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(data["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_grammar_recurrence_certificate",
        "source_atlas_version": data["source_atlas_version"],
        "sentence_count": data["sentence_count"],
        "total_edge_count": data["total_edge_count"],
        "repeat_edge_count": data["repeat_edge_count"],
        "mutation_edge_count": data["mutation_edge_count"],
        "dangerous_edge_count": data["dangerous_edge_count"],
        "obstruction_edge_count": data["obstruction_edge_count"],
        "obstruction_detected": data["obstruction_detected"],
        "native_interpretation": data["native_interpretation"],
        "mother_rule": data["mother_rule"],
        "central_native_question": data["central_native_question"],
        "proof_status": data["proof_status"],
        "theorem_status": data["theorem_status"],
        "negative_result_boundary": data["negative_result_boundary"],
        "next_recommended_version": data["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.5")
    print("=" * 80)
    print("Native Grammar Recurrence Map")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    atlas = read_json(ATLAS_PATH)
    atlas_certificate = read_json(ATLAS_CERTIFICATE_PATH)
    sentences = read_jsonl(SENTENCES_PATH)

    recurrence_map = build_recurrence_map(sentences, atlas, atlas_certificate)
    certificate = make_certificate(recurrence_map)
    report = make_report(recurrence_map)

    MAP_PATH.write_text(json.dumps(recurrence_map, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_atlas_version: {recurrence_map['source_atlas_version']}")
    print(f"sentence_count: {recurrence_map['sentence_count']}")
    print(f"total_edge_count: {recurrence_map['total_edge_count']}")
    print(f"repeat_edge_count: {recurrence_map['repeat_edge_count']}")
    print(f"mutation_edge_count: {recurrence_map['mutation_edge_count']}")
    print(f"dangerous_edge_count: {recurrence_map['dangerous_edge_count']}")
    print(f"obstruction_edge_count: {recurrence_map['obstruction_edge_count']}")
    print(f"obstruction_detected: {recurrence_map['obstruction_detected']}")
    print(f"native_interpretation: {recurrence_map['native_interpretation']}")
    print(f"proof_status: {recurrence_map['proof_status']}")
    print(f"mother_rule: {recurrence_map['mother_rule']}")
    print(f"next: {recurrence_map['next_recommended_version']}")

    print(f"Wrote recurrence map JSON to: {MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote recurrence map Markdown to: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
