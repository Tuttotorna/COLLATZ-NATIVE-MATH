# Negative Search Result Boundary

Version: v2.5

This document defines how to interpret negative search results.

## Negative finite result

A negative finite result means:

no obstruction candidate was detected inside the selected finite search domain

## It does not mean

A negative finite result does not mean:

- Collatz is solved
- global closure is proved
- obstruction-preserving regeneration is impossible
- shadow always erases
- debt always erases
- finite evidence implies proof

## Correct interpretation

Negative finite results are evidence.

They support the native closure direction only inside the tested domain.

## Required reporting

Every negative result must report:

- search domain
- candidate generation rule
- tested trajectory count
- debt-window count
- regeneration count
- dangerous-regeneration count
- obstruction-candidate count
- proof status

## Proof status

The proof status must remain:

not_a_proof

until a general argument exists.

## Boundary sentence

No obstruction detected in a finite domain is not the same as no obstruction can exist.
