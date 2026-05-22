# Translation Validity Rules

Version: v2.0

This document defines when a translation is valid.

## Rule 1: Native source preservation

Every translated statement must preserve its native source object.

If the native object disappears, the translation is invalid.

## Rule 2: No premature theorem language

Before a standard proof exists, translation must avoid theorem claims.

Allowed:

- definition candidate
- condition candidate
- structural mapping
- proof target
- obstruction target

Not allowed:

- theorem proved
- conjecture solved
- global closure established
- all trajectories covered

## Rule 3: Evidence remains evidence

Finite computational artifacts remain evidence.

They do not become proof through translation.

## Rule 4: Closure is not terminality

Native closure must not be translated as simply reaching 1.

Native closure means obstruction potential erased.

Classical terminality means the trajectory reaches 1.

These may be related later, but v2.0 keeps them distinct.

## Rule 5: Hardness is not obstruction

Hardness metrics must not be translated as counterexamples.

Hardness means stress.

Obstruction means persistent unclosed debt.

## Rule 6: Compensation is not automatically closure

A recovered bad window is not automatically full native closure.

Translation must preserve the distinction between:

- local recovery
- shadow erasure
- regeneration testing
- obstruction erasure

## Rule 7: Reversibility

A translated standard statement must be reversible back to the native object.

If reversibility fails, the translation is not accepted.
