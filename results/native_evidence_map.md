# Native Evidence Map

Version: v1.9

This report maps existing computational artifacts into native objects.

It does not add a bigger scan.

It does not prove the Collatz conjecture.

It prevents the previous mistake: returning to standard mathematics before the native structure is complete.

## Native objects

- debt
- shadow
- compensation
- regeneration
- closure
- obstruction

## Evidence mappings

### frontier_stability_certificate

Source: results/frontier_stability_certificate.json

Native role: frontier_anchor

Closure status: EVIDENCE_FOR_LOCAL_CLOSURE_NOT_FULL_NATIVE_CLOSURE

Obstruction status: NO_OBSTRUCTION_DETECTED_IN_SELECTED_FRONTIER

Native object mapping:

- debt: detected_as_hard_frontier_recovery_structure
- shadow: represented_by_post_chain_recovery_distance
- compensation: detected_by_recovery_after_chain
- regeneration: not_primary_in_this_artifact
- closure: frontier_remained_stable_under_selected_scan
- obstruction: not_detected

Proof status: finite_evidence_not_proof

Limits: This artifact stabilizes a selected frontier case. It does not establish global native closure.

### compensation_law_candidate_certificate

Source: results/compensation_law_candidate_certificate.json

Native role: compensation_recovery_evidence

Closure status: LOCALLY_RECOVERED_NOT_FULLY_CLOSED

Obstruction status: NO_UNRECOVERED_BAD_WINDOW

Native object mapping:

- debt: bad_windows_detected
- shadow: implicit_in_recovery_after_bad_windows
- compensation: all_detected_bad_windows_recovered
- regeneration: not_exhaustively_tested_by_this_artifact
- closure: local_recovery_evidence_only
- obstruction: not_detected

Proof status: finite_evidence_not_proof

Limits: This artifact supports compensation behavior over selected candidates, but does not prove forced compensation for all admissible debt structures.

### adversarial_compensation_certificate

Source: results/adversarial_compensation_certificate.json

Native role: adversarial_obstruction_search

Closure status: REGENERATED_BUT_COMPENSATED

Obstruction status: NO_COUNTEREXAMPLE_CANDIDATE_DETECTED

Native object mapping:

- debt: adversarial_bad_windows_detected
- shadow: tested_through_extended_recovery_windows
- compensation: all_adversarial_bad_windows_recovered
- regeneration: stress_tested_by_adversarial_candidate_generation
- closure: evidence_against_selected_obstruction_candidates
- obstruction: not_detected

Proof status: finite_evidence_not_proof

Limits: This artifact is the strongest current finite adversarial evidence, but remains bounded and computational.

### hardness_metric_report

Source: results/hardness_metric_report.json

Native role: hardness_is_stress_not_obstruction

Closure status: UNDECIDED_BY_HARDNESS_ALONE

Obstruction status: HARDNESS_DOES_NOT_IMPLY_OBSTRUCTION

Native object mapping:

- debt: stress_measured_across_multiple_metrics
- shadow: metric_dependent
- compensation: metric_dependent
- regeneration: metric_dependent
- closure: not_decided_by_hardness_alone
- obstruction: not_equivalent_to_hardness

Proof status: classification_not_proof

Limits: This artifact prevents the incorrect inference that the hardest case under one metric is automatically a native obstruction.

## Conclusion

The existing artifacts support the native research path, but only as finite evidence.

The next correct step is not another larger scan by default.

The next correct step is the native-to-standard translation boundary, after the native objects have been mapped.
