# Cheapness Ratio

The cheapness ratio measures how much 2-adic shadow is regenerated per unit of compression cost.

For a block:

    3 n_i + 1 = 2^(a_i) n_(i+1)

define:

    s_i = v2(n_i + 1)
    s_(i+1) = v2(n_(i+1) + 1)

If:

    s_(i+1) > s_i

then shadow has been regenerated.

The regenerated shadow is:

    R_i = s_(i+1) - s_i

The compression cost is:

    C_i = max(1, a_i - 1)

The cheapness ratio is:

    Q_i = R_i / C_i

---

## Interpretation

High Q_i means:

    much future escape potential was regenerated at low immediate compression cost.

Low Q_i means:

    regeneration was expensive.

The dangerous pattern for Collatz would be an infinite chain in which high cheapness remains sustainable while average compression debt stays below or equal to:

    log2(3)

---

## Threshold note

The rough escape threshold is:

    average(a_i) <= log2(3)

Since:

    log2(3) - 1 ~= 0.58496

a long-term trajectory can only escape if its extra compression cost remains too low relative to generated escape capacity.

This repository treats Q_i as an exploratory signal, not as a proof.
