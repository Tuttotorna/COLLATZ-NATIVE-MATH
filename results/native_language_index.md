# Native Language Index

Version: v4.2

A native structural reading of the Collatz dynamics.

Core rule:

    No solution before native language.

Boundary:

    proof_status: not_a_proof
    theorem_status: no_theorems_introduced
    collatz_status: not_claimed_solved
    global_closure_status: not_claimed
    global_invariant_status: not_claimed

## Summary

- section_count: 12
- total_indexed_items: 101
- existing_indexed_items: 101
- missing_required_count: 0

## Sections

### Entry Point

native_role: reader_orientation

- OK | README.md | main_entry | Primary public entry point.
- OK | START_HERE.md | reading_order | Recommended starting order.
- OK | CRC_CONJECTURE.md | corrected_framing | Native Collatz framing.
- OK | docs/README_CONSOLIDATION_V41.md | entry_consolidation | v4.1 entry correction.
- OK | docs/ENTRY_POINT_BOUNDARY.md | entry_boundary | Prevents solution-first framing.
- OK | docs/PUBLIC_REPO_POSITIONING.md | public_positioning | Public description boundary.

### Native Language Summary

native_role: route_summary

- OK | docs/NATIVE_LANGUAGE_SUMMARY.md | summary | v4.0 native language summary.
- OK | docs/NATIVE_LANGUAGE_ROUTE.md | route | v3.1 to v3.9 route.
- OK | docs/WHAT_COLLATZ_HAS_SAID.md | observations | Bounded native observations.
- OK | docs/NATIVE_LANGUAGE_BOUNDARY.md | boundary | Native-language boundary.
- OK | docs/V40_PUBLIC_POSITIONING.md | positioning | Public positioning from v4.0.
- OK | results/native_language_summary.json | summary_artifact | Machine-readable v4.0 summary.
- OK | results/native_language_summary.md | summary_report | Human-readable v4.0 summary.
- OK | results/native_language_summary_certificate.json | summary_certificate | v4.0 certificate.

### Native Grammar

native_role: grammar_definition

- OK | docs/NATIVE_GRAMMAR_MAP.md | grammar_map | Native grammar map.
- OK | docs/NATIVE_GRAMMAR_OBJECTS.md | grammar_objects | Native grammar objects.
- OK | docs/NATIVE_GRAMMAR_TRANSITIONS.md | grammar_transitions | Native grammar transitions.
- OK | docs/NATIVE_GRAMMAR_SEQUENCES.md | grammar_sequences | Native grammar sequences.
- OK | docs/GRAMMAR_PROBE_RECLASSIFICATION.md | probe_reclassification | Reclassifies scans as grammar probes.
- OK | docs/NATIVE_GRAMMAR_FORBIDDEN_TRANSLATIONS.md | forbidden_translations | Forbidden premature translations.
- OK | results/native_grammar_map_manifest.json | grammar_manifest | v3.2 grammar manifest.

### Native Sentences

native_role: trajectory_as_language

- OK | examples/extract_native_sentences.py | sentence_extractor | Builds native sentence artifacts.
- OK | docs/NATIVE_SENTENCE_EXTRACTOR.md | sentence_extractor_doc | Explains extraction.
- OK | docs/NATIVE_SENTENCE_TYPES.md | sentence_types | Native sentence types.
- OK | docs/TRAJECTORY_AS_NATIVE_UTTERANCE.md | trajectory_utterance | Trajectory as native utterance.
- OK | docs/SENTENCE_EXTRACTION_BOUNDARY.md | sentence_boundary | Extraction boundary.
- OK | results/native_sentences.jsonl | sentence_rows | Native sentence rows.
- OK | results/native_sentence_summary.json | sentence_summary | Native sentence summary.
- OK | results/native_sentence_report.md | sentence_report | Native sentence report.
- OK | results/native_sentence_certificate.json | sentence_certificate | Native sentence certificate.

### Native Sentence Atlas

native_role: sentence_family_mapping

