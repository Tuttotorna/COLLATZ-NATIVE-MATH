import json
from pathlib import Path


def test_v28_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "EXPANDED_BOUNDED_OBSTRUCTION_SEARCH.md",
        root / "docs" / "TARGETED_EXPANSION_STRATEGY.md",
        root / "docs" / "EXPANDED_SEARCH_RESULT_TYPES.md",
        root / "docs" / "V28_NEGATIVE_RESULT_BOUNDARY.md",
        root / "docs" / "V28_EVIDENCE_STATUS.md",
        root / "docs" / "V28_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.8" in text


def test_v28_script_exists():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "expanded_bounded_obstruction_search.py"

    assert script.exists()
    text = script.read_text(encoding="utf-8")

    assert "VERSION = \"v2.8\"" in text
    assert "Expanded Bounded Obstruction Search" in text
    assert "not_a_proof" in text


def test_v28_artifacts_exist():
    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "expanded_bounded_obstruction_search_rows.jsonl").exists()
    assert (root / "results" / "expanded_bounded_obstruction_search_summary.json").exists()
    assert (root / "results" / "expanded_bounded_obstruction_search_certificate.json").exists()


def test_v28_certificate_fields():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "expanded_bounded_obstruction_search_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_version",
        "expansion_strategy",
        "search_domain",
        "tested_candidate_count",
        "debt_window_count",
        "regeneration_count",
        "dangerous_regeneration_count",
        "obstruction_candidate_count",
        "obstruction_detected",
        "native_interpretation",
        "closure_result_counts",
        "proof_status",
        "theorem_status",
        "negative_result_boundary",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v2.8"
    assert data["certificate_type"] == "expanded_bounded_obstruction_search_certificate"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v2.9 Shadow Persistence Instrumentation"


def test_v28_negative_result_boundary():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "expanded_bounded_obstruction_search_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["negative_result_boundary"] == (
        "No obstruction detected in a finite expanded bounded domain is not the same as no obstruction can exist."
    )


def test_v28_rows_are_valid_jsonl():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "expanded_bounded_obstruction_search_rows.jsonl"

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert rows

    required = {
        "version",
        "source_version",
        "n0",
        "odd_blocks",
        "debt_window_count",
        "recovered_debt_window_count",
        "unrecovered_debt_window_count",
        "regeneration_count",
        "dangerous_regeneration_count",
        "obstruction_candidate_count",
        "closure_result_type",
        "hardest_recovery_score",
    }

    valid_result_types = {
        "NO_DEBT_DETECTED",
        "DEBT_LOCALLY_RECOVERED",
        "REGENERATED_BUT_COMPENSATED",
        "DANGEROUS_REGENERATION_DETECTED",
        "OBSTRUCTION_CANDIDATE_DETECTED",
        "UNDECIDED",
    }

    for row in rows:
        assert required.issubset(row.keys())
        assert row["version"] == "v2.8"
        assert row["closure_result_type"] in valid_result_types


def test_v28_summary_consistent_with_rows():
    root = Path(__file__).resolve().parents[1]

    rows = [
        json.loads(line)
        for line in (root / "results" / "expanded_bounded_obstruction_search_rows.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]

    summary = json.loads(
        (root / "results" / "expanded_bounded_obstruction_search_summary.json")
        .read_text(encoding="utf-8")
    )

    assert summary["version"] == "v2.8"
    assert summary["tested_candidate_count"] == len(rows)
    assert summary["debt_window_count"] == sum(row["debt_window_count"] for row in rows)
    assert summary["regeneration_count"] == sum(row["regeneration_count"] for row in rows)
    assert summary["dangerous_regeneration_count"] == sum(
        row["dangerous_regeneration_count"] for row in rows
    )
    assert summary["obstruction_candidate_count"] == sum(
        row["obstruction_candidate_count"] for row in rows
    )


def test_v28_is_targeted_not_blind_bruteforce():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "TARGETED_EXPANSION_STRATEGY.md").read_text(encoding="utf-8")

    assert "Blind brute force answers the wrong question." in text
    assert "It is looking for obstruction structure." in text
    assert "Targeted expansion is still finite." in text


def test_v28_next_step_is_shadow_instrumentation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V28_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v2.9 Shadow Persistence Instrumentation" in text
    assert "The next real weakness is not candidate size." in text
    assert "The next weakness is shadow measurement." in text
