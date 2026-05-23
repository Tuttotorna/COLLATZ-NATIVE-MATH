# Mature Rebound Guard V0

## Status

This document introduces a bounded guard layer over fuzzy rebound anatomy.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It corrects an important ambiguity exposed by Fuzzy Rebound Anatomy V0.

## Why this layer exists

Fuzzy Rebound Anatomy V0 detected two `breach_after_fuzzy_pattern` cases.

However, both were caused by a weak prior debt peak.

That means the raw ratio:

    post_horizon_max_prefix / prior_debt_peak

can become large when the denominator is structurally weak.

So the word `breach` must be guarded.

A rebound that exceeds a small early prefix is not the same as a rebound that exceeds a mature debt peak.

## Native distinction

The guard separates:

    weak-prefix rebound

from:

    mature-debt rebound

A weak-prefix rebound may grow locally.

A mature-debt rebound would challenge the near-breach isolation result.

## Mature prior peak threshold

V0 uses:

    mature_prior_peak_threshold = 4.0

A rebound is mature only if:

    prior_debt_peak >= 4.0

Otherwise it is classified as weak-prefix rebound.

## Guarded classification

Raw v6.3 labels are preserved.

Guarded v6.4 labels are added:

    weak_prefix_rebound
    weak_prefix_false_breach
    mature_harmless_rebound
    mature_second_near_breach_candidate
    mature_breach_after_fuzzy_pattern

## Core question

The bounded question is:

    Do any fuzzy rebounds exceed a mature prior debt peak?

If no, the v6.3 breach signal was a weak-prefix artifact.

If yes, the near-breach grammar boundary must be reopened.

## Boundary

    mature_rebound_guard != proof
    weak-prefix false breach != theorem
    no mature breach observed != no mature breach possible
    bounded guard != global closure
    Collatz status remains unsolved

## V0 output artifacts

The builder writes:

    results/mature_rebound_guard_v0.json
    results/mature_rebound_guard_v0.md
    results/mature_rebound_guard_v0_certificate.json
