# Shadow Persistence Instrumentation Report

Version: v2.9

This report instruments the v2.8 expanded bounded obstruction search output.

It does not prove the Collatz conjecture.

It does not prove global closure.

It does not prove that obstruction-preserving shadow cannot exist.

## Summary

- tested_candidate_count: 320
- source_debt_window_count: 157129
- source_regeneration_count: 156143
- source_dangerous_regeneration_count: 24588
- source_obstruction_candidate_count: 0
- persistent_shadow_signal_count: 80
- obstruction_candidate_shadow_count: 0
- obstruction_detected: False
- native_interpretation: PERSISTENT_SHADOW_SIGNALS_FOUND_WITHOUT_OBSTRUCTION_CANDIDATE
- proof_status: not_a_proof

## Classification counts

- DEBT_WITHOUT_REGENERATION_SHADOW: 26
- NO_SHADOW_SIGNAL: 20
- PERSISTENT_SHADOW_SIGNAL: 80
- REGENERATION_WITHOUT_DANGEROUS_SHADOW_SIGNAL: 194

## Strongest shadow case

- n0: 9780657630
- shadow_persistence_score: 10
- shadow_classification: PERSISTENT_SHADOW_SIGNAL
- dangerous_regeneration_count: 4863
- min_positive_surplus: 7.15128842860846e-05
- max_post_recovery_blocks: 183
- hardest_recovery_score: 74280320.99431963

## Top shadow persistence cases

| n0 | classification | score | dangerous regeneration | min surplus | max post recovery blocks | hardest recovery score |
|---|---:|---:|---:|---:|---:|---:|
| 9780657630 | PERSISTENT_SHADOW_SIGNAL | 10 | 4863 | 7.15128842860846e-05 | 183 | 74280320.99431963 |
| 9780657631 | PERSISTENT_SHADOW_SIGNAL | 10 | 4835 | 7.15128842860846e-05 | 183 | 74280320.99431963 |
| 670617279 | PERSISTENT_SHADOW_SIGNAL | 10 | 2294 | 0.0001438822575672294 | 231 | 15179077.92751667 |
| 63728127 | PERSISTENT_SHADOW_SIGNAL | 10 | 1710 | 0.0001438822575672294 | 236 | 15179077.92751667 |
| 2298025 | PERSISTENT_SHADOW_SIGNAL | 10 | 1204 | 0.0006230848644295239 | 110 | 4943146.874254355 |
| 626331 | PERSISTENT_SHADOW_SIGNAL | 10 | 1087 | 0.00040335293738058553 | 110 | 4943146.874254355 |
| 68719476735 | PERSISTENT_SHADOW_SIGNAL | 10 | 875 | 0.0007517849931295562 | 86 | 1629455.2447775372 |
| 3542887 | PERSISTENT_SHADOW_SIGNAL | 10 | 695 | 0.00040335293738058553 | 112 | 4167566.030178391 |
| 1117065 | PERSISTENT_SHADOW_SIGNAL | 10 | 633 | 0.00040335293738058553 | 65 | 1041271.7029595028 |
| 68719476728 | PERSISTENT_SHADOW_SIGNAL | 10 | 610 | 0.00040335293738058553 | 76 | 1041271.7029595028 |
| 68719476730 | PERSISTENT_SHADOW_SIGNAL | 10 | 606 | 0.00040335293738058553 | 75 | 1041271.7029595028 |
| 837799 | PERSISTENT_SHADOW_SIGNAL | 10 | 599 | 0.00040335293738058553 | 65 | 1041271.7029595028 |
| 68719476732 | PERSISTENT_SHADOW_SIGNAL | 10 | 568 | 0.00040335293738058553 | 76 | 1041271.7029595028 |
| 68719476733 | PERSISTENT_SHADOW_SIGNAL | 10 | 564 | 0.00040335293738058553 | 74 | 1041271.7029595028 |
| 16777214 | PERSISTENT_SHADOW_SIGNAL | 10 | 236 | 0.00040335293738058553 | 85 | 1629455.2447775372 |
| 131071 | PERSISTENT_SHADOW_SIGNAL | 10 | 213 | 0.00040335293738058553 | 62 | 1041271.7029595028 |
| 1048568 | PERSISTENT_SHADOW_SIGNAL | 10 | 213 | 0.00040335293738058553 | 62 | 1041271.7029595028 |
| 1048570 | PERSISTENT_SHADOW_SIGNAL | 10 | 202 | 0.00040335293738058553 | 61 | 1041271.7029595028 |
| 1048572 | PERSISTENT_SHADOW_SIGNAL | 10 | 170 | 0.00040335293738058553 | 55 | 1041271.7029595028 |
| 1048573 | PERSISTENT_SHADOW_SIGNAL | 10 | 166 | 0.00040335293738058553 | 53 | 1041271.7029595028 |

## Boundary

No obstruction-preserving shadow detected in a finite instrumentation layer is not proof that such shadow cannot exist.

Correct interpretation:

The current finite instrumentation found shadow persistence signals, but the certificate must keep proof status separate from evidence status.

Incorrect interpretation:

Do not claim final proof, global closure, or impossibility of obstruction-preserving shadow from this bounded instrumentation layer.

