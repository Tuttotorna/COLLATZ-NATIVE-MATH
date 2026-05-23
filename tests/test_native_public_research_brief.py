import json
import subprocess
import sys
from pathlib import Path


def run_public_brief_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_public_research_brief.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_v45_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_PUBLIC_RESEARCH_BRIEF.md",
        root / "docs" / "PUBLIC_BRIEF_BOUNDARY.md",
        root / "docs" / "PUBLIC_BRIEF_READER_PATH.md",
        root / "docs" / "PUBLIC_BRIEF_ALLOWED_CLAIMS.md",
        root / "docs" / "PUBLIC_BRIEF_FORBIDDEN_CLAIMS.md",
        root / "docs" / "V45_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v4.5" in text


def test_v45_manifest_exists_and_is_correct():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_public_research_brief_manifest.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.5"
    assert data["layer"] == "native_public_research_brief"
    assert data["status"] == "public_brief_layer_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"
    assert data["next_recommended_version"] == "v4.6 Public README Shortform"


def test_public_brief_outputs_exist_and_are_valid():
    run_public_brief_once()

    root = Path(__file__).resolve().parents[1]

    json_path = root / "results" / "native_public_research_brief.json"
    md_path = root / "results" / "native_public_research_brief.md"
    cert_path = root / "results" / "native_public_research_brief_certificate.json"

    assert json_path.exists()
    assert md_path.exists()
    assert cert_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    assert data["version"] == "v4.5"
    assert data["status"] == "public_brief_defined"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["collatz_status"] == "not_claimed_solved"

    assert cert["version"] == "v4.5"
    assert cert["certificate_type"] == "native_public_research_brief_certificate"
    assert cert["status"] == "public_brief_defined"
    assert cert["brief_section_count"] >= 8
    assert cert["proof_status"] == "not_a_proof"
    assert cert["collatz_status"] == "not_claimed_solved"


def test_public_brief_integrity_counts():
    run_public_brief_once()

    root = Path(__file__).resolve().parents[1]
    cert = json.loads(
        (root / "results" / "native_public_research_brief_certificate.json")
        .read_text(encoding="utf-8")
    )

    assert cert["audit_total_failure_count"] == 0
    assert cert["index_total_items"] == 101
    assert cert["obstruction_relevant_invariant_candidate_count"] == 0
    assert cert["allowed_public_claim_count"] >= 5
    assert cert["forbidden_public_claim_count"] >= 6


def test_public_brief_markdown_preserves_boundary():
    run_public_brief_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "native_public_research_brief.md").read_text(encoding="utf-8")

    assert "No solution before native language." in text
    assert "proof_status: not_a_proof" in text
    assert "collatz_status: not_claimed_solved" in text
    assert "global_closure_status: not_claimed" in text
    assert "global_invariant_status: not_claimed" in text


def test_next_step_is_public_readme_shortform():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V45_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v4.6 Public README Shortform" in text
    assert "one-sentence description" in text
    assert "No solution before native language." in text
