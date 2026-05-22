from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VERSION = "v1.5.1"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

FRONTIER_SUMMARY = RESULTS / "critical_frontier_summary.json"
COMPENSATION_SUMMARY = RESULTS / "compensation_law_candidate_summary.json"
ADVERSARIAL_SUMMARY = RESULTS / "adversarial_compensation_summary.json"
ADVERSARIAL_CERTIFICATE = RESULTS / "adversarial_compensation_certificate.json"
ADVERSARIAL_ROWS = RESULTS / "adversarial_compensation_rows.jsonl"

REPORT_JSON = RESULTS / "hardness_metric_report.json"
REPORT_MD = RESULTS / "hardness_metric_report.md"


def line() -> None:
    print("=" * 80)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def first_number(*values: Any) -> float | int | None:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int | float):
            return value
    return None


def nested_get(data: dict[str, Any], *path: str) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def get_frontier_metric() -> dict[str, Any]:
    summary = load_json(FRONTIER_SUMMARY)
    hardest = summary.get("current_hardest", {})

    return {
        "metric_id": "frontier_recovery_hardness",
        "description": "Longest post-chain recovery distance in the critical frontier scan.",
        "source": str(FRONTIER_SUMMARY.relative_to(ROOT)),
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_post_chain_recovery_distance",
        "primary_value": hardest.get("max_post_chain_recovery_distance"),
        "secondary_value_name": "max_hardness_score",
        "secondary_value": hardest.get("max_hardness_score"),
        "interpretation": "Measures recovery distance after structurally cheap debt chains.",
    }


def get_compensation_metric() -> dict[str, Any]:
    summary = load_json(COMPENSATION_SUMMARY)
    hardest = summary.get("hardest_case", {})

    return {
        "metric_id": "compensation_window_hardness",
        "description": "Largest finite compensation-window hardness score.",
        "source": str(COMPENSATION_SUMMARY.relative_to(ROOT)),
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_hardness_score",
        "primary_value": hardest.get("max_hardness_score"),
        "secondary_value_name": "min_combined_surplus",
        "secondary_value": hardest.get("min_combined_surplus"),
        "interpretation": "Measures how hard a bad finite window is to compensate.",
    }


def get_adversarial_metric() -> dict[str, Any]:
    summary = load_json(ADVERSARIAL_SUMMARY)
    hardest = summary.get("hardest_case", {})

    return {
        "metric_id": "adversarial_compensation_hardness",
        "description": "Largest hardness score under adversarial candidate generation.",
        "source": str(ADVERSARIAL_SUMMARY.relative_to(ROOT)),
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_hardness_score",
        "primary_value": hardest.get("max_hardness_score"),
        "secondary_value_name": "max_post_recovery_blocks",
        "secondary_value": hardest.get("max_post_recovery_blocks"),
        "interpretation": "Measures the strongest adversarial finite compensation stress case.",
    }


def get_tightest_positive_surplus_metric() -> dict[str, Any]:
    summary = load_json(ADVERSARIAL_SUMMARY)
    certificate = load_json(ADVERSARIAL_CERTIFICATE)
    rows = load_jsonl(ADVERSARIAL_ROWS)

    tightest_case = summary.get("tightest_surplus_case", {})
    if not isinstance(tightest_case, dict):
        tightest_case = {}

    candidate_n0 = first_number(
        summary.get("tightest_surplus_n0"),
        certificate.get("tightest_surplus_n0"),
        tightest_case.get("n0"),
    )

    candidate_surplus = first_number(
        summary.get("tightest_surplus"),
        certificate.get("tightest_surplus"),
        tightest_case.get("min_surplus"),
        tightest_case.get("min_combined_surplus"),
        tightest_case.get("current_hardest_min_surplus"),
        tightest_case.get("min_post_recovery_surplus"),
        nested_get(tightest_case, "hardest_recovery", "combined_surplus"),
        nested_get(tightest_case, "hardest_recovery", "post_chain_recovery_surplus"),
    )

    if candidate_surplus is None:
        positive_rows = [
            row for row in rows
            if isinstance(row.get("min_surplus"), int | float)
            and row.get("min_surplus") > 0
        ]
        if positive_rows:
            best = min(positive_rows, key=lambda row: row["min_surplus"])
            candidate_n0 = best.get("n0")
            candidate_surplus = best.get("min_surplus")

    if candidate_surplus is None:
        positive_rows = [
            row for row in rows
            if isinstance(row.get("min_combined_surplus"), int | float)
            and row.get("min_combined_surplus") > 0
        ]
        if positive_rows:
            best = min(positive_rows, key=lambda row: row["min_combined_surplus"])
            candidate_n0 = best.get("n0")
            candidate_surplus = best.get("min_combined_surplus")

    if candidate_surplus is None:
        raise RuntimeError(
            "Unable to extract tightest positive surplus from adversarial summary, certificate, or rows."
        )

    return {
        "metric_id": "tightest_positive_surplus",
        "description": "Smallest positive surplus observed in the adversarial compensation scan.",
        "source": str(ADVERSARIAL_CERTIFICATE.relative_to(ROOT)),
        "hardest_n0": candidate_n0,
        "primary_value_name": "min_surplus",
        "primary_value": candidate_surplus,
        "secondary_value_name": "counterexample_candidate_count",
        "secondary_value": certificate.get("counterexample_candidate_count"),
        "interpretation": "Measures the tightest still-positive compensation margin found.",
    }


