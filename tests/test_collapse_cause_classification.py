import json
import subprocess
import sys
from pathlib import Path

def test_collapse_cause_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_collapse_causes.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.5" in result.stdout
    assert "Classifying collapse causes" in result.stdout
    assert "Global primary cause counts" in result.stdout

def test_collapse_cause_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "collapse_cause_classification.jsonl"
    summary_path = root / "results" / "collapse_cause_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.5"
    assert summary["total_classified_episodes"] >= 1
    assert isinstance(summary["primary_cause_counts"], dict)

def test_classified_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "collapse_cause_classification.jsonl"

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
        "cause_flags",
        "primary_cause",
        "post_chain_average_debt",
        "compensation_surplus",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())
        assert isinstance(row["cause_flags"], dict)
        assert isinstance(row["primary_cause"], str)

def test_known_cause_keys_exist():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "collapse_cause_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    known = {
        "debt_spike",
        "shadow_exhaustion",
        "failed_regeneration",
        "post_chain_overcompensation",
        "terminal_descent",
    }

    assert set(summary["flag_counts"].keys()).issubset(known)
