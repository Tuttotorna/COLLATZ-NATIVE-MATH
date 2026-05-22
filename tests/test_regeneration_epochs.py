import json
import math
import subprocess
import sys
from pathlib import Path

def v2(n: int) -> int:
    c = 0
    n = abs(n)
    while n % 2 == 0:
        c += 1
        n //= 2
    return c

def next_odd_block(n: int):
    value = 3 * n + 1
    a = v2(value)
    m = value // (2 ** a)
    return a, m

def test_regeneration_example_2729_to_2047():
    n = 2729
    s = v2(n + 1)
    a, m = next_odd_block(n)
    s_next = v2(m + 1)

    assert a == 2
    assert m == 2047
    assert s == 1
    assert s_next == 11
    assert s_next > s

def test_escape_consumes_shadow_for_2047_prefix():
    n = 2047
    shadows = []
    debts = []

    for _ in range(10):
        s = v2(n + 1)
        a, m = next_odd_block(n)
        shadows.append(s)
        debts.append(a)
        n = m

    assert debts == [1] * 10
    assert shadows == [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

def test_analyze_regeneration_epochs_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_regeneration_epochs.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v0.2" in result.stdout
    assert "regeneration_events" in result.stdout

def test_regeneration_epoch_results_written():
    root = Path(__file__).resolve().parents[1]
    results_path = root / "results" / "regeneration_epochs_sample.jsonl"
    summary_path = root / "results" / "regeneration_epochs_summary.json"

    assert results_path.exists()
    assert summary_path.exists()

    rows = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["version"] == "v0.2"
    assert summary["all_reach_1_in_sample"] is True
