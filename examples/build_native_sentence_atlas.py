#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v3.4

Native Sentence Atlas.

This builder reads the v3.3 native sentence extraction artifacts and builds
an atlas of the native language currently observed.

It does not solve Collatz.
It does not prove Collatz.
It does not treat termination as the primary question.

It asks:
What sentence forms does Collatz produce in the observed bounded domain?

Outputs:
- results/native_sentence_atlas.json
- results/native_sentence_atlas.md
- results/native_sentence_atlas_certificate.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "v3.4"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

SOURCE_SENTENCES_PATH = RESULTS_DIR / "native_sentences.jsonl"
SOURCE_SUMMARY_PATH = RESULTS_DIR / "native_sentence_summary.json"
SOURCE_CERTIFICATE_PATH = RESULTS_DIR / "native_sentence_certificate.json"

ATLAS_JSON_PATH = RESULTS_DIR / "native_sentence_atlas.json"
ATLAS_MD_PATH = RESULTS_DIR / "native_sentence_atlas.md"
ATLAS_CERTIFICATE_PATH = RESULTS_DIR / "native_sentence_atlas_certificate.json"


EXPECTED_SENTENCE_CLASSES = [
    "NO_DEBT_SENTENCE",
    "LOCAL_RECOVERY_SENTENCE",
    "REGENERATED_BUT_COMPENSATED_SENTENCE",
    "DANGEROUS_REGENERATION_SENTENCE",
    "OBSTRUCTION_CANDIDATE_SENTENCE",
    "UNDECIDED_SENTENCE",
]


