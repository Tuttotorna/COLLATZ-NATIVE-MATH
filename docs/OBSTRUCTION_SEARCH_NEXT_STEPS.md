# Obstruction Search Next Steps

Version: v2.5

This document defines the next logical step after the v2.5 protocol.

## Current state

v2.5 defines the obstruction search protocol.

It does not run the obstruction search yet.

## Recommended next version

v2.6 Bounded Obstruction Search Scanner

## v2.6 purpose

The next scanner should:

1. load existing trajectory candidate sets
2. compute debt windows
3. detect regeneration after compensation
4. classify regeneration
5. count dangerous regeneration
6. attempt obstruction candidate classification
7. produce a bounded negative-result certificate

## What v2.6 must not claim

v2.6 must not claim:

- Collatz solved
- global closure proved
- obstruction impossible
- finite search equals proof

## Correct v2.6 output

The correct v2.6 output is a bounded obstruction-search certificate.

Not a theorem.
Not a proof.
Not a global closure claim.
