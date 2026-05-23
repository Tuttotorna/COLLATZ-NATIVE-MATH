# Native Grammar Transitions

Version: v3.2

This document defines allowed native grammar transitions.

A transition is a relation between native grammar objects.

## Primary transitions

expansion -> discharge

Meaning:

Every odd expansion calls for binary discharge.

## Debt transition

weak discharge -> debt

Meaning:

If discharge is insufficient relative to expansion pressure, debt is generated.

## Shadow transition

debt -> shadow

Meaning:

Debt may persist beyond local appearance.

## Compensation transition

debt -> compensation

Meaning:

Later discharge may repair prior debt.

## Regeneration transition

compensation -> regeneration

Meaning:

After repair, debt may reappear.

## Benign regeneration transition

regeneration -> compensation

Meaning:

Renewed debt can still be repaired.

## Dangerous regeneration transition

regeneration -> persistent shadow

Meaning:

Renewed debt may carry unresolved obstruction potential.

## Closure transition

compensation + shadow erasure + failed obstruction preservation -> closure

Meaning:

Closure occurs when obstruction potential is erased.

## Obstruction transition

debt + non-erased shadow + dangerous regeneration + insufficient compensation -> obstruction candidate

Meaning:

Obstruction is not stress alone.

Obstruction requires persistent unclosed debt.

## Forbidden transition

hardness -> obstruction

This transition is invalid.

Hardness measures stress.

Obstruction requires self-preserving unclosed debt.

## Forbidden transition

reaching 1 -> native closure

This transition is invalid.

Reaching 1 is a classical terminal translation.

Native closure is obstruction potential erased.
