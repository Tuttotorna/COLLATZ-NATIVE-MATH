import json
from pathlib import Path

def test_obstruction_search_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "OBSTRUCTION_SEARCH_PROTOCOL.md",
        root / "docs" / "OBSTRUCTION_CANDIDATE_SIGNATURE.md",
        root / "docs" / "NEGATIVE_SEARCH_RESULT_BOUNDARY.md",
        root / "docs" / "OBSTRUCTION_SEARCH_RESULT_TYPES.md",
        root / "docs" / "OBSTRUCTION_SEARCH_MINIMUM_REPORT.md",
        root / "docs" / "OBSTRUCTION_SEARCH_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.5" in text

def test_obstruction_search_manifest_exists_and_is_v25():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_search_protocol_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.5"
    assert data["layer"] == "obstruction_search_protocol"
    assert data["status"] == "protocol_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v2.6 Bounded Obstruction Search Scanner"

def test_obstruction_signature_requires_all_six_components():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_search_protocol_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["obstruction_signature"] == [
        "persistent_debt",
        "non_erased_shadow",
        "dangerous_regeneration",
        "insufficient_compensation",
        "no_closure_event",
        "internal_admissibility",
    ]

def test_search_result_types_are_defined():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_search_protocol_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["search_result_types"] == [
        "NO_DEBT_DETECTED",
        "DEBT_LOCALLY_RECOVERED",
        "REGENERATED_BUT_COMPENSATED",
        "DANGEROUS_REGENERATION_DETECTED",
        "OBSTRUCTION_CANDIDATE_DETECTED",
        "CLOSED",
        "UNDECIDED",
    ]

def test_negative_result_boundary_is_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NEGATIVE_SEARCH_RESULT_BOUNDARY.md").read_text(encoding="utf-8")

    assert "No obstruction detected in a finite domain is not the same as no obstruction can exist." in text
    assert "A negative finite result does not mean:" in text
    assert "global closure is proved" in text
    assert "finite evidence implies proof" in text

def test_search_protocol_targets_obstruction_preserving_regeneration():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OBSTRUCTION_SEARCH_PROTOCOL.md").read_text(encoding="utf-8")

    assert "The search target is not a long trajectory." in text
    assert "obstruction-preserving regeneration" in text
    assert "How would we detect obstruction-preserving regeneration if it existed?" in text

def test_obstruction_candidate_signature_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OBSTRUCTION_CANDIDATE_SIGNATURE.md").read_text(encoding="utf-8")

    assert "All six are required." in text
    assert "Local recovery is not enough." in text
    assert "A candidate is not an obstruction candidate unless all six signature components are present together." in text

def test_minimum_report_fields_are_required():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_search_protocol_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    required = {
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
    }

    assert required.issubset(set(data["minimum_report_fields"]))

def test_result_types_boundary_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OBSTRUCTION_SEARCH_RESULT_TYPES.md").read_text(encoding="utf-8")

    assert "Only OBSTRUCTION_CANDIDATE_DETECTED is a native obstruction candidate result." in text
    assert "DANGEROUS_REGENERATION_DETECTED is a warning result, not a proof of obstruction." in text

def test_next_steps_are_scanner_not_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OBSTRUCTION_SEARCH_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v2.6 Bounded Obstruction Search Scanner" in text
    assert "Not a theorem." in text
    assert "Not a proof." in text
    assert "Not a global closure claim." in text

def test_forbidden_claims_include_proof_boundaries():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "obstruction_search_protocol_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "obstruction_preserving_regeneration_impossible" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
    assert "hard_case_equals_obstruction" in forbidden
    assert "local_recovery_equals_native_closure" in forbidden
