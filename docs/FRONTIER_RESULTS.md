# Critical Frontier Results

v1.1 writes two result files.

## results/critical_frontier_scan.jsonl

One JSON object per scanned candidate.

Main fields:

    n0
    odd_start
    reaches_1
    odd_blocks
    trajectory_average_debt
    chain_episodes
    post_chain_recovered
    post_chain_unrecovered
    max_post_chain_recovery_distance
    min_post_chain_recovery_surplus
    max_hardness_score
    hardest_episode

## results/critical_frontier_summary.json

Compact summary of the scan.

Main fields:

    candidate_count
    completed_count
    previous_critical_n0
    previous_critical_distance
    previous_critical_surplus
    previous_critical_hardness
    current_hardest
    current_longest_recovery
    current_tightest_surplus
    harder_than_previous_critical

The important Boolean is:

    harder_than_previous_critical

If true, the next step should dissect the new hardest case.

If false, the v1.0 case remains the current frontier.
