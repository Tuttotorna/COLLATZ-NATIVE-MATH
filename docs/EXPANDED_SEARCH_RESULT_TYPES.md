# Expanded Search Result Types

Version: v2.8

The v2.8 scanner uses the same bounded result discipline as v2.6.

## NO_DEBT_DETECTED

No bad window was detected.

## DEBT_LOCALLY_RECOVERED

Debt exists but was locally recovered.

This does not imply native closure.

## REGENERATED_BUT_COMPENSATED

Debt regenerated after compensation, but no obstruction candidate appeared.

## DANGEROUS_REGENERATION_DETECTED

Stressful regeneration appeared.

This is important evidence, but it is not obstruction by itself.

## OBSTRUCTION_CANDIDATE_DETECTED

The scanner detected a bounded candidate matching obstruction conditions.

This requires further analysis.

It is not automatically a classical counterexample.

## UNDECIDED

The scanner cannot classify the case strongly enough.

UNDECIDED is allowed because overclaiming is worse than uncertainty.
