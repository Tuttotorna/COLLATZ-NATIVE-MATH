# Audit Entry File Requirements

Version: v4.3

Entry files must preserve the corrected public position.

## Entry files

README.md

START_HERE.md

CRC_CONJECTURE.md

## Required phrases

No solution before native language.

not_a_proof

not_claimed_solved

## Forbidden assertive claims

Collatz is solved.

We solved Collatz.

Proof of Collatz.

Collatz proof complete.

global closure is proved.

global invariant is proved.

obstruction is impossible.

## Boundary language allowed

Forbidden phrases are allowed only when they appear inside explicit negation or boundary language.

Preferred status-safe wording:

    obstruction_impossibility_status: not_claimed

## Reason

The reader must not enter through solution-first framing.

## Patch 9 entry sanitization rule

Entry files use status-safe wording for sensitive claims:

    proof_status: not_a_proof
    collatz_status: not_claimed_solved
    global_closure_status: not_claimed
    global_invariant_status: not_claimed
    obstruction_impossibility_status: not_claimed

This removes ambiguity for the audit and for readers.
