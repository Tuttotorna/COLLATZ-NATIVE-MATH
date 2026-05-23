import json
import subprocess
import sys
from pathlib import Path


def run_extractor_once():
    root = Path(__file__).resolve().parents[1]
    script = root / "examples" / "extract_native_sentences.py"

    assert script.exists()

    subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_native_sentence_docs_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / "docs" / "NATIVE_SENTENCE_EXTRACTOR.md",
        root / "docs" / "NATIVE_SENTENCE_TYPES.md",
        root / "docs" / "TRAJECTORY_AS_NATIVE_UTTERANCE.md",
        root / "docs" / "SENTENCE_EXTRACTION_BOUNDARY.md",
        root / "docs" / "V33_EVIDENCE_STATUS.md",
        root / "docs" / "V33_NEXT_STEPS.md",
    ]

    for path in required:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "Version: v3.3" in text


def test_native_sentence_outputs_exist():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]

    assert (root / "results" / "native_sentences.jsonl").exists()
    assert (root / "results" / "native_sentence_summary.json").exists()
    assert (root / "results" / "native_sentence_report.md").exists()
    assert (root / "results" / "native_sentence_certificate.json").exists()


def test_native_sentence_certificate_fields():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentence_certificate.json"

    data = json.loads(path.read_text(encoding="utf-8"))

    required = [
        "version",
        "certificate_type",
        "source_version",
        "sentence_count",
        "native_sentence_class_counts",
        "dangerous_regeneration_sentence_count",
        "obstruction_candidate_sentence_count",
        "obstruction_detected",
        "mother_rule",
        "proof_status",
        "negative_result_boundary",
        "next_recommended_version",
    ]

    for key in required:
        assert key in data

    assert data["version"] == "v3.3"
    assert data["certificate_type"] == "native_sentence_extraction_certificate"
    assert data["mother_rule"] == "No solution before native language."
    assert data["proof_status"] == "not_a_proof"
    assert data["next_recommended_version"] == "v3.4 Native Sentence Atlas"


def test_native_sentences_are_jsonl_and_have_required_fields():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentences.jsonl"

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert rows

    required = {
        "version",
        "source_version",
        "n0",
        "native_sentence_class",
        "native_tokens",
        "native_reading",
        "proof_status",
        "translation_status",
    }

    for row in rows:
        assert required.issubset(row.keys())
        assert row["version"] == "v3.3"
        assert row["proof_status"] == "not_a_proof"
        assert row["translation_status"] == "native_sentence_extraction_only"
        assert isinstance(row["native_tokens"], list)
        assert row["native_tokens"]


def test_native_sentence_classes_are_valid():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]
    path = root / "results" / "native_sentences.jsonl"

    valid = {
        "MINIMAL_SENTENCE",
        "DEBT_SENTENCE",
        "DEBT_COMPENSATION_SENTENCE",
        "REGENERATION_COMPENSATION_SENTENCE",
        "DANGEROUS_REGENERATION_SENTENCE",
        "OBSTRUCTION_CANDIDATE_SENTENCE",
    }

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    for row in rows:
        assert row["native_sentence_class"] in valid


def test_summary_consistent_with_rows():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]

    rows = [
        json.loads(line)
        for line in (root / "results" / "native_sentences.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]

    summary = json.loads(
        (root / "results" / "native_sentence_summary.json").read_text(encoding="utf-8")
    )

    assert summary["version"] == "v3.3"
    assert summary["sentence_count"] == len(rows)
    assert summary["proof_status"] == "not_a_proof"
    assert summary["mother_rule"] == "No solution before native language."

    class_counts = {}
    for row in rows:
        klass = row["native_sentence_class"]
        class_counts[klass] = class_counts.get(klass, 0) + 1

    assert summary["native_sentence_class_counts"] == dict(sorted(class_counts.items()))


def test_sentence_extraction_boundary_forbids_solution_language():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SENTENCE_EXTRACTION_BOUNDARY.md").read_text(encoding="utf-8")

    assert "Collatz is solved" in text
    assert "global closure is proved" in text
    assert "no obstruction can exist" in text
    assert "native sentence extraction is proof" in text


def test_report_contains_mother_rule_and_boundary():
    run_extractor_once()

    root = Path(__file__).resolve().parents[1]
    text = (root / "results" / "native_sentence_report.md").read_text(encoding="utf-8")

    assert "No solution before native language." in text
    assert "This report does not solve Collatz." in text
    assert "No obstruction sentence extracted in a finite source artifact is not proof" in text
