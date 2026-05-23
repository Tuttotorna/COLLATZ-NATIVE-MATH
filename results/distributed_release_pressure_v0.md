# Distributed Release Pressure V0 Results

## Status

This is a bounded measurement result.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

## Parameters

- max_odd_seed: `999`
- odd_steps: `120`
- post_peak_horizon: `20`

## Counts

- odd_seeds_measured: `500`
- terminated_within_bound: `500`
- not_terminated_within_bound: `0`
- records_with_positive_debt_peak: `388`
- records_with_post_peak_release: `495`
- positive_debt_records_with_post_peak_release: `388`

## Aggregate measurements

- mean_debt_peak: `1.261549113165`
- max_debt_peak: `6.892124975745`
- mean_response_delay: `1.288888888889`
- median_response_delay: `1.000000000000`
- min_response_delay: `1.000000000000`
- max_response_delay: `7.000000000000`
- mean_post_peak_release_count_h: `4.404000000000`
- mean_post_peak_strong_release_count_h: `2.840000000000`
- mean_post_peak_release_mass_h: `10.114403955132`
- debt_peak_vs_post_peak_release_count_h_pearson: `0.534051282576`
- debt_peak_vs_post_peak_strong_release_count_h_pearson: `0.671853328236`
- debt_peak_vs_post_peak_release_mass_h_pearson: `0.753686487924`
- debt_peak_vs_total_release_count_pearson: `0.627969192984`

## Highest debt-peak samples

- seed `703`: debt_peak=`6.892124975745`, peak_index=`33`, response_delay=`1`, post_peak_release_count_h=`6`, post_peak_release_mass_h=`14.486965591654`
- seed `27`: debt_peak=`6.832421226170`, peak_index=`31`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `31`: debt_peak=`6.633112417947`, peak_index=`29`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `937`: debt_peak=`6.477600617158`, peak_index=`34`, response_delay=`1`, post_peak_release_count_h=`6`, post_peak_release_mass_h=`14.486965591654`
- seed `41`: debt_peak=`6.229756723715`, peak_index=`30`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `871`: debt_peak=`6.191683935998`, peak_index=`13`, response_delay=`2`, post_peak_release_count_h=`6`, post_peak_release_mass_h=`11.486452209335`
- seed `47`: debt_peak=`6.032719876656`, peak_index=`28`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `55`: debt_peak=`5.805949014809`, peak_index=`31`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `63`: debt_peak=`5.610028804834`, peak_index=`29`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`
- seed `71`: debt_peak=`5.437561608829`, peak_index=`27`, response_delay=`1`, post_peak_release_count_h=`5`, post_peak_release_mass_h=`11.963535626110`

## Native interpretation

The machine tests whether debt peaks are followed by distributed release pressure.

The target signal is not one maximal discharge, but timing and density of release after peak.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
