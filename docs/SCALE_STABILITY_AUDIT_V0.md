# Scale Stability Audit V0

## Status

This document introduces a bounded scale-stability audit for the Distributed Release Pressure signal.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether a bounded empirical signal survives changes in scale and measurement parameters.

## Why this layer exists

Compression Debt Machine V0 measured debt, release, and regeneration.

Distributed Release Pressure V0 measured whether debt peaks are followed by rapid and stronger post-peak release pressure.

The strongest v4.9 signal was:

    debt_peak -> post_peak_release_mass

The next question is not whether this signal exists in one bounded run.

The next question is:

    Does the signal remain stable when N, odd_steps, and post_peak_horizon change?

## Native question

The audit asks:

    Is distributed release pressure a scale-stable bounded signal,
    or only an artifact of one parameter setting?

## Parameters audited

The audit varies:

    max_odd_seed
    odd_steps
    post_peak_horizon

Each configuration produces:

    debt_peak_vs_post_peak_release_count_h_pearson
    debt_peak_vs_post_peak_strong_release_count_h_pearson
    debt_peak_vs_post_peak_release_mass_h_pearson
    debt_peak_vs_total_release_count_pearson
    median_response_delay
    mean_response_delay

## Stability criterion

A signal is considered bounded-stable if:

    1. it appears across multiple configurations,
    2. it preserves sign,
    3. it does not collapse toward zero under scale change,
    4. it keeps the same qualitative interpretation.

This is not a theorem.

It is a reproducibility audit.

## Primary signal

The primary signal is:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Secondary signals

Secondary signals:

    debt_peak_vs_post_peak_strong_release_count_h_pearson
    debt_peak_vs_post_peak_release_count_h_pearson
    debt_peak_vs_total_release_count_pearson

These measure whether the pressure appears as:

    more release events
    more strong release events
    more total releases
    greater release mass

## Boundary

    scale_stability_audit != proof
    stable_signal != theorem
    correlation != causation
    bounded reproducibility != global closure
    no collapse under tested scales != universal invariant

## V0 output artifacts

The builder writes:

    results/scale_stability_audit_v0.json
    results/scale_stability_audit_v0.md
    results/scale_stability_audit_v0_certificate.json
