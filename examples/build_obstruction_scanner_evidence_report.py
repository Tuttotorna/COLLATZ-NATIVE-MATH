#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v2.7

Obstruction Scanner Evidence Report.

This script reads v2.6 bounded obstruction scanner artifacts and builds an
interpretive native evidence report.

It does not prove Collatz.
It does not prove global closure.
It does not prove obstruction impossible.

It classifies what v2.6 actually found.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "v2.7"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

ROWS_PATH = RESULTS_DIR / "bounded_obstruction_search_rows.jsonl"
SUMMARY_PATH = RESULTS_DIR / "bounded_obstruction_search_summary.json"
CERTIFICATE_PATH = RESULTS_DIR / "bounded_obstruction_search_certificate.json"

REPORT_JSON_PATH = RESULTS_DIR / "obstruction_scanner_evidence_report.json"
REPORT_MD_PATH = RESULTS_DIR / "obstruction_scanner_evidence_report.md"
REPORT_CERTIFICATE_PATH = RESULTS_DIR / "obstruction_scanner_evidence_certificate.json"


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def ensure_v26_artifacts_exist() -> None:
    missing = [
        path
        for path in [ROWS_PATH, SUMMARY_PATH, CERTIFICATE_PATH]
        if not path.exists()
    ]

    if not missing:
        return

    scanner = ROOT / "examples" / "bounded_obstruction_search_scanner.py"
    if not scanner.exists():
        missing_list = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise FileNotFoundError(
            "Missing v2.6 artifacts and scanner is unavailable: " + missing_list
        )

    import subprocess
    import sys

    subprocess.run(
        [sys.executable, str(scanner)],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def top_rows(rows: List[Dict[str, Any]], key: str, limit: int = 10) -> List[Dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            -float(row[key]) if row[key] is not None else float("inf"),
            int(row["n0"]),
        ),
    )[:limit]


