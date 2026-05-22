# Post-Chain Recovery

v0.7 found that every detected chain episode recovered above log2(3) with recovery distance 1.

That result is useful, but it is also too local.

The v0.7 recovery window starts at:

    chain_start_block

This can make recovery look immediate because the first regeneration block itself often has enough debt to push the average above the threshold.

v0.8 corrects the question.

The new question is:

    after the chain has ended,
    how many future blocks are needed before the post-chain window crosses above log2(3)?

---

## Two recovery windows

v0.8 separates two measurements.

### Chain-start recovery

Starts at:

    chain_start_block

This was the v0.7 definition.

### Post-chain recovery

Starts at:

    chain_end_block + 1

This asks what happens after the locally compatible chain has already completed.

---

## Why this matters

A chain can look compensated if we include its starting regeneration block.

But the harder test is:

    after the chain ends,
    does later motion compensate the low-debt behavior?

This avoids a false impression of immediate compensation.

---

## Native target

The v0.8 target is:

    every finite cheap regeneration chain should have finite post-chain recovery

unless it terminates directly.

If post-chain recovery is absent in a tested trajectory, that case becomes structurally important.
