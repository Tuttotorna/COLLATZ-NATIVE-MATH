# Fuzzy Near-Breach Grammar Audit V0

## Status

This document introduces a bounded fuzzy near-breach grammar audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether approximate versions of the two near-breach grammars recur or concatenate inside bounded trajectories.

## Why this layer exists

Near-Breach Grammar Recurrence Audit V0 showed:

    exact Pattern A/B hits exist
    exact Pattern A/B recurrence does not appear
    exact Pattern A/B concatenation does not appear
    post-pattern debt gain is negative

But exact matching is strict.

A true dangerous grammar may appear as a variant.

This audit therefore searches for fuzzy near-breach grammars.

## Pattern A

    [3, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 4, 1, 2, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1]

## Pattern B

    [6, 1, 1, 1, 2, 1, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1]

## Fuzzy matching

For a candidate window and a pattern of equal length:

    hamming_distance = number of unequal a_i positions
    similarity = 1 - hamming_distance / pattern_length

A fuzzy hit is:

    similarity >= 0.85

V0 uses exact-length windows only.

## Measurements

For each measured odd seed:

    fuzzy_A_count
    fuzzy_B_count
    fuzzy_combined_count
    fuzzy_pattern_after_pattern
    fuzzy_recurrence_distance
    mean_similarity
    max_similarity
    post_fuzzy_pattern_debt_gain
    post_fuzzy_pattern_new_local_peak

## Boundary

    fuzzy_grammar_audit != proof
    fuzzy recurrence != counterexample
    no fuzzy recurrence observed != no fuzzy recurrence possible
    bounded fuzzy grammar != global invariant
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/fuzzy_near_breach_grammar_audit_v0.json
    results/fuzzy_near_breach_grammar_audit_v0.md
    results/fuzzy_near_breach_grammar_audit_v0_certificate.json
