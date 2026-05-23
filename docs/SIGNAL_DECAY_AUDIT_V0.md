# Signal Decay Audit V0

## Status

This document introduces a bounded decay audit for the distributed release pressure signal.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether the primary signal decays toward zero or remains above a positive bounded floor.

## Why this layer exists

Scale Stability Audit V0 showed that the primary signal remained positive across scale changes:

    debt_peak_vs_post_peak_release_mass_h_pearson

However, the values decreased as the tested domain increased.

That creates a precise question:

    Is the signal decaying toward zero,
    or approaching a positive floor?

## Native question

The native question is:

    Does distributed release pressure remain structurally visible
    as the observation scale increases?

## Primary signal

The primary signal remains:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Decay measurements

The audit measures:

    signal_decay_slope
    scale_vs_primary_signal_correlation
    early_window_mean
    late_window_mean
    late_to_early_ratio
    last_signal_value
    signal_floor_estimate

## Bounded interpretation

If the signal remains positive and the late-window mean remains above threshold:

    bounded positive floor candidate

If the signal keeps decreasing sharply:

    possible finite-scale artifact

## Boundary

    signal_decay_audit != proof
    positive_floor_candidate != theorem
    correlation != causation
    bounded floor != global invariant
    no zero crossing in tested range != universal closure

## V0 output artifacts

The builder writes:

    results/signal_decay_audit_v0.json
    results/signal_decay_audit_v0.md
    results/signal_decay_audit_v0_certificate.json
