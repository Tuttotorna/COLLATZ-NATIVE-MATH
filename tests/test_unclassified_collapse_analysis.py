import json
import subprocess
import sys
from pathlib import Path

def test_unclassified_collapse_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_unclassified_collapses.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.6" in result.stdout
    assert "refined taxonomy" in result.stdout
    assert "resolved unclassified" in result.stdout

def test_unclassified_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "unclassified_collapse_analysis.jsonl"
    summary_path = root / "results" / "unclassified_collapse_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.6"
    assert summary["total_episodes"] >= 1
    assert "v05_unclassified_count" in summary
    assert "v06_unclassified_count" in summary
    assert "resolved_unclassified_count" in summary

def test_refined_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "unclassified_collapse_analysis.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    required = {
        "n0",
        "v05_primary_cause",
        "v06_primary_cause",
        "v05_cause_flags",
        "v06_cause_flags",
        "was_v05_unclassified",
        "still_v06_unclassified",
        "chain_length_segments",
        "trajectory_average_debt",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())
        assert isinstance(row["v06_cause_flags"], dict)

def test_v06_does_not_increase_unclassified_count():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "unclassified_collapse_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["v06_unclassified_count"] <= summary["v05_unclassified_count"]
