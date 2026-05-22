from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VERSION = "v1.5"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

FRONTIER_SUMMARY = RESULTS / "critical_frontier_summary.json"
FRONTIER_CERTIFICATE = RESULTS / "frontier_stability_certificate.json"

COMPENSATION_SUMMARY = RESULTS / "compensation_law_candidate_summary.json"
COMPENSATION_CERTIFICATE = RESULTS / "compensation_law_candidate_certificate.json"

ADVERSARIAL_SUMMARY = RESULTS / "adversarial_compensation_summary.json"
ADVERSARIAL_CERTIFICATE = RESULTS / "adversarial_compensation_certificate.json"

REPORT_JSON = RESULTS / "hardness_metric_report.json"
REPORT_MD = RESULTS / "hardness_metric_report.md"


def line() -> None:
    print("=" * 80)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "missing": True,
            "path": str(path.relative_to(ROOT)),
        }
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def frontier_metric(frontier_summary: dict[str, Any]) -> dict[str, Any]:
    hardest = frontier_summary.get("current_hardest", {})
    return {
        "metric_id": "frontier_recovery_hardness",
        "metric_name": "Frontier recovery hardness",
        "source": "results/critical_frontier_summary.json",
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_post_chain_recovery_distance",
        "primary_value": hardest.get("max_post_chain_recovery_distance"),
        "secondary_value_name": "max_hardness_score",
        "secondary_value": hardest.get("max_hardness_score"),
        "min_surplus": hardest.get("min_post_chain_recovery_surplus"),
        "meaning": (
            "Measures the hardest finite frontier case by post-chain recovery distance "
            "inside the critical frontier protocol."
        ),
        "limit": (
            "This is a finite frontier metric. It is not a global Collatz proof and "
            "does not define the only possible meaning of hardness."
        ),
    }


def compensation_metric(comp_summary: dict[str, Any]) -> dict[str, Any]:
    hardest = comp_summary.get("hardest_case", {})
    return {
        "metric_id": "compensation_window_hardness",
        "metric_name": "Compensation-window hardness",
        "source": "results/compensation_law_candidate_summary.json",
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_hardness_score",
        "primary_value": hardest.get("max_hardness_score"),
        "secondary_value_name": "min_combined_surplus",
        "secondary_value": hardest.get("min_combined_surplus"),
        "bad_windows": hardest.get("bad_windows"),
        "all_bad_windows_recovered": comp_summary.get("all_bad_windows_recovered"),
        "meaning": (
            "Measures the hardest case under the finite compensation-window candidate "
            "protocol, where bad local windows must be recovered by later surplus."
        ),
        "limit": (
            "This metric is window-protocol dependent. A larger value here does not "
            "automatically replace the frontier-recovery hardest case."
        ),
    }


def adversarial_metric(adv_summary: dict[str, Any]) -> dict[str, Any]:
    hardest = adv_summary.get("hardest_case", {})
    tightest = adv_summary.get("tightest_surplus_case", {})
    return {
        "metric_id": "adversarial_compensation_hardness",
        "metric_name": "Adversarial compensation hardness",
        "source": "results/adversarial_compensation_summary.json",
        "hardest_n0": hardest.get("n0"),
        "primary_value_name": "max_hardness_score",
        "primary_value": hardest.get("max_hardness_score"),
        "secondary_value_name": "max_post_recovery_blocks",
        "secondary_value": hardest.get("max_post_recovery_blocks"),
        "tightest_surplus_n0": tightest.get("n0"),
        "tightest_surplus": tightest.get("min_surplus"),
        "counterexample_candidate_count": adv_summary.get("counterexample_candidate_count"),
        "all_bad_windows_recovered": adv_summary.get("all_bad_windows_recovered"),
        "meaning": (
            "Measures hardness under an adversarially generated finite candidate set, "
            "searching for bad compensation windows and counterexample candidates."
        ),
        "limit": (
            "This is a stronger finite stress test than the basic compensation scan, "
            "but it remains finite and candidate-set dependent."
        ),
    }


