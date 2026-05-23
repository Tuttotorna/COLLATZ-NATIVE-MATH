# Expanded Bounded Obstruction Search

Version: v2.8

This document describes the expanded bounded obstruction search.

v2.8 does not perform blind brute force.

It expands around near-obstruction evidence from v2.6 and v2.7.

The target remains obstruction-preserving regeneration.

The target is not merely a long trajectory.
The target is not merely a hard case.
The target is not merely tight surplus.
The target is not merely many bad windows.

## Purpose

v2.8 asks a sharper question:

Where prior evidence shows stress, does the stress become self-preserving obstruction?

## Expansion strategy

The scanner expands around:

- known trajectory anchors;
- cases with many dangerous regenerations;
- cases with many debt windows;
- cases with high recovery stress;
- cases with tight positive surplus;
- neighborhoods around powers of two.

This is a targeted finite expansion.

## Correct interpretation

If no obstruction candidate is found, the result means:

No obstruction candidate was detected inside this expanded bounded domain.

It does not mean:

No obstruction can exist.

## Status

v2.8 is an evidence layer.

It is not a proof layer.
