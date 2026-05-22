# Closure Result Types

Version: v2.4

This document defines result types for native closure analysis.

## CLOSED

Meaning:

Obstruction potential is erased.

Required native structure:

debt detected, compensation sufficient, shadow erased, regeneration tested, no self-preserving debt remains.

## LOCALLY_RECOVERED_NOT_CLOSED

Meaning:

A bad window recovered locally, but full native closure was not established.

Reason:

shadow erasure or regeneration testing is incomplete.

## REGENERATED_BUT_COMPENSATED

Meaning:

Debt regenerated, but renewed debt was compensated without preserving obstruction potential.

Reason:

regeneration occurred but remained benign or compensated.

## DANGEROUS_REGENERATION

Meaning:

Regeneration occurred with persistent shadow, weakening compensation, or unresolved obstruction potential.

Reason:

closure requires further testing.

## OBSTRUCTION_CANDIDATE

Meaning:

Persistent debt, non-erased shadow, dangerous regeneration, insufficient compensation, no closure event, and internal admissibility are all present.

Reason:

this is the native counterexample target.

## UNDECIDED

Meaning:

The available native or evidence layer is insufficient to classify closure.

Reason:

definition, measurement, or evidence boundary is incomplete.

## Boundary

Only CLOSED means native closure.

Local recovery, positive surplus, and benign compensation are not automatically full closure.
