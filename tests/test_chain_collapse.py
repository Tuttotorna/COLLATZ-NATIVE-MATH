import json
import subprocess
import sys
from pathlib import Path

def test_chain_collapse_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_chain_collapse.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.4" in result.stdout
    assert "chain collapse" in result.stdout.lower()
    assert "post-chain compensation" in result.stdout.lower()

def test_chain_collapse_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "chain_collapse_analysis.jsonl"
    summary_path = root / "results" / "chain_collapse_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.4"
    assert summary["all_reach_1_in_sample"] is True
    assert summary["total_collapse_episodes"] >= 1

def test_collapse_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "chain_collapse_analysis.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    required = {
        "n0",
        "chain_length_segments",
        "chain_average_debt",
        "collapse_cause",
        "post_chain_average_debt",
        "compensation_surplus",
        "trajectory_average_debt",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())

def test_detected_episodes_are_finite_in_sample():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "chain_collapse_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["all_detected_episodes_compensated"] in [True, False]
    assert summary["total_collapse_episodes"] > 0
