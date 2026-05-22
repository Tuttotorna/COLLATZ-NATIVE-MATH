# Epoch Analysis Notes

v0.2 adds the first operational analysis of regeneration epochs.

The script:

    examples/analyze_regeneration_epochs.py

computes:

    odd block transitions
    debt words
    shadow words
    regeneration events
    cheapness ratios
    future escape capacities
    average debt relative to log2(3)

The goal is not to prove Collatz.

The goal is to identify whether the native language creates a sharper target than the original formulation.

Current target:

    Collatz true
    <=>
    no infinite cheap regeneration chain in positive odd Collatz dynamics

The script searches for local cheap regenerations and then checks whether such events remain globally sustainable.

Observed in v0.1:

    cheap regeneration exists locally.

Therefore, the false target is:

    no cheap regeneration exists.

The correct target is:

    no infinite cheap regeneration chain exists in N+.
