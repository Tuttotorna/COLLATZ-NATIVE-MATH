# Native Sentence Extractor

Version: v3.3

This document defines the Native Sentence Extractor.

The extractor does not try to solve Collatz.

It reads existing trajectory evidence as native grammar sentences.

The purpose is to move from grammar map to grammar utterance.

## Mother rule

No solution before native language.

## What is a native sentence?

A native sentence is a sequence of grammar objects produced by a trajectory.

Examples:

- trajectory observed
- debt generated
- compensation found
- regeneration found
- dangerous regeneration found
- obstruction not preserved

These are not proof statements.

They are descriptions of what the Collatz dynamics produced inside a bounded observation layer.

## Why this matters

The classical question asks whether every trajectory reaches 1.

The native question asks what kind of structure the trajectory generates before it is translated into terminal language.

The extractor follows the native question.

## Output artifacts

The extractor writes:

- results/native_sentences.jsonl
- results/native_sentence_summary.json
- results/native_sentence_report.md
- results/native_sentence_certificate.json

## Boundary

A native sentence is not a theorem.

A native sentence is not a proof.

A native sentence is a grammar-level reading of trajectory behavior.
