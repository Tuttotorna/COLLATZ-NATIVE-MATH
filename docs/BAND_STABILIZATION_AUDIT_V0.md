# Band Stabilization Audit V0

## Status

This document introduces a bounded band-stabilization audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether local seed-block release-pressure signals stabilize into a positive band after the initial decay.

## Why this layer exists

Seed-Scale Stratification Audit V0 showed:

    cumulative signal decays
    local block signal also decays
    no zero crossing was observed
    after the first block, local signals appeared to oscillate in a weaker positive band

This creates a sharper question:

    After the initial seed-scale drop, does the local signal stabilize above zero?

## Native question

The native question is:

    Does debt-to-release pressure remain locally visible as a positive band
    after low-seed effects are removed?

## Primary signal

The primary signal remains:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Block design

The audit measures non-overlapping blocks:

    1..999
    1001..1999
    2001..2999
    ...
    19001..19999

Only odd seeds are measured.

## Band measurements

The audit computes:

    block_signal_values
    post_initial_block_signal_values
    rolling_mean_3
    rolling_min_3
    rolling_max_3
    band_floor
    band_ceiling
    band_width
    zero_crossing_observed
    post_initial_zero_crossing_observed
    post_initial_slope
    post_initial_correlation
    median_response_delay_values

## Boundary

    band_stabilization_audit != proof
    positive_band != theorem
    band_floor != global invariant
    no zero crossing in tested blocks != universal closure
    bounded stabilization != termination proof

## V0 output artifacts

The builder writes:

    results/band_stabilization_audit_v0.json
    results/band_stabilization_audit_v0.md
    results/band_stabilization_audit_v0_certificate.json
