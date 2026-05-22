import json
from pathlib import Path

def test_native_closure_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_CLOSURE_CONDITIONS.md",
        root / "docs" / "NATIVE_CLOSURE_TEST.md",
        root / "docs" / "NATIVE_DEBT_ERASURE.md",
        root / "docs" / "NATIVE_SHADOW_ERASURE.md",
        root / "docs" / "NATIVE_COMPENSATION_SUFFICIENCY.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v1.8" in text

def test_native_closure_manifest_exists_and_is_v18():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_conditions_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v1.8"
    assert data["layer"] == "native_closure_conditions"
    assert data["status"] == "closure_conditions_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["next_recommended_version"] == "v1.9 Native Evidence Mapping"

def test_native_closure_definition_is_structural():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_conditions_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    expected = [
        "debt_was_generated",
        "debt_shadow_was_carried",
        "compensation_appeared",
        "compensation_was_sufficient",
        "shadow_was_erased",
        "regeneration_was_tested",
        "regeneration_did_not_preserve_obstruction",
        "no_self_preserving_debt_structure_remained",
    ]

    assert data["native_closure_definition"] == expected

def test_closure_is_not_terminality():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_CLOSURE_CONDITIONS.md").read_text(encoding="utf-8")

    assert "Native closure is not reaching 1." in text
    assert "Native closure = obstruction potential erased." in text
    assert "The terminal state is a classical endpoint." in text

def test_closure_test_result_types():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_closure_conditions_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    expected = [
        "CLOSED",
        "LOCALLY_RECOVERED_NOT_CLOSED",
        "REGENERATED_BUT_COMPENSATED",
        "OBSTRUCTION_CANDIDATE",
        "UNDECIDED",
    ]

    assert data["closure_result_types"] == expected

def test_debt_erasure_distinguishes_local_and_structural_erasure():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_DEBT_ERASURE.md").read_text(encoding="utf-8")

    assert "Local erasure" in text
    assert "Structural erasure" in text
    assert "Local erasure is evidence." in text
    assert "It is not full closure." in text

def test_shadow_erasure_is_defined():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_SHADOW_ERASURE.md").read_text(encoding="utf-8")

    assert "Shadow erasure occurs" in text
    assert "future obstruction" in text
    assert "The native method studies closure before terminality." in text

def test_compensation_sufficiency_is_not_local_recovery():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_COMPENSATION_SUFFICIENCY.md").read_text(encoding="utf-8")

    assert "Compensation is not sufficient merely because" in text
    assert "recovery is not automatically closure" in text
    assert "recovery + positive surplus + shadow erasure + failed obstruction regeneration" in text
