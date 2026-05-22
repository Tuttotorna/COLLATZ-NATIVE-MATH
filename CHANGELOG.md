# Changelog

## v0.1.0

Initial repository structure.

Added:

- problem-born framing
- Math_Collatz core language
- debt words
- 2-adic shadow
- cheap regeneration chain conjecture
- trace demo
- regeneration scan
- tests
- GitHub Actions CI

## v0.2.0

Added regeneration epoch analysis.

New files:

- docs/REGENERATION_EPOCHS.md
- docs/CHEAPNESS_RATIO.md
- docs/EPOCH_ANALYSIS_NOTES.md
- examples/analyze_regeneration_epochs.py
- tests/test_regeneration_epochs.py
- results/regeneration_epochs_sample.jsonl
- results/regeneration_epochs_summary.json

Core addition:

    regeneration events
    regenerated shadow
    compression cost
    cheapness ratio
    future escape capacity

v0.2 clarifies that local cheap regeneration exists, so the real target is not:

    no cheap regeneration exists

but:

    no infinite cheap regeneration chain exists in positive odd Collatz dynamics.

## v0.3.0

Added cheap regeneration chain analysis.

New files:

- docs/CHAIN_ANALYSIS.md
- docs/CRC_CHAIN_MODEL.md
- docs/CHAIN_RESULTS.md
- examples/analyze_cheap_regeneration_chains.py
- tests/test_cheap_regeneration_chains.py
- results/cheap_regeneration_chains.jsonl
- results/cheap_regeneration_chain_summary.json

Core addition:

    chain-compatible regeneration events
    segment average debt
    debt break detection
    finite cheap regeneration chain diagnostics

v0.3 moves the project from local cheap regeneration to chain sustainability.

The target is now operationally phrased as:

    local cheap regeneration exists,
    but no infinite cheap regeneration chain should exist in positive odd Collatz dynamics.

## v0.4.0

Added chain collapse analysis.

New files:

- docs/CHAIN_COLLAPSE.md
- docs/POST_CHAIN_COMPENSATION.md
- docs/COLLAPSE_RESULTS.md
- examples/analyze_chain_collapse.py
- tests/test_chain_collapse.py
- results/chain_collapse_analysis.jsonl
- results/chain_collapse_summary.json

Core addition:

    chain collapse episodes
    post-chain compensation
    compensation surplus
    collapse cause
    chain length
    chain average debt

v0.4 moves from detecting chain-compatible segments to asking where and why those chains break.

## v0.5.0

Added collapse cause classification.

New files:

- docs/COLLAPSE_CAUSE_CLASSIFICATION.md
- docs/COLLAPSE_MECHANISMS.md
- docs/CLASSIFICATION_RESULTS.md
- examples/analyze_collapse_causes.py
- tests/test_collapse_cause_classification.py
- results/collapse_cause_classification.jsonl
- results/collapse_cause_summary.json

Core addition:

    debt spike classification
    shadow exhaustion classification
    failed regeneration classification
    post-chain overcompensation classification
    terminal descent classification
    primary collapse cause

v0.5 moves from detecting that chains collapse to classifying how they collapse.

## v0.6.0

Added unclassified collapse analysis and refined collapse taxonomy.

New files:

- docs/UNCLASSIFIED_COLLAPSE_ANALYSIS.md
- docs/REFINED_COLLAPSE_TAXONOMY.md
- docs/UNCLASSIFIED_RESULTS.md
- examples/analyze_unclassified_collapses.py
- tests/test_unclassified_collapse_analysis.py
- results/unclassified_collapse_analysis.jsonl
- results/unclassified_collapse_summary.json

Core addition:

    soft_debt_break
    weak_regeneration
    delayed_compensation
    end_of_chain_without_escape
    refined v0.6 primary collapse cause

v0.6 targets the unclassified residue left by v0.5.

## v0.7.0

Added compensation law search.

New files:

- docs/COMPENSATION_LAW_SEARCH.md
- docs/RECOVERY_WINDOW.md
- docs/COMPENSATION_RESULTS.md
- examples/analyze_compensation_law.py
- tests/test_compensation_law_search.py
- results/compensation_law_search.jsonl
- results/compensation_law_summary.json

Core addition:

    chain deficit
    recovery window
    recovery distance
    recovery debt
    recovery surplus
    compensation law candidate search

v0.7 moves from classifying collapse to measuring how fast low-debt chains are compensated.

## v0.8.0

Added post-chain recovery analysis.

New files:

- docs/POST_CHAIN_RECOVERY.md
- docs/RECOVERY_COMPARISON.md
- docs/POST_CHAIN_RESULTS.md
- examples/analyze_post_chain_recovery.py
- tests/test_post_chain_recovery.py
- results/post_chain_recovery_analysis.jsonl
- results/post_chain_recovery_summary.json

