# Extended Band Audit V0

## Status

This document introduces an extended bounded band audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It extends the local seed-block release-pressure band test to a larger bounded domain.

## Why this layer exists

Band Stabilization Audit V0 detected a post-initial positive band up to 19999.

The signal did not cross zero, but it retained residual decay.

The next question is:

    Does the positive band persist when the seed domain is extended?

## Native question

The native question is:

    Does local debt-to-release pressure remain visible far beyond the initial low-seed region?

## Primary signal

The primary signal remains:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Extended block design

The audit measures non-overlapping blocks:

    1..999
    1001..1999
    2001..2999
    ...
    99001..99999

Only odd seeds are measured.

## Measurements

The audit computes:

    block_signal_values
    post_initial_block_signal_values
    rolling_mean_5
    rolling_min_5
    rolling_max_5
    last_5_mean
    last_5_min
    last_10_mean
    last_10_min
    full_slope
    post_initial_slope
    last_half_slope
    zero_crossing_observed
    post_initial_zero_crossing_observed
    median_response_delay_values

## Boundary

    extended_band_audit != proof
    positive_extended_band != theorem
    last_5_positive != invariant
    no zero crossing in tested blocks != universal closure
    bounded persistence != termination proof

## V0 output artifacts

The builder writes:

    results/extended_band_audit_v0.json
    results/extended_band_audit_v0.md
    results/extended_band_audit_v0_certificate.json
