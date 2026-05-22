# Compensation Results

v0.7 generates:

    results/compensation_law_search.jsonl
    results/compensation_law_summary.json

Each row records:

    n0
    chain start
    chain end
    chain length
    chain deficit
    recovery found
    recovery distance
    recovery average debt
    recovery surplus
    full trajectory average debt

The target is to measure whether every chain-compatible episode is later compensated.

The long-term proof target would be:

    every positive low-debt regeneration chain has finite recovery.
