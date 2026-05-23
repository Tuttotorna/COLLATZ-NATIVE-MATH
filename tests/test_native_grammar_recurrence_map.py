import json
import subprocess
import sys
from pathlib import Path


def run_recurrence_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_grammar_recurrence_map.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_grammar_recurrence_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_GRAMMAR_RECURRENCE_MAP.md",
        root / "docs" / "RECURRENCE_AS_NATIVE_BEHAVIOR.md",
        root / "docs" / "DANGEROUS_RECURRENCE.md",
        root / "docs" / "GRAMMAR_MUTATION_TYPES.md",
        root / "docs" / "RECURRENCE_MAP_LIMITS.md",
        root / "docs" / "V35_EVIDENCE_STATUS.md",
        root / "docs" / "V35_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.5" in text


def test_native_grammar_recurrence_outputs_exist():
    run_recurrence_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_grammar_recurrence_map.json").exists()
    assert (root / "results" / "native_grammar_recurrence_map.md").exists()
    assert (root / "results" / "native_grammar_recurrence_certificate.json").exists()


def test_native_grammar_recurrence_certificate_fields():
    run_recurrence_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_recurrence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_atlas_version",
        "sentence_count",
        "total_edge_count",
        "repeat_edge_count",
        "mutation_edge_count",
        "dangerous_edge_count",
        "obstruction_edge_count",
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

    assert data["version"] == "v3.5"
    assert data["certificate_type"] == "native_grammar_recurrence_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.6 Native Grammar Mutation Atlas"


def test_recurrence_map_has_edges_and_counts():
    run_recurrence_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_recurrence_map.json").read_text(encoding="utf-8"))

    assert data["version"] == "v3.5"
    assert data["layer"] == "native_grammar_recurrence_map"
    assert data["sentence_count"] > 0
    assert data["total_edge_count"] >= 0
    assert data["repeat_edge_count"] >= 0
    assert data["mutation_edge_count"] >= 0
    assert data["repeat_edge_count"] + data["mutation_edge_count"] == data["total_edge_count"]


def test_recurrence_map_is_not_proof():
    run_recurrence_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_recurrence_map.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["negative_result_boundary"] == (
        "No obstruction recurrence detected in this bounded recurrence map is not proof that obstruction recurrence cannot exist."
    )


def test_recurrence_keeps_native_language_priority():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_GRAMMAR_RECURRENCE_MAP.md").read_text(encoding="utf-8")

    assert "No solution before native language." in text
    assert "It does not ask whether Collatz is solved." in text
    assert "Which native sentence forms repeat, mutate, stabilize, or disappear?" in text


def test_dangerous_recurrence_boundary_is_explicit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "DANGEROUS_RECURRENCE.md").read_text(encoding="utf-8")

    assert "Dangerous recurrence is not obstruction" in text
    assert "near-obstruction is not obstruction" in text
    assert "Obstruction recurrence cannot exist." in text


def test_mutation_types_define_toward_obstruction():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "GRAMMAR_MUTATION_TYPES.md").read_text(encoding="utf-8")

    assert "toward_obstruction_candidate" in text
    assert "The same sentence class appears again." in text
    assert "dangerous_to_non_obstruction" in text


def test_next_step_is_mutation_atlas():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V35_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.6 Native Grammar Mutation Atlas" in text
    assert "After recurrence, the next question is mutation." in text
    assert "No solution before native language." in text
