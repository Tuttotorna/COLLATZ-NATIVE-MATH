# Bounded Obstruction Search Scanner

Version: v2.6

This document describes the bounded obstruction search scanner.

The scanner searches for native obstruction signatures, not merely long trajectories or hard cases.

Native obstruction signature:

    persistent debt
    non-erased shadow
    dangerous regeneration
    insufficient compensation
    no closure event
    internal admissibility

The scanner emits bounded evidence only.

It does not prove the Collatz conjecture.

It does not prove global closure.

It does not prove that obstruction-preserving regeneration is impossible.

Output artifacts:

    results/bounded_obstruction_search_rows.jsonl
    results/bounded_obstruction_search_summary.json
    results/bounded_obstruction_search_certificate.json

Correct interpretation:

    No obstruction was detected in this finite bounded domain.

Incorrect interpretation:

    No obstruction can exist.

v2.6 is a scanner layer, not a proof layer.
