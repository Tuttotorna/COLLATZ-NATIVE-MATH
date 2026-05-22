# Obstruction-Preserving Regeneration

Version: v2.3

This document defines obstruction-preserving regeneration.

## Definition

Obstruction-preserving regeneration occurs when debt repeatedly regenerates while retaining obstruction potential.

It requires:

1. repeated debt formation;
2. persistence of prior shadow;
3. failure of shadow erasure;
4. insufficient compensation;
5. no closure event;
6. structural admissibility of the continuing chain.

In short:

obstruction-preserving regeneration = regeneration that keeps debt alive as obstruction

## Not enough

The following are not enough:

- repeated bad windows;
- high hardness;
- long recovery distance;
- tight positive surplus;
- large odd-block count;
- local recovery;
- ordinary regeneration.

These are stress indicators, not obstruction.

## Candidate form

A candidate obstruction-preserving regeneration chain has the form:

D1 -> C1? -> D2 -> C2? -> D3 -> C3? -> ...

where each C either fails, is insufficient, or does not erase shadow.

The key condition is not the absence of all compensation.
The key condition is the absence of sufficient obstruction-erasing compensation.

## Failure of closure

Closure fails only if obstruction potential remains self-preserving.

Therefore:

failure of local recovery is not required;
failure of shadow erasure is required.

## Status

No such obstruction-preserving regeneration chain has been established by this repository.

The purpose of this definition is to make the target explicit before native closure lemma candidates.
