import json
import subprocess
import sys
from pathlib import Path

def test_compensation_law_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_compensation_law.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.7" in result.stdout
    assert "compensation law" in result.stdout
    assert "total_chain_episodes" in result.stdout

def test_compensation_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "compensation_law_search.jsonl"
    summary_path = root / "results" / "compensation_law_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.7"
    assert summary["total_chain_episodes"] >= 1
    assert "all_chain_episodes_recovered" in summary

def test_compensation_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "compensation_law_search.jsonl"

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
        "recovery_found",
        "recovery_distance_blocks",
        "recovery_average_debt",
        "recovery_surplus",
        "trajectory_average_debt",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())

def test_recovered_windows_cross_threshold():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "compensation_law_search.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    for row in rows:
        if row["recovery_found"]:
            assert row["recovery_average_debt"] > row["escape_threshold_log2_3"] if "escape_threshold_log2_3" in row else True
            assert row["recovery_surplus"] > 0
