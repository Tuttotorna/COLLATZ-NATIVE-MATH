import json
import subprocess
import sys
from pathlib import Path


def run_stability_map_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_grammar_stability_map.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_grammar_stability_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_GRAMMAR_STABILITY_MAP.md",
        root / "docs" / "STABILITY_AS_NATIVE_BEHAVIOR.md",
        root / "docs" / "DANGEROUS_STABILITY.md",
        root / "docs" / "DANGEROUS_INSTABILITY.md",
        root / "docs" / "STABILITY_AROUND_9780657630.md",
        root / "docs" / "STABILITY_MAP_LIMITS.md",
        root / "docs" / "V37_EVIDENCE_STATUS.md",
        root / "docs" / "V37_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.7" in text


def test_native_grammar_stability_outputs_exist():
    run_stability_map_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_grammar_stability_map.json").exists()
    assert (root / "results" / "native_grammar_stability_map.md").exists()
    assert (root / "results" / "native_grammar_stability_certificate.json").exists()


def test_native_grammar_stability_certificate_fields():
    run_stability_map_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_grammar_stability_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_mutation_version",
        "source_mutation_edge_count",
        "stability_edge_count",
        "stable_edge_count",
        "unstable_edge_count",
        "dangerous_stable_edge_count",
        "dangerous_unstable_edge_count",
        "release_edge_count",
        "obstruction_relevant_edge_count",
        "obstruction_detected",
        "stability_score",
        "release_score",
        "dangerous_instability_score",
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

    assert data["version"] == "v3.7"
    assert data["certificate_type"] == "native_grammar_stability_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.8 Native Conservation Map"


def test_stability_map_has_native_layer():
    run_stability_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_stability_map.json").read_text(encoding="utf-8"))

    assert data["version"] == "v3.7"
    assert data["layer"] == "native_grammar_stability_map"
    assert data["central_native_question"] == "What does Collatz preserve under recurrence and mutation?"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"


def test_stability_map_has_core_counts():
    run_stability_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_stability_map.json").read_text(encoding="utf-8"))

    assert data["stability_edge_count"] >= 0
    assert data["stable_edge_count"] >= 0
    assert data["unstable_edge_count"] >= 0
    assert data["dangerous_stable_edge_count"] >= 0
    assert data["dangerous_unstable_edge_count"] >= 0
    assert data["release_edge_count"] >= 0
    assert data["obstruction_relevant_edge_count"] >= 0


def test_stability_map_is_not_proof():
    run_stability_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_grammar_stability_map.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["negative_result_boundary"] == (
        "No obstruction-stable grammar detected in this bounded stability map is not proof that obstruction-stable grammar cannot exist."
    )


def test_stability_docs_define_recurrence_mutation_stability():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "STABILITY_AS_NATIVE_BEHAVIOR.md").read_text(encoding="utf-8")

    assert "Recurrence means return." in text
    assert "Mutation means transformation." in text
    assert "Stability means resistance to transformation." in text
    assert "What does Collatz keep?" in text


def test_dangerous_instability_is_not_proof():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "DANGEROUS_INSTABILITY.md").read_text(encoding="utf-8")

    assert "Dangerous instability" in text
    assert "does not prove obstruction impossible" in text
    assert "Collatz can generate danger without keeping danger" in text


def test_9780657630_stability_node_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "STABILITY_AROUND_9780657630.md").read_text(encoding="utf-8")

    assert "9780657630" in text
    assert "not treated as a proof object" in text
    assert "treated as a grammar node" in text
    assert "It does not solve Collatz." in text


def test_next_step_is_conservation_map():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V37_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.8 Native Conservation Map" in text
    assert "Stability asks what resists mutation." in text
    assert "Conservation asks what remains invariant" in text
    assert "No solution before native language." in text
