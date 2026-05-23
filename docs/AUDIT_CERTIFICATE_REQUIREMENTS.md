# Audit Certificate Requirements

Version: v4.3

Core certificates should preserve boundary fields when applicable.

## Required status

proof_status: not_a_proof

## Accepted theorem status

theorem_status: no_theorems_introduced

## Accepted Collatz status

collatz_status: not_claimed_solved

## Accepted global closure status

global_closure_status: not_claimed

## Accepted global invariant status

global_invariant_status: not_claimed

## Reason

A bounded artifact must not silently become a proof claim.

A certificate must preserve the native-language boundary.
