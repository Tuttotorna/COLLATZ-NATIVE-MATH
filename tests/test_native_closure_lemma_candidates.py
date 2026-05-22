import json
from pathlib import Path

def test_native_closure_lemma_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_CLOSURE_LEMMA_CANDIDATES.md",
        root / "docs" / "DEBT_ERASURE_LEMMA_CANDIDATES.md",
        root / "docs" / "SHADOW_ERASURE_LEMMA_CANDIDATES.md",
        root / "docs" / "REGENERATION_LEMMA_CANDIDATES.md",
        root / "docs" / "CLOSURE_RESULT_TYPES.md",
        root / "docs" / "NATIVE_CLOSURE_LEMMA_STATUS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.4" in text

def test_native_closure_lemma_manifest_exists_and_is_v24():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.4"
    assert data["layer"] == "native_closure_lemma_candidates"
    assert data["status"] == "closure_lemma_candidates_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v2.5 Obstruction Search Protocol"

def test_closure_result_types_are_defined():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["closure_result_types"] == [
        "CLOSED",
        "LOCALLY_RECOVERED_NOT_CLOSED",
        "REGENERATED_BUT_COMPENSATED",
        "DANGEROUS_REGENERATION",
        "OBSTRUCTION_CANDIDATE",
        "UNDECIDED",
    ]

def test_closure_requirements_are_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["closure_requirements"] == [
        "debt_detected",
        "compensation_sufficient",
        "shadow_erased",
        "regeneration_tested",
        "no_self_preserving_debt_remains",
    ]

def test_obstruction_candidate_requirements_are_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["obstruction_candidate_requirements"] == [
        "persistent_debt",
        "non_erased_shadow",
        "dangerous_regeneration",
        "insufficient_compensation",
        "no_closure_event",
        "internal_admissibility",
    ]

def test_lemma_candidates_have_reversible_native_meaning():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for item in data["lemma_candidates"]:
        assert item["lemma_id"]
        assert item["candidate_statement"]
        assert item["native_object"]
        assert item["native_meaning_retained"]
        assert item["status"] in {"stable_boundary_candidate", "open_candidate"}

def test_local_recovery_not_closure_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_CLOSURE_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "Native closure is not reaching 1." in text
    assert "local recovery does not equal obstruction erasure" in text
    assert "No proof of the Collatz conjecture is claimed." in text

def test_debt_erasure_boundary_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "DEBT_ERASURE_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "local recovery != debt erasure" in text
    assert "Debt erasure is stronger than local recovery." in text
    assert "debt loses obstruction power" in text

def test_shadow_erasure_boundary_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SHADOW_ERASURE_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "Native closure requires shadow erasure." in text
    assert "local recovery is not shadow erasure" in text
    assert "v2.4 does not prove that shadow always erases" in text

def test_regeneration_boundary_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "REGENERATION_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "regeneration != obstruction" in text
    assert "obstruction requires obstruction-preserving regeneration" in text
    assert "The existence of a renewed bad window after compensation does not by itself imply native obstruction." in text

def test_closure_result_type_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "CLOSURE_RESULT_TYPES.md").read_text(encoding="utf-8")

    assert "Only CLOSED means native closure." in text
    assert "OBSTRUCTION_CANDIDATE" in text
    assert "DANGEROUS_REGENERATION" in text
    assert "UNDECIDED" in text

def test_forbidden_claims_include_no_proof_boundaries():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "closure_lemma_candidate_treated_as_theorem" in forbidden
    assert "obstruction_preserving_regeneration_impossible" in forbidden
    assert "shadow_always_erases" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
