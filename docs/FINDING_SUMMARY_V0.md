# COLLATZ-NATIVE-MATH v6.x Finding Summary V0

## Status

This is a bounded finding summary.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It summarizes the measurement line from v4.8 through v6.4.

## One-sentence thesis

In bounded odd-step Collatz measurements, debt accumulation tends to trigger fast release, post-response debt generally falls below prior peaks, near-breach grammars exist but appear isolated, and apparent fuzzy breaches were reclassified as weak-prefix artifacts rather than mature regeneration chains.

## Negative result

No mature second near-breach chain was observed in the measured artifacts.

## What this repository currently measures

The repository measures bounded odd-step Collatz behavior through a native vocabulary:

```text
debt
release
response
regeneration
near-breach
weak-prefix rebound
mature-debt rebound
```

The central bounded question is:

```text
Can debt regenerate into a persistent mature low-compression chain?
```

In the current measured artifacts, the answer observed so far is:

```text
No persistent mature low-compression regeneration chain observed.
```

## Findings

### F1 — Debt creates measurable release pressure

- status: `bounded_positive_signal`
- interpretation: Higher bounded debt peaks tend to be followed by stronger or more massive release behavior.
- boundary: Correlation is not proof and does not imply global closure.

Evidence:

- v4.8_debt_peak_vs_release_count: `0.639086442305`
- v4.8_debt_peak_vs_strong_release_count: `0.634836694059`
- v4.9_debt_peak_vs_post_peak_release_mass: `0.753686487924`
- v4.9_debt_peak_vs_post_peak_strong_release_count: `0.671853328236`

### F2 — The pressure signal is scale-positive but decays with seed scale

- status: `positive_signal_with_decay`
- interpretation: The debt-release correlation remains positive in the tested ranges, but the seed-scale axis weakens it.
- boundary: A positive bounded floor is not a theorem and cannot be extrapolated as an invariant.

Evidence:

- v5.1_first_signal: `0.902147798416`
- v5.1_last_signal: `0.573203184545`
- v5.1_relative_drop: `0.364623861465`
- v5.1_zero_crossing_observed: `false`
- v5.2_decay_axes: `['seed_scale_axis']`
- v5.2_growth_axes: `['odd_step_depth_axis', 'post_peak_horizon_axis']`

### F3 — After the initial drop, local seed blocks remain positive but weak

- status: `weak_positive_band`
- interpretation: The signal does not vanish in the tested local bands, but it becomes weak and should not be overstated.
- boundary: A weak positive band is descriptive only.

Evidence:

- v5.4_band_status: `positive_band_candidate`
- v5.4_post_initial_floor: `0.224419744454`
- v5.4_post_initial_mean: `0.305118957953`
- v5.5_band_status: `positive_but_weak_extended_band`
- v5.5_last_10_mean: `0.159226194808`
- v5.5_last_10_min: `0.086403404844`

### F4 — Response time is highly stable

- status: `strong_response_time_invariance_candidate`
- interpretation: Across measured blocks, the first post-peak response usually appears immediately or very quickly.
- boundary: Stable response timing is not a termination proof.

Evidence:

- v5.6_timing_status: `strong_response_time_invariance`
- v5.6_median_delay_all_1: `true`
- v5.6_p_delay_1_floor: `0.668000000000`
- v5.6_p_delay_le_2_floor: `0.852000000000`
- v5.6_no_response_rate_max: `0.010000000000`

### F5 — Post-response debt usually collapses below the prior peak

- status: `strong_post_response_reduction_candidate`
- interpretation: Once response occurs, bounded debt typically reduces rather than forming a new peak.
- boundary: Post-response reduction is bounded evidence only.

Evidence:

- v5.7_survival_status: `strong_debt_reduction_after_response`
- v5.7_p_reduced_floor: `0.990000000000`
- v5.7_p_new_peak_ceiling: `0.000000000000`
- v5.7_last_10_p_reduced_mean: `1.000000000000`
- v5.7_last_10_p_new_peak_mean: `0.000000000000`

