import json
from pathlib import Path

def test_native_grammar_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_GRAMMAR_MAP.md",
        root / "docs" / "NATIVE_GRAMMAR_OBJECTS.md",
        root / "docs" / "NATIVE_GRAMMAR_TRANSITIONS.md",
        root / "docs" / "NATIVE_GRAMMAR_SEQUENCES.md",
        root / "docs" / "GRAMMAR_PROBE_RECLASSIFICATION.md",
        root / "docs" / "NATIVE_GRAMMAR_FORBIDDEN_TRANSLATIONS.md",
        root / "docs" / "V32_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.2" in text

def test_native_grammar_manifest_exists_and_is_v32():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v3.2"
    assert data["layer"] == "native_grammar_map"
    assert data["status"] == "native_grammar_defined"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.3 Native Sentence Extractor"

def test_mother_rule_and_secondary_rule_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["mother_rule"] == "No solution before native language."
    assert data["secondary_rule"] == "No proof before native description."

def test_core_grammar_objects_are_present():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    objects = {item["object"] for item in data["grammar_objects"]}

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

    assert required.issubset(objects)

def test_native_transitions_include_closure_and_obstruction():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    transitions = {item["transition"] for item in data["grammar_transitions"]}

    assert "expansion -> discharge" in transitions
    assert "weak_discharge -> debt" in transitions
    assert "debt -> shadow" in transitions
    assert "debt -> compensation" in transitions
    assert "compensation -> regeneration" in transitions
    assert "regeneration -> compensation" in transitions
    assert "regeneration -> persistent_shadow" in transitions
    assert "compensation + shadow_erasure + failed_obstruction_preservation -> closure" in transitions
    assert "debt + non_erased_shadow + dangerous_regeneration + insufficient_compensation -> obstruction_candidate" in transitions

def test_native_sequences_are_defined():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    sequence_ids = {item["sequence_id"] for item in data["native_sequences"]}

    assert "minimal_odd_block_sentence" in sequence_ids
    assert "debt_sentence" in sequence_ids
    assert "recovery_sentence" in sequence_ids
    assert "shadow_sentence" in sequence_ids
    assert "regeneration_sentence" in sequence_ids
    assert "benign_regeneration_sentence" in sequence_ids
    assert "closure_candidate_sentence" in sequence_ids
    assert "obstruction_candidate_sentence" in sequence_ids

def test_forbidden_translations_block_classical_collapse():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    forbidden = set(data["forbidden_translations"])

    assert "native_grammar_to_proof_claim" in forbidden
    assert "closure_to_reaches_1" in forbidden
    assert "dangerous_regeneration_to_obstruction" in forbidden
    assert "no_obstruction_detected_to_obstruction_impossible" in forbidden
    assert "hardest_case_to_deepest_native_meaning" in forbidden
    assert "standard_notation_to_native_understanding" in forbidden

def test_prior_layers_are_reclassified_as_grammar_probes():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_map_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    reclassified = data["reclassified_layers"]

    assert reclassified["frontier_stability_scans"] == "grammar_probes_for_recovery_pressure"
    assert reclassified["compensation_scans"] == "grammar_probes_for_debt_repair"
    assert reclassified["adversarial_compensation_scans"] == "grammar_probes_for_near_obstruction_behavior"
    assert reclassified["hardness_reports"] == "grammar_probes_for_structural_stress"
    assert reclassified["bounded_obstruction_scanner"] == "grammar_probe_for_obstruction_preserving_regeneration"
    assert reclassified["shadow_persistence_instrumentation"] == "grammar_probe_for_non_erased_debt_traces"
    assert reclassified["formal_lemma_drafts"] == "deferred_translation_layer"
    assert reclassified["proof_obligations"] == "translation_debts"
    assert reclassified["termination_question"] == "classical_endpoint_translation"

def test_docs_state_no_solution_before_language():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "NATIVE_GRAMMAR_MAP.md").read_text(encoding="utf-8")

    assert "Do not solve first." in text
    assert "Describe first." in text
    assert "This is not a proof of the Collatz conjecture." in text

def test_next_step_is_native_sentence_extractor():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "V32_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.3 Native Sentence Extractor" in text
    assert "To listen." in text
    assert "It must remain a native description layer." in text
