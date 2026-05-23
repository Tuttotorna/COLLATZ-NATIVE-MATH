# Residual Decay Audit V0 Results

## Status

This is a bounded residual decay audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`axis_decay_detected`

## Residual attribution

- decay_axes: `seed_scale_axis`
- growth_axes: `odd_step_depth_axis, post_peak_horizon_axis`
- flat_axes: `none`
- floor_preserved_axes: `none`
- zero_crossing_axes: `none`

## Axis summaries

### seed_scale_axis

- axis_name: `seed_scale_axis`
- axis_values: `99.000000000000, 199.000000000000, 499.000000000000, 999.000000000000, 1999.000000000000, 3999.000000000000`
- axis_log10_values: `1.995635194598, 2.298853076410, 2.698100545623, 2.999565488226, 3.300812794118, 3.601951404134`
- primary_signal_values: `0.902147798416, 0.893777022886, 0.837313550277, 0.753686487924, 0.594846762749, 0.437674092626`
- first_signal: `0.902147798416`
- last_signal: `0.437674092626`
- total_drop: `0.464473705789`
- relative_drop: `0.514853227603`
- min_signal: `0.437674092626`
- max_signal: `0.902147798416`
- mean_signal: `0.736574285813`
- slope_per_axis_unit: `-0.000122184237`
- slope_per_log10_axis: `-0.287644601008`
- axis_vs_signal_correlation_log10: `-0.941021490039`
- direction: `decay`
- floor_status: `positive_but_weak_floor`
- zero_crossing_observed: `False`
- all_positive: `True`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

### odd_step_depth_axis

- axis_name: `odd_step_depth_axis`
- axis_values: `40.000000000000, 80.000000000000, 120.000000000000, 160.000000000000, 200.000000000000, 240.000000000000`
- axis_log10_values: `1.602059991328, 1.903089986992, 2.079181246048, 2.204119982656, 2.301029995664, 2.380211241712`
- primary_signal_values: `0.206687080967, 0.594846762749, 0.594846762749, 0.594846762749, 0.594846762749, 0.594846762749`
- first_signal: `0.206687080967`
- last_signal: `0.594846762749`
- total_drop: `-0.388159681782`
- relative_drop: `-1.878006501255`
- min_signal: `0.206687080967`
- max_signal: `0.594846762749`
- mean_signal: `0.530153482452`
- slope_per_axis_unit: `0.001386284578`
- slope_per_log10_axis: `0.446397187293`
- axis_vs_signal_correlation_log10: `0.810682692480`
- direction: `growth`
- floor_status: `positive_but_weak_floor`
- zero_crossing_observed: `False`
- all_positive: `True`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

### post_peak_horizon_axis

- axis_name: `post_peak_horizon_axis`
- axis_values: `5.000000000000, 10.000000000000, 15.000000000000, 20.000000000000, 25.000000000000, 30.000000000000`
- axis_log10_values: `0.698970004336, 1.000000000000, 1.176091259056, 1.301029995664, 1.397940008672, 1.477121254720`
- primary_signal_values: `0.102341982902, 0.364542454174, 0.471265860777, 0.594846762749, 0.633983550100, 0.667700061668`
- first_signal: `0.102341982902`
- last_signal: `0.667700061668`
- total_drop: `-0.565358078766`
- relative_drop: `-5.524204854484`
- min_signal: `0.102341982902`
- max_signal: `0.667700061668`
- mean_signal: `0.472446778728`
- slope_per_axis_unit: `0.021478254763`
- slope_per_log10_axis: `0.737737091907`
- axis_vs_signal_correlation_log10: `0.994610444962`
- direction: `growth`
- floor_status: `positive_but_weak_floor`
- zero_crossing_observed: `False`
- all_positive: `True`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

## Native interpretation

The audit separates whether signal decay comes from seed scale, odd-step depth, or post-peak horizon.

This prevents treating a mixed parameter effect as a single structural law.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
