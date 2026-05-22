# Collapse Results

v0.4 generates:

    results/chain_collapse_analysis.jsonl
    results/chain_collapse_summary.json

Each row describes one detected chain episode.

A chain episode contains:

    chain start
    chain end
    chain length
    chain average debt
    collapse block
    collapse cause
    collapse average debt
    post-chain average debt
    compensation surplus

The goal is to distinguish:

    local cheapness
    finite compatible chains
    actual sustained escape candidates

A proof path would need to show that sustained escape candidates cannot continue indefinitely.
