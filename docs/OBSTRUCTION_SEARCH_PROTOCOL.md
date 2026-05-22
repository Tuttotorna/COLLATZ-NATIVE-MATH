# Obstruction Search Protocol

Version: v2.5

This document defines how the project should search for obstruction-preserving regeneration.

This is a protocol.
It is not a proof.
It is not a theorem.
It is not a claim that no obstruction exists.

## Core target

The search target is not a long trajectory.

The search target is:

obstruction-preserving regeneration

Meaning:

renewed debt that keeps obstruction potential alive through persistent debt, non-erased shadow, insufficient compensation, no closure event, and internal admissibility.

## Search question

How would we detect obstruction-preserving regeneration if it existed?

This is the correct v2.5 question.

## Required obstruction signature

A candidate must show all of the following:

1. persistent debt
2. non-erased shadow
3. dangerous regeneration
4. insufficient compensation
5. no closure event
6. internal admissibility

If one component is missing, the case is not a native obstruction candidate.

## What does not qualify

The following do not qualify by themselves:

- long trajectory
- high odd-block count
- high hardness score
- tight positive surplus
- many bad windows
- local recovery
- repeated regeneration
- reaching 1 late

These are stress indicators, not obstruction.

## Search stages

The protocol has seven stages:

1. generate candidate trajectories
2. detect debt windows
3. track shadow across later structure
4. detect regeneration after compensation
5. classify regeneration as benign, dangerous, or obstruction-preserving
6. test closure result type
7. record bounded result

## Result boundary

A negative finite search result means:

no obstruction candidate was detected inside the selected finite search domain

It does not mean:

global closure is proved

## Current role

v2.5 prepares the first explicit obstruction-oriented search layer.

The next step should implement a bounded obstruction-search scanner.
