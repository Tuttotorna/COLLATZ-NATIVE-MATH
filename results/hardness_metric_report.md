# Hardness Metric Report

Version: v1.5

This report prevents one specific ambiguity:

There is not one single meaning of "hardest Collatz case" in this repository.

Different scanners measure different structural pressures.

## Summary table

| metric_id | hardest_n0 | primary_value_name | primary_value | source |
|---|---:|---|---:|---|
| frontier_recovery_hardness | 9780657630 | max_post_chain_recovery_distance | 114 | results/critical_frontier_summary.json |
| compensation_window_hardness | 670617279 | max_hardness_score | 10922.491951698601 | results/compensation_law_candidate_summary.json |
| adversarial_compensation_hardness | 63728127 | max_hardness_score | 14264423.973214354 | results/adversarial_compensation_summary.json |
| tightest_positive_surplus | 63728127 | min_surplus | None | results/adversarial_compensation_summary.json |
| known_long_trajectory_anchor | 837799 | odd_blocks | 195 | results/adversarial_compensation_rows.jsonl |

## Interpretation

The repository now separates at least five hardness lenses:

1. frontier recovery hardness
2. compensation-window hardness
3. adversarial compensation hardness
4. tightest positive surplus
5. known long-trajectory anchor

Different hardest cases are not contradictions unless two metrics claim to measure the same ordering rule.

## Contradiction check

- Multiple hardness lenses: `True`
- Contradiction: `False`
- Reason: Different metrics answer different questions. Different hardest_n0 values are expected unless two metrics define the same ordering rule.

## Frontier recovery hardness

- Metric ID: `frontier_recovery_hardness`
- Source: `results/critical_frontier_summary.json`
- Hardest n0: `9780657630`
- Primary value: `max_post_chain_recovery_distance = 114`
- Secondary value: `max_hardness_score = 15.100955299032181`

Meaning: Measures the hardest finite frontier case by post-chain recovery distance inside the critical frontier protocol.

Limit: This is a finite frontier metric. It is not a global Collatz proof and does not define the only possible meaning of hardness.

## Compensation-window hardness

- Metric ID: `compensation_window_hardness`
- Source: `results/compensation_law_candidate_summary.json`
- Hardest n0: `670617279`
- Primary value: `max_hardness_score = 10922.491951698601`
- Secondary value: `min_combined_surplus = 3.749927884388882e-05`

Meaning: Measures the hardest case under the finite compensation-window candidate protocol, where bad local windows must be recovered by later surplus.

Limit: This metric is window-protocol dependent. A larger value here does not automatically replace the frontier-recovery hardest case.

## Adversarial compensation hardness

- Metric ID: `adversarial_compensation_hardness`
- Source: `results/adversarial_compensation_summary.json`
- Hardest n0: `63728127`
- Primary value: `max_hardness_score = 14264423.973214354`
- Secondary value: `max_post_recovery_blocks = 236`

Meaning: Measures hardness under an adversarially generated finite candidate set, searching for bad compensation windows and counterexample candidates.

Limit: This is a stronger finite stress test than the basic compensation scan, but it remains finite and candidate-set dependent.

## Tightest positive surplus

- Metric ID: `tightest_positive_surplus`
- Source: `results/adversarial_compensation_summary.json`
- Hardest n0: `63728127`
- Primary value: `min_surplus = None`
- Secondary value: `max_post_recovery_blocks = 236`

Meaning: Identifies the closest observed recovery margin above the escape threshold among available compensation-style scans.

Limit: A tiny positive surplus is evidence of near-critical compensation in the tested domain, not evidence that all possible domains are covered.

## Known long-trajectory anchor

- Metric ID: `known_long_trajectory_anchor`
- Source: `results/adversarial_compensation_rows.jsonl`
- Hardest n0: `837799`
- Primary value: `odd_blocks = 195`
- Secondary value: `bad_windows = 4214`

Meaning: Keeps a familiar long-trajectory reference case visible, so the reader does not confuse classical trajectory length with the repository's newer hardness metrics.

Limit: A famous long trajectory is not necessarily the hardest case under frontier, compensation, or adversarial compensation metrics.


## Boundary

This report is a metric-unification artifact.

It is not a proof of the Collatz conjecture.

It is a finite, auditable map of which case is hardest under which measurement lens.
