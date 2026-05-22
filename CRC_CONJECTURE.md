# CRC Conjecture

CRC means Cheap Regeneration Chain.

## Informal statement

No positive odd Collatz trajectory can sustain an infinite cheap regeneration chain.

## Native formulation

A positive odd trajectory can escape only if it repeatedly does the following:

    regenerate 2-adic shadow of -1
    consume that shadow through a = 1 escape steps
    regenerate it again
    consume it again
    ...

while keeping the average compression debt at or below the escape threshold:

    average(a_i) <= log2(3)

The CRC conjecture says:

    this cannot happen in positive odd Collatz dynamics.

## Relation to Collatz

If every positive odd trajectory fails to sustain an infinite cheap regeneration chain, then every escaping trajectory is excluded.

This would reduce Collatz to the impossibility of infinite cheap regeneration.

## Current status

This is not proved.

This repository only formalizes and tests the language.
