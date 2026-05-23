# Seed-Scale Stratification Audit V0 Results

## Status

This is a bounded seed-scale stratification audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Bounded assessment

`local_seed_block_decay_detected`

## Comparison

- cumulative_direction: `decay`
- block_direction: `decay`
- cumulative_min_signal: `0.388313933083`
- block_min_signal: `0.293181671861`
- attribution: `local_block_decay`
- positivity_status: `both_positive`

## Cumulative summary

- family_name: `cumulative_ranges`
- x_values: `999.000000000000, 1999.000000000000, 2999.000000000000, 3999.000000000000, 4999.000000000000, 5999.000000000000`
- log10_x_values: `2.999565488226, 3.300812794118, 3.476976465760, 3.601951404134, 3.698883136753, 3.778078861937`
- primary_signal_values: `0.753686487924, 0.594846762749, 0.489542406303, 0.437674092626, 0.401201250877, 0.388313933083`
- first_signal: `0.753686487924`
- last_signal: `0.388313933083`
- total_drop: `0.365372554840`
- relative_drop: `0.484780556232`
- min_signal: `0.388313933083`
- max_signal: `0.753686487924`
- mean_signal: `0.510877488927`
- slope_per_log10_x: `-0.485200171034`
- x_vs_signal_correlation_log10: `-0.993421267818`
- direction: `decay`
- floor_status: `positive_but_weak_floor`
- all_positive: `True`
- zero_crossing_observed: `False`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

## Block summary

- family_name: `local_blocks`
- x_values: `500.000000000000, 1500.000000000000, 2500.000000000000, 3500.000000000000, 4500.000000000000, 5500.000000000000`
- log10_x_values: `2.698970004336, 3.176091259056, 3.397940008672, 3.544068044350, 3.653212513775, 3.740362689494`
- primary_signal_values: `0.753686487924, 0.457273489036, 0.314858662758, 0.318594574258, 0.293181671861, 0.363033387905`
- first_signal: `0.753686487924`
- last_signal: `0.363033387905`
- total_drop: `0.390653100019`
- relative_drop: `0.518323077670`
- min_signal: `0.293181671861`
- max_signal: `0.753686487924`
- mean_signal: `0.416771378957`
- slope_per_log10_x: `-0.419346423989`
- x_vs_signal_correlation_log10: `-0.918927250044`
- direction: `decay`
- floor_status: `positive_but_weak_floor`
- all_positive: `True`
- zero_crossing_observed: `False`
- median_response_delay_values: `1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000, 1.000000000000`
- median_response_delay_all_at_most_1: `True`

## Cumulative range results

- 1..999: primary_signal=`0.753686487924`, median_response_delay=`1.000000000000`
- 1..1999: primary_signal=`0.594846762749`, median_response_delay=`1.000000000000`
- 1..2999: primary_signal=`0.489542406303`, median_response_delay=`1.000000000000`
- 1..3999: primary_signal=`0.437674092626`, median_response_delay=`1.000000000000`
- 1..4999: primary_signal=`0.401201250877`, median_response_delay=`1.000000000000`
- 1..5999: primary_signal=`0.388313933083`, median_response_delay=`1.000000000000`

## Local block results

- 1..999: primary_signal=`0.753686487924`, median_response_delay=`1.000000000000`
- 1001..1999: primary_signal=`0.457273489036`, median_response_delay=`1.000000000000`
- 2001..2999: primary_signal=`0.314858662758`, median_response_delay=`1.000000000000`
- 3001..3999: primary_signal=`0.318594574258`, median_response_delay=`1.000000000000`
- 4001..4999: primary_signal=`0.293181671861`, median_response_delay=`1.000000000000`
- 5001..5999: primary_signal=`0.363033387905`, median_response_delay=`1.000000000000`

## Native interpretation

The audit tests whether seed-scale decay is local or produced by cumulative mixing.

A local block signal that remains positive while cumulative signal decays suggests dilution rather than collapse.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
