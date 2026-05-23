# Shadow Chain Classification

Version: v2.9

This document defines the v2.9 shadow classifications.

## NO_SHADOW_SIGNAL

No meaningful debt or regeneration signal is present.

## DEBT_WITHOUT_REGENERATION_SHADOW

Debt appears, but regeneration does not preserve a shadow signal.

## REGENERATION_WITHOUT_DANGEROUS_SHADOW_SIGNAL

Regeneration appears, but it does not cross the dangerous-regeneration boundary.

## DANGEROUS_REGENERATION_WITH_WEAK_SHADOW_SIGNAL

Dangerous regeneration appears, but the evidence is not strong enough to classify it as persistent shadow.

## PERSISTENT_SHADOW_SIGNAL

Dangerous regeneration appears together with tight surplus, long recovery distance, or high recovery stress.

This is the important v2.9 class.

It is not obstruction by itself.

It means the prior debt line deserves further analysis.

## OBSTRUCTION_CANDIDATE_SHADOW

A bounded obstruction-candidate shadow would require obstruction candidate conditions already present in the source layer.

If this appears, it is not automatically a classical counterexample.

It is a native obstruction candidate requiring direct analysis.
