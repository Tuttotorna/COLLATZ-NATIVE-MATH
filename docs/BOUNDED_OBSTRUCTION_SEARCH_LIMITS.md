# Bounded Obstruction Search Limits

Version: v2.6

Limit 1: finite domain.
The scanner tests a finite deterministic candidate set.

Limit 2: bounded windows.
The scanner uses bounded bad-window lengths and bounded recovery lookahead.

Limit 3: bounded regeneration logic.
Dangerous regeneration is classified by finite stress indicators.

Limit 4: terminality is not closure.
Reaching 1 is not treated as native closure.

Limit 5: no proof claim.
The scanner is an evidence generator.

Correct conclusion:

    No obstruction candidate was detected in this bounded search.

Forbidden conclusion:

    No obstruction can exist.
