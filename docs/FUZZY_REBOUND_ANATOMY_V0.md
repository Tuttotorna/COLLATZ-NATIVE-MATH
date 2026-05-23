# Fuzzy Rebound Anatomy V0

## Status

This document introduces a bounded fuzzy rebound anatomy audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It studies fuzzy near-breach grammar instances that produce post-pattern local growth.

## Why this layer exists

Fuzzy Near-Breach Grammar Audit V0 showed:

    fuzzy recurrence does not appear
    fuzzy pattern-after-pattern does not appear
    dangerous fuzzy chains do not appear
    but 3 fuzzy pattern instances produce post-pattern local growth

Therefore the next question is not whether a chain exists.

The next question is what those rebound cases are.

## Native question

The native question is:

    Are fuzzy rebound cases harmless isolated rebounds,
    or do they approach a second near-breach boundary?

## Measurements

For every fuzzy A/B instance with post-pattern local growth, this audit records:

    seed
    pattern type
    position
    window
    hamming_distance
    similarity
    pattern_start_prefix
    pattern_end_prefix
    post_horizon_max_prefix
    post_pattern_debt_gain
    post_pattern_new_local_peak
    prior_debt_peak
    post_max_to_prior_peak_ratio
    gap_to_prior_peak
    after_pattern_a_sequence
    after_pattern_delta_sequence
    after_pattern_prefix_sequence
    next_release_delay
    second_near_breach_candidate

## Classification

A rebound is classified as:

    harmless_rebound:
        post-pattern growth exists but remains far below prior peak

    near_peak_rebound:
        post-pattern growth approaches prior peak

    second_near_breach_candidate:
        post-pattern growth reaches at least 95% of prior peak

    breach_after_fuzzy_pattern:
        post-pattern growth exceeds prior peak

## Boundary

    fuzzy_rebound_anatomy != proof
    local rebound != counterexample
    no second breach observed != no second breach possible
    bounded rebound anatomy != global invariant
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/fuzzy_rebound_anatomy_v0.json
    results/fuzzy_rebound_anatomy_v0.md
    results/fuzzy_rebound_anatomy_v0_certificate.json
