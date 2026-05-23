import json
from pathlib import Path


def test_formal_lemma_draft_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "FORMAL_NATIVE_STANDARD_LEMMA_DRAFT.md",
        root / "docs" / "LEMMA_DRAFT_BOUNDARY.md",
        root / "docs" / "LOCAL_DEBT_FORMALIZATION.md",
        root / "docs" / "COMPENSATION_FORMALIZATION.md",
        root / "docs" / "SHADOW_REGENERATION_FORMALIZATION.md",
        root / "docs" / "NON_OBSTRUCTION_LEMMA_DRAFTS.md",
        root / "docs" / "FORMAL_PROOF_OBLIGATIONS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.0" in text


def test_formal_lemma_manifest_exists_and_is_v30():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v3.0"
    assert data["layer"] == "formal_native_to_standard_lemma_draft"
    assert data["status"] == "formal_lemma_drafts_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v3.1 Proof Obligation Tracker"


def test_bridge_statement_is_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    expected = (
        "Persistent shadow signal does not imply obstruction unless compensation fails "
        "and obstruction potential remains self-preserving."
    )

    assert data["central_bridge_statement"] == expected

    text = (root / "docs" / "FORMAL_NATIVE_STANDARD_LEMMA_DRAFT.md").read_text(
        encoding="utf-8"
    )
    assert expected in text


def test_reversibility_rule_is_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["reversibility_rule"] == (
        "native_object -> standard_expression -> formal_lemma_draft -> native_meaning_retained"
    )

    for item in data["lemma_drafts"]:
        assert item["lemma_id"]
        assert item["native_object"]
        assert item["draft_statement"]
        assert item["native_meaning_retained"]
        assert item["status"] in {
            "stable_draft",
            "stable_boundary_draft",
            "open_draft",
        }


def test_core_lemma_drafts_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    lemma_ids = {item["lemma_id"] for item in data["lemma_drafts"]}

    required = {
        "L1_odd_block_decomposition",
        "L2_discharge_exponent_uniqueness",
        "L3_local_debt_formation",
        "L4_cumulative_debt_interval",
        "C1_bad_window_equivalence",
        "C2_compensation_recovery",
        "C3_positive_surplus",
        "C4_local_recovery_not_closure",
        "S2_shadow_signal_not_obstruction",
        "R2_regeneration_not_obstruction",
        "N5_obstruction_candidate_requirements",
    }

    assert required.issubset(lemma_ids)


def test_no_forbidden_claims_are_allowed():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "obstruction_impossible" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
    assert "lemma_draft_treated_as_theorem" in forbidden


def test_proof_obligations_are_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "formal_lemma_draft_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    obligations = set(data["proof_obligations"])

    assert "shadow_erasure_criterion" in obligations
    assert "regeneration_closure_criterion" in obligations
    assert "obstruction_impossibility" in obligations
    assert "finite_to_general_transition" in obligations
    assert "native_closure_theorem" in obligations

    text = (root / "docs" / "FORMAL_PROOF_OBLIGATIONS.md").read_text(
        encoding="utf-8"
    )
    assert "Until these obligations are satisfied, there is no proof." in text


def test_shadow_and_regeneration_boundaries_are_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SHADOW_REGENERATION_FORMALIZATION.md").read_text(
        encoding="utf-8"
    )

    assert "shadow signal != obstruction" in text
    assert "regeneration != obstruction" in text
    assert "obstruction requires self-preserving unclosed debt" in text


def test_non_obstruction_boundaries_are_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NON_OBSTRUCTION_LEMMA_DRAFTS.md").read_text(
        encoding="utf-8"
    )

    assert "High hardness does not imply native obstruction." in text
    assert "Tight positive surplus identifies structural stress but not obstruction." in text
    assert "No obstruction detected in a finite bounded domain is not proof" in text