def tightest_surplus_metric(comp_summary: dict[str, Any], adv_summary: dict[str, Any]) -> dict[str, Any]:
    comp_case = comp_summary.get("tightest_surplus_case", {})
    adv_case = adv_summary.get("tightest_surplus_case", {})

    comp_surplus = as_float(comp_case.get("min_surplus"), default=float("inf"))
    adv_surplus = as_float(adv_case.get("min_surplus"), default=float("inf"))

    if adv_surplus <= comp_surplus:
        selected = adv_case
        source = "results/adversarial_compensation_summary.json"
        protocol = "adversarial_compensation"
        value = adv_surplus
    else:
        selected = comp_case
        source = "results/compensation_law_candidate_summary.json"
        protocol = "compensation_law_candidate"
        value = comp_surplus

    if value == float("inf"):
        value = None

    return {
        "metric_id": "tightest_positive_surplus",
        "metric_name": "Tightest positive surplus",
        "source": source,
        "protocol": protocol,
        "hardest_n0": selected.get("n0"),
        "primary_value_name": "min_surplus",
        "primary_value": value,
        "secondary_value_name": "max_post_recovery_blocks",
        "secondary_value": selected.get("max_post_recovery_blocks"),
        "meaning": (
            "Identifies the closest observed recovery margin above the escape threshold "
            "among available compensation-style scans."
        ),
        "limit": (
            "A tiny positive surplus is evidence of near-critical compensation in the "
            "tested domain, not evidence that all possible domains are covered."
        ),
    }


def known_anchor_metric(frontier_summary: dict[str, Any], comp_summary: dict[str, Any], adv_summary: dict[str, Any]) -> dict[str, Any]:
    known_n0 = 837799

    # Try to recover known anchor from available row files.
    candidate = None
    for rel in [
        "adversarial_compensation_rows.jsonl",
        "compensation_law_candidate_rows.jsonl",
        "critical_frontier_scan.jsonl",
    ]:
        path = RESULTS / rel
        if not path.exists():
            continue
        for line_text in path.read_text(encoding="utf-8").splitlines():
            if not line_text.strip():
                continue
            row = json.loads(line_text)
            if row.get("n0") == known_n0:
                candidate = {
                    "source": f"results/{rel}",
                    "row": row,
                }
                break
        if candidate:
            break

    row = candidate["row"] if candidate else {}
    source = candidate["source"] if candidate else "not_found"

    return {
        "metric_id": "known_long_trajectory_anchor",
        "metric_name": "Known long-trajectory anchor",
        "source": source,
        "hardest_n0": known_n0,
        "primary_value_name": "odd_blocks",
        "primary_value": row.get("odd_blocks"),
        "secondary_value_name": "bad_windows",
        "secondary_value": row.get("bad_windows"),
        "meaning": (
            "Keeps a familiar long-trajectory reference case visible, so the reader "
            "does not confuse classical trajectory length with the repository's newer "
            "hardness metrics."
        ),
        "limit": (
            "A famous long trajectory is not necessarily the hardest case under "
            "frontier, compensation, or adversarial compensation metrics."
        ),
    }


