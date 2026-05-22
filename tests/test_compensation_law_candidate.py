import json
import subprocess
import sys
from pathlib import Path


def test_compensation_law_candidate_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "analyze_compensation_law_candidate.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.3" in result.stdout
    assert "Compensation law candidate finite scan" in result.stdout
    assert "all bad windows recovered:" in result.stdout


def test_compensation_law_candidate_outputs_exist():
    root = Path(__file__).resolve().parents[1]

    rows_path = root / "results" / "compensation_law_candidate_rows.jsonl"
    summary_path = root / "results" / "compensation_law_candidate_summary.json"
    certificate_path = root / "results" / "compensation_law_candidate_certificate.json"

    assert rows_path.exists()
    assert summary_path.exists()
    assert certificate_path.exists()

    rows = [
        json.loads(line)
        for line in rows_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))

    assert rows
    assert summary["version"] == "v1.3"
    assert certificate["version"] == "v1.3"
    assert certificate["certificate_type"] == "finite_compensation_law_candidate_certificate"

    assert summary["candidate_count"] == len(rows)
    assert summary["total_bad_windows"] >= 0
    assert summary["total_recovered_bad_windows"] >= 0
    assert summary["total_unrecovered_bad_windows"] >= 0

    assert (
        summary["total_bad_windows"]
        == summary["total_recovered_bad_windows"] + summary["total_unrecovered_bad_windows"]
    )

    assert certificate["total_bad_windows"] == summary["total_bad_windows"]
    assert certificate["total_recovered_bad_windows"] == summary["total_recovered_bad_windows"]
    assert certificate["total_unrecovered_bad_windows"] == summary["total_unrecovered_bad_windows"]


def test_known_critical_case_is_present():
    root = Path(__file__).resolve().parents[1]

    rows_path = root / "results" / "compensation_law_candidate_rows.jsonl"

    rows = [
        json.loads(line)
        for line in rows_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    critical = [row for row in rows if row["n0"] == 9780657630]
    assert critical

    row = critical[0]
    assert row["reaches_1"] is True
    assert row["odd_blocks"] == 425
    assert row["trajectory_average_debt"] > 0
    assert row["all_bad_windows_recovered"] is True
