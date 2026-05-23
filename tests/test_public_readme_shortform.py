import json
import subprocess
import sys
from pathlib import Path


def run_shortform_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_public_readme_shortform.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v46_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "PUBLIC_README_SHORTFORM.md",
        root / "docs" / "README_SHORTFORM_BOUNDARY.md",
        root / "docs" / "README_SHORTFORM_STRUCTURE.md",
        root / "docs" / "README_SHORTFORM_READER_GUIDE.md",
        root / "docs" / "V46_EVIDENCE_STATUS.md",
        root / "docs" / "V46_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.6" in text


def test_v46_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "public_readme_shortform_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.6"
    assert data["layer"] == "public_readme_shortform"
    assert data["status"] == "shortform_layer_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.7 Public Entry Consistency Audit"


def test_shortform_outputs_exist_and_are_valid():
    run_shortform_once()

    root = Path(__file__).resolve().parents[1]

    json_path = root / "results" / "public_readme_shortform.json"
    md_path = root / "results" / "public_readme_shortform.md"
    cert_path = root / "results" / "public_readme_shortform_certificate.json"

    assert json_path.exists()
    assert md_path.exists()
    assert cert_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.6"
    assert data["status"] == "shortform_defined"
    assert data["core_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"

    assert cert["version"] == "v4.6"
    assert cert["certificate_type"] == "public_readme_shortform_certificate"
    assert cert["status"] == "shortform_defined"
    assert cert["proof_status"] == "not_a_proof"
    assert cert["collatz_status"] == "not_claimed_solved"


def test_readme_contains_public_shortform():
    run_shortform_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "README.md").read_text(encoding="utf-8")

    assert "<!-- V4.6_PUBLIC_README_SHORTFORM -->" in text
    assert "## Public shortform" in text
    assert "COLLATZ-NATIVE-MATH is a native structural reading of Collatz dynamics." in text
    assert "What is Collatz before it becomes a conjecture?" in text
    assert "No solution before native language." in text
    assert "results/native_public_research_brief.md" in text
    assert "proof_status: not_a_proof" in text
    assert "collatz_status: not_claimed_solved" in text


def test_shortform_integrity_counts():
    run_shortform_once()

    root = Path(__file__).resolve().parents[1]
    cert = json.loads(
        (root / "results" / "public_readme_shortform_certificate.json")
        .read_text(encoding="utf-8")
    )

    assert cert["audit_total_failure_count"] == 0
    assert cert["index_total_items"] == 101
    assert cert["invariant_candidate_count"] == 45
    assert cert["obstruction_relevant_invariant_candidate_count"] == 0
    assert cert["what_this_is_count"] >= 4
    assert cert["what_this_is_not_count"] >= 5
    assert cert["current_bounded_status_count"] >= 6


def test_next_step_is_public_entry_consistency_audit():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V46_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.7 Public Entry Consistency Audit" in text
    assert "README shortform exists" in text
    assert "No solution before native language." in text
