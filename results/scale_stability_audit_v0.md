# Scale Stability Audit V0 Results

## Status

This is a bounded reproducibility audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`scale_stable_positive_signal`

## Stability summary

- configs_tested: `6`
- primary_signal_name: `debt_peak_vs_post_peak_release_mass_h_pearson`
- primary_signal_values: `0.902147798416, 0.901699568955, 0.827124187287, 0.753686487924, 0.677380713808, 0.633983550100`
- primary_signal_positive_count: `6`
- primary_signal_all_positive: `True`
- primary_signal_min: `0.633983550100`
- primary_signal_max: `0.902147798416`
- primary_signal_mean: `0.782670384415`
- primary_signal_spread: `0.268164248315`
- primary_signal_min_above_0_5: `True`
- primary_signal_mean_above_0_6: `True`
- strong_release_signal_values: `0.901543291910, 0.881606316737, 0.806659739530, 0.671853328236, 0.557815010142, 0.492037265621`
- release_count_signal_values: `0.830875912376, 0.796957810390, 0.646879609170, 0.534051282576, 0.472278788745, 0.447824099157`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

## Configuration results

### max_odd_seed=99, odd_steps=80, post_peak_horizon=10

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.260869565217`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.902147798416`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.901543291910`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.830875912376`

### max_odd_seed=199, odd_steps=80, post_peak_horizon=10

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.250000000000`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.901699568955`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.881606316737`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.796957810390`

### max_odd_seed=499, odd_steps=100, post_peak_horizon=15

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.257142857143`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.827124187287`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.806659739530`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.646879609170`

### max_odd_seed=999, odd_steps=120, post_peak_horizon=20

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.288888888889`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.753686487924`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.671853328236`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.534051282576`

### max_odd_seed=1499, odd_steps=140, post_peak_horizon=20

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.330645161290`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.677380713808`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.557815010142`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.472278788745`

### max_odd_seed=1999, odd_steps=160, post_peak_horizon=25

- median_response_delay: `1.000000000000`
- mean_response_delay: `1.357142857143`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.633983550100`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.492037265621`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.447824099157`

## Native interpretation

The audit checks whether the post-peak release pressure signal survives scale changes.

If the primary signal remains positive and strong, the debt/release language is not only descriptive in one run.

It becomes a bounded reproducible measurement pattern.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
