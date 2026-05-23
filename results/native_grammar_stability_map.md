# Native Grammar Stability Map

Version: v3.7

This report studies what Collatz preserves in its own grammar.

It does not solve Collatz.

It does not prove Collatz.

It asks what remains stable under recurrence and mutation.

## Core rule

No solution before native language.

## Central native question

What does Collatz preserve under recurrence and mutation?

## Summary

- source_mutation_version: v3.6
- source_mutation_edge_count: 50
- stability_edge_count: 45
- stable_edge_count: 8
- unstable_edge_count: 37
- dangerous_stable_edge_count: 0
- dangerous_unstable_edge_count: 37
- release_edge_count: 28
- obstruction_relevant_edge_count: 0
- obstruction_detected: False
- stability_score: 0.17777777777777778
- release_score: 0.6222222222222222
- dangerous_instability_score: 1.0
- native_interpretation: DANGEROUS_GRAMMAR_APPEARS_UNSTABLE_IN_THIS_ATLAS
- proof_status: not_a_proof

## Stability type counts

- class_stable: 8
- dangerous_unstable_release: 28
- toward_dangerous_transition: 9

## Strong node profiles

- n0=9780657630 role=release_node out=5 in=6 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=9780657631 role=release_node out=5 in=4 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=9780657622 role=transition_node out=1 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657629 role=transition_node out=2 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657626 role=transition_node out=2 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657628 role=transition_node out=2 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657625 role=transition_node out=1 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657623 role=transition_node out=1 in=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657627 role=stable_node out=1 in=0 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=626331 role=release_node out=1 in=0 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=131071 role=release_node out=1 in=0 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=837799 role=stable_node out=1 in=0 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=837791 role=stable_node out=1 in=0 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=837806 role=stable_node out=1 in=0 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=837807 role=stable_node out=1 in=1 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=4099 role=release_node out=1 in=1 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=77031 role=release_node out=1 in=0 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=77039 role=release_node out=1 in=0 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=63 role=release_node out=1 in=1 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=626327 role=release_node out=1 in=1 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0

## Dangerous unstable edges

- 9780657630 -> 9780657633 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657631 -> 9780657633 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657622 -> 9780657630 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657630 -> 9780657638 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657629 -> 9780657630 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657630 -> 9780657634 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657626 -> 9780657630 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657630 -> 9780657635 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657625 -> 9780657630 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657628 -> 9780657630 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657630 -> 9780657632 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657623 -> 9780657631 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657629 -> 9780657631 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657631 -> 9780657634 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657626 -> 9780657631 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657631 -> 9780657635 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657628 -> 9780657631 REGENERATION_COMPENSATION_SENTENCE -> DANGEROUS_REGENERATION_SENTENCE type=toward_dangerous_transition
- 9780657631 -> 9780657636 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 9780657631 -> 9780657632 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release
- 626331 -> 626332 DANGEROUS_REGENERATION_SENTENCE -> REGENERATION_COMPENSATION_SENTENCE type=dangerous_unstable_release

## Dangerous stable edges

- none observed in this bounded stability map

## Near 9780657630

- n0=9780657630 role=release_node out=5 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=9780657631 role=release_node out=5 stable_ratio=0.0 release_ratio=1.0 dangerous_ratio=1.0
- n0=9780657622 role=transition_node out=1 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657629 role=transition_node out=2 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657626 role=transition_node out=2 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657628 role=transition_node out=2 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657625 role=transition_node out=1 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657623 role=transition_node out=1 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=1.0
- n0=9780657627 role=stable_node out=1 stable_ratio=1.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657633 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657638 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657634 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657635 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657632 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0
- n0=9780657636 role=incoming_only_node out=0 stable_ratio=0.0 release_ratio=0.0 dangerous_ratio=0.0

## Boundary

No obstruction-stable grammar detected in this bounded stability map is not proof that obstruction-stable grammar cannot exist.

## Next

v3.8 Native Conservation Map

