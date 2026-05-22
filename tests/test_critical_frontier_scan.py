import json
import subprocess
import sys
from pathlib import Path


def test_critical_frontier_scan_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "scan_critical_frontier.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.2" in result.stdout
    assert "Critical frontier scan with stability certificate" in result.stdout
    assert "comparison status:" in result.stdout
    assert "frontier stable:" in result.stdout


def test_critical_frontier_results_exist():
    root = Path(__file__).resolve().parents[1]

    scan_path = root / "results" / "critical_frontier_scan.jsonl"
    summary_path = root / "results" / "critical_frontier_summary.json"
    certificate_path = root / "results" / "frontier_stability_certificate.json"

    assert scan_path.exists()
    assert summary_path.exists()
    assert certificate_path.exists()

    rows = [
        json.loads(line)
        for line in scan_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))

    assert rows

    assert summary["version"] == "v1.2"
    assert summary["previous_critical_n0"] == 9780657630
    assert summary["previous_critical_hardness"] == 15.100955299032181
    assert summary["current_hardest"]["n0"] == 9780657630
    assert summary["comparison_status"] == "SAME_AS_PREVIOUS"
    assert summary["same_case"] is True
    assert summary["harder_than_previous_critical"] is False
    assert summary["frontier_stable"] is True

    assert certificate["version"] == "v1.2"
    assert certificate["certificate_type"] == "frontier_stability_certificate"
    assert certificate["previous_critical_n0"] == 9780657630
    assert certificate["previous_critical_hardness"] == 15.100955299032181
    assert certificate["current_hardest_n0"] == 9780657630
    assert certificate["comparison_status"] == "SAME_AS_PREVIOUS"
    assert certificate["same_case"] is True
    assert certificate["harder_than_previous_critical"] is False
    assert certificate["frontier_stable"] is True


def test_previous_critical_still_active_frontier():
    root = Path(__file__).resolve().parents[1]

    summary_path = root / "results" / "critical_frontier_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    hardest = summary["current_hardest"]

    assert hardest["n0"] == 9780657630
    assert hardest["max_post_chain_recovery_distance"] == 114
    assert hardest["min_post_chain_recovery_surplus"] == 0.00275679752445801
    assert hardest["max_hardness_score"] == 15.100955299032181
    assert summary["comparison_status"] == "SAME_AS_PREVIOUS"
    assert summary["frontier_stable"] is True
