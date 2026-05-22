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

## v0.7 compensation form

v0.7 turns CRC into a compensation-window search.

A dangerous chain has:

    chain_average_debt <= log2(3)

The compensating event is the first future window from the chain start with:

    recovery_average_debt > log2(3)

The refined CRC target becomes:

    no infinite chain can avoid finite recovery above log2(3).

## v0.8 post-chain recovery form

v0.8 refines the compensation form.

The earlier recovery window started at:

    chain_start_block

The stricter window starts at:

    chain_end_block + 1

The CRC target becomes:

    no finite cheap regeneration chain can be extended into an unrecovered post-chain escape window indefinitely.

## v0.9 hard recovery form

v0.9 adds hard recovery ranking.

The refined CRC target becomes:

    if every finite cheap chain recovers,
    the hardest recovered chains should reveal the limiting obstruction.

Hard cases are ranked by:

    long recovery distance
    small recovery surplus
    large chain deficit
    large recovery gap
    high combined hardness score

## v1.0 critical case form

v1.0 focuses the CRC target onto one critical recovered case.

The refined question becomes:

    can the critical recovery pattern be generalized or bounded?

If the pattern can be made arbitrarily long without recovery, the CRC direction fails.

If the pattern cannot be extended indefinitely, it may become a lemma candidate.

## v1.1 frontier form

v1.1 reframes the CRC search as a frontier problem.

Instead of asking only:

    does one hard case recover?

it asks:

    how does hardness move across nearby and structured candidates?

The relevant obstruction is no longer a single recovery event.

The relevant obstruction is whether recovery hardness can grow without bound.
