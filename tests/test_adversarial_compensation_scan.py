import json
import subprocess
import sys
from pathlib import Path

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

def test_adversarial_compensation_scan_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "adversarial_compensation_scan.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.4" in result.stdout
    assert "Adversarial compensation scan" in result.stdout
    assert "counterexample candidates found:" in result.stdout

def test_adversarial_compensation_results_exist_and_are_consistent():
    root = Path(__file__).resolve().parents[1]

    rows_path = root / "results" / "adversarial_compensation_rows.jsonl"
    summary_path = root / "results" / "adversarial_compensation_summary.json"
    certificate_path = root / "results" / "adversarial_compensation_certificate.json"

    assert rows_path.exists()
    assert summary_path.exists()
    assert certificate_path.exists()

    rows = load_jsonl(rows_path)
    summary = load_json(summary_path)
    certificate = load_json(certificate_path)

    assert rows
    assert summary["version"] == "v1.4"
    assert certificate["version"] == "v1.4"
    assert certificate["certificate_type"] == "adversarial_compensation_certificate"

    assert summary["generated_candidate_count"] == len(rows)
    assert summary["total_bad_windows"] == sum(row["bad_windows"] for row in rows)
    assert summary["total_recovered_bad_windows"] == sum(row["recovered_bad_windows"] for row in rows)
    assert summary["total_unrecovered_bad_windows"] == sum(row["unrecovered_bad_windows"] for row in rows)
    assert summary["all_bad_windows_recovered"] == (summary["total_unrecovered_bad_windows"] == 0)

    assert certificate["generated_candidate_count"] == summary["generated_candidate_count"]
    assert certificate["total_bad_windows"] == summary["total_bad_windows"]
    assert certificate["total_recovered_bad_windows"] == summary["total_recovered_bad_windows"]
    assert certificate["total_unrecovered_bad_windows"] == summary["total_unrecovered_bad_windows"]
    assert certificate["all_bad_windows_recovered"] == summary["all_bad_windows_recovered"]

def test_known_hard_cases_are_scanned():
    root = Path(__file__).resolve().parents[1]
    rows_path = root / "results" / "adversarial_compensation_rows.jsonl"
    rows = load_jsonl(rows_path)

    observed = {row["n0"] for row in rows}

    assert 670617279 in observed
    assert 9780657630 in observed

def test_no_unrecovered_bad_windows_in_current_finite_scan():
    root = Path(__file__).resolve().parents[1]
    summary_path = root / "results" / "adversarial_compensation_summary.json"
    certificate_path = root / "results" / "adversarial_compensation_certificate.json"

    summary = load_json(summary_path)
    certificate = load_json(certificate_path)

    assert summary["total_unrecovered_bad_windows"] == 0
    assert summary["all_bad_windows_recovered"] is True
    assert summary["counterexample_candidate_count"] == 0
    assert summary["counterexample_candidates"] == []

    assert certificate["total_unrecovered_bad_windows"] == 0
    assert certificate["all_bad_windows_recovered"] is True
    assert certificate["counterexample_candidate_count"] == 0
    assert certificate["counterexample_candidates"] == []
    assert certificate["not_a_collatz_proof"] is True
    assert certificate["finite_domain_only"] is True
