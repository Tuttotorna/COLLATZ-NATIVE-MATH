# Residual Decay Audit V0

## Status

This document introduces a bounded residual decay audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It separates the causes of signal decay by varying one measurement axis at a time.

## Why this layer exists

Signal Decay Audit V0 showed:

    the primary signal decays with scale
    the primary signal remains positive
    no zero crossing was observed
    a positive bounded floor candidate appeared

However, v5.1 changed several parameters together:

    max_odd_seed
    odd_steps
    post_peak_horizon

Therefore the observed decay could be caused by:

    larger seed range
    longer odd-step observation
    wider post-peak horizon
    interaction between parameters

## Native question

The native question is:

    Which measurement axis is responsible for weakening the release-pressure signal?

## Audited axes

The audit separates three axes.

### Axis A: seed-scale axis

Vary:

    max_odd_seed

Hold fixed:

    odd_steps
    post_peak_horizon

### Axis B: odd-step-depth axis

Vary:

    odd_steps

Hold fixed:

    max_odd_seed
    post_peak_horizon

### Axis C: post-peak-horizon axis

Vary:

    post_peak_horizon

Hold fixed:

    max_odd_seed
    odd_steps

## Primary signal

The primary signal remains:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Residual decay measurements

For each axis, the audit measures:

    signal_values
    axis_vs_signal_correlation
    signal_slope
    first_signal
    last_signal
    total_drop
    relative_drop
    min_signal
    mean_signal
    zero_crossing_observed

## Boundary

    residual_decay_audit != proof
    axis attribution != theorem
    correlation != causation
    bounded axis signal != global invariant
    no zero crossing in tested axes != universal closure

## V0 output artifacts

The builder writes:

    results/residual_decay_audit_v0.json
    results/residual_decay_audit_v0.md
    results/residual_decay_audit_v0_certificate.json
