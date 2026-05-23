#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v2.9

Shadow Persistence Instrumentation.

This builder reads v2.8 expanded bounded obstruction search artifacts and adds
a native instrumentation layer for shadow persistence.

It does not prove the Collatz conjecture.
It does not claim global closure.
It does not claim that shadow always erases.

It asks a narrower native question:

When dangerous regeneration appears, does it look independent,
or does it carry a trace of prior debt structure?

Outputs:
- results/shadow_persistence_report.json
- results/shadow_persistence_report.md
- results/shadow_persistence_certificate.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "v2.9"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

SOURCE_ROWS = RESULTS_DIR / "expanded_bounded_obstruction_search_rows.jsonl"
SOURCE_SUMMARY = RESULTS_DIR / "expanded_bounded_obstruction_search_summary.json"
SOURCE_CERTIFICATE = RESULTS_DIR / "expanded_bounded_obstruction_search_certificate.json"

REPORT_JSON = RESULTS_DIR / "shadow_persistence_report.json"
REPORT_MD = RESULTS_DIR / "shadow_persistence_report.md"
CERTIFICATE_JSON = RESULTS_DIR / "shadow_persistence_certificate.json"


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

    rows: List[Dict[str, Any]] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

    return rows


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def classify_shadow_signal(row: Dict[str, Any]) -> Dict[str, Any]:
    n0 = row.get("n0")
    debt_windows = safe_int(row.get("debt_window_count"))
    regeneration_count = safe_int(row.get("regeneration_count"))
    dangerous_regeneration_count = safe_int(row.get("dangerous_regeneration_count"))
    obstruction_candidate_count = safe_int(row.get("obstruction_candidate_count"))
    min_surplus = safe_float(row.get("min_positive_surplus"))
    max_post_recovery_blocks = safe_int(row.get("max_post_recovery_blocks"))
    hardest_recovery_score = safe_float(row.get("hardest_recovery_score"), 0.0) or 0.0
    closure_result_type = str(row.get("closure_result_type", "UNDECIDED"))

    sample_dangerous = row.get("sample_dangerous_regenerations") or []
    sample_count = len(sample_dangerous)

    has_debt = debt_windows > 0
    has_regeneration = regeneration_count > 0
    has_dangerous_regeneration = dangerous_regeneration_count > 0
    has_obstruction_candidate = obstruction_candidate_count > 0

    tight_surplus = min_surplus is not None and min_surplus < 0.001
    long_recovery_shadow = max_post_recovery_blocks >= 32
    high_recovery_stress = hardest_recovery_score >= 100000.0
    sampled_dangerous_events = sample_count > 0

    evidence_score = 0

    if has_debt:
        evidence_score += 1

    if has_regeneration:
        evidence_score += 1

    if has_dangerous_regeneration:
        evidence_score += 2

    if tight_surplus:
        evidence_score += 2

    if long_recovery_shadow:
        evidence_score += 2

    if high_recovery_stress:
        evidence_score += 1

    if sampled_dangerous_events:
        evidence_score += 1

    if has_obstruction_candidate:
        classification = "OBSTRUCTION_CANDIDATE_SHADOW"
    elif has_dangerous_regeneration and (tight_surplus or long_recovery_shadow or high_recovery_stress):
        classification = "PERSISTENT_SHADOW_SIGNAL"
    elif has_dangerous_regeneration:
        classification = "DANGEROUS_REGENERATION_WITH_WEAK_SHADOW_SIGNAL"
    elif has_regeneration:
        classification = "REGENERATION_WITHOUT_DANGEROUS_SHADOW_SIGNAL"
    elif has_debt:
        classification = "DEBT_WITHOUT_REGENERATION_SHADOW"
    else:
        classification = "NO_SHADOW_SIGNAL"

    return {
        "version": VERSION,
        "n0": n0,
        "source_closure_result_type": closure_result_type,
        "debt_window_count": debt_windows,
        "regeneration_count": regeneration_count,
        "dangerous_regeneration_count": dangerous_regeneration_count,
        "obstruction_candidate_count": obstruction_candidate_count,
        "min_positive_surplus": min_surplus,
        "max_post_recovery_blocks": max_post_recovery_blocks,
        "hardest_recovery_score": hardest_recovery_score,
        "sample_dangerous_regeneration_count": sample_count,
        "signals": {
            "has_debt": has_debt,
            "has_regeneration": has_regeneration,
            "has_dangerous_regeneration": has_dangerous_regeneration,
            "tight_surplus": tight_surplus,
            "long_recovery_shadow": long_recovery_shadow,
            "high_recovery_stress": high_recovery_stress,
            "sampled_dangerous_events": sampled_dangerous_events,
            "has_obstruction_candidate": has_obstruction_candidate,
        },
        "shadow_persistence_score": evidence_score,
        "shadow_classification": classification,
    }


