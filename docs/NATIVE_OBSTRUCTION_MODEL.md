# Native Obstruction Model

Version: v1.7

This document defines what a native obstruction would have to be.

A native obstruction is not simply a large number.
A native obstruction is not simply a long trajectory.
A native obstruction is not simply a hard case under one metric.

A native obstruction is a self-preserving debt structure that avoids forced compensation.

## Core definition

A native obstruction is a trajectory structure with all of the following properties:

1. Debt is generated.
2. Debt persists.
3. The debt shadow is not erased.
4. Regeneration occurs.
5. Compensation is insufficient.
6. No closure event is forced.
7. The structure remains internally admissible.

In short:

    A native obstruction is persistent unclosed debt.

## Native obstruction versus classical counterexample

A classical Collatz counterexample is usually framed as:

- a trajectory that never reaches 1
- or a non-trivial cycle

The native method reframes the target.

The native target is:

    Can there exist a self-preserving debt structure that never forces compensating discharge?

If no such structure can exist, native closure becomes plausible.
If such a structure can exist, it becomes the correct obstruction candidate.

## Necessary components

A native obstruction requires:

- a debt chain
- a shadow carrier
- regeneration
- compensation avoidance
- closure failure

If any one of these fails, the obstruction fails natively.

## Not enough for obstruction

The following are not enough:

- high stopping time
- high odd-block count
- high hardness score
- tight positive surplus
- long post-chain recovery
- many bad windows
- local instability

These are stress indicators.
They are not native obstructions.

## Obstruction standard

A candidate becomes a native obstruction candidate only when it shows:

- debt persistence beyond local recovery
- regeneration after apparent compensation
- no forced surplus restoration
- no detected closure event
- no collapse into known recovered behavior

## Current evidence status

Existing scans found many hard structures, but no unrecovered bad-window structure inside the selected finite candidate sets.

This supports the native research path.

It does not prove global closure.

## Central question

Can debt regenerate forever without ever forcing compensating discharge?

That is the native obstruction question.
