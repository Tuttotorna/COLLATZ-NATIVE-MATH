# Research Notes

Current native reduction:

    Collatz true
    <=>
    no infinite cheap regeneration chain in positive odd Collatz dynamics

Core objects:

    a_i = v2(3 n_i + 1)
    s_i = v2(n_i + 1)
    A_k = cumulative debt
    W = debt word

Observed structure:

    a_i = 1 is local escape
    a_i >= 2 is local compression
    s_i >= 2 implies a_i = 1
    a_i = 1 implies s_(i+1) = s_i - 1

Therefore:

    escape consumes shadow

A positive escaping trajectory would need:

    repeated regeneration of shadow
    average compression debt <= log2(3)

The next research target is to define a rigorous obstruction to infinite cheap regeneration.
