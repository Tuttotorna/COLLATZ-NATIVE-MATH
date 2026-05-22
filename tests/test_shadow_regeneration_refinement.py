import json
from pathlib import Path

def test_shadow_regeneration_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "SHADOW_DEFINITION_REFINEMENT.md",
        root / "docs" / "SHADOW_ERASURE_REFINEMENT.md",
        root / "docs" / "REGENERATION_DEFINITION_REFINEMENT.md",
        root / "docs" / "BENIGN_VS_DANGEROUS_REGENERATION.md",
        root / "docs" / "OBSTRUCTION_PRESERVING_REGENERATION.md",
        root / "docs" / "SHADOW_REGENERATION_STATUS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.3" in text

def test_shadow_regeneration_manifest_exists_and_is_v23():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_regeneration_refinement_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.3"
    assert data["layer"] == "shadow_regeneration_definition_refinement"
    assert data["status"] == "shadow_and_regeneration_refined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v2.4 Native Closure Lemma Candidates"

def test_refined_definitions_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_regeneration_refinement_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    objects = {item["native_object"] for item in data["refined_definitions"]}

    required = {
        "shadow",
        "shadow_erasure",
        "regeneration",
        "benign_regeneration",
        "dangerous_regeneration",
        "obstruction_preserving_regeneration",
    }

    assert required.issubset(objects)

def test_obstruction_threshold_is_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_regeneration_refinement_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["obstruction_threshold"] == [
        "persistent_debt",
        "non_erased_shadow",
        "dangerous_regeneration",
        "insufficient_compensation",
        "no_closure_event",
        "internal_admissibility",
    ]

def test_regeneration_alone_is_not_obstruction():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_regeneration_refinement_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert "regeneration_alone" in data["not_sufficient_for_obstruction"]
    assert "repeated_bad_windows" in data["not_sufficient_for_obstruction"]
    assert "tight_positive_surplus" in data["not_sufficient_for_obstruction"]

def test_shadow_definition_refinement_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SHADOW_DEFINITION_REFINEMENT.md").read_text(encoding="utf-8")

    assert "shadow = persistence of obstruction-relevant prior debt influence" in text
    assert "Shadow must preserve relevance to prior debt." in text
    assert "Shadow erasure requires more than local recovery." in text

def test_shadow_erasure_refinement_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SHADOW_ERASURE_REFINEMENT.md").read_text(encoding="utf-8")

    assert "shadow erasure = prior debt loses obstruction-carrying power" in text
    assert "local recovery != shadow erasure" in text
    assert "Closure requires debt erasure and shadow erasure." in text

def test_regeneration_definition_refinement_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "REGENERATION_DEFINITION_REFINEMENT.md").read_text(encoding="utf-8")

    assert "debt -> compensation -> renewed debt" in text
    assert "Benign regeneration" in text
    assert "Dangerous regeneration" in text
    assert "Obstruction-preserving regeneration" in text

def test_benign_vs_dangerous_regeneration_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "BENIGN_VS_DANGEROUS_REGENERATION.md").read_text(encoding="utf-8")

    assert "regeneration != obstruction" in text
    assert "Benign regeneration supports the native closure direction." in text
    assert "Dangerous regeneration identifies where closure must be tested harder." in text

def test_obstruction_preserving_regeneration_text():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "OBSTRUCTION_PRESERVING_REGENERATION.md").read_text(encoding="utf-8")

    assert "obstruction-preserving regeneration = regeneration that keeps debt alive as obstruction" in text
    assert "failure of shadow erasure is required" in text
    assert "No such obstruction-preserving regeneration chain has been established" in text

def test_forbidden_claims_include_key_boundaries():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_regeneration_refinement_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "obstruction_preserving_regeneration_impossible" in forbidden
    assert "shadow_always_erases" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
    assert "regeneration_equals_obstruction" in forbidden
    assert "local_recovery_equals_shadow_erasure" in forbidden
