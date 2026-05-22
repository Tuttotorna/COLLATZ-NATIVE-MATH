# Native Evidence Status

Version: v1.9

This document defines status labels used by the native evidence map.

## Closure status labels

EVIDENCE_FOR_LOCAL_CLOSURE_NOT_FULL_NATIVE_CLOSURE

Meaning:

A structure recovered locally or remained stable in a selected finite scan, but full native closure was not established.

LOCALLY_RECOVERED_NOT_FULLY_CLOSED

Meaning:

Bad windows recovered locally, but shadow erasure and regeneration closure are not globally proven.

REGENERATED_BUT_COMPENSATED

Meaning:

Adversarial or regenerated stress appeared, but selected finite cases still compensated.

UNDECIDED_BY_HARDNESS_ALONE

Meaning:

Hardness identifies stress. Hardness alone cannot decide closure.

## Obstruction status labels

NO_OBSTRUCTION_DETECTED_IN_SELECTED_FRONTIER

Meaning:

No obstruction appeared inside the selected frontier scan.

NO_UNRECOVERED_BAD_WINDOW

Meaning:

Every detected bad window recovered in the selected scan.

NO_COUNTEREXAMPLE_CANDIDATE_DETECTED

Meaning:

The adversarial scan found no counterexample candidate inside its selected candidate set.

HARDNESS_DOES_NOT_IMPLY_OBSTRUCTION

Meaning:

A hard case is not automatically an obstruction.

## Proof status

All current v1.9 evidence remains:

finite_evidence_not_proof

or:

classification_not_proof

The project has not claimed proof.
