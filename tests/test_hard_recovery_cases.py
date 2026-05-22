import json
import math
import subprocess
import sys
from pathlib import Path

def test_hard_recovery_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_hard_recovery_cases.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.9" in result.stdout
    assert "hard recovery cases" in result.stdout.lower()
    assert "hardest overall" in result.stdout

def test_hard_recovery_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "hard_recovery_cases.jsonl"
    summary_path = root / "results" / "hard_recovery_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.9"
    assert summary["total_chain_episodes"] >= 1
    assert "top_by_hardness_score" in summary
    assert "top_by_recovery_distance" in summary
    assert "top_by_smallest_surplus" in summary

def test_hard_recovery_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "hard_recovery_cases.jsonl"

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
        "chain_deficit_below_threshold",
        "post_chain_recovery_found",
        "post_chain_recovery_distance_blocks",
        "post_chain_recovery_surplus",
        "recovery_distance_gap",
        "hardness_score",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())

def test_hardness_score_is_finite_for_recovered_rows():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "hard_recovery_cases.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    recovered = [row for row in rows if row["post_chain_recovery_found"]]
    assert recovered

    for row in recovered[:100]:
        assert isinstance(row["hardness_score"], float)
        assert math.isfinite(row["hardness_score"])
