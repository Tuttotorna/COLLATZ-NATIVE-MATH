# Local Debt Formalization

Version: v3.0

This document drafts formal local debt statements.

## Draft L1: odd block decomposition

Native object:

odd block

Draft statement:

For every odd positive integer n, there exists a unique positive integer a and a unique odd positive integer m such that:

3n + 1 = 2^a m

Native meaning retained:

one expansion followed by one discharge event.

Status:

stable draft.

## Draft L2: discharge exponent uniqueness

Native object:

discharge

Draft statement:

For every odd positive integer n, the discharge exponent a(n) = v2(3n + 1) is uniquely determined.

Native meaning retained:

local reduction strength after expansion.

Status:

stable draft.

## Draft L3: local debt formation

Native object:

local debt

Draft statement:

Let a(n) = v2(3n + 1). A block has local debt when:

log2(3) - a(n) > 0

Native meaning retained:

under-discharge creates structural burden.

Status:

stable draft.

## Draft L4: cumulative debt

Native object:

debt chain

Draft statement:

For a finite interval I of odd blocks, define:

D(I) = sum over i in I of (log2(3) - a_i)

If D(I) > 0, the interval carries cumulative debt.

Native meaning retained:

accumulated structural burden across contiguous native structure.

Status:

stable draft.

## Boundary

These local debt drafts are definitions and formal candidates.

They do not prove global closure.
