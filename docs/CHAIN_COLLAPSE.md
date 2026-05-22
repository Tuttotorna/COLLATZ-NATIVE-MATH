# Chain Collapse Analysis

v0.4 studies where finite cheap regeneration chains break.

v0.3 showed that local cheap regeneration can create chain-compatible segments.

Therefore the target moved again.

The false target is:

    no chain-compatible segment exists

The correct target is:

    no infinite chain-compatible sequence exists in positive odd Collatz dynamics.

v0.4 asks:

    where does a compatible chain collapse?
    what debt event breaks it?
    does post-chain compensation push average debt above log2(3)?

---

## Chain-compatible segment

A regeneration segment is chain-compatible when:

    the regeneration is locally cheap
    another regeneration follows
    the segment average debt is <= log2(3)

Such a segment is dangerous locally.

It means:

    shadow was regenerated cheaply
    the following segment did not immediately overpay debt
    the trajectory reached another regeneration

---

## Chain collapse

A chain collapses when a sequence of chain-compatible segments is followed by a segment where:

    average debt > log2(3)

or the trajectory terminates at 1.

The collapse segment is important.

It identifies the point where local escape economics fails.

---

## Post-chain compensation

Post-chain compensation measures the debt paid after a compatible chain.

If a chain has low average debt, a later segment may overpay debt.

v0.4 measures:

    chain length
    chain debt
    chain average debt
    collapse debt
    collapse average debt
    post-collapse average debt
    compensation surplus

The compensation surplus is:

    observed average debt - log2(3)

Positive surplus means the chain has been pushed above the escape threshold.

---

## Native target

The v0.4 target is:

    finite cheap regeneration chains exist,
    but they are followed by debt compensation.

Long-term target:

    every positive cheap regeneration chain is finite
    and every finite chain is eventually compensated.