### F6 — Extended horizons did not produce new post-response peaks

- status: `extended_horizon_no_new_peak_observed`
- interpretation: Increasing bounded horizon length did not create post-response new-peak behavior in the tested range.
- boundary: No bounded new peak is not global impossibility.

Evidence:

- v5.8_zero_new_peak_all_horizons: `true`
- v5.8_p_new_peak_after_release_max_values: `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
- v5.8_reduced_floor_all_horizons: `0.990000000000`
- v5.8_max_regen_ratio_all_horizons: `0.994339595811`

### F7 — Near-breach candidates exist but remain below breach

- status: `near_breach_below_one_percent_gap`
- interpretation: Some trajectories nearly rebuild prior debt, but no true breach was observed in the bounded set.
- boundary: Near-breach is not divergence and not a proof boundary.

Evidence:

- v5.9_records_measured: `50000`
- v5.9_breach_count: `0`
- v5.9_max_regeneration_ratio: `0.994339595811`
- v5.9_min_gap_to_breach: `0.005660404189`
- v5.9_top10_min_gap: `0.005660404189`

### F8 — Near-breach grammar is expansion-rich but isolated

- status: `isolated_near_breach_grammar`
- interpretation: Near-breach windows are driven by expansion-rich grammar, but measured recurrences did not chain.
- boundary: Grammar isolation is a bounded observation, not a global theorem.

Evidence:

- v6.0_near_breach_response_delay_histogram: `{'1': 11, '2': 9}`
- v6.0_near_breach_time_to_post_max_histogram: `{'16': 11, '27': 9}`
- v6.0_near_breach_a1_rate: `0.677731092437`
- v6.0_near_breach_a_ge_3_rate: `0.112920168067`
- v6.1_recurrence_seed_count: `0`
- v6.1_pattern_after_pattern_seed_count: `0`

### F9 — Fuzzy grammar increases hits but not dangerous chains

- status: `fuzzy_isolated_occurrences`
- interpretation: Relaxing exact grammar increases detected pattern hits, but did not generate recurring dangerous chains in the bounded test.
- boundary: Fuzzy absence of chains is not a global exclusion.

Evidence:

- v6.2_fuzzy_hit_seed_count: `52`
- v6.2_fuzzy_hit_rate: `0.001040000000`
- v6.2_fuzzy_recurrence_seed_count: `0`
- v6.2_dangerous_fuzzy_chain_seed_count: `0`
- v6.2_post_fuzzy_pattern_new_local_peak_rate: `0.057692307692`

### F10 — Apparent fuzzy breaches were weak-prefix artifacts

- status: `false_breach_corrected`
- interpretation: The raw v6.3 breach signal was caused by low prior peaks, not by mature debt regeneration.
- boundary: Correcting false positives strengthens measurement language but does not prove Collatz.

Evidence:

- v6.3_breach_after_fuzzy_pattern_instance_count: `2`
- v6.4_raw_breach_count: `2`
- v6.4_weak_prefix_false_breach_count: `2`
- v6.4_mature_rebound_count: `0`
- v6.4_mature_breach_count: `0`
- v6.4_mature_second_near_breach_count: `0`

## What is new inside this repo

- A native debt/release vocabulary was made computable.
- Post-peak release pressure was measured across scale and horizon variations.
- Response timing and post-response debt survival were separated from raw correlation.
- Near-breach grammar was isolated and then guarded against fuzzy false positives.
- Weak-prefix rebound was separated from mature-debt rebound.

## Strongest current claim

Within the measured bounded artifacts, no persistent mature low-compression regeneration chain was observed.

## Weakest current point

The work remains empirical and bounded; larger scale, independent replication, and formalization are needed.

## Non-claims

- This is not a proof of Collatz.
- This does not solve Collatz.
- This does not establish a global invariant.
- This does not exclude all possible divergent behavior.
- This is bounded measurement evidence only.

## Source artifacts

- v4.8_compression_debt: `results/compression_debt_machine_v0.json` | present=`True` | version=`v4.8` | machine=`Compression Debt Machine V0` | assessment=`None`
- v4.9_distributed_release_pressure: `results/distributed_release_pressure_v0.json` | present=`True` | version=`v4.9` | machine=`Distributed Release Pressure V0` | assessment=`None`
- v5.0_scale_stability: `results/scale_stability_audit_v0.json` | present=`True` | version=`v5.0` | machine=`Scale Stability Audit V0` | assessment=`scale_stable_positive_signal`
- v5.1_signal_decay: `results/signal_decay_audit_v0.json` | present=`True` | version=`v5.1` | machine=`Signal Decay Audit V0` | assessment=`positive_floor_candidate_with_decay`
- v5.2_residual_decay: `results/residual_decay_audit_v0.json` | present=`True` | version=`v5.2` | machine=`Residual Decay Audit V0` | assessment=`axis_decay_detected`
- v5.3_seed_scale_stratification: `results/seed_scale_stratification_audit_v0.json` | present=`True` | version=`v5.3` | machine=`Seed-Scale Stratification Audit V0` | assessment=`local_seed_block_decay_detected`
- v5.4_band_stabilization: `results/band_stabilization_audit_v0.json` | present=`True` | version=`v5.4` | machine=`Band Stabilization Audit V0` | assessment=`post_initial_positive_band_candidate`
- v5.5_extended_band: `results/extended_band_audit_v0.json` | present=`True` | version=`v5.5` | machine=`Extended Band Audit V0` | assessment=`positive_but_weak_extended_band`
- v5.6_response_time_invariance: `results/response_time_invariance_audit_v0.json` | present=`True` | version=`v5.6` | machine=`Response-Time Invariance Audit V0` | assessment=`strong_response_time_invariance_candidate`
- v5.7_post_response_debt_survival: `results/post_response_debt_survival_audit_v0.json` | present=`True` | version=`v5.7` | machine=`Post-Response Debt Survival Audit V0` | assessment=`strong_post_response_debt_reduction_candidate`
- v5.8_post_response_horizon_extension: `results/post_response_horizon_extension_audit_v0.json` | present=`True` | version=`v5.8` | machine=`Post-Response Horizon Extension Audit V0` | assessment=`extended_horizon_no_new_peak_with_strong_reduction`
- v5.9_near_breach: `results/near_breach_audit_v0.json` | present=`True` | version=`v5.9` | machine=`Near-Breach Audit V0` | assessment=`near_breach_below_one_percent_gap`
- v6.0_near_breach_anatomy: `results/near_breach_anatomy_v0.json` | present=`True` | version=`v6.0` | machine=`Near-Breach Anatomy V0` | assessment=`near_breach_expansion_rich_regeneration_grammar`
- v6.1_near_breach_grammar_recurrence: `results/near_breach_grammar_recurrence_audit_v0.json` | present=`True` | version=`v6.1` | machine=`Near-Breach Grammar Recurrence Audit V0` | assessment=`near_breach_grammar_isolated_occurrences_detected`
- v6.2_fuzzy_near_breach_grammar: `results/fuzzy_near_breach_grammar_audit_v0.json` | present=`True` | version=`v6.2` | machine=`Fuzzy Near-Breach Grammar Audit V0` | assessment=`fuzzy_grammar_isolated_occurrences_detected`
- v6.3_fuzzy_rebound_anatomy: `results/fuzzy_rebound_anatomy_v0.json` | present=`True` | version=`v6.3` | machine=`Fuzzy Rebound Anatomy V0` | assessment=`breach_after_fuzzy_pattern_detected`
- v6.4_mature_rebound_guard: `results/mature_rebound_guard_v0.json` | present=`True` | version=`v6.4` | machine=`Mature Rebound Guard V0` | assessment=`raw_breaches_reclassified_as_weak_prefix_artifacts`

## Missing sources

None.

## Boundary

- proof_status: `not_a_proof`
- collatz_status: `not_claimed_solved`
- theorem_status: `no_theorem_claimed`
- global_closure_status: `not_claimed`
- global_invariant_status: `not_claimed`
- bounded_evidence_status: `measurement_only`
