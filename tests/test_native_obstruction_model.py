import json
from pathlib import Path

def test_native_obstruction_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_OBSTRUCTION_MODEL.md",
        root / "docs" / "NATIVE_FAILURE_CONDITION.md",
        root / "docs" / "NATIVE_REGENERATION.md",
        root / "docs" / "NATIVE_CLOSURE_OPPOSITE.md",
        root / "docs" / "NATIVE_HARDNESS_VS_OBSTRUCTION.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v1.7" in text

def test_native_obstruction_manifest_exists_and_is_v17():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_obstruction_model_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v1.7"
    assert data["layer"] == "native_obstruction_model"
    assert data["status"] == "obstruction_model_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["standard_translation_status"] == "deferred_until_native_closure"
    assert data["next_recommended_version"] == "v1.8 Native Closure Conditions"

def test_native_obstruction_definition_is_structural():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_obstruction_model_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    expected = [
        "debt_is_generated",
        "debt_persists",
        "shadow_is_not_erased",
        "regeneration_occurs",
        "compensation_is_insufficient",
        "no_closure_event_is_forced",
        "structure_remains_internally_admissible",
    ]

    assert data["native_obstruction_definition"] == expected

def test_hardness_is_not_obstruction():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_obstruction_model_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert "high_hardness_score" in data["not_sufficient_for_obstruction"]
    assert "high_odd_block_count" in data["not_sufficient_for_obstruction"]
    assert "tight_positive_surplus" in data["not_sufficient_for_obstruction"]
    assert data["hardness_vs_obstruction_rule"] == (
        "Hardness measures stress; obstruction requires self-preserving unclosed debt."
    )

def test_native_failure_condition_is_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_FAILURE_CONDITION.md").read_text(encoding="utf-8")

    assert "The native method fails if it cannot distinguish stress from obstruction." in text
    assert "persistent debt" in text
    assert "repeated regeneration" in text
    assert "no compensating discharge" in text

def test_native_regeneration_chain_is_defined():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_REGENERATION.md").read_text(encoding="utf-8")

    assert "debt -> compensation -> renewed debt" in text
    assert "D1 -> C1 -> D2 -> C2 -> D3 -> C3" in text
    assert "Dangerous regeneration" in text

def test_native_closure_opposite_is_defined():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_CLOSURE_OPPOSITE.md").read_text(encoding="utf-8")

    assert "A closure condition is meaningful only if its opposite is explicit." in text
    assert "persists, regenerates, and avoids compensating discharge indefinitely" in text
    assert "Closure is not reaching 1" in text

def test_hardness_vs_obstruction_metric_separation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_HARDNESS_VS_OBSTRUCTION.md").read_text(encoding="utf-8")

    assert "Hardness measures stress." in text
    assert "Obstruction is not stress." in text
    assert "n0 = 9780657630" in text
    assert "n0 = 670617279" in text
    assert "n0 = 63728127" in text
    assert "n0 = 837799" in text
