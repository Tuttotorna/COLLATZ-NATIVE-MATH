import json
from pathlib import Path

def test_native_method_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_METHOD.md",
        root / "docs" / "STANDARD_TRANSLATION_BOUNDARY.md",
        root / "docs" / "NATIVE_OBJECTS.md",
        root / "docs" / "NATIVE_RESEARCH_PROGRAM.md",
        root / "docs" / "EVIDENCE_LAYER_STATUS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v1.6" in text

def test_native_method_boundary_manifest():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_method_boundary_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v1.6"
    assert data["layer"] == "native_method_boundary"
    assert data["proof_status"] == "not_a_proof"
    assert data["evidence_layer_status"] == "finite_deterministic_evidence"
    assert data["next_recommended_version"] == "v1.7 Native Obstruction Model"

def test_native_sequence_order():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_method_boundary_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["native_sequence"] == [
        "native_primitives",
        "native_dynamics",
        "native_obstruction_question",
        "native_closure_criterion",
        "computational_evidence",
        "standard_mathematical_translation",
    ]

def test_standard_translation_boundary_is_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "STANDARD_TRANSLATION_BOUNDARY.md").read_text(encoding="utf-8")

    assert "The standard layer is a translation layer, not the source layer." in text
    assert "The standard layer is necessary." in text
    assert "But it comes later." in text

def test_native_objects_include_obstruction_and_closure():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_OBJECTS.md").read_text(encoding="utf-8")

    assert "Obstruction candidate" in text
    assert "Native closure" in text
    assert "debt persists without adequate compensating discharge" in text

def test_evidence_layer_not_claimed_as_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "EVIDENCE_LAYER_STATUS.md").read_text(encoding="utf-8")

    assert "They do not prove the Collatz conjecture." in text
    assert "finite deterministic behavior" in text
