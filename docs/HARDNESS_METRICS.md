# Hardness Metrics

Version: v1.5

This repository uses more than one hardness lens.

That is intentional.

There is not one single meaning of "hardest Collatz case" unless a metric is specified.

## Core distinction

A case can be hard because:

1. it has long recovery distance after a bad chain
2. it has very tight positive compensation surplus
3. it has many bad windows
4. it is hard under an adversarial neighborhood scan
5. it is a familiar long-trajectory anchor

These are not the same question.

Therefore, different `hardest_n0` values are not contradictions.

## Current metric families

### Frontier recovery hardness

Source:

`results/critical_frontier_summary.json`

Typical hardest case:

`n0 = 9780657630`

This metric emphasizes post-chain recovery distance in the critical frontier scan.

### Compensation-window hardness

Source:

`results/compensation_law_candidate_summary.json`

This metric emphasizes local bad windows and their later finite recovery.

### Adversarial compensation hardness

Source:

`results/adversarial_compensation_summary.json`

Typical hardest case in v1.4:

`n0 = 63728127`

This metric stresses the compensation law against an adversarially generated finite candidate set.

### Tightest positive surplus

This metric asks where the recovery margin gets closest to zero while still remaining positive.

A very small positive surplus is structurally important because it marks near-failure without observed failure.

### Known long-trajectory anchor

Typical reference case:

`n0 = 837799`

This is kept as a familiar comparison point, not as the universal hardest case.

## Generated report

Run:

`python examples/build_hardness_metric_report.py`

Outputs:

`results/hardness_metric_report.json`

`results/hardness_metric_report.md`

## Boundary

This is a finite metric-unification report.

It is not a proof of the Collatz conjecture.
