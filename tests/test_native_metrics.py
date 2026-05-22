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

def test_a_equals_one_when_shadow_at_least_two():
    for n in range(1, 5000, 2):
        s = v2(n + 1)
        a, _ = next_odd_block(n)
        if s >= 2:
            assert a == 1

def test_escape_consumes_shadow():
    for n in range(1, 5000, 2):
        s = v2(n + 1)
        a, m = next_odd_block(n)
        if a == 1 and s >= 2:
            assert v2(m + 1) == s - 1

def test_trace_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "trace_collatz_native.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH" in result.stdout
    assert "average_debt" in result.stdout

def test_scan_script_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "scan_regeneration_chains.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "Regeneration scan" in result.stdout