- OK | examples/build_native_sentence_atlas.py | atlas_builder | Builds native sentence atlas.
- OK | docs/NATIVE_SENTENCE_ATLAS.md | atlas_doc | Native sentence atlas.
- OK | docs/NATIVE_SENTENCE_FAMILIES.md | sentence_families | Sentence families.
- OK | docs/NATIVE_SENTENCE_ATLAS_INTERPRETATION.md | atlas_interpretation | Atlas interpretation.
- OK | docs/RARE_NATIVE_SENTENCES.md | rare_sentences | Rare native sentences.
- OK | docs/DANGEROUS_SENTENCE_ATLAS.md | dangerous_sentences | Dangerous sentence atlas.
- OK | results/native_sentence_atlas.json | atlas_json | Atlas JSON.
- OK | results/native_sentence_atlas.md | atlas_md | Atlas Markdown.
- OK | results/native_sentence_atlas_certificate.json | atlas_certificate | Atlas certificate.

### Native Grammar Recurrence

native_role: what_returns

- OK | examples/build_native_grammar_recurrence_map.py | recurrence_builder | Builds recurrence map.
- OK | docs/NATIVE_GRAMMAR_RECURRENCE_MAP.md | recurrence_map | Native recurrence map.
- OK | docs/RECURRENCE_AS_NATIVE_BEHAVIOR.md | recurrence_behavior | Recurrence as native behavior.
- OK | docs/DANGEROUS_RECURRENCE.md | dangerous_recurrence | Dangerous recurrence.
- OK | docs/GRAMMAR_MUTATION_TYPES.md | mutation_types_bridge | Mutation types bridge.
- OK | results/native_grammar_recurrence_map.json | recurrence_json | Recurrence map JSON.
- OK | results/native_grammar_recurrence_map.md | recurrence_md | Recurrence map Markdown.
- OK | results/native_grammar_recurrence_certificate.json | recurrence_certificate | Recurrence certificate.

### Native Grammar Mutation

native_role: what_changes

- OK | examples/build_native_grammar_mutation_atlas.py | mutation_builder | Builds mutation atlas.
- OK | docs/NATIVE_GRAMMAR_MUTATION_ATLAS.md | mutation_atlas | Native mutation atlas.
- OK | docs/MUTATION_AS_NATIVE_GRAMMAR.md | mutation_behavior | Mutation as native grammar.
- OK | docs/DANGEROUS_TO_RECOVERY_MUTATIONS.md | danger_to_recovery | Danger-to-recovery mutations.
- OK | docs/DANGEROUS_PERSISTENCE_MUTATIONS.md | dangerous_persistence | Dangerous persistence mutations.
- OK | docs/MUTATION_AROUND_9780657630.md | stress_node_mutation | Mutation around 9780657630.
- OK | results/native_grammar_mutation_atlas.json | mutation_json | Mutation atlas JSON.
- OK | results/native_grammar_mutation_atlas.md | mutation_md | Mutation atlas Markdown.
- OK | results/native_grammar_mutation_certificate.json | mutation_certificate | Mutation certificate.

### Native Grammar Stability

native_role: what_resists_change

- OK | examples/build_native_grammar_stability_map.py | stability_builder | Builds stability map.
- OK | docs/NATIVE_GRAMMAR_STABILITY_MAP.md | stability_map | Native stability map.
- OK | docs/STABILITY_AS_NATIVE_BEHAVIOR.md | stability_behavior | Stability as native behavior.
- OK | docs/DANGEROUS_STABILITY.md | dangerous_stability | Dangerous stability.
- OK | docs/DANGEROUS_INSTABILITY.md | dangerous_instability | Dangerous instability.
- OK | docs/STABILITY_AROUND_9780657630.md | stress_node_stability | Stability around 9780657630.
- OK | results/native_grammar_stability_map.json | stability_json | Stability map JSON.
- OK | results/native_grammar_stability_map.md | stability_md | Stability map Markdown.
- OK | results/native_grammar_stability_certificate.json | stability_certificate | Stability certificate.

### Native Conservation

native_role: what_remains_through_change

