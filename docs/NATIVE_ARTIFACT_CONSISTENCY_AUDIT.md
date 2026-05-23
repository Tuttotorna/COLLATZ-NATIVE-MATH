# Native Artifact Consistency Audit

Version: v4.3

This document defines the native artifact consistency audit.

## Purpose

After v4.2, the repository has a role-based index.

v4.3 checks whether the indexed repository is internally coherent.

## What the audit checks

- indexed files exist
- entry files preserve native-first framing
- core certificates preserve non-proof status
- builders exist
- README route contains latest route versions
- no entry file claims proof or solution

## What the audit does not do

It does not add theory.

It does not prove Collatz.

It does not claim Collatz is solved.

It does not claim global closure.

It does not claim global invariance.

## Core rule

No solution before native language.
