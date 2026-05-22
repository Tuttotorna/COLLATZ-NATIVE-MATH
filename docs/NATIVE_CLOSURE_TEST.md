# Native Closure Test

Version: v1.8

This document defines the native closure test.

The test is not a standard proof.
The test is a structural checklist.

## Closure test question

When is debt no longer dangerous?

A debt structure is no longer dangerous when it cannot preserve obstruction potential after compensation and regeneration testing.

## Required stages

The native closure test has seven stages:

1. Detect debt.
2. Track debt shadow.
3. Detect compensation.
4. Measure compensation sufficiency.
5. Test shadow erasure.
6. Test regeneration.
7. Decide obstruction erasure.

## Stage 1: Detect debt

Debt exists when local discharge is insufficient relative to expansion pressure.

This does not mean failure.
It means local danger.

## Stage 2: Track debt shadow

Debt shadow exists when the effect of a debt structure persists after the local debt event.

Shadow is the memory of danger inside the trajectory.

## Stage 3: Detect compensation

Compensation appears when later discharge repairs the bad structure.

Compensation is necessary but not sufficient for closure.

## Stage 4: Measure compensation sufficiency

Compensation is sufficient when the combined structure has positive surplus strong enough to remove obstruction potential.

A tiny positive surplus can recover locally, but it may still require regeneration testing.

## Stage 5: Test shadow erasure

Shadow erasure occurs when the prior debt no longer constrains the later trajectory as an obstruction carrier.

## Stage 6: Test regeneration

Regeneration testing asks whether dangerous debt reappears in a self-preserving form.

Regeneration alone is not failure.
Dangerous regeneration is regeneration that avoids closure.

## Stage 7: Decide obstruction erasure

Obstruction erasure occurs when no persistent unclosed debt structure remains.

## Native closure result types

The closure test may return:

- CLOSED
- LOCALLY_RECOVERED_NOT_CLOSED
- REGENERATED_BUT_COMPENSATED
- OBSTRUCTION_CANDIDATE
- UNDECIDED

## Interpretation

CLOSED means obstruction potential was erased.

OBSTRUCTION_CANDIDATE means debt persists, regenerates, and avoids sufficient compensation.

UNDECIDED means the native test boundary is not yet strong enough.
