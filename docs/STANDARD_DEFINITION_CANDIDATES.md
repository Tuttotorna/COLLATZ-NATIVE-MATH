# Standard Definition Candidates

Version: v2.1

This document introduces candidate standard definitions for the native objects.

These are not theorems.

These are not proof claims.

They are controlled translation candidates.

Every definition must remain reversible:

    native object -> standard definition candidate -> native meaning retained

If reversibility fails, the definition is invalid for this project.

## Definition candidate: odd block

Native object:

    odd block

Candidate standard definition:

For an odd positive integer n, define:

    T(n) = (3n + 1) / 2^a

where:

    a = v2(3n + 1)

and T(n) is odd.

The pair:

    (n, a)

is one odd block.

Native meaning retained:

    one expansion event followed by one discharge event.

## Definition candidate: discharge exponent

Native object:

    discharge

Candidate standard definition:

    a(n) = v2(3n + 1)

where v2(m) is the largest exponent a such that 2^a divides m.

Native meaning retained:

    local reduction strength after expansion.

## Definition candidate: expansion pressure

Native object:

    expansion

Candidate standard definition:

The expansion pressure of an odd block is represented by:

    log2(3)

Native meaning retained:

    the upward structural force introduced by multiplication by 3.

## Definition candidate: debt

Native object:

    debt

Candidate standard definition:

A block contributes debt when its discharge exponent is insufficient relative to expansion pressure.

Candidate local debt:

    d(n) = log2(3) - a(n)

A positive value means under-discharge.

Native meaning retained:

    structural burden created by insufficient discharge.

## Definition candidate: cumulative debt

Native object:

    debt chain

Candidate standard definition:

For a finite sequence of odd blocks n0, n1, ..., nk, define cumulative debt over an interval I:

    D(I) = sum over i in I of (log2(3) - a(ni))

Native meaning retained:

    accumulated burden across a contiguous native structure.

## Definition candidate: bad window

Native object:

    bad window

Candidate standard definition:

A finite interval I of odd blocks is a bad window when:

    average a over I < log2(3)

Equivalently:

    D(I) > 0

Native meaning retained:

    local obstruction candidate.

## Definition candidate: compensation

Native object:

    compensation

Candidate standard definition:

A later interval J compensates an earlier bad window I when the combined interval I union J satisfies:

    average a over I union J > log2(3)

Equivalently:

    D(I union J) < 0

Native meaning retained:

    later discharge repairs prior debt.

## Definition candidate: surplus

Native object:

    surplus

Candidate standard definition:

For a compensated interval K, surplus is:

    S(K) = average a over K - log2(3)

Positive surplus means the interval is above escape pressure.

Native meaning retained:

    remaining positive compensation margin.

## Definition candidate: shadow

Native object:

    shadow

Candidate standard definition:

A shadow exists when a prior debt interval continues to influence later admissibility after local compensation.

Candidate standard form:

    A debt interval I has shadow into later interval L if later instability measures depend on I's prior deficit structure.

Native meaning retained:

    memory of unresolved danger.

## Definition candidate: regeneration

Native object:

    regeneration

Candidate standard definition:

Regeneration occurs when, after a compensated interval, a later interval again satisfies the bad-window condition.

Native meaning retained:

    renewed danger after apparent recovery.

## Definition candidate: obstruction candidate

Native object:

    obstruction candidate

Candidate standard definition:

An obstruction candidate is an admissible sequence of odd blocks for which debt persists, shadow is not erased, regeneration continues, and no sufficient compensation condition is reached.

Native meaning retained:

    self-preserving unclosed debt.

## Definition candidate: closure candidate

Native object:

    closure

Candidate standard definition:

A closure candidate is a finite structural condition showing that obstruction potential is erased:

    debt generated
    shadow tracked
    compensation sufficient
    shadow erased
    regeneration tested
    no self-preserving debt remains

Native meaning retained:

    obstruction potential erased.

## Status

These definitions are candidates.

They prepare the standard layer.

They do not prove the Collatz conjecture.
