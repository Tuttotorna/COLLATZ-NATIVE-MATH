# Obstruction Search Result Types

Version: v2.5

This document defines result types for obstruction search.

## NO_DEBT_DETECTED

No debt window was found.

## DEBT_LOCALLY_RECOVERED

Debt was detected and locally compensated.

This is not full native closure.

## REGENERATED_BUT_COMPENSATED

Debt regenerated but renewed debt was compensated without preserving obstruction potential.

## DANGEROUS_REGENERATION_DETECTED

Regeneration appeared with persistent shadow, weakening compensation, or unresolved obstruction potential.

This is not obstruction by itself.

## OBSTRUCTION_CANDIDATE_DETECTED

All obstruction signature components were detected:

persistent debt
non-erased shadow
dangerous regeneration
insufficient compensation
no closure event
internal admissibility

## CLOSED

Obstruction potential was erased.

## UNDECIDED

The search did not have enough structural information to classify the case.

## Boundary

Only OBSTRUCTION_CANDIDATE_DETECTED is a native obstruction candidate result.

DANGEROUS_REGENERATION_DETECTED is a warning result, not a proof of obstruction.
