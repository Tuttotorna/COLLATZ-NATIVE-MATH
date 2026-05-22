# Native Failure Condition

Version: v1.7

This document defines what would count as failure for the native method.

The native method does not fail merely because a trajectory is long.
The native method does not fail merely because a case is hard.
The native method fails if it cannot distinguish stress from obstruction.

## Failure condition

The native method fails if it cannot define a structural difference between:

- a long but compensated trajectory
- and a true non-compensating debt structure

A useful native method must expose that distinction.

## Strong native failure

A strong native failure would be the discovery of a candidate with:

1. persistent debt
2. persistent shadow
3. repeated regeneration
4. no compensating discharge
5. no closure event
6. no finite recovery under the defined native protocol

Such a case would not automatically prove a classical counterexample.
But it would defeat the current native closure direction.

## Weak native failure

A weak native failure occurs if the model remains only descriptive.

For example:

- naming debt without measuring it
- naming compensation without defining recovery
- naming shadow without defining persistence
- naming closure without defining its opposite

The v1.7 obstruction model exists to prevent this.

## What does not count as failure

The following do not count as native failure:

- a larger hard number
- a longer trajectory
- a tighter surplus
- a bigger finite scan
- a different hardest case under a different metric

These may reveal stress, but not necessarily obstruction.

## Native requirement

Every native primitive must eventually support one of two outcomes:

- closure is forced
- obstruction is structurally possible

If a primitive does neither, it is not useful.
