import json
from pathlib import Path

def test_native_language_inversion_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_LANGUAGE_INVERSION.md",
        root / "docs" / "NO_SOLVING_POSTURE.md",
        root / "docs" / "COLLATZ_AS_NATIVE_LANGUAGE.md",
        root / "docs" / "TERMINATION_AS_TRANSLATION.md",
        root / "docs" / "LEARNING_COLLATZ_GRAMMAR.md",
        root / "docs" / "ROUTE_CORRECTION_FROM_V30.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.1" in text

def test_native_language_inversion_manifest_exists_and_is_v31():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v3.1"
    assert data["layer"] == "native_language_inversion"
    assert data["status"] == "route_correction_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v3.2 Native Grammar Map"

def test_mother_rule_is_native_language_before_solution():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["mother_rule"] == "No solution before native language."
    assert data["secondary_rule"] == "No proof before native description."
    assert data["central_native_question"] == "What is Collatz before it becomes a conjecture?"
    assert data["deeper_native_question"] == "What kind of debt can survive its own discharge?"

def test_forbidden_starting_posture_is_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_starting_posture"])

    assert "solve_first" in forbidden
    assert "prove_first" in forbidden
    assert "termination_first" in forbidden
    assert "human_terminal_pressure_first" in forbidden

def test_correct_starting_posture_is_explicit():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    correct = set(data["correct_starting_posture"])

    assert "listen_first" in correct
    assert "describe_first" in correct
    assert "learn_native_language_first" in correct
    assert "observe_generated_structure_first" in correct

def test_native_language_objects_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    required = {
        "expansion",
        "discharge",
        "debt",
        "shadow",
        "regeneration",
        "compensation",
        "closure",
        "obstruction",
    }

    assert required.issubset(set(data["native_language_objects"]))

def test_previous_layers_are_reclassified():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_inversion_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    reclassified = data["reclassified_layers"]

    assert reclassified["computational_scans"] == "native_instrumentation"
    assert reclassified["evidence_reports"] == "grammar_probes"
    assert reclassified["formal_lemma_drafts"] == "deferred_translation_layer"
    assert reclassified["proof_obligations"] == "translation_debts"
    assert reclassified["termination_question"] == "classical_translation_endpoint"

def test_no_solving_posture_doc_contains_route_correction():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NO_SOLVING_POSTURE.md").read_text(encoding="utf-8")

    assert "Do not solve first." in text
    assert "Do not prove first." in text
    assert "language-learning instrumentation" in text

def test_termination_is_translation_not_source():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "TERMINATION_AS_TRANSLATION.md").read_text(encoding="utf-8")

    assert "Termination is a translation-layer endpoint." in text
    assert "Reaching 1 is not native closure." in text
    assert "Native closure is obstruction potential erased." in text

def test_route_correction_from_v30_reclassifies_formal_lemmas():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "ROUTE_CORRECTION_FROM_V30.md").read_text(encoding="utf-8")

    assert "v3.1 does not delete v3.0." in text
    assert "deferred translation layer" in text
    assert "translation debts" in text
