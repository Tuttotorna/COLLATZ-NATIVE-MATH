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

## v0.3 operational CRC form

v0.3 turns CRC into a finite diagnostic.

A locally cheap regeneration event is not enough.

The dangerous case is:

    locally cheap regeneration
    followed by another regeneration
    while the segment average debt remains <= log2(3)

Such an event is marked:

    chain_compatible = true

The long-term target becomes:

    no infinite sequence of chain_compatible regeneration events exists in N+.

## v0.4 collapse form

v0.4 adds the collapse form of CRC.

A chain-compatible segment is dangerous locally.

A finite chain-compatible run becomes less dangerous if followed by compensation:

    post_chain_average_debt > log2(3)

The long-term target becomes:

    every positive cheap regeneration chain is finite
    and every finite chain is eventually compensated by debt.

## v0.5 classified collapse form

v0.5 adds collapse cause classification.

A chain can collapse through:

    debt_spike
    shadow_exhaustion
    failed_regeneration
    post_chain_overcompensation
    terminal_descent

The CRC target becomes sharper:

    no infinite chain can avoid all collapse mechanisms forever.

## v0.6 refined collapse form

v0.6 refines the CRC obstruction vocabulary.

A chain can now collapse through:

    terminal_descent
    post_chain_overcompensation
    delayed_compensation
    debt_spike
    soft_debt_break
    failed_regeneration
    weak_regeneration
    shadow_exhaustion
    end_of_chain_without_escape

The refined CRC target is:

    no infinite chain can avoid the full collapse taxonomy forever.
