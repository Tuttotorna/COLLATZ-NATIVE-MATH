# Evidence to Native Objects

Version: v1.9

This document defines the mapping between computational artifacts and native objects.

## Frontier stability certificate

Source:

results/frontier_stability_certificate.json

Native role:

frontier anchor

Native interpretation:

- debt: hard frontier recovery structure
- shadow: post-chain recovery distance
- compensation: recovery after chain
- regeneration: not primary in this artifact
- closure: local frontier stability evidence
- obstruction: not detected in selected frontier

## Compensation law candidate certificate

Source:

results/compensation_law_candidate_certificate.json

Native role:

compensation recovery evidence

Native interpretation:

- debt: bad windows
- shadow: recovery after bad windows
- compensation: recovered bad windows
- regeneration: not exhaustively tested
- closure: local recovery only
- obstruction: unrecovered bad window if present

## Adversarial compensation certificate

Source:

results/adversarial_compensation_certificate.json

Native role:

adversarial obstruction search

Native interpretation:

- debt: adversarial bad windows
- shadow: extended recovery windows
- compensation: recovered adversarial bad windows
- regeneration: stress-tested through adversarial candidate generation
- closure: evidence against selected obstruction candidates
- obstruction: counterexample candidate if present

## Hardness metric report

Source:

results/hardness_metric_report.json

Native role:

hardness is stress, not obstruction

Native interpretation:

- debt: metric-dependent stress
- shadow: metric-dependent persistence
- compensation: metric-dependent recovery
- regeneration: metric-dependent
- closure: not decided by hardness alone
- obstruction: not equivalent to hardness

## Summary

The artifacts do not all measure the same thing.

That is correct.

Native structure is multidimensional.

Hardness, recovery, surplus, frontier stability, and adversarial compensation are different evidence views.
