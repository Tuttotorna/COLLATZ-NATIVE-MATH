# Compensation Formalization

Version: v3.0

This document drafts formal compensation statements.

## Draft C1: bad window equivalence

Native object:

bad window

Draft statement:

A finite interval I of odd blocks is a bad window if and only if its average discharge is below log2(3).

Equivalently:

D(I) > 0

Native meaning retained:

local obstruction candidate.

Status:

stable draft.

## Draft C2: compensation recovery

Native object:

compensation

Draft statement:

A later interval J compensates a bad window I when the combined interval K = I followed by J satisfies:

average discharge over K > log2(3)

Equivalently:

D(K) < 0

Native meaning retained:

later discharge repairs prior debt.

Status:

stable draft.

## Draft C3: positive surplus

Native object:

surplus

Draft statement:

For a compensated interval K, define:

S(K) = average discharge over K - log2(3)

If S(K) > 0, the interval has positive surplus.

Native meaning retained:

positive compensation margin after repair.

Status:

stable draft.

## Draft C4: local recovery is not closure

Native object:

closure boundary

Draft statement:

Positive surplus after compensation establishes local recovery of the measured interval, but does not by itself establish native closure.

Native meaning retained:

local recovery does not equal obstruction erasure.

Status:

stable boundary draft.

## Boundary

Compensation is necessary for closure, but compensation alone is not full closure.

Shadow and regeneration must still be tested.