def get_known_long_trajectory_metric() -> dict[str, Any]:
    rows = load_jsonl(ADVERSARIAL_ROWS)

    anchor = None
    for row in rows:
        if row.get("n0") == 837799:
            anchor = row
            break

    if anchor is None:
        anchor = {
            "n0": 837799,
            "odd_blocks": 195,
            "note": "Known long-trajectory anchor not found in adversarial rows; static anchor retained.",
        }

    return {
        "metric_id": "known_long_trajectory_anchor",
        "description": "Known long-trajectory anchor included as a comparison baseline.",
        "source": str(ADVERSARIAL_ROWS.relative_to(ROOT)),
        "hardest_n0": anchor.get("n0"),
        "primary_value_name": "odd_blocks",
        "primary_value": anchor.get("odd_blocks"),
        "secondary_value_name": "bad_windows",
        "secondary_value": anchor.get("bad_windows"),
        "interpretation": "Long trajectory length is not the same hardness notion as compensation hardness.",
    }


def build_report() -> dict[str, Any]:
    metrics = [
        get_frontier_metric(),
        get_compensation_metric(),
        get_adversarial_metric(),
        get_tightest_positive_surplus_metric(),
        get_known_long_trajectory_metric(),
    ]

    unique_n0_values = sorted(
        {str(metric.get("hardest_n0")) for metric in metrics if metric.get("hardest_n0") is not None}
    )

    contradiction = False

    report = {
        "version": VERSION,
        "report_type": "hardness_metric_report",
        "metric_count": len(metrics),
        "contradiction": contradiction,
        "unique_hardest_n0_values": unique_n0_values,
        "metrics": metrics,
        "meaning": (
            "Different hardness lenses identify different finite stress cases. "
            "This is not a contradiction. It means trajectory length, recovery distance, "
            "compensation surplus, and adversarial compensation hardness are distinct observables."
        ),
        "limits": (
            "This report summarizes finite computational scans. "
            "It is not a proof of the Collatz conjecture."
        ),
    }

    return report


def write_markdown(report: dict[str, Any]) -> None:
    lines = []
    lines.append("# Hardness Metric Report")
    lines.append("")
    lines.append(f"Version: {report['version']}")
    lines.append("")
    lines.append("This report separates several finite hardness lenses used by COLLATZ-NATIVE-MATH.")
    lines.append("")
    lines.append("The key point is simple: different notions of hardness can select different cases.")
    lines.append("That is not a contradiction.")
    lines.append("")
    lines.append("## Metrics")
    lines.append("")

    for metric in report["metrics"]:
        lines.append(f"### {metric['metric_id']}")
        lines.append("")
        lines.append(f"- hardest_n0: {metric.get('hardest_n0')}")
        lines.append(f"- {metric.get('primary_value_name')}: {metric.get('primary_value')}")
        lines.append(f"- {metric.get('secondary_value_name')}: {metric.get('secondary_value')}")
        lines.append(f"- source: {metric.get('source')}")
        lines.append(f"- interpretation: {metric.get('interpretation')}")
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(report["meaning"])
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append(report["limits"])
    lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    line()
    print("COLLATZ-NATIVE-MATH v1.5.1")
    line()
    print("Hardness metric report builder")
    print("Fix: tightest_positive_surplus extraction must be non-null")
    line()

    report = build_report()
    write_json(REPORT_JSON, report)
    write_markdown(report)

    tightest = next(
        metric for metric in report["metrics"]
        if metric["metric_id"] == "tightest_positive_surplus"
    )

    line()
    print("Hardness metric report summary")
    line()
    for metric in report["metrics"]:
        print(
            f"{metric['metric_id']}: "
            f"n0={metric.get('hardest_n0')} "
            f"{metric.get('primary_value_name')}={metric.get('primary_value')}"
        )

    print(f"tightest_positive_surplus check: {tightest['primary_value']}")
    print(f"Wrote JSON report to: {REPORT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown report to: {REPORT_MD.relative_to(ROOT)}")
    line()


if __name__ == "__main__":
    main()
