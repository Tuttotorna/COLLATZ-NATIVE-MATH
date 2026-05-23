# Distributed Release Pressure V0

## Status

This document introduces a bounded measurement layer after Compression Debt Machine V0.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global invariant claim.

It measures how release events are distributed after compression debt peaks.

## Why this layer exists

Compression Debt Machine V0 showed a useful distinction.

High debt peak did not strongly correlate with one single maximum discharge.

High debt peak correlated more strongly with the number of release events.

This suggests a different native hypothesis:

    debt is not necessarily cancelled by one maximal collapse
    debt may generate distributed release pressure

## Native question

After a trajectory reaches a debt peak, how quickly does the next release arrive, and how much release pressure appears after the peak?

## Odd-step drift

For odd n_i:

    3*n_i + 1 = 2^a_i * n_(i+1)

where:

    a_i = v2(3*n_i + 1)

The exact odd-step logarithmic drift is:

    delta_i = log2(n_(i+1) / n_i)

Interpretation:

    delta_i > 0  => debt creation
    delta_i < -1 => release
    delta_i < -2 => strong release

## Debt peak

For a bounded odd-step trajectory, define prefix debt:

    P_j = sum(delta_i for i = 0..j)

The debt peak is:

    debt_peak = max(P_j)

The peak index is the first index where this maximum is reached.

## Response delay

The release response delay is the number of odd steps between the debt peak and the first later release event.

In V0:

    release event iff delta_i < -1

So:

    response_delay = first index t > peak_index where delta_t < -1

If no later release exists inside the bound:

    response_delay = null

## Post-peak release pressure

For a fixed horizon H after the peak:

    post_peak_release_count_H
    post_peak_strong_release_count_H
    post_peak_release_mass_H

where:

    release_mass = sum(abs(delta_i) for post-peak delta_i < -1)

This measures not just whether discharge happens, but whether discharge pressure is distributed after debt creation.

## Pressure hypothesis

The bounded hypothesis is:

    high debt peaks are followed by short response delays
    or by higher post-peak release pressure

This is not a proof.

It is a detector for a possible native law:

    debt creates local release pressure

## Boundary

    distributed_release_pressure != proof
    short_response_delay != termination theorem
    post_peak_release_mass != global invariant
    bounded pressure signal != global closure
    no pressure found != counterexample

## V0 output artifacts

The builder writes:

    results/distributed_release_pressure_v0.json
    results/distributed_release_pressure_v0.md
    results/distributed_release_pressure_v0_certificate.json
