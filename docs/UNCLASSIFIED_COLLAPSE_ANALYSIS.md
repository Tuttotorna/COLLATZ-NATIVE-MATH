# Unclassified Collapse Analysis

v0.5 introduced collapse cause classification.

It found classified causes such as:

    debt_spike
    failed_regeneration
    post_chain_overcompensation

but also left some collapse episodes marked:

    unclassified

v0.6 targets those cases.

The goal is to reduce the unknown residue inside the Math_Collatz collapse language.

---

## Why unclassified matters

If a finite cheap regeneration chain collapses but the collapse is unclassified, then the current native language is incomplete.

The system should not hide that.

An unclassified episode means:

    the chain stopped being chain-compatible,
    but the classifier did not yet identify the native mechanism.

v0.6 adds new cause classes to reduce this residue.

---

## New cause classes

### soft_debt_break

A collapse segment rises above the escape threshold, but without a large spike.

Operational signal:

    collapse_average_debt > log2(3)
    collapse_max_a < 4

This means the chain was broken by distributed debt rather than a single spike.

### weak_regeneration

The next regeneration exists, but it is not locally cheap.

Operational signal:

    next regeneration exists
    next_is_locally_cheap = false

This means the chain did regenerate, but not economically enough to remain dangerous.

### delayed_compensation

The immediate post-chain average debt may remain below log2(3), but the full trajectory average is above log2(3).

Operational signal:

    post_chain_average_debt <= log2(3)
    trajectory_average_debt > log2(3)

This means compensation exists, but outside the immediate collapse window.

### end_of_chain_without_escape

The chain ends, reaches later termination, or fails to continue as a cheap chain even if no single spike is visible.

Operational signal:

    no next chain-compatible event follows

This is a structural break in chain continuity.

---

## v0.6 target

v0.6 does not prove Collatz.

It improves the collapse vocabulary.

Target:

    reduce unclassified collapse residue
    sharpen CRC obstruction language
