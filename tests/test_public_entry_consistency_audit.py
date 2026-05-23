import json
import subprocess
import sys
from pathlib import Path


def run_public_entry_audit_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_public_entry_consistency_audit.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v47_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "PUBLIC_ENTRY_CONSISTENCY_AUDIT.md",
        root / "docs" / "PUBLIC_ENTRY_AUDIT_CHECKS.md",
        root / "docs" / "PUBLIC_ENTRY_AUDIT_BOUNDARY.md",
        root / "docs" / "PUBLIC_ENTRY_ALIGNMENT_REQUIREMENTS.md",
        root / "docs" / "V47_EVIDENCE_STATUS.md",
        root / "docs" / "V47_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.7" in text


def test_v47_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "public_entry_consistency_audit_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.7"
    assert data["layer"] == "public_entry_consistency_audit"
    assert data["status"] == "public_entry_audit_layer_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.8 Public Release Snapshot"


def test_public_entry_audit_outputs_exist_and_pass():
    run_public_entry_audit_once()

    root = Path(__file__).resolve().parents[1]

    json_path = root / "results" / "public_entry_consistency_audit.json"
    md_path = root / "results" / "public_entry_consistency_audit.md"
    cert_path = root / "results" / "public_entry_consistency_audit_certificate.json"

    assert json_path.exists()
    assert md_path.exists()
    assert cert_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.7"
    assert data["status"] == "public_entry_audit_passed"
    assert data["total_failure_count"] == 0
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"

    assert cert["version"] == "v4.7"
    assert cert["certificate_type"] == "public_entry_consistency_audit_certificate"
    assert cert["status"] == "public_entry_audit_passed"
    assert cert["total_failure_count"] == 0


def test_public_entry_audit_check_counts_are_zero():
    run_public_entry_audit_once()

    root = Path(__file__).resolve().parents[1]
    cert = json.loads(
        (root / "results" / "public_entry_consistency_audit_certificate.json")
        .read_text(encoding="utf-8")
    )

    assert cert["entry_failure_count"] == 0
    assert cert["artifact_missing_count"] == 0
    assert cert["certificate_failure_count"] == 0
    assert cert["source_shortform_version"] == "v4.6"
    assert cert["source_shortform_status"] == "shortform_defined"
    assert cert["source_audit_total_failure_count"] == 0


def test_readme_public_entry_requirements_are_present():
    root = Path(__file__).resolve().parents[1]
    text = (root / "README.md").read_text(encoding="utf-8")

    assert "<!-- V4.6_PUBLIC_README_SHORTFORM -->" in text
    assert "What is Collatz before it becomes a conjecture?" in text
    assert "No solution before native language." in text
    assert "results/native_public_research_brief.md" in text
    assert "results/native_audit_report_consolidation.md" in text
    assert "proof_status: not_a_proof" in text
    assert "collatz_status: not_claimed_solved" in text


def test_v47_next_step_is_public_release_snapshot():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V47_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.8 Public Release Snapshot" in text
    assert "public-ready state" in text
    assert "No solution before native language." in text
