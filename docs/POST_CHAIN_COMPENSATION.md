# Post-Chain Compensation

Post-chain compensation is the debt paid after a locally favorable regeneration chain.

In the native language:

    cheap regeneration creates escape capacity
    escape consumes shadow
    chain-compatible segments can remain temporarily below log2(3)
    collapse occurs when debt rises above the threshold

The main measurement is:

    compensation_surplus = post_chain_average_debt - log2(3)

If compensation_surplus > 0, then the chain has been overpaid by compression.

---

## Why this matters

A single cheap regeneration event does not threaten Collatz.

A single chain-compatible segment does not threaten Collatz.

A finite chain-compatible run is only dangerous if it can avoid later compensation.

Therefore v0.4 measures whether low-debt runs are followed by high-debt correction.

---

## Current status

This is not a proof.

It is an operational way to locate the structure that a proof would need to control:

    all low-debt regeneration chains must be finite
    and must be compensated by later debt.
