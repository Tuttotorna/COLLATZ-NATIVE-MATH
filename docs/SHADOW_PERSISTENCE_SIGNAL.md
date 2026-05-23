# Shadow Persistence Signal

Version: v2.9

This document defines the shadow persistence signal used by the v2.9 instrumentation layer.

## Shadow persistence

A shadow persistence signal exists when a case shows multiple signs that prior debt may still be structurally relevant after compensation.

The v2.9 signal uses bounded indicators:

- debt windows exist;
- regeneration exists;
- dangerous regeneration exists;
- positive surplus is tight;
- recovery distance is long;
- recovery stress is high;
- dangerous regeneration samples exist.

## Strong signal

A strong signal is reported when dangerous regeneration combines with tight surplus, long recovery, or high recovery stress.

## Weak signal

A weak signal is reported when dangerous regeneration exists but without enough additional evidence of persistent shadow.

## No signal

No signal is reported when debt does not regenerate or when no dangerous regeneration appears.

## Important boundary

A shadow persistence signal is not obstruction.

A signal says:

look here more carefully

It does not say:

this is a counterexample

It does not say:

global closure fails
