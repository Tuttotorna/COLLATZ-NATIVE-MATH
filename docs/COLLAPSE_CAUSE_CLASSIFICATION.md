# Collapse Cause Classification

v0.5 classifies why finite cheap regeneration chains collapse.

v0.4 showed that chain-compatible segments exist, but sampled chains remain finite.

v0.5 asks:

    what breaks them?

The goal is not only to detect collapse.

The goal is to classify the mechanism of collapse in the native language of Collatz.

---

## Collapse causes

v0.5 introduces these collapse cause classes:

### debt_spike

A high-debt block appears near or at collapse.

Operational signal:

    max a in collapse window >= 4

This indicates a strong compression event.

### shadow_exhaustion

The chain loses 2-adic shadow and cannot immediately regenerate it.

Operational signal:

    ending shadow <= 1

This means the trajectory has consumed the local fuel for a = 1 escape.

### failed_regeneration

A chain-compatible run ends without a locally cheap regeneration following it.

Operational signal:

    the next regeneration is absent or not locally cheap

### post_chain_overcompensation

The post-chain average debt rises above the escape threshold:

    post_chain_average_debt > log2(3)

This means the low-debt phase has been compensated by later debt.

### terminal_descent

The trajectory reaches 1.

Operational signal:

    reaches_1 = true and no further regeneration remains

---

## Why this matters

The CRC target is:

    no infinite cheap regeneration chain in positive odd Collatz dynamics

To prove this, it may not be enough to know that finite chains collapse.

We need to know how they collapse.

If the same collapse mechanisms recur across large samples, the proof target becomes sharper.

Instead of proving vaguely:

    every cheap chain ends

we can attempt to prove:

    every cheap chain must end through one of a finite set of native collapse mechanisms.
