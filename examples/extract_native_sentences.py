#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.3

Native Sentence Extractor.

This script does not try to solve Collatz.
It extracts native grammar sentences from existing trajectory evidence.

Input priority:
1. results/expanded_bounded_obstruction_search_rows.jsonl
2. results/bounded_obstruction_search_rows.jsonl

Outputs:
- results/native_sentences.jsonl
- results/native_sentence_summary.json
- results/native_sentence_report.md
- results/native_sentence_certificate.json
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "v3.3"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

EXPANDED_ROWS = RESULTS_DIR / "expanded_bounded_obstruction_search_rows.jsonl"
BOUNDED_ROWS = RESULTS_DIR / "bounded_obstruction_search_rows.jsonl"

SENTENCES_PATH = RESULTS_DIR / "native_sentences.jsonl"
SUMMARY_PATH = RESULTS_DIR / "native_sentence_summary.json"
REPORT_PATH = RESULTS_DIR / "native_sentence_report.md"
CERTIFICATE_PATH = RESULTS_DIR / "native_sentence_certificate.json"


def load_rows() -> tuple[str, List[Dict[str, Any]]]:
    if EXPANDED_ROWS.exists():
        source = EXPANDED_ROWS
        source_version = "v2.8"
    elif BOUNDED_ROWS.exists():
        source = BOUNDED_ROWS
        source_version = "v2.6"
    else:
        raise FileNotFoundError(
            "No source row artifact found. Expected v2.8 expanded rows or v2.6 bounded rows."
        )

    rows: List[Dict[str, Any]] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

    return source_version, rows


def sentence_tokens(row: Dict[str, Any]) -> List[str]:
    debt_windows = int(row.get("debt_window_count", 0))
    recovered = int(row.get("recovered_debt_window_count", 0))
    unrecovered = int(row.get("unrecovered_debt_window_count", 0))
    regenerations = int(row.get("regeneration_count", 0))
    dangerous = int(row.get("dangerous_regeneration_count", 0))
    obstruction = int(row.get("obstruction_candidate_count", 0))
    result_type = str(row.get("closure_result_type", "UNDECIDED"))

    tokens: List[str] = ["trajectory_observed"]

    if debt_windows <= 0:
        tokens.append("no_debt_sentence")
    else:
        tokens.append("debt_generated")

    if recovered > 0:
        tokens.append("compensation_found")

    if unrecovered > 0:
        tokens.append("unrecovered_debt_found")

    if regenerations > 0:
        tokens.append("regeneration_found")

    if dangerous > 0:
        tokens.append("dangerous_regeneration_found")

    if obstruction > 0 or result_type == "OBSTRUCTION_CANDIDATE_DETECTED":
        tokens.append("obstruction_candidate_found")
    elif dangerous > 0:
        tokens.append("obstruction_not_preserved")
    elif regenerations > 0:
        tokens.append("regenerated_but_compensated")
    elif recovered > 0:
        tokens.append("local_recovery_found")
    else:
        tokens.append("no_obstruction_signal")

    if result_type == "NO_DEBT_DETECTED":
        tokens.append("native_sentence_minimal")
    elif result_type == "DEBT_LOCALLY_RECOVERED":
        tokens.append("native_sentence_recovery")
    elif result_type == "REGENERATED_BUT_COMPENSATED":
        tokens.append("native_sentence_benign_regeneration")
    elif result_type == "DANGEROUS_REGENERATION_DETECTED":
        tokens.append("native_sentence_dangerous_regeneration")
    elif result_type == "OBSTRUCTION_CANDIDATE_DETECTED":
        tokens.append("native_sentence_obstruction_candidate")
    else:
        tokens.append("native_sentence_undecided")

    return tokens


def sentence_class(row: Dict[str, Any], tokens: List[str]) -> str:
    if "obstruction_candidate_found" in tokens:
        return "OBSTRUCTION_CANDIDATE_SENTENCE"
    if "dangerous_regeneration_found" in tokens:
        return "DANGEROUS_REGENERATION_SENTENCE"
    if "regeneration_found" in tokens:
        return "REGENERATION_COMPENSATION_SENTENCE"
    if "compensation_found" in tokens:
        return "DEBT_COMPENSATION_SENTENCE"
    if "debt_generated" in tokens:
        return "DEBT_SENTENCE"
    return "MINIMAL_SENTENCE"


