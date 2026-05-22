import json
import subprocess
import sys
from pathlib import Path

def test_critical_case_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_critical_case.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.0" in result.stdout
    assert "Critical case dissection" in result.stdout
    assert "post-chain recovery distance" in result.stdout

def test_critical_case_results_written():
    root = Path(__file__).resolve().parents[1]

    dissection_path = root / "results" / "critical_case_dissection.json"
    blocks_path = root / "results" / "critical_case_blocks.jsonl"
    window_path = root / "results" / "critical_case_window.jsonl"
    summary_path = root / "results" / "critical_case_summary.json"

    assert dissection_path.exists()
    assert blocks_path.exists()
    assert window_path.exists()
    assert summary_path.exists()

    dissection = json.loads(dissection_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert dissection["version"] == "v1.0"
    assert summary["version"] == "v1.0"
    assert dissection["n0"] == 9780657630
    assert summary["n0"] == 9780657630
    assert summary["post_chain_recovery_distance_blocks"] >= 1
    assert summary["post_chain_recovery_surplus"] > 0

def test_critical_case_window_has_crossing():
    root = Path(__file__).resolve().parents[1]
    window_path = root / "results" / "critical_case_window.jsonl"

    rows = [
        json.loads(line)
        for line in window_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert rows
    assert any(row["post_crossed_threshold"] for row in rows)

    crossing_rows = [row for row in rows if row["post_crossed_threshold"]]
    first = crossing_rows[0]

    assert first["post_partial_average"] > 1.584
    assert first["post_partial_surplus"] > 0

def test_critical_case_summary_consistency():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "critical_case_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["critical_chain_start_block"] <= summary["critical_chain_end_block"]
    assert summary["post_chain_recovery_start_block"] == summary["critical_chain_end_block"] + 1
    assert summary["first_crossing_block"] == summary["post_chain_recovery_end_block"]
    assert summary["post_chain_recovery_distance_blocks"] == summary["first_crossing_relative_to_post_start"] + 1
