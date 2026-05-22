# Frontier Comparison Rule

Version: v1.2

The comparison rule is deterministic.

Previous critical baseline:

    previous_critical_n0 = 9780657630
    previous_critical_hardness = 15.100955299032181
    previous_critical_distance = 114
    previous_critical_min_surplus = 0.00275679752445801
    comparison_tolerance = 1e-9

Statuses:

    SAME_AS_PREVIOUS
    HARDER_THAN_PREVIOUS
    SOFTER_THAN_PREVIOUS
    NUMERIC_TIE_DIFFERENT_CASE

A frontier is stable when:

    current_hardest_n0 == previous_critical_n0
    abs(current_hardest_hardness - previous_critical_hardness) <= tolerance

The baseline must not be rounded below the comparison tolerance.
