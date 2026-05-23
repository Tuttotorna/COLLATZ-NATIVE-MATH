# Post-Response Debt Survival Audit V0

## Status

This document introduces a bounded post-response debt survival audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It measures whether the rapid release response after a debt peak actually reduces debt.

## Why this layer exists

Response-Time Invariance Audit V0 showed:

    median response delay is 1 in every tested block up to 99999
    most debt peaks receive a release response within 1 to 3 odd steps
    response timing is more stable than release-mass correlation

The next question is not whether the response arrives.

The next question is whether it works.

## Native question

The native question is:

    After the first post-peak release arrives,
    how much debt survives?

## Debt peak

For an odd-step trajectory, define cumulative debt:

    P_j = sum(delta_i for i = 0..j)

Then:

    debt_peak = max(P_j)

The peak index is the first index where this maximum is reached.

## First response

The first response is:

    first later step t > peak_index where delta_t < -1

If no such step exists inside the bound:

    response_delay = null

## Survival measurements

For a trajectory with a post-peak release:

    debt_after_first_release = P_t
    debt_drop_after_first_release = debt_peak - debt_after_first_release
    survival_ratio = debt_after_first_release / debt_peak

If debt_peak <= 0, ratio-style metrics are marked null.

## Interpretation

    survival_ratio < 1  => first response reduced debt below peak
    survival_ratio < 0  => first response over-discharged below zero
    survival_ratio >= 1 => debt survived at or above peak after first response

The audit also checks whether a new peak appears after the first response:

    new_peak_after_release = max(P_j for j > t) > debt_peak

## Boundary

    post_response_debt_survival != proof
    debt_drop != termination theorem
    survival_ratio != global invariant
    no new peak in tested window != universal closure
    bounded response effectiveness != Collatz solved

## V0 output artifacts

The builder writes:

    results/post_response_debt_survival_audit_v0.json
    results/post_response_debt_survival_audit_v0.md
    results/post_response_debt_survival_audit_v0_certificate.json
