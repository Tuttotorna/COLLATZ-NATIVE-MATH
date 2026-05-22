# Compensation Law Candidate

Version: v1.3

This document defines a finite, falsifiable candidate law for the Collatz native-math framework.

Core idea:

For an odd Collatz block:

    odd n -> (3n + 1) / 2^a

where:

    a = v2(3n + 1)

The logarithmic growth pressure is controlled by:

    log2(3) - a

If a trajectory has a local window whose average debt is below log2(3), that window is structurally dangerous.

The v1.3 candidate law says:

    Every maximal bad debt window must be followed by a finite recovery window
    such that the combined average debt reaches or exceeds log2(3).

This is not claimed as a proof.

The current scanner tests this law over a selected finite frontier and emits:

    results/compensation_law_candidate_rows.jsonl
    results/compensation_law_candidate_summary.json
    results/compensation_law_candidate_certificate.json

A proof would require replacing finite observation with arithmetic necessity.
