# Fuzzy Rebound Anatomy V0 Results

## Status

This is a bounded fuzzy rebound anatomy audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`breach_after_fuzzy_pattern_detected`

## Summary

- records_measured: `50000`
- fuzzy_instance_count: `52`
- rebound_instance_count: `3`
- rebound_seed_count: `3`
- second_near_breach_instance_count: `0`
- breach_after_fuzzy_pattern_instance_count: `2`
- rebound_class_counts: `{'breach_after_fuzzy_pattern': 2, 'harmless_rebound': 1}`
- mean_post_pattern_debt_gain: `1.396503199073`
- max_post_pattern_debt_gain: `3.094738704637`
- mean_post_max_to_prior_peak_ratio: `4.943930575254`
- max_post_max_to_prior_peak_ratio: `12.033347383535`
- min_gap_to_prior_peak: `-11.033347383535`
- mean_next_release_delay_after_pattern_end: `8.666666666667`
- min_next_release_delay_after_pattern_end: `4.000000000000`
- max_next_release_delay_after_pattern_end: `11.000000000000`

## Rebound instances

### seed `79263` pattern `B` position `0`

- hamming_distance: `2`
- similarity: `0.882352941176`
- post_pattern_debt_gain: `3.094738704637`
- prior_debt_peak: `0.584968567831`
- post_horizon_max_prefix: `7.039129985160`
- post_max_to_prior_peak_ratio: `12.033347383535`
- gap_to_prior_peak: `-11.033347383535`
- rebound_class: `breach_after_fuzzy_pattern`
- next_release_delay_after_pattern_end: `11`

after_pattern_a_sequence:

`1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 5, 1, 2, 1, 1, 1, 1, 1, 2, 1, 6, 1, 5, 2, 3, 4, 1, 4, 1, 1, 2, 3, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 5, 3, 1, 1, 1`

### seed `69015` pattern `B` position `2`

- hamming_distance: `2`
- similarity: `0.882352941176`
- post_pattern_debt_gain: `0.924819912716`
- prior_debt_peak: `1.169936614773`
- post_horizon_max_prefix: `3.039447852986`
- post_max_to_prior_peak_ratio: `2.597959423276`
- gap_to_prior_peak: `-1.597959423276`
- rebound_class: `breach_after_fuzzy_pattern`
- next_release_delay_after_pattern_end: `11`

after_pattern_a_sequence:

`2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 5, 1, 1, 1, 1, 1, 3, 1, 3, 5, 1, 1, 1, 1, 2, 1, 2, 1, 2, 3, 1, 6, 2, 2, 3, 1, 2, 4, 1, 2, 2, 4, 1, 1, 2, 3, 4`

### seed `89749` pattern `B` position `0`

- hamming_distance: `2`
- similarity: `0.882352941176`
- post_pattern_debt_gain: `0.169950979866`
- prior_debt_peak: `-4.415032141030`
- post_horizon_max_prefix: `-0.885147360967`
- post_max_to_prior_peak_ratio: `0.200484918952`
- gap_to_prior_peak: `0.799515081048`
- rebound_class: `harmless_rebound`
- next_release_delay_after_pattern_end: `4`

after_pattern_a_sequence:

`2, 1, 2, 3, 1, 6, 2, 2, 3, 1, 2, 4, 1, 2, 2, 4, 1, 1, 2, 3, 4`

## Native interpretation

This audit separates local rebound from second near-breach behavior.

A rebound is dangerous only if it approaches or exceeds the prior debt peak.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
