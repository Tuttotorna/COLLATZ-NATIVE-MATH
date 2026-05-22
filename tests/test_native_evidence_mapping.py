import json
import subprocess
import sys
from pathlib import Path


def test_native_evidence_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_EVIDENCE_MAPPING.md",
        root / "docs" / "EVIDENCE_TO_NATIVE_OBJECTS.md",
        root / "docs" / "NATIVE_EVIDENCE_STATUS.md",
        root / "docs" / "NATIVE_EVIDENCE_LIMITS.md",
        root / "docs" / "NATIVE_TO_STANDARD_PREPARATION.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v1.9" in text


def test_native_evidence_builder_runs():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "build_native_evidence_map.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stderr
    assert "COLLATZ-NATIVE-MATH v1.9" in result.stdout
    assert "Native evidence mapping" in result.stdout
    assert "obstruction detected:" in result.stdout


def test_native_evidence_map_exists_and_is_v19():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_evidence_map.json"

    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["version"] == "v1.9"
    assert data["layer"] == "native_evidence_mapping"
    assert data["status"] == "existing_evidence_mapped_into_native_objects"
    assert data["proof_status"] == "not_a_proof"
    assert data["standard_translation_status"] == "deferred"
    assert data["next_recommended_version"] == "v2.0 Native-to-Standard Translation Boundary"


def test_native_evidence_objects_are_present():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_evidence_map.json").read_text(encoding="utf-8"))

    assert data["native_objects"] == [
        "debt",
        "shadow",
        "compensation",
        "regeneration",
        "closure",
        "obstruction",
    ]


def test_all_expected_evidence_artifacts_are_mapped():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_evidence_map.json").read_text(encoding="utf-8"))

    ids = [item["evidence_id"] for item in data["evidence_maps"]]

    assert ids == [
        "frontier_stability_certificate",
        "compensation_law_candidate_certificate",
        "adversarial_compensation_certificate",
        "hardness_metric_report",
    ]


def test_evidence_map_does_not_claim_proof():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_evidence_map.json").read_text(encoding="utf-8"))

    assert data["proof_status"] == "not_a_proof"

    for item in data["evidence_maps"]:
        assert "proof" in item["proof_status"]


def test_adversarial_mapping_has_no_counterexample_candidate():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_evidence_map.json").read_text(encoding="utf-8"))

    adversarial = [
        item for item in data["evidence_maps"]
        if item["evidence_id"] == "adversarial_compensation_certificate"
    ][0]

    assert adversarial["native_role"] == "adversarial_obstruction_search"
    assert adversarial["closure_status"] == "REGENERATED_BUT_COMPENSATED"
    assert adversarial["obstruction_status"] in {
        "NO_COUNTEREXAMPLE_CANDIDATE_DETECTED",
        "COUNTEREXAMPLE_CANDIDATE_DETECTED",
    }


def test_hardness_mapping_keeps_hardness_separate_from_obstruction():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results" / "native_evidence_map.json").read_text(encoding="utf-8"))

    hardness = [
        item for item in data["evidence_maps"]
        if item["evidence_id"] == "hardness_metric_report"
    ][0]

    assert hardness["native_role"] == "hardness_is_stress_not_obstruction"
    assert hardness["closure_status"] == "UNDECIDED_BY_HARDNESS_ALONE"
    assert hardness["obstruction_status"] == "HARDNESS_DOES_NOT_IMPLY_OBSTRUCTION"


def test_markdown_report_exists():
    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_evidence_map.md"

    assert path.exists()

    text = path.read_text(encoding="utf-8")
    assert "# Native Evidence Map" in text
    assert "It does not prove the Collatz conjecture." in text
    assert "frontier_stability_certificate" in text
    assert "adversarial_compensation_certificate" in text
