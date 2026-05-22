# Compensation Law Search

v0.7 moves from classifying collapse to measuring compensation.

Earlier versions showed:

    cheap regeneration exists
    chain-compatible segments exist
    finite cheap chains exist
    detected chains collapse
    collapse residue can be classified

v0.6 reduced unclassified collapse residue to zero in the sampled set.

v0.7 asks a sharper quantitative question:

    after a low-debt cheap regeneration chain,
    how many future blocks are needed before the average debt crosses back above log2(3)?

---

## Core quantities

For a chain episode:

    chain_average_debt <= log2(3)

The deficit below threshold is:

    chain_deficit = log2(3) - chain_average_debt

The recovery window is the smallest future window starting at the chain start such that:

    window_average_debt > log2(3)

The recovery distance is:

    recovery_distance_blocks

The recovery debt is:

    recovery_debt

The recovery surplus is:

    recovery_average_debt - log2(3)

---

## Why this matters

A chain-compatible segment is locally dangerous.

But if every such segment is followed by compensation within a bounded or structurally constrained future window, then the CRC obstruction becomes quantitative.

The target becomes:

    no low-debt chain can avoid compensation indefinitely.

This is not a proof.

It is a search for a compensation law.