def contradiction_check(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    by_n0: dict[str, list[str]] = {}
    for metric in metrics:
        n0 = metric.get("hardest_n0")
        if n0 is None:
            continue
        by_n0.setdefault(str(n0), []).append(metric["metric_id"])

    unique_hardest = sorted(by_n0.keys(), key=lambda x: int(x) if x.isdigit() else x)

    return {
        "multiple_hardness_lenses": True,
        "unique_hardest_n0_values": unique_hardest,
        "hardest_n0_to_metrics": by_n0,
        "is_contradiction": False,
        "reason": (
            "Different metrics answer different questions. Different hardest_n0 values "
            "are expected unless two metrics define the same ordering rule."
        ),
    }


def build_markdown(report: dict[str, Any]) -> str:
    rows = []
    for metric in report["metrics"]:
        rows.append(
            "| {metric_id} | {hardest_n0} | {primary_value_name} | {primary_value} | {source} |".format(
                metric_id=metric.get("metric_id"),
                hardest_n0=metric.get("hardest_n0"),
                primary_value_name=metric.get("primary_value_name"),
                primary_value=metric.get("primary_value"),
                source=metric.get("source"),
            )
        )

    rows_text = "\n".join(rows)

    metric_sections = []
    for metric in report["metrics"]:
        metric_sections.append(
            "\n".join(
                [
                    f"## {metric.get('metric_name')}",
                    "",
                    f"- Metric ID: `{metric.get('metric_id')}`",
                    f"- Source: `{metric.get('source')}`",
                    f"- Hardest n0: `{metric.get('hardest_n0')}`",
                    f"- Primary value: `{metric.get('primary_value_name')} = {metric.get('primary_value')}`",
                    f"- Secondary value: `{metric.get('secondary_value_name')} = {metric.get('secondary_value')}`",
                    "",
                    f"Meaning: {metric.get('meaning')}",
                    "",
                    f"Limit: {metric.get('limit')}",
                    "",
                ]
            )
        )

    metric_sections_text = "\n".join(metric_sections)

    return f"""# Hardness Metric Report

Version: {report["version"]}

This report prevents one specific ambiguity:

There is not one single meaning of "hardest Collatz case" in this repository.

Different scanners measure different structural pressures.

## Summary table

| metric_id | hardest_n0 | primary_value_name | primary_value | source |
|---|---:|---|---:|---|
{rows_text}

## Interpretation

The repository now separates at least five hardness lenses:

1. frontier recovery hardness
2. compensation-window hardness
3. adversarial compensation hardness
4. tightest positive surplus
5. known long-trajectory anchor

Different hardest cases are not contradictions unless two metrics claim to measure the same ordering rule.

## Contradiction check

- Multiple hardness lenses: `{report["contradiction_check"]["multiple_hardness_lenses"]}`
- Contradiction: `{report["contradiction_check"]["is_contradiction"]}`
- Reason: {report["contradiction_check"]["reason"]}

{metric_sections_text}

## Boundary

This report is a metric-unification artifact.

It is not a proof of the Collatz conjecture.

It is a finite, auditable map of which case is hardest under which measurement lens.
"""


def main() -> None:
    line()
    print("COLLATZ-NATIVE-MATH v1.5")
    line()
    print("Hardness metric report builder")
    line()

    frontier_summary = load_json(FRONTIER_SUMMARY)
    frontier_certificate = load_json(FRONTIER_CERTIFICATE)
    comp_summary = load_json(COMPENSATION_SUMMARY)
    comp_certificate = load_json(COMPENSATION_CERTIFICATE)
    adv_summary = load_json(ADVERSARIAL_SUMMARY)
    adv_certificate = load_json(ADVERSARIAL_CERTIFICATE)

    metrics = [
        frontier_metric(frontier_summary),
        compensation_metric(comp_summary),
        adversarial_metric(adv_summary),
        tightest_surplus_metric(comp_summary, adv_summary),
        known_anchor_metric(frontier_summary, comp_summary, adv_summary),
    ]

    report = {
        "version": VERSION,
        "report_type": "hardness_metric_report",
        "meaning": (
            "Unifies the repository's hardness vocabulary by separating distinct "
            "measurement lenses."
        ),
        "boundary": (
            "This report is finite, descriptive, and metric-based. It is not a proof "
            "of the Collatz conjecture."
        ),
        "inputs": {
            "frontier_summary": str(FRONTIER_SUMMARY.relative_to(ROOT)),
            "frontier_certificate": str(FRONTIER_CERTIFICATE.relative_to(ROOT)),
            "compensation_summary": str(COMPENSATION_SUMMARY.relative_to(ROOT)),
            "compensation_certificate": str(COMPENSATION_CERTIFICATE.relative_to(ROOT)),
            "adversarial_summary": str(ADVERSARIAL_SUMMARY.relative_to(ROOT)),
            "adversarial_certificate": str(ADVERSARIAL_CERTIFICATE.relative_to(ROOT)),
        },
        "input_status": {
            "frontier_summary_missing": bool(frontier_summary.get("missing")),
            "frontier_certificate_missing": bool(frontier_certificate.get("missing")),
            "compensation_summary_missing": bool(comp_summary.get("missing")),
            "compensation_certificate_missing": bool(comp_certificate.get("missing")),
            "adversarial_summary_missing": bool(adv_summary.get("missing")),
            "adversarial_certificate_missing": bool(adv_certificate.get("missing")),
        },
        "metrics": metrics,
        "contradiction_check": contradiction_check(metrics),
    }

    write_json(REPORT_JSON, report)
    REPORT_MD.write_text(build_markdown(report), encoding="utf-8")

    line()
    print("Hardness metric report summary")
    line()
    for metric in metrics:
        print(
            f"{metric['metric_id']}: "
            f"n0={metric.get('hardest_n0')} "
            f"{metric.get('primary_value_name')}={metric.get('primary_value')}"
        )
    print(f"Wrote JSON report to: {REPORT_JSON.relative_to(ROOT)}")
    print(f"Wrote Markdown report to: {REPORT_MD.relative_to(ROOT)}")
    line()


if __name__ == "__main__":
    main()
