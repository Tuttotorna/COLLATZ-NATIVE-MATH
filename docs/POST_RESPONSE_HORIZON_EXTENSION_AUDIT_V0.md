# Post-Response Horizon Extension Audit V0

## Status

This document introduces a bounded post-response horizon extension audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether post-response new-peak regeneration appears only when the odd-step observation horizon is extended.

## Why this layer exists

Post-Response Debt Survival Audit V0 showed:

    median response delay is 1
    response reduces debt below peak in almost all tested cases
    no new peak after first release was observed inside ODD_STEPS = 160

The remaining limitation is direct:

    maybe a new post-response peak appears later than 160 odd steps

This audit varies odd_steps while keeping seed blocks fixed.

## Native question

The native question is:

    Does the first release close the local debt episode,
    or does debt regenerate into a new higher peak later?

## Horizon configurations

The audit tests:

    odd_steps = 160, 240, 320, 480, 640, 960

The seed domain is bounded:

    odd seeds from 1 to 49999

The block size is:

    999

## Core measurements

For each horizon:

    p_new_peak_after_release
    p_reduced_below_peak
    median_survival_ratio
    max_post_response_regeneration_ratio
    p_any_post_response_regeneration
    median_time_to_new_peak_if_any

## Regeneration ratio

For a trajectory with a first post-peak release:

    post_response_max_debt = max cumulative debt after the response
    regeneration_ratio = post_response_max_debt / debt_peak

If:

    regeneration_ratio > 1

then a new higher debt peak appeared after the first release.

## Boundary

    horizon_extension_audit != proof
    no new peak within tested horizon != no new peak ever
    bounded horizon stability != global closure
    response effectiveness != termination theorem
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/post_response_horizon_extension_audit_v0.json
    results/post_response_horizon_extension_audit_v0.md
    results/post_response_horizon_extension_audit_v0_certificate.json
