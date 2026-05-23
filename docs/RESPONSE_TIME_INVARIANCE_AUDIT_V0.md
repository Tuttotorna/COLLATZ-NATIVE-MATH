# Response-Time Invariance Audit V0

## Status

This document introduces a bounded response-time invariance audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether release response timing remains stable even when the debt-to-release-mass correlation weakens.

## Why this layer exists

Extended Band Audit V0 showed:

    debt-to-release-mass correlation remains positive up to 99999
    the signal becomes weak at higher seed blocks
    no zero crossing was observed
    median response delay stayed at 1 across all tested blocks

This suggests that the more robust structure may not be release mass.

The more robust structure may be response timing.

## Native question

The native question is:

    Does every debt peak tend to trigger a rapid release response
    even when release-mass correlation becomes weak?

## Primary timing signal

For each seed trajectory, define:

    debt_peak = max cumulative odd-step drift
    peak_index = first index where debt_peak appears
    response_delay = first later odd-step index with delta < -1 minus peak_index

A delay of 1 means:

    the first later odd step after the debt peak is already a release event

## Measurements

The audit computes, per seed block:

    median_response_delay
    mean_response_delay
    p_delay_1
    p_delay_le_2
    p_delay_le_3
    max_response_delay
    no_response_rate
    debt_peak_vs_response_delay_pearson
    debt_peak_vs_has_immediate_response_pearson

## Boundary

    response_time_invariance != proof
    median_delay_1 != termination theorem
    immediate_response_rate != global invariant
    no zero crossing in timing signal != universal closure
    bounded response timing != Collatz solved

## V0 output artifacts

The builder writes:

    results/response_time_invariance_audit_v0.json
    results/response_time_invariance_audit_v0.md
    results/response_time_invariance_audit_v0_certificate.json
