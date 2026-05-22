import json
import subprocess
import sys
from pathlib import Path


def run_scanner_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "bounded_obstruction_search_scanner.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_bounded_obstruction_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "BOUNDED_OBSTRUCTION_SEARCH_SCANNER.md",
        root / "docs" / "BOUNDED_OBSTRUCTION_SIGNATURE.md",
        root / "docs" / "BOUNDED_SEARCH_NEGATIVE_RESULT.md",
        root / "docs" / "BOUNDED_SEARCH_RESULT_TYPES.md",
        root / "docs" / "BOUNDED_OBSTRUCTION_SEARCH_LIMITS.md",
        root / "docs" / "BOUNDED_OBSTRUCTION_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.6" in text


def test_bounded_obstruction_scanner_outputs_exist():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "bounded_obstruction_search_rows.jsonl").exists()
    assert (root / "results" / "bounded_obstruction_search_summary.json").exists()
    assert (root / "results" / "bounded_obstruction_search_certificate.json").exists()


def test_bounded_obstruction_certificate_fields():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "bounded_obstruction_search_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "search_domain",
        "candidate_generation_rule",
        "tested_candidate_count",
        "debt_window_count",
        "regeneration_count",
        "dangerous_regeneration_count",
        "obstruction_candidate_count",
        "closure_result_counts",
        "proof_status",
        "negative_result_boundary",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v2.6"
    assert data["certificate_type"] == "bounded_obstruction_search_certificate"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["minimum_report_fields_present"] is True
    assert data["next_recommended_version"] == "v2.7 Obstruction Scanner Evidence Report"


def test_negative_result_boundary_is_explicit():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "bounded_obstruction_search_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["negative_result_boundary"] == (
        "No obstruction detected in a finite domain is not the same as no obstruction can exist."
    )


def test_rows_are_jsonl_and_have_native_fields():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "bounded_obstruction_search_rows.jsonl"

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert rows

    required = {
        "version",
        "n0",
        "odd_blocks",
        "debt_window_count",
        "recovered_debt_window_count",
        "unrecovered_debt_window_count",
        "regeneration_count",
        "dangerous_regeneration_count",
        "obstruction_candidate_count",
        "closure_result_type",
    }

    for row in rows:
        assert required.issubset(row.keys())
        assert row["version"] == "v2.6"


def test_search_result_types_are_valid():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "bounded_obstruction_search_rows.jsonl"

    valid = {
        "NO_DEBT_DETECTED",
        "DEBT_LOCALLY_RECOVERED",
        "REGENERATED_BUT_COMPENSATED",
        "DANGEROUS_REGENERATION_DETECTED",
        "OBSTRUCTION_CANDIDATE_DETECTED",
        "CLOSED",
        "UNDECIDED",
    }

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    for row in rows:
        assert row["closure_result_type"] in valid


def test_known_anchor_is_included():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "bounded_obstruction_search_rows.jsonl"

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    n0_values = {row["n0"] for row in rows}

    assert 837799 in n0_values
    assert 63728127 in n0_values
    assert 670617279 in n0_values
    assert 9780657630 in n0_values


def test_summary_is_consistent_with_rows():
    run_scanner_once()

    root = Path(__file__).resolve().parents[1]

    rows = [
        json.loads(line)
        for line in (root / "results" / "bounded_obstruction_search_rows.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]

    summary = json.loads(
        (root / "results" / "bounded_obstruction_search_summary.json")
        .read_text(encoding="utf-8")
    )

    assert summary["version"] == "v2.6"
    assert summary["tested_candidate_count"] == len(rows)
    assert summary["debt_window_count"] == sum(row["debt_window_count"] for row in rows)
    assert summary["regeneration_count"] == sum(row["regeneration_count"] for row in rows)
    assert summary["dangerous_regeneration_count"] == sum(
        row["dangerous_regeneration_count"] for row in rows
    )
    assert summary["obstruction_candidate_count"] == sum(
        row["obstruction_candidate_count"] for row in rows
    )


def test_docs_forbid_proof_claims():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "BOUNDED_SEARCH_NEGATIVE_RESULT.md").read_text(encoding="utf-8")

    assert "Collatz is proved." in text
    assert "Global closure is proved." in text
    assert "Finite evidence implies theorem." in text
    assert "v2.6 does not do that." in text
