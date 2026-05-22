# Bounded Search Result Types

Version: v2.6

NO_DEBT_DETECTED:
No bad window was detected.

DEBT_LOCALLY_RECOVERED:
Debt windows were detected, but they were locally compensated.
This does not imply full native closure.

REGENERATED_BUT_COMPENSATED:
Debt regenerated after compensation, but obstruction was not detected.

DANGEROUS_REGENERATION_DETECTED:
Stressful regeneration was detected.
This requires attention, but it is not obstruction by itself.

OBSTRUCTION_CANDIDATE_DETECTED:
The bounded scanner found a structure matching obstruction-candidate conditions inside the protocol.
This is not a classical counterexample by itself.

CLOSED:
The scanner may use this when obstruction potential is treated as erased under a bounded closure test.

UNDECIDED:
The bounded scanner cannot classify the case strongly enough.
UNDECIDED is allowed.