def native_reading(row: Dict[str, Any], tokens: List[str]) -> str:
    n0 = row.get("n0")

    if "obstruction_candidate_found" in tokens:
        return f"n0={n0}: debt persisted into an obstruction-candidate sentence under the bounded grammar."
    if "dangerous_regeneration_found" in tokens:
        return f"n0={n0}: debt was generated, compensation appeared, regeneration returned, but obstruction was not preserved."
    if "regeneration_found" in tokens:
        return f"n0={n0}: debt was generated, compensated, and regenerated in a non-obstruction sentence."
    if "compensation_found" in tokens:
        return f"n0={n0}: debt was generated and locally compensated."
    if "debt_generated" in tokens:
        return f"n0={n0}: debt was generated but the native sentence remains weakly classified."
    return f"n0={n0}: no debt sentence was detected in the bounded grammar."


def extract_sentence(row: Dict[str, Any], source_version: str) -> Dict[str, Any]:
    tokens = sentence_tokens(row)
    klass = sentence_class(row, tokens)

    return {
        "version": VERSION,
        "source_version": source_version,
        "n0": row.get("n0"),
        "odd_blocks": row.get("odd_blocks"),
        "source_closure_result_type": row.get("closure_result_type"),
        "native_sentence_class": klass,
        "native_tokens": tokens,
        "native_reading": native_reading(row, tokens),
        "debt_window_count": row.get("debt_window_count", 0),
        "regeneration_count": row.get("regeneration_count", 0),
        "dangerous_regeneration_count": row.get("dangerous_regeneration_count", 0),
        "obstruction_candidate_count": row.get("obstruction_candidate_count", 0),
        "min_positive_surplus": row.get("min_positive_surplus"),
        "hardest_recovery_score": row.get("hardest_recovery_score"),
        "proof_status": "not_a_proof",
        "translation_status": "native_sentence_extraction_only",
    }


def summarize(sentences: List[Dict[str, Any]], source_version: str) -> Dict[str, Any]:
    class_counts = Counter(str(item["native_sentence_class"]) for item in sentences)
    token_counts = Counter(token for item in sentences for token in item["native_tokens"])

    obstruction_count = sum(
        int(item.get("obstruction_candidate_count", 0)) for item in sentences
    )

    dangerous_sentences = [
        item for item in sentences
        if item["native_sentence_class"] == "DANGEROUS_REGENERATION_SENTENCE"
    ]

    obstruction_sentences = [
        item for item in sentences
        if item["native_sentence_class"] == "OBSTRUCTION_CANDIDATE_SENTENCE"
    ]

    strongest_by_score = None
    scored = [
        item for item in sentences
        if item.get("hardest_recovery_score") is not None
    ]
    if scored:
        strongest_by_score = max(
            scored,
            key=lambda item: float(item.get("hardest_recovery_score") or 0.0),
        )

    tightest_by_surplus = None
    with_surplus = [
        item for item in sentences
        if item.get("min_positive_surplus") is not None
    ]
    if with_surplus:
        tightest_by_surplus = min(
            with_surplus,
            key=lambda item: float(item.get("min_positive_surplus")),
        )

    return {
        "version": VERSION,
        "layer": "native_sentence_extractor",
        "source_version": source_version,
        "sentence_count": len(sentences),
        "native_sentence_class_counts": dict(sorted(class_counts.items())),
        "native_token_counts": dict(sorted(token_counts.items())),
        "dangerous_regeneration_sentence_count": len(dangerous_sentences),
        "obstruction_candidate_sentence_count": len(obstruction_sentences),
        "obstruction_candidate_count": obstruction_count,
        "obstruction_detected": obstruction_count > 0,
        "strongest_recovery_sentence": None if strongest_by_score is None else {
            "n0": strongest_by_score["n0"],
            "native_sentence_class": strongest_by_score["native_sentence_class"],
            "hardest_recovery_score": strongest_by_score["hardest_recovery_score"],
            "native_reading": strongest_by_score["native_reading"],
        },
        "tightest_surplus_sentence": None if tightest_by_surplus is None else {
            "n0": tightest_by_surplus["n0"],
            "native_sentence_class": tightest_by_surplus["native_sentence_class"],
            "min_positive_surplus": tightest_by_surplus["min_positive_surplus"],
            "native_reading": tightest_by_surplus["native_reading"],
        },
        "primary_claim": "The extractor reads trajectory evidence as native grammar sentences, not as proof.",
        "mother_rule": "No solution before native language.",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "standard_translation_status": "deferred_after_native_sentence_extraction",
        "negative_result_boundary": "No obstruction sentence extracted in a finite source artifact is not proof that obstruction cannot exist.",
        "next_recommended_version": "v3.4 Native Sentence Atlas",
    }


