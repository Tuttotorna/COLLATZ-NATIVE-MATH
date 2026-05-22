# Frontier Stability Certificate

Version: v1.2

This document defines the finite frontier stability certificate emitted by:

    python examples/scan_critical_frontier.py

The certificate compares the current hardest frontier case against the previous critical case using the exact stored baseline:

    n0 = 9780657630
    hardness = 15.100955299032181
    post-chain recovery distance = 114
    minimum surplus = 0.00275679752445801

If the same case remains hardest within tolerance, the scanner records:

    comparison_status = SAME_AS_PREVIOUS
    frontier_stable = true
    harder_than_previous_critical = false

This is a finite computational certificate over the selected candidate frontier.
It is not a proof of the Collatz conjecture.
