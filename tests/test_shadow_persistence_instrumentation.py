import json
import subprocess
import sys
from pathlib import Path


def ensure_v29_artifacts():
    root = Path(__file__).resolve().parents[1]
    report = root / "results" / "shadow_persistence_report.json"
    md = root / "results" / "shadow_persistence_report.md"
    cert = root / "results" / "shadow_persistence_certificate.json"

    if report.exists() and md.exists() and cert.exists():
        return

    script = root / "examples" / "build_shadow_persistence_instrumentation.py"
    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_shadow_persistence_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "SHADOW_PERSISTENCE_INSTRUMENTATION.md",
        root / "docs" / "SHADOW_PERSISTENCE_SIGNAL.md",
        root / "docs" / "SHADOW_CHAIN_CLASSIFICATION.md",
        root / "docs" / "V29_EVIDENCE_STATUS.md",
        root / "docs" / "V29_LIMITS.md",
        root / "docs" / "V29_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v2.9" in text


def test_shadow_persistence_builder_exists():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_shadow_persistence_instrumentation.py"

    assert script.exists()
    text = script.read_text(encoding="utf-8")

    assert "Shadow Persistence Instrumentation" in text
    assert "obstruction-preserving shadow" in text
    assert "not_a_proof" in text


def test_shadow_persistence_artifacts_exist():
    ensure_v29_artifacts()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "shadow_persistence_report.json").exists()
    assert (root / "results" / "shadow_persistence_report.md").exists()
    assert (root / "results" / "shadow_persistence_certificate.json").exists()


def test_shadow_persistence_certificate_fields():
    ensure_v29_artifacts()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_persistence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_version",
        "tested_candidate_count",
        "source_debt_window_count",
        "source_regeneration_count",
        "source_dangerous_regeneration_count",
        "source_obstruction_candidate_count",
        "shadow_classification_counts",
        "persistent_shadow_signal_count",
        "obstruction_candidate_shadow_count",
        "strongest_shadow_case",
        "native_interpretation",
        "obstruction_detected",
        "proof_status",
        "negative_result_boundary",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v2.9"
    assert data["certificate_type"] == "shadow_persistence_instrumentation_certificate"
    assert data["proof_status"] == "not_a_proof"
    assert data["theorem_status"] == "no_theorems_introduced"
    assert data["minimum_report_fields_present"] is True
    assert data["next_recommended_version"] == "v3.0 Formal Native-to-Standard Lemma Draft"


def test_shadow_classification_counts_are_present():
    ensure_v29_artifacts()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_persistence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))
    counts = data["shadow_classification_counts"]

    assert isinstance(counts, dict)
    assert counts

    allowed = {
        "NO_SHADOW_SIGNAL",
        "DEBT_WITHOUT_REGENERATION_SHADOW",
        "REGENERATION_WITHOUT_DANGEROUS_SHADOW_SIGNAL",
        "DANGEROUS_REGENERATION_WITH_WEAK_SHADOW_SIGNAL",
        "PERSISTENT_SHADOW_SIGNAL",
        "OBSTRUCTION_CANDIDATE_SHADOW",
    }

    for key in counts:
        assert key in allowed


def test_negative_result_boundary_is_explicit():
    ensure_v29_artifacts()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "shadow_persistence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["negative_result_boundary"] == (
        "No obstruction-preserving shadow detected in a finite instrumentation layer is not proof that such shadow cannot exist."
    )


def test_report_is_not_proof():
    ensure_v29_artifacts()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "shadow_persistence_report.md").read_text(encoding="utf-8")

    assert "It does not prove the Collatz conjecture." in text
    assert "It does not prove global closure." in text
    assert "Do not claim final proof" in text


def test_v29_next_step_is_formal_draft_not_raw_scan():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "V29_NEXT_STEPS.md").read_text(encoding="utf-8")

    assert "v3.0 Formal Native-to-Standard Lemma Draft" in text
    assert "The next step should not be another raw scan." in text
    assert "Formal lemma draft only." in text
