import json
from pathlib import Path

def test_standard_definition_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "STANDARD_DEFINITION_CANDIDATES.md",
        root / "docs" / "STANDARD_DEFINITION_REVERSIBILITY.md",
        root / "docs" / "STANDARD_DEFINITION_TABLE.md",
        root / "docs" / "DEFINITION_STATUS.md",
        root / "docs" / "NEXT_STANDARDIZATION_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.1" in text

def test_standard_definition_manifest_exists_and_is_v21():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "standard_definition_candidates_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v2.1"
    assert data["layer"] == "standard_definition_candidates"
    assert data["status"] == "definition_candidates_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["standard_translation_status"] == "definition_candidates_only"
    assert data["next_recommended_version"] == "v2.2 Local Debt Lemma Candidates"

def test_reversibility_rule_is_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "standard_definition_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["reversibility_rule"] == (
        "native_object -> standard_definition_candidate -> native_meaning_retained"
    )

    for item in data["definition_candidates"]:
        assert item["native_object"]
        assert item["standard_definition_candidate"]
        assert item["native_meaning_retained"]
        assert item["status"] in {"stable_candidate", "open_candidate"}

def test_core_stable_definitions_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "standard_definition_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    native_objects = {item["native_object"] for item in data["definition_candidates"]}

    required = {
        "odd_block",
        "discharge_exponent",
        "expansion_pressure",
        "local_debt",
        "cumulative_debt",
        "bad_window",
        "compensation",
        "surplus",
    }

    assert required.issubset(native_objects)

def test_open_definitions_are_marked_open():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "standard_definition_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    statuses = {item["native_object"]: item["status"] for item in data["definition_candidates"]}

    assert statuses["shadow"] == "open_candidate"
    assert statuses["regeneration"] == "open_candidate"
    assert statuses["obstruction_candidate"] == "open_candidate"
    assert statuses["closure_candidate"] == "open_candidate"

def test_no_forbidden_claims_are_allowed():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "standard_definition_candidates_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_claims"])

    assert "collatz_solved" in forbidden
    assert "global_closure_proved" in forbidden
    assert "finite_evidence_implies_proof" in forbidden
    assert "hardness_implies_obstruction" in forbidden
    assert "local_recovery_equals_native_closure" in forbidden
    assert "reaching_1_equals_native_closure" in forbidden

def test_definition_status_separates_stable_and_open():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "DEFINITION_STATUS.md").read_text(encoding="utf-8")

    assert "Stable candidate definitions" in text
    assert "Open candidate definitions" in text
    assert "No proof claim is made." in text

def test_next_steps_are_lemma_candidates_not_theorems():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NEXT_STANDARDIZATION_STEPS.md").read_text(encoding="utf-8")

    assert "v2.2 Local Debt Lemma Candidates" in text
    assert "Not proof." in text
    assert "Not theorem." in text
    assert "Definitions first." in text
