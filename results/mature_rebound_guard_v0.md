# Mature Rebound Guard V0 Results

## Status

This is a bounded guard over fuzzy rebound anatomy.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`raw_breaches_reclassified_as_weak_prefix_artifacts`

## Summary

- source_version: `v6.3`
- source_machine: `Fuzzy Rebound Anatomy V0`
- rebound_instance_count: `3`
- raw_breach_after_fuzzy_pattern_count: `2`
- weak_prefix_rebound_count: `3`
- weak_prefix_false_breach_count: `2`
- mature_rebound_count: `0`
- mature_breach_count: `0`
- mature_second_near_breach_count: `0`
- mature_harmless_rebound_count: `0`
- guarded_class_counts: `{'weak_prefix_false_breach': 2, 'weak_prefix_rebound': 1}`
- raw_class_counts: `{'breach_after_fuzzy_pattern': 2, 'harmless_rebound': 1}`
- mature_prior_peak_threshold: `4.000000000000`
- second_near_breach_threshold: `0.950000000000`
- max_raw_ratio: `12.033347383535`
- max_mature_ratio: `None`
- mean_prior_peak: `-0.886708986142`
- min_prior_peak: `-4.415032141030`
- max_prior_peak: `1.169936614773`
- mean_weak_prior_peak: `-0.886708986142`
- max_weak_prior_peak: `1.169936614773`
- mean_post_pattern_debt_gain: `1.396503199073`
- max_post_pattern_debt_gain: `3.094738704637`
- raw_breach_reclassified_as_weak_prefix_false_breach: `2`

## Weak-prefix false breaches

### seed `79263` pattern `B` position `0`

- raw_rebound_class: `breach_after_fuzzy_pattern`
- guarded_rebound_class: `weak_prefix_false_breach`
- prior_debt_peak: `0.584968567831`
- mature_prior_peak_threshold: `4.000000000000`
- prior_peak_deficit_to_maturity: `3.415031432169`
- post_horizon_max_prefix: `7.039129985160`
- post_max_to_prior_peak_ratio: `12.033347383535`
- post_pattern_debt_gain: `3.094738704637`

### seed `69015` pattern `B` position `2`

- raw_rebound_class: `breach_after_fuzzy_pattern`
- guarded_rebound_class: `weak_prefix_false_breach`
- prior_debt_peak: `1.169936614773`
- mature_prior_peak_threshold: `4.000000000000`
- prior_peak_deficit_to_maturity: `2.830063385227`
- post_horizon_max_prefix: `3.039447852986`
- post_max_to_prior_peak_ratio: `2.597959423276`
- post_pattern_debt_gain: `0.924819912716`

## Mature breach instances

None.

## Mature second near-breach instances

None.

## Native interpretation

The guard separates raw rebound over a weak prefix from rebound over mature accumulated debt.

A raw breach caused by a low prior peak is reclassified as a weak-prefix artifact.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
