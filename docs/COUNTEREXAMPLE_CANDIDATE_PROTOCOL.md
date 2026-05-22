# Counterexample Candidate Protocol

Version: v1.4

A counterexample candidate is recorded when a bad compensation window is found and no later recovery is observed within the finite traced trajectory.

Definitions:

bad window:
A contiguous odd-block debt window whose average debt is below log2(3).

recovered window:
A bad window whose combined average, after appending later odd-block debts, rises back to at least log2(3).

unrecovered window:
A bad window for which no such recovery is found before the traced trajectory ends.

This protocol does not prove that an unrecovered window is a true Collatz counterexample.
It only marks it as a finite computational counterexample candidate requiring deeper analysis.
