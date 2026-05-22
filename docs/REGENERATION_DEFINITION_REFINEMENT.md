# Regeneration Definition Refinement

Version: v2.3

This document refines regeneration.

Regeneration is the reappearance of debt structure after apparent compensation.

## Refined definition

Regeneration occurs when, after a compensated debt interval, a later interval again satisfies the bad-window condition.

Native form:

debt -> compensation -> renewed debt

Standard candidate form:

An interval I is bad.
A later interval J compensates I.
A later interval R becomes bad after the compensation event.

Then R is a regeneration event.

## Benign regeneration

Regeneration is benign when renewed debt is again compensated without preserving obstruction potential.

Benign regeneration has this form:

D1 -> C1 -> D2 -> C2 -> D3 -> C3

where each debt event receives compensation and does not preserve a self-sustaining shadow.

## Dangerous regeneration

Regeneration is dangerous when renewed debt becomes harder to erase or preserves obstruction potential.

Dangerous regeneration has signs such as:

- shrinking surplus;
- persistent shadow;
- increasing recovery distance;
- repeated bad-window formation;
- dependence on prior debt structure;
- failure of shadow erasure.

Dangerous regeneration is not automatically obstruction.
It becomes obstruction-relevant only if it becomes self-preserving.

## Obstruction-preserving regeneration

Regeneration is obstruction-preserving when renewed debt continues without sufficient compensation or shadow erasure.

Native form:

D1 -> D2 -> D3 -> ...

or:

D1 -> weak C1 -> D2 -> weak C2 -> D3

where compensation never destroys obstruction potential.

## Status

The refined regeneration model prepares the next layer:

v2.4 Native Closure Lemma Candidates.
