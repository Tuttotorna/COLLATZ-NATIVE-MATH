import json
import subprocess
import sys
from pathlib import Path


def run_mutation_atlas_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_grammar_mutation_atlas.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_grammar_mutation_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_GRAMMAR_MUTATION_ATLAS.md",
        root / "docs" / "MUTATION_AS_NATIVE_GRAMMAR.md",
        root / "docs" / "DANGEROUS_TO_RECOVERY_MUTATIONS.md",
        root / "docs" / "DANGEROUS_PERSISTENCE_MUTATIONS.md",
        root / "docs" / "MUTATION_AROUND_9780657630.md",
        root / "docs" / "MUTATION_ATLAS_LIMITS.md",
        root / "docs" / "V36_EVIDENCE_STATUS.md",
        root / "docs" / "V36_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.6" in text


def test_native_grammar_mutation_outputs_exist():
    run_mutation_atlas_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_grammar_mutation_atlas.json").exists()
    assert (root / "results" / "native_grammar_mutation_atlas.md").exists()
    assert (root / "results" / "native_grammar_mutation_certificate.json").exists()


def test_native_grammar_mutation_certificate_fields():
    run_mutation_atlas_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_mutation_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_recurrence_version",
        "source_sentence_count",
        "source_total_edge_count",
        "mutation_edge_count",
        "dangerous_mutation_count",
        "dangerous_release_mutation_count",
        "dangerous_persistence_mutation_count",
        "obstruction_mutation_count",
        "obstruction_detected",
        "native_interpretation",
        "mother_rule",
        "central_native_question",
        "proof_status",
        "theorem_status",
        "negative_result_boundary",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v3.6"
    assert data["certificate_type"] == "native_grammar_mutation_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.7 Native Grammar Stability Map"


def test_mutation_atlas_has_native_layer():
    run_mutation_atlas_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_mutation_atlas.json").read_text(encoding="utf-8"))

    assert data["version"] == "v3.6"
    assert data["layer"] == "native_grammar_mutation_atlas"
    assert data["central_native_question"] == "How does one native sentence transform into another?"
    assert data["mutation_edge_count"] >= 0
    assert data["proof_status"] == "not_a_proof"


def test_mutation_atlas_is_not_proof():
    run_mutation_atlas_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_mutation_atlas.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["negative_result_boundary"] == (
        "No obstruction mutation detected in this bounded mutation atlas is not proof that obstruction mutation cannot exist."
    )


def test_mutation_types_are_documented():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_GRAMMAR_MUTATION_ATLAS.md").read_text(encoding="utf-8")

    assert "dangerous release mutation" in text
    assert "dangerous persistence mutation" in text
    assert "toward-obstruction mutation" in text
    assert "No solution before native language." in text


def test_dangerous_release_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "DANGEROUS_TO_RECOVERY_MUTATIONS.md").read_text(encoding="utf-8")

    assert "Dangerous forms always recover." in text
    assert "Obstruction is impossible." in text
    assert "Collatz is solved." in text
    assert "bounded mutation atlas observed dangerous-release behavior" in text


def test_9780657630_is_treated_as_grammar_node_not_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "MUTATION_AROUND_9780657630.md").read_text(encoding="utf-8")

    assert "9780657630" in text
    assert "possible grammar node" in text
    assert "It does not imply obstruction." in text
    assert "A strong mutation node is not a proof." in text


def test_next_step_is_stability_map():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V36_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.7 Native Grammar Stability Map" in text
    assert "After recurrence and mutation, the next native question is stability." in text
    assert "No solution before native language." in text
