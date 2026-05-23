# Audit Checks

Version: v4.3

The v4.3 audit performs five check groups.

## 1. Index audit

Checks whether indexed files exist.

## 2. Entry audit

Checks README.md, START_HERE.md, and CRC_CONJECTURE.md for native-first framing.

## 3. Certificate audit

Checks core certificates for non-proof boundary.

## 4. Builder audit

Checks whether latest builder scripts exist.

## 5. README route audit

Checks whether README route includes the current route versions.

## False positive protection

The audit checks forbidden claims line by line.

It rejects assertive claims.

It allows negated boundary language.

Allowed examples:

    It is not a claim that Collatz is solved.
    Do not claim Proof of Collatz.
    audit_passed != proof
    obstruction_impossibility_status: not_claimed

Rejected examples:

    Collatz is solved.
    Proof of Collatz.

## Passing meaning

A pass means repository artifacts are internally consistent under the v4.3 audit.

A pass does not mean Collatz is solved.

## Patch 9 conservative standalone-only detector

Forbidden-claim detection now fails only on pure standalone assertive lines.

This prevents repeated false positives from safety language, examples, lists, and boundary statements.
