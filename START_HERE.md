# START HERE

This repository starts from one principle:

    the problem should generate the mathematics needed to make it speak.

For Collatz, the problem-born language begins with the accelerated odd dynamics:

    3 n_i + 1 = 2^(a_i) n_(i+1)

where:

    a_i = v2(3 n_i + 1)

This turns Collatz into a sequence of compression debts:

    W = (a_0, a_1, a_2, ...)

The second native quantity is the 2-adic shadow of -1:

    s_i = v2(n_i + 1)

Escape steps consume this shadow.

Regeneration restores it.

The key open target here is:

    no infinite cheap regeneration chain in positive odd Collatz dynamics

Read in this order:

    CORE_IDEA.md
    MATH_COLLATZ.md
    CRC_CONJECTURE.md
    docs/DEBT_WORDS.md
    docs/TWO_ADIC_SHADOW.md
    docs/CHEAP_REGENERATION.md

## v0.2 step

After reading the core files, run:

    python examples/analyze_regeneration_epochs.py

This computes regeneration events and cheapness ratios.

The v0.2 target is:

    distinguish local cheap regeneration from infinite cheap regeneration chains.

## v0.3 step

After v0.2, run:

    python examples/analyze_cheap_regeneration_chains.py

This moves from single regeneration events to finite cheap regeneration chain diagnostics.

The v0.3 question is:

    does local cheap regeneration connect into a sustained low-debt chain,
    or is it broken by accumulated compression debt?
