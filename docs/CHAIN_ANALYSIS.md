# Chain Analysis

v0.3 moves from local regeneration events to regeneration chains.

v0.2 showed an important fact:

    local cheap regeneration exists.

Therefore the false target is:

    no cheap regeneration exists

The correct target is:

    no infinite cheap regeneration chain exists in positive odd Collatz dynamics.

---

## Native chain question

After a cheap regeneration event, the trajectory receives new 2-adic shadow of -1.

That shadow may produce a run of local escape blocks:

    a = 1

The central v0.3 question is:

    after a cheap regeneration,
    can the trajectory regenerate cheaply again
    before the average debt rises above log2(3)?

If yes, the chain continues.

If no, the chain breaks.

---

## Chain segment

A chain segment starts at a regeneration event:

    s_(i+1) > s_i

and continues until the next regeneration event or until the trajectory reaches 1.

For each segment, v0.3 measures:

    start block
    end block
    start n
    regenerated shadow
    compression cost
    cheapness ratio
    blocks until next regeneration
    cumulative debt inside the segment
    average debt inside the segment
    maximum n inside the segment
    whether the segment remains below the escape threshold

---

## Escape threshold

The rough multiplicative escape threshold is:

    average(a_i) <= log2(3)

where:

    a_i = v2(3 n_i + 1)

If a chain stays below or equal to this threshold indefinitely, it remains a candidate escape chain.

If every candidate chain is eventually forced above the threshold, escape fails.

---

## v0.3 target

The v0.3 target is not a proof.

It is an operational detector:

    detect cheap regeneration chains
    measure whether they remain economically favorable
    identify where they break

The long-term conjectural target remains:

    no infinite cheap regeneration chain in N+
