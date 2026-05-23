#!/usr/bin/env python3
"""
COLLATZ-NATIVE-MATH v4.2

Native Language Index.

This builder creates a navigation index organized by native-language role.

It does not add theory.
It does not solve Collatz.
It does not prove Collatz.
It does not claim global closure or global invariance.

Outputs:
- results/native_language_index.json
- results/native_language_index.md
- results/native_language_index_certificate.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


VERSION = "v4.2"
ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

INDEX_JSON_PATH = RESULTS_DIR / "native_language_index.json"
INDEX_MD_PATH = RESULTS_DIR / "native_language_index.md"
INDEX_CERTIFICATE_PATH = RESULTS_DIR / "native_language_index_certificate.json"


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def item(path: str, role: str, description: str, required: bool = True) -> Dict[str, Any]:
    return {
        "path": path,
        "role": role,
        "description": description,
        "exists": exists(path),
        "required": required,
    }


def build_sections() -> List[Dict[str, Any]]:
    return [
        {
            "section_id": "entry_point",
            "title": "Entry Point",
            "native_role": "reader_orientation",
            "items": [
                item("README.md", "main_entry", "Primary public entry point."),
                item("START_HERE.md", "reading_order", "Recommended starting order."),
                item("CRC_CONJECTURE.md", "corrected_framing", "Native Collatz framing."),
                item("docs/README_CONSOLIDATION_V41.md", "entry_consolidation", "v4.1 entry correction."),
                item("docs/ENTRY_POINT_BOUNDARY.md", "entry_boundary", "Prevents solution-first framing."),
                item("docs/PUBLIC_REPO_POSITIONING.md", "public_positioning", "Public description boundary."),
            ],
        },
        {
            "section_id": "native_language_summary",
            "title": "Native Language Summary",
            "native_role": "route_summary",
            "items": [
                item("docs/NATIVE_LANGUAGE_SUMMARY.md", "summary", "v4.0 native language summary."),
                item("docs/NATIVE_LANGUAGE_ROUTE.md", "route", "v3.1 to v3.9 route."),
                item("docs/WHAT_COLLATZ_HAS_SAID.md", "observations", "Bounded native observations."),
                item("docs/NATIVE_LANGUAGE_BOUNDARY.md", "boundary", "Native-language boundary."),
                item("docs/V40_PUBLIC_POSITIONING.md", "positioning", "Public positioning from v4.0."),
                item("results/native_language_summary.json", "summary_artifact", "Machine-readable v4.0 summary."),
                item("results/native_language_summary.md", "summary_report", "Human-readable v4.0 summary."),
                item("results/native_language_summary_certificate.json", "summary_certificate", "v4.0 certificate."),
            ],
        },
        {
            "section_id": "grammar",
            "title": "Native Grammar",
            "native_role": "grammar_definition",
            "items": [
                item("docs/NATIVE_GRAMMAR_MAP.md", "grammar_map", "Native grammar map."),
                item("docs/NATIVE_GRAMMAR_OBJECTS.md", "grammar_objects", "Native grammar objects."),
                item("docs/NATIVE_GRAMMAR_TRANSITIONS.md", "grammar_transitions", "Native grammar transitions."),
                item("docs/NATIVE_GRAMMAR_SEQUENCES.md", "grammar_sequences", "Native grammar sequences."),
                item("docs/GRAMMAR_PROBE_RECLASSIFICATION.md", "probe_reclassification", "Reclassifies scans as grammar probes."),
                item("docs/NATIVE_GRAMMAR_FORBIDDEN_TRANSLATIONS.md", "forbidden_translations", "Forbidden premature translations."),
                item("results/native_grammar_map_manifest.json", "grammar_manifest", "v3.2 grammar manifest."),
            ],
        },
        {
            "section_id": "sentences",
            "title": "Native Sentences",
            "native_role": "trajectory_as_language",
            "items": [
                item("examples/extract_native_sentences.py", "sentence_extractor", "Builds native sentence artifacts."),
                item("docs/NATIVE_SENTENCE_EXTRACTOR.md", "sentence_extractor_doc", "Explains extraction."),
                item("docs/NATIVE_SENTENCE_TYPES.md", "sentence_types", "Native sentence types."),
                item("docs/TRAJECTORY_AS_NATIVE_UTTERANCE.md", "trajectory_utterance", "Trajectory as native utterance."),
                item("docs/SENTENCE_EXTRACTION_BOUNDARY.md", "sentence_boundary", "Extraction boundary."),
                item("results/native_sentences.jsonl", "sentence_rows", "Native sentence rows."),
                item("results/native_sentence_summary.json", "sentence_summary", "Native sentence summary."),
                item("results/native_sentence_report.md", "sentence_report", "Native sentence report."),
                item("results/native_sentence_certificate.json", "sentence_certificate", "Native sentence certificate."),
            ],
        },
        {
            "section_id": "sentence_atlas",
            "title": "Native Sentence Atlas",
            "native_role": "sentence_family_mapping",
            "items": [
                item("examples/build_native_sentence_atlas.py", "atlas_builder", "Builds native sentence atlas."),
                item("docs/NATIVE_SENTENCE_ATLAS.md", "atlas_doc", "Native sentence atlas."),
                item("docs/NATIVE_SENTENCE_FAMILIES.md", "sentence_families", "Sentence families."),
                item("docs/NATIVE_SENTENCE_ATLAS_INTERPRETATION.md", "atlas_interpretation", "Atlas interpretation."),
                item("docs/RARE_NATIVE_SENTENCES.md", "rare_sentences", "Rare native sentences."),
                item("docs/DANGEROUS_SENTENCE_ATLAS.md", "dangerous_sentences", "Dangerous sentence atlas."),
                item("results/native_sentence_atlas.json", "atlas_json", "Atlas JSON."),
                item("results/native_sentence_atlas.md", "atlas_md", "Atlas Markdown."),
                item("results/native_sentence_atlas_certificate.json", "atlas_certificate", "Atlas certificate."),
            ],
        },
        {
            "section_id": "recurrence",
            "title": "Native Grammar Recurrence",
            "native_role": "what_returns",
            "items": [
                item("examples/build_native_grammar_recurrence_map.py", "recurrence_builder", "Builds recurrence map."),
                item("docs/NATIVE_GRAMMAR_RECURRENCE_MAP.md", "recurrence_map", "Native recurrence map."),
                item("docs/RECURRENCE_AS_NATIVE_BEHAVIOR.md", "recurrence_behavior", "Recurrence as native behavior."),
                item("docs/DANGEROUS_RECURRENCE.md", "dangerous_recurrence", "Dangerous recurrence."),
                item("docs/GRAMMAR_MUTATION_TYPES.md", "mutation_types_bridge", "Mutation types bridge."),
                item("results/native_grammar_recurrence_map.json", "recurrence_json", "Recurrence map JSON."),
                item("results/native_grammar_recurrence_map.md", "recurrence_md", "Recurrence map Markdown."),
                item("results/native_grammar_recurrence_certificate.json", "recurrence_certificate", "Recurrence certificate."),
            ],
        },
        {
            "section_id": "mutation",
            "title": "Native Grammar Mutation",
            "native_role": "what_changes",
            "items": [
                item("examples/build_native_grammar_mutation_atlas.py", "mutation_builder", "Builds mutation atlas."),
                item("docs/NATIVE_GRAMMAR_MUTATION_ATLAS.md", "mutation_atlas", "Native mutation atlas."),
                item("docs/MUTATION_AS_NATIVE_GRAMMAR.md", "mutation_behavior", "Mutation as native grammar."),
                item("docs/DANGEROUS_TO_RECOVERY_MUTATIONS.md", "danger_to_recovery", "Danger-to-recovery mutations."),
                item("docs/DANGEROUS_PERSISTENCE_MUTATIONS.md", "dangerous_persistence", "Dangerous persistence mutations."),
                item("docs/MUTATION_AROUND_9780657630.md", "stress_node_mutation", "Mutation around 9780657630."),
                item("results/native_grammar_mutation_atlas.json", "mutation_json", "Mutation atlas JSON."),
                item("results/native_grammar_mutation_atlas.md", "mutation_md", "Mutation atlas Markdown."),
                item("results/native_grammar_mutation_certificate.json", "mutation_certificate", "Mutation certificate."),
            ],
        },
        {
            "section_id": "stability",
            "title": "Native Grammar Stability",
            "native_role": "what_resists_change",
            "items": [
                item("examples/build_native_grammar_stability_map.py", "stability_builder", "Builds stability map."),
                item("docs/NATIVE_GRAMMAR_STABILITY_MAP.md", "stability_map", "Native stability map."),
                item("docs/STABILITY_AS_NATIVE_BEHAVIOR.md", "stability_behavior", "Stability as native behavior."),
                item("docs/DANGEROUS_STABILITY.md", "dangerous_stability", "Dangerous stability."),
                item("docs/DANGEROUS_INSTABILITY.md", "dangerous_instability", "Dangerous instability."),
                item("docs/STABILITY_AROUND_9780657630.md", "stress_node_stability", "Stability around 9780657630."),
                item("results/native_grammar_stability_map.json", "stability_json", "Stability map JSON."),
                item("results/native_grammar_stability_map.md", "stability_md", "Stability map Markdown."),
                item("results/native_grammar_stability_certificate.json", "stability_certificate", "Stability certificate."),
            ],
        },
        {
            "section_id": "conservation",
            "title": "Native Conservation",
            "native_role": "what_remains_through_change",
            "items": [
                item("examples/build_native_conservation_map.py", "conservation_builder", "Builds conservation map."),
                item("docs/NATIVE_CONSERVATION_MAP.md", "conservation_map", "Native conservation map."),
                item("docs/CONSERVATION_AS_NATIVE_BEHAVIOR.md", "conservation_behavior", "Conservation as native behavior."),
                item("docs/CONSERVATION_OF_DANGER_RELEASE.md", "danger_release_conservation", "Conservation of danger-release."),
                item("docs/CONSERVATION_OF_INSTABILITY.md", "instability_conservation", "Conservation of instability."),
                item("docs/CONSERVATION_AROUND_9780657630.md", "stress_node_conservation", "Conservation around 9780657630."),
                item("results/native_conservation_map.json", "conservation_json", "Conservation map JSON."),
                item("results/native_conservation_map.md", "conservation_md", "Conservation map Markdown."),
                item("results/native_conservation_certificate.json", "conservation_certificate", "Conservation certificate."),
            ],
        },
        {
            "section_id": "invariant_candidates",
            "title": "Native Invariant Candidates",
            "native_role": "what_may_remain_under_repeated_native_tests",
            "items": [
                item("examples/build_native_invariant_candidate_map.py", "invariant_builder", "Builds invariant candidate map."),
                item("docs/NATIVE_INVARIANT_CANDIDATE_MAP.md", "invariant_map", "Native invariant candidate map."),
                item("docs/INVARIANT_CANDIDATE_BOUNDARY.md", "invariant_boundary", "Invariant candidate boundary."),
                item("docs/DANGER_RELEASE_INVARIANT_CANDIDATES.md", "danger_release_candidates", "Danger-release invariant candidates."),
                item("docs/DANGEROUS_STABILITY_INVARIANT_CANDIDATES.md", "dangerous_stability_candidates", "Dangerous-stability invariant candidates."),
                item("docs/OBSTRUCTION_RELEVANT_INVARIANT_CANDIDATES.md", "obstruction_relevant_candidates", "Obstruction-relevant invariant candidates."),
                item("docs/INVARIANT_CANDIDATES_AROUND_9780657630.md", "stress_node_invariant", "Invariant candidates around 9780657630."),
                item("results/native_invariant_candidate_map.json", "invariant_json", "Invariant candidate map JSON."),
                item("results/native_invariant_candidate_map.md", "invariant_md", "Invariant candidate map Markdown."),
                item("results/native_invariant_candidate_certificate.json", "invariant_certificate", "Invariant candidate certificate."),
            ],
        },
        {
            "section_id": "earlier_native_boundary",
            "title": "Earlier Native Boundary Layers",
            "native_role": "method_boundary",
            "items": [
                item("docs/NATIVE_METHOD.md", "native_method", "Native method boundary."),
                item("docs/STANDARD_TRANSLATION_BOUNDARY.md", "translation_boundary", "Standard translation boundary."),
                item("docs/NATIVE_OBJECTS.md", "native_objects", "Native object list."),
                item("docs/NATIVE_RESEARCH_PROGRAM.md", "research_program", "Native research program."),
                item("docs/EVIDENCE_LAYER_STATUS.md", "evidence_status", "Evidence layer status."),
                item("docs/NATIVE_OBSTRUCTION_MODEL.md", "obstruction_model", "Native obstruction model."),
                item("docs/NATIVE_CLOSURE_CONDITIONS.md", "closure_conditions", "Native closure conditions."),
                item("docs/NATIVE_LANGUAGE_INVERSION.md", "language_inversion", "Native language inversion."),
                item("docs/NO_SOLVING_POSTURE.md", "no_solving_posture", "No solving posture."),
                item("docs/COLLATZ_AS_NATIVE_LANGUAGE.md", "collatz_as_language", "Collatz as native language."),
            ],
        },
        {
            "section_id": "latest_tests",
            "title": "Latest Tests",
            "native_role": "regression_safety",
            "items": [
                item("tests/test_readme_consolidation_v41.py", "v41_tests", "README consolidation tests."),
                item("tests/test_native_language_summary.py", "v40_tests", "Native language summary tests."),
                item("tests/test_native_invariant_candidate_map.py", "v39_tests", "Invariant candidate map tests."),
                item("tests/test_native_conservation_map.py", "v38_tests", "Conservation map tests."),
                item("tests/test_native_grammar_stability_map.py", "v37_tests", "Stability map tests."),
                item("tests/test_native_grammar_mutation_atlas.py", "v36_tests", "Mutation atlas tests."),
                item("tests/test_native_grammar_recurrence_map.py", "v35_tests", "Recurrence map tests."),
            ],
        },
    ]


def build_index() -> Dict[str, Any]:
    sections = build_sections()

    total_items = 0
    existing_items = 0
    missing_required: List[Dict[str, Any]] = []

    for section in sections:
        for current in section["items"]:
            total_items += 1
            if current["exists"]:
                existing_items += 1
            elif current["required"]:
                missing_required.append(
                    {
                        "section_id": section["section_id"],
                        "path": current["path"],
                        "role": current["role"],
                    }
                )

    return {
        "version": VERSION,
        "layer": "native_language_index",
        "status": "navigation_index_defined",
        "mother_rule": "No solution before native language.",
        "secondary_rule": "No proof before native description.",
        "primary_position": "A native structural reading of the Collatz dynamics.",
        "section_count": len(sections),
        "total_indexed_items": total_items,
        "existing_indexed_items": existing_items,
        "missing_required_count": len(missing_required),
        "missing_required_items": missing_required,
        "sections": sections,
        "proof_status": "not_a_proof",
        "theorem_status": "no_theorems_introduced",
        "collatz_status": "not_claimed_solved",
        "global_closure_status": "not_claimed",
        "global_invariant_status": "not_claimed",
        "next_recommended_version": "v4.3 Native Artifact Consistency Audit",
    }


def make_markdown(index: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Native Language Index")
    lines.append("")
    lines.append("Version: v4.2")
    lines.append("")
    lines.append(index["primary_position"])
    lines.append("")
    lines.append("Core rule:")
    lines.append("")
    lines.append("    No solution before native language.")
    lines.append("")
    lines.append("Boundary:")
    lines.append("")
    lines.append("    proof_status: not_a_proof")
    lines.append("    theorem_status: no_theorems_introduced")
    lines.append("    collatz_status: not_claimed_solved")
    lines.append("    global_closure_status: not_claimed")
    lines.append("    global_invariant_status: not_claimed")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- section_count: {index['section_count']}")
    lines.append(f"- total_indexed_items: {index['total_indexed_items']}")
    lines.append(f"- existing_indexed_items: {index['existing_indexed_items']}")
    lines.append(f"- missing_required_count: {index['missing_required_count']}")
    lines.append("")
    lines.append("## Sections")
    lines.append("")

    for section in index["sections"]:
        lines.append(f"### {section['title']}")
        lines.append("")
        lines.append(f"native_role: {section['native_role']}")
        lines.append("")
        for current in section["items"]:
            mark = "OK" if current["exists"] else "MISSING"
            lines.append(f"- {mark} | {current['path']} | {current['role']} | {current['description']}")
        lines.append("")

    lines.append("## Missing required items")
    lines.append("")

    if not index["missing_required_items"]:
        lines.append("- none")
    else:
        for current in index["missing_required_items"]:
            lines.append(f"- {current['section_id']} | {current['path']} | {current['role']}")

    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append(index["next_recommended_version"])
    lines.append("")

    return "\n".join(lines)


def make_certificate(index: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": VERSION,
        "certificate_type": "native_language_index_certificate",
        "section_count": index["section_count"],
        "total_indexed_items": index["total_indexed_items"],
        "existing_indexed_items": index["existing_indexed_items"],
        "missing_required_count": index["missing_required_count"],
        "mother_rule": index["mother_rule"],
        "secondary_rule": index["secondary_rule"],
        "primary_position": index["primary_position"],
        "proof_status": index["proof_status"],
        "theorem_status": index["theorem_status"],
        "collatz_status": index["collatz_status"],
        "global_closure_status": index["global_closure_status"],
        "global_invariant_status": index["global_invariant_status"],
        "next_recommended_version": index["next_recommended_version"],
    }


def main() -> None:
    print("=" * 80)
    print("COLLATZ-NATIVE-MATH v4.2")
    print("=" * 80)
    print("Native Language Index")
    print("=" * 80)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    index = build_index()
    report = make_markdown(index)
    certificate = make_certificate(index)

    INDEX_JSON_PATH.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    INDEX_MD_PATH.write_text(report + "\n", encoding="utf-8")
    INDEX_CERTIFICATE_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"section_count: {index['section_count']}")
    print(f"total_indexed_items: {index['total_indexed_items']}")
    print(f"existing_indexed_items: {index['existing_indexed_items']}")
    print(f"missing_required_count: {index['missing_required_count']}")
    print(f"proof_status: {index['proof_status']}")
    print(f"collatz_status: {index['collatz_status']}")
    print(f"mother_rule: {index['mother_rule']}")
    print(f"next: {index['next_recommended_version']}")
    print(f"Wrote index JSON to: {INDEX_JSON_PATH.relative_to(ROOT)}")
    print(f"Wrote index Markdown to: {INDEX_MD_PATH.relative_to(ROOT)}")
    print(f"Wrote certificate to: {INDEX_CERTIFICATE_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
