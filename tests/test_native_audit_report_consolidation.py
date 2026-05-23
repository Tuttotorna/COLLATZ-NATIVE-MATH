import json
import subprocess
import sys
from pathlib import Path


def run_consolidation_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_audit_report_consolidation.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v44_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_AUDIT_REPORT_CONSOLIDATION.md",
        root / "docs" / "CONSOLIDATED_NATIVE_STATUS.md",
        root / "docs" / "AUDIT_REPORT_READER_GUIDE.md",
        root / "docs" / "V44_PUBLIC_STATUS_REPORT.md",
        root / "docs" / "V44_BOUNDARY.md",
        root / "docs" / "V44_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.4" in text


def test_v44_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_audit_report_consolidation_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.4"
    assert data["layer"] == "native_audit_report_consolidation"
    assert data["status"] == "consolidation_layer_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.5 Native Public Research Brief"


def test_v44_builder_outputs_exist_and_are_valid():
    run_consolidation_once()

    root = Path(__file__).resolve().parents[1]

    json_path = root / "results" / "native_audit_report_consolidation.json"
    md_path = root / "results" / "native_audit_report_consolidation.md"
    cert_path = root / "results" / "native_audit_report_consolidation_certificate.json"

    assert json_path.exists()
    assert md_path.exists()
    assert cert_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.4"
    assert data["status"] == "consolidated"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"

    assert cert["version"] == "v4.4"
    assert cert["certificate_type"] == "native_audit_report_consolidation_certificate"
    assert cert["status"] == "consolidated"
    assert cert["proof_status"] == "not_a_proof"
    assert cert["collatz_status"] == "not_claimed_solved"
    assert cert["next_recommended_version"] == "v4.5 Native Public Research Brief"


def test_v44_consolidates_v43_audit_pass():
    run_consolidation_once()

    root = Path(__file__).resolve().parents[1]
    cert = json.loads(
        (root / "results" / "native_audit_report_consolidation_certificate.json")
        .read_text(encoding="utf-8")
    )

    assert cert["audit_total_failure_count"] == 0
    assert cert["indexed_items"] is not None
    assert cert["obstruction_relevant_invariant_candidate_count"] == 0


def test_v44_markdown_preserves_boundary():
    run_consolidation_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "native_audit_report_consolidation.md").read_text(encoding="utf-8")

    assert "proof_status: not_a_proof" in text
    assert "collatz_status: not_claimed_solved" in text
    assert "global_closure_status: not_claimed" in text
    assert "global_invariant_status: not_claimed" in text
    assert "No solution before native language." in text


def test_v44_next_step_is_public_research_brief():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V44_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.5 Native Public Research Brief" in text
    assert "first-time readers" in text
    assert "No solution before native language." in text
