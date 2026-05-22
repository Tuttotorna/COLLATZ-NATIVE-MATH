# Standard Translation Boundary

Version: v1.6

This document defines when standard mathematics is allowed to re-enter the project.

## Rule

Standard mathematical language should re-enter only after the native structure has been exposed.

The standard layer is a translation layer, not the source layer.

## Why this boundary exists

The classical Collatz problem already imposes a frame:

- integer iteration
- parity split
- stopping time
- convergence to 1
- proof by standard inequalities or modular structure

Those are legitimate tools.

But they may hide the structural mechanism that the native method is trying to isolate.

The native method first asks what the trajectory itself is doing.

Only later should the result be translated into standard proof language.

## Allowed before native closure

Before native closure is defined, standard mathematics may be used only as instrumentation:

- exact arithmetic
- deterministic computation
- reproducible scans
- JSON result artifacts
- regression tests
- bounded finite certificates

## Not allowed before native closure

Before native closure is defined, the project should avoid presenting the native method as if it were already a conventional proof.

Avoid:

- premature theorem claims
- premature proof claims
- over-reduction to classical inequalities
- hiding native objects behind standard notation
- treating computational evidence as proof

## Allowed after native closure

After the native closure criterion is defined, standard mathematics may be used to translate:

- native primitives into definitions
- native compensation into inequalities
- native obstruction absence into lemmas
- native closure into theorem-like form

## Summary

The standard layer is necessary.

But it comes later.

The native layer must be completed first.
