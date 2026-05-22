# Regeneration Epochs

This document defines the first operational unit of COLLATZ-NATIVE-MATH v0.2.

The v0.1 language introduced:

    a_i = v2(3 n_i + 1)
    s_i = v2(n_i + 1)

where n_i is a positive odd term in the accelerated odd Collatz dynamics:

    3 n_i + 1 = 2^(a_i) n_(i+1)

The v0.2 question is:

    when does the trajectory regenerate the 2-adic shadow of -1,
    how much does it regenerate,
    and what does it cost?

---

## Escape consumption

If:

    s_i >= 2

then:

    a_i = 1

and:

    s_(i+1) = s_i - 1

Therefore:

    local escape consumes shadow.

A run of a_i = 1 steps is not free growth.

It spends a finite 2-adic reserve.

---

## Regeneration

A regeneration event occurs when the next odd term has greater shadow:

    s_(i+1) > s_i

The regenerated shadow is:

    regenerated_shadow = s_(i+1) - s_i

The compression cost of the block is:

    compression_cost = max(1, a_i - 1)

The cheapness ratio is:

    cheapness_ratio = regenerated_shadow / compression_cost

This is not a proof quantity yet.

It is an exploratory measurement for detecting candidate cheap regeneration events.

---

## Epoch

A regeneration epoch is the segment beginning at a regeneration event and continuing through the escape steps that consume the regenerated shadow.

Operationally, for a block i where:

    s_(i+1) > s_i

the generated escape reserve is approximately:

    future_escape_capacity = max(0, s_(i+1) - 1)

because shadow s >= 2 supports a = 1 escape steps until the shadow falls to 1.

The epoch is dangerous when it creates a large future_escape_capacity at low compression_cost.

---

## CRC target

CRC means Cheap Regeneration Chain.

The current native target is:

    No positive odd Collatz trajectory can sustain an infinite cheap regeneration chain.

v0.2 does not prove this.

v0.2 creates the first measurable objects:

    regeneration events
    regenerated shadow
    compression cost
    cheapness ratio
    future escape capacity
    average debt
