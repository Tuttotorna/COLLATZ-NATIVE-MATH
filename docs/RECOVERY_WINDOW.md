# Recovery Window

The recovery window measures how long a cheap regeneration chain remains below the escape threshold.

For a detected chain start block b:

    b = chain_start_block

scan forward through the odd-block trajectory.

For each future window:

    b ... j

compute:

    average_debt(b, j)

The first j such that:

    average_debt(b, j) > log2(3)

defines the recovery point.

The distance:

    j - b + 1

is the recovery distance in odd blocks.

---

## Interpretation

Small recovery distance means:

    compensation arrives quickly.

Large recovery distance means:

    the chain remains economically favorable for longer.

No recovery before reaching 1 would be a strong warning case.

In sampled positive trajectories, v0.7 records whether every detected chain has a recovery point.

---

## Native meaning

The recovery window is the first operational candidate for a compensation law:

    low-debt escape economics cannot remain below threshold indefinitely.