def ensure_source_artifacts() -> None:
    if SOURCE_SENTENCES_PATH.exists() and SOURCE_SUMMARY_PATH.exists() and SOURCE_CERTIFICATE_PATH.exists():
        return

    extractor = ROOT / "examples" / "extract_native_sentences.py"
    if not extractor.exists():
        raise FileNotFoundError("Missing v3.3 native sentence extractor.")

    subprocess.run(
        [sys.executable, str(extractor)],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def first_present(row: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in row:
            return row[key]
    return default


def as_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def normalize_sentence(row: Dict[str, Any]) -> Dict[str, Any]:
    n0 = as_int(first_present(row, ["n0", "number", "start", "odd_start"], 0), 0)

    sentence_class = first_present(
        row,
        [
            "sentence_class",
            "native_sentence_class",
            "native_sentence_type",
            "closure_result_type",
            "class",
            "classification",
        ],
        "UNDECIDED_SENTENCE",
    )

    sentence_class = str(sentence_class)

    recovery_score = as_float(
        first_present(
            row,
            [
                "hardest_recovery_score",
                "recovery_score",
                "score",
                "hardness",
                "native_score",
            ],
            0.0,
        ),
        0.0,
    )

    min_surplus = as_float(
        first_present(
            row,
            [
                "min_positive_surplus",
                "tightest_positive_surplus",
                "surplus",
                "min_surplus",
            ],
            None,
        ),
        None,
    )

    debt_windows = as_int(first_present(row, ["debt_window_count", "bad_windows", "bad_window_count"], 0), 0)
    regenerations = as_int(first_present(row, ["regeneration_count", "regenerations"], 0), 0)
    dangerous_regenerations = as_int(
        first_present(row, ["dangerous_regeneration_count", "dangerous_regenerations"], 0),
        0,
    )
    obstruction_candidates = as_int(
        first_present(row, ["obstruction_candidate_count", "obstruction_candidates"], 0),
        0,
    )

    odd_blocks = as_int(first_present(row, ["odd_blocks", "odd_block_count", "trajectory_odd_blocks"], 0), 0)

    if obstruction_candidates > 0 and "OBSTRUCTION" not in sentence_class:
        sentence_class = "OBSTRUCTION_CANDIDATE_SENTENCE"

    return {
        "version": VERSION,
        "source_row_version": first_present(row, ["version"], None),
        "n0": n0,
        "sentence_class": sentence_class,
        "recovery_score": recovery_score,
        "min_positive_surplus": min_surplus,
        "debt_window_count": debt_windows,
        "regeneration_count": regenerations,
        "dangerous_regeneration_count": dangerous_regenerations,
        "obstruction_candidate_count": obstruction_candidates,
        "odd_blocks": odd_blocks,
        "source_row": row,
    }


def classify_sentence_family(sentence_class: str) -> str:
    upper = sentence_class.upper()

    if "OBSTRUCTION" in upper:
        return "obstruction_candidate_family"
    if "DANGEROUS" in upper:
        return "dangerous_regeneration_family"
    if "REGENERATED" in upper or "REGENERATION" in upper:
        return "regeneration_family"
    if "RECOVERY" in upper or "RECOVERED" in upper or "COMPENSATED" in upper:
        return "recovery_family"
    if "NO_DEBT" in upper:
        return "no_debt_family"
    if "UNDECIDED" in upper:
        return "undecided_family"

    return "unclassified_family"


def native_sentence_words(row: Dict[str, Any]) -> List[str]:
    words: List[str] = []

    if row["debt_window_count"] > 0:
        words.append("debt")
    if row["regeneration_count"] > 0:
        words.append("regeneration")
    if row["dangerous_regeneration_count"] > 0:
        words.append("dangerous_regeneration")
    if row["min_positive_surplus"] is not None:
        words.append("surplus")
    if row["obstruction_candidate_count"] > 0:
        words.append("obstruction_candidate")

    family = classify_sentence_family(row["sentence_class"])
    if family == "no_debt_family":
        words.append("no_debt")
    elif family == "recovery_family":
        words.append("local_recovery")
    elif family == "dangerous_regeneration_family":
        words.append("stress")
    elif family == "obstruction_candidate_family":
        words.append("unclosed_debt")

    if not words:
        words.append("unclassified")

    return words


def build_atlas(sentences: List[Dict[str, Any]], source_summary: Dict[str, Any], source_certificate: Dict[str, Any]) -> Dict[str, Any]:
    normalized = [normalize_sentence(row) for row in sentences]

    class_counter = Counter(row["sentence_class"] for row in normalized)
    family_counter = Counter(classify_sentence_family(row["sentence_class"]) for row in normalized)

    missing_sentence_classes = [
        name for name in EXPECTED_SENTENCE_CLASSES
        if name not in class_counter
    ]

    rows_with_score = [row for row in normalized if row["recovery_score"] is not None]
    rows_with_surplus = [row for row in normalized if row["min_positive_surplus"] is not None]

    strongest_by_recovery = sorted(
        rows_with_score,
        key=lambda row: float(row["recovery_score"] or 0.0),
        reverse=True,
    )[:10]

    tightest_by_surplus = sorted(
        rows_with_surplus,
        key=lambda row: float(row["min_positive_surplus"]),
    )[:10]

    most_debt_windows = sorted(
        normalized,
        key=lambda row: int(row["debt_window_count"]),
        reverse=True,
    )[:10]

    most_dangerous_regeneration = sorted(
        normalized,
        key=lambda row: int(row["dangerous_regeneration_count"]),
        reverse=True,
    )[:10]

    obstruction_sentences = [
        row for row in normalized
        if row["obstruction_candidate_count"] > 0
        or "OBSTRUCTION" in row["sentence_class"].upper()
    ]

    dangerous_sentences = [
        row for row in normalized
        if row["dangerous_regeneration_count"] > 0
        or "DANGEROUS" in row["sentence_class"].upper()
    ]

    word_counter = Counter()
    grammar_profiles: Dict[str, List[int]] = defaultdict(list)

    for row in normalized:
        words = native_sentence_words(row)
        for word in words:
            word_counter[word] += 1
        grammar_profiles[" ".join(words)].append(row["n0"])

    rare_profiles = [
        {
            "profile": profile,
            "count": len(n0_values),
            "sample_n0_values": n0_values[:10],
        }
        for profile, n0_values in sorted(grammar_profiles.items(), key=lambda item: (len(item[1]), item[0]))
        if len(n0_values) <= 5
    ]

    dominant_profiles = [
        {
            "profile": profile,
            "count": len(n0_values),
            "sample_n0_values": n0_values[:10],
        }
        for profile, n0_values in sorted(grammar_profiles.items(), key=lambda item: len(item[1]), reverse=True)
    ][:10]

    native_interpretation = (
        "OBSTRUCTION_SENTENCE_PRESENT"
        if obstruction_sentences
        else "DANGEROUS_SENTENCES_PRESENT_BUT_NO_OBSTRUCTION_SENTENCE"
        if dangerous_sentences
        else "NO_DANGEROUS_SENTENCE_PRESENT"
    )

    atlas = {
        "version": VERSION,
        "layer": "native_sentence_atlas",
        "source_version": source_certificate.get("version", source_summary.get("version")),
        "source_sentence_count": len(sentences),
        "sentence_count": len(normalized),
        "sentence_class_counts": dict(class_counter),
        "sentence_family_counts": dict(family_counter),
        "native_word_counts": dict(word_counter),
        "missing_sentence_classes": missing_sentence_classes,
        "obstruction_sentence_count": len(obstruction_sentences),
        "dangerous_sentence_count": len(dangerous_sentences),
        "obstruction_detected": len(obstruction_sentences) > 0,
        "native_interpretation": native_interpretation,
        "strongest_by_recovery": simplify_rows(strongest_by_recovery),
        "tightest_by_surplus": simplify_rows(tightest_by_surplus),
        "most_debt_windows": simplify_rows(most_debt_windows),
        "most_dangerous_regeneration": simplify_rows(most_dangerous_regeneration),
        "dominant_grammar_profiles": dominant_profiles,
        "rare_grammar_profiles": rare_profiles[:20],
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "central_native_question": "What sentence forms does Collatz produce before it is translated into a terminal conjecture?",
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "negative_result_boundary": "No obstruction sentence detected in this atlas is not proof that obstruction sentences cannot exist.",
        "next_recommended_version": "v3.5 Native Grammar Recurrence Map",
    }

    return atlas


def simplify_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    simplified: List[Dict[str, Any]] = []
    for row in rows:
        simplified.append(
            {
                "n0": row["n0"],
                "sentence_class": row["sentence_class"],
                "sentence_family": classify_sentence_family(row["sentence_class"]),
                "native_words": native_sentence_words(row),
                "recovery_score": row["recovery_score"],
                "min_positive_surplus": row["min_positive_surplus"],
                "debt_window_count": row["debt_window_count"],
                "regeneration_count": row["regeneration_count"],
                "dangerous_regeneration_count": row["dangerous_regeneration_count"],
                "obstruction_candidate_count": row["obstruction_candidate_count"],
                "odd_blocks": row["odd_blocks"],
            }
        )
    return simplified


def make_markdown_report(atlas: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Sentence Atlas")
    lines.append("")
    lines.append("Version: v3.4")
    lines.append("")
    lines.append("This report maps the sentence forms currently extracted from Collatz-native observations.")
    lines.append("")
    lines.append("It does not solve Collatz.")
    lines.append("")
    lines.append("It does not prove Collatz.")
    lines.append("")
    lines.append("It asks what Collatz is saying in the observed native grammar.")
    lines.append("")
    lines.append("## Core rule")
    lines.append("")
    lines.append(atlas["mother_rule"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- sentence_count: {atlas['sentence_count']}")
    lines.append(f"- dangerous_sentence_count: {atlas['dangerous_sentence_count']}")
    lines.append(f"- obstruction_sentence_count: {atlas['obstruction_sentence_count']}")
    lines.append(f"- obstruction_detected: {atlas['obstruction_detected']}")
    lines.append(f"- native_interpretation: {atlas['native_interpretation']}")
    lines.append(f"- proof_status: {atlas['proof_status']}")
    lines.append("")
    lines.append("## Sentence class counts")
    lines.append("")
    for key, value in sorted(atlas["sentence_class_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Sentence family counts")
    lines.append("")
    for key, value in sorted(atlas["sentence_family_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Native word counts")
    lines.append("")
    for key, value in sorted(atlas["native_word_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Strongest recovery-stress sentences")
    lines.append("")
    for item in atlas["strongest_by_recovery"][:10]:
        lines.append(
            f"- n0={item['n0']} class={item['sentence_class']} "
            f"score={item['recovery_score']} surplus={item['min_positive_surplus']}"
        )
    lines.append("")
    lines.append("## Tightest surplus sentences")
    lines.append("")
    for item in atlas["tightest_by_surplus"][:10]:
        lines.append(
            f"- n0={item['n0']} class={item['sentence_class']} "
            f"surplus={item['min_positive_surplus']} score={item['recovery_score']}"
        )
    lines.append("")
    lines.append("## Dominant grammar profiles")
    lines.append("")
    for item in atlas["dominant_grammar_profiles"]:
        lines.append(
            f"- profile={item['profile']} count={item['count']} "
            f"sample={item['sample_n0_values']}"
        )
    lines.append("")
    lines.append("## Rare grammar profiles")
    lines.append("")
    for item in atlas["rare_grammar_profiles"][:20]:
        lines.append(
            f"- profile={item['profile']} count={item['count']} "
            f"sample={item['sample_n0_values']}"
        )
    lines.append("")
    lines.append("## Negative result boundary")
    lines.append("")
    lines.append(atlas["negative_result_boundary"])
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(atlas["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(atlas: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_sentence_atlas_certificate",
        "source_version": atlas["source_version"],
        "sentence_count": atlas["sentence_count"],
        "dangerous_sentence_count": atlas["dangerous_sentence_count"],
        "obstruction_sentence_count": atlas["obstruction_sentence_count"],
        "obstruction_detected": atlas["obstruction_detected"],
        "native_interpretation": atlas["native_interpretation"],
        "missing_sentence_classes": atlas["missing_sentence_classes"],
        "mother_rule": atlas["mother_rule"],
        "central_native_question": atlas["central_native_question"],
        "proof_status": atlas["proof_status"],
        "theorem_status": atlas["theorem_status"],
        "negative_result_boundary": atlas["negative_result_boundary"],
        "next_recommended_version": atlas["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v3.4")
    print("=" * 80)
    print("Native Sentence Atlas")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ensure_source_artifacts()

    sentences = read_jsonl(SOURCE_SENTENCES_PATH)
    source_summary = read_json(SOURCE_SUMMARY_PATH)
    source_certificate = read_json(SOURCE_CERTIFICATE_PATH)

    atlas = build_atlas(sentences, source_summary, source_certificate)
    certificate = make_certificate(atlas)
    markdown = make_markdown_report(atlas)

    ATLAS_JSON_PATH.write_text(json.dumps(atlas, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ATLAS_MD_PATH.write_text(markdown + "\n", encoding="utf-8")
    ATLAS_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"source_version: {atlas['source_version']}")
    print(f"sentence_count: {atlas['sentence_count']}")
    print(f"dangerous_sentence_count: {atlas['dangerous_sentence_count']}")
    print(f"obstruction_sentence_count: {atlas['obstruction_sentence_count']}")
    print(f"obstruction_detected: {atlas['obstruction_detected']}")
    print(f"native_interpretation: {atlas['native_interpretation']}")
    print(f"proof_status: {atlas['proof_status']}")
    print(f"mother_rule: {atlas['mother_rule']}")
    print(f"next: {atlas['next_recommended_version']}")

    if atlas["strongest_by_recovery"]:
        strongest = atlas["strongest_by_recovery"][0]
        print(
            "strongest sentence: "
            f"n0={strongest['n0']} class={strongest['sentence_class']} "
            f"score={strongest['recovery_score']}"
        )

    if atlas["tightest_by_surplus"]:
        tightest = atlas["tightest_by_surplus"][0]
        print(
            "tightest surplus sentence: "
            f"n0={tightest['n0']} class={tightest['sentence_class']} "
            f"surplus={tightest['min_positive_surplus']}"
        )

    print(f"Wrote atlas JSON to: {ATLAS_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote atlas Markdown to: {ATLAS_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {ATLAS_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