- OK | examples/build_native_conservation_map.py | conservation_builder | Builds conservation map.
- OK | docs/NATIVE_CONSERVATION_MAP.md | conservation_map | Native conservation map.
- OK | docs/CONSERVATION_AS_NATIVE_BEHAVIOR.md | conservation_behavior | Conservation as native behavior.
- OK | docs/CONSERVATION_OF_DANGER_RELEASE.md | danger_release_conservation | Conservation of danger-release.
- OK | docs/CONSERVATION_OF_INSTABILITY.md | instability_conservation | Conservation of instability.
- OK | docs/CONSERVATION_AROUND_9780657630.md | stress_node_conservation | Conservation around 9780657630.
- OK | results/native_conservation_map.json | conservation_json | Conservation map JSON.
- OK | results/native_conservation_map.md | conservation_md | Conservation map Markdown.
- OK | results/native_conservation_certificate.json | conservation_certificate | Conservation certificate.

### Native Invariant Candidates

native_role: what_may_remain_under_repeated_native_tests

- OK | examples/build_native_invariant_candidate_map.py | invariant_builder | Builds invariant candidate map.
- OK | docs/NATIVE_INVARIANT_CANDIDATE_MAP.md | invariant_map | Native invariant candidate map.
- OK | docs/INVARIANT_CANDIDATE_BOUNDARY.md | invariant_boundary | Invariant candidate boundary.
- OK | docs/DANGER_RELEASE_INVARIANT_CANDIDATES.md | danger_release_candidates | Danger-release invariant candidates.
- OK | docs/DANGEROUS_STABILITY_INVARIANT_CANDIDATES.md | dangerous_stability_candidates | Dangerous-stability invariant candidates.
- OK | docs/OBSTRUCTION_RELEVANT_INVARIANT_CANDIDATES.md | obstruction_relevant_candidates | Obstruction-relevant invariant candidates.
- OK | docs/INVARIANT_CANDIDATES_AROUND_9780657630.md | stress_node_invariant | Invariant candidates around 9780657630.
- OK | results/native_invariant_candidate_map.json | invariant_json | Invariant candidate map JSON.
- OK | results/native_invariant_candidate_map.md | invariant_md | Invariant candidate map Markdown.
- OK | results/native_invariant_candidate_certificate.json | invariant_certificate | Invariant candidate certificate.

### Earlier Native Boundary Layers

native_role: method_boundary

- OK | docs/NATIVE_METHOD.md | native_method | Native method boundary.
- OK | docs/STANDARD_TRANSLATION_BOUNDARY.md | translation_boundary | Standard translation boundary.
- OK | docs/NATIVE_OBJECTS.md | native_objects | Native object list.
- OK | docs/NATIVE_RESEARCH_PROGRAM.md | research_program | Native research program.
- OK | docs/EVIDENCE_LAYER_STATUS.md | evidence_status | Evidence layer status.
- OK | docs/NATIVE_OBSTRUCTION_MODEL.md | obstruction_model | Native obstruction model.
- OK | docs/NATIVE_CLOSURE_CONDITIONS.md | closure_conditions | Native closure conditions.
- OK | docs/NATIVE_LANGUAGE_INVERSION.md | language_inversion | Native language inversion.
- OK | docs/NO_SOLVING_POSTURE.md | no_solving_posture | No solving posture.
- OK | docs/COLLATZ_AS_NATIVE_LANGUAGE.md | collatz_as_language | Collatz as native language.

### Latest Tests

native_role: regression_safety

- OK | tests/test_readme_consolidation_v41.py | v41_tests | README consolidation tests.
- OK | tests/test_native_language_summary.py | v40_tests | Native language summary tests.
- OK | tests/test_native_invariant_candidate_map.py | v39_tests | Invariant candidate map tests.
- OK | tests/test_native_conservation_map.py | v38_tests | Conservation map tests.
- OK | tests/test_native_grammar_stability_map.py | v37_tests | Stability map tests.
- OK | tests/test_native_grammar_mutation_atlas.py | v36_tests | Mutation atlas tests.
- OK | tests/test_native_grammar_recurrence_map.py | v35_tests | Recurrence map tests.

## Missing required items

- none

## Next

v4.3 Native Artifact Consistency Audit

