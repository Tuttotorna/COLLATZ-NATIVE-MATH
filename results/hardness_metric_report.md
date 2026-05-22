# Hardness Metric Report

Version: v1.5.1

This report separates several finite hardness lenses used by COLLATZ-NATIVE-MATH.

The key point is simple: different notions of hardness can select different cases.
That is not a contradiction.

## Metrics

### frontier_recovery_hardness

- hardest_n0: 9780657630
- max_post_chain_recovery_distance: 114
- max_hardness_score: 15.100955299032181
- source: results/critical_frontier_summary.json
- interpretation: Measures recovery distance after structurally cheap debt chains.

### compensation_window_hardness

- hardest_n0: 670617279
- max_hardness_score: 10922.491951698601
- min_combined_surplus: 3.749927884388882e-05
- source: results/compensation_law_candidate_summary.json
- interpretation: Measures how hard a bad finite window is to compensate.

### adversarial_compensation_hardness

- hardest_n0: 63728127
- max_hardness_score: 14264423.973214354
- max_post_recovery_blocks: 236
- source: results/adversarial_compensation_summary.json
- interpretation: Measures the strongest adversarial finite compensation stress case.

### tightest_positive_surplus

- hardest_n0: 63728127
- min_surplus: 1.7736432994075457e-05
- counterexample_candidate_count: 0
- source: results/adversarial_compensation_certificate.json
- interpretation: Measures the tightest still-positive compensation margin found.

### known_long_trajectory_anchor

- hardest_n0: 837799
- odd_blocks: 195
- bad_windows: 4214
- source: results/adversarial_compensation_rows.jsonl
- interpretation: Long trajectory length is not the same hardness notion as compensation hardness.

## Interpretation

Different hardness lenses identify different finite stress cases. This is not a contradiction. It means trajectory length, recovery distance, compensation surplus, and adversarial compensation hardness are distinct observables.

## Limits

This report summarizes finite computational scans. It is not a proof of the Collatz conjecture.
