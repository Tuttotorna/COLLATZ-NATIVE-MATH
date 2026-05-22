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
    assert "COLLATZ-NATIVE-MATH v1.5" in result.stdout
    assert "Hardness metric report builder" in result.stdout
    assert "frontier_recovery_hardness" in result.stdout
    assert "adversarial_compensation_hardness" in result.stdout


def test_hardness_metric_report_files_exist():
    root = Path(__file__).resolve().parents[1]

    json_path = root / "results" / "hardness_metric_report.json"
    md_path = root / "results" / "hardness_metric_report.md"

    assert json_path.exists()
    assert md_path.exists()

    report = json.loads(json_path.read_text(encoding="utf-8"))
    md = md_path.read_text(encoding="utf-8")

    assert report["version"] == "v1.5"
    assert report["report_type"] == "hardness_metric_report"
    assert len(report["metrics"]) >= 5
    assert "There is not one single meaning" in md
    assert "frontier_recovery_hardness" in md
    assert "compensation_window_hardness" in md
    assert "adversarial_compensation_hardness" in md
    assert "tightest_positive_surplus" in md
    assert "known_long_trajectory_anchor" in md


def test_hardness_metrics_are_not_treated_as_contradictions():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "results" / "hardness_metric_report.json"

    report = json.loads(json_path.read_text(encoding="utf-8"))
    check = report["contradiction_check"]

    assert check["multiple_hardness_lenses"] is True
    assert check["is_contradiction"] is False
    assert "Different metrics answer different questions" in check["reason"]


def test_required_known_metric_ids_present():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "results" / "hardness_metric_report.json"

    report = json.loads(json_path.read_text(encoding="utf-8"))
    metric_ids = {metric["metric_id"] for metric in report["metrics"]}

    assert "frontier_recovery_hardness" in metric_ids
    assert "compensation_window_hardness" in metric_ids
    assert "adversarial_compensation_hardness" in metric_ids
    assert "tightest_positive_surplus" in metric_ids
    assert "known_long_trajectory_anchor" in metric_ids


def test_expected_frontier_and_adversarial_cases_are_visible():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "results" / "hardness_metric_report.json"

    report = json.loads(json_path.read_text(encoding="utf-8"))
    by_id = {metric["metric_id"]: metric for metric in report["metrics"]}

    assert by_id["frontier_recovery_hardness"]["hardest_n0"] == 9780657630
    assert by_id["frontier_recovery_hardness"]["primary_value"] == 114

    assert by_id["adversarial_compensation_hardness"]["hardest_n0"] == 63728127
    assert by_id["adversarial_compensation_hardness"]["primary_value"] > 0

    assert by_id["known_long_trajectory_anchor"]["hardest_n0"] == 837799
