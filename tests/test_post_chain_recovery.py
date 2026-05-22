import json
import subprocess
import sys
from pathlib import Path

def test_post_chain_recovery_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_post_chain_recovery.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.8" in result.stdout
    assert "post-chain recovery" in result.stdout.lower()
    assert "post_chain_recovered_episodes" in result.stdout

def test_post_chain_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "post_chain_recovery_analysis.jsonl"
    summary_path = root / "results" / "post_chain_recovery_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.8"
    assert summary["total_chain_episodes"] >= 1
    assert "post_chain_recovered_episodes" in summary
    assert "post_chain_unrecovered_episodes" in summary

def test_post_chain_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "post_chain_recovery_analysis.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    required = {
        "n0",
        "chain_start_block",
        "chain_end_block",
        "chain_average_debt",
        "chain_start_recovery_found",
        "chain_start_recovery_distance_blocks",
        "post_chain_recovery_found",
        "post_chain_recovery_distance_blocks",
        "post_chain_unrecovered",
        "recovery_distance_gap",
        "trajectory_average_debt",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())

def test_post_chain_recovery_counts_are_consistent():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "post_chain_recovery_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    total = summary["total_chain_episodes"]
    recovered = summary["post_chain_recovered_episodes"]
    unrecovered = summary["post_chain_unrecovered_episodes"]

    assert recovered + unrecovered == total
