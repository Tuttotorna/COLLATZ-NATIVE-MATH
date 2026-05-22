import json
import subprocess
import sys
from pathlib import Path


def test_hardness_metric_report_builder_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_hardness_metric_report.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.5.1" in result.stdout
    assert "Hardness metric report builder" in result.stdout
    assert "tightest_positive_surplus check:" in result.stdout


def test_hardness_metric_report_exists_and_is_structured():
    root = Path(__file__).resolve().parents[1]
    report_path = root / "results" / "hardness_metric_report.json"
    report_md_path = root / "results" / "hardness_metric_report.md"

    assert report_path.exists()
    assert report_md_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["version"] == "v1.5.1"
    assert report["report_type"] == "hardness_metric_report"
    assert report["metric_count"] == 5
    assert report["contradiction"] is False

    metric_ids = {metric["metric_id"] for metric in report["metrics"]}

    assert "frontier_recovery_hardness" in metric_ids
    assert "compensation_window_hardness" in metric_ids
    assert "adversarial_compensation_hardness" in metric_ids
    assert "tightest_positive_surplus" in metric_ids
    assert "known_long_trajectory_anchor" in metric_ids


def test_tightest_positive_surplus_is_not_null():
    root = Path(__file__).resolve().parents[1]
    report_path = root / "results" / "hardness_metric_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    metric = next(
        metric for metric in report["metrics"]
        if metric["metric_id"] == "tightest_positive_surplus"
    )

    assert metric["hardest_n0"] == 63728127
    assert metric["primary_value_name"] == "min_surplus"
    assert metric["primary_value"] is not None
    assert metric["primary_value"] > 0
    assert metric["primary_value"] == 1.7736432994075457e-05


def test_hardness_lenses_can_select_different_cases():
    root = Path(__file__).resolve().parents[1]
    report_path = root / "results" / "hardness_metric_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    values = {
        metric["metric_id"]: metric["hardest_n0"]
        for metric in report["metrics"]
    }

    assert values["frontier_recovery_hardness"] == 9780657630
    assert values["compensation_window_hardness"] == 670617279
    assert values["adversarial_compensation_hardness"] == 63728127
    assert values["tightest_positive_surplus"] == 63728127
    assert values["known_long_trajectory_anchor"] == 837799

    assert len(set(values.values())) >= 4
