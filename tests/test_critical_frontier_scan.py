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
    assert "COLLATZ-NATIVE-MATH v1.1" in result.stdout
    assert "Critical frontier scan" in result.stdout
    assert "Frontier summary" in result.stdout

def test_critical_frontier_results_exist():
    root = Path(__file__).resolve().parents[1]

    scan_path = root / "results" / "critical_frontier_scan.jsonl"
    summary_path = root / "results" / "critical_frontier_summary.json"

    assert scan_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in scan_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert rows
    assert summary["version"] == "v1.1"
    assert summary["candidate_count"] == len(rows)
    assert summary["previous_critical_n0"] == 9780657630

def test_frontier_contains_previous_critical():
    root = Path(__file__).resolve().parents[1]
    scan_path = root / "results" / "critical_frontier_scan.jsonl"

    rows = [
        json.loads(line)
        for line in scan_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    previous = [row for row in rows if row["n0"] == 9780657630]

    assert previous
    row = previous[0]
    assert row["reaches_1"] is True
    assert row["max_post_chain_recovery_distance"] >= 100
    assert row["max_hardness_score"] >= 15.0

def test_frontier_summary_has_hardest_case():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "critical_frontier_summary.json"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    hardest = summary["current_hardest"]

    assert hardest is not None
    assert hardest["n0"] > 0
    assert hardest["max_hardness_score"] > 0
    assert hardest["hardest_episode"] is not None
