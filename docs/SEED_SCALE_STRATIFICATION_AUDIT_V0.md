# Seed-Scale Stratification Audit V0

## Status

This document introduces a bounded seed-scale stratification audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It separates cumulative seed-scale decay from local block-level behavior.

## Why this layer exists

Residual Decay Audit V0 showed that the primary release-pressure signal weakens mainly along the seed-scale axis.

However, cumulative seed-scale measurement can hide two different phenomena:

    1. true local weakening in higher seed regions
    2. dilution caused by mixing heterogeneous seed blocks into one cumulative pool

Therefore the next question is:

    Does the release-pressure signal decay inside local seed blocks,
    or does it only decay when blocks are accumulated together?

## Native question

The native question is:

    Is seed-scale decay local, or cumulative?

## Primary signal

The primary signal remains:

    debt_peak_vs_post_peak_release_mass_h_pearson

Interpretation:

    higher debt peaks are followed by proportionally stronger post-peak release mass

## Cumulative vs block signal

The audit measures two signal families.

### Cumulative signal

For cumulative ranges:

    1..999
    1..1999
    1..2999
    1..3999
    1..4999
    1..5999

### Local block signal

For non-overlapping seed blocks:

    1..999
    1001..1999
    2001..2999
    3001..3999
    4001..4999
    5001..5999

Only odd seeds are measured.

## Key distinction

If cumulative signal decays but block signal remains positive:

    seed-scale decay is probably a mixing/dilution effect

If both cumulative and block signal decay:

    seed-scale decay is probably local

If block signal oscillates:

    seed-scale behavior is heterogeneous

## Boundary

    seed_scale_stratification != proof
    block_signal != theorem
    cumulative_decay != global law
    positive block signal != invariant
    no zero crossing in tested blocks != universal closure

## V0 output artifacts

The builder writes:

    results/seed_scale_stratification_audit_v0.json
    results/seed_scale_stratification_audit_v0.md
    results/seed_scale_stratification_audit_v0_certificate.json
