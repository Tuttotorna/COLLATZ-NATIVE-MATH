# v3.2 Next Steps

Version: v3.2

The next logical step after the Native Grammar Map is:

v3.3 Native Sentence Extractor

## Purpose of v3.3

The repository should begin extracting native sentences from trajectories.

Not to prove.

Not to solve.

To listen.

## A native sentence extractor should identify sequences such as:

expansion -> discharge

weak discharge -> debt

debt -> compensation

debt -> shadow -> regeneration

regeneration -> compensation

regeneration -> dangerous regeneration

dangerous regeneration -> no obstruction candidate

debt -> closure candidate

## Output goal

For each trajectory, the extractor should emit a grammar trace.

Example:

n0 = 27

grammar trace:

debt generated
compensation found
regeneration found
dangerous regeneration found
obstruction not preserved

## Why this matters

The current scanners measure.

The next layer should translate measurements into native sentences.

This is closer to Collatz speaking in its own language.

## Boundary

v3.3 must not become a proof attempt.

It must remain a native description layer.
