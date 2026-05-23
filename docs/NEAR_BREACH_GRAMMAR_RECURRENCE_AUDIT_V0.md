# Near-Breach Grammar Recurrence Audit V0

## Status

This document introduces a bounded near-breach grammar recurrence audit.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It tests whether the two near-breach grammars discovered in Near-Breach Anatomy V0 recur inside trajectories.

## Why this layer exists

Near-Breach Anatomy V0 found two dominant post-response grammars:

Pattern A:

    [3, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 4, 1, 2, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1]

Pattern B:

    [6, 1, 1, 1, 2, 1, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1]

The next question is whether these grammars are isolated episodes or recurring structures.

## Native question

The native question is:

    Can near-breach grammars concatenate?

If they are isolated, the trajectory absorbs the quasi-failure.

If they recur and restart debt growth, they may expose the dangerous grammar.

## Measurements

For each measured odd seed, the audit extracts the full odd-step a-sequence and searches for:

    pattern_A_count
    pattern_B_count
    pattern_A_positions
    pattern_B_positions
    combined_pattern_count
    pattern_after_pattern
    min_distance_between_patterns
    post_pattern_debt_gain
    post_pattern_new_local_peak

## Pattern matching

Patterns are exact a-sequence matches.

This is intentionally strict.

A later version may test fuzzy or approximate matches.

## Boundary

    grammar_recurrence != proof
    pattern recurrence != counterexample
    no recurrence observed != no recurrence possible
    bounded recurrence search != global invariant
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/near_breach_grammar_recurrence_audit_v0.json
    results/near_breach_grammar_recurrence_audit_v0.md
    results/near_breach_grammar_recurrence_audit_v0_certificate.json