Core addition:

    chain-start recovery vs post-chain recovery
    recovery distance gap
    instant post-chain recovery
    post-chain unrecovered episodes

v0.8 corrects v0.7 by measuring recovery after the chain has ended, not only from the chain start.

## v0.9.0

Added hard recovery case analysis.

New files:

- docs/HARD_RECOVERY_CASES.md
- docs/HARDNESS_SCORE.md
- docs/HARD_RECOVERY_RESULTS.md
- examples/analyze_hard_recovery_cases.py
- tests/test_hard_recovery_cases.py
- results/hard_recovery_cases.jsonl
- results/hard_recovery_summary.json

Core addition:

    hardness score
    top hard recovery cases
    longest post-chain recovery cases
    tightest recovery surplus cases
    largest chain deficit cases
    largest recovery gap cases

v0.9 identifies the structurally hardest recovered compensation cases.

## v1.0.0

Added critical case dissection.

New files:

- docs/CRITICAL_CASE_DISSECTION.md
- docs/CRITICAL_CASE_RESULTS.md
- docs/CRITICAL_PATTERN_NOTES.md
- examples/analyze_critical_case.py
- tests/test_critical_case.py
- results/critical_case_dissection.json
- results/critical_case_blocks.jsonl
- results/critical_case_window.jsonl
- results/critical_case_summary.json

Core addition:

    hard case n0 = 9780657630
    block-by-block post-chain recovery window
    first crossing above log2(3)
    focused debt word
    recovery surplus dissection
    critical pattern notes

v1.0 turns the hardest sampled recovered case into a concrete object for inspection.

## v1.1.0

Added critical frontier scan.

New files:

- docs/CRITICAL_FRONTIER_SCAN.md
- docs/FRONTIER_RESULTS.md
- docs/FRONTIER_LIMITS.md
- examples/scan_critical_frontier.py
- tests/test_critical_frontier_scan.py
- results/critical_frontier_scan.jsonl
- results/critical_frontier_summary.json

Core addition:

    bounded frontier scan around hard cases
    local neighborhood scan around known frontier centers
    structured near-Mersenne candidates
    automatic hardest-case ranking
    automatic comparison against the v1.0 critical case

v1.1 tests whether the v1.0 hard case is isolated or part of a wider frontier.

## v1.2 - Frontier stability certificate exact baseline

- Preserves the v1.1 critical frontier scanner as deterministic core.
- Adds a v1.2 wrapper that emits a frontier stability certificate.
- Uses the exact previous critical hardness baseline: 15.100955299032181.
- Avoids false HARDER_THAN_PREVIOUS classification caused by rounded baseline 15.100955.
- Records comparison_status, frontier_stable, and harder_than_previous_critical.
- Adds regression tests for exact frontier stability.

## v1.3 - Compensation law candidate

- Adds a finite compensation-law candidate scanner.
- Detects maximal bad debt windows where average debt is below log2(3).
- Searches shortest post-window recovery restoring the combined average to log2(3).
- Emits a finite compensation-law candidate certificate.
- Adds regression tests for the v1.3 outputs.

## v1.4 - Adversarial compensation scan

- Adds an adversarial scanner for the compensation-law candidate.
- Expands around known hard cases using local neighborhoods, powers-of-two offsets, and bit-flip perturbations.
- Searches for unrecovered bad compensation windows.
- Emits finite rows, summary, and certificate artifacts.
- Adds regression tests for the adversarial certificate.

## v1.5 - Hardness metric report

- Adds a metric-unification report for Collatz hardness.
- Separates frontier recovery hardness, compensation-window hardness, adversarial compensation hardness, tightest surplus, and known trajectory anchors.
- Adds `examples/build_hardness_metric_report.py`.
- Adds `docs/HARDNESS_METRICS.md`.
- Adds generated reports in `results/hardness_metric_report.json` and `results/hardness_metric_report.md`.
- Adds regression tests proving that multiple hardest cases are not treated as contradictions.

## v1.5.1 - Fix tightest positive surplus extraction

- Fixes `tightest_positive_surplus` in the hardness metric report.
- Ensures the metric extracts a real positive value instead of `None`.
- Adds regression coverage for the expected current value:
  `n0 = 63728127`, `min_surplus = 1.7736432994075457e-05`.

## v1.6 - Native Method Boundary

- Adds a native-method boundary layer.
- Separates native method from computational evidence.
- Defines native primitives: debt, discharge, shadow, regeneration, compensation, obstruction candidate, and native closure.
- Adds a standard translation boundary.
- Clarifies that previous scans are evidence layers, not the native theory itself.
- Defines the next research step as v1.7 Native Obstruction Model.
