# Local Debt Lemma Candidates

Version: v2.2

This document introduces local debt lemma candidates.

These are not theorems.
These are not proof claims.
They are candidate statements prepared after v2.1 definitions.

Every lemma candidate must remain reversible:

native object -> standard definition -> lemma candidate -> native meaning retained

If native meaning is lost, the lemma candidate is invalid.

## Lemma candidate 1: odd block decomposition

Native object:

odd block

Candidate statement:

For every odd positive integer n, there exists a unique integer a >= 1 such that:

3n + 1 = 2^a m

where m is odd.

The odd-block transition is:

n -> m

Native meaning retained:

one expansion event followed by one discharge event.

Status:

stable lemma candidate.

## Lemma candidate 2: discharge exponent uniqueness

Native object:

discharge

Candidate statement:

For every odd positive integer n, the discharge exponent:

a(n) = v2(3n + 1)

is uniquely determined.

Native meaning retained:

local reduction strength after expansion.

Status:

stable lemma candidate.

## Lemma candidate 3: local debt formation

Native object:

local debt

Candidate statement:

For an odd block n, define:

d(n) = log2(3) - a(n)

If d(n) > 0, the block creates local debt.
If d(n) <= 0, the block does not create positive local debt.

Native meaning retained:

structural burden created by insufficient discharge.

Status:

stable lemma candidate.

## Lemma candidate 4: local debt is not obstruction

Native object:

debt

Candidate statement:

The existence of local debt at one block is not sufficient to define an obstruction candidate.

Native meaning retained:

debt is local danger, not global failure.

Status:

boundary lemma candidate.

## Lemma candidate 5: cumulative debt over an interval

Native object:

debt chain

Candidate statement:

For a finite interval I of odd blocks, cumulative debt is:

D(I) = sum over i in I of (log2(3) - a_i)

If D(I) > 0, the interval has net debt.
If D(I) <= 0, the interval has no positive net debt.

Native meaning retained:

accumulated structural burden across a finite native structure.

Status:

stable lemma candidate.

## Lemma candidate 6: debt requires interval context

Native object:

debt chain

Candidate statement:

A single local debt event can be neutralized by later discharge.
Therefore obstruction cannot be inferred from a single positive local debt value.

Native meaning retained:

obstruction requires persistence, not isolated stress.

Status:

boundary lemma candidate.

## Current status

The local debt layer is definitionally stable.

It is still not a proof layer.
