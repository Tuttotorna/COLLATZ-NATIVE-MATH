# Critical Case Results

v1.0 generates:

    results/critical_case_dissection.json
    results/critical_case_blocks.jsonl
    results/critical_case_window.jsonl
    results/critical_case_summary.json

The outputs serve different purposes.

## critical_case_dissection.json

High-level record of the selected hardest episode.

## critical_case_blocks.jsonl

Full odd-block trajectory for the critical start.

## critical_case_window.jsonl

Focused block-by-block view from the hard chain through the full post-chain recovery window.

## critical_case_summary.json

Compact summary for README-level reporting.

The most important fields are:

    n0
    chain_start_block
    chain_end_block
    post_chain_recovery_start_block
    post_chain_recovery_end_block
    post_chain_recovery_distance_blocks
    post_chain_recovery_surplus
    first_crossing_block
