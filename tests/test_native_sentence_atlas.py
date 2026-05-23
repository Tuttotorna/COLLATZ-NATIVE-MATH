import json
import subprocess
import sys
from pathlib import Path


def run_atlas_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_sentence_atlas.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_sentence_atlas_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_SENTENCE_ATLAS.md",
        root / "docs" / "NATIVE_SENTENCE_FAMILIES.md",
        root / "docs" / "NATIVE_SENTENCE_ATLAS_INTERPRETATION.md",
        root / "docs" / "RARE_NATIVE_SENTENCES.md",
        root / "docs" / "DANGEROUS_SENTENCE_ATLAS.md",
        root / "docs" / "V34_ATLAS_LIMITS.md",
        root / "docs" / "V34_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.4" in text


def test_native_sentence_atlas_outputs_exist():
    run_atlas_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_sentence_atlas.json").exists()
    assert (root / "results" / "native_sentence_atlas.md").exists()
    assert (root / "results" / "native_sentence_atlas_certificate.json").exists()


def test_native_sentence_atlas_certificate_fields():
    run_atlas_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentence_atlas_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_version",
        "sentence_count",
        "dangerous_sentence_count",
        "obstruction_sentence_count",
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

    assert data["version"] == "v3.4"
    assert data["certificate_type"] == "native_sentence_atlas_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.5 Native Grammar Recurrence Map"


def test_native_sentence_atlas_has_counts():
    run_atlas_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentence_atlas.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v3.4"
    assert data["layer"] == "native_sentence_atlas"
    assert data["sentence_count"] > 0
    assert isinstance(data["sentence_class_counts"], dict)
    assert isinstance(data["sentence_family_counts"], dict)
    assert isinstance(data["native_word_counts"], dict)


def test_native_sentence_atlas_is_not_proof():
    run_atlas_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentence_atlas.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["negative_result_boundary"] == (
        "No obstruction sentence detected in this atlas is not proof that obstruction sentences cannot exist."
    )


def test_atlas_keeps_native_language_priority():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "NATIVE_SENTENCE_ATLAS.md").read_text(encoding="utf-8")

    assert "No solution before native language." in text
    assert "The purpose is not to solve Collatz." in text
    assert "The purpose is to listen" in text


def test_dangerous_sentence_boundary_is_explicit():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "DANGEROUS_SENTENCE_ATLAS.md").read_text(encoding="utf-8")

    assert "Dangerous is not obstruction" in text
    assert "A tight surplus is not obstruction." in text
    assert "High recovery stress is not obstruction." in text


def test_atlas_limit_rejects_final_truth_claim():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "V34_ATLAS_LIMITS.md").read_text(encoding="utf-8")

    assert "The atlas does not prove Collatz." in text
    assert "The atlas does not disprove Collatz." in text
    assert "It cannot say:" in text
    assert "This is the final truth of all Collatz trajectories." in text


def test_next_step_is_recurrence_not_solution():
    root = Path(__file__).resolve().parents[1]

    text = (root / "docs" / "V34_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.5 Native Grammar Recurrence Map" in text
    assert "the next question is not proof" in text
    assert "No solution before native language." in text
