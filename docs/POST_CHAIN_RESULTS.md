# Post-Chain Recovery Results

v0.8 generates:

    results/post_chain_recovery_analysis.jsonl
    results/post_chain_recovery_summary.json

Each row records one chain episode and compares:

    recovery from chain start
    recovery after chain end

This is stricter than v0.7.

The key output is:

    post_chain_unrecovered_episodes

A nonzero value is not a proof against Collatz.

It means the current compensation-window definition needs deeper analysis.
