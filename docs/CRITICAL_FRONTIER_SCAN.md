# Critical Frontier Scan

v1.1 moves from one hard case to a frontier search.

v1.0 isolated the hardest known recovered case:

    n0 = 9780657630
    post-chain recovery distance = 114
    post-chain recovery surplus ~= 0.002757

v1.1 asks a sharper question:

    is this case isolated,
    or is it part of a larger frontier of hard recovery cases?

---

## What v1.1 scans

The scan uses three candidate families:

1. Known hard cases already observed in earlier runs.
2. Local neighborhoods around the hardest known centers.
3. Structured candidates such as near-Mersenne odd values.

The scan is intentionally bounded.

It is not a proof search over all integers.

It is a frontier detector.

---

## Output

The script writes:

    results/critical_frontier_scan.jsonl
    results/critical_frontier_summary.json

Each scanned candidate receives:

    odd_blocks
    trajectory_average_debt
    chain_episodes
    max_post_chain_recovery_distance
    min_post_chain_recovery_surplus
    max_hardness_score
    hardest_episode

---

## Interpretation

A stronger frontier case has one or more of:

    longer post-chain recovery distance
    smaller positive recovery surplus
    larger chain deficit
    larger hardness score

If v1.1 finds a harder case than v1.0, that case becomes the next microscope target.

If it does not, v1.0 remains the current critical case.
