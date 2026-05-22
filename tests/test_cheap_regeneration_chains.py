import json
import math
import subprocess
import sys
from pathlib import Path

def test_chain_analysis_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_cheap_regeneration_chains.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.3" in result.stdout
    assert "cheapness threshold" in result.stdout
    assert "chain_compatible_events" in result.stdout

def test_chain_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "cheap_regeneration_chains.jsonl"
    summary_path = root / "results" / "cheap_regeneration_chain_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.3"
    assert summary["all_reach_1_in_sample"] is True
    assert summary["cheapness_threshold"] > 1.7

def test_cheapness_threshold_formula():
    threshold = 1 / (math.log2(3) - 1)
    assert 1.70 < threshold < 1.72

def test_chain_rows_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "cheap_regeneration_chains.jsonl"

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    required = {
        "n0",
        "event_block",
        "event_n",
        "regenerated_shadow",
        "compression_cost",
        "cheapness_ratio",
        "is_locally_cheap",
        "chain_compatible",
        "breaks_by_debt",
        "segment_average_debt",
    }

    for row in rows[:50]:
        assert required.issubset(row.keys())
