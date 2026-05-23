# Signal Decay Audit V0 Results

## Status

This is a bounded decay audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`positive_floor_candidate_with_decay`

## Decay summary

- configs_tested: `8`
- primary_signal_name: `debt_peak_vs_post_peak_release_mass_h_pearson`
- scales: `99.000000000000, 199.000000000000, 499.000000000000, 999.000000000000, 1499.000000000000, 1999.000000000000, 2999.000000000000, 3999.000000000000`
- log10_scales: `1.995635194598, 2.298853076410, 2.698100545623, 2.999565488226, 3.175801632848, 3.300812794118, 3.476976465760, 3.601951404134`
- primary_signal_values: `0.902147798416, 0.901699568955, 0.827124187287, 0.753686487924, 0.677380713808, 0.633983550100, 0.547488820066, 0.573203184545`
- first_signal: `0.902147798416`
- last_signal: `0.573203184545`
- total_drop: `0.328944613871`
- relative_drop: `0.364623861465`
- slope_per_seed: `-0.000094295856`
- slope_per_log10_scale: `-0.238675497946`
- scale_vs_primary_signal_correlation: `-0.966306493918`
- early_window_mean: `0.846164510645`
- late_window_mean: `0.608014067130`
- late_to_early_ratio: `0.718553023059`
- signal_floor_estimate_last3_mean: `0.584891851570`
- signal_floor_min_last3: `0.547488820066`
- zero_crossing_observed: `False`
- all_positive: `True`
- floor_candidate: `True`
- decay_detected: `True`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

## Configuration results

### max_odd_seed=99, odd_steps=80, post_peak_horizon=10

- primary_signal: `0.902147798416`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.260869565217`

### max_odd_seed=199, odd_steps=80, post_peak_horizon=10

- primary_signal: `0.901699568955`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.250000000000`

### max_odd_seed=499, odd_steps=100, post_peak_horizon=15

- primary_signal: `0.827124187287`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.257142857143`

### max_odd_seed=999, odd_steps=120, post_peak_horizon=20

- primary_signal: `0.753686487924`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.288888888889`

### max_odd_seed=1499, odd_steps=140, post_peak_horizon=20

- primary_signal: `0.677380713808`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.330645161290`

### max_odd_seed=1999, odd_steps=160, post_peak_horizon=25

- primary_signal: `0.633983550100`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.357142857143`

### max_odd_seed=2999, odd_steps=180, post_peak_horizon=25

- primary_signal: `0.547488820066`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.408299866131`

### max_odd_seed=3999, odd_steps=200, post_peak_horizon=30

- primary_signal: `0.573203184545`
- median_response_delay: `1.000000000000`
- mean_response_delay: `1.430792377131`

## Native interpretation

The audit checks whether the release-pressure signal is collapsing toward zero or preserving a positive bounded floor candidate.

A positive floor candidate is not a theorem.

It is a bounded reproducibility signal.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
