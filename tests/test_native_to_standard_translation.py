import json
from pathlib import Path

def test_translation_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_TO_STANDARD_TRANSLATION_BOUNDARY.md",
        root / "docs" / "TRANSLATION_TABLE.md",
        root / "docs" / "TRANSLATION_VALIDITY_RULES.md",
        root / "docs" / "STANDARD_PROOF_PREPARATION.md",
        root / "docs" / "NATIVE_STANDARD_GLOSSARY.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.0" in text

def test_translation_manifest_exists_and_is_v20():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_to_standard_translation_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.0"
    assert data["layer"] == "native_to_standard_translation_boundary"
    assert data["status"] == "translation_boundary_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["standard_translation_status"] == "allowed_under_reversibility_rule"
    assert data["next_recommended_version"] == "v2.1 Standard Definition Candidates"

def test_translation_table_contains_core_native_objects():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_to_standard_translation_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    native_objects = {row["native_object"] for row in data["translation_table"]}

    expected = {
        "odd_block",
        "expansion",
        "discharge",
        "debt",
        "bad_window",
        "compensation",
        "shadow",
        "regeneration",
        "obstruction",
        "closure",
    }

    assert expected.issubset(native_objects)

def test_reversibility_rule_is_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_to_standard_translation_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["translation_rule"] == "Every standard statement must map back to a native object."
    assert data["reversibility_rule"] == "native_object -> standard_expression -> native_meaning_retained"

def test_forbidden_premature_claims_are_blocked():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_to_standard_translation_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_before_proof"])

    assert "theorem_proved" in forbidden
    assert "conjecture_solved" in forbidden
    assert "finite_evidence_treated_as_proof" in forbidden
    assert "hardness_treated_as_obstruction" in forbidden
    assert "reaching_1_treated_as_native_closure" in forbidden

def test_boundary_doc_preserves_native_source_layer():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_TO_STANDARD_TRANSLATION_BOUNDARY.md").read_text(encoding="utf-8")

    assert "The native method remains the source layer." in text
    assert "The standard layer is a translation layer." in text
    assert "Translation must be reversible." in text

def test_translation_validity_rules_preserve_key_distinctions():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "TRANSLATION_VALIDITY_RULES.md").read_text(encoding="utf-8")

    assert "Closure is not terminality" in text
    assert "Hardness is not obstruction" in text
    assert "Compensation is not automatically closure" in text
    assert "Evidence remains evidence" in text

def test_standard_proof_preparation_does_not_claim_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "STANDARD_PROOF_PREPARATION.md").read_text(encoding="utf-8")

    assert "without claiming one" in text
    assert "v2.0 does not claim" in text
    assert "The next step after v2.0 should be v2.1 Standard Definition Candidates." in text

def test_native_standard_glossary_has_directional_constraint():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_STANDARD_GLOSSARY.md").read_text(encoding="utf-8")

    assert "Native objects define the meaning." in text
    assert "Standard terms express the meaning." in text
    assert "The glossary is directional but reversible." in text
