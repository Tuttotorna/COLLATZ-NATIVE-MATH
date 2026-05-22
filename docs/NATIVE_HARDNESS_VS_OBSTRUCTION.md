# Native Hardness vs Obstruction

Version: v1.7

This document separates hardness from obstruction.

## Hardness

Hardness measures stress.

Examples:

- long recovery distance
- tight positive surplus
- many bad windows
- high odd-block count
- high compensation hardness score
- high adversarial compensation hardness score

Hardness is useful because it identifies where the structure is under stress.

## Obstruction

Obstruction is not stress.

Obstruction requires persistent unclosed debt.

A hard case may still be fully compensated.
A tight case may still close.
A long case may still have a forced discharge mechanism.

## Current metric separation

Existing repository evidence already shows that different hardness metrics identify different hard cases:

- frontier recovery hardness points to n0 = 9780657630
- compensation window hardness points to n0 = 670617279
- adversarial compensation hardness points to n0 = 63728127
- known long trajectory anchor points to n0 = 837799

This is not a contradiction.

It means hardness is multidimensional.

## Native lesson

No single hardness metric should be mistaken for obstruction.

The native obstruction model must ask a stronger question:

    Does stress become self-preserving?

If no, it is hardness.
If yes, it becomes obstruction candidate behavior.
