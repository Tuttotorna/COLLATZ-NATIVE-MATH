import json
from pathlib import Path

def test_lemma_candidate_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "LOCAL_DEBT_LEMMA_CANDIDATES.md",
        root / "docs" / "BAD_WINDOW_LEMMA_CANDIDATES.md",
        root / "docs" / "COMPENSATION_LEMMA_CANDIDATES.md",
        root / "docs" / "SURPLUS_LEMMA_CANDIDATES.md",
        root / "docs" / "HARDNESS_OBSTRUCTION_LEMMA_CANDIDATES.md",
        root / "docs" / "LEMMA_CANDIDATE_STATUS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.2" in text

def test_lemma_candidate_manifest_exists_and_is_v22():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "local_debt_lemma_candidates_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.2"
    assert data["layer"] == "local_debt_lemma_candidates"
    assert data["status"] == "lemma_candidates_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["standard_translation_status"] == "lemma_candidates_only"
    assert data["next_recommended_version"] == "v2.3 Shadow and Regeneration Definition Refinement"

def test_reversibility_rule_is_v22():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "local_debt_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["reversibility_rule"] == (
        "native_object -> standard_definition -> lemma_candidate -> native_meaning_retained"
    )

    for item in data["lemma_candidates"]:
        assert item["lemma_id"]
        assert item["native_object"]
        assert item["candidate_statement"]
        assert item["native_meaning_retained"]
        assert item["status"] in {"stable_candidate", "boundary_candidate", "open_candidate"}

def test_core_lemma_candidates_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "local_debt_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    lemma_ids = {item["lemma_id"] for item in data["lemma_candidates"]}

    required = {
        "odd_block_decomposition",
        "discharge_exponent_uniqueness",
        "local_debt_formation",
        "cumulative_debt_interval",
        "bad_window_equivalence",
        "compensation_recovery",
        "positive_surplus",
        "local_recovery_not_native_closure",
        "hardness_not_obstruction",
        "tight_surplus_not_obstruction",
        "obstruction_requires_persistence",
    }

    assert required.issubset(lemma_ids)

def test_candidate_counts_are_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "local_debt_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["stable_candidate_count"] == 7
    assert data["boundary_candidate_count"] == 3
    assert data["open_candidate_count"] == 1

def test_no_forbidden_claims_are_allowed_in_v22():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "local_debt_lemma_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "lemma_candidate_treated_as_theorem" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
    assert "hardness_implies_obstruction" in forbidden
    assert "local_recovery_equals_native_closure" in forbidden
    assert "positive_surplus_equals_full_closure" in forbidden
    assert "reaching_1_equals_native_closure" in forbidden

def test_local_debt_is_not_obstruction_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "LOCAL_DEBT_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "local debt is not obstruction" in text.lower()
    assert "debt is local danger, not global failure" in text
    assert "obstruction requires persistence, not isolated stress" in text

def test_bad_window_equivalence_is_defined():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "BAD_WINDOW_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "bad window equivalence" in text.lower()
    assert "D(I) > 0" in text
    assert "local obstruction candidate" in text

def test_compensation_recovery_is_not_closure():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "COMPENSATION_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "local recovery is not full closure" in text.lower()
    assert "Local recovery alone does not imply native closure." in text
    assert "Compensation is not fully sufficient until the prior debt shadow is tested." in text

def test_surplus_is_not_full_closure():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SURPLUS_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "Positive surplus is necessary for local recovery" in text
    assert "it is not sufficient for full native closure" in text
    assert "tight positive surplus identifies structural stress, but not obstruction" in text

def test_hardness_obstruction_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "HARDNESS_OBSTRUCTION_LEMMA_CANDIDATES.md").read_text(encoding="utf-8")

    assert "Hardness measures stress." in text
    assert "High hardness is not sufficient to identify obstruction." in text
    assert "duration is not persistence of unclosed debt" in text
    assert "obstruction is persistent unclosed debt" in text

def test_lemma_candidate_status_is_not_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "LEMMA_CANDIDATE_STATUS.md").read_text(encoding="utf-8")

    assert "Stable lemma candidates" in text
    assert "Boundary lemma candidates" in text
    assert "Open lemma candidates" in text
    assert "No proof claim is made." in text
    assert "v2.2 introduces lemma candidates only." in text
