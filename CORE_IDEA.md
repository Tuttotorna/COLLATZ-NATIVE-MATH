# Core Idea

The Collatz rule is simple.

The unresolved state is not the local rule.

The unresolved state is whether the global behavior of the rule is forced.

This repository explores a problem-born language:

    Collatz is not first treated as a sequence of numbers.
    Collatz is treated as a sequence of compression debts.

The local odd-to-odd transition is:

    3 n_i + 1 = 2^(a_i) n_(i+1)

The compression debt is:

    a_i = v2(3 n_i + 1)

If a_i = 1, the odd-to-odd block grows locally.

If a_i >= 2, the block compresses locally.

The escape threshold is controlled by:

    average(a_i) <= log2(3)

A trajectory can sustain escape only if its average compression debt remains too low.

The language then asks:

    how can a trajectory keep generating low debt?

The answer seems to require repeated regeneration of the 2-adic shadow of -1.

So the target becomes:

    Collatz escape would require an infinite cheap regeneration chain.

The conjectural native reduction is:

    Collatz true
    <=>
    no infinite cheap regeneration chain in positive odd Collatz dynamics
