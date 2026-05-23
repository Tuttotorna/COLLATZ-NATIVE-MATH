import json
import subprocess
import sys
from pathlib import Path


def run_audit_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_artifact_consistency_audit.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v43_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_ARTIFACT_CONSISTENCY_AUDIT.md",
        root / "docs" / "AUDIT_CHECKS.md",
        root / "docs" / "AUDIT_BOUNDARY.md",
        root / "docs" / "AUDIT_CERTIFICATE_REQUIREMENTS.md",
        root / "docs" / "AUDIT_ENTRY_FILE_REQUIREMENTS.md",
        root / "docs" / "V43_EVIDENCE_STATUS.md",
        root / "docs" / "V43_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.3" in text


def test_v43_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_artifact_consistency_audit_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.3"
    assert data["layer"] == "native_artifact_consistency_audit"
    assert data["status"] == "audit_layer_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["not_theory_layer"] is True
    assert data["not_proof_layer"] is True
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.4 Native Audit Report Consolidation"


def test_audit_outputs_exist_and_pass():
    run_audit_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_artifact_consistency_audit.json").exists()
    assert (root / "results" / "native_artifact_consistency_audit.md").exists()
    assert (root / "results" / "native_artifact_consistency_audit_certificate.json").exists()

    certificate = json.loads(
        (root / "results" / "native_artifact_consistency_audit_certificate.json")
        .read_text(encoding="utf-8")
    )

    assert certificate["version"] == "v4.3"
    assert certificate["certificate_type"] == "native_artifact_consistency_audit_certificate"
    assert certificate["status"] == "audit_passed"
    assert certificate["total_failure_count"] == 0


def test_audit_json_has_all_check_groups():
    run_audit_once()

    root = Path(__file__).resolve().parents[1]
    data = json.loads(
        (root / "results" / "native_artifact_consistency_audit.json")
        .read_text(encoding="utf-8")
    )

    assert "index_audit" in data
    assert "entry_audit" in data
    assert "certificate_audit" in data
    assert "builder_audit" in data
    assert "readme_route_audit" in data

    assert data["index_audit"]["missing_required_count"] == 0
    assert data["entry_audit"]["entry_failure_count"] == 0
    assert data["certificate_audit"]["certificate_failure_count"] == 0
    assert data["builder_audit"]["builder_missing_count"] == 0
    assert data["readme_route_audit"]["missing_route_version_count"] == 0


def test_audit_boundary_doc_forbids_overclaims():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "AUDIT_BOUNDARY.md").read_text(encoding="utf-8")

    assert "Collatz solved." in text
    assert "Proof found." in text
    assert "Global closure established." in text
    assert "Global invariant established." in text
    assert "Obstruction impossible." in text
    assert "No solution before native language." in text


def test_next_step_is_audit_report_consolidation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V43_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.4 Native Audit Report Consolidation" in text
    assert "audit result" in text
    assert "index result" in text
    assert "No solution before native language." in text
