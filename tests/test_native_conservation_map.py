import json
import subprocess
import sys
from pathlib import Path


def run_conservation_map_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_conservation_map.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_conservation_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_CONSERVATION_MAP.md",
        root / "docs" / "CONSERVATION_AS_NATIVE_BEHAVIOR.md",
        root / "docs" / "CONSERVATION_OF_DANGER_RELEASE.md",
        root / "docs" / "CONSERVATION_OF_INSTABILITY.md",
        root / "docs" / "CONSERVATION_AROUND_9780657630.md",
        root / "docs" / "CONSERVATION_MAP_LIMITS.md",
        root / "docs" / "V38_EVIDENCE_STATUS.md",
        root / "docs" / "V38_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.8" in text


def test_native_conservation_outputs_exist():
    run_conservation_map_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_conservation_map.json").exists()
    assert (root / "results" / "native_conservation_map.md").exists()
    assert (root / "results" / "native_conservation_certificate.json").exists()


def test_native_conservation_certificate_fields():
    run_conservation_map_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_conservation_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_stability_version",
        "source_stability_edge_count",
        "conservation_candidate_count",
        "obstruction_relevant_conservation_count",
        "dangerous_stability_conservation_count",
        "danger_release_conservation_count",
        "instability_conservation_count",
        "stability_conservation_count",
        "obstruction_detected",
        "danger_release_conservation_ratio",
        "instability_conservation_ratio",
        "dangerous_stability_conservation_ratio",
        "obstruction_relevant_conservation_ratio",
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

    assert data["version"] == "v3.8"
    assert data["certificate_type"] == "native_conservation_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["next_recommended_version"] == "v3.9 Native Invariant Candidate Map"


def test_conservation_map_has_native_layer():
    run_conservation_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_conservation_map.json").read_text(encoding="utf-8"))

    assert data["version"] == "v3.8"
    assert data["layer"] == "native_conservation_map"
    assert data["central_native_question"] == "What remains conserved across recurrence, mutation, and stability?"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"


def test_conservation_map_has_core_counts():
    run_conservation_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_conservation_map.json").read_text(encoding="utf-8"))

    assert data["conservation_candidate_count"] >= 0
    assert data["obstruction_relevant_conservation_count"] >= 0
    assert data["dangerous_stability_conservation_count"] >= 0
    assert data["danger_release_conservation_count"] >= 0
    assert data["instability_conservation_count"] >= 0
    assert data["stability_conservation_count"] >= 0


def test_conservation_map_is_not_proof():
    run_conservation_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_conservation_map.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["negative_result_boundary"] == (
        "Bounded conservation signals do not imply global theorem or global closure."
    )


def test_conservation_docs_define_sequence():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_CONSERVATION_MAP.md").read_text(encoding="utf-8")

    assert "recurrence = what returns" in text
    assert "mutation = what changes" in text
    assert "stability = what resists change" in text
    assert "conservation = what remains through change" in text


def test_danger_release_conservation_boundary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "CONSERVATION_OF_DANGER_RELEASE.md").read_text(encoding="utf-8")

    assert "does not prove that obstruction is impossible" in text
    assert "danger behaves as something that releases" in text
    assert "Danger release conservation is not proof of global closure." in text


def test_9780657630_conservation_probe():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "CONSERVATION_AROUND_9780657630.md").read_text(encoding="utf-8")

    assert "9780657630" in text
    assert "not treated as a proof object" in text
    assert "treated as a conservation probe" in text
    assert "It does not solve Collatz." in text


def test_next_step_is_invariant_candidate_map():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V38_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.9 Native Invariant Candidate Map" in text
    assert "Conservation asks what remains through change." in text
    assert "Invariant candidates ask which conserved behaviors" in text
    assert "No solution before native language." in text
