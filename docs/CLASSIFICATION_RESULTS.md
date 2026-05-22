# Classification Results

v0.5 generates:

    results/collapse_cause_classification.jsonl
    results/collapse_cause_summary.json

Each row describes one collapse episode with classified mechanisms.

Fields include:

    n0
    chain length
    chain average debt
    collapse cause
    collapse max debt
    ending shadow
    post-chain average debt
    compensation surplus
    cause flags
    primary cause

The key diagnostic is:

    which mechanisms recur across finite chain collapses?

The target remains:

    no infinite cheap regeneration chain in positive odd Collatz dynamics.
