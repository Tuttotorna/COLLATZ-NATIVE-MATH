# Near-Breach Audit V0

## Status

This document introduces a bounded near-breach audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It searches for the trajectories that come closest to violating the post-response no-new-peak condition.

## Why this layer exists

Post-Response Horizon Extension Audit V0 showed:

    no post-response new peak appeared across tested horizons
    p_new_peak_after_release remained 0
    max regeneration ratio reached 0.9943395958105086

This means the important cases are not failures.

The important cases are near-failures.

## Native question

The native question is:

    Which seeds come closest to regenerating a new post-response debt peak?

## Near-breach definition

For a trajectory with a post-response maximum:

    regeneration_ratio = post_response_max_debt / debt_peak

A true breach would be:

    regeneration_ratio > 1

A near-breach is:

    regeneration_ratio close to 1 from below

Define:

    gap_to_breach = 1 - regeneration_ratio

Lower gap means closer to breach.

## Measurements

The audit records top near-breach candidates:

    seed
    debt_peak
    peak_index
    response_index
    response_delay
    debt_after_first_release
    survival_ratio
    post_response_max_debt
    regeneration_ratio
    gap_to_breach
    time_to_post_response_max
    odd_steps
    terminated

It also measures whether near-breach severity grows with seed scale.

## Boundary

    near_breach_audit != proof
    no breach observed != no breach possible
    near-breach candidate != counterexample
    bounded gap != global invariant
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/near_breach_audit_v0.json
    results/near_breach_audit_v0.md
    results/near_breach_audit_v0_certificate.json
