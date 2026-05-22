# Recovery Comparison

v0.8 compares:

    chain_start_recovery
    post_chain_recovery

The difference is important.

If chain_start_recovery exists but post_chain_recovery does not, then the earlier result was too weak.

If both exist, the compensation signal is stronger.

If post_chain_recovery takes many blocks, that may reveal a longer economic escape pocket.

The key metrics are:

    chain_start_recovery_distance
    post_chain_recovery_distance
    recovery_gap
    post_chain_recovery_average_debt
    post_chain_recovery_surplus
    post_chain_unrecovered

The recovery gap is:

    post_chain_recovery_distance - chain_start_recovery_distance

when both are defined.