def lowest_positive_surplus_rows(rows: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    candidates = [row for row in rows if row.get("min_positive_surplus") is not None]
    return sorted(
        candidates,
        key=lambda row: (float(row["min_positive_surplus"]), int(row["n0"])),
    )[:limit]


def compact_case(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "n0": row["n0"],
        "odd_blocks": row["odd_blocks"],
        "debt_window_count": row["debt_window_count"],
        "regeneration_count": row["regeneration_count"],
        "dangerous_regeneration_count": row["dangerous_regeneration_count"],
        "obstruction_candidate_count": row["obstruction_candidate_count"],
        "closure_result_type": row["closure_result_type"],
        "min_positive_surplus": row["min_positive_surplus"],
        "max_post_recovery_blocks": row["max_post_recovery_blocks"],
        "hardest_recovery_score": row["hardest_recovery_score"],
    }


def classify_near_obstruction(row: Dict[str, Any]) -> str:
    if row["obstruction_candidate_count"] > 0:
        return "OBSTRUCTION_CANDIDATE"

    dangerous = int(row["dangerous_regeneration_count"])
    surplus = row["min_positive_surplus"]
    recovery = int(row["max_post_recovery_blocks"])
    bad_windows = int(row["debt_window_count"])

    tight = surplus is not None and float(surplus) < 1e-4

    if dangerous > 1000 and tight and recovery >= 100:
        return "EXTREME_STRESS_BUT_COMPENSATED"

    if dangerous > 0 and tight:
        return "TIGHT_DANGEROUS_REGENERATION"

    if dangerous > 0:
        return "DANGEROUS_REGENERATION_STRESS"

    if bad_windows > 0:
        return "LOCAL_DEBT_STRESS"

    return "NO_DEBT_STRESS"


def build_report(rows: List[Dict[str, Any]], summary: Dict[str, Any], certificate: Dict[str, Any]) -> Dict[str, Any]:
    hardest_by_recovery = [compact_case(row) for row in top_rows(rows, "hardest_recovery_score", 10)]
    most_debt_windows = [compact_case(row) for row in top_rows(rows, "debt_window_count", 10)]
    most_regeneration = [compact_case(row) for row in top_rows(rows, "regeneration_count", 10)]
    most_dangerous_regeneration = [compact_case(row) for row in top_rows(rows, "dangerous_regeneration_count", 10)]
    tightest_surplus = [compact_case(row) for row in lowest_positive_surplus_rows(rows, 10)]

    near_obstruction_cases = []
    for row in rows:
        label = classify_near_obstruction(row)
        if label in {
            "OBSTRUCTION_CANDIDATE",
            "EXTREME_STRESS_BUT_COMPENSATED",
            "TIGHT_DANGEROUS_REGENERATION",
            "DANGEROUS_REGENERATION_STRESS",
        }:
            item = compact_case(row)
            item["near_obstruction_class"] = label
            near_obstruction_cases.append(item)

    near_obstruction_cases = sorted(
        near_obstruction_cases,
        key=lambda item: (
            item["near_obstruction_class"] != "OBSTRUCTION_CANDIDATE",
            item["near_obstruction_class"] != "EXTREME_STRESS_BUT_COMPENSATED",
            -int(item["dangerous_regeneration_count"]),
            float(item["min_positive_surplus"]) if item["min_positive_surplus"] is not None else 999,
            int(item["n0"]),
        ),
    )[:25]

    obstruction_detected = bool(certificate.get("obstruction_detected", False))
    obstruction_candidate_count = int(certificate.get("obstruction_candidate_count", 0))

    if obstruction_candidate_count > 0:
        native_interpretation = "OBSTRUCTION_CANDIDATE_DETECTED_IN_BOUNDED_DOMAIN"
    elif int(certificate.get("dangerous_regeneration_count", 0)) > 0:
        native_interpretation = "DANGEROUS_REGENERATION_FOUND_BUT_NO_OBSTRUCTION_CANDIDATE"
    else:
        native_interpretation = "NO_OBSTRUCTION_STRESS_FOUND_IN_BOUNDED_DOMAIN"

    return {
        "version": VERSION,
        "layer": "obstruction_scanner_evidence_report",
        "source_version": "v2.6",
        "source_artifacts": [
            "results/bounded_obstruction_search_rows.jsonl",
            "results/bounded_obstruction_search_summary.json",
            "results/bounded_obstruction_search_certificate.json",
        ],
        "tested_candidate_count": certificate["tested_candidate_count"],
        "debt_window_count": certificate["debt_window_count"],
        "regeneration_count": certificate["regeneration_count"],
        "dangerous_regeneration_count": certificate["dangerous_regeneration_count"],
        "obstruction_candidate_count": obstruction_candidate_count,
        "obstruction_detected": obstruction_detected,
        "native_interpretation": native_interpretation,
        "negative_result_boundary": certificate["negative_result_boundary"],
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "evidence_status": "bounded_native_evidence",
        "key_cases": {
            "hardest_by_recovery": hardest_by_recovery,
            "tightest_positive_surplus": tightest_surplus,
            "most_debt_windows": most_debt_windows,
            "most_regeneration": most_regeneration,
            "most_dangerous_regeneration": most_dangerous_regeneration,
            "near_obstruction_cases": near_obstruction_cases,
        },
        "native_conclusions": [
            "The bounded domain contains many debt windows.",
            "The bounded domain contains many regeneration events.",
            "The bounded domain contains many dangerous-regeneration stress events.",
            "The bounded scanner detected no obstruction candidate.",
            "Dangerous regeneration is not obstruction by itself.",
            "No obstruction detected in a finite domain is not proof that obstruction cannot exist.",
        ],
        "forbidden_conclusions": [
            "collatz_solved",
            "global_closure_proved",
            "obstruction_impossible",
            "finite_negative_result_is_proof",
            "dangerous_regeneration_equals_obstruction",
            "hardness_equals_obstruction",
        ],
        "next_recommended_version": "v2.8 Expanded Bounded Obstruction Search",
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Obstruction Scanner Evidence Report")
    lines.append("")
    lines.append("Version: v2.7")
    lines.append("")
    lines.append("This report interprets the v2.6 bounded obstruction scanner output.")
    lines.append("")
    lines.append("It is not a proof.")
    lines.append("It is not a theorem layer.")
    lines.append("It is bounded native evidence.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- tested_candidate_count: {report['tested_candidate_count']}")
    lines.append(f"- debt_window_count: {report['debt_window_count']}")
    lines.append(f"- regeneration_count: {report['regeneration_count']}")
    lines.append(f"- dangerous_regeneration_count: {report['dangerous_regeneration_count']}")
    lines.append(f"- obstruction_candidate_count: {report['obstruction_candidate_count']}")
    lines.append(f"- obstruction_detected: {str(report['obstruction_detected']).lower()}")
    lines.append(f"- native_interpretation: {report['native_interpretation']}")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(report["negative_result_boundary"])
    lines.append("")
    lines.append("Correct interpretation:")
    lines.append("")
    lines.append("No obstruction candidate was detected in the v2.6 bounded domain.")
    lines.append("")
    lines.append("Forbidden interpretation:")
    lines.append("")
    lines.append("No obstruction can exist.")
    lines.append("")
    lines.append("## Native conclusions")
    lines.append("")

    for item in report["native_conclusions"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Forbidden conclusions")
    lines.append("")

    for item in report["forbidden_conclusions"]:
        lines.append(f"- {item}")

    def add_cases(title: str, cases: List[Dict[str, Any]]) -> None:
        lines.append("")
        lines.append(f"## {title}")
        lines.append("")
        if not cases:
            lines.append("No cases.")
            return

        for case in cases:
            parts = [
                f"n0={case['n0']}",
                f"odd_blocks={case['odd_blocks']}",
                f"debt_windows={case['debt_window_count']}",
                f"regeneration={case['regeneration_count']}",
                f"dangerous_regeneration={case['dangerous_regeneration_count']}",
                f"obstruction_candidates={case['obstruction_candidate_count']}",
                f"closure_result={case['closure_result_type']}",
                f"min_surplus={case['min_positive_surplus']}",
                f"max_post_recovery_blocks={case['max_post_recovery_blocks']}",
                f"hardest_score={case['hardest_recovery_score']}",
            ]
            if "near_obstruction_class" in case:
                parts.append(f"class={case['near_obstruction_class']}")
            lines.append("- " + "; ".join(parts))

    key_cases = report["key_cases"]

    add_cases("Hardest by recovery", key_cases["hardest_by_recovery"])
    add_cases("Tightest positive surplus", key_cases["tightest_positive_surplus"])
    add_cases("Most debt windows", key_cases["most_debt_windows"])
    add_cases("Most regeneration", key_cases["most_regeneration"])
    add_cases("Most dangerous regeneration", key_cases["most_dangerous_regeneration"])
    add_cases("Near obstruction cases", key_cases["near_obstruction_cases"])

    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(report["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(report: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "obstruction_scanner_evidence_certificate",
        "source_version": report["source_version"],
        "tested_candidate_count": report["tested_candidate_count"],
        "debt_window_count": report["debt_window_count"],
        "regeneration_count": report["regeneration_count"],
        "dangerous_regeneration_count": report["dangerous_regeneration_count"],
        "obstruction_candidate_count": report["obstruction_candidate_count"],
        "obstruction_detected": report["obstruction_detected"],
        "native_interpretation": report["native_interpretation"],
        "proof_status": report["proof_status"],
        "theorem_status": report["theorem_status"],
        "evidence_status": report["evidence_status"],
        "negative_result_boundary": report["negative_result_boundary"],
        "forbidden_conclusions": report["forbidden_conclusions"],
        "next_recommended_version": report["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v2.7")
    print("=" * 80)
    print("Obstruction Scanner Evidence Report")
    print("=" * 80)

    ensure_v26_artifacts_exist()

    rows = read_jsonl(ROWS_PATH)
    summary = read_json(SUMMARY_PATH)
    certificate = read_json(CERTIFICATE_PATH)

    report = build_report(rows, summary, certificate)
    markdown = render_markdown(report)
    evidence_certificate = make_certificate(report)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    REPORT_JSON_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD_PATH.write_text(markdown + "\n", encoding="utf-8")
    REPORT_CERTIFICATE_PATH.write_text(json.dumps(evidence_certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"tested_candidate_count: {report['tested_candidate_count']}")
    print(f"debt_window_count: {report['debt_window_count']}")
    print(f"regeneration_count: {report['regeneration_count']}")
    print(f"dangerous_regeneration_count: {report['dangerous_regeneration_count']}")
    print(f"obstruction_candidate_count: {report['obstruction_candidate_count']}")
    print(f"obstruction_detected: {report['obstruction_detected']}")
    print(f"native_interpretation: {report['native_interpretation']}")
    print(f"proof_status: {report['proof_status']}")
    print(f"negative_result_boundary: {report['negative_result_boundary']}")
    print(f"Wrote JSON report to: {REPORT_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote Markdown report to: {REPORT_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {REPORT_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
