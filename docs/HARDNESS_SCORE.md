# Hardness Score

v0.9 introduces a first simple hardness score.

The score is not a theorem.

It is an operational ranking.

A recovery case becomes harder when:

    post-chain recovery distance is larger
    recovery surplus is smaller
    chain deficit is larger
    recovery gap is larger
    chain length is larger

The score is:

    hardness_score =
        log2(1 + post_chain_recovery_distance)
      + log2(1 + recovery_gap)
      + chain_deficit_below_threshold
      + chain_length_segments
      + 1 / (1 + 1000 * recovery_surplus)

The last term increases when recovery surplus is very small.

This score is intentionally simple.

It is meant to sort cases, not to prove anything.
