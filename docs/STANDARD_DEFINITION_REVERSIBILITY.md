# Standard Definition Reversibility

Version: v2.1

This document defines the reversibility rule for v2.1 definitions.

## Core rule

A standard definition is valid only if it maps back to a native object without losing the native meaning.

Required form:

    native object -> standard definition candidate -> native meaning retained

## Invalid definition

A definition is invalid if it:

- hides the native object;
- replaces native structure with unrelated classical notation;
- turns evidence into proof;
- treats hardness as obstruction;
- treats reaching 1 as native closure;
- treats local recovery as full closure;
- removes shadow or regeneration from the model.

## Valid definition

A definition is valid if it:

- preserves the native object;
- gives a standard measurable form;
- keeps the native interpretation visible;
- remains reversible;
- avoids theorem claims;
- avoids proof claims.

## Why reversibility matters

The project already drifted too early into classical mathematics once.

v2.1 prevents that drift.

Standard language may now re-enter, but only as reversible translation.

## Practical test

For every standard statement, ask:

    What native object does this statement preserve?

If the answer is unclear, the statement is not acceptable yet.
