import json
import subprocess
import sys
from pathlib import Path


def run_invariant_candidate_map_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_invariant_candidate_map.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_invariant_candidate_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_INVARIANT_CANDIDATE_MAP.md",
        root / "docs" / "INVARIANT_CANDIDATE_BOUNDARY.md",
        root / "docs" / "DANGER_RELEASE_INVARIANT_CANDIDATES.md",
        root / "docs" / "DANGEROUS_STABILITY_INVARIANT_CANDIDATES.md",
        root / "docs" / "OBSTRUCTION_RELEVANT_INVARIANT_CANDIDATES.md",
        root / "docs" / "INVARIANT_CANDIDATES_AROUND_9780657630.md",
        root / "docs" / "V39_EVIDENCE_STATUS.md",
        root / "docs" / "V39_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.9" in text


def test_native_invariant_candidate_outputs_exist():
    run_invariant_candidate_map_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_invariant_candidate_map.json").exists()
    assert (root / "results" / "native_invariant_candidate_map.md").exists()
    assert (root / "results" / "native_invariant_candidate_certificate.json").exists()


def test_native_invariant_candidate_certificate_fields():
    run_invariant_candidate_map_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_invariant_candidate_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_conservation_version",
        "source_conservation_candidate_count",
        "invariant_candidate_count",
        "obstruction_relevant_invariant_candidate_count",
        "dangerous_stability_invariant_candidate_count",
        "danger_release_invariant_candidate_count",
        "instability_invariant_candidate_count",
        "weak_invariant_candidate_count",
        "obstruction_detected",
        "danger_release_invariant_ratio",
        "dangerous_stability_invariant_ratio",
        "obstruction_relevant_invariant_ratio",
        "native_interpretation",
        "mother_rule",
        "central_native_question",
        "proof_status",
        "theorem_status",
        "global_invariant_status",
        "negative_result_boundary",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v3.9"
    assert data["certificate_type"] == "native_invariant_candidate_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["global_invariant_status"] == "not_claimed"
    assert data["next_recommended_version"] == "v4.0 Native Language Summary"


def test_invariant_candidate_map_has_native_layer():
    run_invariant_candidate_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_invariant_candidate_map.json").read_text(encoding="utf-8"))

    assert data["version"] == "v3.9"
    assert data["layer"] == "native_invariant_candidate_map"
    assert data["central_native_question"] == "Which conserved behaviors are strong enough to become native invariant candidates?"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["global_invariant_status"] == "not_claimed"


def test_invariant_candidate_map_has_core_counts():
    run_invariant_candidate_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_invariant_candidate_map.json").read_text(encoding="utf-8"))

    assert data["invariant_candidate_count"] >= 0
    assert data["obstruction_relevant_invariant_candidate_count"] >= 0
    assert data["dangerous_stability_invariant_candidate_count"] >= 0
    assert data["danger_release_invariant_candidate_count"] >= 0
    assert data["instability_invariant_candidate_count"] >= 0
    assert data["weak_invariant_candidate_count"] >= 0


def test_invariant_candidate_map_is_not_proof():
    run_invariant_candidate_map_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_invariant_candidate_map.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["global_invariant_status"] == "not_claimed"
    assert data["negative_result_boundary"] == (
        "Bounded invariant candidates are not global invariants and do not imply theorem or proof."
    )


def test_invariant_docs_define_distinctions():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_INVARIANT_CANDIDATE_MAP.md").read_text(encoding="utf-8")

    assert "recurrence = what returns" in text
    assert "mutation = what changes" in text
    assert "stability = what resists change" in text
    assert "conservation = what remains through change" in text
    assert "invariant candidate = what may remain under repeated native tests" in text


def test_invariant_candidate_boundary_forbids_global_claim():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "INVARIANT_CANDIDATE_BOUNDARY.md").read_text(encoding="utf-8")

    assert "This behavior is globally invariant." in text
    assert "This proves Collatz." in text
    assert "This proves global closure." in text
    assert "This proves obstruction impossible." in text


def test_9780657630_invariant_candidate_probe():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "INVARIANT_CANDIDATES_AROUND_9780657630.md").read_text(encoding="utf-8")

    assert "9780657630" in text
    assert "not treated as a proof object" in text
    assert "treated as an invariant-candidate probe" in text
    assert "It does not solve Collatz." in text


def test_next_step_is_native_language_summary():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V39_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.0 Native Language Summary" in text
    assert "solution-seeking to native-language learning" in text
    assert "current non-proof boundary" in text
    assert "No solution before native language." in text
