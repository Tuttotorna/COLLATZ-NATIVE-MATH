# Evidence Layer Status

Version: v1.6

This document classifies the existing repository outputs.

## Evidence layer

The following are evidence artifacts:

- results/frontier_stability_certificate.json
- results/critical_frontier_summary.json
- results/compensation_law_candidate_certificate.json
- results/compensation_law_candidate_summary.json
- results/adversarial_compensation_certificate.json
- results/adversarial_compensation_summary.json
- results/hardness_metric_report.json
- results/hardness_metric_report.md

## Meaning

These files show finite deterministic behavior over selected candidate sets.

They support the native research path.

They do not prove the Collatz conjecture.

## Correct interpretation

The evidence layer says:

- selected bad windows recovered
- selected adversarial candidates did not produce unrecovered obstruction
- different hardness metrics identify different structural stress points
- known hard cases remain important but not unique under all metrics

## Incorrect interpretation

The evidence layer does not say:

- the conjecture is proved
- all possible trajectories are covered
- finite scans imply global closure
- hardness metrics are theorem statements

## Role in the project

The evidence layer is downstream of the native method.

It is useful for testing native claims.

It should not replace the native method.