def markdown_report(summary: Dict[str, Any], sentences: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Native Sentence Report")
    lines.append("")
    lines.append("Version: v3.3")
    lines.append("")
    lines.append("This report does not solve Collatz.")
    lines.append("")
    lines.append("It extracts native sentences from existing trajectory evidence.")
    lines.append("")
    lines.append("Mother rule: No solution before native language.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- source version: {summary['source_version']}")
    lines.append(f"- sentence count: {summary['sentence_count']}")
    lines.append(f"- obstruction detected: {summary['obstruction_detected']}")
    lines.append(f"- proof status: {summary['proof_status']}")
    lines.append("")
    lines.append("## Native sentence class counts")
    lines.append("")
    for key, value in summary["native_sentence_class_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Strongest recovery sentence")
    lines.append("")
    if summary["strongest_recovery_sentence"]:
        item = summary["strongest_recovery_sentence"]
        lines.append(f"- n0: {item['n0']}")
        lines.append(f"- class: {item['native_sentence_class']}")
        lines.append(f"- score: {item['hardest_recovery_score']}")
        lines.append(f"- reading: {item['native_reading']}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Tightest surplus sentence")
    lines.append("")
    if summary["tightest_surplus_sentence"]:
        item = summary["tightest_surplus_sentence"]
        lines.append(f"- n0: {item['n0']}")
        lines.append(f"- class: {item['native_sentence_class']}")
        lines.append(f"- surplus: {item['min_positive_surplus']}")
        lines.append(f"- reading: {item['native_reading']}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(summary["negative_result_boundary"])
    lines.append("")
    lines.append("## Sample native sentences")
    lines.append("")
    for item in sentences[:20]:
        lines.append(f"- {item['native_reading']}")
    lines.append("")
    return "\n".join(lines) + "\n"


def make_certificate(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_sentence_extraction_certificate",
        "source_version": summary["source_version"],
        "sentence_count": summary["sentence_count"],
        "native_sentence_class_counts": summary["native_sentence_class_counts"],
        "dangerous_regeneration_sentence_count": summary["dangerous_regeneration_sentence_count"],
        "obstruction_candidate_sentence_count": summary["obstruction_candidate_sentence_count"],
        "obstruction_candidate_count": summary["obstruction_candidate_count"],
        "obstruction_detected": summary["obstruction_detected"],
        "strongest_recovery_sentence": summary["strongest_recovery_sentence"],
        "tightest_surplus_sentence": summary["tightest_surplus_sentence"],
        "mother_rule": summary["mother_rule"],
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "standard_translation_status": "deferred_after_native_sentence_extraction",
        "negative_result_boundary": summary["negative_result_boundary"],
        "next_recommended_version": summary["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.3")
    print("=" * 80)
    print("Native Sentence Extractor")
    print("=" * 80)

    source_version, rows = load_rows()
    sentences = [extract_sentence(row, source_version) for row in rows]
    summary = summarize(sentences, source_version)
    certificate = make_certificate(summary)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with SENTENCES_PATH.open("w", encoding="utf-8") as handle:
        for sentence in sentences:
            handle.write(json.dumps(sentence, sort_keys=True) + "\n")

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(markdown_report(summary, sentences), encoding="utf-8")
    CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_version: {summary['source_version']}")
    print(f"sentence_count: {summary['sentence_count']}")
    print(f"dangerous_regeneration_sentence_count: {summary['dangerous_regeneration_sentence_count']}")
    print(f"obstruction_candidate_sentence_count: {summary['obstruction_candidate_sentence_count']}")
    print(f"obstruction_detected: {summary['obstruction_detected']}")
    print(f"proof_status: {summary['proof_status']}")
    print(f"mother_rule: {summary['mother_rule']}")
    print(f"next: {summary['next_recommended_version']}")

    if summary["strongest_recovery_sentence"]:
        item = summary["strongest_recovery_sentence"]
        print(
            "strongest recovery sentence: "
            f"n0={item['n0']} class={item['native_sentence_class']} "
            f"score={item['hardest_recovery_score']}"
        )

    if summary["tightest_surplus_sentence"]:
        item = summary["tightest_surplus_sentence"]
        print(
            "tightest surplus sentence: "
            f"n0={item['n0']} class={item['native_sentence_class']} "
            f"surplus={item['min_positive_surplus']}"
        )

    print(f"Wrote native sentences to: {SENTENCES_PATH.relative_to(ROOT)}")
    print(f"Wrote summary to: {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote report to: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
