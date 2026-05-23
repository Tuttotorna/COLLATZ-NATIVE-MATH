import json
import subprocess
import sys
from pathlib import Path


def run_report_builder_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_obstruction_scanner_evidence_report.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v27_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "OBSTRUCTION_SCANNER_EVIDENCE_REPORT.md",
        root / "docs" / "V26_EVIDENCE_INTERPRETATION.md",
        root / "docs" / "NEAR_OBSTRUCTION_CASES.md",
        root / "docs" / "DANGEROUS_REGENERATION_EVIDENCE.md",
        root / "docs" / "EVIDENCE_REPORT_LIMITS.md",
        root / "docs" / "OBSTRUCTION_EVIDENCE_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.7" in text


def test_v27_report_outputs_exist():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "obstruction_scanner_evidence_report.json").exists()
    assert (root / "results" / "obstruction_scanner_evidence_report.md").exists()
    assert (root / "results" / "obstruction_scanner_evidence_certificate.json").exists()


def test_v27_report_certificate_fields():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_scanner_evidence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.7"
    assert data["certificate_type"] == "obstruction_scanner_evidence_certificate"
    assert data["source_version"] == "v2.6"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["evidence_status"] == "bounded_native_evidence"
    assert data["next_recommended_version"] == "v2.8 Expanded Bounded Obstruction Search"


def test_v27_negative_result_boundary_is_preserved():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_scanner_evidence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["negative_result_boundary"] == (
        "No obstruction detected in a finite domain is not the same as no obstruction can exist."
    )


def test_v27_report_has_key_case_groups():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_scanner_evidence_report.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    key_cases = data["key_cases"]

    required = {
        "hardest_by_recovery",
        "tightest_positive_surplus",
        "most_debt_windows",
        "most_regeneration",
        "most_dangerous_regeneration",
        "near_obstruction_cases",
    }

    assert required.issubset(key_cases.keys())

    for name in required:
        assert isinstance(key_cases[name], list)


def test_v27_forbidden_conclusions_are_explicit():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_scanner_evidence_report.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_conclusions"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "obstruction_impossible" in forbidden
    assert "finite_negative_result_is_proof" in forbidden
    assert "dangerous_regeneration_equals_obstruction" in forbidden
    assert "hardness_equals_obstruction" in forbidden


def test_v27_markdown_report_contains_boundary():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "obstruction_scanner_evidence_report.md").read_text(encoding="utf-8")

    assert "Version: v2.7" in text
    assert "It is not a proof." in text
    assert "No obstruction candidate was detected in the v2.6 bounded domain." in text
    assert "No obstruction can exist." in text


def test_v27_source_counts_match_v26_certificate():
    run_report_builder_once()

    root = Path(__file__).resolve().parents[1]

    v26 = json.loads(
        (root / "results" / "bounded_obstruction_search_certificate.json").read_text(encoding="utf-8")
    )
    v27 = json.loads(
        (root / "results" / "obstruction_scanner_evidence_certificate.json").read_text(encoding="utf-8")
    )

    assert v27["tested_candidate_count"] == v26["tested_candidate_count"]
    assert v27["debt_window_count"] == v26["debt_window_count"]
    assert v27["regeneration_count"] == v26["regeneration_count"]
    assert v27["dangerous_regeneration_count"] == v26["dangerous_regeneration_count"]
    assert v27["obstruction_candidate_count"] == v26["obstruction_candidate_count"]
    assert v27["obstruction_detected"] == v26["obstruction_detected"]
