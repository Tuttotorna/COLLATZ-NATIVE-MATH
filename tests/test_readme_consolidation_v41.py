import json
from pathlib import Path


def test_v41_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "README_CONSOLIDATION_V41.md",
        root / "docs" / "ENTRY_POINT_BOUNDARY.md",
        root / "docs" / "PUBLIC_REPO_POSITIONING.md",
        root / "docs" / "README_ROUTE_SUMMARY.md",
        root / "docs" / "V41_NON_PROOF_BOUNDARY.md",
        root / "docs" / "V41_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.1" in text


def test_v41_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "readme_consolidation_v41_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.1"
    assert data["layer"] == "native_language_readme_consolidation"
    assert data["status"] == "entry_point_consolidated"
    assert data["mother_rule"] == "No solution before native language."
    assert data["secondary_rule"] == "No proof before native description."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.2 Native Language Index"


def test_readme_has_correct_primary_position():
    root = Path(__file__).resolve().parents[1]
    text = (root / "README.md").read_text(encoding="utf-8")

    assert "A native structural reading of the Collatz dynamics." in text
    assert "This repository does not begin by trying to solve Collatz." in text
    assert "What is Collatz before it becomes a conjecture?" in text
    assert "No solution before native language." in text
    assert "No proof before native description." in text


def test_readme_forbids_proof_claims():
    root = Path(__file__).resolve().parents[1]
    text = (root / "README.md").read_text(encoding="utf-8")

    assert "proof_status: not_a_proof" in text
    assert "theorem_status: no_theorems_introduced" in text
    assert "collatz_status: not_claimed_solved" in text
    assert "global_closure_status: not_claimed" in text
    assert "global_invariant_status: not_claimed" in text


def test_start_here_is_native_first():
    root = Path(__file__).resolve().parents[1]
    text = (root / "START_HERE.md").read_text(encoding="utf-8")

    assert "Do not start from the proof question." in text
    assert "Start from the native-language question." in text
    assert "No solution before native language." in text
    assert "It is not a proof of Collatz." in text
    assert "It is not a claim that Collatz is solved." in text


def test_crc_conjecture_reframed():
    root = Path(__file__).resolve().parents[1]
    text = (root / "CRC_CONJECTURE.md").read_text(encoding="utf-8")

    assert "Not solution-first" in text
    assert "What is Collatz before it becomes a conjecture?" in text
    assert "No solution before native language." in text
    assert "The repository is building a native description first." in text


def test_public_positioning_doc_is_not_solution_first():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "PUBLIC_REPO_POSITIONING.md").read_text(encoding="utf-8")

    assert "COLLATZ-NATIVE-MATH is a native structural reading of the Collatz dynamics." in text
    assert "This project does not begin by trying to solve Collatz." in text
    assert "Do not present this repository as:" in text
    assert "a proof of Collatz" in text
    assert "a solution to Collatz" in text


def test_non_proof_boundary_doc_contains_required_statuses():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V41_NON_PROOF_BOUNDARY.md").read_text(encoding="utf-8")

    assert "proof_status: not_a_proof" in text
    assert "theorem_status: no_theorems_introduced" in text
    assert "collatz_status: not_claimed_solved" in text
    assert "global_closure_status: not_claimed" in text
    assert "global_invariant_status: not_claimed" in text


def test_next_step_is_native_language_index():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V41_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.2 Native Language Index" in text
    assert "navigation layer" in text
    assert "No solution before native language." in text
