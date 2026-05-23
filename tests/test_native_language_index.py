import json
import subprocess
import sys
from pathlib import Path


def run_index_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_language_index.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v42_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_LANGUAGE_INDEX.md",
        root / "docs" / "INDEX_READING_ORDER.md",
        root / "docs" / "INDEX_ROLE_MAP.md",
        root / "docs" / "INDEX_BOUNDARY.md",
        root / "docs" / "V42_EVIDENCE_STATUS.md",
        root / "docs" / "V42_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.2" in text


def test_v42_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_index_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.2"
    assert data["layer"] == "native_language_index"
    assert data["status"] == "navigation_index_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["not_theory_layer"] is True
    assert data["not_proof_layer"] is True
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.3 Native Artifact Consistency Audit"


def test_index_outputs_exist():
    run_index_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_language_index.json").exists()
    assert (root / "results" / "native_language_index.md").exists()
    assert (root / "results" / "native_language_index_certificate.json").exists()


def test_index_certificate_fields():
    run_index_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_language_index_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "section_count",
        "total_indexed_items",
        "existing_indexed_items",
        "missing_required_count",
        "mother_rule",
        "secondary_rule",
        "primary_position",
        "proof_status",
        "theorem_status",
        "collatz_status",
        "global_closure_status",
        "global_invariant_status",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v4.2"
    assert data["certificate_type"] == "native_language_index_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.3 Native Artifact Consistency Audit"


def test_index_has_required_sections():
    run_index_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_language_index.json").read_text(encoding="utf-8"))

    section_ids = {section["section_id"] for section in data["sections"]}

    required = {
        "entry_point",
        "native_language_summary",
        "grammar",
        "sentences",
        "sentence_atlas",
        "recurrence",
        "mutation",
        "stability",
        "conservation",
        "invariant_candidates",
        "earlier_native_boundary",
        "latest_tests",
    }

    assert required.issubset(section_ids)


def test_index_is_not_theory_or_proof():
    run_index_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_language_index.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["global_closure_status"] == "not_claimed"
    assert data["global_invariant_status"] == "not_claimed"


def test_index_markdown_contains_navigation_roles():
    run_index_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "native_language_index.md").read_text(encoding="utf-8")

    assert "Entry Point" in text
    assert "Native Grammar" in text
    assert "Native Sentences" in text
    assert "Native Grammar Recurrence" in text
    assert "Native Grammar Mutation" in text
    assert "Native Grammar Stability" in text
    assert "Native Conservation" in text
    assert "Native Invariant Candidates" in text


def test_index_role_map_has_core_distinctions():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "INDEX_ROLE_MAP.md").read_text(encoding="utf-8")

    assert "what_returns" in text
    assert "what_changes" in text
    assert "what_resists_change" in text
    assert "what_remains_through_change" in text
    assert "what_may_remain_under_repeated_native_tests" in text


def test_index_boundary_forbids_claims():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "INDEX_BOUNDARY.md").read_text(encoding="utf-8")

    assert "Collatz solved." in text
    assert "Proof found." in text
    assert "Global closure established." in text
    assert "Global invariant established." in text
    assert "Obstruction impossible." in text


def test_next_step_is_consistency_audit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V42_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.3 Native Artifact Consistency Audit" in text
    assert "indexed files exist" in text
    assert "result certificates agree with summaries" in text
    assert "No solution before native language." in text
