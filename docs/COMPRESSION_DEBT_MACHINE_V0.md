# Compression Debt Machine V0

## Status

This document introduces a bounded measurement machine.

It is not a proof of Collatz.

It is not a claim that Collatz is solved.

It is not a theorem layer.

It is not a global closure claim.

It is not a global invariant claim.

It is a computable instrument for measuring compression debt, release, and regeneration in odd Collatz dynamics.

## Native purpose

The repository asks:

    What is Collatz before it becomes a conjecture?

The Compression Debt Machine makes one part of that question operational.

It transforms the native vocabulary:

    expansion
    discharge
    debt
    regeneration
    compensation
    obstruction

into bounded measurable quantities.

The goal is not to prove termination.

The goal is to measure whether a possible divergent behavior would need to preserve a low-compression regeneration grammar.

## Odd-step dynamics

For an odd integer n_i:

    3*n_i + 1 = 2^a_i * n_(i+1)

where:

    a_i = v2(3*n_i + 1)
    n_(i+1) = (3*n_i + 1) / 2^a_i

The value a_i is the local 2-adic discharge.

## Logarithmic drift

The exact odd-step logarithmic drift is:

    delta_i = log2(n_(i+1) / n_i)

Equivalently:

    delta_i = log2(3 + 1/n_i) - a_i

Interpretation:

    delta_i > 0  => expansion / debt creation
    delta_i = 0  => local balance
    delta_i < 0  => discharge / compression

For large n_i, the dominant threshold is:

    log2(3) ~= 1.584962500721156

So:

    a_i = 1  => usually expansion
    a_i = 2  => mild discharge
    a_i >= 3 => strong discharge

## Cumulative compression debt

For a window of k odd steps:

    D_k = sum(delta_i for i = 0..k-1)

Interpretation:

    D_k > 0  => the window accumulated net expansion
    D_k < 0  => the window discharged more than it expanded

The maximum cumulative value inside the window is the debt peak.

    debt_peak = max(prefix_sum(delta_i))

## Cheap regeneration chain

A cheap regeneration chain is a bounded odd-step window whose mean drift remains near non-negative.

Given tolerance epsilon >= 0:

    cheap_chain(window, epsilon) is true iff mean(delta_i) >= -epsilon

This is a bounded detector.

It does not imply divergence.

It only identifies windows where compression is locally insufficient or nearly insufficient.

## Release event

A release event is a step whose drift is strongly negative.

In V0:

    release_step        iff delta_i < -1
    strong_release_step iff delta_i < -2

Equivalently, for large odd values:

    a_i >= 3 usually produces release
    a_i >= 4 usually produces strong release

## Regeneration

Regeneration is the return of positive cumulative debt after a release.

In V0, a window is marked as regeneration-capable if:

    1. it reaches positive debt,
    2. then suffers a release,
    3. then returns to positive debt again.

This is a bounded grammatical detector.

It does not prove the existence of infinite regeneration.

## Native reduction

A possible divergent Collatz behavior would require more than local growth.

It would require an infinite low-compression regeneration grammar.

In V0 language:

    Collatz divergence would require unbounded persistence of cheap regeneration.

The Compression Debt Machine measures bounded approximations of such grammar.

## Obstruction candidate

An obstruction candidate is not a proof.

In V0, an obstruction candidate is a bounded empirical pattern where high debt peaks are followed by stronger future releases.

Informally:

    the trajectory creates debt,
    then the dynamics force discharge.

Computable form:

    debt_peak(window) high
    =>
    future_release_strength(window) high

This must remain bounded evidence only.

## Main falsifiable question

The first falsifiable question is:

    Do high-debt windows tend to be followed by stronger releases?

If yes, the debt/release language measures something structural.

If no, the vocabulary must be corrected.

## Boundary

    compression_debt_measurement != proof
    cheap_regeneration_detected != divergence
    release_detected != termination proof
    obstruction_candidate != obstruction theorem
    bounded evidence != global closure

## V0 output artifacts

The builder writes:

    results/compression_debt_machine_v0.json
    results/compression_debt_machine_v0.md
    results/compression_debt_machine_v0_certificate.json

The certificate preserves the non-proof boundary.
