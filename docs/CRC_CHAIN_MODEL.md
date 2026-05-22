# CRC Chain Model

CRC means Cheap Regeneration Chain.

The model:

    shadow is regenerated
    shadow is consumed by local escape
    shadow must be regenerated again
    the chain is dangerous only if this can continue indefinitely at low average debt

---

## Definitions

For a positive odd Collatz trajectory:

    3 n_i + 1 = 2^(a_i) n_(i+1)

define:

    a_i = v2(3 n_i + 1)
    s_i = v2(n_i + 1)

A regeneration event is:

    s_(i+1) > s_i

Regenerated shadow:

    R_i = s_(i+1) - s_i

Compression cost:

    C_i = max(1, a_i - 1)

Cheapness ratio:

    Q_i = R_i / C_i

A regeneration is flagged as locally cheap when:

    Q_i >= 1 / (log2(3) - 1)

Numerically:

    1 / (log2(3) - 1) ~= 1.7095

---

## Chain condition

A cheap regeneration chain is a sequence of regeneration events where each regeneration is followed by another regeneration before the accumulated debt becomes clearly compressive.

v0.3 does not claim to fully formalize infinity.

It builds finite chain diagnostics.

The key finite diagnostic is:

    Does the segment between two regeneration events keep average debt <= log2(3)?

If yes, the segment is chain-compatible.

If no, the chain is broken by debt.

---

## Native reduction

The intended native reduction is:

    Collatz true
    <=>
    every positive cheap regeneration chain is finite

or, more operationally:

    no positive trajectory can sustain chain-compatible regeneration forever.
