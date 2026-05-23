import json
import subprocess
import sys
from pathlib import Path


def run_native_language_summary_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_language_summary.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_language_summary_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_LANGUAGE_SUMMARY.md",
        root / "docs" / "NATIVE_LANGUAGE_ROUTE.md",
        root / "docs" / "WHAT_COLLATZ_HAS_SAID.md",
        root / "docs" / "NATIVE_LANGUAGE_BOUNDARY.md",
        root / "docs" / "V40_PUBLIC_POSITIONING.md",
        root / "docs" / "V40_EVIDENCE_STATUS.md",
        root / "docs" / "V40_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.0" in text


def test_native_language_summary_outputs_exist():
    run_native_language_summary_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_language_summary.json").exists()
    assert (root / "results" / "native_language_summary.md").exists()
    assert (root / "results" / "native_language_summary_certificate.json").exists()


def test_native_language_summary_certificate_fields():
    run_native_language_summary_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_summary_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_invariant_version",
        "source_invariant_candidate_count",
        "source_danger_release_invariant_candidate_count",
        "source_dangerous_stability_invariant_candidate_count",
        "source_obstruction_relevant_invariant_candidate_count",
        "route_version_count",
        "native_language_object_count",
        "learned_pattern_count",
        "primary_position",
        "mother_rule",
        "central_native_question",
        "native_interpretation",
        "proof_status",
        "theorem_status",
        "global_closure_status",
        "global_invariant_status",
        "collatz_status",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v4.0"
    assert data["certificate_type"] == "native_language_summary_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["global_closure_status"] == "not_claimed"
    assert data["global_invariant_status"] == "not_claimed"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.1 Native Language README Consolidation"


def test_native_language_summary_has_route():
    run_native_language_summary_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_language_summary.json").read_text(encoding="utf-8"))

    assert data["version"] == "v4.0"
    assert data["layer"] == "native_language_summary"
    assert data["route_version_count"] == 9

    versions = [item["version"] for item in data["route"]]

    assert versions == [
        "v3.1",
        "v3.2",
        "v3.3",
        "v3.4",
        "v3.5",
        "v3.6",
        "v3.7",
        "v3.8",
        "v3.9",
    ]


def test_native_language_summary_is_not_proof():
    run_native_language_summary_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_language_summary.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["global_closure_status"] == "not_claimed"
    assert data["global_invariant_status"] == "not_claimed"
    assert data["collatz_status"] == "not_claimed_solved"


def test_primary_position_is_present():
    run_native_language_summary_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_language_summary.json").read_text(encoding="utf-8"))

    assert data["primary_position"] == (
        "Collatz is not treated first as a conjecture to solve, but as a native dynamical language whose grammar can be observed, mapped, and only later translated."
    )


def test_docs_contain_no_solution_before_language():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "NATIVE_LANGUAGE_SUMMARY.md").read_text(encoding="utf-8")

    assert "No solution before native language." in text
    assert "No proof before native description." in text
    assert "This is not a proof." in text
    assert "This is not a theorem." in text
    assert "This is not a solution claim." in text


def test_what_collatz_has_said_contains_observations():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "WHAT_COLLATZ_HAS_SAID.md").read_text(encoding="utf-8")

    assert "Collatz can generate dangerous native sentence forms." in text
    assert "Some dangerous native forms release." in text
    assert "Some dangerous native forms remain stable" in text
    assert "No obstruction-relevant invariant candidate was detected" in text
    assert "9780657630" in text


def test_public_positioning_is_not_solution_first():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V40_PUBLIC_POSITIONING.md").read_text(encoding="utf-8")

    assert "should not be presented as another attempt to solve Collatz first" in text
    assert "A native structural reading of the Collatz dynamics." in text
    assert "No solution before native language." in text


def test_next_step_is_readme_consolidation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V40_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.1 Native Language README Consolidation" in text
    assert "The README should stop looking like a proof attempt." in text
    assert "No solution before native language." in text