def summarize_shadow_rows(source_summary: Dict[str, Any], source_certificate: Dict[str, Any], shadow_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    classification_counts: Dict[str, int] = {}

    for row in shadow_rows:
        cls = str(row["shadow_classification"])
        classification_counts[cls] = classification_counts.get(cls, 0) + 1

    persistent_rows = [
        row for row in shadow_rows
        if row["shadow_classification"] == "PERSISTENT_SHADOW_SIGNAL"
    ]

    obstruction_shadow_rows = [
        row for row in shadow_rows
        if row["shadow_classification"] == "OBSTRUCTION_CANDIDATE_SHADOW"
    ]

    dangerous_weak_rows = [
        row for row in shadow_rows
        if row["shadow_classification"] == "DANGEROUS_REGENERATION_WITH_WEAK_SHADOW_SIGNAL"
    ]

    strongest_shadow_row = max(
        shadow_rows,
        key=lambda row: (
            safe_int(row.get("shadow_persistence_score")),
            safe_int(row.get("dangerous_regeneration_count")),
            float(row.get("hardest_recovery_score") or 0.0),
        ),
    ) if shadow_rows else None

    strongest_native_interpretation = "NO_SHADOW_ROWS"

    if obstruction_shadow_rows:
        strongest_native_interpretation = "OBSTRUCTION_CANDIDATE_SHADOW_DETECTED"
    elif persistent_rows:
        strongest_native_interpretation = "PERSISTENT_SHADOW_SIGNALS_FOUND_WITHOUT_OBSTRUCTION_CANDIDATE"
    elif dangerous_weak_rows:
        strongest_native_interpretation = "DANGEROUS_REGENERATION_FOUND_WITH_WEAK_SHADOW_SIGNAL"
    else:
        strongest_native_interpretation = "NO_PERSISTENT_SHADOW_SIGNAL_DETECTED"

    return {
        "version": VERSION,
        "layer": "shadow_persistence_instrumentation",
        "source_version": source_certificate.get("version", source_summary.get("version")),
        "source": {
            "rows": str(SOURCE_ROWS.relative_to(ROOT)),
            "summary": str(SOURCE_SUMMARY.relative_to(ROOT)),
            "certificate": str(SOURCE_CERTIFICATE.relative_to(ROOT)),
        },
        "tested_candidate_count": len(shadow_rows),
        "source_debt_window_count": source_certificate.get("debt_window_count"),
        "source_regeneration_count": source_certificate.get("regeneration_count"),
        "source_dangerous_regeneration_count": source_certificate.get("dangerous_regeneration_count"),
        "source_obstruction_candidate_count": source_certificate.get("obstruction_candidate_count"),
        "shadow_classification_counts": classification_counts,
        "persistent_shadow_signal_count": len(persistent_rows),
        "obstruction_candidate_shadow_count": len(obstruction_shadow_rows),
        "strongest_shadow_case": None if strongest_shadow_row is None else {
            "n0": strongest_shadow_row["n0"],
            "shadow_persistence_score": strongest_shadow_row["shadow_persistence_score"],
            "shadow_classification": strongest_shadow_row["shadow_classification"],
            "dangerous_regeneration_count": strongest_shadow_row["dangerous_regeneration_count"],
            "min_positive_surplus": strongest_shadow_row["min_positive_surplus"],
            "max_post_recovery_blocks": strongest_shadow_row["max_post_recovery_blocks"],
            "hardest_recovery_score": strongest_shadow_row["hardest_recovery_score"],
        },
        "native_interpretation": strongest_native_interpretation,
        "obstruction_detected": len(obstruction_shadow_rows) > 0,
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction-preserving shadow detected in a finite instrumentation layer is not proof that such shadow cannot exist.",
        "next_recommended_version": "v3.0 Formal Native-to-Standard Lemma Draft",
    }


def write_markdown_report(summary: Dict[str, Any], shadow_rows: List[Dict[str, Any]]) -> None:
    strongest = summary["strongest_shadow_case"]

    top_rows = sorted(
        shadow_rows,
        key=lambda row: (
            safe_int(row.get("shadow_persistence_score")),
            safe_int(row.get("dangerous_regeneration_count")),
            float(row.get("hardest_recovery_score") or 0.0),
        ),
        reverse=True,
    )[:20]

    lines = [
        "# Shadow Persistence Instrumentation Report",
        "",
        "Version: v2.9",
        "",
        "This report instruments the v2.8 expanded bounded obstruction search output.",
        "",
        "It does not prove the Collatz conjecture.",
        "",
        "It does not prove global closure.",
        "",
        "It does not prove that obstruction-preserving shadow cannot exist.",
        "",
        "## Summary",
        "",
        f"- tested_candidate_count: {summary['tested_candidate_count']}",
        f"- source_debt_window_count: {summary['source_debt_window_count']}",
        f"- source_regeneration_count: {summary['source_regeneration_count']}",
        f"- source_dangerous_regeneration_count: {summary['source_dangerous_regeneration_count']}",
        f"- source_obstruction_candidate_count: {summary['source_obstruction_candidate_count']}",
        f"- persistent_shadow_signal_count: {summary['persistent_shadow_signal_count']}",
        f"- obstruction_candidate_shadow_count: {summary['obstruction_candidate_shadow_count']}",
        f"- obstruction_detected: {summary['obstruction_detected']}",
        f"- native_interpretation: {summary['native_interpretation']}",
        f"- proof_status: {summary['proof_status']}",
        "",
        "## Classification counts",
        "",
    ]

    for key in sorted(summary["shadow_classification_counts"]):
        lines.append(f"- {key}: {summary['shadow_classification_counts'][key]}")

    lines.extend([
        "",
        "## Strongest shadow case",
        "",
    ])

    if strongest is None:
        lines.append("No strongest shadow case was available.")
    else:
        for key, value in strongest.items():
            lines.append(f"- {key}: {value}")

    lines.extend([
        "",
        "## Top shadow persistence cases",
        "",
        "| n0 | classification | score | dangerous regeneration | min surplus | max post recovery blocks | hardest recovery score |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])

    for row in top_rows:
        lines.append(
            f"| {row['n0']} | {row['shadow_classification']} | "
            f"{row['shadow_persistence_score']} | "
            f"{row['dangerous_regeneration_count']} | "
            f"{row['min_positive_surplus']} | "
            f"{row['max_post_recovery_blocks']} | "
            f"{row['hardest_recovery_score']} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        summary["negative_result_boundary"],
        "",
        "Correct interpretation:",
        "",
        "The current finite instrumentation found shadow persistence signals, but the certificate must keep proof status separate from evidence status.",
        "",
        "Incorrect interpretation:",
        "",
        "Do not claim final proof, global closure, or impossibility of obstruction-preserving shadow from this bounded instrumentation layer.",
        "",
    ])

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_certificate(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "shadow_persistence_instrumentation_certificate",
        "source_version": summary["source_version"],
        "tested_candidate_count": summary["tested_candidate_count"],
        "source_debt_window_count": summary["source_debt_window_count"],
        "source_regeneration_count": summary["source_regeneration_count"],
        "source_dangerous_regeneration_count": summary["source_dangerous_regeneration_count"],
        "source_obstruction_candidate_count": summary["source_obstruction_candidate_count"],
        "shadow_classification_counts": summary["shadow_classification_counts"],
        "persistent_shadow_signal_count": summary["persistent_shadow_signal_count"],
        "obstruction_candidate_shadow_count": summary["obstruction_candidate_shadow_count"],
        "strongest_shadow_case": summary["strongest_shadow_case"],
        "native_interpretation": summary["native_interpretation"],
        "obstruction_detected": summary["obstruction_detected"],
        "proof_status": summary["proof_status"],
        "theorem_status": summary["theorem_status"],
        "negative_result_boundary": summary["negative_result_boundary"],
        "minimum_report_fields_present": True,
        "next_recommended_version": summary["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v2.9")
    print("=" * 80)
    print("Shadow Persistence Instrumentation")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = read_jsonl(SOURCE_ROWS)
    source_summary = read_json(SOURCE_SUMMARY)
    source_certificate = read_json(SOURCE_CERTIFICATE)

    shadow_rows = [classify_shadow_signal(row) for row in source_rows]
    summary = summarize_shadow_rows(source_summary, source_certificate, shadow_rows)
    certificate = make_certificate(summary)

    REPORT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown_report(summary, shadow_rows)
    CERTIFICATE_JSON.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_version: {summary['source_version']}")
    print(f"tested_candidate_count: {summary['tested_candidate_count']}")
    print(f"source_debt_window_count: {summary['source_debt_window_count']}")
    print(f"source_regeneration_count: {summary['source_regeneration_count']}")
    print(f"source_dangerous_regeneration_count: {summary['source_dangerous_regeneration_count']}")
    print(f"source_obstruction_candidate_count: {summary['source_obstruction_candidate_count']}")
    print(f"persistent_shadow_signal_count: {summary['persistent_shadow_signal_count']}")
    print(f"obstruction_candidate_shadow_count: {summary['obstruction_candidate_shadow_count']}")
    print(f"obstruction_detected: {summary['obstruction_detected']}")
    print(f"native_interpretation: {summary['native_interpretation']}")
    print(f"proof_status: {summary['proof_status']}")
    print(f"negative_result_boundary: {summary['negative_result_boundary']}")

    strongest = summary["strongest_shadow_case"]
    if strongest:
        print(
            "strongest shadow case: "
            f"n0={strongest['n0']} "
            f"score={strongest['shadow_persistence_score']} "
            f"classification={strongest['shadow_classification']}"
        )

    print(f"Wrote JSON report to: {REPORT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown report to: {REPORT_MD.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_JSON.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
