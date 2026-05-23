# Near-Breach Anatomy V0

## Status

This document introduces a bounded near-breach anatomy audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It studies the internal structure of the strongest near-breach trajectories found by the previous audit.

## Why this layer exists

Near-Breach Audit V0 showed:

    breach_count = 0
    max_regeneration_ratio = 0.9943395958105086
    min_gap_to_breach = 0.00566040418949143

The strongest cases do not cross the old post-release peak threshold.

But they come very close.

This audit asks what their internal grammar looks like.

## Native question

The native question is:

    What sequence structure allows a trajectory to regenerate almost all post-response debt
    without crossing the previous debt peak?

## Anatomy fields

For each selected seed, the audit extracts:

    odd trajectory
    a_i sequence
    delta_i sequence
    prefix_debt sequence
    peak_index
    response_index
    post_response_max_index
    response_delay
    time_to_post_response_max
    regeneration_ratio
    gap_to_breach

## Window extraction

For each candidate, the audit extracts three local windows:

    pre_peak_window
    peak_to_response_window
    response_to_post_max_window

The goal is to expose:

    local expansion grammar
    discharge grammar
    regeneration grammar

## Comparison

The audit compares top near-breach seeds against deterministic control seeds.

Controls are chosen from the same measured domain but away from the near-breach top set.

The comparison measures:

    mean a
    a=1 rate
    a>=3 rate
    positive delta rate
    release rate
    strong release rate
    prefix peak
    trajectory odd length
    regeneration ratio

## Boundary

    near_breach_anatomy != proof
    repeated pattern != theorem
    near-breach grammar != counterexample
    bounded anatomy != global invariant
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/near_breach_anatomy_v0.json
    results/near_breach_anatomy_v0.md
    results/near_breach_anatomy_v0_certificate.json
